import cv2
import itertools
import numpy as np
from .ExpantionDetector import ExpantionDetector


class HoughFloor(ExpantionDetector):
    def __init__(self):
        self.lines = []
        self.intersections = []

    def _remove_duplicates(self, diff=0.25):
        """ Remove lines with the same rico """

        def rico(line):
            return (line[1][1] - line[0][1]) / (line[1][0] - line[0][0])

        delete = []
        for (i1, line1), (i2, line2) in itertools.combinations(enumerate(self.lines), 2):
            rc1 = rico(line1)
            rc2 = rico(line2)

            if (rc1 + rc1 * diff) > rc2 > (rc1 - rc1 * diff) or (rc1 + rc1 * diff) < rc2 < (rc1 - rc1 * diff):
                delete.append(i1 if abs(rc1) < abs(rc2) else i2)

        self.lines = [self.lines[i] for i in range(len(self.lines)) if i not in delete]

    def _line_intersections(self):
        """ Calculate the intersection point for each line combination """
        intersections = []
        for line1, line2 in itertools.combinations(self.lines, 2):
            xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
            ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

            def det(a, b):
                return a[0] * b[1] - a[1] * b[0]

            div = det(xdiff, ydiff)
            if div == 0:
                raise Exception('lines do not intersect')

            d = (det(*line1), det(*line2))
            x = int(det(d, xdiff) / div)
            y = int(det(d, ydiff) / div)
            intersections.append((x, y))

        return intersections

    def render(self, img: np.ndarray) -> np.ndarray:
        """ Render detections onto the given image """
        for line in self.lines:
            cv2.line(img, line[0], line[1], (0, 0, 255), 1)

        intersections = self._line_intersections()

        for intersection in intersections:
            cv2.circle(img, intersection, 10, (0, 255, 0))

        cv2.imshow("ExpantionDetection", img)
        return img

    def detect(self, mask: np.ndarray):
        edges = cv2.Canny(mask, 0, 1, apertureSize=3)

        tresh = 50
        lines = cv2.HoughLines(edges, 1, np.pi / 180, tresh)
        while len(lines) > 10:
            tresh += 1
            lines = cv2.HoughLines(edges, 1, np.pi / 180, tresh)

        if lines is not None:
            for i in range(0, len(lines)):
                rho = lines[i][0][0]
                theta = lines[i][0][1]
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * (a)))
                pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * (a)))

                self.lines.append((pt1, pt2))

        self._remove_duplicates()
        intersections = self._line_intersections()

        for inter in intersections:
            self.intersections.append((inter[0]/mask.shape[1], inter[1]/mask.shape[0]))

        return self.intersections
