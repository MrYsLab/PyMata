__author__ = 'afy'
from PyMata.pymata import PyMata
import time

# Create an instance of PyMata.
firmata = PyMata("/dev/ttyACM0")

# configure the stepper # 0  to use pins 9.10,11,12 and specify 512 steps per revolution
firmata.stepper_config(0, 512,  [12, 11, 10, 9])

# allow some time to be able to look at motor
time.sleep(1)

# move motor #0 500 steps forward at a speed of 20
firmata.stepper_step(0, 20, 500)
#print 'forward'

# move motor #0 500 steps reverse at a speed of 20
firmata.stepper_step(0, 20, -500)

# close firmata
firmata.close()

