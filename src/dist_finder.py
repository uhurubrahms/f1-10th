#!/usr/bin/env python

import rospy
import math
from sensor_msgs.msg import LaserScan
from race.msg import pid_input

desired_trajectory = 1
vel = 5

pub = rospy.Publisher('error', pid_input, queue_size=10)

## Input: data: Lidar scan data
## theta: The angle at which the distance is requried
## OUTPUT: distance of scan at angle theta
def getRange(data,theta):
    """ Find the index of the arary that corresponds to angle theta.
    Return the lidar scan value at that index
    Do some error checking for NaN and absurd values """
    car_theta = math.radians(theta) - math.pi / 2
    if car_theta > 3 * math.pi / 4:
        car_theta = 3 * math.pi / 4
    elif car_theta < -3 * math.pi / 4:
        car_theta = -3 * math.pi / 4

    float_index = (car_theta + 3 * math.pi / 4) / data.angle_increment
    index = int(float_index)
    return data.ranges[index]
    

def callback(data):
    theta = 50;
    a = getRange(data, theta)
    b = getRange(data, 0)
    swing = math.radians(theta)

    alpha = math.atan2( a * math.cos(swing) - b , a * math.sin(swing) )
    AB = b * math.cos(alpha)

    error = AB - desired_trajectory

    #ABprime = a * math.cos(math.asin(a * math.sin(swing) / math.sqrt(a*a + b*b - 2*a*b*math.cos(swing))) - math.pi / 2 + swing)

    print "a {}\nb {}".format(a, b)
    print "AB {}".format(AB)
    #print "ABprime {}".format(ABprime)
    print "error {}".format(error)

    msg = pid_input()
    msg.pid_error = error
    msg.pid_vel = vel
    pub.publish(msg)
    

if __name__ == '__main__':
    print("Laser node started")
    rospy.init_node('dist_finder',anonymous = True)
    rospy.Subscriber("scan",LaserScan,callback)
    rospy.spin()