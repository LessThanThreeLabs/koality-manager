import os

from manager.shared import python_bin_directory, virtualenv_directory
from manager.shared.script import ShellScript


class PlatformPackageScript(ShellScript):
	@classmethod
	def get_script(cls):
		return '''
			pip install virtualenv
			virtualenv %s --no-site-packages
			cd /tmp
			git clone git@github.com:LessThanThreeLabs/agles.git
			cd agles/ci/platform
			%s install -r requirements.txt
			%s setup.py install
			cd /tmp
			rm -rf agles
		''' % (virtualenv_directory,
				os.path.join(python_bin_directory, 'pip'),
				os.path.join(python_bin_directory, 'python'))


class WebPackageScript(ShellScript):
	@classmethod
	def get_script(cls):
		return '''
			mkdir nvm
			wget -P nvm https://raw.github.com/creationix/nvm/master/nvm.sh
			source nvm/nvm.sh
			nvm use 0.8.12
			cd /tmp
			git clone git@github.com:LessThanThreeLabs/koality-webserver.git
			cd koality-webserver
			npm install -g
			cd /tmp
			rm -rf koality-webserver
			git clone git@github.com:LessThanThreeLabs/koality-api-server.git
			cd koality-api-server
			npm install -g
			cd /tmp
			rm -rf koality-api-server
		'''
