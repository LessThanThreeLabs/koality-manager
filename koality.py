#!/usr/bin/env python

import argparse
import sys

from collections import OrderedDict


def main():
	def package():
		from manager.package import Packager
		parser = argparse.ArgumentParser()
		parser.add_argument("-i", "--installable", action="store_true",
			help="Creates an installable tar file without the packager")
		args, unknown = parser.parse_known_args()
		Packager().run(args.installable)

	def install():
		from manager.install import Installer
		Installer().run()

	def upgrade():
		from manager.upgrade import Upgrader
		Upgrader().run()

	def run():
		from manager.run import Runner
		Runner().run()

	valid_actions = OrderedDict([
		('package', package),
		('install', install),
		('upgrade', upgrade),
		('run', run)
	])

	chosen_actions = sys.argv[1:]

	if not chosen_actions:
		raise Exception('No valid actions specified. Must be in %s' % valid_actions.keys())

	invalid_actions = filter(lambda action: action not in valid_actions and not action.startswith('-'), chosen_actions)
	if invalid_actions:
		raise Exception('Invalid actions %s specified. Must be in %s' % (invalid_actions, valid_actions.keys()))

	for action_name, action_method in valid_actions.iteritems():
		if action_name in chosen_actions:
			action_method()


if __name__ == '__main__':
	main()
