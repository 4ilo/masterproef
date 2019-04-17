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

    nodes = [-126565, -126574, -126583, -126592, -126601, -126610, -126619, -126628, -126637, -126646, -126655]
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
