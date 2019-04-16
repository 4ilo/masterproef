
import cv2
from ExpantionDetector.HoughVanishing import transform


class BoundingBox:
    def __init__(self, x=None, y=None, w=None, h=None, class_id=None):
        self.class_id = class_id
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def from_yolo(self, class_id, x_c, y_c, w, h):
        """ Initialise class from darknet annotaion fromat """
        self.class_id = class_id

        self.w = w
        self.h = h
        self.x = x_c - w / 2
        self.y = y_c - h / 2

    def render(self, img, color=(0, 255, 0), text=None):
        """ Render bounding box onto image """
        cv2.rectangle(img, transform(self._tl(), img.shape), transform(self._br(), img.shape), color, 1)

        if text is not None:
            cv2.putText(img, text, transform(self.center, img.shape), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
        return img

    @property
    def center(self):
        """ Get center of boundign box """
        return self.x + self.w/2, self.y + self.h/2

    def _tl(self):
        """ Get top left corner """
        return self.x, self.y

    def _br(self):
        """ Get bottom right corner """
        return self.x + self.w, self.y + self.h

    def __repr__(self):
        return "x: {}, y: {}, w: {}, h:{}".format(self.x, self.y, self.w, self.h)


