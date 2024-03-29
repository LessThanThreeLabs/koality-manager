import subprocess


class Script(object):
	@classmethod
	def run(cls):
		return NotImplementedError()


class ShellScript(Script):
	@classmethod
	def run(cls):
		return subprocess.call(['bash', '-c', cls.get_script()]) == 0

	@classmethod
	def get_script(cls):
		raise NotImplementedError()

	@classmethod
	def multiline(cls, *lines):
		return '\n'.join(lines)
