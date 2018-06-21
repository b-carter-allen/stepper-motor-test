import math
import datetime, time
import objects as ob
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor
import RPi.GPIO as GPIO
import os

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
LinearMotor.setSpeed(30)
RotaryMotor = mh.getStepper(200,2)
RotaryMotor.setSpeed(2)


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
        LinearMotor.oneStep(Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.INTERLEAVE)
    while detect(endstop)== 1:
        LinearMotor.oneStep(Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.INTERLEAVE)
    turnOffMotors()
    print ("Platform Centered")

def reset_linear_platform():
    if detect(endstop_pins[0])== 1:
        print("At endstop 1")
        turnOffMotors()
    while detect(endstop_pins[0])==0:
        LinearMotor.oneStep(Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.INTERLEAVE)
    while detect(endstop_pins[0])==1:
        LinearMotor.oneStep(Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.INTERLEAVE)
    turnOffMotors()
    print ("linear platform reset")

#takes a picture with Camera 1 and stores
#the .jpg in "file" (path), then takes a picture with Camera 2
#and does the same
def take_picture_cameras(file):
    GPIO.output(camera_pins[0],False)
    GPIO.output(camera_pins[1],False)
    GPIO.output(camera_pins[2],True)
    timestr1 = time.strftime("/C1_D%Y_%m_%d-T%H_%M_%S")
    #make_dir=time.strftime("Camera1_D_%Y_%m_%d_T_%H_%M")
    capture1="raspistill -t 500 -st -o %s.jpg" % (file+timestr1)
    os.system(capture1)
    print("Camera 1 Capture Succesful")
    GPIO.output(camera_pins[0],True)
    GPIO.output(camera_pins[1],False)
    GPIO.output(camera_pins[2],True)
    timestr2 = time.strftime("/C2_D%Y_%m_%d-T%H_%M_%S")
    capture2 = "raspistill -t 500 -st -o %s.jpg" % (file+timestr2)
    os.system(capture2)
    print("Camera 2 Capture Successful")

def rotate_steps(n_steps):
    for i in range(int(n_steps)):
        RotaryMotor.oneStep(Adafruit_MotorHAT.FORWARD,Adafruit_MotorHAT.MICROSTEP)

def rotate_vial(interval):
    rotate_steps(interval)
    turnOffMotors()
    print ("vial rotated by", interval)

def rotate_reset():
    for i in range(int(1600)):
        RotaryMotor.oneStep(Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.MICROSTEP)
    print("Vial Rotated to Reset")

## ------------------- ##

def input_cmd(): ## returns object with parameters
    n_vials = int(input("Number of Vials (6 or less): "))
    steps = int(input("Number of pictures per vial: "))
    time = float(input("Length of Operation (mins): "))
    n_reps = int(input("Number of repetitions in length of operation: "))
    store_path = str(raw_input("Path (folder in home dir): "))

    return ob.Operation_Input(n_vials, steps, time, n_reps, store_path)

def root_file_gen(newpath):
    root_folder = time.strftime("Run_%Y_%m_%d-%H:%M")
    newpath = os.path.join(os.path.expanduser('~'), newpath, root_folder)
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    return (newpath)

def vial_file_gen(rootpath, n_vial):
    vial_folder = ("Vial_" + str(n_vial))
    rootpath = os.path.join(rootpath, vial_folder)
    if not os.path.exists(rootpath):
        os.makedirs(rootpath)

    return (rootpath)

def run_file_gen(vialpath, n_run):
    run_folder = ("Time_" + str(n_run))
    vialpath = os.path.join(vialpath, run_folder)
    if not os.path.exists(vialpath):
        os.makedirs(vialpath)
    
    return (vialpath)


def operation(input_ob):
	n_vials = input_ob.n_vials
	steps = input_ob.steps
	time = input_ob.time
	n_reps = input_ob.n_reps
        rootpath = root_file_gen(input_ob.store_path)
	interval = math.floor(1600 / steps)
	remainder = 1600 - (steps * interval)
	reset_linear_platform()
	for i in range(n_vials):
            vialpath = vial_file_gen(rootpath, n_vials + 1)    
            next_endstop_number=2+i
            for j in range(steps):
                runpath = run_file_gen(vialpath, steps + 1)
                take_picture_cameras(runpath)
                rotate_vial(interval)
            if i == n_vials-1:
                reset_linear_platform()
            else:
                move_linear_platform(next_endstop_number)
            for k in range(int(remainder)):
                RotaryMotor.oneStep(Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.MICROSTEP)
            rotate_reset()
	print ("rep complete")

def main():
    input_ob = input_cmd()
    periodic_scheduler = ob.Periodic_Scheduler(input_ob)
    periodic_scheduler.setup(60.0 * input_ob.time / float(input_ob.n_reps), operation, input_ob)
    periodic_scheduler.run()

if __name__ == '__main__':
    main()