#!/usr/bin/python
#import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_Stepper
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor

import time
import atexit
import RPi.GPIO as GPIO
import time

GPIOPIN=17

GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIOPIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def detect():
    if GPIO.input(GPIOPIN) == True:
        return(1)
    else:
        return(0)
try:
    while 1:
        while detect()==0:
            
            if detect()==1:
                print("HIT")
                while detect()==1:
                    pass
except KeyboardInterrupt:
    print("\nKeyboard interrupt, Cleaning up GPIO")
    GPIO.cleanup()

#!/usr/bin/python

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr = 0x60)

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

myStepper = mh.getStepper(200, 1)  # 200 steps/rev, motor port #1
myStepper.setSpeed(1)             # 30 RPM

def check_uncertainty(number_revs,iterations):
    rev = 1600*number_revs
    for j in range(0,iterations,1):
        for i in range(0,rev,1): #runs motor for roughly one full revolution
            myStepper.oneStep(Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.MICROSTEP)
        for k in range(0,rev,1):
            myStepper.oneStep(Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.MICROSTEP)
        print("Iteration " + str(j+1))
    print("Done, Check against starting reference!")
    return
def move_motor_endstop(direction):
    if direction=="left":
        while detect()==0:
            myStepper.oneStep(Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.MICROSTEP)
    elif direction=="right":
        while detect()==0:
            myStepper.oneStep(Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.MICROSTEP)
    else:
        print("at endstop")
    return
move_motor_endstop("left")
        
