from manager.shared import dependencies_directory
from manager.shared.script import ShellScript


class NginxPackageScript(ShellScript):
	@classmethod
	def get_script(cls):
		return '''
			cd %s
			if [ ! -d nginx ]; then
				wget http://nginx.org/download/nginx-1.4.3.tar.gz
				tar -xf nginx-1.4.3.tar.gz
				rm nginx-1.4.3.tar.gz
				mv nginx-1.4.3 nginx
			fi
		''' % dependencies_directory
