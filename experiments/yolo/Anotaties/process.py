#!/usr/bin/python3
import glob, os

current_dir = os.path.dirname(os.path.abspath(__file__))

path_data = 'data/oli/'

percentage_test = 15

file_train = open('train.txt', 'w')
file_test = open('test.txt', 'w')

counter = 1
index_test = round(100/percentage_test)
for pathAndName in glob.iglob(os.path.join(current_dir + '/Anotations_yolo', "*.txt")):
    title, ext = os.path.splitext(os.path.basename(pathAndName))

    if counter == index_test:
        counter = 1
        file_test.write(path_data + title + '.png\n')
    else:
        file_train.write(path_data + title + '.png\n')
        counter += 1
