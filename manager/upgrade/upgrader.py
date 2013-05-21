import os

from manager.install import Installer
from manager.shared import upgrade_directory, python_bin_directory
from manager.shared.script import ShellScript


class Upgrader(object):
	def run(self):
		try:
			self._run_with_exceptions([KoalityShutdownScript, DatabaseMigrateScript])
			Installer().run()
		finally:
			self._run_with_exceptions([KoalityStartupScript])

	def _run_with_exceptions(self, scripts):
		for script in scripts:
			if not script.run():
				raise ScriptFailedException(script)
		return True


class KoalityShutdownScript(ShellScript):
	@classmethod
	def get_script(cls):
		return 'service koality stop || true'


class DatabaseMigrateScript(ShellScript):
	@classmethod
	def get_script(cls):
		return '''
			cd %s
			r=0
			while [ "$r" -eq "0" ]; do
				sudo -u lt3 %s upgrade +1
				r=$?
			done
			if [ "$r" -ne "255" ]; then
				exit $r
			fi
		''' % (os.path.join(upgrade_directory, 'alembic'),
			os.path.join(python_bin_directory, 'alembic'))


class KoalityStartupScript(ShellScript):
	@classmethod
	def get_script(cls):
		return 'service koality start'


class ScriptFailedException(Exception):
	pass
