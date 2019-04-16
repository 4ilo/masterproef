import cv2
import argparse
from os import listdir
from os.path import isfile, join

from Detector import detect_objects
from DetectionAngle import DetectionAngle
from segmentation.segmentation import Segmentation
from ExpantionDetector.HighestPixel import HighestPixel


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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run implementation")
    parser.add_argument('input_path', type=str, help="Path to input images")

    args = parser.parse_args()

    # Get all images
    images = sorted([f for f in listdir(args.input_path) if isfile(join(args.input_path, f))])

    # Init segmentation network
    seg_network = Segmentation("{}/{}".format(args.input_path, images[0]))

    for image_path in images:
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

        cv2.imshow("test", img)

        cv2.waitKey(0)
