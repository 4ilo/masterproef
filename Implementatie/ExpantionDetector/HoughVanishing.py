import cv2
import numpy as np
from .ExpantionDetector import ExpantionDetector


def transform(point: tuple, shape: tuple) -> tuple:
    """ Transform point in relative coordinates to absolute coordinates """
    return tuple((point * np.flip(shape[:2])).astype(int))


class HoughVanishing(ExpantionDetector):
    def __init__(self):
        self.std_dev = 0.34
        self.houghlines_divisor = 10
        self.min_crossing_angle = 1
        self.theta_tresh = 0.2

        self.lines = []
        self.intersections = []

    def _prepare(self, img):
        """ Prepare image for detection """
        # Resize image
        scale = 1000 / img.shape[1]
        img = cv2.resize(img, (0, 0), fx=scale, fy=scale)

        # Convert to grayscale
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Blur image to reduce noise
        img_blur = cv2.blur(img_gray, (3, 3))

        return img, img_gray, img_blur

    def _calc_treshold(self, img_gray):
        """ Calculate a threshold for edge detection based on the median grayscale value """
        vector = np.reshape(img_gray, img_gray.shape[0] * img_gray.shape[1])
        median = np.median(vector)

        low_tresh = median / self.std_dev
        high_tresh = median * self.std_dev

        return low_tresh, high_tresh

    def detect(self, orig: np.ndarray) -> list:
        """
        Perform the vanishing point detection
        :param orig: Input image
        :return: List of (relative to w and h) vanishing point possibilitys
        """

        # Prepare image for detection
        img, img_gray, img_blur = self._prepare(orig)

        # Calculate thresholds for Canny edge detector
        thresh_l, thresh_h = self._calc_treshold(img_gray)

        # Detect edges using Canny, and appy mask to grayscale image
        mask = cv2.Canny(img_blur, thresh_l, thresh_h, 3)
        img_edges = cv2.bitwise_and(img_gray, img_gray, mask=mask)

        # Detect lines using Hough transform
        hough_tresh = int(np.sqrt(((img.shape[0] * img.shape[0]) + (img.shape[1] * img.shape[1]))) / self.houghlines_divisor)
        lines = cv2.HoughLines(img_edges, 1, np.pi / 180, hough_tresh)

        if lines is not None:
            for i in range(len(lines)):
                rho1 = lines[i][0][0]
                theta1 = lines[i][0][1]

                # Don't use horizontal and vertical lines
                if (theta1 > (0 + self.theta_tresh)) and (theta1 < (np.pi / 2 - self.theta_tresh)) or (
                        theta1 > ((np.pi / 2) + self.theta_tresh)) and (theta1 < (np.pi - self.theta_tresh)):
                    costheta1 = np.cos(theta1)
                    sintheta1 = np.sin(theta1)
                    x0 = costheta1 * rho1
                    y0 = sintheta1 * rho1

                    height, width, _ = img.shape
                    pt1 = ((x0 + 1000 * (-sintheta1)) / width, (y0 + 1000 * costheta1) / height)
                    pt2 = ((x0 - 1000 * (-sintheta1)) / width, (y0 - 1000 * costheta1) / height)

                    self.lines.append((pt1, pt2))

                    # Check every line combination
                    for j in range(i + 1):
                        rho2 = lines[j][0][0]
                        theta2 = lines[j][0][1]
                        costheta2 = np.cos(theta2)
                        sintheta2 = np.sin(theta2)

                        # Don't use lines that are the same
                        if (abs(theta1) - abs(theta2)) < self.min_crossing_angle:
                            break

                        det = (costheta1 * sintheta2) - (sintheta1 * costheta2)
                        intersection_x = (((sintheta2 * rho1) - (sintheta1 * rho2)) / det) / width
                        intersection_y = (((-costheta2 * rho1) + (costheta1 * rho2)) / det) / height

                        self.intersections.append((intersection_x, intersection_y))

        return self.intersections

    def render(self, img: np.ndarray) -> np.ndarray:
        """ Render the vanishing points onto the given frame """
        for point in self.intersections:
            cv2.circle(img, transform(point, img.shape), 10, (0, 0, 255))

        # for line in self.lines:
        #     cv2.line(img, transform(line[0], img.shape), transform(line[1], img.shape), (255, 0, 0), 5)

        return img
