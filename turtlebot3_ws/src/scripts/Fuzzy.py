 
import rclpy
import math

from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf2_ros import TransformRegistration
from rclpy.qos import QoSProfile, ReliabilityPolicy


mynode_ = None
pub_ = None
regions_ = {
    'right': 0,
    'fright': 0,
    'front1': 0,
    'front2': 0,
    'fleft': 0,
    'left': 0,
}
twstmsg_ = None

eprevious = 0
eI=0


# main function attached to timer callback
def timer_callback():
    global pub_, twstmsg_
    if ( twstmsg_ != None ):
        pub_.publish(twstmsg_)


def clbk_laser(msg):
    global regions_, twstmsg_
    
    regions_ = {
        #LIDAR readings are anti-clockwise
        'front1':  find_nearest (msg.ranges[0:5]),
        'front2':  find_nearest (msg.ranges[355:360]),
        'right':  find_nearest(msg.ranges[265:275]),
        'fright': find_nearest (msg.ranges[310:320]),
        'fleft':  find_nearest (msg.ranges[40:50]),
        'left':   find_nearest (msg.ranges[85:95])
        
    }    
    twstmsg_= movement()

    
# Find nearest point
def find_nearest(list):
    f_list = filter(lambda item: item > 0.0, list)  # exclude zeros
    return min(min(f_list, default=10), 10)

#Basic movement method
def movement():
    #print("here")
    global regions_, mynode_
    regions = regions_
    
    print("Min distance in right region: ", regions_['right'])
    
    #create an object of twist class, used to express the linear and angular velocity of the turtlebot 
    msg = Twist()
    
    #If an obstacle is found to be within 0.25 of the LiDAR sensors front region the linear velocity is set to 0 (turtlebot stops)
    '''if (regions_['front1'])< 0.25:
        msg.linear.x = 0.0
        msg.angular.z = 0.0
        return msg
    #if there is no obstacle in front of the robot, it continues to move forward
    elif (regions_['front2'])< 0.25:
        msg.linear.x = 0.0
        msg.angular.z = 0.0
        return msg
    else:'''
    x= PID()
    msg.linear.x = 0.1
    msg.angular.z = x
    return msg
        

	

def Fuzzy():

    a=0.25
    b=0.5
    c=0.75
    x=0.6

def front_right_Sensor(a,b,c,x)
    


    y_Low=Low(a,b,x)
    y_Medium=Medium (a,b,c,x)
    y_High=High(b,c,x)


    
a=0.25
b=0.5
c=0.75
x=0.6

def Back_right_Sensor(a,b,c,x)
    
    y_Low=Low(a,b,x)
    y_Medium=Medium (a,b,c,x)
    y_High=High(b,c,x)




def Low(a,b,x):
    # Low Sensor
    if 0<=x<=a:
        y_Low=1
        return ('y_Low',y_Low)
    if a<x<=b:
        y_Low=b-x/b-a
    return ('y_Low',y_Low)

def Medium (a,b,c,x):
    # Medium Sensor
    if a<=x<=b:
        y_Medium=x-a/b-a
        return ('y_Medium',y_Medium)
    
    if b<x<=c:
        y_Medium=c-x/c-b
        return ('y_Medium',y_Medium)
    
def High(b,c,x):
    if b<=x<=c:
        y_High=x-a/b-a
        return ('y_Hig',y_High)
    
    if b<x<=c:
        y_High=c-x/c-b
        return ('y_Hig',y_High)


    


	


	




#used to stop the rosbot
def stop():
    global pub_
    msg = Twist()
    msg.angular.z = 0.0
    msg.linear.x = 0.0
    pub_.publish(msg)


def main():
    global pub_, mynode_global

    rclpy.init()
    mynode_ = rclpy.create_node('reading_laser')

    # define qos profile (the subscriber default 'reliability' is not compatible with robot publisher 'best effort')
    qos = QoSProfile(
        depth=10,
        reliability=ReliabilityPolicy.BEST_EFFORT,
    )

    # publisher for twist velocity messages (default qos depth 10)
    pub_ = mynode_.create_publisher(Twist, '/cmd_vel', 10)

    # subscribe to laser topic (with our qos)
    sub = mynode_.create_subscription(LaserScan, '/scan', clbk_laser, qos)

    # Configure timer
    timer_period = 0.2  # seconds 
    timer = mynode_.create_timer(timer_period, timer_callback)

    # Run and handle keyboard interrupt (ctrl-c)
    try:
        rclpy.spin(mynode_)
    except KeyboardInterrupt:
        stop()  # stop the robot
    except:
        stop()  # stop the robot
    finally:
        # Clean up
        mynode_.destroy_timer(timer)
        mynode_.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
