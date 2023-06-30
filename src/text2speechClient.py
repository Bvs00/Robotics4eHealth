#!/usr/bin/python3
from nao_nodes.srv import *
import rospy

def text_2_speech(msg="Ciao"):
    rospy.wait_for_service('/tts')
    
    try: 
        myRospy = rospy.ServiceProxy('/tts',Text2Speech)
        _ = myRospy(msg)
    except rospy.ServiceException as e:
        print("Service Failed: %s", e)

if __name__ == "__main__":
    text_2_speech("Ciao Simone")
