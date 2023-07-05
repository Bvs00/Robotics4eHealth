#!/usr/bin/env python3
import os
import rospy
from sensor_msgs.msg import Image
from detector import Detector
import numpy as np
from classmap import objects

DET_PATH=os.path.join(os.path.dirname(__file__),'efficientdet_d1_coco17_tpu-32')
mydetector = Detector(DET_PATH)

rospy.init_node('detector_node')


def rcv_image(msg):
    image = np.frombuffer(msg.data, dtype=np.uint8).reshape(msg.height, msg.width, -1)

    detections = mydetector(image)

    object_det = 0
    for clabel,score,box in zip(detections['detection_classes'], detections['detection_scores'], detections['detection_boxes']):
        
        object_det = clabel

        print("HOLAAA: ", str(clabel))

    if object_det in objects:
        print("\n\n\nHo riconosciuto l'oggetto")
        print("L'oggetto riconosciuto è: ", str(objects[object_det]))
        return object_det
        



si = rospy.Subscriber("/in_rgb", Image, rcv_image)



try:
    rospy.spin()

except KeyboardInterrupt:
    print("Shutting down")
    
