import sys
import os
import csv
import numpy as np

import utils
from utils import error
import describe
import histogram

housenames = ["Ravenclaw", "Slytherin", "Gryffindor", "Hufflepuff"]

def calc_mean(feature):
    mean_feature = 0.0
    for v in feature:
        mean_feature += v
    mean_feature /= len(feature)
    return mean_feature

def calc_mean_features(features, feature_number):
    mean_features = [ {"Ravenclaw": 0, "Slytherin": 0, "Gryffindor": 0, "Hufflepuff":0 } for i in range(feature_number) ]
    for i in range (len(features)):
        for housename in housenames:
            mean_features[i][housename] = calc_mean(features[i][housename])
    return mean_features

def main(filename, feature_number, mean_features):
    # checks
    if not os.path.isfile(filename):
        error('no such file: %s' % filename)

    # parser: csv to feature lists
    with open(filename, 'r') as fs:
        reader = csv.reader(fs)
        student_number = sum(1 for row in reader) - 1
        fs.seek(0)
        reader.__next__()
        features = [ { "House": "", "Marks": np.empty([feature_number, 1]) } for i in range(student_number) ]
        i_line = 0
        for line in reader:
            for i, field in enumerate(line):
                if i == 1:
                    features[i_line]["House"] = field
                elif i >= 6:
                    features[i_line]["Marks"][i - 6][0] = float(field) if field != "" else mean_features[i - 6][features[i_line]["House"]]
            i_line += 1

    return features

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    if not os.path.isfile(sys.argv[1]):
        error('no such file: %s' % sys.argv[1])

    header_histo, features_histo = histogram.main_pichu(sys.argv[1])
    feature_number = len(header_histo)
    mean_features = calc_mean_features(features_histo, feature_number)
    features = main(sys.argv[1], feature_number, mean_features)
