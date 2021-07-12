# shutterplate-arm
![python](https://img.shields.io/badge/Python-3.8-yellow)
![ROS](https://img.shields.io/badge/ROS-Noetic-brightgreen)
![CMake](https://img.shields.io/badge/CMake-3.3-critical)
<p></p>
<h2>for webots</h2>
<p>use "blah" folder</p>
<p>contains proto,wbt and controller script for shutterplate assembly arm</p>
<h2>ROS packages</h2>
<p>use asseyend for urdfs</p>
<p>use asseyendmvit for moveit</p>
<h2><b>ROS supported version : NOETIC </b></h2>
![NOETIC INSTALLATION](http://wiki.ros.org/noetic/Installation) 
<h2>ROS requirements</h2>

````
sudo apt install ros-noetic-moveit
sudo apt install ros-noetic-moveit-ros-planning
sudo apt-get install ros-noetic-ros-control ros-noetic-ros-controllers
sudo apt-get install ros-noetic-robot-state-publisher
````

<h2>setup</h2>

````
mkdir -p catkin_ws/src
cd catkin_ws/
catkin_make
cd src/
git clone https://github.com/asishb212/shutterplate-arm.git
git clone https://github.com/pal-robotics/gazebo_ros_link_attacher.git
cd ..
catkin_make
````

<h2>Run simulation!!</h2>

````
roslaunch asseyendmvit main.launch
````
