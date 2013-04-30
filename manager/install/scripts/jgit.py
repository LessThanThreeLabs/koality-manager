import os

from manager.shared import dependencies_directory
from manager.shared.script import ShellScript


class JgitInstallScript(ShellScript):
	_install_script = '''
		cd %s
		mvn install
		cp org.eclipse.jgit.pgm/target/jgit /usr/bin/
	''' % os.path.join(dependencies_directory, 'jgit')

	_link_script = ''

	@classmethod
	def get_script(cls):
		return '\n'.join((
			cls._install_script,
			cls._link_script
		))
