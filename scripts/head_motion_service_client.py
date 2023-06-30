#!/usr/bin/env python
import sys
import rospy
from std_msgs.msg import Float32MultiArray
from naoqi import ALProxy
from group3.srv import *

def send_movement():
    rospy.wait_for_service('/arm_rotation/left/shoulder/wrist')
    
    speed = 0.1  # Replace with the desired speed
    
    try:
        if len(sys.argv) > 1:
            argomento = sys.argv[1]

        if argomento == "down":
            pub_movement_head = rospy.ServiceProxy('/head_rotation/pitch', HeadMotion)

            pitchPosition = 0.15  # Replace with the desired angle

            response = pub_movement_head(pitchPosition,speed)
            print(response.ack)
            #return response.ack
        
        elif argomento == "up":
            normalAngle = -0.169877886772


            pub_movement_head = rospy.ServiceProxy('/head_rotation/pitch', HeadMotion)
            response = pub_movement_head(normalAngle,speed)
            print(response.ack)
            #return response.ack
        
    except rospy.ServiceException as e:
        print("Service Failed: %s", e)


if __name__ == '__main__':
    try:

        send_movement()
    except rospy.ROSInterruptException:
        pass
