import os

from string import Template

from manager.shared import koality_root, service_directory
from manager.shared.script import Script


class KoalityServiceInstallScript(Script):
	@classmethod
	def run(cls):
		koality_command = '%s -r' % os.path.join(koality_root, 'koality.py')
		with open(os.path.join(service_directory, 'init.d.template')) as template:
			script = Template(template.read()).safe_substitute(koality_command=koality_command)
		init_path = os.path.join('/etc', 'init.d', 'koality')
		with open(init_path, 'w') as init_file:
			os.chmod(init_path, 0755)
			init_file.write(script)
		return True
