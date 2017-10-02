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


# Ping callback function
def cb_ping(data):
    print(str(data[2]) + ' centimeters')


# Create a PyMata instance
board = PyMata("/dev/ttyACM0", verbose=True)


# you may need to press control-c twice to exit
def signal_handler(sig, frame):
    print('You pressed Ctrl+C!!!!')
    if board is not None:
        board.reset()
        board.close()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

# Configure Trigger and Echo pins
# Using default of 50 ms ping interval and max distance of 200 cm.
board.sonar_config(12, 12, cb_ping)

# Example of changing ping interval to 100, and max distance to 150
# board.sonar_config(12, 12, cb_ping, 100, 150)

time.sleep(10)
board.close()
