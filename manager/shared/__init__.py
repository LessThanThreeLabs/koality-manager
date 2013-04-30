import os

dependencies_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'dependencies'))
virtualenv_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'virtualenv'))
python_bin_directory = os.path.join(virtualenv_directory, 'bin')
