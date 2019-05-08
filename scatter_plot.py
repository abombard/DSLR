#!/usr/bin/python3.7

import sys
import os
import copy
import matplotlib.pyplot as plt

import utils
from utils import error
import describe

def usage():
    error('%s [dataset]' % sys.argv[0])

def scatter(h1, f1, h2, f2):
    f1 = copy.copy(f1)
    f2 = copy.copy(f2)

    to_pop = [i for i in range(len(f1)) if not f1[i] or not f2[i]]
    f1 = [x for i, x in enumerate(f1) if i not in to_pop]
    f2 = [x for i, x in enumerate(f2) if i not in to_pop]

    plt.scatter(f1, f2, alpha=0.8, c="green", edgecolor='none', s=30)
    plt.xlabel(h1)
    plt.ylabel(h2)
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()
    if not os.path.isfile(sys.argv[1]):
        error('no such file: %s' % sys.argv[1])

    headers, features, is_numeric = describe.main(sys.argv[1])
    headers = headers[6:]
    features = features[6:]

    i1, i2 = 1, 3
    scatter(headers[i1], features[i1], headers[i2], features[i2])
    sys.exit(0)

    # test all features
    imax = len(features)
    for i1 in range(imax-1):
        h1 = headers[i1]
        for i2 in range(i1+1, imax):
            f1 = features[i2]
            h2 = headers[i2]
            f2 = features[i2]
            scatter(h1, f1, h2, f2)
    sys.exit(0)
