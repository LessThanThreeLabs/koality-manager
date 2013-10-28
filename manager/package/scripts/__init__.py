from java import JavaPackageScript
from jgit import JgitPackageScript
from koality import PythonPackageScript, PlatformPackageScript, WebPackageScript, WebPackageCleanupScript
from log import LogPackageScript
from mercurial import MercurialPackageScript
from nginx import NginxPackageScript
from openssh import OpenSshPackageScript
from rabbitmq import RabbitmqPackageScript
from redis import RedisPackageScript


package_scripts = [
	NginxPackageScript,
	JavaPackageScript,
	JgitPackageScript,
	MercurialPackageScript,
	OpenSshPackageScript,
	RabbitmqPackageScript,
	RedisPackageScript,
	PythonPackageScript,
	PlatformPackageScript,
	WebPackageScript,
	WebPackageCleanupScript,
	LogPackageScript,
]
