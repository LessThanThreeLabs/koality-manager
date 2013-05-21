import os

from manager.shared import dependencies_directory
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
			sudo -u postgres psql -c "alter database koality owner to lt3"
		'''
