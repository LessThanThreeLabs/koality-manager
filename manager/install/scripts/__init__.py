from dependencies import DependenciesInstallScript, CircusInstallScript, JavaInstallScript, HaproxyInstallScript
from dependencies import RabbitmqInstallScript, RedisInstallScript, PostgresInstallScript
from jgit import JgitInstallScript
from koality import KoalityLinkScript, KoalityServiceInstallScript
from openssh import OpenSshInstallScript, OpenSshConfigureScript
from platform import PlatformPythonInstallScript, PlatformRabbitmqInstallScript, PlatformSchemaInstallScript
from user import Lt3UserInstallScript, GitUserInstallScript, VerificationUserInstallScript
from web import WebInstallScript

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
	Lt3UserInstallScript,
	GitUserInstallScript,
	VerificationUserInstallScript,
	PlatformPythonInstallScript,
	PlatformRabbitmqInstallScript,
	PlatformSchemaInstallScript,
	WebInstallScript,
	KoalityLinkScript,
	KoalityServiceInstallScript
]
