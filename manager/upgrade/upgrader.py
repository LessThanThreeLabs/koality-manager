import os
import shutil

from manager.install import Installer
from manager.shared import upgrade_directory, python_bin_directory, node_directory
from manager.shared.script import Script, ShellScript


class Upgrader(object):
	def run(self, restart=True):
		try:
			self._run_with_exceptions(KoalityShutdownScript)
			Installer().run()
			self._run_with_exceptions(DatabaseMigrateScript)
			CopyRedisScript.run()
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
			'sudo -u lt3 %s upgrade head' % alembic_bin
		)


class CopyRedisScript(Script):
	@classmethod
	def run(cls):
		old_redis_dir = os.path.realpath(os.path.join('/etc', 'koality', 'oldroot', 'node', 'webserver', 'redis', 'db'))
		new_redis_dir = os.path.abspath(os.path.join(node_directory, 'webserver', 'redis', 'db'))
		for filename in os.listdir(old_redis_dir):
			if os.path.isfile(os.path.join(old_redis_dir, filename)):
				shutil.copy(os.path.join(old_redis_dir, filename), os.path.join(new_redis_dir, filename))
		return True


class KoalityStartupScript(ShellScript):
	@classmethod
	def get_script(cls):
		return 'service koality start'


class ScriptFailedException(Exception):
	pass
