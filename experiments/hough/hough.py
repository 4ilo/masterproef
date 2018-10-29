import cv2 as cv
import numpy as np

print(cv.__version__)

img = cv.imread('img/img1.png')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)


def nothing(x):
    pass


cv.namedWindow('edges')
cv.createTrackbar('tres1', 'edges', 50, 200, nothing)
cv.createTrackbar('tres2', 'edges', 200, 500, nothing)
cv.createTrackbar('apature', 'edges', 3, 7, nothing)

a = 3

while True:
    k = cv.waitKey(1) & 0xFF
    if k == 27:
        break           # Break on esc

    if k == 115:
        # Show values when 's' is pressed
        print("tres1: {}, tres2: {}, apature: {}".format(t1, t2, a_t))

    t1 = cv.getTrackbarPos('tres1', 'edges')
    t2 = cv.getTrackbarPos('tres2', 'edges')
    a_t = cv.getTrackbarPos('apature', 'edges')

    if a_t % 2 != 0 and a_t >=3:
        a = a_t

    edges = cv.Canny(gray, t1, t2, apertureSize=a)

    cv.imshow('edges', edges)

lines = cv.HoughLines(edges, 1, np.pi/180, 100)
for line in lines:
    rho,theta = line[0]
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))

    cv.line(img,(x1,y1),(x2,y2),(0,0,255),2)

# minLineLength = 100
# maxLineGap = 10
#
# cv.namedWindow('lines')
# cv.createTrackbar('minLineLength', 'lines', minLineLength, 200, nothing)
# cv.createTrackbar('maxLineGap', 'lines', maxLineGap, 20, nothing)
#
# while True:
#     k = cv.waitKey(1) & 0xFF
#     if k == 27:
#         break           # Break on esc
#
#     img_cpy = img.copy()
#
#     minLineLength = cv.getTrackbarPos('minLineLength', 'lines')
#     maxLineGap = cv.getTrackbarPos('maxLineGap', 'lines')
#
#     lines = cv.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength, maxLineGap)
#
#     for line in lines:
#         x1,y1,x2,y2 = line[0]
#         cv.line(img_cpy, (x1,y1), (x2,y2), (0,255,0),2)
#
#     cv.imshow('lines', img_cpy)

cv.imshow("Lines", img)
cv.waitKey(0)