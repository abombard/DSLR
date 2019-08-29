import sys
import os
import numpy as np

import utils
from utils import error
import file
import logreg_train
import logreg_predict

feature_number = 13

def usage():
    error('%s [theta dataset]' % sys.argv[0])

def ask_marks():
    mark_matrix = np.zeros([feature_number + 1, 1])
    mark_matrix[0][0] = 1.0
    subject_list = ["Arithmancy", "Astronomy", "Herbology",             \
    "Defense Against the Dark Arts", "Divination", "Muggle Studies",    \
    "Ancient Runes", "History of Magic", "Transfiguration", "Potions",  \
    "Care of Magical Creatures", "Charms", "Flying"]
    i = 1
    print("Fill your marks")
    for subject in subject_list:
        loop = True
        while loop:
            try:
                mark = float(input(subject + ": "))
                if mark < 0.0 or mark > 20.0:
                    raise Exception()
                mark_matrix[i][0] = mark / 20.0
                i += 1
                loop = False
            except:
                print("mark must be a number between 0 and 20")
    return mark_matrix

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    if not os.path.isfile(sys.argv[1]):
        error('no such file: %s' % sys.argv[1])
    mark_matrix = ask_marks()
    theta_data = file.read_theta(sys.argv[1], feature_number + 1)
    houses = logreg_predict.logreg_predict(mark_matrix, theta_data)
    print("Sorting Hat: Hum, you will go to... " + houses[0] + "!")
    
