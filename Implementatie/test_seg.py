import cv2
import argparse
import numpy as np

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
    mask = get_floor_mask(preds)

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
    intersections = vanishing.detect(img)
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
    exit(0)

    boxes = []

    filename = image_path.split('.')[0]
    for line in open(filename+'.detect', 'r'):
        box = BoundingBox()
        data = [float(x) for x in line.rstrip().split(' ')]

        box.from_yolo(*data)
        boxes.append(box)

    for box in boxes:
        angle = DetectionAngle(intersections[0])
        ang = angle.calculate(box)
        print(ang)

        draw(img, box, intersections[0])

    if args.output_path:
        cv2.imwrite(args.output_path, img)
    else:
        cv2.waitKey(0)
