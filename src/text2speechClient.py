#!/usr/bin/python3

from group3.srv import *
import rospy

def text_2_speech(msg):
    rospy.wait_for_service('/tts')

    try: 
        myRospy = rospy.ServiceProxy('/tts',Text2Speech)
        respose = myRospy(msg)
        return respose.ack
    
    except rospy.ServiceException as e:
        print("Service Failed: %s", e)

if __name__ == "__main__":
    text_2_speech("Ciao Giuseppe, i ragazzi mi maltrattano")
