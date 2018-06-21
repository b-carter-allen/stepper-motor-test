#!/usr/bin/python
#import Adafruit_MotorHAT, Adafruit_Stepper
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_StepperMotor

import time
import atexit

mh = Adafruit_MotorHAT(addr = 0x60)

def turnOffMotors():
        mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
        mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
        mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
        mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)
 
#atexit.register(turnOffMotors)

#stepper1 = mh.getStepper(200,1)

#stepper1.oneStep(FORWARD, MICROSTEP)

        
