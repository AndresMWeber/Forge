Forge: Just another autorigger
###################################################################################################
`Online Documentation (ReadTheDocs) <http://rigforge.readthedocs.io/en/latest/>`_

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://raw.githubusercontent.com/AndresMWeber/Forge/master/LICENSE
    
.. image:: https://badge.fury.io/py/Forge.svg
    :target: https://badge.fury.io/py/Forge
    
.. image:: https://img.shields.io/github/issues/AndresMWeber/Forge.svg
    :target: https://github.com/AndresMWeber/Forge/issues
    
.. image:: https://circleci.com/gh/AndresMWeber/Forge.svg?style=shield&circle-token=:circle-token
    :target: https://circleci.com/gh/AndresMWeber/Forge/

.. image:: https://coveralls.io/repos/github/AndresMWeber/Forge/badge.svg?branch=master
    :target: https://coveralls.io/github/AndresMWeber/Forge?branch=master

.. image:: https://landscape.io/github/AndresMWeber/Forge/master/landscape.svg?style=flat
    :target: https://landscape.io/github/AndresMWeber/Forge/master
    
.. image:: https://codeclimate.com/github/AndresMWeber/Forge/badges/gpa.svg
   :target: https://codeclimate.com/github/AndresMWeber/Forge
   
.. image:: https://codeclimate.com/github/AndresMWeber/Forge/badges/issue_count.svg
   :target: https://codeclimate.com/github/AndresMWeber/Forge
   :alt: Issue Count
   
.. image:: https://www.versioneye.com/user/projects/593e29396725bd0060f1cdc4/badge.svg
    :target: https://www.versioneye.com/user/projects/593e29396725bd0060f1cdc4?child=summary

.. image:: https://api.codacy.com/project/badge/Grade/d19b2899a7b8415d960bfa4a5e580599
    :target: https://www.codacy.com/app/AndresMWeber/Forge?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=AndresMWeber/Forge&amp;utm_campaign=Badge_Grade

.. image:: https://img.shields.io/waffle/label/AndresMWeber/Forge/in%20progress.svg
    :target: https://waffle.io/AndresMWeber/Forge
    
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
