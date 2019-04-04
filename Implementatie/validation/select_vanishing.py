#!/usr/bin/env python

import argparse
import cv2
import numpy as np

from os import listdir
from os.path import isfile, join

points = {}
current = ""
img = np.zeros((512, 512, 3), np.uint8)


def callback(event, x, y, flags, param):
    global points, current, img
    if event == cv2.EVENT_LBUTTONUP:
        cv2.circle(img, (x, y), 10, (255, 0, 0), 1)
        points[current] = (x/img.shape[1], y/img.shape[0])


def save(output_file):
    global points

    # Write values to file
    with open(output_file, 'w') as f:
        for key, val in points.items():
            f.write("{},{},{}\n".format(key, val[0], val[1]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Annotate vanishing point on images')
    parser.add_argument('input_dir')
    parser.add_argument('output_file')

    args = parser.parse_args()

    images = [f for f in listdir(args.input_dir) if isfile(join(args.input_dir, f))]

    cv2.namedWindow("image")
    cv2.setMouseCallback("image", callback)

    for i, image in enumerate(images):
        img = cv2.imread('{}/{}'.format(args.input_dir, image))
        current = image

        while(1):
            cv2.imshow("image", img)
            k = cv2.waitKey(1) & 0xFF
            if k == ord(' '):
                break

        if i%10 == 0:
            save(args.output_file)

    save(args.output_file)
