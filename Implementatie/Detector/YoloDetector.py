import os
import cv2
from DetectionAngle import BoundingBox
from .darknet.Darknet import performDetect

CONFIG_PATH = "/darknet/all/"


def detect_objects(input_path, image):
    """ Run yolo detector on img_path """

    # Get darknet config dir
    darknet_dir = os.path.dirname(os.path.abspath(__file__)) + CONFIG_PATH

    # Get image width and height
    img_path = "{}/{}".format(input_path, image)
    img = cv2.imread(img_path)
    img_h, img_w = img.shape[:2]

    # Run darknet detector
    detections = performDetect(imagePath=img_path,
                               thresh=0.25,
                               configPath=darknet_dir + "cust.cfg",
                               weightPath=darknet_dir + "cust.weights",
                               metaPath=darknet_dir + "cust.data",
                               showImage=False)

    # Convert detections to BoundingBox format
    boxes = []
    for det in detections:
        box = BoundingBox()
        box.from_yolo(det[0], det[2][0]/img_w, det[2][1]/img_h, det[2][2]/img_w, det[2][3]/img_h)
        boxes.append(box)

    return boxes
