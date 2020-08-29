# starts robot with line following controller without the server

import atexit
from hardware.robot import Robot
import hardware.camera as cam
from autonomy.controllers.linefollowing import LineFollowing

robot = Robot.getInstance() 

# called on exit to clean up
def exit_handler():
    print('\nTerminating Program')
    cam.closeCamera()
    Robot.getInstance().turnOff()
    print('Program Terminated')

atexit.register(exit_handler)
robot.setController(LineFollowing())
robot.turnOn()

# robot runs in a seperate daemon thread
# while true stops program from ending instantly

while True:
    pass