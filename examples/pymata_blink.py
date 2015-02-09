#!/usr/bin/python

__author__ = 'Copyright (c) 2013 Alan Yorinks All rights reserved.'

"""
Copyright (c) 2013 Alan Yorinks All rights reserved.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU  General Public
License as published by the Free Software Foundation; either
version 3 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


This file demonstrates how to use some of the basic PyMata operations
"""

import time
import sys
import signal

from PyMata.pymata import PyMata

# digital pin 13 is connected to an LED
BOARD_LED = 13

# create a PyMata instance
firmata = PyMata("/dev/ttyACM0")


def signal_handler(sig, frame):
    print('You pressed Ctrl+C!!!!')
    if firmata is not None:
        firmata.reset()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

# set digital pin 13 to be an output port
firmata.set_pin_mode(BOARD_LED, firmata.OUTPUT, firmata.DIGITAL)

time.sleep(5)
print("Blinking LED on pin 13")

#  blink for 10 times
for x in range(10):
    print(x + 1)
    firmata.digital_write(BOARD_LED, 1)
    #  wait a half second between toggles.
    time.sleep(.5)
    firmata.digital_write(BOARD_LED, 0)
    time.sleep(.5)

# close PyMata when we are done
firmata.close()
