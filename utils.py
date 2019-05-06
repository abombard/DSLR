#!/usr/bin/python3.7

import sys
import re

def error(*args):
    print('error: %s' % args, file=sys.stderr)
    sys.exit(1)

re_dig = re.compile(r"[-]?\d+\.\d*")
def is_digit(s):
    return re_dig.match(s)

