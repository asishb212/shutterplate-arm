#! /usr/bin/env python

import rospy
import sys
import moveit_commander
import moveit_msgs
import geometry_msgs.msg
from tf.transformations import euler_from_quaternion,quaternion_from_euler
import yaml
import time

moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node("lol",anonymous=True)
robot=moveit_commander.RobotCommander()
scene = moveit_commander.PlanningSceneInterface()

group_name = "arm"
group = moveit_commander.MoveGroupCommander(group_name)
planning_frame = group.get_planning_frame()
eef_link = group.get_end_effector_link()
group_names = robot.get_group_names()

grasping_group = 'end'
touch_links = robot.get_link_names(group=grasping_group)

box_pose = geometry_msgs.msg.PoseStamped()
box_pose.header.frame_id = "c7"
box_pose.pose.orientation.w = 1.0
box_name = "box"
scene.add_box(box_name, box_pose, size=(0.1, 0.1, 0.1))
scene.attach_box(eef_link, box_name, touch_links=touch_links)