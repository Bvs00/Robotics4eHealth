#!/usr/bin/env python

import rospy
from std_msgs.msg import Float32MultiArray

def talker():
    rospy.init_node('arm_controller', anonymous=True)
    #pub_r_pitch = rospy.Publisher('/arm_rotation/shoulder/right/pitch', Float32MultiArray, queue_size=1)
    #pub_r_wrist = rospy.Publisher('/arm_rotation/wrist/right/yaw',Float32MultiArray, queue_size=1)
    #pub_r_roll = rospy.Publisher('/arm_rotation/shoulder/right/roll',Float32MultiArray, queue_size=1)

    pub_l_pitch = rospy.Publisher('/arm_rotation/shoulder/left/pitch', Float32MultiArray, queue_size=1)
    pub_l_wrist = rospy.Publisher('/arm_rotation/wrist/left/yaw',Float32MultiArray, queue_size=1)
    #pub_l_roll = rospy.Publisher('/arm_rotation/shoulder/left/roll',Float32MultiArray, queue_size=1)

    angle_sholder = 0.5  # Replace with the desired angle
    speed = 0.1  # Replace with the desired speed

    # Publish the motion command
    msg_sholder = Float32MultiArray()
    msg_sholder.data = [angle_sholder, speed]

    angle_wrist_l = -1.8238
    #angle_wrist_r = 2.0

    
    msg_wrist_l = Float32MultiArray()
    msg_wrist_l.data = [angle_wrist_l, speed]

    #msg_wrist_r = Float32MultiArray()
    #msg_wrist_r.data = [angle_wrist_r, speed]

    #angle_roll_r = 1.0
    #angle_roll_l = -1.0

    #msg_roll_r = Float32MultiArray()
    #msg_roll_r.data = [angle_roll_r, speed]
    #msg_roll_l = Float32MultiArray()
    #msg_roll_l.data = [angle_roll_l, speed]



    #while pub_r_pitch.get_num_connections() <= 0:
    #    rospy.sleep(1.0)
    #pub_r_pitch.publish(msg_sholder)

    while pub_l_pitch.get_num_connections() <= 0:
        rospy.sleep(1.0)
    pub_l_pitch.publish(msg_sholder)

    while pub_l_wrist.get_num_connections() <= 0:
        rospy.sleep(1.0)
    pub_l_wrist.publish(msg_wrist_l)

    #while pub_r_wrist.get_num_connections() <= 0:
    #    rospy.sleep(1.0)
    #pub_r_wrist.publish(msg_wrist_r)

    #while pub_l_roll.get_num_connections() <= 0:
    #    rospy.sleep(1.0)
    #pub_l_roll.publish(msg_roll_l)

    #while pub_r_roll.get_num_connections() <= 0:
    #    rospy.sleep(1.0)
    #pub_r_roll.publish(msg_roll_r)
        

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
