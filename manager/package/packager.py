from scripts import package_scripts


class Packager(object):
	def run(self):
		self._run_with_exceptions(package_scripts)

	def _run_with_exceptions(self, scripts):
		for script in scripts:
			if not script.run():
				raise ScriptFailedException(script)
		return True


class ScriptFailedException(Exception):
	pass
