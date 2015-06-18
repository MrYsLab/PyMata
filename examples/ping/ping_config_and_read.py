#!/usr/bin/env python
"""
Copyright (c) 2013-2015 Alan Yorinks All rights reserved.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU  General Public
License as published by the Free Software Foundation; either
version 3 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 General Public License for more details.

You should have received a copy of the GNU  General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""
import time
import sys
import signal

from PyMata.pymata import PyMata

firmata = None

# create a PyMata instance
board = PyMata("/dev/ttyACM0", verbose=True)

def signal_handler(sig, frame):
    print('You pressed Ctrl+C')
    if firmata is not None:
        firmata.reset()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Configure 4 pins for 4 SONAR modules
firmata.sonar_config(12, 12)

time.sleep(1)

# Create a forever loop that will sequentially turn on all LEDS,
# then print out the sonar data for the 4 PING devices
# then sequentially turns off all LEDS and print PING data again

while 1:
    data = firmata.get_sonar_data()
    print(str(data[2]) + ' centimeters')
    # firmata.get_sonar_data()
    #print(firmata.get_sonar_data())
    time.sleep(.2)

