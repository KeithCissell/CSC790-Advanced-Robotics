#!/user/bin/env python

from __future__ import print_function
from __future__ import division

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist

import numpy as np


g_orange_left_frac = 0
g_orange_right_frac = 0


def frac_callback(orange_frac):
    
    global g_orange_left_frac, g_orange_right_frac
    g_orange_left_frac = float(orange_frac.data.split(' ')[0])
    g_orange_right_frac = float(orange_frac.data.split(' ')[1])
    
    print(g_orange_left_frac, g_orange_right_frac)
    
    
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
        
        left_right_sum = g_orange_left_frac + g_orange_right_frac
        
        # Scan for orange
        if (left_right_sum == 0.0):
            vel_msg.linear.x = 0.0
            vel_msg.angular.z = 0.8
            # print("Scanning...")
        else:
            # Find the pct diff
            left_pct = g_orange_left_frac / left_right_sum
            right_pct = g_orange_right_frac / left_right_sum
            pct_diff = left_pct - right_pct
            # print("Preping move...", pct_diff)
            
            # Move forward
            if (pct_diff >= 0.45 and pct_diff <= 0.55):
                vel_msg.linear.x = 0.3
                vel_msg.angular.z = 0.0
            # Veer right
            elif (pct_diff < 0.45):
                vel_msg.linear.x = 0.3
                vel_msg.angular.z = -0.1
            # Veer left
            elif (pct_diff > 0.55):
                vel_msg.linear.x = 0.3
                vel_msg.angular.z = 0.1
        
        # print(vel_msg.linear.x, vel_msg.angular.z)
        control_publisher.publish(vel_msg)
        rate.sleep()


if __name__ == '__main__':
    rospy.init_node('orange_frac_controller', anonymous=True)
    
    rospy.Subscriber('/ddr/orange_frac', String, frac_callback)
    
    try:
        run_control_publisher()
    except rospy.ROSInterruptException:
        pass
    
    rospy.spin()