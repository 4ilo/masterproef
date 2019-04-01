from .BoundingBox import BoundingBox
import math

SENSOR_WIDTH = 3.68
SENSOR_HEIGHT = 2.76
SENSOR_W = 3280
SENSOR_H = 2464
FOCAL_LENGTH = 3.04


class DetectionAngle:
    def __init__(self, vanishing_point):
        self.vanishing_point = vanishing_point
        self._focal_length = (max(SENSOR_W, SENSOR_H) * FOCAL_LENGTH) / SENSOR_WIDTH

    def calculate(self, box: BoundingBox):
        """ Calculate the angle between the camera and the center of a detected object """
        diff = (box.center[0] - self.vanishing_point[0]) * SENSOR_W

        alpha = math.atan(diff/self._focal_length)
        return math.degrees(alpha)
