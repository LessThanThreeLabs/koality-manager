import argparse

import os

from manager.shared import koality_root
from manager.shared.script import Script, ShellScript
from scripts import package_scripts


class Packager(object):
	version = '0.1.5'
	packaged_directory = os.path.abspath(os.path.join(koality_root, os.pardir, version))

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
			return '''
				rm -rf %s
				cp -r %s %s
				rm -rf %s
				rm -rf %s
			''' % (Packager.packaged_directory,
				koality_root,
				Packager.packaged_directory,
				os.path.join(Packager.packaged_directory, 'manager', 'package'),
				os.path.join(Packager.packaged_directory, '.git'))


	class AddUpgradeRevertScript(Script):
		@classmethod
		def run(cls):
			upgrade_script_path = os.path.join(Packager.packaged_directory, 'upgrade_script')
			with open(upgrade_script_path, 'w') as upgrade_script:
				upgrade_script.write('sudo $(dirname $0)/koality.py upgrade')
				os.chmod(upgrade_script_path, 0777)
			revert_script_path = os.path.join(Packager.packaged_directory, 'revert_script')
			with open(revert_script_path, 'w') as revert_script:
				revert_script.write('true')
				os.chmod(revert_script_path, 0777)
			return True


	class TarScript(ShellScript):
		@classmethod
		def get_script(cls):
			return '''
				tar -czf %s %s
				rm -rf %s
			''' % (os.path.join(koality_root, os.pardir, 'koality-%s.tar.gz' % Packager.version),
				Packager.packaged_directory,
				Packager.packaged_directory)


class ScriptFailedException(Exception):
	pass
