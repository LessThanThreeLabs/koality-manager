import os

from manager.shared import conf_directory, dependencies_directory, node_directory, nvm_directory, python_bin_directory, virtualenv_directory
from manager.shared.script import ShellScript


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
			cd /tmp
			rm -rf agles
		''' % (virtualenv_directory,
				dependencies_directory,
				os.path.join(conf_directory, 'redis'),
				os.path.join(conf_directory, 'redis'),
				os.path.join(conf_directory, 'haproxy'),
				os.path.join(conf_directory, 'haproxy'),
				os.path.join(python_bin_directory, 'pip'),
				os.path.join(python_bin_directory, 'python'))


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
			npm install -g grunt-cli
			cd node
			git clone git@github.com:LessThanThreeLabs/koality-webserver.git webserver
			cd webserver
			npm install
			grunt production
			rm -rf src front/src front/test .git
			cd %s
			git clone git@github.com:LessThanThreeLabs/koality-api-server.git api-server
			cd api-server
			npm install
			./compile
			rm -rf src .git
		''' % (node_directory,
				node_directory,
				nvm_directory,
				nvm_directory,
				os.path.join(nvm_directory, 'nvm.sh'),
				node_directory)
