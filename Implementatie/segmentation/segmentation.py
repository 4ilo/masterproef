import tensorflow as tf
import numpy as np
import os
import cv2
import itertools

from segmentation.model import DeepLabResNetModel

IMG_MEAN = np.array((104.00698793, 116.66876762, 122.67891434), dtype=np.float32)
NUM_CLASSES = 27


def remove_duplicates(lines, diff=0.25):
    """ Remove lines with the same theta """
    def rico(line):
        return (line[1][1] - line[0][1])/(line[1][0] - line[0][0])

    delete = []
    for (i1, line1), (i2, line2) in itertools.combinations(enumerate(lines), 2):
        rc1 = rico(line1)
        rc2 = rico(line2)

        t1 = rc1 + rc1 * diff
        t2 = rc1 - rc1 * diff
        if (rc1 + rc1 * diff) > rc2 > (rc1 - rc1 * diff) or (rc1 + rc1 * diff) < rc2 < (rc1 - rc1 * diff):
            delete.append(i1 if abs(rc1) < abs(rc2) else i2)

    return [lines[i] for i in range(len(lines)) if i not in delete]


def get_floor_mask(img, floor_label=4):
    """ Create binary mask for floor pixels """
    n, h, w, c = img.shape

    mask = np.zeros((h, w), dtype=np.uint8)
    for j, j_val in enumerate(img[0, :, :, 0]):
        for i, i_val in enumerate(j_val):
            if i_val == floor_label:
                mask[j, i] = 1

    return mask


def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = int(det(d, xdiff) / div)
    y = int(det(d, ydiff) / div)
    return x, y


def run_segmentation(image_name="img/test.png"):

    # Read image
    img = tf.image.decode_png(tf.read_file(image_name), channels=3)

    # Convert to bgr
    img_r, img_g, img_b = tf.split(axis=2, num_or_size_splits=3, value=img)
    img = tf.cast(tf.concat(axis=2, values=[img_b, img_g, img_r]), dtype=tf.float32)

    img -= IMG_MEAN

    net = DeepLabResNetModel({'data': tf.expand_dims(img, dim=0)}, is_training=False, num_classes=NUM_CLASSES)

    restore_var = tf.global_variables()

    # Predictions
    raw_output = net.layers['fc_out']
    raw_output_up = tf.image.resize_bilinear(raw_output, tf.shape(img)[0:2, ])
    raw_output_up = tf.argmax(raw_output_up, dimension=3)
    pred = tf.expand_dims(raw_output_up, dim=3)

    # Setup tf
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    sess = tf.Session(config=config)
    init = tf.global_variables_initializer()

    sess.run(init)

    # Load weights
    checkpoint = tf.train.get_checkpoint_state("restore_weights")

    if checkpoint and checkpoint.model_checkpoint_path:
        loader = tf.train.Saver(var_list=restore_var)
        load_step = int(os.path.basename(checkpoint.model_checkpoint_path).split('-')[1])
        loader.restore(sess, checkpoint.model_checkpoint_path)
        print("Restored model parameters from {}".format(checkpoint.model_checkpoint_path))
    else:
        print("No checkpoint file found")

    preds = sess.run(pred)

    mask = get_floor_mask(preds)

    edges = cv2.Canny(mask, 0, 1, apertureSize=3)

    img = cv2.imread(image_name)
    test = cv2.bitwise_and(img, img, mask=mask)
    cv2.imshow("test", test)
    cv2.waitKey(0)

    tresh = 50
    lines = cv2.HoughLines(edges, 1, np.pi / 180, tresh)
    while len(lines) > 10:
        tresh += 1
        lines = cv2.HoughLines(edges, 1, np.pi / 180, tresh)

    point_lines = []

    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * (a)))
            pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * (a)))

            point_lines.append((pt1, pt2))

    point_lines = remove_duplicates(point_lines)

    for line in point_lines:
        cv2.line(img, line[0], line[1], (0, 0, 255), 1)

    # intersection = line_intersection(point_lines[0], point_lines[1])

    # cv2.circle(img, intersection, 10, (0, 255, 0))

    cv2.imshow("test", img)
    cv2.waitKey(0)



    # img = cv2.imread("img/test.png")
    # test = cv2.bitwise_and(img, img, mask=mask)
    # cv2.imshow('test', test)
    # cv2.imshow('test2', img)
    # cv2.waitKey(0)
