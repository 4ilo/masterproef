# Olivier Van den Eede
import cv2 as cv
import numpy as np

print("OpenCV " + cv.__version__)

FILE = "img/fig4.png"


def createSilderWindow(value_low=[0, 0, 0], value_high=[255, 255, 255], name='Slider'):
    """ Create a window with slider trackbars """
    def nothing(x):
        pass

    cv.namedWindow(name)

    lower = np.array(value_low, dtype="uint8")
    higher = np.array(value_high, dtype="uint8")

    cv.createTrackbar('low_h', name, lower[0], 180, nothing)
    cv.createTrackbar('low_s', name, lower[1], 255, nothing)
    cv.createTrackbar('low_v', name, lower[2], 255, nothing)

    cv.createTrackbar('high_h', name, higher[0], 180, nothing)
    cv.createTrackbar('high_s', name, higher[1], 255, nothing)
    cv.createTrackbar('high_v', name, higher[2], 255, nothing)

    return lower, higher


def getTrackbarPos(name='Slider'):
    """ Get the values of the trackbars """
    lower = np.array([0, 0, 0])
    higher = np.array([0, 0, 0])

    lower[0] = cv.getTrackbarPos('low_h', name)
    lower[1] = cv.getTrackbarPos('low_s', name)
    lower[2] = cv.getTrackbarPos('low_v', name)

    higher[0] = cv.getTrackbarPos('high_h', name)
    higher[1] = cv.getTrackbarPos('high_s', name)
    higher[2] = cv.getTrackbarPos('high_v', name)

    return lower, higher


def close_blobs(mask):
    """ Erode & dilate to close the blobs """
    kernel = np.ones((5, 5), np.uint8)

    mask = cv.erode(mask, kernel, iterations=1)
    mask = cv.dilate(mask, kernel, iterations=2)

    return mask


def sift(img, x, y, w, h):
    sub = img[y:y+h, x:x+w]
    gray = cv.cvtColor(sub, cv.COLOR_BGR2GRAY)

    sift = cv.xfeatures2d.SURF_create(1)
    kp, des = sift.detectAndCompute(gray, None)
    if des is not None:
        print("#kps: {}, descriptors: {}".format(len(kp), des.shape))

    cv.drawKeypoints(sub, kp, sub)

    # sign = cv.imread('img/sign.png')
    # sign_g = cv.cvtColor(sign, cv.COLOR_BGR2GRAY)
    # kp, des = sift.detectAndCompute(sign_g, None)
    # cv.drawKeypoints(sign, kp, sign)

    cv.imshow('cropped', sub)
    cv.imshow('sign', sign)
    cv.waitKey(0)


def detect_color(mask, draw_on):
    image = draw_on.copy()

    mask = close_blobs(mask)

    img2, contours, hierarchie = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        x, y, w, h = cv.boundingRect(cnt)
        cv.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 1)
        sift(draw_on, x, y, w, h)

    return image


if __name__ == '__main__':
    # Read image file
    orig = cv.imread(FILE)
    img = orig.copy()
    cv.imshow('Input', img)

    # Convert to hsv
    img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    cv.imshow('Hsv', img)

    # Split in h, s & v
    h, s, v = cv.split(img)


    def nothing(x):
        print('Value: {}'.format(x))

    low = 17                      # Fig4
    high = 25

    cv.namedWindow('test')
    cv.createTrackbar('low_h', 'test', low, 180, nothing)
    cv.createTrackbar('high_h', 'test', high, 180, nothing)
    cv.imshow("test", h)

    while True:
        mask = cv.inRange(h, low, high)

        cv.imshow('test', mask)

        low = cv.getTrackbarPos('low_h', 'test')
        high = cv.getTrackbarPos('high_h', 'test')

        # Check for key input
        k = cv.waitKey(1) & 0xFF
        if k == 27:
            break           # Break on esc

    box = detect_color(mask, draw_on=orig)
    cv.imshow('Boxes', box)
    cv.waitKey(0)

    # lower, higher = createSilderWindow(value_low=[10, 50, 70], value_high=[40, 70, 100])
    #
    # cv.namedWindow('Boxes')
    #
    # while True:
    #     # Get the color values in the given range
    #     mask = cv.inRange(img, lower, higher)
    #
    #     # Show the masked output
    #     cv.imshow('Slider', mask)
    #
    #     # Check for key input
    #     k = cv.waitKey(1) & 0xFF
    #     if k == 27:
    #         break           # Break on esc
    #
    #     if k == 115:
    #         # Show values when 's' is pressed
    #         print("LOW - H: {}, S: {}, V: {}".format(lower[0], lower[1], lower[2]))
    #         print("HIGH - H: {}, S: {}, V: {}".format(higher[0], higher[1], higher[2]))
    #
    #     if k == 98:
    #         # Draw bounding boxes if 'b' is pressed
    #         box = detect_color(mask, draw_on=orig)
    #         cv.imshow('Boxes', box)
    #
    #     lower, higher = getTrackbarPos()

