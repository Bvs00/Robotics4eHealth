#!/usr/bin/env python

import rospy
from std_msgs.msg import Float32MultiArray
from naoqi import ALProxy
from group3.srv import *

def talker():
    rospy.wait_for_service('/arm_rotation/left/shoulder/wrist')
    print("mhm")
    try:
        pub_l_pitch = rospy.ServiceProxy('/arm_rotation/left/shoulder/wrist', arm_controller_service)

        angle_shoulder = 0.0  # Replace with the desired angle
        speed = 0.1  # Replace with the desired speed

        # Publish the motion command

        angle_wrist_l = -1.0


        _ = pub_l_pitch(float32(angle_shoulder),float32(angle_wrist_l),float32(speed))
        #print("La risposta è: " + str(response.ack))

    except rospy.ServiceException as e:
        print("Service Failed: %s", e)


if __name__ == '__main__':
    try:
        print("OOK")
        talker()
    except rospy.ROSInterruptException:
        pass
