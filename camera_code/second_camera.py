import RPi.GPIO as GPIO
import os
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
camera_pins=[4,17,18]
for i in range(3):
    GPIO.setup(camera_pins[i],GPIO.OUT)
filepath="/home/pi/Test_Timestamp_Photos/"
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
    
take_picture_cameras(filepath)