#!/usr/bin/python3.7

import sys
import matplotlib
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

    # Generate a normal distribution, center at x=0m y=5
    fig, axs = plt.subplots(1, 2, sharey=True, tight_layout=True)

    x = [s for n, s in cvs.items()]
    y = [n for n, s in cvs.items()]
    n_bins = len(x)

    axs[0].hist(x, bins=n_bins)
    axs[1].hist(y, bins=n_bins)

    plt.show()
