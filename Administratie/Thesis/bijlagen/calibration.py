import cv2
import glob
import numpy as np

# Termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Rows and Cols on chessboard
cb_row = 7
cb_col = 7

# Prepare object points like (0,0,0) (1,0,0)
objp = np.zeros((cb_row * cb_col, 3), np.float32)
objp[:, :2] = np.mgrid[0:cb_col, 0:cb_row].T.reshape(-1, 2)

# Arrays to store object points and image points from the images
objpoints = []
imgpoints = []

images = glob.glob('img/*.png')

# Get datapoints for each image (at least 10 images)
for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find corners
    ret, corners = cv2.findChessboardCorners(gray, (cb_col, cb_row), None)

    if ret == True:
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, 1), criteria)
        imgpoints.append(corners)


# Calculate camera matrix
img = cv2.imread('img/frame060.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

print("Focal length(x-y): {} - {}".format(mtx[0][0], mtx[1][1]))
