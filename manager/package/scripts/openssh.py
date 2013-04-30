from manager.shared import dependencies_directory
from manager.shared.script import ShellScript


class OpenSshPackageScript(ShellScript):
	def get_script(self):
		return '''
			cd %s
			wget http://openbsd.mirrors.pair.com/OpenSSH/portable/openssh-6.0p1.tar.gz
			git clone git://github.com/LessThanThreeLabs/openssh-for-git.git
			tar -xf openssh-6.0p1.tar.gz
			mv openssh-6.0p1 openssh
			cd openssh
			patch -p1 < ../openssh-for-git/openssh-6.0p1-authorized-keys-script.dff
			rm -rf ../openssh-for-git
		''' % dependencies_directory
