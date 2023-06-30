#!/usr/bin/env python
import sys
import rospy
from std_msgs.msg import Float32MultiArray
from naoqi import ALProxy
from group3.srv import *


def projectManager():
    status = send_movement("up")

    if (status == "ACK"):
        print("Il braccio si è alzato correttamente")
    else:
        return 1

    rospy.sleep(5)
    status = send_movement("down")

    if (status == "ACK"):
        print("Il braccio si è abbassato correttamente")
    else:
        return 1
    



def send_movement(movement):
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
            return response.ack
        
        elif argomento == "down":
            memory_proxy = ALProxy("ALMemory", "10.0.1.236", 9559)
            
            valueWrist = memory_proxy.getData('Device/SubDeviceList/RWristYaw/Position/Actuator/Value')
            valueShoulder = memory_proxy.getData('Device/SubDeviceList/RShoulderPitch/Position/Actuator/Value')

            pub_movement_arm = rospy.ServiceProxy('/arm_rotation/left/shoulder/wrist', arm_controller_service)

            response = pub_movement_arm((valueShoulder),(valueWrist),(speed))
            return response.ack
        




    except rospy.ServiceException as e:
        print("Service Failed: %s", e)




if __name__ == "__main__":
    projectManager()