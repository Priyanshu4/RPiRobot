import atexit
from hardware.robot import Robot
import hardware.camera as cam
import server.controlserver as controlserver

robot = Robot.getInstance() 

# called on exit to clean up
def exit_handler():
    print('\nTerminating Program')
    cam.closeCamera()
    Robot.getInstance().turnOff()
    print('Program Terminated')

atexit.register(exit_handler)
controlserver.startServer()
