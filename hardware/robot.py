import threading
from time import time
from robotconfiguration import drivetrain
import hardware.camera as cam
import server.controlserver as controlserver

class Robot(object):
    """singleton robot class
       contains a drivetrain, a camera, and a controller object
       this runs the methods in the controller that control the robot
    """
        
    instance = None

    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = Robot(drivetrain, camera = cam.getCamera())
        return cls.instance

    def __init__(self, drivetrain, camera = None, controller = None):
        self.drivetrain = drivetrain
        self.camera = camera
        self.controller = controller
        self.running = False

    def turnOn(self):
        if not self.running:
            print('Starting Robot')
            self.running = True
            self.currentCameraImage = None
            self.currentDisplayImage = None
            if self.controller is not None:
                self.controller.robot = self
                self.controller.setup()
            self.loopThread = threading.Thread(target = self.runLoop, daemon = True)
            self.loopThread.name = 'Robot Thread'
            self.loopThread.start()

    def runLoop(self):
        self.deltaTime = 0
        startTime = time()
        while (self.running):
            self.deltaTime = time() - startTime
            startTime = time()
            if self.camera is not None:
                self.currentCameraImage = cam.grabOpenCVImage(self.camera)
                self.currentDisplayImage = self.currentCameraImage
            if self.controller is not None:
                self.controller.loop()
            if self.currentDisplayImage is not None:
                controlserver.updateVideoFeedImage(self.currentDisplayImage)
        return None
        
    def turnOff(self):
        if self.running:
            print('Shutting Robot Down')
            self.running = False
            self.loopThread.join()
            self.drivetrain.stop()

    def setController(self, controller):
        isrunning = self.running 
        # if the robot is running, it must be temporarily turned off to switch controllers
        if isrunning:
            self.turnOff()
        self.controller = controller
        print('Switching controller to ', str(type(controller)))
        if isrunning:
            self.turnOn()

    
