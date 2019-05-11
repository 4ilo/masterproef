import cv2
import argparse
import numpy as np
import matplotlib.pyplot as plt

from tqdm import tqdm
from os import listdir
from os.path import isfile, join

from ExpantionDetector.HoughFloor import HoughFloor
from ExpantionDetector.HighestPixel import HighestPixel
from segmentation.segmentation import Segmentation
from ExpantionDetector.HoughVanishing import HoughVanishing, transform


def test_hough(image_path, images):
    """ Test Hough transform vanishing point detector """
    errors = []

    print("HoughLines:")
    for image in tqdm(images):
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

    return errors


def test_seg_highest(mask, vanishing_point):
    """ Test 1 image with highest pixel segmentation """

    vanishing = HighestPixel()
    detection = vanishing.detect(mask)

    # Calculate error
    detection = np.array(detection)
    real = np.array(vanishing_point)

    return np.linalg.norm(real - detection)


def test_seg_hough(mask, vanishing_point):
    """ Test 1 image with Hough Transfrom on floor segmentation """

    vanishing = HoughFloor()
    detection = vanishing.detect(mask)

    if detection:
        # Calculate error
        detection = np.array(detection[0])
        real = np.array(vanishing_point)

        return np.linalg.norm(real - detection)

    return 1


def test_seg(image_path, images):
    """ Perform test with all techniques depending on floor segmentation """
    errors_hough = []
    errors_highest = []

    # Init segmentation network
    seg_network = Segmentation("{}/{}".format(image_path, images[0]))

    print("Seg network:")
    for image in tqdm(images):
        img = cv2.imread("{}/{}".format(image_path, image))

        # Run segmentation
        preds = seg_network.run(img)

        # Only select floor pixels
        mask = seg_network.get_floor_mask(preds)

        # Segmentation Hough
        errors_hough.append(test_seg_hough(mask, vanishing_points[image]))
        errors_highest.append(test_seg_highest(mask, vanishing_points[image]))

    return errors_highest, errors_hough


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

    # Run tests
    e1 = test_hough(args.input_path, images)
    e2, e3 = test_seg(args.input_path, images)

    # Plot
    plt.plot(e1)
    plt.plot(e2)
    plt.plot(e3)

    plt.xlabel("Test image")
    plt.ylabel("Euclidean error")
    plt.legend(['Hough transform: {}'.format(round(np.mean(e1), 3)), 'Seg Highest pixel: {}'.format(round(np.mean(e2),3)), 'Seg Hough: {}'.format(round(np.mean(e3),3))])
    plt.show()
