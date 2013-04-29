#!/usr/bin/env python

import argparse

from manager import Installer, Runner, Upgrader


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-r', '--run', action='store_true',
		help='Runs koality')
	parser.add_argument('-i', '--install', action='store_true',
		help='Installs koality from scratch')
	parser.add_argument('-u', '--upgrade', action='store_true',
		help='Upgrades koality from a previous version')
	args = parser.parse_args()

	if args.run:
		Runner().run()
	elif args.install:
		Installer().run()
	elif args.upgrade:
		Upgrader().run()
	else:
		raise Exception('No valid mode specified')


if __name__ == '__main__':
	main()
