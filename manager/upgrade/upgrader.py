import os

from manager.install import Installer
from manager.shared import upgrade_directory
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
			alembic upgrade head
		''' % os.path.join(upgrade_directory, 'alembic')


class KoalityStartupScript(ShellScript):
	@classmethod
	def get_script(cls):
		return 'service koality start'


class ScriptFailedException(Exception):
	pass
