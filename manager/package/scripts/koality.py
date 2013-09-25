import json
import os

from manager.shared import conf_directory, dependencies_directory, node_directory, nvm_directory
from manager.shared import python_directory, python_bin_directory, upgrade_directory
from manager.shared.script import Script, ShellScript


class PythonPackageScript(ShellScript):
	@classmethod
	def get_script(cls):
		return cls.multiline(
			'if [ -d %s ]; then' % os.path.join(dependencies_directory, 'cached', 'python'),
			'	rm -rf %s' % python_directory,
			'	cp -r %s %s' % (os.path.join(dependencies_directory, 'cached', 'python'), python_directory),
			'	exit',
			'fi',
			'sudo apt-get install -y libbz2-dev zlib1g-dev',
			'rm -rf %s' % python_directory,
			'cd /tmp',
			'git clone git@github.com:LessThanThreeLabs/python.git',
			'cd python',
			'./configure',
			'make',
			'make install prefix=%s' % python_directory,
			'cd /tmp',
			'rm -rf python',
			'curl https://bitbucket.org/pypa/setuptools/raw/0.7.4/ez_setup.py | %s' % os.path.join(python_bin_directory, 'python'),
			'curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | %s' % os.path.join(python_bin_directory, 'python'),
			'%s install pip --upgrade' % os.path.join(python_directory, 'pip'),
			'mkdir -p %s' % os.path.join(dependencies_directory, 'cached'),
			'cp -r %s %s' % (python_directory, os.path.join(dependencies_directory, 'cached'))
		)


class PlatformPackageScript(ShellScript):
	@classmethod
	def get_script(cls):
		return cls.multiline(
			'cd /tmp',
			'git clone git@github.com:LessThanThreeLabs/agles.git -b 0.4.6',
			'cp agles/ci/scripts/rabbitmq_setup.sh %s' % dependencies_directory,
			'cd agles/ci/platform',
			'mkdir -p %s' % os.path.join(conf_directory, 'redis'),
			'cp conf/redis/* %s' % os.path.join(conf_directory, 'redis'),
			'mkdir -p %s' % os.path.join(upgrade_directory, 'alembic'),
			'rm -rf %s/*' % os.path.join(upgrade_directory, 'alembic'),
			'cp -r alembic* %s' % os.path.join(upgrade_directory, 'alembic'),
			'%s install -r requirements.txt' % os.path.join(python_bin_directory, 'pip'),
			'%s setup.py install' % os.path.join(python_bin_directory, 'python'),
			'%s -m compileall %s' % (os.path.join(python_bin_directory, 'python'), os.path.join(python_directory, 'lib')),
			"find %s -name '*.py' | xargs rm" % os.path.join(python_directory, 'lib'),
			'cd /tmp',
			'rm -rf agles'
		)


class WebPackageScript(ShellScript):
	@classmethod
	def get_script(cls):
		return cls.multiline(
			'mkdir -p %s' % node_directory,
			'cd %s' % node_directory,
			'mkdir -p %s' % nvm_directory,
			'if [ ! -f %s ]; then' % os.path.join(nvm_directory, 'nvm.sh'),
			'  wget -P %s https://raw.github.com/creationix/nvm/master/nvm.sh' % nvm_directory,
			'fi',
			'source %s' % os.path.join(nvm_directory, 'nvm.sh'),
			'nvm install v0.10.13',
			'nvm use v0.10.13',
			'npm install -g iced-coffee-script',
			'rm -rf webserver',
			'wget https://s3.amazonaws.com/koality_code/libraries/private-cd855575be99a357/koality-webserver-0.4.1.tgz',
			'tar -xvf koality-webserver-0.4.1.tgz',
			'rm koality-webserver-0.4.1.tgz',
			'mv package webserver',
			'cd webserver',
			'rm -rf node_modules',
			'mkdir -p %s' % os.path.join(conf_directory, 'haproxy', 'cert'),
			'cp haproxy.conf %s' % os.path.join(conf_directory, 'haproxy'),
			'npm install',
			'rm -f redis/*',
			'chmod -R a+w redis'
		)


class WebPackageCleanupScript(Script):
	@classmethod
	def run(cls):
		for root, dirs, files in os.walk(os.path.join(node_directory, 'webserver')):
			if 'package.json' in files:
				package_path = os.path.join(root, 'package.json')
				with open(package_path) as package_file:
					package_config = json.load(package_file)
				sanitized_package_config = {}
				for key in ('name', 'version', 'main'):
					if key in package_config:
						sanitized_package_config[key] = package_config[key]
				with open(package_path, 'w') as package_file:
					json.dump(sanitized_package_config, package_file)
		return True
