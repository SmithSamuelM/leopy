[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

[![Documentation Status](https://readthedocs.org/projects/leopy/badge/?style=flat)](https://readthedocs.org/projects/leopy)

[![PyPI Package latest release](https://img.shields.io/pypi/v/leopy.svg)](https://pypi.org/project/leopy)

[![Commits since latest release](https://img.shields.io/github/commits-since/SmithSamuelM/leopy/v0.1.1.svg)](https://github.com/SmithSamuelM/leopy/compare/v0.1.1...master)

[![PyPI Wheel](https://img.shields.io/pypi/wheel/leopy.svg)](https://pypi.org/project/leopy)

[![Supported versions](https://img.shields.io/pypi/pyversions/leopy.svg)](https://pypi.org/project/leopy)

[![Supported implementations](https://img.shields.io/pypi/implementation/leopy.svg)](https://pypi.org/project/leopy)

[![Travis-CI Build Status](https://travis-ci.org/SmithSamuelM/leopy.svg?branch=master)](https://travis-ci.org/SmithSamuelM/leopy)



# Hyperledger Aries Cloud Agent Controller Demo



Search and change leopy to name of project repo etc.
Also files with leopy in them.
Change this readme

* Free software: Apache Software License 2.0

## Installation

Clone this repo

```bash
$ cd /.../leopy/src/
$ python3 -m leopy.leopyd -v 1
```

Navigate browser to

http://localhost:8080/events

to see SSE stream of events sent by Agent to Controller



To use pip install

```bash
$ pip3 install leopy
```

Then from command line

```bash
$ leopyd -v 1

```

For help

```bash

$ leopyd -h

usage: leopyd [-h] [-V] [-v VERBOSE] [-P PORT]

Runs leopy controller server. Example: app.py --port 8080'

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         Prints out version of script runner.
  -v VERBOSE, --verbose VERBOSE
                        Verbosity level.
  -P PORT, --port PORT  Port number the server should listen on. Default is
                        8080.
```


## Documentation


https://leopy.readthedocs.io/


## Development


To run the all tests run::

```bash

$    tox
```

Note, to combine the coverage data from all the tox environments run:

```bash
$ PYTEST_ADDOPTS=--cov-append tox
```

