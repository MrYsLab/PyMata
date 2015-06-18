#!/usr/bin/python
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

You should have received a copy of the GNU General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


This file demonstrates how to retrieve capability and configuration data.

The servo_config is set to illustrate the digital_response_table being marked
a servo device. Pin 12 is set to digital output and pin A0 is set to analog
imput.

Your output should like this:

PyMata Digital Response Table
[[0, 0, None], [0, 0, None], [0, 0, None], [0, 0, None], [0, 0, None],
 [4, 0, None], [0, 0, None], [0, 0, None], [0, 0, None], [0, 0, None],
 [0, 0, None], [0, 0, None], [1, 0, None], [0, 0, None], [0, 0, None],
 [0, 0, None], [0, 0, None], [0, 0, None], [0, 0, None], [0, 0, None]]
PyMata Analog Response Table
[[0, 216, None], [0, 0, None], [0, 0, None], [0, 0, None], [0, 0, None],
 [0, 0, None]]

"""

import time
import sys
import signal

from PyMata.pymata import PyMata

def signal_handler(sig, frame):
    print('You pressed Ctrl+C')
    if board is not None:
        board.reset()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Create a PyMata instance
board = PyMata("/dev/ttyACM0")

# Set the pin mode
board.servo_config(5)
board.set_pin_mode(12, board.OUTPUT, board.DIGITAL)
board.set_pin_mode(0, board.INPUT, board.ANALOG)

# Send query request to Arduino
board.capability_query()

# Some boards take a long time to respond - adjust as needed
time.sleep(5)
print("Pin Capability Report")
print(board.get_capability_query_results())

print("PyMata Digital Response Table")
print(board.get_digital_response_table())

print("PyMata Analog Response Table")
print(board.get_analog_response_table())

