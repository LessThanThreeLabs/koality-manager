import os

from manager.shared import dependencies_directory
from manager.shared.script import ShellScript


class MercurialInstallScript(ShellScript):
	@classmethod
	def get_script(cls):
		return cls.multiline(
			'cd %s' % os.path.join(dependencies_directory, 'hg'),
			'sudo make install'
		)
