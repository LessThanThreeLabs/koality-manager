import os

from manager.shared import koality_root, conf_directory, dependencies_directory
from manager.shared.script import ShellScript


class DependenciesInstallScript(ShellScript):
	_dependencies = (
		'make',
		'git',
		'python-software-properties',
		'build-essential',
		'libyaml-dev',
		'python-dev',
		'python-pip'
	)

	@classmethod
	def get_script(cls):
		return cls.multiline(
			'apt-get update',
			'apt-get install -y %s' % ' '.join(cls._dependencies)
		)


class CircusInstallScript(ShellScript):
	@classmethod
	def get_script(cls):
		return 'pip install circus'


class JavaInstallScript(ShellScript):
	@classmethod
	def get_script(cls):
		return cls.multiline(
			"if [ ! -d '/usr/lib/jvm/java-6-sun' ]; then",
			'	cd %s' % os.path.join(dependencies_directory, 'java'),
			'	./oab-java.sh',
			'	add-apt-repository -y ppa:flexiondotorg/java',
			'	apt-get update',
			'	apt-get install -y sun-java6-jdk maven',
			'fi'
		)


class HaproxyInstallScript(ShellScript):
	@classmethod
	def get_script(cls):
		return cls.multiline(
			'if [ ! "$(which haproxy)" ]; then',
			'	cd %s' % os.path.join(dependencies_directory, 'haproxy'),
			'	make clean',
			'	make install USE_OPENSSL=1 -j 4',
			'fi',
			'cd %s' % os.path.join(conf_directory, 'haproxy'),
			"sed -i.bak -r 's!( crt ).+( ciphers )!\\1%s\\2!g' haproxy.conf" % os.path.join('/etc', 'koality', 'cert', 'server.pem')
		)


class RabbitmqInstallScript(ShellScript):
	@classmethod
	def get_script(cls):
		return cls.multiline(
			'apt-get install -y rabbitmq-server',
			'dpkg -i %s' % os.path.join(dependencies_directory, 'rabbitmq-server.deb'),
			'mkdir /etc/rabbitmq/rabbitmq.conf.d',
			'rabbitmq-plugins enable rabbitmq_management',
			'service rabbitmq-server restart',
			'wget --http-user=guest --http-password=guest localhost:55672/cli/rabbitmqadmin',
			'chmod +x rabbitmqadmin',
			'mv rabbitmqadmin /usr/local/bin/rabbitmqadmin'
		)


class RedisInstallScript(ShellScript):
	@classmethod
	def get_script(cls):
		return cls.multiline(
			'if [ ! "$(which redis-server)" ]; then',
			'	cd %s' % os.path.join(dependencies_directory, 'redis'),
			'	make',
			'	make install',
			'	rm -f %s/*' % os.path.join(koality_root, 'db', 'redis'),
			'	chmod a+w %s' % os.path.join(koality_root, 'db', 'redis'),
			'fi'
		)


class PostgresInstallScript(ShellScript):
	@classmethod
	def get_script(cls):
		return cls.multiline(
			'apt-get install -y postgresql libpq-dev',
			"sed -i.bak -r 's/^(\\w+(\\s+\\S+){2,3}\\s+)\\w+$/\\1trust/g' /etc/postgresql/9.1/main/pg_hba.conf",
			"sed -i.bak -r 's/^.*fsync .*$/fsync off/g' /etc/postgresql/9.1/main/postgresql.conf",
			'service postgresql restart',
		)
