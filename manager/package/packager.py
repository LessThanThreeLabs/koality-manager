import argparse

import os

from manager.shared import koality_root
from manager.shared.script import Script, ShellScript
from scripts import package_scripts


class Packager(object):
	version = '0.1.5'
	packaged_directory = os.path.join('/tmp', 'koality', version)
	internal_packaged_directory = os.path.abspath(os.path.join(packaged_directory, 'koality'))

	def run(self, installable=False):
		self._run_with_exceptions(package_scripts)

		if installable:
			self._run_with_exceptions([Packager.RepackageScript, Packager.AddUpgradeRevertScript, Packager.TarScript])

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
				'rm -rf %s' % os.path.join(Packager.internal_packaged_directory, '.git')
			)


	class AddUpgradeRevertScript(Script):
		@classmethod
		def run(cls):
			upgrade_script_path = os.path.join(Packager.packaged_directory, 'upgrade_script')
			with open(upgrade_script_path, 'w') as upgrade_script:
				upgrade_script.write(ShellScript.multiline(
					'#!/bin/sh',
					'cd $(dirname $0)',
					'oldroot=$(readlink -f /etc/koality/root)',
					'newroot=$(readlink -m $oldroot/../%s)' % Packager.version,
					'if [ -e "$oldroot" ]; then'
					'	rm -rf $oldroot.bak',
					'	mv $oldroot $oldroot.bak',
					'fi',
					'mv koality $newroot',
					'cd $newroot',
					'sudo ./koality.py upgrade'
				))
				os.chmod(upgrade_script_path, 0777)
			revert_script_path = os.path.join(Packager.packaged_directory, 'revert_script')
			with open(revert_script_path, 'w') as revert_script:
				revert_script.write(ShellScript.multiline(
					'#!/bin/sh',
					'true'
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


class ScriptFailedException(Exception):
	pass
