import sys
import time
import tempfile
import ikpy
from ikpy.chain import Chain
import math
from controller import Supervisor

IKPY_MAX_ITERATIONS = 1

# Initialize the Webots Supervisor.
supervisor = Supervisor()
timeStep = int(4 * supervisor.getBasicTimeStep())

# Create the arm chain from the URDF
filename = None
fh=open('aaa.urdf','wb')
with tempfile.NamedTemporaryFile(suffix='.urdf', delete=False) as file:
    filename = file.name
    file.write(supervisor.getUrdf().encode('utf-8'))
    fh.write(supervisor.getUrdf().encode('utf-8'))
armChain = Chain.from_urdf_file(filename)

for i in [0, 6]:
    armChain.active_links_mask[0] = False

# Initialize the arm motors and encoders.
motors = []
for link in armChain.links:
    if 'm' in link.name:
        motor = supervisor.getDevice(link.name)
        motor.setVelocity(0.5)
        position_sensor = motor.getPositionSensor()
        position_sensor.enable(timeStep)
        motors.append(motor)

def pickup(motors):
    while supervisor.step(timeStep) != -1:
        motors[0].setPosition(0.2)
        motors[1].setPosition(-0.55)
        motors[2].setPosition(-0.4)
        motors[3].setPosition(0.7)
        motors[4].setPosition(0.3)

        position = armChain.forward_kinematics([0] + [m.getPositionSensor().getValue() for m in motors] + [0])
        print(position)
        break

def move(coord):
    while supervisor.step(timeStep) != -1:
        x,y,z=coord
        # Call "ikpy" to compute the inverse kinematics of the arm.
        initial_position = [0] + [m.getPositionSensor().getValue() for m in motors] + [0]
        ikResults = armChain.inverse_kinematics([x, y, z], max_iter=IKPY_MAX_ITERATIONS, initial_position=initial_position)
    
        # Recalculate the inverse kinematics of the arm if necessary.
        position = armChain.forward_kinematics(ikResults)
        squared_distance = (position[0, 3] - x)**2 + (position[1, 3] - y)**2 + (position[2, 3] - z)**2
        if math.sqrt(squared_distance) < 0.01:
            return True
        # Actuate the arm motors with the IK results.
        for i in range(4):
            motors[i].setPosition(ikResults[i + 1])
        motors[4].setPosition(ikResults[2] - ikResults[3] + math.pi / 2)
        # Keep the hand orientation perpendicular.
        motors[5].setPosition(ikResults[1])

coords=[[0.19,-0.4,0.63],[0.19,0.4,0.63]]
delay=0.5

def main():
    if move(coords[0]):pass  
    supervisor.step(100)
    print("1")
    if move(coords[1]):pass  
    time.sleep(delay)
    print('done')

iters=1
for i in range(iters):
    #pickup(motors)
    main()
