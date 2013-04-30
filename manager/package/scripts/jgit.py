from manager.shared import dependencies_directory
from manager.shared.script import ShellScript


class JgitPackageScript(ShellScript):
	@classmethod
	def get_script(cls):
		return '''
			cd /tmp
			git clone git://github.com/LessThanThreeLabs/jgit.git
			cd jgit
			mvn install
			mv org.eclipse.jgit.pgm/target/jgit %s
			rm -rf /tmp/jgit
		''' % dependencies_directory
