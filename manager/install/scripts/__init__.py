from dependencies import DependenciesInstallScript, JavaInstallScript
from jgit import JgitInstallScript
from openssh import OpenSshInstallScript, OpenSshConfigureScript, OpenSshLaunchScript

install_scripts = [
	DependenciesInstallScript,
	JavaInstallScript,
	JgitInstallScript,
	OpenSshInstallScript,
	OpenSshConfigureScript,
	OpenSshLaunchScript
]
