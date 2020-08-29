from flask import Flask, render_template, Response, send_file, make_response
from flask_socketio import SocketIO
import cv2
import os
import datetime

from robotconfiguration import serverport, snapshotsfolder
import hardware.robot as robot
from autonomy.controllers.linefollowing import LineFollowing
from autonomy.controllers.randomlymoving import RandomlyMoving

app = Flask(__name__)
socketio = SocketIO(app)

# for the video feed
currentImage = None
currentImageBytes = None
imageSize = (576, 432)
noVideoFeedImage = cv2.imread('server/static/images/nofeedimage.png')

def startServer():
    print('Starting Flask Webserver')
    socketio.run(app, host='0.0.0.0', port=serverport, debug=False)

@app.route('/')
def robot_template():   
    if robot.Robot.getInstance().controller is None:
        return render_template('index.html')
    
@app.route('/video_feed')
def video_feed():
    return Response(genVideoFeed(), mimetype='multipart/x-mixed-replace; boundary=frame')

# message handling
@socketio.on('message')
def handle_message(message):
    print('Received message from client: ' + message)

@socketio.on('turn on')
def handle_turn_on():
    print('Received TURN ON command from client')
    robot.Robot.getInstance().turnOn()

@socketio.on('turn off')
def handle_turn_off():
    global currentImage
    print('Received TURN OFF command from client')
    robot.Robot.getInstance().turnOff()
    currentImage = None

@socketio.on('set left right speeds')
def handle_set_left_right_speeds(left, right):
    print('Received speeds from client:', 'left:', round(left, 3), 'right:',  round(right, 3))
    if robot.Robot.getInstance().running:
        robot.Robot.getInstance().drivetrain.setMotorSpeeds(left, right)
    else:
        print('Robot off, ignoring set speeds')

@socketio.on('set forward turn speeds')
def handle_set_forward_turn_speeds(forward, turn):
    print('Received speeds from client:', 'forward:', round(forward, 3), 'turn:', round(turn, 3))
    if robot.Robot.getInstance().running:
        robot.Robot.getInstance().drivetrain.setForwardAndTurnSpeed(forward, turn)
    else:
        print('Robot off, ignoring set speeds')

@socketio.on('save snapshot')
def handle_save_snapshot():
    print('Recieved save snapshot command from client')
    now = datetime.datetime.now()
    timestamp = now.strftime('%Y-%m-%d__%H_%M_%S')
    extension = '.jpeg'
    path = os.path.join(snapshotsfolder, timestamp + extension)
    cv2.imwrite(path, currentImage)

@socketio.on('set control mode')
def handle_set_control_mode(controlmode):
    print('Received set control mode command from client:', controlmode)
    controller = None
    if controlmode == "Keyboard Control":
        controller = None
    elif controlmode == "Line Following":
        controller = LineFollowing()
    elif controlmode == "Randomly Moving":
        controller = RandomlyMoving()
    robot.Robot.getInstance().setController(controller)

def updateVideoFeedImage(image):
    global currentImage
    global currentImageBytes
    currentImage = cv2.resize(image, imageSize)
    currentImageBytes = cv2.imencode('.JPEG', currentImage)[1].tostring()
    
def genVideoFeed():
    while True:
        if currentImage is None or currentImageBytes is None:
            updateVideoFeedImage(noVideoFeedImage)
        yield (b'--frame\r\n'
             b'Content-Type: image/jpeg\r\n\r\n' + currentImageBytes + b'\r\n') 


