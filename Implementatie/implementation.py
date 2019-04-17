import cv2
import argparse
import numpy as np
from os import listdir
from os.path import isfile, join

from Detector import detect_objects
from DetectionAngle import DetectionAngle
from segmentation.segmentation import Segmentation
from ExpantionDetector.HighestPixel import HighestPixel
from MapRenderer import MapRenderer


def get_vp(seg_network, img):
    """ Find the vanishing point """
    # Run segmentation
    preds = seg_network.run(img)

    # Only select floor pixels
    mask = seg_network.get_floor_mask(preds)

    # Use HighestPixel detector
    vanishing = HighestPixel()
    vp = vanishing.detect(mask)
    cv2.circle(img, (int(img.shape[1] / 2), int(img.shape[0] / 2)), 10, (0, 0, 255))
    vanishing.render(img)

    return vp


def render_result(img, fig):
    """
    Show the result image and route on the same frame
    :param img: Result image
    :param fig: Route on map
    :return: Combined image
    """
    # Resize fig to height of image
    ratio = img.shape[0] / fig.shape[0]
    dim = (int(fig.shape[1] * ratio), img.shape[0])
    fig_small = cv2.resize(fig, dim, interpolation=cv2.INTER_AREA)

    # Combine img and fig onto same frame
    figure = np.concatenate((img, fig_small), axis=1)
    cv2.imshow("Result", figure)
    return figure


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run implementation")
    parser.add_argument('input_path', type=str, help="Path to input images")

    args = parser.parse_args()

    # Get all images
    images = sorted([f for f in listdir(args.input_path) if isfile(join(args.input_path, f))])

    # Init segmentation network
    seg_network = Segmentation("{}/{}".format(args.input_path, images[0]))

    nodes = [4427,-137923,-137925,-137927,-137931,-137933,-137935,-137939,-137941,-137943,-137945,-137947,-137949,-137951,-137953,-137955,-137957,-137959,-137961,-137963,-137965,-137967,-137969,-137971,-137973,-137975,-137977,-137979,-137981,-137983,-137985,-137987,-137989,-137991,-137993,-137995,-137997,-137999,-138001,-138003,-138005,-138007,-138009,-138011,-138013,-138015,-138017,-138019,-138023,-138021,-138025,-138027,-138029,]
    mr = MapRenderer("data/map.osm")

    for i, image_path in enumerate(images):
        img = cv2.imread("{}/{}".format(args.input_path, image_path))

        # Run object detector
        objects = detect_objects(image_path)

        # Find vanishing point
        vp = get_vp(seg_network, img)

        # Calculate image offset
        angle_det = DetectionAngle(vp)
        img_offset = angle_det.calculate_offset()
        print(img_offset)

        # Calculate angle for each detection
        for obj in objects:
            angle = angle_det.calculate(obj)
            obj.render(img, text="%.3f" % angle)

        fig = mr.show_route(nodes[i % len(nodes)])

        render_result(img, fig)

        cv2.waitKey(0)
