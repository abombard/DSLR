#!/usr/bin/python3.7

import sys
import os
import csv
import matplotlib
import matplotlib.pyplot as plt

import utils
from utils import error
import describe

def usage():
    error('%s [dataset]' % sys.argv[0])

def count_elem_in(List, Min, Max):
    count = 0
    for elem in List:
        if Min <= elem and elem <= Max:
            count += 1
    return count

def histogram(course, houses):
    stats = describe.stats(sys.argv[1])
    total = stats[course]["Count"]
    lims = [
        stats[course]["min"],
        stats[course]["min"] + (stats[course]["max"] - stats[course]["min"]) * 1 / 11,
        stats[course]["min"] + (stats[course]["max"] - stats[course]["min"]) * 2 / 11,
        stats[course]["min"] + (stats[course]["max"] - stats[course]["min"]) * 3 / 11,
        stats[course]["min"] + (stats[course]["max"] - stats[course]["min"]) * 4 / 11,
        stats[course]["min"] + (stats[course]["max"] - stats[course]["min"]) * 5 / 11,
        stats[course]["min"] + (stats[course]["max"] - stats[course]["min"]) * 6 / 11,
        stats[course]["min"] + (stats[course]["max"] - stats[course]["min"]) * 7 / 11,
        stats[course]["min"] + (stats[course]["max"] - stats[course]["min"]) * 8 / 11,
        stats[course]["min"] + (stats[course]["max"] - stats[course]["min"]) * 9 / 11,
        stats[course]["min"] + (stats[course]["max"] - stats[course]["min"]) * 10 / 11,
        stats[course]["max"],
    ]

    legend = [[], []]
    ind = [x for x in range(len(lims) - 1)]
    bottom = [0 for x in range(len(lims) - 1)]
    colors = {"Ravenclaw": "green", "Slytherin": "red", "Gryffindor": "blue", "Hufflepuff": "yellow"}
    for house, notes in houses.items():
        counts = [count_elem_in(notes, lims[i], lims[i+1]) / total * 100 for i in range(len(lims) - 1)]
        p = [plt.bar(ind, counts, width = 1, bottom=bottom, align='edge', color=colors[house])]
        bottom = [bottom[i] + counts[i] for i in range(len(lims) - 1)]
        legend[0] += [p[0]]
        legend[1] += [house]

    plt.title(course)
    plt.xticks([x for x in range(len(lims))], (["%.3f" % x for x in lims]))
    plt.legend(tuple(legend[0]), tuple(legend[1]))
    plt.show()

def main_pichu(filename):
    # checks
    if not os.path.isfile(filename):
        error('no such file: %s' % filename)

    header = []
    features = []

    # parser: csv to feature lists
    with open(filename, 'r') as fs:
        reader = csv.reader(fs)
        header = reader.__next__()
        header = header[6:]
        features = [ {"Ravenclaw": [], "Slytherin": [], "Gryffindor": [], "Hufflepuff":[] } for i in range(len(header)) ]
        is_numeric = [ False for i in range(len(header)) ]
        for line in reader:
            for i, field in enumerate(line):
                if i == 1:
                    house = field
                elif i >= 6 and field != "":
                    features[i - 6][house] += [float(field)]

    return (header, features)

if __name__ == '__main__':
    # checks
    if len(sys.argv) != 2:
        usage()
    if not os.path.isfile(sys.argv[1]):
        error('no such file: %s' % sys.argv[1])

    header, features = main_pichu(sys.argv[1])
    index = 0
    histogram(header[index], features[index])
