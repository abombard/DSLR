import sys
import numpy as np

def read_theta(theta_path, theta_number):
    try:
        with open(theta_path, "r") as theta_file:
            theta_file.readline()
            theta_list = theta_file.readline().split(",")
            theta_matrix = np.empty([theta_number, 1])
            for i in range(len(theta_matrix)):
                theta_matrix[i][0] = theta_list[i]
            theta_file.close()
    except:
        theta_matrix = np.empty([theta_number, 1])
    return theta_matrix

def write_theta(theta_path, theta_matrix):
    try:
        with open(theta_path, "w") as theta_file:
            theta_file.write("theta\n")
            for i in range(len(theta_matrix)):
                theta_file.write(str(theta_matrix[i][0]))
                if i < len(theta_matrix) - 1:
                    theta_file.write(",")
            theta_file.write("\n")
            theta_file.close()
    except:
        print("open theta file failed")
        exit(1)
