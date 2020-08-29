# RPiRobot
 
Code for a small remote-controlled 4 wheel robot built using the raspberry pi. This was made as a fun hobby project.  

##### Hardware
The hardware of the robot consists of a raspberry pi with a camera module, 4 DC motors with wheels, 2 motor controller boards (which can control 2 motors each) and a breadboard. A 9 volt battery powers the motors and a portable phone charger powers the pi. The robot is differential wheeled, so to turn the robot, the wheels on the left and right sides are rotated at different speeds. 

##### Remote Control via a Webserver
The robot runs a webserver that is used to control it. The webserver can be accessed in a browser from the ip address of the raspberry pi. The webserver displays the robot's camera feed and allows the robot to be controlled via arrow keys. The webserver also has some other features such as the ability to save snapshots of the camera feed to the raspberry pi. 

##### Line Following
The robot also has the ability to autonomously follow a path that is laid out by a line. The robot uses OpenCV methods to process camera images in order to detect the line and uses proportional control along with other other techniques to follow the line.







