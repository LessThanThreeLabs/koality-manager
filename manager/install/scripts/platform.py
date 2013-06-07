import os
import random
import string

from manager.shared import dependencies_directory, node_directory
from manager.shared.script import ShellScript


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
		return '''
			sudo -u postgres psql -c "create user lt3 with password ''"
			sudo -u postgres psql -c "create database koality"
			sudo -u postgres psql -c "grant all privileges on database koality to lt3"
			sudo -u postgres psql -c "alter database koality owner to lt3"
		'''
