import os
import subprocess

from string import Template

from manager.shared import koality_root, service_directory, python_bin_directory
from manager.shared.script import Script, ShellScript


class KoalityLinkScript(ShellScript):
	@classmethod
	def get_script(cls):
		return '''
			mkdir -p /etc/koality/python
			rm -r /etc/koality/python/bin
			ln -s %s /etc/koality/python/bin
			rm -r /etc/koality/root
			ln -s %s /etc/koality/root
		''' % (python_bin_directory, koality_root)


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
		return subprocess.call(['update-rc.d', 'koality', 'defaults']) == 0
