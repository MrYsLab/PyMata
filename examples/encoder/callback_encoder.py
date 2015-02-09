#!/usr/bin/env python

__author__ = 'Copyright (c) 2015 Alan Yorinks All rights reserved.'

"""
Copyright (c) 2015 Alan Yorinks All rights reserved.

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

"""

"""
This demo illustrates retrieving data from an encoder using a callback
It will only work on an Arduino Uno and requires the PyMataPlus sketch to be installed on the Arduino
"""

import time
import signal
import sys

from PyMata.pymata import PyMata


# encoder pins
ENCODER_A = 14
ENCODER_B = 15

# Indices into callback return data list
DEVICE = 0
PIN = 1
DATA = 2


def encoder_callback(data):
    print("Data = %d" % data[DATA])

# create a PyMata instance
board = PyMata("/dev/ttyACM0")


def signal_handler(sig, frame):
    print('You pressed Ctrl+C!!!!')
    if board is not None:
        board.reset()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

# configure the pins for the encoder
board.encoder_config(ENCODER_B, ENCODER_A, encoder_callback)

while 1:
    time.sleep(.2)
