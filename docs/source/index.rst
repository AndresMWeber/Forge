Forge: Just another autorigger
###################################################################################################
`Online Documentation (ReadTheDocs) <http://mayasig-cli.readthedocs.io/en/latest/#module-maya_signatures.commands.scrape>`_

.. image:: https://badge.fury.io/py/Forge.svg
    :target: https://badge.fury.io/py/Forge

.. image:: https://circleci.com/gh/AndresMWeber/Forge.svg?style=shield&circle-token=:circle-token
    :target: https://circleci.com/gh/AndresMWeber/Forge/

.. image:: https://coveralls.io/repos/github/AndresMWeber/forge/badge.svg?branch=master
    :target: https://coveralls.io/github/AndresMWeber/Forge?branch=master

.. image:: https://landscape.io/github/AndresMWeber/Forge/master/landscape.svg?style=flat
    :target: https://landscape.io/github/AndresMWeber/Forge/master
    :alt: Code Health

.. contents::

.. section-numbering::

Synopsis
=============

My Autorigger.  Ain't yo business..yet!

Features
--------
-  Caching
-  Uses automated naming conventions as read in config.yml
-  Up to date with online help docs
-  Temp file generator
-  JSON file output
-  CLI access
-  Dict output

Installation
============
Windows, etc.
-------------
A universal installation method (that works on Windows, Mac OS X, Linux, …, and always provides the latest version) is to use `pip`:

.. code-block:: bash

    # Make sure we have an up-to-date version of pip and setuptools:
    $ pip install --upgrade pip setuptools
    $ pip install Forge


(If ``pip`` installation fails for some reason, you can try
``easy_install forge`` as a fallback.)

Usage
=============

Python Package Usage
---------------------
Use this tool via package level functions

.. code-block:: python

    import forge
    forge.lorem_ipsum()


Version Support
===============
This package supports the Maya 2015, 2016 and 2017 so far so please be aware.

Class Documentation
===================
.. automodule:: forge
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:

.. automodule:: forge.templates
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:

.. automodule:: forge.elements
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:

.. automodule:: forge.elements.augmentors
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:

.. automodule:: forge.core.nodes.base
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:

.. automodule:: forge.core.nodes.maya
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
