#!/usr/bin/python3.7

import sys

def error(*args):
    print('error: %s' % args, file=sys.stderr)
    sys.exit(1)

