import os

conf_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'conf'))
dependencies_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'dependencies'))
virtualenv_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'virtualenv'))
python_bin_directory = os.path.join(virtualenv_directory, 'bin')
node_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'node'))
nvm_directory = os.path.join(node_directory, 'nvm')
