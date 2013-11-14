#!/usr/bin/env python

import os
import sys
from lib.pidtrk import *


def main():
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError, e:
        sys.exit(1)

    os.chdir('/')
    os.setsid()
    os.umask(0)

    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError, e:
        sys.exit(1)

    ptrk = ProcessTrack()
    ptrk.process_poll()

if __name__ == '__main__':
    main()
