import sys
import os
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

if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage()
    if not os.path.isfile(sys.argv[1]):
        error('no such file: %s' % sys.argv[1])
    if not os.path.isfile(sys.argv[2]):
        error('no such file: %s' % sys.argv[2])

    header_histo, features_histo = histogram.main_pichu(sys.argv[1])
    feature_number = len(header_histo)
    mean_features = logreg_train.calc_mean_features(features_histo, feature_number)
    data = logreg_train.main(sys.argv[1], feature_number, mean_features)
    data["Features"] = logreg_train.scale(data["Features"])
    data["Features"] = np.vstack((np.matrix(np.ones(len(data["Features"][0]))), data["Features"]))
    tn = feature_number + 1
    theta_data = file.read_theta(sys.argv[2], tn)
    houses = logreg_predict(data["Features"], theta_data)
    file.write_houses(houses)
