#! /usr/bin/env python

import rospy
import sys
import moveit_commander
import geometry_msgs.msg
from gazebo_ros_link_attacher.srv import Attach, AttachRequest
from tf.transformations import euler_from_quaternion,quaternion_from_euler
import time

moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node("lol",anonymous=True)
robot=moveit_commander.RobotCommander()

arm=moveit_commander.MoveGroupCommander("arm")
grip=moveit_commander.MoveGroupCommander("end")

attach_srv = rospy.ServiceProxy('/link_attacher_node/attach',Attach)
attach_srv.wait_for_service()
detach_srv = rospy.ServiceProxy('/link_attacher_node/detach',Attach)
detach_srv.wait_for_service()
rospy.loginfo("\033[0;32m attach plugin loaded \033[0;32m")

pose1=geometry_msgs.msg.Pose()
pose1.position.x=rospy.get_param('/pickerup/position/x')
pose1.position.y=rospy.get_param('/pickerup/position/y')
pose1.position.z=rospy.get_param('/pickerup/position/z')
pose1.orientation.w=rospy.get_param('/pickerup/orientation/w')
pose1.orientation.x=rospy.get_param('/pickerup/orientation/x')
pose1.orientation.y=rospy.get_param('/pickerup/orientation/y')
pose1.orientation.z=rospy.get_param('/pickerup/orientation/z')

pose2=geometry_msgs.msg.Pose()
pose2.position.x=rospy.get_param('/pickerdown/position/x')
pose2.position.y=rospy.get_param('/pickerdown/position/y')
pose2.position.z=rospy.get_param('/pickerdown/position/z')
pose2.orientation.w=rospy.get_param('/pickerdown/orientation/w')
pose2.orientation.x=rospy.get_param('/pickerdown/orientation/x')
pose2.orientation.y=rospy.get_param('/pickerdown/orientation/y')
pose2.orientation.z=rospy.get_param('/pickerdown/orientation/z')

pose3=geometry_msgs.msg.Pose()
pose3.position.x=rospy.get_param('/dropup/position/x')
pose3.position.y=rospy.get_param('/dropup/position/y')
pose3.position.z=rospy.get_param('/dropup/position/z')
pose3.orientation.w=rospy.get_param('/dropup/orientation/w')
pose3.orientation.x=rospy.get_param('/dropup/orientation/x')
pose3.orientation.y=rospy.get_param('/dropup/orientation/y')
pose3.orientation.z=rospy.get_param('/dropup/orientation/z')

pose4=geometry_msgs.msg.Pose()
pose4.position.x=rospy.get_param('/dropdown/position/x')
pose4.position.y=rospy.get_param('/dropdown/position/y')
pose4.position.z=rospy.get_param('/dropdown/position/z')
pose4.orientation.w=rospy.get_param('/dropdown/orientation/w')
pose4.orientation.x=rospy.get_param('/dropdown/orientation/x')
pose4.orientation.y=rospy.get_param('/dropdown/orientation/y')
pose4.orientation.z=rospy.get_param('/dropdown/orientation/z')

iters=1
delay=0
work_delay=1
for i in range(iters):

    arm.set_pose_target(pose1)
    plan=arm.go(wait=True)
    time.sleep(delay)

    arm.set_pose_target(pose2)
    plan=arm.go(wait=True)
    
    rospy.loginfo("\033[0;32m attaching cylinder to arm \033[0;32m")
    req = AttachRequest()
    req.model_name_1 = "robot"
    req.link_name_1 = "c6"
    req.model_name_2 = "unit_cylinder"
    req.link_name_2 = "link"
    attach_srv.call(req)
    time.sleep(2)
    
    arm.set_pose_target(pose1)
    plan=arm.go(wait=True)
    time.sleep(delay)

    joints=arm.get_current_joint_values()
    joints[0]=-3.085023245079391
    plan=arm.go(joints)
    time.sleep(delay)

    #arm.set_pose_target(pose3)
    #plan=arm.go(wait=True)
    #time.sleep(delay)
    
    arm.set_pose_target(pose4)
    plan=arm.go(wait=True)
    time.sleep(delay)
    
    time.sleep(2)
    rospy.loginfo("\033[0;32m Detaching cylinder to arm \033[0;32m")
    req = AttachRequest()
    req.model_name_1 = "robot"
    req.link_name_1 = "c6"
    req.model_name_2 = "unit_cylinder"
    req.link_name_2 = "link"
    detach_srv.call(req)

    arm.set_pose_target(pose3)
    plan=arm.go(wait=True)
    time.sleep(delay)
    
