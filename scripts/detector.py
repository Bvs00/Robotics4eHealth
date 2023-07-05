#!/usr/bin/env python

from cv_bridge import CvBridge
from naoqi import ALProxy
from optparse import OptionParser
import numpy as np
import rospy
from group3.srv import *
import time


objects = {
    2: 'bicycle',
    3: 'car',
    4: 'motorcycle',
    5: 'airplane',
    6: 'bus',
    7: 'train',
    8: 'truck',
    9: 'boat',
    10: 'traffic light',
    11: 'fire hydrant',
    13: 'stop sign',
    14: 'parking meter',
    15: 'bench',
    16: 'bird',
    17: 'cat',
    18: 'dog',
    19: 'horse',
    20: 'sheep',
    21: 'cow',
    22: 'elephant',
    23: 'bear',
    24: 'zebra',
    25: 'giraffe',
    27: 'backpack',
    28: 'umbrella',
    31: 'handbag',
    32: 'tie',
    33: 'suitcase',
    34: 'frisbee',
    35: 'skis',
    36: 'snowboard',
    37: 'sports ball',
    38: 'kite',
    39: 'baseball bat',
    40: 'baseball glove',
    41: 'skateboard',
    42: 'surfboard',
    43: 'tennis racket',
    44: 'bottle',
    46: 'wine glass',
    47: 'cup',
    48: 'fork',
    49: 'knife',
    50: 'spoon',
    51: 'bowl',
    52: 'banana',
    53: 'apple',
    54: 'sandwich',
    55: 'orange',
    56: 'broccoli',
    57: 'carrot',
    58: 'hot dog',
    59: 'pizza',
    60: 'donut',
    61: 'cake',
    64: 'potted plant',
    65: 'bed',
    67: 'dining table',
    70: 'toilet',
    72: 'tv',
    73: 'laptop',
    74: 'mouse',
    75: 'remote',
    76: 'keyboard',
    77: 'cell phone',
    78: 'microwave',
    79: 'oven',
    80: 'toaster',
    81: 'sink',
    82: 'refrigerator',
    84: 'book',
    85: 'clock',
    86: 'vase',
}



TOP_CAMERA = 0
BOTTOM_CAMERA = 1
DEPTH_CAMERA = 2

RES_120P = 0
RES_240P = 1
RES_480P = 2
RES_960P = 3

COLORSPACE_GRAYSCALE = 8
COLORSPACE_RGB = 13

MODE_RGB = 0
MODE_DEPTH = 1
MODE_RGBD = 2

def detector_obj():

    parser = OptionParser()
    parser.add_option("--ip", dest="ip", default="10.0.1.236")
    parser.add_option("--port", dest="port", default=9559)
    (options, args) = parser.parse_args()
    try:
        image_input = ImageInputNode(options.ip, int(options.port))
        obj = image_input.start()
        return obj
    except rospy.ROSInterruptException:
        pass

class ImageInputNode:

    def __init__(self, ip, port, resolution=RES_240P, rgb_camera=TOP_CAMERA, fps=6):
        self.fps = fps

        if resolution == RES_120P:
            self.width, self.height = 160, 120
        elif resolution == RES_240P:
            self.width, self.height = 320, 240
        elif resolution == RES_480P:
            self.width, self.height = 640, 480
        elif resolution == RES_960P:
            self.width, self.height = 1280, 960
        else:
            self.width, self.height = None, None
        self.camera = ALProxy("ALVideoDevice", ip, port)
        self.rgb_sub = self.camera.subscribeCamera("RGB Stream", rgb_camera, resolution, COLORSPACE_RGB, self.fps)
        if not self.rgb_sub:
            raise Exception("Camera is not initialized properly")
        self.image_publisher = rospy.ServiceProxy('/image/detector_object', ImageDetector)
        self.bridge = CvBridge()

    def get_color_frame(self):
        raw_rgb = self.camera.getImageRemote(self.rgb_sub)
        image = np.frombuffer(raw_rgb[6], np.uint8).reshape(raw_rgb[1], raw_rgb[0], 3)
        return image

    def get_fov(self, mode="RGB"):
        hfov, vfov = 0, 0
        if mode == "RGB":
            hfov = 57.2 * np.pi / 180
            vfov = 44.3 * np.pi / 180
        return hfov, vfov
    
    def stop(self):
        self.camera.unsubscribe(self.rgb_sub)

    def start(self):
        rospy.wait_for_service("/image/detector_object")

        start_time = time.time()

        rate = rospy.Rate(self.fps)
        while (time.time() - start_time) < 1000:
            frame = self.get_color_frame()
            if frame is not None:
                msg = self.bridge.cv2_to_imgmsg(frame)
                msg.header.stamp = rospy.Time.now()
                response = self.image_publisher(msg)
            if(response.obj in objects.values()):
                return response.obj

            rate.sleep()
        return "ACK"

            