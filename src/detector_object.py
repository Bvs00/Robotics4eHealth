#!/usr/bin/env python3
import os
import rospy
from sensor_msgs.msg import Image
from detector import Detector
import numpy as np
from classmap import objects
from group3.srv import *

# Qui siamo nel server del service che prende l'immagine e detecta gli oggetti


DET_PATH=os.path.join(os.path.dirname(__file__),'efficientdet_d1_coco17_tpu-32')
mydetector = Detector(DET_PATH)

rospy.init_node('detector_node')


def rcv_image(msg):
    image = np.frombuffer(msg.image.data, dtype=np.uint8).reshape(msg.image.height, msg.image.width, -1)

    detections = mydetector(image)

    object_det = 0
    for clabel,score,box in zip(detections['detection_classes'], detections['detection_scores'], detections['detection_boxes']):
        
        object_det = clabel
        print("NEL FOR: ", str(object_det))

    if object_det in objects:
        response = ImageDetectorResponse()
        response.obj = str(objects[object_det])
        print("\n\n\nFind Object:", response.obj)
        return response
    else:
        response = ImageDetectorResponse()
        response.obj = "ACK"
        # print("ACK:", response.obj)
        return response
        



si = rospy.Service("/image/detector_object", ImageDetector, rcv_image)



try:
    rospy.spin()

except KeyboardInterrupt:
    print("Shutting down")
    
