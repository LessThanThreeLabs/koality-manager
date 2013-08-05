from manager.shared.script import ShellScript


class Lt3UserInstallScript(ShellScript):
	@classmethod
	def get_script(cls):
		return '''
			adduser lt3 --home /home/lt3 --shell /bin/bash --disabled-password --gecos ""
			echo 'lt3 ALL=(ALL) NOPASSWD:ALL' > koality.sudo
			chown 0:0 koality.sudo
			chmod 0440 koality.sudo
			mv koality.sudo /etc/sudoers.d/koality
			mkdir /tmp/model_server
			chown -R lt3:lt3 /tmp/model_server
		'''


class GitUserInstallScript(ShellScript):
	@classmethod
	def get_script(cls):
		return '''
			adduser git --home /home/git --shell /bin/bash --disabled-password --gecos ''
			yes no | sudo -u git ssh-keygen -t rsa -N "" -f /home/git/.ssh/id_rsa -C git_user
			sudo -u git bash -c 'key=$(cat /home/git/.ssh/id_rsa.pub); grep "$key" /home/git/.ssh/authorized_keys || echo "$key" >> /home/git/.ssh/authorized_keys'
			sudo -u git HOME=/home/git git config --global user.email "koality@koalitycode.com"
			sudo -u git HOME=/home/git git config --global user.name "Koality"
			mkdir -p /git/repositories
			sudo -u git bash -c 'echo -e "[ui]\\nusername = Koality <koality@koalitycode.com>\\n\\n[extensions]\\nmq =" > /home/git/.hgrc'
			chown -R git:git /git
		'''


class HgUserInstallScript(ShellScript):
	@classmethod
	def get_script(cls):
		return '''
			adduser hg --home /home/hg --shell /bin/bash --disabled-password --gecos ''
			yes no | sudo -u hg ssh-keygen -t rsa -N "" -f /home/hg/.ssh/id_rsa -C hg_user
			sudo bash -c 'key=$(cat /home/hg/.ssh/id_rsa.pub); grep "$key" /home/git/.ssh/authorized_keys || echo "$key" >> /home/git/.ssh/authorized_keys'
		'''


class VerificationUserInstallScript(ShellScript):
	@classmethod
	def get_script(cls):
		return '''
			adduser verification --home /home/verification --shell /bin/bash --disabled-password --gecos ''
			yes no | sudo -u verification ssh-keygen -t rsa -N "" -f /home/verification/.ssh/id_rsa -C verification_user
			mkdir -p /verification/server /verification/snapshotter
			chown -R verification:verification /verification
		'''
