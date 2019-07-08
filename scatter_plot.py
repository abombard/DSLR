#!/usr/bin/python3.7

import sys
import os
import matplotlib.pyplot as plt

import utils
from utils import error
import describe

def usage():
    error('%s [dataset]' % sys.argv[0])

def scatter(h1, f1, h2, f2, house):
    to_pop = [i for i in range(len(f1)) if not f1[i] or not f2[i]]
    f1_clean = [x for i, x in enumerate(f1) if i not in to_pop]
    f2_clean = [x for i, x in enumerate(f2) if i not in to_pop]
    house_clean = [x for i, x in enumerate(house) if i not in to_pop]

    plt.scatter([x for i, x in enumerate(f1_clean) if house_clean[i] == "Ravenclaw"], [x for i, x in enumerate(f2_clean) if house_clean[i] == "Ravenclaw"], alpha=0.8, c="green", edgecolor='none', s=30, label="Ravenclaw")
    plt.scatter([x for i, x in enumerate(f1_clean) if house_clean[i] == "Slytherin"], [x for i, x in enumerate(f2_clean) if house_clean[i] == "Slytherin"], alpha=0.8, c="red", edgecolor='none', s=30, label="Slytherin")
    plt.scatter([x for i, x in enumerate(f1_clean) if house_clean[i] == "Gryffindor"], [x for i, x in enumerate(f2_clean) if house_clean[i] == "Gryffindor"], alpha=0.8, c="blue", edgecolor='none', s=30, label="Gryffindor")
    plt.scatter([x for i, x in enumerate(f1_clean) if house_clean[i] == "Hufflepuff"], [x for i, x in enumerate(f2_clean) if house_clean[i] == "Hufflepuff"], alpha=0.8, c="yellow", edgecolor='none', s=30, label="Hufflepuff")
    plt.xlabel(h1)
    plt.ylabel(h2)
    plt.legend(loc=2)
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()
    if not os.path.isfile(sys.argv[1]):
        error('no such file: %s' % sys.argv[1])

    headers, features, is_numeric = describe.read_data(sys.argv[1])
    house = features[1]
    headers = headers[6:]
    features = features[6:]

    i1, i2 = 1, 3
    scatter(headers[i1], features[i1], headers[i2], features[i2], house)
    sys.exit(0)

    # test all features
    imax = len(features)
    for i1 in range(imax-1):
        h1 = headers[i1]
        for i2 in range(i1+1, imax):
            f1 = features[i1]
            h2 = headers[i2]
            f2 = features[i2]
            scatter(h1, f1, h2, f2, house)
    sys.exit(0)
