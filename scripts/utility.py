#!/usr/bin/env python

import rospy
from naoqi import ALProxy
from group3.srv import *


def text_2_speech(msg):
    rospy.wait_for_service('/tts')

    try: 
        myRospy = rospy.ServiceProxy('/tts',Text2Speech)
        respose = myRospy(msg)
        return respose.ack
    
    except rospy.ServiceException as e:
        print("Service Failed: %s", e)


def request_distance():
    memory_proxy = ALProxy("ALMemory", "10.0.1.236", 9559)
    sonar_proxy = ALProxy("ALSonar", "10.0.1.236", 9559)

    sonar_proxy.subscribe("myApplication")

    value = 0.0
    mean = 0.0
    count = 0
    max_count = 20
    r = rospy.Rate(5) # 5hz

    while count < max_count:
        sl = memory_proxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
        sr = memory_proxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
        x = (sl + sr)/2
        
        value += x
        count += 1
        
        r.sleep()

    mean = (value/(max_count))
    print("mean_rel: ", str(mean))
    
    return mean
