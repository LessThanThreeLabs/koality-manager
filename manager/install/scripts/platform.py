import os

from manager.shared import dependencies_directory, python_bin_directory
from manager.shared.script import ShellScript


class PlatformRabbitmqInstallScript(ShellScript):
	@classmethod
	def get_script(cls):
		return os.path.join(dependencies_directory, 'rabbitmq_setup.sh')


class PlatformSchemaInstallScript(ShellScript):
	@classmethod
	def get_script(cls):
		return '''
			sudo -u postgres psql -c "create user lt3 with password ''"
			sudo -u postgres psql -c "create database koality"
			sudo -u postgres psql -c "grant all privileges on database koality to lt3"
			%s
		''' % os.path.join(python_bin_directory, 'koality-schema')
