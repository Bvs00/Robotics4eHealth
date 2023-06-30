#!/usr/bin/python
from naoqi import ALProxy
from optparse import OptionParser
import rospy
from group3.srv import *


class HeadMotionNode:

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.motion_proxy = ALProxy("ALMotion", ip, port)

    def head_pitch(self, msg):
        try:
            self.motion_proxy.setAngles(["HeadPitch"], msg.pitchPosition, msg.speed)
            response = HeadMotionResponse()
            response.ack = "ACK"
            return response
        except:
            self.motion_proxy = ALProxy("ALMotion", self.ip, self.port)
            self.motion_proxy.setAngles(["HeadPitch"], msg.pitchPosition, msg.speed)
            response = HeadMotionResponse()
            response.ack = "NACK"
            return response

    def start(self):
        rospy.init_node("head_motion_node")
        rospy.Service("/head_rotation/pitch", HeadMotion, self.head_pitch)
        rospy.spin()

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("--ip", dest="ip", default="10.0.1.236")
    parser.add_option("--port", dest="port", default=9559)
    (options, args) = parser.parse_args()

    try:
        node = HeadMotionNode(options.ip, int(options.port))
        node.start()
    except rospy.ROSInterruptException:
        pass
