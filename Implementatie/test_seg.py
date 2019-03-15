import cv2
import argparse
import numpy as np

from ExpantionDetector.HoughDetector import HoughDetector
from ExpantionDetector.HighestPixel import HighestPixel
from segmentation.segmentation import run_segmentation


def get_floor_mask(img, floor_label=4):
    """ Create binary mask for floor pixels """
    n, h, w, c = img.shape

    mask = np.zeros((h, w), dtype=np.uint8)
    for j, j_val in enumerate(img[0, :, :, 0]):
        for i, i_val in enumerate(j_val):
            if i_val == floor_label:
                mask[j, i] = 1

    return mask


if __name__ == "__main__":
    # Parse input image_path
    parser = argparse.ArgumentParser(description="Do something")
    parser.add_argument('image_path', type=str, help="Path to input image")
    parser.add_argument('--output_path', type=str, default=False, help="Provide output path to save result")

    args = parser.parse_args()
    image_path = args.image_path

    # Run segmentation network on the image
    preds = run_segmentation(image_path)

    # Only select floor pixels
    mask = get_floor_mask(preds)

    img = cv2.imread(image_path)
    floor = cv2.bitwise_and(img, img, mask=mask)
    cv2.imshow("floor", floor)

    # Detect Expantion point with Hough lines
    hough = HoughDetector()
    intersections = hough.detect(mask)
    hough.render(img.copy())

    expantion = HighestPixel()
    expantion.detect(mask)
    img = expantion.render(img.copy())

    if args.output_path:
        cv2.imwrite(args.output_path, img)
    else:
        cv2.waitKey(0)
