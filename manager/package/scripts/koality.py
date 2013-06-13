import json
import os

from manager.shared import conf_directory, dependencies_directory, node_directory, nvm_directory
from manager.shared import python_bin_directory, upgrade_directory, virtualenv_directory
from manager.shared.script import Script, ShellScript


class PythonPackageScript(ShellScript):
	@classmethod
	def get_script(cls):
		return cls.multiline(
			'cd /tmp',
			'git clone git@github.com:LessThanThreeLabs/python.git',
			'cd python',
			'./configure --prefix=%s' % os.path.join(dependencies_directory, 'python'),
			'make',
			'make install'
		)


class PlatformPackageScript(ShellScript):
	@classmethod
	def get_script(cls):
		return cls.multiline(
			'pip install virtualenv',
			'rm -rf %s' % virtualenv_directory,
			'virtualenv %s --no-site-packages --python %s' % (virtualenv_directory, os.path.join(dependencies_directory, 'python')),
			'cd /tmp',
			'git clone git@github.com:LessThanThreeLabs/agles.git',
			'cp agles/ci/scripts/rabbitmq_setup.sh %s' % dependencies_directory,
			'cd agles/ci/platform',
			'mkdir -p %s' % os.path.join(conf_directory, 'redis'),
			'cp conf/redis/* %s' % os.path.join(conf_directory, 'redis'),
			'mkdir -p %s' % os.path.join(upgrade_directory, 'alembic'),
			'cp -r alembic* %s' % os.path.join(upgrade_directory, 'alembic'),
			'%s install -r requirements.txt --upgrade' % os.path.join(python_bin_directory, 'pip'),
			'%s setup.py install' % os.path.join(python_bin_directory, 'python'),
			'python -m compileall %s' % os.path.join(virtualenv_directory, 'lib'),
			"find %s -name '*.py' | xargs rm" % os.path.join(virtualenv_directory, 'lib'),
			'virtualenv %s --relocatable' % virtualenv_directory,
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
			'source %s' % os.path.join(nvm_directory, 'nvm.sh'),
			'nvm install v0.8.12',
			'nvm use v0.8.12',
			'npm install -g iced-coffee-script',
			'rm -rf webserver',
			'wget https://s3.amazonaws.com/koality_code/libraries/private-cd855575be99a357/koality-webserver-0.1.0.tgz',
			'tar -xvf koality-webserver-0.1.0.tgz',
			'rm koality-webserver-0.1.0.tgz',
			'mv package webserver',
			'cd webserver',
			'rm -rf node_modules',
			'mkdir -p %s' % os.path.join(conf_directory, 'haproxy', 'cert'),
			'cp haproxy.conf %s' % os.path.join(conf_directory, 'haproxy'),
			'npm install',
			'rm -f redis/*',
			'chmod -R a+w redis',
		)


class WebPackageCleanupScript(Script):
	@classmethod
	def run(cls):
		for root, dirs, files in os.walk(os.path.join(node_directory, 'webserver')):
			if 'package.json' in files:
				package_path = os.path.join(root, 'package.json')
				with open(package_path) as package_file:
					package_config = json.load(package_file)
				for entry in ('dependencies', 'devDependencies', 'scripts'):
					if entry in package_config:
						del package_config[entry]
				with open(package_path, 'w') as package_file:
					json.dump(package_config, package_file)
		return True
