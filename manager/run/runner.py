import os

from circus.arbiter import Arbiter
from circus.watcher import Watcher

from manager.shared import python_bin_directory


class Runner(object):
	def __init__(self):
		self._koality_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
		self._watchers = [
			Watcher(
				name='model_server',
				cmd=self._python_bin('koality-start-model-server'),
				working_dir='/tmp/model_server',
				user='lt3'
			),
			Watcher(
				name='verification_server',
				cmd=self._python_bin('koality-start-verification-server'),
				args=['--type', 'aws', '--cleanup'],
				working_dir='/verification/server',
				user='verification'
			),
			Watcher(
				name='ec2_snapshotter',
				cmd=self._python_bin('koality-ec2-snapshotter'),
				args=['--daemon'],
				working_dir='/verification/snapshotter',
				user='verification'
			)
		]
		self.watchers = [Watcher]

	def _python_bin(self, bin_name):
		return os.path.join(python_bin_directory, bin_name)

	def run(self):
		arbiter = Arbiter(self._watchers, 'tcp://127.0.0.1:5555', 'tcp://127.0.0.1:5556', debug=True)
		try:
			arbiter.start()
		finally:
			arbiter.stop()
