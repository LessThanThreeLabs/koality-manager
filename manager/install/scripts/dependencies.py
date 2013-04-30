import os

from manager.shared import dependencies_directory
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
		return 'apt-get install -y %s' % ' '.join(cls._dependencies)


class CircusInstallScript(ShellScript):
	@classmethod
	def get_script(cls):
		return 'pip install circus'


class JavaInstallScript(ShellScript):
	@classmethod
	def get_script(cls):
		return '''
			if [ ! -d '/usr/lib/jvm/java-6-sun' ]; then
				cd %s
				./oab-java.sh
				add-apt-repository -y ppa:flexiondotorg/java
				apt-get update
				apt-get install -y sun-java6-jdk maven
			fi
		''' % os.path.join(dependencies_directory, 'java')


class HaproxyInstallScript(ShellScript):
	@classmethod
	def get_script(cls):
		return '''
			cd %s
			make clean
			make install USE_OPENSSL=1 -j 4
		''' % os.path.join(dependencies_directory, 'haproxy')


class RabbitmqInstallScript(ShellScript):
	@classmethod
	def get_script(cls):
		return '''
			apt-get install -y rabbitmq-server
			dpkg -i %s
			mkdir /etc/rabbitmq/rabbitmq.conf.d
			rabbitmq-plugins enable rabbitmq_management
			service rabbitmq-server restart
			wget --http-user=guest --http-password=guest localhost:55672/cli/rabbitmqadmin
			chmod +x rabbitmqadmin
			mv rabbitmqadmin /usr/local/bin/rabbitmqadmin
		''' % os.path.join(dependencies_directory, 'rabbitmq-server.deb')


class RedisInstallScript(ShellScript):
	@classmethod
	def get_script(cls):
		return '''
			cd %s
			make
			make install
		''' % os.path.join(dependencies_directory, 'redis')


class PostgresInstallScript(ShellScript):
	@classmethod
	def get_script(cls):
		return '''
			apt-get install -y postgresql libpq-dev
			sed -i.bak -r 's/^.*fsync .*$/fsync off/g' /etc/postgresql/9.1/main/postgresql.conf
			service postgresql restart
		'''
