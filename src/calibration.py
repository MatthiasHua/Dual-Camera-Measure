from flask import Flask, render_template, Response
from src.camera import Camera
import numpy as np
import cv2
import glob
from src import app
from src import cam

@app.route('/chessboard_calibration')
def chessboard_calibration():
    #tmp_zoom = cam.zoom
    #cam.zoom = 1
    #cam.set_resolution_ratio()

    objpoints = np.load('objpoints.npy').tolist()
    imgpoints = np.load('imgpoints.npy').tolist()
    # print(imgpoints)
    cam.updata()
    
    left = cam.get_img()[0]
    right = cam.get_img()[1]
    grayleft = cv2.cvtColor(left, cv2.COLOR_BGR2GRAY)
    grayright = cv2.cvtColor(right, cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    retleft, cornersleft = cv2.findChessboardCorners(grayleft, (8,6), None)
    retright, cornersright = cv2.findChessboardCorners(grayright, (8,6), None)

    # If found, add object points, image points (after refining them)
    if retleft and retright:
        print("find")

	# left
        objpoints.append(objp)

        cv2.cornerSubPix(grayleft,cornersleft,(11,11),(-1,-1),criteria)
        imgpoints.append(cornersleft)

        # Draw and display the corners
        cv2.drawChessboardCorners(left, (8,6), corners,ret)
	cam.chessboard_left = left
	# right
        objpoints.append(objp)

        cv2.cornerSubPix(grayright,cornersright,(11,11),(-1,-1),criteria)
        imgpoints.append(cornersright)

        # Draw and display the corners
        cv2.drawChessboardCorners(right, (8,6), corners,ret)
        cam.chessboard_right = right

        np.save('objpoints.npy', objpoints)
        np.save('imgpoints.npy', imgpoints)

	return '1'
    return '0'

@app.route('/chessboard_left/<int:id>.jpg')
def chessboard_left(id):

    ret, leftjpg = cv2.imencode('.jpg', cam.chessboard_left)
    return leftjpg.tobytes()

@app.route('/chessboard_right/<int:id>.jpg')
def chessboard_right(id):

    ret, rightjpg = cv2.imencode('.jpg', cam.chessboard_right)
    return rightjpg.tobytes()



