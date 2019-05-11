import os
import cv2
import time
import argparse
import numpy as np
from tqdm import tqdm
from os import listdir
import matplotlib.pyplot as plt
from os.path import isfile, join

from ExpantionDetector.HoughFloor import HoughFloor
from ExpantionDetector.HighestPixel import HighestPixel
from segmentation.segmentation import Segmentation
from ExpantionDetector.HoughVanishing import HoughVanishing, transform

if __name__ == "__main__":
    print("##### FORCE CPU WITH \"FORCE_CPU=1\" ENV VARIABLE ######")
    parser = argparse.ArgumentParser(description='Get average vp calculation time')
    parser.add_argument('img_path', help="Path to image files")
    args = parser.parse_args()

    # Get all images
    images = sorted([args.img_path + "/" + f for f in listdir(args.img_path) if isfile(join(args.img_path, f))])
    images = images[:100]

    highest_data = []

    # Init network
    seg_network = Segmentation(images[0])
    img = cv2.imread(images[0])
    preds = seg_network.run(img)

    # Run highest pixel
    print("Highest pixel segmentation")
    for img in tqdm(images):
        start = time.time()

        img = cv2.imread(img)

        # Run segmentation
        preds = seg_network.run(img)

        # Only select floor pixels
        mask = seg_network.get_floor_mask(preds)

        # Segmentation highest pixel
        vanishing = HighestPixel()
        detection = vanishing.detect(mask)

        end = time.time()
        highest_data.append(end-start)


    hough_seg_data = []
    # Run hough segmentation
    print("Hough segmentation")
    for img in tqdm(images):
        start = time.time()

        img = cv2.imread(img)

        # Run segmentation
        preds = seg_network.run(img)

        # Only select floor pixels
        mask = seg_network.get_floor_mask(preds)

        # Segmentation highest pixel
        vanishing = HoughFloor()
        detection = vanishing.detect(mask)

        end = time.time()
        hough_seg_data.append(end-start)


    hough_data = []
    # Run hough 
    print("Hough")
    for img in tqdm(images):
        start = time.time()

        img = cv2.imread(img)
        vanishing = HoughVanishing()
        detection = vanishing.detect(img)

        end = time.time()
        hough_data.append(end-start)


    print("Mean Higest pixel: {}".format(np.mean(highest_data)))

    print("Mean Hough seg: {}".format(np.mean(hough_seg_data)))

    print("Mean Hough: {}".format(np.mean(hough_data)))