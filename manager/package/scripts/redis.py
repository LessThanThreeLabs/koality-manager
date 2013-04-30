from manager.shared import dependencies_directory
from manager.shared.script import ShellScript


class RedisPackageScript(ShellScript):
	@classmethod
	def get_script(cls):
		return '''
			cd %s
			wget http://redis.googlecode.com/files/redis-2.6.10.tar.gz
			tar xzf redis-2.6.10.tar.gz
			mv redis-2.6.10 redis
			rm redis-2.6.10.tar.gz
		''' % dependencies_directory
