#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Joy
from ackermann_msgs.msg import AckermannDrive

def callbackJoy(msg):
    global speed
    global steering_angle

    leftStickY = msg.axes[1]    #The left stick Y controls the speed of the motors
    rightStickX = msg.axes[3]   #The right stick X controls the steering angle of the car

    speed = (leftStickY*32)+64  #The leftStickY value is between -1 and 1, converted to [0-128] to get the whole range, and [0-64] to get only half

    rightStickX = 0

def main():
    global speed
    global steering_angle
    
    speed = 64
    steering_angle = 0

    msgAckermann = AckermannDrive()

    #according with the tutorials, add here the publisher declarations, the init_node and rate
    rospy.init_node('autobot_teleop', anonymous=True)
    rospy.Subscriber("/joy", Joy, callbackJoy)
    pubAckermann = rospy.Publisher("/ackermann",AckermannDrive,queue_size=1)

    rate = rospy.Rate(10)   #10Hz
    while not rospy.is_shutdown():
        #and add here maybe the publish method of the publisher and sleep method of the rate
        msgAckermann.speed = speed
        msgAckermann.steering_angle = steering_angle
        pubAckermann.publish(msgAckermann)
        rate.sleep()

if __name__== '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass