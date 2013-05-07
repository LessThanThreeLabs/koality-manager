from manager.shared import dependencies_directory
from manager.shared.script import ShellScript


class JavaPackageScript(ShellScript):
	@classmethod
	def get_script(cls):
		return '''
			cd %s
			if [ ! -d java ]; then
				git clone git://github.com/flexiondotorg/oab-java6.git java
				rm -rf java/.git
			fi
		''' % dependencies_directory
