#!/usr/bin/python
from naoqi import ALProxy
from optparse import OptionParser
from std_msgs.msg import Float32MultiArray
import rospy
from group3.srv import *

class ShoulderMotionNode:

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.motion_proxy = ALProxy("ALMotion", ip, port)

    def left_shoulder_and_wrist(self, msg):
        try:
            print(msg)
            self.motion_proxy.setAngles(["LShoulderPitch"], msg.angle_shoulder, msg.speed)
            self.motion_proxy.setAngles(["LWristYaw"], msg.angle_wrist, msg.speed)
            #response = arm_controller_serviceResponse()
            #response.ack = "OK"
            #return response
        except:
            self.motion_proxy = ALProxy("ALMotion", self.ip, self.port)
            self.motion_proxy.setAngles(["LShoulderPitch"], msg.x, msg.y)
            self.motion_proxy.setAngles(["LWristYaw"], msg.x, msg.y)


    def start(self):
        rospy.init_node("shoulders_motion_node")
        
        rospy.Service("/arm_rotation/left/shoulder/wrist", arm_controller_service, self.left_shoulder_and_wrist)
        
        rospy.spin()

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("--ip", dest="ip", default="10.0.1.236")
    parser.add_option("--port", dest="port", default=9559)
    (options, args) = parser.parse_args()

    try:
        node = ShoulderMotionNode(options.ip, int(options.port))
        node.start()
    except rospy.ROSInterruptException:
        pass
