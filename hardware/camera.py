import numpy as np
from robotconfiguration import cameraresolution, cameraframerate
camera = None

def initCamera(): # camera can only be initialized on raspberry pi 
    from picamera import PiCamera
    global camera
    camera = PiCamera()
    camera.resolution = cameraresolution
    camera.framerate = cameraframerate

def getCamera():
    if camera is None or camera.closed:
        initCamera()
    return camera

def closeCamera():
    if camera is not None or not camera.closed:
        camera.close()

def grabOpenCVImage(camera):
    """ grabs opencv compatible image given the camera"""
    imageWidth, imageHeight = camera.resolution
    image = np.empty((imageHeight, imageWidth, 3), dtype=np.uint8)
    frame = camera.capture(image, 'bgr', use_video_port = True)
    return image



