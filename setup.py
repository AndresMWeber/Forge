"""Packaging settings."""
import codecs
from os.path import abspath, dirname, join
from setuptools import setup, find_packages
from distutils.util import convert_path


__package__ = 'forge'
__author__ = 'Andres Weber'
__url__ = 'https://github.com/andresmweber/forge.git'
__email__ = 'andresmweber@gmail.com'
__keywords__ = ['maya',
                'autorigger',
                'rigging',
                'templates',
                'maya.cmds',
                'autodesk']
__requirements__ = ['simplejson', 'nomenclate', 'six', 'Qt.py']
__requirements_test__ = ['nose', 'coveralls']
__requirements_dev__ = ['twine', 'sphinx', 'docutils', 'docopt']

# from:
# http://stackoverflow.com/questions/2058802/how-can-i-get-the-version-defined-in-setup-py-setuptools-in-my-package
main_ns = {}
with open(convert_path('%s/version.py' % __package__)) as ver_file:
    exec (ver_file.read(), main_ns)
__version__ = main_ns['__version__']

with codecs.open(join(abspath(dirname(__file__)), 'README.rst'), encoding='utf-8') as readme_file:
    __long_description__ = readme_file.read()



setup(
    name=__package__,
    version=__version__,
    description=("A toolset for building and maintaining rigs in Maya (and more later)."
                 "maya.cmds command (or build stubs) for its signature in Python."),
    long_description=__long_description__,
    url=__url__,
    author=__author__,
    author_email=__email__,
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: Public Domain',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    keywords=__keywords__,
    packages=find_packages(exclude=['docs', 'tests*']),
    install_requires=__requirements__,
    extras_require={
        'test': __requirements_test__,
        'dev': __requirements_dev__
    },
    cmdclass={'test': 'tox'},
)
