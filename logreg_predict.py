import sys
import os
import csv
import numpy as np

import utils
from utils import error
import describe
import histogram
import file
import logreg_train

housenames = ["Ravenclaw", "Slytherin", "Gryffindor", "Hufflepuff"]

def usage():
    error('%s [dataset] [theta dataset]' % sys.argv[0])

def logreg_predict(features, theta_features):
    predicted_houses = [ "" for i in range(features.shape[1]) ]
    for i in range(features.shape[1]):
        max_p = 0.0
        for house in housenames:
            p = logreg_train.h(theta_features[house], features[:, i].reshape(-1,1))
            if p > max_p:
                max_p = p
                predicted_houses[i] = house

    return predicted_houses

def read_data(filename, feature_number, mean_features):
    # checks
    if not os.path.isfile(filename):
        error('no such file: %s' % filename)

    # parser: csv to feature lists
    try:
        with open(filename, 'r') as fs:
            reader = csv.reader(fs)
            student_number = sum(1 for row in reader) - 1
            fs.seek(0)
            reader.__next__()
            data = np.zeros([feature_number, student_number])
            i_line = 0
            for line in reader:
                for i, field in enumerate(line):
                    if i >= 6:
                        data[i - 6][i_line] = float(field) if field != "" else mean_features[i - 6]
                i_line += 1
    except:
        error("invalid dataset")

    return data

if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage()
    if not os.path.isfile(sys.argv[1]):
        error('no such file: %s' % sys.argv[1])
    if not os.path.isfile(sys.argv[2]):
        error('no such file: %s' % sys.argv[2])

    train_file = "resources/dataset_train.csv"
    header_histo, features_histo = histogram.read_data(train_file)
    feature_number = len(header_histo)
    mean_features = logreg_train.calc_mean_features(features_histo, feature_number)
    data = read_data(sys.argv[1], feature_number, mean_features)
    train_data = logreg_train.read_data(train_file, feature_number, mean_features)
    min_matrix = np.min(train_data["Features"], axis = 1).reshape(-1, 1)
    max_matrix = np.max(train_data["Features"], axis = 1).reshape(-1, 1)
    data = logreg_train.scale(data, min_matrix, max_matrix)
    data = np.vstack((np.matrix(np.ones(len(data[0]))), data))
    tn = feature_number + 1
    theta_data = file.read_theta(sys.argv[2], tn)
    houses = logreg_predict(data, theta_data)
    file.write_houses(houses)
