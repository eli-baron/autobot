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

	speed = 64	#half the [0-127] to get 0 speed in ForwardBackward command

	msgAckermann = AckermannDrive()
	rospy.init_node('mobile_base_node', anonymous=True)
	rospy.Subscriber("/ackermann", AckermannDrive, callbackAckermann)
	rate=rospy.Rate(10)
	rc=Roboclaw("/dev/ttyACM1",115200)
	rc.Open()
	address=0x80
	br = tf.TransformBroadcaster()
	autobot_x = 0

	while not rospy.is_shutdown():
		autobot_x += speed*0.001
		msgAckermann.speed = speed
		rc.ForwardBackwardM1(address,int(msgAckermann.speed))		#0 power forward = 64
		rc.ForwardBackwardM2(address,int(-msgAckermann.speed))	#0 power backward = 64
		br.sendTransform((autobot_x, 0, 0),tf.transformations.quaternion_from_euler(0,0,0),rospy.Time.now(),"base_link","odom")
		rate.sleep()
	#rospy.spin()

if __name__=='__main__':
	try:
	   	main()
	except rospy.ROSInterruptException:
		pass
