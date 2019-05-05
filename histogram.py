#!/usr/bin/python3.7

import sys
import matplotlib.pyplot as plt

from utils import error
import describe

def usage():
    error('%s [dataset]' % sys.argv[0])

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()

    stats = describe.stats(sys.argv[1])
    cvs = { name : stat["Std"] / stat["Mean"] for name, stat in stats.items() }
    print(cvs)

    
