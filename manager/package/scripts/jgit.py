from manager.shared import dependencies_directory
from manager.shared.script import ShellScript


class JgitPackageScript(ShellScript):
	def get_script(self):
		return '''
			cd %s
			git clone git://github.com/LessThanThreeLabs/jgit.git
		''' % dependencies_directory
