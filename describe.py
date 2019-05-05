#!/usr/bin/python3.7

import os
import sys
import csv
import re
import math

from utils import error

def usage():
    error('%s [dataset]' % sys.argv[0])

re_dig = re.compile(r"[-]?\d+\.\d*")
def is_digit(s):
    return re_dig.match(s)

def clean_feature(feature, empty_is_valid=False, empty_default=0):
    if empty_is_valid:
        return [x if x else empty_default for x in feature]
    else:
        return [x for x in feature if x]

# {{{ describe

def describe_count(feature):
    i = 0
    for x in feature:
        i += 1
    return i

def describe_mean(feature):
    n = 0
    for x in feature:
        n += x
    return n / describe_count(feature)

def describe_std(feature):
    mean = describe_mean(feature)
    variance = 0
    for x in feature:
        variance += (x - mean) ** 2
    variance /= describe_count(feature) - 1
    return math.sqrt(variance)

def describe_min(feature):
    m = feature[0]
    for x in feature:
        if x < m:
            m = x
    return m

def describe_25(feature):
	index = (describe_count(feature) - 1) / 4
	index_dec = index % 1
	v_inf = sorted(feature)[int(index)]
	v_sup = sorted(feature)[int(index) + 1]
	return v_inf * (1 - index_dec) + v_sup * index_dec

def describe_50(feature):
	index = (describe_count(feature) - 1) / 2
	index_dec = index % 1
	v_inf = sorted(feature)[int(index)]
	v_sup = sorted(feature)[int(index) + 1]
	return v_inf * (1 - index_dec) + v_sup * index_dec

def describe_75(feature):
	index = (describe_count(feature) - 1) * 3 / 4
	index_dec = index % 1
	v_inf = sorted(feature)[int(index)]
	v_sup = sorted(feature)[int(index) + 1]
	return v_inf * (1 - index_dec) + v_sup * index_dec

def describe_max(feature):
    m = feature[0]
    for x in feature:
        if x > m:
            m = x
    return m

# }}}

todo = {
    'Count': describe_count,
    'Mean' : describe_mean,
    'Std'  : describe_std,
    'min'  : describe_min,
    '25%'  : describe_25,
    '50%'  : describe_50,
    '75%'  : describe_75,
    'max'  : describe_max,
}

def main(filename):
    # checks
    if not os.path.isfile(filename):
        error('no such file: %s' % filename)

    header = []
    features = []
    is_numeric = []

    # parser: csv to feature lists
    with open(filename, 'r') as fs:
        reader = csv.reader(fs)
        header = reader.__next__()
        features = [ [] for i in range(len(header)) ]
        is_numeric = [ False for i in range(len(header)) ]
        for line in reader:
            for i, field in enumerate(line):
                if is_digit(field):
                    is_numeric[i] = True
                    features[i] += [float(field)]
                else:
                    features[i] += [field]

    return (header, features, is_numeric)

def stats(filename):
    header, features, is_numeric = main(filename)

    # describe
    output = {
        header[i] : {
            stat : stat_describe(clean_feature(feature)) for stat, stat_describe in todo.items()
        } for i, feature in enumerate(features) if is_numeric[i]
    }
    return output

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()

    header, features, is_numeric = main(sys.argv[1])

    # print output
    fmtf = '%20.8f'
    fmts = '%20.19s'
    fmts2 = '%8s'
    sys.stdout.write(fmts2 % '')
    for i, head in enumerate(header):
        if is_numeric[i]: sys.stdout.write(fmts % head)
    sys.stdout.write('\n')

    for name, describe_function in todo.items():
        sys.stdout.write(fmts2 % name)
        for i, feature in enumerate(features):
            if is_numeric[i]:
                stat = describe_function(clean_feature(feature))
                sys.stdout.write(fmtf % stat)
        sys.stdout.write('\n')
