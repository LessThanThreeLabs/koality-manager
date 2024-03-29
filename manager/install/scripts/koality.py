import os
import subprocess

from string import Template

from manager.shared import koality_root, service_directory, python_bin_directory
from manager.shared.script import Script, ShellScript


class KoalityLinkScript(ShellScript):
	@classmethod
	def get_script(cls):
		return '''
			mkdir -p /etc/koality
			rm -rf /etc/koality/python
			ln -s %s /etc/koality/python
			rm -rf /etc/koality/root
			ln -s %s /etc/koality/root
		''' % (os.path.abspath(os.path.join(python_bin_directory, os.pardir)), koality_root)


class KoalityServiceInstallScript(Script):
	@classmethod
	def run(cls):
		koality_command = '%s run' % os.path.join(koality_root, 'koality.py')
		with open(os.path.join(service_directory, 'init.d.template')) as template:
			script = Template(template.read()).safe_substitute(koality_command=koality_command)
		init_path = os.path.join('/etc', 'init.d', 'koality')
		with open(init_path, 'w') as init_file:
			os.chmod(init_path, 0755)
			init_file.write(script)
		return subprocess.call(['update-rc.d', 'koality', 'defaults', '60']) == 0
