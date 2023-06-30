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

        if argomento == "up":
            pub_movement_arm = rospy.ServiceProxy('/arm_rotation/left/shoulder/wrist', arm_controller_service)

            angle_shoulder = 0.5  # Replace with the desired angle
            
            # Publish the motion command

            angle_wrist_l = -1.8238

            response = pub_movement_arm((angle_shoulder),(angle_wrist_l),(speed))
            print(response.ack)
            #return response.ack
        
        elif argomento == "down":
            memory_proxy = ALProxy("ALMemory", "10.0.1.236", 9559)
            
            valueWrist = memory_proxy.getData('Device/SubDeviceList/RWristYaw/Position/Actuator/Value')
            valueShoulder = memory_proxy.getData('Device/SubDeviceList/RShoulderPitch/Position/Actuator/Value')

            pub_movement_arm = rospy.ServiceProxy('/arm_rotation/left/shoulder/wrist', arm_controller_service)

            response = pub_movement_arm((valueShoulder),(valueWrist),(speed))
            print(response.ack)
            #return response.ack
        




    except rospy.ServiceException as e:
        print("Service Failed: %s", e)


if __name__ == '__main__':
    try:

        send_movement()
    except rospy.ROSInterruptException:
        pass
