import os

from manager.shared import dependencies_directory
from manager.shared.script import ShellScript


class MercurialPackageScript(ShellScript):
	@classmethod
	def get_script(cls):
		hg_dir = os.path.join(dependencies_directory, 'hg')
		return cls.multiline(
			'sudo apt-get install -y mercurial',
			'[ ! -d %s ] || rm -rf %s' % (hg_dir, hg_dir),
			'hg clone https://bitbucket.org/akostov/custom_mercurial %s' % hg_dir,
			'rm -rf %s' % (os.path.join(hg_dir, '.hg'))
		)
