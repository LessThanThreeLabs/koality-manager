import os

from manager.install import Installer
from manager.shared import upgrade_directory, python_bin_directory
from manager.shared.script import ShellScript


class Upgrader(object):
	def run(self, restart=True):
		try:
			self._run_with_exceptions(KoalityShutdownScript)
			Installer().run()
			self._run_with_exceptions(DatabaseMigrateScript)
		finally:
			if restart:
				self._run_with_exceptions(KoalityStartupScript)

	def _run_with_exceptions(self, script):
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
		alembic_bin = os.path.join(python_bin_directory, 'alembic')
		return cls.multiline(
			'cd %s' % os.path.join(upgrade_directory, 'alembic'),
			"database_version=$(%s current --head-only 2>/dev/null | awk '{print $1}')" % alembic_bin,
			'r=0',
			'while [ "$r" -eq "0" ]; do',
			'	sudo -u lt3 %s upgrade +1' % alembic_bin,
			'	r=$?',
			'done',
			'if [ "$r" -ne "255" ]; then',
			'	%s downgrade $database_version' % alembic_bin,
			'	exit $r',
			'fi'
		)


class KoalityStartupScript(ShellScript):
	@classmethod
	def get_script(cls):
		return 'service koality start'


class ScriptFailedException(Exception):
	pass
