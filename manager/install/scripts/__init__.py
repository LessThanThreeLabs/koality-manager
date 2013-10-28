from dependencies import DependenciesInstallScript, CircusInstallScript, JavaInstallScript, NginxInstallScript
from dependencies import RabbitmqInstallScript, RedisInstallScript, PostgresInstallScript
from jgit import JgitInstallScript
from koality import KoalityLinkScript, KoalityServiceInstallScript
from mercurial import MercurialInstallScript
from openssh import OpenSshInstallScript, OpenSshConfigureScript
from platform import PlatformPythonInstallScript, PlatformRabbitmqInstallScript, PlatformSchemaInstallScript
from user import Lt3UserInstallScript, GitUserInstallScript, HgUserInstallScript, VerificationUserInstallScript
from web import WebInstallScript

install_scripts = [
	DependenciesInstallScript,
	CircusInstallScript,
	JavaInstallScript,
	JgitInstallScript,
	NginxInstallScript,
	RabbitmqInstallScript,
	RedisInstallScript,
	PostgresInstallScript,
	MercurialInstallScript,
	OpenSshInstallScript,
	OpenSshConfigureScript,
	Lt3UserInstallScript,
	GitUserInstallScript,
	HgUserInstallScript,
	VerificationUserInstallScript,
	PlatformPythonInstallScript,
	PlatformRabbitmqInstallScript,
	PlatformSchemaInstallScript,
	WebInstallScript,
	KoalityLinkScript,
	KoalityServiceInstallScript
]
