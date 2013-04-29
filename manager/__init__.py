import os

from install.installer import Installer
from run.runner import Runner
from upgrade.upgrader import Upgrader


dependencies_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'dependencies'))
