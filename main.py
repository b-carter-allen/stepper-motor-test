import math
import datetime, time
import objects as ob
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor
import RPi.GPIO as GPIO

## Variables ##


## System Setup ##
endstop_pins=[17,27,22,18,23,24]
GPIO.setmode(GPIO.BCM)
for i in range(6):
    GPIO.setup(endstop_pins[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr = 0x60)
LinearMotor = mh.getStepper(200, 1)
LinearMotor.setSpeed(3)
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
        return(True)
    else:
        return(False)
#Define a function that moves the endstop right to the next endstop
def move_linear_platform(endstop_number):
    endstop_pins=[17,27,22,18,23,24]
    GPIO.setmode(GPIO.BCM)
    for i in range(6):
        GPIO.setup(endstop_pins[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
    endstop=endstop_pins[endstop_number - 1]
    if detect(endstop_pins[0])== True:
        turnOffMotors()
    while detect(endstop)== False:
        LinearMotor.oneStep(Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.MICROSTEP)
    while detect(endstop)== True:
        LinearMotor.oneStep(Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.MICROSTEP)
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

def take_picture():
	print ("pictures taken")
	# print ("pictures stored")

def rotate_vial(interval):
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