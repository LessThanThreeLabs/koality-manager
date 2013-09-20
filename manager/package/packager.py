import os

from manager.shared import koality_root
from manager.shared.script import Script, ShellScript
from scripts import package_scripts


class Packager(object):
	version = '0.4.5-internal-1'
	packaged_directory = os.path.join('/tmp', 'koality', version)
	internal_packaged_directory = os.path.abspath(os.path.join(packaged_directory, 'koality'))

	def run(self, publish=True):
		self._run_with_exceptions(package_scripts)
		self._run_with_exceptions([Packager.RepackageScript, Packager.AddInstallationScripts, Packager.TarScript])
		if publish:
			self._run_with_exceptions([Packager.PublishScript])

	def _run_with_exceptions(self, scripts):
		for script in scripts:
			if not script.run():
				raise ScriptFailedException(script)
		return True

	class RepackageScript(ShellScript):
		@classmethod
		def get_script(cls):
			return cls.multiline(
				'rm -rf %s' % Packager.packaged_directory,
				'mkdir -p %s' % Packager.packaged_directory,
				'cp -r %s %s' % (koality_root, Packager.internal_packaged_directory),
				'rm -rf %s' % os.path.join(Packager.internal_packaged_directory, 'manager', 'package'),
				'rm -rf %s' % os.path.join(Packager.internal_packaged_directory, 'dependencies', 'cached'),
				'rm -rf %s' % os.path.join(Packager.internal_packaged_directory, '.git')
			)

	class AddInstallationScripts(Script):
		@classmethod
		def run(cls):
			install_script_path = os.path.join(Packager.packaged_directory, 'install_script')
			with open(install_script_path, 'w') as install_script:
				install_script.write(ShellScript.multiline(
					'#!/bin/sh',
					'cd $(dirname $0)',
					'mv koality/* .',
					'rm koality/.*',
					'rmdir koality',
					'sudo ./koality.py install'
				))
				os.chmod(install_script_path, 0777)
			upgrade_script_path = os.path.join(Packager.packaged_directory, 'upgrade_script')
			with open(upgrade_script_path, 'w') as upgrade_script:
				upgrade_script.write(ShellScript.multiline(
					'#!/bin/sh',
					'cd $(dirname $0)',
					'oldroot=$(readlink -f /etc/koality/root)',
					'newroot=$(readlink -m $oldroot/../%s)' % Packager.version,
					'sudo chown -R lt3:lt3 $oldroot/..',
					'sudo rm /etc/koality/oldroot',
					'if [ -e "$newroot" ]; then',
					'	rm -rf $newroot.bak',
					'	mv $newroot $newroot.bak',
					'   sudo ln -s $newroot.bak /etc/koality/oldroot',
					'else',
					'   sudo ln -s $oldroot /etc/koality/oldroot',
					'fi',
					'mv koality $newroot',
					'cd $newroot',
					'sudo ./koality.py upgrade > $(dirname $0)/upgrade.log 2>&1'
				))
				os.chmod(upgrade_script_path, 0777)
			revert_script_path = os.path.join(Packager.packaged_directory, 'revert_script')
			with open(revert_script_path, 'w') as revert_script:
				revert_script.write(ShellScript.multiline(
					'#!/bin/sh',
					'koalityroot=$(readlink -f /etc/koality/root)',
					'oldroot=$(readlink -f /etc/koality/oldroot)',
					'if [ -e "${koalityroot}.bak" ]; then',
					'   mv "$koalityroot" "${koalityroot}.bak2"',
					'   mv "${koalityroot}.bak" "$koalityroot"',
					'   cd $koalityroot',
					'else',
					'   cd $oldroot',
					'fi',
					'sudo ./koality.py install > $(dirname $0)/revert.log 2>&1',
					'sudo service koality restart'
				))
				os.chmod(revert_script_path, 0777)
			return True

	class TarScript(ShellScript):
		@classmethod
		def get_script(cls):
			tarfile = 'koality-%s.tar.gz' % Packager.version
			return cls.multiline(
				'cd %s' % os.path.join(Packager.packaged_directory, os.pardir),
				'tar -czf %s %s' % (
					tarfile,
					Packager.version
				),
				'rm -rf %s' % Packager.packaged_directory,
				'mv %s %s' % (
					tarfile,
					os.path.join(koality_root, os.pardir)
				)
			)

	class PublishScript(ShellScript):
		@classmethod
		def get_script(cls):
			tarfile = 'koality-%s.tar.gz' % Packager.version
			return cls.multiline(
				'cd %s' % os.path.join(koality_root, os.pardir),
				's3cmd put %s s3://koality_release/upgrade/%s' % (tarfile, tarfile)
			)


class ScriptFailedException(Exception):
	pass
