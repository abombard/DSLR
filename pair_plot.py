#!/usr/bin/python3.7

import sys
import os
import matplotlib.pyplot as plt

import utils
from utils import error
import describe
import histogram

def usage():
    error('%s [dataset]' % sys.argv[0])

housenames = ["Ravenclaw", "Slytherin", "Gryffindor", "Hufflepuff"]
housecolors = ["green", "red", "blue", "yellow"]

def pair_histogram(course, houses, i1, i2, imax):
    stats = describe.stats(sys.argv[1])
    total = stats[course]["Count"]

    Min = stats[course]["min"]
    Max = stats[course]["max"]
    D   = Max - Min
    lims = [Min + D * i / 11 for i in range(12)]

    ind = [x for x in range(len(lims) - 1)]
    bottom = [0 for x in range(len(lims) - 1)]
    colors = { housenames[i]: housecolors[i] for i in range(len(housenames)) }
    for house, notes in houses.items():
        counts = [histogram.count_elem_in(notes, lims[i], lims[i+1]) / total * 100 for i in range(len(lims) - 1)]
        p = [plt.bar(ind, counts, width = 1, bottom=bottom, align='edge', color=colors[house])]
        bottom = [bottom[i] + counts[i] for i in range(len(lims) - 1)]
    if i1 == (imax - 1):
        plt.xticks([x for x in (3, len(lims) - 1)], (["%.3f" % x for x in [lims[3], lims[-1]]]))
        plt.xlabel(course, fontsize=6)
    else:
        plt.xticks([])
    plt.ylabel(course[0:10], fontsize=6) if i2 == 0 else plt.yticks([])

def pair_scatter(h2, f2, h1, f1, house, i1, i2, imax):
    to_pop = [i for i in range(len(f1)) if not f1[i] or not f2[i]]
    f1_clean = [x for i, x in enumerate(f1) if i not in to_pop]
    f2_clean = [x for i, x in enumerate(f2) if i not in to_pop]
    house_clean = [x for i, x in enumerate(house) if i not in to_pop]

    plt.scatter([x for i, x in enumerate(f1_clean) if house_clean[i] == "Ravenclaw"], [x for i, x in enumerate(f2_clean) if house_clean[i] == "Ravenclaw"], alpha=0.8, c="green", edgecolor='none', s=5, label="Ravenclaw")
    plt.scatter([x for i, x in enumerate(f1_clean) if house_clean[i] == "Slytherin"], [x for i, x in enumerate(f2_clean) if house_clean[i] == "Slytherin"], alpha=0.8, c="red", edgecolor='none', s=5, label="Slytherin")
    plt.scatter([x for i, x in enumerate(f1_clean) if house_clean[i] == "Gryffindor"], [x for i, x in enumerate(f2_clean) if house_clean[i] == "Gryffindor"], alpha=0.8, c="blue", edgecolor='none', s=5, label="Gryffindor")
    plt.scatter([x for i, x in enumerate(f1_clean) if house_clean[i] == "Hufflepuff"], [x for i, x in enumerate(f2_clean) if house_clean[i] == "Hufflepuff"], alpha=0.8, c="yellow", edgecolor='none', s=5, label="Hufflepuff")
    plt.xlabel(h1, fontsize=6) if i1 == (imax - 1) else plt.xticks([])
    plt.ylabel(h2[0:10], fontsize=6) if i2 == 0 else plt.yticks([])

if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()
    if not os.path.isfile(sys.argv[1]):
        error('no such file: %s' % sys.argv[1])

    header_histo, features_histo = histogram.read_data(sys.argv[1])
    headers, features, is_numeric = describe.read_data(sys.argv[1])
    house = features[1]
    headers = headers[6:]
    features = features[6:]
    imax = len(features)
    for i1 in range(imax):
        h1 = headers[i1]
        for i2 in range(imax):
            f1 = features[i1]
            h2 = headers[i2]
            f2 = features[i2]
            ax = plt.subplot(13, 13, i1 * 13 + i2 + 1)
            if i1 != i2: pair_scatter(h1, f1, h2, f2, house, i1, i2, imax)
            else: pair_histogram(header_histo[i1], features_histo[i1], i1, i2, imax)
    # fig_manager = plt.get_current_fig_manager()
    # fig_manager.window.showMaximized()
    plt.suptitle("Pair Plot")
    leg = plt.legend(tuple(housenames), loc='upper right')
    plt.draw()


    # Get the bounding box of the original legend
    bb = leg.get_bbox_to_anchor().inverse_transformed(ax.transAxes)

    # Change to location of the legend. 
    xOffset = 1.5
    bb.x0 += xOffset
    bb.x1 += xOffset
    leg.set_bbox_to_anchor(bb, transform = ax.transAxes)


    plt.show()

