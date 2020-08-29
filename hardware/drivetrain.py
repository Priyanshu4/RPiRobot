class DriveTrain(object):
    """differential drivetrain of a robot, has left and right motors (or motor groups)"""

    def __init__(self, leftMotor, rightMotor):
        self.leftMotor = leftMotor
        self.rightMotor = rightMotor

    def setMotorSpeeds(self, left, right):
        """ Sets the speed of left and right motors

        Speeds should be from (-1 to 1)
        Negative speed is backwards
        0 is stopped
        Positive speed is forwards

        """
        left = self.limitSpeed(left)
        right = self.limitSpeed(right)

        if left > 0:
            self.leftMotor.forward(left)
        elif left < 0: 
            self.leftMotor.backward(-left)
        else:
            self.leftMotor.stop()

        if right > 0:
            self.rightMotor.forward(right)
        elif right < 0: 
            self.rightMotor.backward(-right)
        else:
            self.rightMotor.stop()
     
    def setForwardAndTurnSpeed(self, forwardSpeed, turnSpeed):
        left = forwardSpeed + turnSpeed
        right = forwardSpeed - turnSpeed
        self.setMotorSpeeds(left, right)

    def turnInPlace(self, direction, speed = 1):
        """
        Turns in place. Direction = True for right, False for left
        """
        if direction:
            self.setMotorSpeeds(speed, -speed)
        else:
            self.setMotorSpeeds(-speed, speed)

    def stop(self):
        self.leftMotor.stop()
        self.rightMotor.stop()

    def reverse(self):
        self.leftMotor.reverse()
        self.rightMotor.reverse()

    def limitSpeed(self, speed):
        if speed > 1:
            return 1
        elif speed < -1:
            return -1
        else:
            return speed

    def getSpeeds(self):
            return leftMotor.value(), rightMotor.value()
