from haproxy import HaproxyPackageScript
from java import JavaPackageScript
from jgit import JgitPackageScript
from koality import PlatformPackageScript, WebPackageScript
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
	PlatformPackageScript,
	WebPackageScript
]
