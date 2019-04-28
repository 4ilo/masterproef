import cv2
import copy
import argparse
from tqdm import tqdm
from os import listdir
import brambox.boxes as bbb
import matplotlib.pyplot as plt
from os.path import isfile, join
from Detector.darknet.Darknet import performDetect


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run validation set through yolo detector')
    parser.add_argument('validation_path', help="Path to validation image files")
    parser.add_argument('yolo_config_dir', help="Path to yolo cfg, data and weights dir")
    parser.add_argument('annotations_path', help="Path to darknet annotations for validation images")
    args = parser.parse_args()

    # Get all images
    images = sorted([f for f in listdir(args.validation_path) if isfile(join(args.validation_path, f))])

    # Get classes to validate
    classes = open("{}/{}".format(args.yolo_config_dir, 'cust.names')).read().split('\n')

    # Run yolo detector for all validation images
    detections = {}
    for image in tqdm(images):
        open("{}/{}.txt".format(args.annotations_path, image.split('.')[0]), 'a')   # Make sure annotation file exists

        image_path = "{}/{}".format(args.validation_path, image)

        # Get image width and height
        img = cv2.imread(image_path)
        img_h, img_w = img.shape[:2]

        dets = performDetect(imagePath=image_path,
                                   thresh=0.25,
                                   configPath=args.yolo_config_dir + "/cust.cfg",
                                   weightPath=args.yolo_config_dir + "/cust.weights",
                                   metaPath=args.yolo_config_dir + "/cust.data",
                                   showImage=False)

        data = []
        for det in dets:
            darknet_string = "{} {} {} {} {}\n".format(classes.index(det[0]),
                                                       det[2][0] / img_w,
                                                       det[2][1] / img_h,
                                                       det[2][2] / img_w,
                                                       det[2][3] / img_h
                                                       )

            # Parse detections into brambox detection format
            bounding_box = bbb.annotations.DarknetAnnotation().deserialize(darknet_string, classes, img_w, img_h)
            detection = bbb.Detection.create(bounding_box)
            detection.confidence = det[1]
            data.append(detection)

        detections[image.split('.')[0]] = data

    # Read annotations file
    annotations = bbb.parse('anno_darknet', args.annotations_path, image_width=img_w, image_height=img_h, class_label_map=classes)

    # Generate PR-curve and compute AP for every individual class.
    plt.figure()

    for c in classes:
        anno_c = bbb.filter_discard(copy.deepcopy(annotations), [lambda anno: anno.class_label == c])
        det_c = bbb.filter_discard(copy.deepcopy(detections), [lambda det: det.class_label == c])
        p, r = bbb.pr(det_c, anno_c)
        ap = bbb.ap(p, r)
        plt.plot(r, p, label=f'{c}: {round(ap * 100, 2)}%')

    plt.gcf().suptitle('PR-curve individual example')
    plt.gca().set_ylabel('Precision')
    plt.gca().set_xlabel('Recall')
    plt.gca().set_xlim([0, 1])
    plt.gca().set_ylim([0, 1])
    plt.legend()
    plt.show()
