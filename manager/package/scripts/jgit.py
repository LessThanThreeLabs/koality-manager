import os

from manager.shared import dependencies_directory
from manager.shared.script import ShellScript


class JgitPackageScript(ShellScript):
	@classmethod
	def get_script(cls):
		jgit_dir = os.path.join(dependencies_directory, 'jgit')
		jgit_version_file = os.path.join(jgit_dir, '.version')
		return '''
			cd /tmp
			git clone git://github.com/LessThanThreeLabs/jgit.git
			cd jgit
			headsha=$(git rev-parse HEAD)
			if [ -f %s ] && [ "$(cat %s)" == "$headsha" ]; then
				echo "Newest jgit already packaged"
			else
				mvn install
				mkdir -p %s
				mv org.eclipse.jgit.pgm/target/jgit %s
				echo $headsha > %s
			fi
			rm -rf /tmp/jgit
		''' % (jgit_version_file,
				jgit_version_file,
				jgit_dir,
				jgit_dir,
				jgit_version_file)
