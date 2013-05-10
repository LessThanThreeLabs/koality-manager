from manager.shared import dependencies_directory
from manager.shared.script import ShellScript


class RabbitmqPackageScript(ShellScript):
	@classmethod
	def get_script(cls):
		return '''
			cd %s
			if [ ! -f rabbitmq-server.deb ]; then
				wget http://www.rabbitmq.com/releases/rabbitmq-server/v2.8.7/rabbitmq-server_2.8.7-1_all.deb
				mv rabbitmq-server_2.8.7-1_all.deb rabbitmq-server.deb
			fi
		''' % dependencies_directory
