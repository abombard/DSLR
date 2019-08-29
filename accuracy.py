import sys
import os
import numpy as np

import utils
from utils import error
import histogram
import file
import logreg_train
import logreg_predict

def usage():
    error('%s [train dataset] [theta dataset]' % sys.argv[0])

if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage()
    if not os.path.isfile(sys.argv[1]):
        error('no such file: %s' % sys.argv[1])
    if not os.path.isfile(sys.argv[2]):
        error('no such file: %s' % sys.argv[2])

    header_histo, features_histo = histogram.read_data(sys.argv[1])
    feature_number = len(header_histo)
    mean_features = logreg_train.calc_mean_features(features_histo, feature_number)
    data = logreg_predict.read_data(sys.argv[1], feature_number, mean_features)
    data_house = logreg_train.read_data(sys.argv[1], feature_number, mean_features)
    min_matrix = np.min(data_house["Features"], axis = 1).reshape(-1, 1)
    max_matrix = np.max(data_house["Features"], axis = 1).reshape(-1, 1)
    data = logreg_train.scale(data, min_matrix, max_matrix)
    data = np.vstack((np.matrix(np.ones(len(data[0]))), data))
    tn = feature_number + 1
    theta_data = file.read_theta(sys.argv[2], tn)
    houses = logreg_predict.logreg_predict(data, theta_data)

    l = len(houses)
    e = 0
    for i in range(l):
        if houses[i] != data_house["House"][i]:
            e += 1
    print("accuracy: %.2f%%" % ((l - e) / l * 100))   