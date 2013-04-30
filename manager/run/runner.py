import os

from circus.arbiter import Arbiter
from circus.watcher import Watcher

from manager.shared import conf_directory, python_bin_directory


class Runner(object):
	def __init__(self):
		self._koality_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
		self._watchers = [
			# REDIS
			Watcher(
				name='redis-repostore',
				cmd='redis-server',
				args=[os.path.join(conf_directory, 'redis', 'filesystem_repo_server_redis.conf')],
				user='lt3',
				priority=0
			),
			Watcher(
				name='redis-sessionStore',
				cmd='redis-server',
				args=[os.path.join(conf_directory, 'redis', 'sesssionStoreRedis.conf')],
				user='lt3',
				priority=0
			),
			Watcher(
				name='redis-createAccount',
				cmd='redis-server',
				args=[os.path.join(conf_directory, 'redis', 'createAccountRedis.conf')],
				user='lt3',
				priority=0
			),
			Watcher(
				name='redis-createRepository',
				cmd='redis-server',
				args=[os.path.join(conf_directory, 'redis', 'createRepositoryRedis.conf')],
				user='lt3',
				priority=0
			),
			# HAPROXY
			Watcher(
				name='haproxy',
				cmd='haproxy',
				args=['-f', os.path.join(conf_directory, 'haproxy', 'haproxy.conf')],
				user='root',
				priority=0
			),
			# PLATFORM
			Watcher(
				name='model_server',
				cmd=self._python_bin('koality-start-model-server'),
				working_dir='/tmp/model_server',
				user='lt3',
				env={'HOME': '/home/lt3'},
				priority=1
			),
			Watcher(
				name='verification_server',
				cmd=self._python_bin('koality-start-verification-server'),
				args=['--type', 'aws', '--cleanup'],
				working_dir='/verification/server',
				user='verification',
				env={'HOME': '/home/verification'},
				priority=2
			),
			Watcher(
				name='ec2_snapshotter',
				cmd=self._python_bin('koality-ec2-snapshotter'),
				args=['--daemon'],
				working_dir='/verification/snapshotter',
				user='verification',
				env={'HOME': '/home/verification'},
				priority=2
			),
			Watcher(
				name='filesystem_repo_server',
				cmd=self._python_bin('koality-filesystem-repo-server'),
				args=['-r', '/git/repositories'],
				user='git',
				env={'HOME': '/home/git'},
				priority=2
			),
			# WEB SERVER
			Watcher(
				name='webserver',
				cmd='some path to node',  # TODO: FIX
				args=['--harmony', 'js/index.js', '--httpsPort', '10443', '--mode', 'production'],
				user='lt3',
				env={'HOME': '/home/lt3'},
				priority=2
			),
			# API SERVER
			Watcher(
				name='api-server',
				cmd='some path to node',  # TODO: FIX
				args=['--harmony', 'js/index.js', '--httpsPort', '10443', '--mode', 'production'],
				user='lt3',
				env={'HOME': '/home/lt3'},
				priority=2
			)
		]
		self.watchers = [Watcher]

	def _python_bin(self, bin_name):
		return os.path.join(python_bin_directory, bin_name)

	def run(self):
		arbiter = Arbiter(self._watchers, 'tcp://127.0.0.1:5555', 'tcp://127.0.0.1:5556', debug=True)
		try:
			arbiter.start()
		finally:
			arbiter.stop()
