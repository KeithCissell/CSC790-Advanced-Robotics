#!/user/bin/env python

from __future__ import print_function
from __future__ import division

import rospy
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist

import numpy as np


angle_to_barrel = 100


def angle_callback(angle):
    
    global angle_to_barrel

    angle_to_barrel = angle.data
    
    print(angle_to_barrel)
    
    
def run_control_publisher():
    control_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    
    rate = rospy.Rate(10)
    
    # Initialize twist message to all zeros
    vel_msg = Twist()
    vel_msg.linear.x = 0.0
    vel_msg.linear.y = 0.0
    vel_msg.linear.z = 0.0
    vel_msg.angular.x = 0.0
    vel_msg.angular.y = 0.0
    vel_msg.angular.z = 0.0
    
    while not rospy.is_shutdown():
        
        # Scan for orange
        if (angle_to_barrel > 99.0):
            vel_msg.linear.x = 0.0
            vel_msg.angular.z = 0.3
            print("Scanning...")
        # Move forward
        elif (angle_to_barrel >= -0.25 and angle_to_barrel <= 0.25):
            vel_msg.linear.x = 0.3
            vel_msg.angular.z = 0.0
            print("Forward March")
        # Veer right
        elif (angle_to_barrel > 0.25):
            vel_msg.linear.x = 0.3
            vel_msg.angular.z = 0.1
            print("Veer Right")
        # Veer left
        elif (angle_to_barrel < -0.25):
            vel_msg.linear.x = 0.3
            vel_msg.angular.z = -0.1
            print("Veer Left")

        # print(vel_msg.linear.x, vel_msg.angular.z)
        control_publisher.publish(vel_msg)
        rate.sleep()


if __name__ == '__main__':
    rospy.init_node('ddr_angle_controller', anonymous=True)
    
    rospy.Subscriber('/ddr/angle_to_barrel_rads', Float64, angle_callback)
    
    try:
        run_control_publisher()
    except rospy.ROSInterruptException:
        pass
    
    rospy.spin()