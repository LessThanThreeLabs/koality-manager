from manager.shared import log_directory
from manager.shared.script import ShellScript


class LogPackageScript(ShellScript):
	@classmethod
	def get_script(cls):
		return 'rm -f %s/*' % log_directory
