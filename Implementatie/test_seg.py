import cv2
import argparse
import numpy as np

from ExpantionDetector.HoughFloor import HoughFloor
from ExpantionDetector.HighestPixel import HighestPixel
from segmentation.segmentation import Segmentation
from ExpantionDetector.HoughVanishing import HoughVanishing, transform


from DetectionAngle import *


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


if __name__ == "__main__":
    # Parse input image_path
    parser = argparse.ArgumentParser(description="Do something")
    parser.add_argument('image_path', type=str, help="Path to input image")
    parser.add_argument('--output_path', type=str, default=False, help="Provide output path to save result")

    args = parser.parse_args()
    image_path = args.image_path

    img = cv2.imread(image_path)

    # Init segmentation network
    seg_network = Segmentation(image_path)

    # Run segmentation
    preds = seg_network.run(img)

    # Only select floor pixels
    mask = seg_network.get_floor_mask(preds)

    floor = cv2.bitwise_and(img, img, mask=mask)
    cv2.imshow("floor", floor)

    # Detect Expantion point with Hough lines
    hough = HoughFloor()
    intersections = hough.detect(mask)
    img1 = hough.render(img.copy())

    expantion = HighestPixel()
    expantion.detect(mask)
    img3 = expantion.render(img.copy())

    vanishing = HoughVanishing()
    detection = vanishing.detect(img)
    img2 = img.copy()
    img2 = vanishing.render(img2)
    cv2.imshow("HoughVanishing", img2)

    img1 = cv2.resize(img1, (640, 360))
    img2 = cv2.resize(img2, (640, 360))
    img3 = cv2.resize(img3, (640, 360))

    vis = np.concatenate((img1, img3, img2), axis=0)
    cv2.imshow("test", vis)
    cv2.imwrite("validation/3.png", vis)

    cv2.waitKey(0)
