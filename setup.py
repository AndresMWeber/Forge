"""Packaging settings."""
import codecs
from os.path import abspath, dirname, join
from setuptools import setup, find_packages
from distutils.util import convert_path

__package__ = 'forge'

# from:
# http://stackoverflow.com/questions/2058802/how-can-i-get-the-version-defined-in-setup-py-setuptools-in-my-package
main_ns = {}
with open(convert_path('%s/version.py' % __package__)) as ver_file:
    exec (ver_file.read(), main_ns)

with codecs.open(join(abspath(dirname(__file__)), 'README.rst'), encoding='utf-8') as readme_file:
    long_description = readme_file.read()

setup(
    name='forge',
    version=main_ns['__version__'],
    description=("A toolset for building and maintaining rigs in Maya (and more later)."
                 "maya.cmds command (or build stubs) for its signature in Python."),
    long_description=long_description,
    url='https://github.com/andresmweber/forge.git',
    author='Andres Weber',
    author_email='andresmweber@gmail.com',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: Public Domain',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    keywords=['maya', 'autorigger', 'rigging', 'templates', 'maya.cmds', 'autodesk'],
    packages=find_packages(exclude=['docs', 'tests*']),
    install_requires=['simplejson', 'nomenclate', 'six'],
    extras_require={
        'test': ['nose', 'travis', 'coveralls'],
        'dev': ['twine', 'sphinx', 'docutils', 'docopt']
    },
    cmdclass={'test': 'tox'},
)
