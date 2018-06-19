import RPi.GPIO as gp
import os
import time
gp.setwarnings(False)
gp.setmode(gp.BOARD)

gp.setup(7, gp.OUT)
gp.setup(11, gp.OUT)
gp.setup(12, gp.OUT)

gp.output(7,True)
gp.output(11,False)
gp.output(12,True)

timestr = time.strftime("%Y_%m_%d-%H_%M_%S")


set_date_time="""DATE=$(date +"%Y-%m-%d_%H%M")"""
make_dir="""mkdir CameraTimestamptest"""
cmd="raspistill -o %s.jpg" % timestr
for i in range(3):
    timestr = time.strftime("%Y_%m_%d-%H_%M_%S")
    cmd="raspistill -o %s.jpg" % timestr
    os.system(cmd)
