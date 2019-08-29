import sys
import numpy as np

import utils
from utils import error

housenames = ["Ravenclaw", "Slytherin", "Gryffindor", "Hufflepuff"]

def read_theta(theta_path, tn):
    try:
        with open(theta_path, "r") as theta_file:
            theta_file.readline()
            theta_data = { "Ravenclaw": np.zeros([tn, 1]), "Slytherin": np.zeros([tn, 1]), "Gryffindor": np.zeros([tn, 1]), "Hufflepuff": np.zeros([tn, 1]) }
            for i in range(4):
                theta_list = theta_file.readline().split(",")
                for i in range(tn):
                    theta_data[theta_list[0]][i][0] = theta_list[i + 1]
            theta_file.close()
    except:
        error("invalid theta file")
    return theta_data

def write_theta(theta_path, theta_data):
    try:
        with open(theta_path, "w") as theta_file:
            theta_file.write("house,theta_matrix\n")
            for house in housenames:
                theta_file.write(house + ",")
                for i in range(len(theta_data[house])):
                    theta_file.write(str(theta_data[house][i][0]))
                    if i < len(theta_data[house]) - 1:
                        theta_file.write(",")
                theta_file.write("\n")
            theta_file.close()
    except:
        error("open theta file failed")

def write_houses(houses):
    try:
        with open("houses.csv", "w") as houses_file:
            houses_file.write("Index,Hogwarts House\n")
            for i in range(len(houses)):
                houses_file.write(str(i) + "," + str(houses[i]) + "\n")
            houses_file.close()
    except:
        error("open houses file failed")
