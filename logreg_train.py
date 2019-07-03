import sys
import os
import csv
import numpy as np

import utils
from utils import error
import describe
import histogram
import file

learning_rate = 0.01
logreg_iter_nb = 10000
housenames = ["Ravenclaw", "Slytherin", "Gryffindor", "Hufflepuff"]
theta_path = "theta.csv"

def usage():
    error('%s [dataset]' % sys.argv[0])

def scale(feature_matrix):
    min_matrix = np.min(feature_matrix, axis = 1).reshape(-1, 1)
    max_matrix = np.max(feature_matrix, axis = 1).reshape(-1, 1)
    scaled_feature_matrix = (feature_matrix - min_matrix) / (max_matrix - min_matrix)
    return scaled_feature_matrix

def calc_mean(feature):
    mean_feature = 0.0
    for v in feature:
        mean_feature += v
    mean_feature /= len(feature)
    return mean_feature

def calc_mean_features(features, feature_number):
    mean_features = [ { "Ravenclaw": 0, "Slytherin": 0, "Gryffindor": 0, "Hufflepuff": 0 } for i in range(feature_number) ]
    for i in range (len(features)):
        for housename in housenames:
            mean_features[i][housename] = calc_mean(features[i][housename])
    return mean_features

def g(z):
    return 1 / (1 + np.exp(-z))

def h(theta_matrix, x):
    return g(np.dot(theta_matrix.T, x))

def logreg_step(house, x, theta_matrix, y):
    m = float(len(theta_matrix[0]))
    diff = h(theta_matrix, x) - y
    sum_matrix = np.dot(x, diff.T)
    theta_matrix -= learning_rate / m * sum_matrix

def logreg(house, data, theta_matrix):
    y = np.empty([len(data["House"]), 1])
    for i in range(len(y)):
        y[i][0] = 1.0 if data["House"][i] == house else 0.0
    y = y.reshape(1, -1)
    for i in range(logreg_iter_nb):
        logreg_step(house, data["Features"], theta_matrix, y)

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
        data = { "House": [ "" for i in range(student_number)], "Features": np.empty([feature_number, student_number]) }
        i_line = 0
        for line in reader:
            for i, field in enumerate(line):
                if i == 1:
                    data["House"][i_line] = field
                elif i >= 6:
                    data["Features"][i - 6][i_line] = float(field) if field != "" else mean_features[i - 6][data["House"][i_line]]
            i_line += 1

    return data

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    if not os.path.isfile(sys.argv[1]):
        error('no such file: %s' % sys.argv[1])

    header_histo, features_histo = histogram.main_pichu(sys.argv[1])
    feature_number = len(header_histo)
    mean_features = calc_mean_features(features_histo, feature_number)
    data = main(sys.argv[1], feature_number, mean_features)
    data["Features"] = scale(data["Features"])
    data["Features"] = np.vstack((np.matrix(np.ones(len(data["Features"][0]))), data["Features"]))
    tn = feature_number + 1
    theta_data = { "Ravenclaw": np.empty([tn, 1]), "Slytherin": np.empty([tn, 1]), "Gryffindor": np.empty([tn, 1]), "Hufflepuff": np.empty([tn, 1]) }
    for house in housenames:
        logreg(house, data, theta_data[house])
    file.write_theta(theta_path, theta_data)
