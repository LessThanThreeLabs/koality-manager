import os

from manager.shared import dependencies_directory
from manager.shared.script import ShellScript


class JgitInstallScript(ShellScript):
	@classmethod
	def get_script(cls):
		return 'cp %s /usr/bin' % os.path.join(dependencies_directory, 'jgit', 'jgit')
