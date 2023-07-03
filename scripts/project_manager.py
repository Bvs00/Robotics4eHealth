#!/usr/bin/env python

import rospy
from naoqi import ALProxy
from group3.srv import *
from motion_controller import *
from utility import *
from abc import ABC, abstractmethod



def project_manager():
    
    request_distance()

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


        
    
    

if __name__ == "__main__":
    rospy.init_node("project_manager")
    project_manager()