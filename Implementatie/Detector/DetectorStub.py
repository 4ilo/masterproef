from DetectionAngle import BoundingBox


def detect_objects(img_path):
    """ Stub yolo detector with annotation files """
    boxes = []

    for line in open("data/det/{}.txt".format(img_path.split('.')[0])):
        box = BoundingBox()
        data = [float(x) for x in line.rstrip().split(' ')]

        box.from_yolo(*data)
        boxes.append(box)

    return boxes
