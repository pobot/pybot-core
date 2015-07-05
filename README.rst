''pybot'' collection
====================

This package is part of POBOT's ``pybot`` packages collection, which aims
at gathering contributions created while experimenting with various technologies or
hardware in the context of robotics projects.

Although primarily focused on robotics applications (taken with its widest acceptation)
some of these contributions can be used in other contexts. Don't hesitate to keep us informed
on any usage you could have made.

Implementation note
-------------------

The collection code is organized using namespace packages, in order to group them in
a single tree rather that resulting in a invading flat collection. Please refer to the official
documentation at <https://www.python.org/dev/peps/pep-0382/> for details.

Package content
===============

General interest modules which are used by other packages of the collection.

At the time of writing, you'll find here :

  - helpers for command line parsers creation, proposing common options sur as debug mode
    activation, logging level setting,...
  - logging helpers, based on Python's logging module
  - helpers for dealing with simple configuration files

Installation
============

::

    $ cd <PROJECT_ROOT_DIR>
    $ python setup.py sdist
    $ pip install dist/*.tar.gz

Documentation
=============

Generation
----------

The documentation generation uses Sphinx (<http://sphinx-doc.org/>).
::

    $ cd <PROJECT_ROOT_DIR>/docs
    $ make html

It can be browsed online at : <http://pobot-pybot.github.io/pybot-core/>

Publication
-----------

The generated documentation can be published on github.io by using the ``buildandcommit`` make target. Beware
that the method used here is slightly different than the one described in article at
<http://daler.github.io/sphinxdoc-test/>.

Instead of modifying the Makefile for changing the ``BUILDDIR`` definition, it uses a symlink from the
``_build`` subdirectory to the the documentation sibling project used to updated the gh-pages branch.
The motivation is that users wanting to generate the documentation for local use only and without the intention
to modify it do not need to setup the gh-branch related stuff.

So, instead of modifying the Makefile as instructed, you only need to use the command:
::

    $ cd <PROJECT_ROOT_DIR>/docs
    $ rm -rf _build     # in case a previous build has created it
    $ ln -s ../../<PROJECT_DOCUMENTATION_ROOT_DIR> _build

As you could notice, this supposes you are using a Linux or similar development environment. Windows users will
have to adapt, by modifying the Makefile for instance. Maybe Windows links can do the trick too, but it's up
to you to investigate this, since Windows is no more my cup of tea since a while ;-)

Examples
========

*Under work*
