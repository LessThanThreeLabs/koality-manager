import json
import os

from manager.shared import conf_directory, dependencies_directory, node_directory, nvm_directory, python_bin_directory, virtualenv_directory
from manager.shared.script import Script, ShellScript


class PlatformPackageScript(ShellScript):
	@classmethod
	def get_script(cls):
		return '''
			pip install virtualenv
			virtualenv %s --no-site-packages
			cd /tmp
			git clone git@github.com:LessThanThreeLabs/agles.git
			cp agles/ci/scripts/rabbitmq_setup.sh %s
			mkdir -p %s
			cp agles/ci/platform/conf/redis/* %s
			mkdir -p %s
			cp agles/ci/web/haproxy.conf %s
			cd agles/ci/platform
			%s install -r requirements.txt
			%s setup.py install
			virtualenv %s --relocatable
			cd /tmp
			rm -rf agles
		''' % (virtualenv_directory,
				dependencies_directory,
				os.path.join(conf_directory, 'redis'),
				os.path.join(conf_directory, 'redis'),
				os.path.join(conf_directory, 'haproxy'),
				os.path.join(conf_directory, 'haproxy'),
				os.path.join(python_bin_directory, 'pip'),
				os.path.join(python_bin_directory, 'python'),
				virtualenv_directory)


class WebPackageScript(ShellScript):
	@classmethod
	def get_script(cls):
		return '''
			mkdir -p %s
			cd %s
			mkdir -p %s
			wget -P %s https://raw.github.com/creationix/nvm/master/nvm.sh
			source %s
			nvm install 0.8.12
			nvm use 0.8.12
			npm install -g iced-coffee-script
			wget https://s3.amazonaws.com/koality_code/libraries/private-cd855575be99a357/koality-webserver-0.1.0.tgz
			tar -xvf koality-webserver-0.1.0.tgz
			rm koality-webserver-0.1.0.tgz
			mv package webserver
			cd webserver
			npm install
			chmod -R a+w redis
		''' % (node_directory,
				node_directory,
				nvm_directory,
				nvm_directory,
				os.path.join(nvm_directory, 'nvm.sh'))


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
