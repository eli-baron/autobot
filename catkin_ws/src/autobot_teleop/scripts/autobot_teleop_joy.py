#!/usr/bin/env python
import rospy

def main():
    #according with the tutorials, add here the publisher declarations, the init_node and rate
    rospy.init_node('autobot_teleop', anonymous=True)
    rate = rospy.Rate(10)   #10Hz
    while not rospy.is_shutdown():
        #and add here maybe the publish method of the publisher and sleep method of the rate
        rate.sleep()

if __name__== '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass