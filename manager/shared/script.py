import subprocess


class ShellScript(object):
	@classmethod
	def run(cls):
		return subprocess.call(cls.get_script(), shell=True) == 0

	@classmethod
	def get_script(classmethod):
		raise NotImplementedError()
