import sys
import time
import tempfile
import ikpy
from ikpy.chain import Chain
import math
from controller import Supervisor
from controller import Robot

IKPY_MAX_ITERATIONS = 1
robot = Robot()
# Initialize the Webots Supervisor.
#robot = Supervisor()
timeStep = int(4 * robot.getBasicTimeStep())

filename = None
fh=open('aaa.urdf','wb')
with tempfile.NamedTemporaryFile(suffix='.urdf', delete=False) as file:
    filename = file.name
    file.write(robot.getUrdf().encode('utf-8'))
    fh.write(robot.getUrdf().encode('utf-8'))
armChain = Chain.from_urdf_file(filename)
#print(armChain)
for i in [0, 6]:
    armChain.active_links_mask[0] = False

# Initialize the arm motors and encoders.
motors = []
for link in armChain.links:
    if 'm' in link.name:
        print(link.name)
        motor = robot.getDevice(link.name)
        motor.setVelocity(10.0) 
        #motor.setPosition(2.0)               
        position_sensor = motor.getPositionSensor()
        position_sensor.enable(timeStep)
        motors.append(motor)

c=0
while True:
    motors[0].setPosition(2.5)
    motors[1].setPosition(0.5)
    motors[2].setPosition(0.25)
    motors[3].setPosition(1.5)
    motors[4].setPosition(0.85)
    c+=1
    if c>=1:
        break
