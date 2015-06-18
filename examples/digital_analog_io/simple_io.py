#!/usr/bin/env python
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


This example illustrates using callbacks for digital and analog input.

Monitor the current analog input and digital input of two pins.
"""

import signal
import sys

from PyMata.pymata import PyMata

# Pin definitions

# Digital Input Pin - D12
PUSH_BUTTON = 12

# Analog Input Pin - A0
POTENTIOMETER = 0

# Indices for data passed to callback function
PIN_MODE = 0  # This is the PyMata Pin MODE = ANALOG = 2 and DIGITAL = 0x20:
PIN_NUMBER = 1
DATA_VALUE = 2

# Control-C signal handler to suppress exceptions if user presses Crtl+C
def signal_handler(sig, frame):
    print('You pressed Ctrl+C')
    if board is not None:
        board.reset()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Data change callback functions
def cb_potentiometer(data):
    print("Analog Data: ",
          " Pin: ", data[PIN_NUMBER],
          " Pin Mode: ", data[PIN_MODE],
          " Data Value: ", data[DATA_VALUE])

def cb_push_button(data):
    print("Digital Data:",
          " Pin: ", data[PIN_NUMBER],
          " Pin Mode: ", data[PIN_MODE],
          " Data Value: ", data[DATA_VALUE])

# Instantiate PyMata
board = PyMata("/dev/ttyACM0", verbose=True)

# Set up pin modes for both pins with callbacks for each
board.set_pin_mode(PUSH_BUTTON, board.INPUT, board.DIGITAL, cb_push_button)
board.set_pin_mode(POTENTIOMETER, board.INPUT, board.ANALOG,
                   cb_potentiometer)

# A forever loop until user presses Ctrl+C
while 1:
    pass
