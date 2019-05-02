import cv2
import argparse
import numpy as np
from os import listdir
from os.path import isfile, join


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Combine images")
    parser.add_argument('image_path', type=str, help="Path to input images")
    parser.add_argument('output_file', type=str, help="Output file")
    parser.add_argument('--direction', type=str, default='h', help="Combining direction (h/v)")
    args = parser.parse_args()


    image_paths = sorted([f for f in listdir(args.image_path) if isfile(join(args.image_path, f))])
    images = []
    
    for path in image_paths:
        img = cv2.imread("{}/{}".format(args.image_path, path))
        images.append(img)
    

    if args.direction == 'h':
        axis = 1
    else:
        axis = 0

    vis = np.concatenate(tuple(images), axis=axis)
    cv2.imshow('out', vis)
    cv2.imwrite(args.output_file, vis)
    cv2.waitKey(0)