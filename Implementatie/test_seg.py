import cv2
import argparse
import itertools
import numpy as np

from segmentation.segmentation import run_segmentation


def get_floor_mask(img, floor_label=4):
    """ Create binary mask for floor pixels """
    n, h, w, c = img.shape

    mask = np.zeros((h, w), dtype=np.uint8)
    for j, j_val in enumerate(img[0, :, :, 0]):
        for i, i_val in enumerate(j_val):
            if i_val == floor_label:
                mask[j, i] = 1

    return mask


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


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Do something")
    parser.add_argument('image_path', type=str, help="Path to input image")
    args = parser.parse_args()
    image_path = args.image_path

    preds = run_segmentation(image_path)

    mask = get_floor_mask(preds)

    edges = cv2.Canny(mask, 0, 1, apertureSize=3)

    img = cv2.imread(image_path)
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