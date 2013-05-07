#!/usr/bin/env python

import sys


def main():
	mode = sys.argv[1] if len(sys.argv) > 1 else None
	if mode == 'run':
		from manager.run import Runner
		Runner().run()
	elif mode == 'install':
		from manager.install import Installer
		Installer().run()
	elif mode == 'upgrade':
		from manager.upgrade import Upgrader
		Upgrader().run()
	elif mode == 'package':
		from manager.package import Packager
		Packager().run()
	else:
		raise Exception('No valid mode specified. Must be "run", "install", or "upgrade"')


if __name__ == '__main__':
	main()
