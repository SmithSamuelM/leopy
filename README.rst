========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|
        |
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/leopy/badge/?style=flat
    :target: https://readthedocs.org/projects/leopy
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/SmithSamuelM/leopy.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/SmithSamuelM/leopy

.. |version| image:: https://img.shields.io/pypi/v/leopy.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/leopy

.. |commits-since| image:: https://img.shields.io/github/commits-since/SmithSamuelM/leopy/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/SmithSamuelM/leopy/compare/v0.1.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/leopy.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/leopy

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/leopy.svg
    :alt: Supported versions
    :target: https://pypi.org/project/leopy

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/leopy.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/leopy


.. end-badges

Search and change leopy to name of project repo etc.
Also files with leopy in them.
Change this readme

Hyperledger Aries Cloud Agent Controller Demo

* Free software: Apache Software License 2.0

Installation
============

::

    pip install leopy

Documentation
=============


https://leopy.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
