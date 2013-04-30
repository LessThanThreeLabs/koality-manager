from dependencies import DependenciesInstallScript, CircusInstallScript, JavaInstallScript, HaproxyInstallScript
from dependencies import RabbitmqInstallScript, RedisInstallScript, PostgresInstallScript
from jgit import JgitInstallScript
from openssh import OpenSshInstallScript, OpenSshConfigureScript, OpenSshLaunchScript
from platform import PlatformRabbitmqInstallScript, PlatformSchemaInstallScript

install_scripts = [
	DependenciesInstallScript,
	CircusInstallScript,
	JavaInstallScript,
	JgitInstallScript,
	HaproxyInstallScript,
	RabbitmqInstallScript,
	RedisInstallScript,
	PostgresInstallScript,
	OpenSshInstallScript,
	OpenSshConfigureScript,
	OpenSshLaunchScript,
	PlatformRabbitmqInstallScript,
	PlatformSchemaInstallScript
]
