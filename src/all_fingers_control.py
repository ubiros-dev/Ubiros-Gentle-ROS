#!/usr/bin/env python
#This code is written by Mostafa Atalla to automate the control of the Ubiros Gentle Pro Soft gripper
#Updated to control all Ubiros Gentle series soft grippers
#


import rospy
import time
import sys, select, termios, tty
from std_msgs.msg import Int8
from std_msgs.msg import Int16

currentLoad = 0

msg = """
Press w to close all of the fingers slowly
Press s to open all of the fingers slowly
Press a to close all of the fingers quickly
Press z to open all of the fingers quickly

"""

#getkey function is for detecting the key entered through the keyboard
def getKey():
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


def updateLoad(data):
    global currentLoad
    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    currentLoad = data.data

#This if statement is making sure that this is the node that is called directly by the user
if __name__=="__main__":

    settings = termios.tcgetattr(sys.stdin)
    rospy.init_node('all_fingers_control')
    pub = rospy.Publisher('UbirosGentle', Int8, queue_size = 1)
    #pubPro = rospy.Publisher('UbirosGentlePro', Int8, queue_size = 1)
    sub = rospy.Subscriber('UbirosGentleLoad', Int16, updateLoad)

#Initiation of variables
    p_increment=5
    n_increment=-5
    all_fingers=50
    #all_fingers_old=50
    status = 0
    #sleepFlag = 0

    time.sleep(3)
    print(msg)

#The main while loop the keeps the code running until the user closes it and it takes actions based on the key pressed
    while(1):
        key = getKey()
        if (key == '\x03'):
            break
	elif (key == '\x1b'):
	    break
        elif (key == 'w'):
	    all_fingers+=p_increment
	    
        elif (key=='s'):
            all_fingers+=n_increment
	    
        elif (key == 'a'):
	    while (all_fingers < 100):
	        all_fingers += p_increment
	        pub.publish(all_fingers)
	        time.sleep(0.02)
	        print 'Percentage: ', all_fingers, '%     Load: ', currentLoad

        elif (key == 'z'):
	    while (all_fingers > 0):
	        all_fingers += n_increment
	        pub.publish(all_fingers)
	        time.sleep(0.02)
	        print 'Percentage: ', all_fingers, '%     Load: ', currentLoad


	elif (key == 'l'):
	    print 'Current load is', currentLoad
            
        else:
            print('Enter the proper key')
            
        if (status == 10):
            print(msg)
	
	status = (status + 1) % 15

	if (key != 'l'):
	    if (all_fingers>100):
	        all_fingers = 100
    	        print('Max Stroke has been achieved')

	    elif (all_fingers<0):
	        all_fingers = 0
	        print('Min Stroke has been achieved')
	
#	    else:
#		print 'Current close percentage is', all_fingers, '%'
	    print 'Percentage: ', all_fingers, '%     Load: ', currentLoad
	    pub.publish(all_fingers)
	    

	#pubPro.publish(all_fingers)
        #all_fingers_old=all_fingers
	#if (sleepFlag == 1):
	#    time.sleep(0.5)
        #    sleepFlag = 0

#This two lines are executed once the user exits the code, they return the fingers back to 50% position.
    all_fingers=50
    pub.publish(all_fingers)
    #pubPro.publish(all_fingers)

