from autonomy.controllers.robotcontroller import RobotController
import cv2
import autonomy.vision.contours as conts
from autonomy.vision.linedetection import LineDetectionPipeline
from autonomy.pidcontrol import PIDController
import hardware.camera as cam
from robotconfiguration import lineHueThreshold, lineSatThreshold, lineValThreshold


class LineFollowing(RobotController):
    """controller for following a line"""

    def __init__(self, robot = None):
        super().__init__(robot)

        # pipeline calibrated for blue yarn lines
        minHue, maxHue = lineHueThreshold
        minSat, maxSat = lineSatThreshold
        minVal, maxVal = lineValThreshold
        self.visionPipeline = LineDetectionPipeline(minHue, maxHue, minSat, maxSat, minVal, maxVal)
       
        self.PID = PIDController(kP = 0.7)
        
        self.fwdSpeed = 0.5 # forward speed

        self.sharpTurnMultiplier = 2 # turnspeed multiplier for when a sharp turn is detected

        # variables for backing up and looking around when no contours are found
        self.turnDirection = True # the current turn direction of the robot (right is True)
        self.framesWithoutContour = 0 # frames that have passed without a contour found
        self.lookingForFrames = 0 # how many frames the robot has been looking for in current direction
        self.framesTillLook = 5 # number of frames without contours till robot starts "looking around"
        self.initialFramesToLook = 10 # initial frames to look around for till direction change
        self.framesToLook = self.initialFramesToLook # frames to look till a direction change
        self.frameLookingIncrements = 4 # increment of framesToLook
        self.lookingTurnSpeed = 0.5 # speed to turn at while looking


    def setup(self):
        imageWidth, imageHeight = cam.getCamera().resolution
        imageCenterX, imageCenterY = imageWidth // 2, imageHeight // 2
        self.annotationY = imageCenterY # y-value at which to draw the error line on the image
        self.setpointX = imageCenterX # target x-value to align the line with

    def loop(self):
        image = self.robot.currentCameraImage
        self.visionPipeline.process(image)
        contours = self.visionPipeline.find_contours_output
        numContours = len(contours)
        print(numContours, 'contours found.')
        if numContours > 0:
            contourMinX, contourMaxX, contourCenterX = self.analyzeContours(contours)
            error = (contourCenterX - self.setpointX) / self.setpointX
            turnSpeed = self.PID.executeControlLoop(error, self.robot.deltaTime)
            if self.isSharpTurn(contourMinX, contourMaxX):
                turnSpeed = turnSpeed * self.sharpTurnMultiplier
                print('SHARP TURN')
            self.robot.drivetrain.setForwardAndTurnSpeed(self.fwdSpeed, turnSpeed)
            self.robot.currentDisplayImage = self.annotateImage(image, contours, contourCenterX)
            self.turnDirection = turnSpeed > 0
            self.lookingForFrames = self.initialFramesToLook
            self.framesWithoutContour = 0
        else:
            self.robot.currentDisplayImage = image
            self.framesWithoutContour += 1
            print('FramesWithoutContour', self.framesWithoutContour)
            if self.framesWithoutContour > self.framesTillLook:
                self.lookAround() # turn back and forth, look for the line
            else:
                self.robot.drivetrain.stop()

    def analyzeContours(self, contours):
        largestContour = conts.getLargestContour(contours)
        minX = conts.getMinX(largestContour)
        maxX = conts.getMaxX(largestContour)
        centerX = (minX + maxX) // 2
        return minX, maxX, centerX

    def isSharpTurn(self, contourMinX, contourMaxX):
        imageWidth, imageHeight = cam.getCamera().resolution
        if contourMinX == 0 and contourMaxX > self.setpointX:
            return True
        elif contourMaxX == imageWidth and contourMinX < self.setpointX:
            return True
        else:
            return False

    def lookAround(self):
        self.lookingForFrames += 1
        if self.lookingForFrames < self.framesToLook:
            self.robot.drivetrain.turnInPlace(self.turnDirection, speed = self.lookingTurnSpeed)
        else:
            self.lookingForFrames = 0
            self.framesToLook += self.frameLookingIncrements
            self.turnDirection = not self.turnDirection

    def annotateImage(self, image, contours, contourCenterX):
        cv2.drawContours(image, contours, -1, (0,255,0))
        setpoint = (self.setpointX, self.annotationY)
        contourPt = (contourCenterX, self.annotationY)
        cv2.circle(image, contourPt, 2, (0, 255, 0), thickness = 2)
        cv2.line(image, setpoint, contourPt, (0, 0, 255), thickness = 3)
        return image
