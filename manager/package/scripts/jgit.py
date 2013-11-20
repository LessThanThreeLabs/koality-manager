import os

from manager.shared import dependencies_directory
from manager.shared.script import ShellScript


class JgitPackageScript(ShellScript):
	@classmethod
	def get_script(cls):
		jgit_branch = '0.7.5'
		jgit_dir = os.path.join(dependencies_directory, 'jgit')
		jgit_version_file = os.path.join(jgit_dir, '.version')
		return '''
			headsha=$(git ls-remote git://github.com/LessThanThreeLabs/jgit.git refs/heads/%s | awk '{print $1}')
			if [ -f %s ] && [ "$(cat %s)" == "$headsha" ]; then
				echo "Newest jgit already packaged"
			else
				cd /tmp
				git clone git://github.com/LessThanThreeLabs/jgit.git -b %s
				cd jgit
				sudo apt-get install -y maven
				mvn install -Dmaven.test.skip=true || exit 1
				mkdir -p %s
				mv org.eclipse.jgit.pgm/target/jgit %s
				echo $headsha > %s
				rm -rf /tmp/jgit
			fi
		''' % (jgit_branch,
				jgit_version_file,
				jgit_version_file,
				jgit_branch,
				jgit_dir,
				jgit_dir,
				jgit_version_file)
