import os

from manager.shared import dependencies_directory
from manager.shared.script import ShellScript


class Lt3UserInstallScript(ShellScript):
	@classmethod
	def get_script(cls):
		return '''
			adduser lt3 --home /home/lt3 --shell /bin/bash --disabled-password --gecos ""
			mkdir /tmp/model_server
		'''


class GitUserInstallScript(ShellScript):
	@classmethod
	def get_script(cls):
		return '''
			adduser git --home /home/git --shell /bin/bash --disabled-password --gecos ''
			sudo -u git ssh-keygen -t rsa -N "" -f /home/git/.ssh/id_rsa -C git_user
			sudo -u git cat /home/git/.ssh/id_rsa.pub >> /home/git/.ssh/authorized_keys
			sudo -u git git config --global user.email "koality@koalitycode.com"
			sudo -u git git config --global user.name "Koality"
			mkdir -p /git/repositories
			chown -R git:git /git
		'''


class VerificationUserInstallScript(ShellScript):
	@classmethod
	def get_script(cls):
		return '''
			adduser verification --home /home/verification --shell /bin/bash --disabled-password --gecos ''
			sudo -u verification ssh-keygen -t rsa -N "" -f /home/verification/.ssh/id_rsa -C verification_user
			mkdir -p /verification/server /verification/snapshotter
			chown -R verification:verification /verification
		'''
		return os.path.join(dependencies_directory, 'rabbitmq_setup.sh')