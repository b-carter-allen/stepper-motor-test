import math
import datetime, time
import objects as ob
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor
import RPi.GPIO as GPIO

## Variables ##


## System Setup ##
endstop_pins=[5,6,13,19,26,20]
camera_pins=[4,17,18]
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
for i in range(3):
    GPIO.setup(camera_pins[i],GPIO.OUT)

for i in range(6):
    GPIO.setup(endstop_pins[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr = 0x60)
LinearMotor = mh.getStepper(200, 1)
LinearMotor.setSpeed(5)
RotaryMotor = mh.getStepper(200,2)
RotaryMotor.setSpeed(5)


## Temp Test Functions ##

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)
#def detect(endstop)
def detect(endstop): # Returns boolean value for whether a specific GPIO pin is obstructed
    if GPIO.input(endstop) == True:
        return(1)
    else:
        return(0)
#Function that moves the endstop right to endstop_number (1-6)
def move_linear_platform(endstop_number): 
    endstop=endstop_pins[endstop_number - 1]
    if detect(endstop_pins[5])== 1:
        turnOffMotors()
    while detect(endstop)== 0:
        LinearMotor.oneStep(Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.MICROSTEP)
    while detect(endstop)== 1:
        LinearMotor.oneStep(Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.MICROSTEP)
    turnOffMotors()
    print ("Platform Centered")

def reset_linear_platform():
    endstop_pins=[17,27,22,18,23,24]
    GPIO.setmode(GPIO.BCM)
    for i in range(6):
        GPIO.setup(endstop_pins[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
    endstop=endstop_pins[endstop_number - 1]
    if detect(endstop_pins[0])== True:
        turnOffMotors()
    while detect(endstop_pins[0])==False:
        LinearMotor.oneStep(Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.MICROSTEP)
    while detect(endstop_pins[0])==True:
        LinearMotor.oneStep(Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.MICROSTEP)
    turnOffMotors()
    print ("linear platform reset")

#takes a picture with Camera 1 and stores
#the .jpg in "file" (path), then takes a picture with Camera 2
#and does the same
def take_picture_cameras(file):
    GPIO.output(camera_pins[0],False)
    GPIO.output(camera_pins[1],False)
    GPIO.output(camera_pins[2],True)
    timestr1 = time.strftime("C1_D%Y_%m_%d-T%H_%M_%S")
    #make_dir=time.strftime("Camera1_D_%Y_%m_%d_T_%H_%M")
    capture1="raspistill -o %s.jpg" % (file+timestr1)
    os.system(capture1)
    print("Camera 1 Capture Succesful")
    GPIO.output(camera_pins[0],True)
    GPIO.output(camera_pins[1],False)
    GPIO.output(camera_pins[2],True)
    timestr2 = time.strftime("C2_D%Y_%m_%d-T%H_%M_%S")
    capture2 = "raspistill -o %s.jpg" % (file+timestr2)
    os.system(capture2)
    print("Camera 2 Capture Successful")

def rotate_vial(interval):
    for i in interval:
        RotaryMotor.oneStep(Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.MICROSTEP)
        print ("vial rotated by", interval)

## ------------------- ##

def input_cmd(): ## returns object with parameters
	n_vials = int(input("Number of Vials (6 or less): "))
	steps = int(input("Number of pictures per vial: "))
	time = float(input("Length of Operation (mins): "))
	n_reps = int(input("Number of repetitions in length of operation: "))

	return ob.Operation_Input(n_vials, steps, time, n_reps)


def operation(input_ob):
	n_vials = input_ob.n_vials
	steps = input_ob.steps
	time = input_ob.time
	n_reps = input_ob.n_reps
	interval = math.floor(200 / steps)
	for i in range(n_vials):
            next_endstop_number=2+i
            for j in range(steps):
                take_picture()
                rotate_vial(interval)
                if i == n_vials-1:
                    reset_linear_platform()
                else:
                    move_linear_platform(next_endstop_number)	
	print ("rep complete")

def main():
	input_ob = input_cmd()
	periodic_scheduler = ob.Periodic_Scheduler(input_ob)
	periodic_scheduler.setup(60.0 * input_ob.time / float(input_ob.n_reps), operation, input_ob)
	periodic_scheduler.run()

if __name__ == '__main__':
	main()