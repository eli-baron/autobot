#! /usr/bin/env python

import rospy
from roboclaw import Roboclaw
from geometry_msgs.msg import Twist
from ackermann_msgs.msg import AckermannDrive

global msg
msg=AckermannDrive()

#def cmd_vel_callback(twist):
	#global linear_x
#	linear_x=twist.linear.x
#	rospy.loginfo(twist.linear.x)
#	linear_x=twist.linear.x
#	msg.linear.x=twist.linear.x

#def roboclaw_test_node():
	#rospy.Subscriber("cmd_vel", Twist, cmd_vel_callback)
	#rospy.spin()
def ackermann_cmd_callback(data):
	msg.speed=data.speed

def main():
	rospy.init_node('mobile_base_node', anonymous=True)
	#rospy.Subscriber("cmd_vel", Twist, cmd_vel_callback)
	rospy.Subscriber("ackermann_cmd_topic", AckermannDrive, ackermann_cmd_callback)
	#global linear_x
	rate=rospy.Rate(10)
	rc=Roboclaw("/dev/ttyACM0",115200)
	rc.Open()
	address=0x80

	while not rospy.is_shutdown():
		rospy.loginfo(msg.speed)
		rc.ForwardM1(address,int(msg.speed*64))		#1/4 power forward
		rc.BackwardM2(address,int(msg.speed*64))	#1/4 power backward
		rate.sleep()
	#rospy.spin()

if __name__=='__main__':
	#global linear_x
	#roboclaw_test_node()
	main()
