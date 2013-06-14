import os
import random
import string

from manager.shared import dependencies_directory, node_directory, python_bin_directory
from manager.shared.script import Script, ShellScript


class PlatformPythonInstallScript(Script):
	@classmethod
	def run(cls):
		for filename in os.listdir(python_bin_directory):
			with open(os.path.join(python_bin_directory, filename)) as script_file:
				contents = script_file.read()
			if contents.startswith('#!/'):
				contents = '\n'.join(['#!%s' % os.path.join(python_bin_directory, 'python')] + contents.split('\n')[1:])
				with open(os.path.join(python_bin_directory, filename), 'w') as script_file:
					script_file.write(contents)
		return True


class PlatformRabbitmqInstallScript(ShellScript):
	@classmethod
	def get_script(cls):
		rabbitmq_setup_script = os.path.join(dependencies_directory, 'rabbitmq_setup.sh')
		platform_rabbitmq_config_file = os.path.join('/etc', 'koality', 'conf', 'rabbit.yml')
		webserver_config_file = os.path.join(node_directory, 'webserver', 'config.json')

		alphanumeric = string.ascii_letters + string.digits
		rabbitmq_password = ''.join(random.choice(alphanumeric) for x in xrange(36))

		return cls.multiline(
			'mkdir -p %s' % os.path.join('/etc', 'koality', 'conf'),
			'sed -i"" "s/password=.*/password=%s/" %s' % (rabbitmq_password, rabbitmq_setup_script),
			'echo -e "rabbit_password: %s" > %s' % (rabbitmq_password, platform_rabbitmq_config_file),
			'sed -i"" "s/\\"password\\": \\".*\\"/\\"password\\": \\"%s\\"/" %s' % (rabbitmq_password, webserver_config_file)
		)


class PlatformSchemaInstallScript(ShellScript):
	@classmethod
	def get_script(cls):
		return cls.multiline(
			'sudo -u postgres psql -c "create user lt3 with password \'\'"',
			'sudo -u postgres psql -c "create database koality"',
			'sudo -u postgres psql -c "grant all privileges on database koality to lt3"',
			'sudo -u postgres psql -c "alter database koality owner to lt3"',
			'sudo -u lt3 %s' % os.path.join(python_bin_directory, 'koality-schema')
		)
