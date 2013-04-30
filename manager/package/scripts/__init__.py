from haproxy import HaproxyPackageScript
from java import JavaPackageScript
from jgit import JgitPackageScript
from koality import PlatformPackageScript, WebPackageScript
from openssh import OpenSshPackageScript


package_scripts = [
	HaproxyPackageScript,
	JavaPackageScript,
	JgitPackageScript,
	OpenSshPackageScript,
	PlatformPackageScript,
	WebPackageScript
]
