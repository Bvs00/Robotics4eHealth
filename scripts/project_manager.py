#!/usr/bin/env python
import sys
import rospy
from std_msgs.msg import Float32MultiArray
from naoqi import ALProxy
from group3.srv import *


def project_manager():
    status = send_movement_arm("up")

    if status != "ACK":
        print("COMANDO SBAGLIATO")
        return
    
    text_2_speech("Fammi vedere cosa hai in mano")

    rospy.sleep(3)
    status = send_movement_arm("down")
    if status != "ACK":
        print("COMANDO SBAGLIATO")
        return
    
    text_2_speech("Bravo hai superato il test")

    



def send_movement_arm(arg):
    rospy.wait_for_service('/arm_rotation/left/shoulder/wrist')
    
    speed = 0.1  # Replace with the desired speed

    try:
        
        if arg == "up":
            pub_movement_arm = rospy.ServiceProxy('/arm_rotation/left/shoulder/wrist', arm_controller_service)

            angle_shoulder = 0.5  # Replace with the desired angle
            
            # Publish the motion command

            angle_wrist_l = -1.8238

            response = pub_movement_arm((angle_shoulder),(angle_wrist_l),(speed))

        
        elif arg == "down":
            memory_proxy = ALProxy("ALMemory", "10.0.1.236", 9559)
            
            valueWrist = memory_proxy.getData('Device/SubDeviceList/RWristYaw/Position/Actuator/Value')
            valueShoulder = memory_proxy.getData('Device/SubDeviceList/RShoulderPitch/Position/Actuator/Value')

            pub_movement_arm = rospy.ServiceProxy('/arm_rotation/left/shoulder/wrist', arm_controller_service)

            response = pub_movement_arm((valueShoulder),(valueWrist),(speed))
        
        
        return response.ack
        
    except rospy.ServiceException as e:
        print("Service Failed: %s", e)

def text_2_speech(msg):
    rospy.wait_for_service('/tts')

    try: 
        myRospy = rospy.ServiceProxy('/tts',Text2Speech)
        respose = myRospy(msg)
        return respose.ack
    
    except rospy.ServiceException as e:
        print("Service Failed: %s", e)

def send_movement_head(arg):
    rospy.wait_for_service('/arm_rotation/left/shoulder/wrist')
    
    speed = 0.1  # Replace with the desired speed
    
    try:

        if arg == "down":
            pub_movement_head = rospy.ServiceProxy('/head_rotation/pitch', HeadMotion)

            pitchPosition = 0.15  # Replace with the desired angle

            response = pub_movement_head(pitchPosition,speed)
        
        elif arg == "up":
            normalAngle = -0.169877886772


            pub_movement_head = rospy.ServiceProxy('/head_rotation/pitch', HeadMotion)
            response = pub_movement_head(normalAngle,speed)
        
        return response.ack
        
    except rospy.ServiceException as e:
        print("Service Failed: %s", e)


if __name__ == "__main__":
    rospy.init_node("project_manager")
    project_manager()