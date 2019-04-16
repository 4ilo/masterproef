from DetectionAngle import BoundingBox


def detect_objects(img_path):
    """ Stub yolo detector with annotation files """
    boxes = []

    # Get class names
    names = open("data/det.names").read().splitlines()

    for line in open("data/det/{}.txt".format(img_path.split('.')[0])):
        box = BoundingBox()
        data = [float(x) for x in line.rstrip().split(' ')]

        box.from_yolo(*data)
        box.class_id = names[int(box.class_id)]
        boxes.append(box)

    return boxes
