import cv2
import argparse
import numpy as np

import matplotlib.pyplot as plt

from os import listdir
from os.path import isfile, join

from ExpantionDetector.HoughFloor import HoughFloor
from ExpantionDetector.HighestPixel import HighestPixel
from segmentation.segmentation import Segmentation
from ExpantionDetector.HoughVanishing import HoughVanishing, transform


from DetectionAngle import *


def get_floor_mask(img, floor_label=4):
    """ Create binary mask for floor pixels """
    n, h, w, c = img.shape

    mask = np.zeros((h, w), dtype=np.uint8)
    for j, j_val in enumerate(img[0, :, :, 0]):
        for i, i_val in enumerate(j_val):
            if i_val == floor_label:
                mask[j, i] = 1

    return mask


def draw(img, box, vanishing_point):
    temp = img.copy()
    # Draw box
    temp = box.render(temp, color=(0, 255 - (box.class_id * 50), 0))

    # Draw line to box
    cv2.line(temp, transform(box.center, img.shape), transform(vanishing_point, img.shape), (255, 0, 0,), 1)

    # draw vanishing point
    cv2.circle(temp, transform(vanishing_point, img.shape), 10, (0, 0, 255))

    cv2.imshow('temp', temp)
    cv2.waitKey(0)


def printProgressBar (iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
    # Print New Line on Complete
    if iteration == total:
        print()


def test_hough(image_path, images):
    errors = []
    length = len(images)

    for i, image in enumerate(images):
        printProgressBar(i+1, length, prefix="HoughLines:", suffix='Complete', length=50)

        img = cv2.imread("{}/{}".format(image_path, image))
        vanishing = HoughVanishing()
        detection = vanishing.detect(img)

        if detection:
            detection = np.array(detection[0])
            real = np.array(vanishing_points[image])

            error = np.linalg.norm(real - detection)
            errors.append(error)

        else:
            errors.append(1)

    plt.plot(errors)
    plt.xlabel("Test image")
    plt.ylabel("Euclidean error")
    plt.show()


def test_seg_highest(image_path, images):
    errors = []
    length = len(images)

    # Init segmentation network
    seg_network = Segmentation("{}/{}".format(image_path, images[0]))

    for i, image in enumerate(images):
        printProgressBar(i + 1, length, prefix="HighestPixel:", suffix='Complete', length=50)

        img = cv2.imread("{}/{}".format(image_path, image))

        # Run segmentation
        preds = seg_network.run(img)

        # Only select floor pixels
        mask = get_floor_mask(preds)

        vanishing = HighestPixel()
        detection = vanishing.detect(mask)

        # Calculate error
        detection = np.array(detection)
        real = np.array(vanishing_points[image])

        error = np.linalg.norm(real - detection)
        errors.append(error)

    plt.plot(errors)
    plt.xlabel("Test image")
    plt.ylabel("Euclidean error")
    plt.show()


def test_seg_hough(image_path, images):
    errors = []
    length = len(images)

    # Init segmentation network
    seg_network = Segmentation("{}/{}".format(image_path, images[0]))

    for i, image in enumerate(images):
        printProgressBar(i + 1, length, prefix="SegHough:", suffix='Complete', length=50)

        img = cv2.imread("{}/{}".format(image_path, image))

        # Run segmentation
        preds = seg_network.run(img)

        # Only select floor pixels
        mask = get_floor_mask(preds)

        # Detect Expantion point with Hough lines
        vanishing = HoughFloor()
        detection = vanishing.detect(mask)

        if detection:
            # Calculate error
            detection = np.array(detection[0])
            real = np.array(vanishing_points[image])

            error = np.linalg.norm(real - detection)
            errors.append(error)

        else:
            errors.append(1)

    plt.plot(errors)
    plt.xlabel("Test image")
    plt.ylabel("Euclidean error")
    plt.show()


if __name__ == "__main__":
    # Parse input image_path
    parser = argparse.ArgumentParser(description="Validate all vanishing_point detectors")
    parser.add_argument('input_path', type=str, help="Path to input images")
    parser.add_argument('vanishing_points', type=str, help="File with vanishing points")
    args = parser.parse_args()

    vanishing_points = {}

    # Open vanishing point file and load the points
    for point in open(args.vanishing_points).readlines():
        data = point.strip().split(',')
        vanishing_points.update({
            data[0]: (float(data[1]), float(data[2]))
        })

    # Get all images from input folder
    images = [f for f in listdir(args.input_path) if isfile(join(args.input_path, f))]

    # test_hough(args.input_path, images)
    # test_seg_highest(args.input_path, images)
    test_seg_hough(args.input_path, images)
