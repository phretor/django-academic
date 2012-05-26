# this is all borrowed from Django source-code

from distutils.core import setup
from setuptools import find_packages

try:
    from academic import get_version
    VERSION = get_version().replace(' ', '-')
except ImportError:
    VERSION = '0.1.0'

try:
    long_description = open('README').read()
except:
    long_description = ''

setup(
    name = 'django-academic',
    version = VERSION,
    url = 'http://github.com/phretor/django-academic',
    author = 'Federico Maggi',
    author_email = 'fede@maggi.cc',
    description = 'A collection of models useful to describe' \
        ' an academic context',
    long_description = long_description,
    
    packages = find_packages(),
    
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
