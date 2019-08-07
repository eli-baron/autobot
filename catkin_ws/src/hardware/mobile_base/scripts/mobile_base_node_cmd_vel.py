#! /usr/bin/env python

import rospy
import tf
from roboclaw import Roboclaw
from geometry_msgs.msg import Twist

global msg
msg=Twist()

def cmd_vel_callback(data):
	msg.linear.x=data.linear.x

def main():
	rospy.init_node('mobile_base_node', anonymous=True)
	rospy.Subscriber("/hardware/mobile_base/cmd_vel", Twist, cmd_vel_callback)
	rate=rospy.Rate(10)
	rc=Roboclaw("/dev/ttyACM0",115200)
	rc.Open()
	address=0x80
	br = tf.TransformBroadcaster()
	autobot_x = 0

	while not rospy.is_shutdown():
		#rospy.loginfo(msg.linear.x)
		autobot_x += msg.linear.x*0.1
		if msg.linear.x > 0:
			rc.ForwardM1(address,int(msg.linear.x*100))		#1/4 power forward = 32
			rc.BackwardM2(address,int(msg.linear.x*100))	#1/4 power backward = 32
		elif msg.linear.x < 0:
			rc.BackwardM1(address,int(msg.linear.x*(-100)))
			rc.ForwardM2(address,int(msg.linear.x*(-100)))
		else:
			rc.ForwardM1(address,int(msg.linear.x))
			rc.BackwardM2(address,int(msg.linear.x))
		br.sendTransform((autobot_x, 0, 0), tf.transformations.quaternion_from_euler(0, 0, 0),rospy.Time.now(),"base_link","odom")
		#print "Sending transform"
		rate.sleep()
	#rospy.spin()

if __name__=='__main__':
	main()
