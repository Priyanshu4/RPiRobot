from autonomy.controllers.robotcontroller import RobotController
from time import sleep
import random

class RandomlyMoving(RobotController):
    """controls robot with random movement"""

    def __init__(self, robot = None):
        super().__init__(robot)
        
        self.minForwardTime = 1
        self.maxForwardTime = 5 
        self.minTurnTime = 0.5
        self.maxTurnTime = 1.8
        
        self.turnSpeed = 1
        self.forwardSpeed = 0.5

    def setup(self):
        self.remainingMoveTime = self.getRandomTurnTime()
        self.getNewRandomMove(True)

    def loop(self):
        self.remainingMoveTime -= self.robot.deltaTime
        print('remainingMoveTime:', self.remainingMoveTime)
        if self.remainingMoveTime <= 0:
            self.getNewRandomMove(not self.movingForward)

    def getNewRandomMove(self, forward):
        self.movingForward = forward
        if self.movingForward:
            self.remainingMoveTime = self.getRandomForwardTime()
            self.robot.drivetrain.setForwardAndTurnSpeed(self.forwardSpeed, 0)
        else:
            self.remainingMoveTime = self.getRandomTurnTime()
            self.robot.drivetrain.turnInPlace(self.getRandomDirection(), speed = self.turnSpeed)

    def getRandomFloat(self, min, max):
        return random.random() * (max - min) + min

    def getRandomForwardTime(self):
        return self.getRandomFloat(self.minForwardTime, self.maxForwardTime)

    def getRandomTurnTime(self):
        return self.getRandomFloat(self.minTurnTime, self.maxTurnTime)
        
    def getRandomDirection(self):
        return random.choice([True, False])

