# this is all borrowed from Django source-code

from distutils.core import setup
from distutils.command.install_data import install_data
from distutils.command.install import INSTALL_SCHEMES

from foopackage import get_version

import os
import sys

class osx_install_data(install_data):
    def finalize_options(self):
        self.set_undefined_options('install', ('install_lib', 'install_dir'))
        install_data.finalize_options(self)

if sys.platform == "darwin": 
    cmdclasses = {'install_data': osx_install_data} 
else: 
    cmdclasses = {'install_data': install_data} 

def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in
    a platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)

for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir != '':
    os.chdir(root_dir)
package_dir = 'foopackage'

for dirpath, dirnames, filenames in os.walk(package_dir):
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        packages.append('.'.join(fullsplit(dirpath)))
    elif filenames:
        data_files.append(
            [dirpath, [os.path.join(dirpath, f) for f in filenames]])

setup(
    name = 'python-foopackage',
    version = get_version().replace(' ', '-'),
    url = 'http://maggi.cc/',
    download_url = 'http://bitbucket.org/phretor/python-foopackage/get/v0.1.gz',
    author = 'Federico Maggi',
    author_email = 'federico@maggi.cc',
    description = 'A Foo Python package.',
    
    packages = packages,
    cmdclass = cmdclasses,
    data_files = data_files,
)
