import cv2
import numpy as np
import config

class Camera(object):

    def __init__(self):
        self.camera = cv2.VideoCapture(config.cam_id)
        # set width and height of the camera 
        self.zoom = 4
        self.set_resolution_ratio()
        for i in range(20):
            self.updata()

    def set_resolution_ratio(self):
        self.camera.set(3, config.width_px * 2 / self.zoom)
        self.camera.set(4, config.height_px / self.zoom)

    def isOpened(self):
        return camera.isOpened()

    def updata(self):
        ret, self.frame = self.camera.read()
        if ret:
            self.split()
            # self.base_show()
        

    def split(self):
        self.left = self.frame[0 : config.height_px // self.zoom, \
            0 : config.width_px // self.zoom]
        self.right = self.frame[0 : config.height_px // self.zoom, \
            config.width_px // self.zoom + 1 : 2 * config.width_px // self.zoom]

    def base_show(self):
        cv2.imshow('left', self.left)
        cv2.imshow('right', self.right)    

    def output(self):
        cv2.imwrite("left.bmp", self.left)
        cv2.imwrite("right.bmp", self.right)

    def get_img(self):
        return self.left, self.right

    def wait(self):
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == '__main__':
    img = cv2.imread('1.png')
    img = split(img)
    base_show(img[0], img[1])
    cv2.waitKey(0)
    cv2.destroyAllWindows()
