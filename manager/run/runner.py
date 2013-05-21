import os
import pwd

from circus.arbiter import Arbiter
from circus.watcher import Watcher

from manager.shared import conf_directory, dependencies_directory, koality_root, node_directory, nvm_directory, python_bin_directory
from manager.shared.script import ShellScript


class Runner(object):
	def __init__(self):
		try:
			git = pwd.getpwnam('git')
			lt3 = pwd.getpwnam('lt3')
			root = pwd.getpwnam('root')
			verification = pwd.getpwnam('verification')
		except:
			raise Exception("Koality must be installed before it can be run")

		self._watchers = [
			# REDIS
			Watcher(
				name='redis-repostore',
				cmd='/usr/local/bin/redis-server',
				args=[os.path.join(conf_directory, 'redis', 'filesystem_repo_server_redis.conf')],
				working_dir=koality_root,
				stdout_stream={'filename': os.path.join(koality_root, 'log', 'redis_repostore_stdout.log')},
				stderr_stream={'filename': os.path.join(koality_root, 'log', 'redis_repostore_stderr.log')},
				uid=lt3[2],
				gid=lt3[3],
				copy_env=True,
				copy_path=True,
				priority=0
			),
			Watcher(
				name='redis-sessionStore',
				cmd='/usr/local/bin/redis-server',
				args=[os.path.join(node_directory, 'webserver', 'redis', 'conf', 'sessionStoreRedis.conf')],
				working_dir=os.path.join(node_directory, 'webserver'),
				stdout_stream={'filename': os.path.join(koality_root, 'log', 'redis_sessionStore_stdout.log')},
				stderr_stream={'filename': os.path.join(koality_root, 'log', 'redis_sessionStore_stderr.log')},
				uid=lt3[2],
				gid=lt3[3],
				copy_env=True,
				copy_path=True,
				priority=0
			),
			Watcher(
				name='redis-createAccount',
				cmd='/usr/local/bin/redis-server',
				args=[os.path.join(node_directory, 'webserver', 'redis', 'conf', 'createAccountRedis.conf')],
				working_dir=os.path.join(node_directory, 'webserver'),
				stdout_stream={'filename': os.path.join(koality_root, 'log', 'redis_createAccount_stdout.log')},
				stderr_stream={'filename': os.path.join(koality_root, 'log', 'redis_createAccount_stderr.log')},
				uid=lt3[2],
				gid=lt3[3],
				copy_env=True,
				copy_path=True,
				priority=0
			),
			Watcher(
				name='redis-createRepository',
				cmd='/usr/local/bin/redis-server',
				args=[os.path.join(node_directory, 'webserver', 'redis', 'conf', 'createRepositoryRedis.conf')],
				working_dir=os.path.join(node_directory, 'webserver'),
				stdout_stream={'filename': os.path.join(koality_root, 'log', 'redis_createRepository_stdout.log')},
				stderr_stream={'filename': os.path.join(koality_root, 'log', 'redis_createRepository_stderr.log')},
				uid=lt3[2],
				gid=lt3[3],
				copy_env=True,
				copy_path=True,
				priority=0
			),
			# HAPROXY
			Watcher(
				name='haproxy',
				cmd='/usr/local/sbin/haproxy',
				args=['-f', os.path.join(conf_directory, 'haproxy', 'haproxy.conf')],
				stdout_stream={'filename': os.path.join(koality_root, 'log', 'haproxy_stdout.log')},
				stderr_stream={'filename': os.path.join(koality_root, 'log', 'haproxy_stderr.log')},
				uid=root[2],
				gid=root[3],
				copy_env=True,
				copy_path=True,
				priority=0
			),
			# PLATFORM
			Watcher(
				name='model_server',
				cmd=self._python_bin('koality-start-model-server'),
				working_dir='/tmp/model_server',
				stdout_stream={'filename': os.path.join(koality_root, 'log', 'model_server_stdout.log')},
				stderr_stream={'filename': os.path.join(koality_root, 'log', 'model_server_stderr.log')},
				uid=lt3[2],
				gid=lt3[3],
				env={'HOME': lt3[5]},
				copy_env=True,
				copy_path=True,
				priority=1
			),
			Watcher(
				name='verification_server',
				cmd=self._python_bin('koality-start-verification-server'),
				args=['--type', 'aws', '--cleanup'],
				working_dir='/verification/server',
				stdout_stream={'filename': os.path.join(koality_root, 'log', 'verification_server_stdout.log')},
				stderr_stream={'filename': os.path.join(koality_root, 'log', 'verification_server_stderr.log')},
				uid=verification[2],
				gid=verification[3],
				env={'HOME': verification[5]},
				copy_env=True,
				copy_path=True,
				priority=2
			),
			Watcher(
				name='ec2_snapshotter',
				cmd=self._python_bin('koality-ec2-snapshotter'),
				args=['--daemon'],
				working_dir='/verification/snapshotter',
				stdout_stream={'filename': os.path.join(koality_root, 'log', 'ec2_snapshotter_stdout.log')},
				stderr_stream={'filename': os.path.join(koality_root, 'log', 'ec2_snapshotter_stderr.log')},
				uid=verification[2],
				gid=verification[3],
				env={'HOME': verification[5]},
				copy_env=True,
				copy_path=True,
				priority=2
			),
			Watcher(
				name='filesystem_repo_server',
				cmd=self._python_bin('koality-start-filesystem-repo-server'),
				args=['-r', '/git/repositories'],
				working_dir='/git',
				stdout_stream={'filename': os.path.join(koality_root, 'log', 'filesystem_repo_server_stdout.log')},
				stderr_stream={'filename': os.path.join(koality_root, 'log', 'filesystem_repo_server_stderr.log')},
				uid=git[2],
				gid=git[3],
				env={'HOME': git[5]},
				copy_env=True,
				copy_path=True,
				priority=2
			),
			# WEB SERVER
			Watcher(
				name='webserver',
				cmd=os.path.join(nvm_directory, 'v0.8.12', 'bin', 'node'),
				args=['--harmony', os.path.join(node_directory, 'webserver', 'libs', 'index.js'), '--httpPort', '1080', '--mode', 'production'],
				working_dir=os.path.join(node_directory, 'webserver'),
				stdout_stream={'filename': os.path.join(koality_root, 'log', 'webserver_stdout.log')},
				stderr_stream={'filename': os.path.join(koality_root, 'log', 'webserver_stderr.log')},
				uid=lt3[2],
				gid=lt3[3],
				env={'HOME': lt3[5]},
				copy_env=True,
				copy_path=True,
				priority=2
			),
		]

	def _python_bin(self, bin_name):
		return os.path.join(python_bin_directory, bin_name)

	def run(self):
		if not Runner.TmpDirCreationScript.run():
			raise Exception('/tmp appears to be inaccessible.')
		if not Runner.RabbitmqSetupScript.run():
			raise Exception('Unable to configure rabbitmq.')
		if not Runner.OpenSshLaunchScript.run():
			raise Exception('''Could not launch openssh daemon.
				Check your system before logging out or this machine may become inaccessible.''')
		if not Runner.HaproxyCertGenerationScript.run():
			raise Exception('Could not verify or create openssl certificate')
		arbiter = Arbiter(self._watchers, 'tcp://127.0.0.1:5555', 'tcp://127.0.0.1:5556', debug=True)
		try:
			arbiter.start()
		finally:
			arbiter.stop()

	class TmpDirCreationScript(ShellScript):
		@classmethod
		def get_script(cls):
			return '''
				mkdir -p /tmp/model_server
				chmod 0777 /tmp/model_server
			'''

	class RabbitmqSetupScript(ShellScript):
		@classmethod
		def get_script(cls):
			return os.path.join(dependencies_directory, 'rabbitmq_setup.sh')

	class OpenSshLaunchScript(ShellScript):
		_move_standard_daemon_script = '''
			service ssh stop 2> /dev/null
			/usr/sbin/sshd -p 2222
		'''

		_modified_daemon_command = '/usr/local/sbin/sshd -f /usr/local/etc/sshd_config'
		# The '^' prevents pkill from killing itself (full regexp capabilities in pkill)
		_start_modified_daemon_script = '''
			pkill '^%s'
			%s
		''' % (_modified_daemon_command, _modified_daemon_command)

		@classmethod
		def get_script(cls):
			return '\n'.join((
				cls._move_standard_daemon_script,
				cls._start_modified_daemon_script
			))

	class HaproxyCertGenerationScript(ShellScript):
		@classmethod
		def get_script(cls):
			cert_directory = os.path.join('/etc/', 'koality', 'cert')
			return cls.multiline(
				'if [ ! -f %s ]; then' % os.path.join(cert_directory, 'server.pem'),
				'	mkdir -p %s' % cert_directory,
				'	cd %s' % cert_directory,
				'	rm -f *',
				'	openssl req -nodes -newkey rsa:2048 -keyout server.key -out server.csr -subj "/C=US/ST=CA/L=San Francisco/O=Koality/OU=Koality/CN=*.koalitycode.com"',
				'	openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt',
				'	cat server.key server.crt > server.pem',
				'fi'
			)
