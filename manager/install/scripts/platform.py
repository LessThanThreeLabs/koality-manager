import json
import os
import random
import re
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


class PlatformRabbitmqInstallScript(Script):
	@classmethod
	def run(cls):
		rabbitmq_setup_script = os.path.join(dependencies_directory, 'rabbitmq_setup.sh')
		platform_rabbitmq_config_file = os.path.join('/etc', 'koality', 'conf', 'rabbit.yml')
		webserver_config_file = os.path.join(node_directory, 'webserver', 'config.json')

		alphanumeric = string.ascii_letters + string.digits
		rabbitmq_password = ''.join(random.choice(alphanumeric) for x in xrange(36))

		config_directory = os.path.join('/etc', 'koality', 'conf')
		if not os.access(config_directory, os.F_OK):
			os.makedirs(config_directory)

		with open(rabbitmq_setup_script) as setup_script:
			setup_script_contents = setup_script.read()
		with open(rabbitmq_setup_script, 'w') as setup_script:
			setup_script.write(re.sub('password=.*', 'password=%s' % rabbitmq_password, setup_script_contents))

		with open(platform_rabbitmq_config_file, 'w') as platform_rabbitmq_config:
			platform_rabbitmq_config.write('rabbit_password: %s' % rabbitmq_password)

		with open(webserver_config_file) as webserver_config:
			config = json.load(webserver_config)
		config['modelConnection']['messageBroker']['password'] = rabbitmq_password
		with open(webserver_config_file, 'w') as webserver_config:
			json.dump(config, webserver_config, indent=2)

		return True


class PlatformSchemaInstallScript(ShellScript):
	@classmethod
	def get_script(cls):
		return cls.multiline(
			'sudo -u postgres psql -c "create user lt3 with password \'\'"',
			'sudo -u postgres psql -c "create database koality"',
			'sudo -u postgres psql -c "grant all privileges on database koality to lt3"',
			'sudo -u postgres psql -c "alter database koality owner to lt3"'
		)
