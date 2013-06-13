from haproxy import HaproxyPackageScript
from java import JavaPackageScript
from jgit import JgitPackageScript
from koality import PythonPackageScript, PlatformPackageScript, WebPackageScript, WebPackageCleanupScript
from log import LogPackageScript
from openssh import OpenSshPackageScript
from rabbitmq import RabbitmqPackageScript
from redis import RedisPackageScript


package_scripts = [
	HaproxyPackageScript,
	JavaPackageScript,
	JgitPackageScript,
	OpenSshPackageScript,
	RabbitmqPackageScript,
	RedisPackageScript,
	PythonPackageScript,
	PlatformPackageScript,
	WebPackageScript,
	WebPackageCleanupScript,
	LogPackageScript,
]
