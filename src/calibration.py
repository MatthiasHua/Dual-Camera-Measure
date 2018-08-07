from flask import Flask, render_template, Response
from src.camera import Camera
import numpy as np
import cv2
import glob
from src import app
from src import cam

@app.route('/chessboard_left/<int:id>.jpg')
def chessboard_left(id):
    #tmp_zoom = cam.zoom
    #cam.zoom = 1
    #cam.set_resolution_ratio()

    objpoints = np.load('objpoints.npy').tolist()
    imgpoints = np.load('imgpoints.npy').tolist()
    print(imgpoints)
    cam.updata()
    left = cam.get_img()[0]
    gray = cv2.cvtColor(left, cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (8,6), None)
    
    # If found, add object points, image points (after refining them)
    if ret == True:
        print("find")
        objpoints.append(objp)

        
        cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        print(corners)
        imgpoints.append(corners)

        # Draw and display the corners
        cv2.drawChessboardCorners(left, (8,6), corners,ret)

        np.save('objpoints.npy', objpoints)
        np.save('imgpoints.npy', imgpoints)

    ret, leftjpg = cv2.imencode('.jpg', left)
    return leftjpg.tobytes()

@app.route('/chessboard_right/<int:id>.jpg')
def chessboard_right(id):
    #tmp_zoom = cam.zoom
    #cam.zoom = 1
    #cam.set_resolution_ratio()

    objpoints = np.load('objpoints.npy').tolist()
    imgpoints = np.load('imgpoints.npy').tolist()
    print(imgpoints)
    right = cam.get_img()[1]
    gray = cv2.cvtColor(right, cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (8,6), None)
    
    # If found, add object points, image points (after refining them)
    if ret == True:
        print("find")
        objpoints.append(objp)

        
        cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        print(corners)
        imgpoints.append(corners)

        # Draw and display the corners
        cv2.drawChessboardCorners(right, (8,6), corners,ret)

        np.save('objpoints.npy', objpoints)
        np.save('imgpoints.npy', imgpoints)

    ret, rightjpg = cv2.imencode('.jpg', right)
    return rightjpg.tobytes()
