import os

koality_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
conf_directory = os.path.join(koality_root, 'conf')
dependencies_directory = os.path.join(koality_root, 'dependencies')
python_directory = os.path.join(koality_root, 'python')
python_bin_directory = os.path.join(python_directory, 'bin')
node_directory = os.path.join(koality_root, 'node')
nvm_directory = os.path.join(node_directory, 'nvm')
service_directory = os.path.join(koality_root, 'service')
upgrade_directory = os.path.join(koality_root, 'upgrade')
log_directory = os.path.join(koality_root, 'log')
