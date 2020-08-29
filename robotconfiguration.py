from gpiozero import Motor
from hardware.motor import MotorGroup
from hardware.drivetrain import DriveTrain

# configuration for the drivetrain
frontLeftMotor = Motor(19, 13) # purple wires
frontRightMotor = Motor(5, 6) # orange wires
backLeftMotor = Motor(25, 16) # green wires
backRightMotor = Motor(23, 24) # blue wires

leftMotorGroup = MotorGroup(frontLeftMotor, backLeftMotor)
rightMotorGroup = MotorGroup(frontRightMotor, backRightMotor)
drivetrain = DriveTrain(leftMotorGroup, rightMotorGroup)

#configuration for the camera
cameraresolution = (320, 240)
cameraframerate = 30

# configuration for server
serverport = 80
snapshotsfolder = "SavedSnapshots"

# configuration for line detection thresholds (line following robot)
lineHueThreshold = (98 , 117) # (min, max) hue
lineSatThreshold = (151, 255) # (min, max) saturation
lineValThreshold = (0  , 255) # (min, max) value or luminance
