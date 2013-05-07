import os

from manager.shared import dependencies_directory, python_bin_directory
from manager.shared.script import ShellScript


class OpenSshInstallScript(ShellScript):
	@classmethod
	def get_script(cls):
		return '''
			if [ ! -f '/usr/local/bin/ssh' ]; then
				cd %s
				./configure
				make -j 4
				make install
			fi
		''' % os.path.join(dependencies_directory, 'openssh')


class OpenSshConfigureScript(ShellScript):
	@classmethod
	def get_script(cls):
		authorized_keys_script = os.path.join(python_bin_directory, 'koality-authorized-keys-script')
		return '''
			cd /usr/local/etc
			grep "AuthorizedKeysScript" sshd_config
			if [ $? -ne 0 ]; then
				mv sshd_config sshd_config.bu
				sed '/AuthorizedKeysFile/d' sshd_config.bu | sed '/PasswordAuthentication/d' > sshd_config

				# Setting the authorized_keys file to something that can't exist so it uses the script
				echo "AuthorizedKeysScript %s" >> sshd_config
				echo "AuthorizedKeysFile /dev/null/authorized_keys" >> sshd_config
				echo "PasswordAuthentication no" >> sshd_config
				echo "AllowUsers git" >> sshd_config
				sed -i.bak -r 's/^AllowUsers .*$/AllowUsers lt3 git ubuntu/g' /etc/ssh/sshd_config
			else
				sed -i.bak -r 's!^AuthorizedKeysScript.*!AuthorizedKeysScript %s!g' sshd_config
			fi
		''' % (authorized_keys_script,
			authorized_keys_script)
