import RPi.GPIO as gp
import os

gp.setwarnings(False)
gp.setmode(gp.BOARD)

gp.setup(7, gp.OUT)
gp.setup(11, gp.OUT)
gp.setup(12, gp.OUT)

gp.output(7,False)
gp.output(11,False)
gp.output(12,True)

cmd="raspistill -o capture_First.jpg"
os.system(cmd)
