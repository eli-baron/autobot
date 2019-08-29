#! /usr/bin/env python

import rospy
import tf
from roboclaw import Roboclaw
from ackermann_msgs.msg import AckermannDrive

def callbackAckermann(msg):
	global speed
	speed=msg.speed

def main():
	global speed

	speed = 0

	msgAckermann = AckermannDrive()
	rospy.init_node('mobile_base_node', anonymous=True)
	rospy.Subscriber("/ackermann", AckermannDrive, callbackAckermann)
	rate=rospy.Rate(10)
	rc=Roboclaw("/dev/ttyACM0",115200)
	rc.Open()
	address=0x80
	br = tf.TransformBroadcaster()
	autobot_x = 0

	while not rospy.is_shutdown():
		autobot_x += speed*0.001
		msgAckermann.speed = speed
		rc.ForwardBackwardM1(address,int(msgAckermann.speed))		#0 power forward = 64
		rc.ForwardBackwardM1(address,int(msgAckermann.speed))	#0 power backward = 64
		rate.sleep()
	#rospy.spin()

if __name__=='__main__':
	try:
    	main()
    except rospy.ROSInterruptException:
        pass
