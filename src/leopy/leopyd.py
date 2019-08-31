#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import argparse
import ioflo.app.run

from ioflo.aid import odict
from ioflo.aid import consoling

from leopy import __version__


def parseArgs(version=__version__):
    d = "Runs leopy controller server. "
    d += "Example: app.py --port 8080'\n"
    p = argparse.ArgumentParser(description=d)
    p.add_argument('-V', '--version',
                   action='version',
                   version=version,
                   help="Prints out version of script runner.")
    p.add_argument('-v', '--verbose',
                   action='store',
                   default='concise',
                   choices=['0', '1', '2', '3', '4'].extend(consoling.VERBIAGE_NAMES),
                   help="Verbosity level.")
    p.add_argument('-P', '--port',
                   action='store',
                   default=8080,
                   help="Port number the server should listen on. Default is 8080.")

    args = p.parse_args()

    if args.verbose in consoling.VERBIAGE_NAMES:
        verbosage = consoling.VERBIAGE_NAMES.index(args.verbose)
    else:
        verbosage = int(args.verbose)

    args.verbose = verbosage  # converted value
    return args


def main():
    args = parseArgs(version=__version__)

    # src directory is projectDirpath
    projectDirpath = os.path.dirname(
        os.path.dirname(
            os.path.abspath(
                os.path.expanduser(__file__)
            )
        )
    )
    floScriptpath = os.path.join(projectDirpath, "leopy/flo/main.flo")

    ioflo.app.run.run(name="skedder",
                      period=0.0625,
                      real=True,
                      retro=True,
                      filepath=floScriptpath,
                      behaviors=['leopy.core'],
                      mode='',
                      username='',
                      password='',
                      verbose=args.verbose,
                      consolepath='',
                      statistics=False,
                      preloads=[
                          ('.main.server.port', odict(value=args.port))
                      ])


if __name__ == '__main__':
    main()
