import RPi.GPIO as GPIO
import time

GPIOPIN=4

GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIOPIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def detect():
    if GPIO.input(GPIOPIN) == False:
        return(1)
    else:
        return(0)
try:
    while 1:
            if detect()==1:
                print("HIT")
                while detect()==1:
                    pass
except KeyboardInterrupt:
    print("\nKeyboard interrupt, Cleaning up GPIO")
    GPIO.cleanup()
    
