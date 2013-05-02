import os

from manager.shared import node_directory
from manager.shared.script import ShellScript


class WebInstallScript(ShellScript):
	@classmethod
	def get_script(cls):
		return 'chmod -R a+w %s' % os.path.join(node_directory, 'webserver', 'redis')
