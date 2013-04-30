from dependencies import DependenciesInstallScript, CircusInstallScript, JavaInstallScript
from jgit import JgitInstallScript
from openssh import OpenSshInstallScript, OpenSshConfigureScript, OpenSshLaunchScript

install_scripts = [
	DependenciesInstallScript,
	CircusInstallScript,
	JavaInstallScript,
	JgitInstallScript,
	OpenSshInstallScript,
	OpenSshConfigureScript,
	OpenSshLaunchScript
]
