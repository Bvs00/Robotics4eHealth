#!/usr/bin/python
from naoqi import ALProxy
from optparse import OptionParser
import rospy
from group3.srv import *

class ArmMotionNode:

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.motion_proxy = ALProxy("ALMotion", ip, port)

    def left_shoulder_and_wrist(self, msg):
        angles = [msg.angle_shoulder, msg.angle_wrist]
        try:
            self.motion_proxy.setAngles(["LShoulderPitch","LWristYaw" ], angles, msg.speed)
            response = arm_controller_serviceResponse()
            response.ack = "ACK"
            return response
        except:
            self.motion_proxy = ALProxy("ALMotion", self.ip, self.port)
            self.motion_proxy.setAngles(["LShoulderPitch","LWristYaw" ], angles, msg.speed)


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
        node = ArmMotionNode(options.ip, int(options.port))
        node.start()
    except rospy.ROSInterruptException:
        pass

