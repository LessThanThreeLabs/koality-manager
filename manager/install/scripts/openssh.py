from script import InstallShellScript


class OpenSshInstallScript(InstallShellScript):
	@classmethod
	def get_script(cls):
		return '''
			if [ ! -f '/usr/local/bin/ssh' ]; then
				cd /tmp
				git clone git://github.com/LessThanThreeLabs/openssh-for-git.git
				wget http://openbsd.mirrors.pair.com/OpenSSH/portable/openssh-6.0p1.tar.gz
				tar -xf /tmp/openssh-6.0p1.tar.gz
				cd openssh-6.0p1
				patch -p1 < /tmp/openssh-for-git/openssh-6.0p1-authorized-keys-script.diff
				./configure
				make -j 4
				make install
			fi
		'''


class OpenSshConfigureScript(InstallShellScript):
	@classmethod
	def get_script(cls):
		return '''
			cd /usr/local/etc
			grep "AuthorizedKeysScript" sshd_config
			if [ $? -ne 0 ]
				then chmod +x #{node[:koality][:source_path][:authorized_keys_script]}
				mv sshd_config sshd_config.bu
				sed '/AuthorizedKeysFile/d' sshd_config.bu | sed '/PasswordAuthentication/d' > sshd_config

				# Setting the authorized_keys file to something that can't exist so it uses the script
				echo "AuthorizedKeysScript #{node[:koality][:source_path][:authorized_keys_script]}" >> sshd_config
				echo "AuthorizedKeysFile /dev/null/authorized_keys" >> sshd_config
				echo "PasswordAuthentication no" >> sshd_config
				echo "AllowUsers git" >> sshd_config
				sed -i.bak -r 's/^AllowUsers .*$/AllowUsers lt3 git ubuntu/g' /etc/ssh/sshd_config
			fi
			'''


class OpenSshLaunchScript(InstallShellScript):
	_move_standard_daemon_script = '''
		service ssh stop
		/usr/sbin/sshd -p 2222
	'''

	_start_modified_daemon_script = '/usr/local/sbin/sshd -f /usr/local/etc/sshd_config'

	@classmethod
	def get_script(cls):
		return '\n'.join((
			cls._move_standard_daemon_script,
			cls._start_modified_daemon_script
		))
