# this is all borrowed from Django source-code

from distutils.core import setup
from distutils.command.install_data import install_data
from distutils.command.install import INSTALL_SCHEMES

import os
import sys

try:
    from foopackage import get_version
    VERSION = get_version().replace(' ', '-')
except ImportError:
    VERSION = '0.1-alpha-1'

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
    name = 'django-foopackage',
    version = VERSION,
    url = 'http://bitbucket.org/phretor/django-foopackage',
    author = 'Federico Maggi',
    author_email = 'federico@maggi.cc',
    description = 'A Django package that provides Foo.',
    
    packages = packages,
    cmdclass = cmdclasses,
    data_files = data_files,

        classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
                'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
                'Topic :: Software Development :: Libraries :: Python Modules',
                'Topic :: Utilities'
        ]
)
