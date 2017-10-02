#!/usr/bin/env python
"""
 Copyright (c) 2015-2017 Alan Yorinks All rights reserved.

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU AFFERO GENERAL PUBLIC LICENSE
 Version 3 as published by the Free Software Foundation; either
 or (at your option) any later version.
 This library is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 General Public License for more details.

 You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
 along with this library; if not, write to the Free Software
 Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA



"""
import time
import sys
import signal

from PyMata.pymata import PyMata

# create a PyMata instance
board = PyMata("/dev/ttyACM0", verbose=True)


# you may need to press ctrl c twice
def signal_handler(sig, frame):
    print('You pressed Ctrl+C')
    if board is not None:
        board.reset()
        board.close()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

# Configure the trigger and echo pins
board.sonar_config(12, 12)

time.sleep(1)

# Create a forever loop that will print out the sonar data for the PING device

while 1:
    data = board.get_sonar_data()
    print(str(data[2]) + ' centimeters')
    time.sleep(.2)
