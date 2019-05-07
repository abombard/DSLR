#!/usr/bin/python3.7

import sys
import os
import matplotlib.pyplot as plt

import utils
from utils import error
import describe

def usage():
    error('%s [dataset]' % sys.argv[0])

if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()
    if not os.path.isfile(sys.argv[1]):
        error('no such file: %s' % sys.argv[1])

    headers, features, is_numeric = describe.main(sys.argv[1])
    headers = headers[6:]
    features = features[6:]

    i1, i2 = 1, 4
    f1 = describe.clean_feature(features[i1], empty_is_valid=True)
    f2 = describe.clean_feature(features[i2], empty_is_valid=True)

    plt.scatter(f1, f2, alpha=0.8, c="green", edgecolor='none', s=30)
    plt.xlabel(headers[i1])
    plt.ylabel(headers[i2])
    plt.show()
