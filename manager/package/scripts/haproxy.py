from manager.shared import dependencies_directory
from manager.shared.script import ShellScript


class HaproxyPackageScript(ShellScript):
	def get_script(self):
		return '''
			cd %s
			wget http://haproxy.1wt.eu/download/1.5/src/devel/haproxy-1.5-dev17.tar.gz
			tar -xf haproxy-1.5-dev-17.tar.gz
			rm haproxy-1.5-dev17.tar.gz
			mv haproxy-1.5-dev17 haproxy
		''' % dependencies_directory
