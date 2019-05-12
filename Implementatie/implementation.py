import cv2
import time
import logging
import argparse
import numpy as np
from os import listdir
from os.path import isfile, join

from MapParser import parse_map
from MapRenderer import MapRenderer
from Detector import detect_objects
from DetectionAngle import DetectionAngle
from segmentation.segmentation import Segmentation
from ExpantionDetector.HighestPixel import HighestPixel

logging.basicConfig(level=logging.WARNING)


def get_vp(seg_network, img):
    """ Find the vanishing point """
    # Run segmentation
    preds = seg_network.run(img)

    # Only select floor pixels
    mask = seg_network.get_floor_mask(preds)

    # Use HighestPixel detector
    vanishing = HighestPixel()
    vp = vanishing.detect(mask)
    cv2.drawMarker(img, (int(img.shape[1] / 2), int(img.shape[0] / 2)), (0, 70, 255), cv2.MARKER_CROSS, 10, 1)
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


def cost(node, detections):
    # filters = ['light', 'smoke_detector', 'exit_sign']
    filters = ['light']
    # split into categories
    data = node.split(filters)

    # Split detections into categories
    data2 = {}
    for f in filters:
        data2.update({
            f: [x for x, _ in detections.items() if x.class_id == f]
        })

    # Link detections to data
    matches = {}
    for f, cat in data.items():
        for obj in cat:
            stop = False
            fault = 0.3
            possible_matches = []

            while not stop:
                real_value = node.objects[obj]
                var = real_value * fault
                possible_matches = [o for o, x in detections.items() if o in data2[f] and (real_value - var) < x < (real_value + var)]

                if len(possible_matches) <= 1 or fault < 0.05:
                    stop = True
                else:
                    fault -= 0.05

            if len(possible_matches):
                matches.update({obj: possible_matches[0]})

    # Calculate cost
    logging.info("Matches: %d", len(matches))

    cost = 0
    for data, detection in matches.items():
        cost += abs(node.objects[data] - detections[detection])

    weights = [1, 0.75, 0.5, 0.3]

    # Add penalty for each non detected object, and a benefit for detected objects
    # Larger angles are more accurate, so they get more weight
    for obj, val in node.objects.items():
        if val >= 30:
            index = 0
        elif 30 > val >= 15:
            index = 1
        elif 15 > val >= 8:
            index = 2
        else:
            index = 3

        if obj in matches.keys():
            cost -= 5 * weights[index]
            pass
        else:
            cost += 10 * weights[index]

    return cost


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run implementation")
    parser.add_argument('input_path', type=str, help="Path to input images")

    args = parser.parse_args()

    # Get all images
    images = sorted([f for f in listdir(args.input_path) if isfile(join(args.input_path, f))])

    # Init segmentation network
    seg_network = Segmentation("{}/{}".format(args.input_path, images[0]))
    mr = MapRenderer("data/map.osm")

    # Parse objects, locations and ways from the map
    objects, locations, ways = parse_map("data/map.osm")
    route = ways[0]
    current_location = list(filter(lambda x: x.node_id == -137971, locations))[0]

    output_file = open("output.csv", "w")
    fps_file = open("fps.txt", "w")
    vp = (0.5, 0.5)

    for i, image_path in enumerate(images):
        fps_start = time.time()
        img = cv2.imread("{}/{}".format(args.input_path, image_path))

        # Run object detector
        obj_start_time = time.time()
        det_objects = detect_objects(args.input_path, image_path)
        obj_end_time = time.time()
        logging.warning("Yolo calculation time: %f", obj_end_time - obj_start_time)

        # Find vanishing point
        vp_start_time = time.time()
        new = get_vp(seg_network, img)
        if new:
            vp = new
        vp_end_time = time.time()
        logging.warning("Segmentation calculation time: %f", vp_end_time - vp_start_time)

        # Calculate image offset
        angle_det = DetectionAngle(vp)
        img_offset = angle_det.calculate_offset()
        logging.info("Vp offset: %f", img_offset)

        # Calculate angle for each detection
        detections = {}
        for obj in det_objects:
            angle = angle_det.calculate(obj) + img_offset
            obj.render(img, text="%.3f" % angle)
            detections.update({obj: angle})

        # Get neighbouring nodes
        back, current, following = route.get_neighbours(current_location)

        cost_c = cost(current, detections)
        cost_f = cost(following, detections) * 1.25

        # Find best match
        costs = sorted([(current, cost_c), (following, cost_f)], key=lambda x: x[1])

        logging.info("Cost Current: %f", cost_c)
        logging.info("Cost Following: %f", cost_f)

        current_location = costs[0][0]
        logging.info("New location: %s", current_location)

        fig = mr.show_route(current_location.node_id)
        img = render_result(img, fig)

        fps_stop = time.time()
        logging.warning("Fps: %f", 1/(fps_stop-fps_start))
        logging.warning("--------------------------------")

        output_file.write("{},{}\n".format(image_path, current_location.id))
        fps_file.write('{}\n'.format(fps_stop-fps_start))

        cv2.waitKey(1)
