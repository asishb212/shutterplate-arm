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
print(armChain)
for i in [0, 6]:
    armChain.active_links_mask[0] = False

# Initialize the arm motors and encoders.
motors = []
for link in armChain.links:
    if 'm' in link.name:
        motor = supervisor.getDevice(link.name)
        motor.setVelocity(1.0)
        position_sensor = motor.getPositionSensor()
        position_sensor.enable(timeStep)
        motors.append(motor)

motors[4].setPosition(1.3)