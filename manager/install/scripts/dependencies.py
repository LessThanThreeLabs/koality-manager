import os

from manager import dependencies_directory
from script import InstallShellScript


class DependenciesInstallScript(InstallShellScript):
	_dependencies = (
		'make',
		'git',
		'postgresql',
		'python-software-properties',
		'build-essential',
		'libyaml-dev'
	)

	@classmethod
	def get_script(cls):
		return 'apt-get install -y %s' % ' '.join(cls._dependencies)


class JavaInstallScript(InstallShellScript):
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


class HaproxyInstallScript(InstallShellScript):
	@classmethod
	def get_script(cls):
		return '''
			cd %s
			make clean
			make install USE_OPENSSL=1 -j 4
		''' % os.path.join(dependencies_directory, 'haproxy')
