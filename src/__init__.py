from flask import Flask, render_template, Response
from src.camera import Camera
import numpy as np
import cv2
import glob

app = Flask(__name__, static_url_path='', static_folder='../static', template_folder='../templates')
cam = Camera()

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*8, 3), np.float32)
objp[:,:2] = np.mgrid[0:8, 0:6].T.reshape(-1,2)

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/chessboard')
@app.route('/chessboard.html')
def chessboard():
    return render_template('chessboard.html')

@app.route('/chessboard')
def chessboard_test():
    return render_template('chessboard_test.html')

@app.route('/rectified')
def rectified():
    return render_template('rectified.html')

@app.route('/left/<int:id>.jpg')
def hello_world(id):
    cam.updata()
    left = cam.get_img()[0]
    ret, leftjpg = cv2.imencode('.jpg', left)
    return leftjpg.tobytes()

def gen_left(cam):
    while True:
        cam.updata()
        left = cam.get_img()[0]
        ret, leftjpg = cv2.imencode('.jpg', left)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + leftjpg.tobytes() + b'\r\n\r\n')

def gen_right(cam):
    while True:
        right = cam.get_img()[1]
        ret, rightjpg = cv2.imencode('.jpg', right)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + rightjpg.tobytes() + b'\r\n\r\n')

@app.route('/video_left')
def video_left():
    return Response(gen_left(cam),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_right')
def video_right():
    return Response(gen_right(cam),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/rectified_left/<int:id>.jpg')
def rectified_left(id):
    objpoints = np.load('objpoints.npy').astype('float32')
    imgpoints = np.load('imgpoints.npy').astype('float32')
    #objpoints.dtype = 'float32'
    #imgpoints.dtype = 'float32'
    print(objpoints.dtype)
    cam.updata()
    img = cam.get_img()[0]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
    h, w = img.shape[:2]
    newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))

    # undistort
    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
    # crop the image
    x,y,w,h = roi
    dst = dst[y:y+h, x:x+w]
    ret, dst = cv2.imencode('.jpg', dst)
    return dst.tobytes()

import src.calibration

if __name__ == '__main__':
    app.run(host='0.0.0.0')
