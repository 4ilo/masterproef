import cv2
import numpy as np
from .ExpantionDetector import ExpantionDetector
from ExpantionDetector.HoughVanishing import transform


class HighestPixel(ExpantionDetector):

    def __init__(self):
        self.expantion_point = False

    def render(self, img: np.ndarray) -> np.ndarray:
        """ Render detections onto the given image """
        cv2.circle(img, transform(self.expantion_point, img.shape), 10, (255, 0, 0))
        cv2.imshow("HighestPixel Expantion", img)

        return img

    def detect(self, mask: np.ndarray):
        # cv2.imshow("mask", mask*255)

        white_pixels = np.nonzero(mask)
        self.expantion_point = (white_pixels[1][0]/mask.shape[1], white_pixels[0][0]/mask.shape[0])

        return self.expantion_point
