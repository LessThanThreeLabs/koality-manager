import os

from manager import dependencies_directory
from script import InstallShellScript


class JgitInstallScript(InstallShellScript):
	_install_script = '''
		cd %s
		mvn install
		cp org.eclipse.jgit.pgm/target/jgit /usr/bin/
		mkdir -p /usr/bin/gitbin
		mv /usr/bin/git-* /usr/bin/gitbin
	''' % os.path.join(dependencies_directory, 'jgit')

	_link_script = ''

	@classmethod
	def get_script(cls):
		return '\n'.join((
			cls._install_script,
			cls._link_script
		))
