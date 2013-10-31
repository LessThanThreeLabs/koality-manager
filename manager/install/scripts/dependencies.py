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
		'python-pip',
		'openssl',
		'libpcre3-dev'
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
		return 'pip install circus==0.7.1'


class JavaInstallScript(ShellScript):
	@classmethod
	def get_script(cls):
		return cls.multiline(
			'if [ ! -d /usr/lib/jvm/java-6-sun ]; then',
			'	wget --no-cookies --header "Cookie: gpw_e24=http%3A%2F%2Fwww.oracle.com%2F" http://download.oracle.com/otn-pub/java/jdk/6u45-b06/jdk-6u45-linux-x64.bin',
			'	chmod u+x jdk-6u45-linux-x64.bin',
			'	./jdk-6u45-linux-x64.bin',
			'	rm jdk-6u45-linux-x64.bin',
			'	mkdir -p /usr/lib/jvm',
			'	mv jdk1.6.0_45 /usr/lib/jvm/java-6-sun',
			'	sudo update-alternatives --install "/usr/bin/java" "java" "/usr/lib/jvm/java-6-sun/bin/java" 1',
			'	sudo update-alternatives --install "/usr/bin/javac" "javac" "/usr/lib/jvm/java-6-sun/bin/javac" 1',
			'	sudo update-alternatives --install "/usr/bin/javaws" "javaws" "/usr/lib/jvm/java-6-sun/bin/javaws" 1',
			'fi'
		)


class NginxInstallScript(ShellScript):
	@classmethod
	def get_script(cls):
		return cls.multiline(
			'if [ ! "$(which nginx)" ]; then',
			'	cd %s' % os.path.join(dependencies_directory, 'nginx'),
			'	make clean',
			'	./configure --with-http_ssl_module --sbin-path=/usr/local/sbin/nginx',
			'	sudo make install',
			'	sudo mkdir -p /etc/nginx',
			'	sudo ln -s /usr/local/nginx/conf/mime.types /etc/nginx/mime.types',
			'fi'
		)


class RabbitmqInstallScript(ShellScript):
	@classmethod
	def get_script(cls):
		return cls.multiline(
			'apt-get install -y rabbitmq-server',
			'dpkg -i %s' % os.path.join(dependencies_directory, 'rabbitmq-server.deb'),
			'mkdir /etc/rabbitmq/rabbitmq.conf.d',
			'if [ ! -f /usr/local/bin/rabbitmqadmin ]; then',
			'	rabbitmq-plugins enable rabbitmq_management',
			'	service rabbitmq-server restart',
			'fi',
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
			'fi',
			'rm -f %s/*' % os.path.join(koality_root, 'db', 'redis'),
			'chmod a+w %s' % os.path.join(koality_root, 'db', 'redis')
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
