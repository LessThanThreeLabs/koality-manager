import os
import pwd

from circus.arbiter import Arbiter
from circus.watcher import Watcher

from manager.shared import conf_directory, node_directory, nvm_directory, python_bin_directory


class Runner(object):
	def __init__(self):
		self._koality_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))

		git = pwd.getpwnam('git')
		lt3 = pwd.getpwnam('lt3')
		root = pwd.getpwnam('root')
		verification = pwd.getpwnam('verification')

		self._watchers = [
			# REDIS
			Watcher(
				name='redis-repostore',
				cmd='/usr/local/bin/redis-server',
				args=[os.path.join(conf_directory, 'redis', 'filesystem_repo_server_redis.conf')],
				working_dir=self._koality_root,
				uid=lt3[2],
				gid=lt3[3],
				priority=0
			),
			Watcher(
				name='redis-sessionStore',
				cmd='/usr/local/bin/redis-server',
				args=[os.path.join(self._koality_root, 'node', 'webserver', 'redis', 'sesssionStoreRedis.conf')],
				working_dir=self._koality_root,
				uid=lt3[2],
				gid=lt3[3],
				priority=0
			),
			Watcher(
				name='redis-createAccount',
				cmd='/usr/local/bin/redis-server',
				args=[os.path.join(self._koality_root, 'node', 'webserver', 'redis', 'createAccountRedis.conf')],
				working_dir=self._koality_root,
				uid=lt3[2],
				gid=lt3[3],
				priority=0
			),
			Watcher(
				name='redis-createRepository',
				cmd='/usr/local/bin/redis-server',
				args=[os.path.join(self._koality_root, 'node', 'webserver', 'redis', 'createRepositoryRedis.conf')],
				working_dir=self._koality_root,
				uid=lt3[2],
				gid=lt3[3],
				priority=0
			),
			# HAPROXY
			Watcher(
				name='haproxy',
				cmd='/usr/local/sbin/haproxy',
				args=['-f', os.path.join(conf_directory, 'haproxy', 'haproxy.conf')],
				uid=root[2],
				gid=root[3],
				priority=0
			),
			# PLATFORM
			Watcher(
				name='model_server',
				cmd=self._python_bin('koality-start-model-server'),
				working_dir='/tmp/model_server',
				uid=lt3[2],
				gid=lt3[3],
				env={'HOME': lt3[5]},
				priority=1
			),
			Watcher(
				name='verification_server',
				cmd=self._python_bin('koality-start-verification-server'),
				args=['--type', 'aws', '--cleanup'],
				working_dir='/verification/server',
				uid=verification[2],
				gid=verification[3],
				env={'HOME': verification[5]},
				priority=2
			),
			Watcher(
				name='ec2_snapshotter',
				cmd=self._python_bin('koality-ec2-snapshotter'),
				args=['--daemon'],
				working_dir='/verification/snapshotter',
				uid=verification[2],
				gid=verification[3],
				env={'HOME': verification[5]},
				priority=2
			),
			Watcher(
				name='filesystem_repo_server',
				cmd=self._python_bin('koality-start-filesystem-repo-server'),
				args=['-r', '/git/repositories'],
				uid=git[2],
				gid=git[3],
				env={'HOME': git[5]},
				priority=2
			),
			# WEB SERVER
			Watcher(
				name='webserver',
				cmd=os.path.join(nvm_directory, 'v0.8.12', 'bin', 'node'),
				args=['--harmony', os.path.join(node_directory, 'webserver', 'libs', 'index.js'), '--httpsPort', '10443', '--mode', 'production'],
				working_dir=os.path.join(node_directory, 'webserver'),
				uid=lt3[2],
				gid=lt3[3],
				env={'HOME': lt3[5]},
				priority=2
			),
			# API SERVER
			Watcher(
				name='api-server',
				cmd=os.path.join(nvm_directory, 'v0.8.12', 'bin', 'node'),
				args=['--harmony', os.path.join(node_directory, 'api-server', 'libs', 'index.js'), '--httpsPort', '10443', '--mode', 'production'],
				working_dir=os.path.join(node_directory, 'api-server'),
				uid=lt3[2],
				gid=lt3[3],
				env={'HOME': lt3[5]},
				priority=2
			)
		]

	def _python_bin(self, bin_name):
		return os.path.join(python_bin_directory, bin_name)

	def run(self):
		arbiter = Arbiter(self._watchers, 'tcp://127.0.0.1:5555', 'tcp://127.0.0.1:5556', debug=True)
		try:
			arbiter.start()
		finally:
			arbiter.stop()
