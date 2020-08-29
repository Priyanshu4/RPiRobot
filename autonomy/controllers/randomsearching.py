from RobotControllers.RandomlyMoving import RandomMoving
import Hardware.Camera as cam
from Autonomy.Vision.LineDetectionPipeline import LineDetectionPipeline
from Autonomy.PIDController import PIDController
from Network.VideoServer.VideoServer import VideoServer
import Autonomy.Vision.Contours as conts
from cv2 import drawContours


class RandomSearching(RandomMoving):
    """robot moves randomly and stays withing a boundary"""

    def __init__(self, robot = None):
        super().__init__(robot)
 
        # pipeline for boundary detection, calibrated for blue yarn lines 
        self.visionPipeline = LineDetectionPipeline(minHue = 98, maxHue = 117, minSat = 151, maxSat = 255, minVal = 0, maxVal = 254)

        # turn speed when it sees a contour
        self.contourTurnSpeed = 1
        self.contourTurnDir = True

        # random move robot variables
        self.forwardSpeed = 1
        self.turnSpeed = 1
        self.minForwardTime = 100
        self.maxForwardTime = 100

    def setup(self):
        self.wasSeeingContour = False

    def loop(self):
        image = self.robot.currentCameraImage
        self.visionPipeline.process(image)
        contours = self.visionPipeline.find_contours_output
        self.annotateImage(image, contours)
        if self.isCloseToBoundary(contours):
            self.robot.drivetrain.setForwardAndTurnSpeed(-self.forwardSpeed, 0)
            self.wasSeeingContour = True
        elif self.wasSeeingContour:
            self.getNewRandomMove(False)
            self.wasSeeingContour = False
        else:
            super().loop(deltaTime)
   
    def isCloseToBoundary(self, contours):
        imgWidth, imgHeight = cam.getCamera().resolution
        for contour in contours:
            if conts.getMinY(contour) > imgHeight / 2:
                return True
        return False

    def annotateImage(self, image, contours):
        drawContours(image, contours, -1, (0,255,0))