from gpiozero import Motor

class MotorGroup(object):
    """ a group (stored as tuple) of motors that are controlled together
        implements the same functions as gpiozero motor class, so they can be easily swapped
    """

    def __init__(self, *motors):
        self.motors = motors
        self.stop()

    def forward(self, speed = 1):
        """ All motors in group go forward, sets speed at given speed between 0 and 1 """
        for motor in self.motors: 
            motor.forward(speed = speed)

    def backward(self, speed = 1):
        """ All motors in group go forward, sets speed at given speed between 0 and 1 """
        for motor in self.motors: 
            motor.backward(speed = speed)

    def reverse(self):
        """ Reverses the direction of all motors in the group, speed stays the same """
        for motor in self.motors: 
            motor.reverse()

    def stop(self):
        """ Stops all motors in group """
        for motor in self.motors: 
            motor.stop()



