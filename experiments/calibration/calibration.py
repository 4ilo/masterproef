import numpy as np
import cv2
import glob

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

cbrow = 7
cbcol = 7

# Prepare object points like (0,0,0) (1,0,0)
objp = np.zeros((cbrow * cbcol, 3), np.float32)
objp[:, :2] = np.mgrid[0:cbcol, 0:cbrow].T.reshape(-1, 2)

# Arrays to store object points and image points from the images
objpoints = []
imgpoints = []

images = glob.glob('img/*.png')

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find corners
    ret, corners = cv2.findChessboardCorners(gray, (cbcol, cbrow), None)

    if ret == True:
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, 1), criteria)
        imgpoints.append(corners)

        # cv2.drawChessboardCorners(img, (cbcol, cbrow), corners2, ret)
        # cv2.imshow("img", img)
        # cv2.waitKey(1)

img = cv2.imread('img/frame060.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

print("Focal length(x-y): {} - {}".format(mtx[0][0], mtx[1][1]))

h, w = img.shape[:2]
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

x,y,w,h = roi
dst = dst[y:y+h, x:x+w]
cv2.imshow('result', dst)
cv2.imshow('orig', img)
cv2.waitKey(0)
