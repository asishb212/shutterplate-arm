#! /usr/bin/env python

import rospy
import sys
import moveit_commander
import geometry_msgs.msg
from gazebo_ros_link_attacher.srv import Attach, AttachRequest
from tf.transformations import euler_from_quaternion,quaternion_from_euler
import yaml
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
print("attach plugin loaded \033[0;32m")

joint_goal = arm.get_current_pose().pose
print(joint_goal)

with open("/home/asish/catkin_ws/src/asseyendmvit/scripts/coords.yaml",'r') as file:
    poses=yaml.load(file,Loader=yaml.FullLoader)

pose1=geometry_msgs.msg.Pose()
pose1.position.x=poses['pickerup']['position']['x']
pose1.position.y=poses['pickerup']['position']['y']
pose1.position.z=poses['pickerup']['position']['z']
pose1.orientation.w=poses['pickerup']['orientation']['w']
pose1.orientation.x=poses['pickerup']['orientation']['x']
pose1.orientation.y=poses['pickerup']['orientation']['y']
pose1.orientation.z=poses['pickerup']['orientation']['z']

pose2=geometry_msgs.msg.Pose()
pose2.position.x=poses['pickerdown']['position']['x']
pose2.position.y=poses['pickerdown']['position']['y']
pose2.position.z=poses['pickerdown']['position']['z']
pose2.orientation.w=poses['pickerdown']['orientation']['w']
pose2.orientation.x=poses['pickerdown']['orientation']['x']
pose2.orientation.y=poses['pickerdown']['orientation']['y']
pose2.orientation.z=poses['pickerdown']['orientation']['z']

pose3=geometry_msgs.msg.Pose()
pose3.position.x=poses['dropup']['position']['x']
pose3.position.y=poses['dropup']['position']['y']
pose3.position.z=poses['dropup']['position']['z']
pose3.orientation.w=poses['dropup']['orientation']['w']
pose3.orientation.x=poses['dropup']['orientation']['x']
pose3.orientation.y=poses['dropup']['orientation']['y']
pose3.orientation.z=poses['dropup']['orientation']['z']

pose4=geometry_msgs.msg.Pose()
pose4.position.x=poses['dropdown']['position']['x']
pose4.position.y=poses['dropdown']['position']['y']
pose4.position.z=poses['dropdown']['position']['z']
pose4.orientation.w=poses['dropdown']['orientation']['w']
pose4.orientation.x=poses['dropdown']['orientation']['x']
pose4.orientation.y=poses['dropdown']['orientation']['y']
pose4.orientation.z=poses['dropdown']['orientation']['z']

iters=1
delay=0
work_delay=1
for i in range(iters):

    arm.set_pose_target(pose1)
    plan=arm.go(wait=True)
    time.sleep(delay)

    arm.set_pose_target(pose2)
    plan=arm.go(wait=True)
    
    print("Attaching cylinder to arm")
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
    rospy.loginfo("Detaching cylinder to arm \033[0;32m")
    req = AttachRequest()
    req.model_name_1 = "robot"
    req.link_name_1 = "c6"
    req.model_name_2 = "unit_cylinder"
    req.link_name_2 = "link"
    detach_srv.call(req)

    arm.set_pose_target(pose3)
    plan=arm.go(wait=True)
    time.sleep(delay)
    
