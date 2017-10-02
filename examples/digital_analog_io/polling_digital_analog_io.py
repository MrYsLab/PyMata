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

This example illustrates using polling for digital input, analog input, and
analog latches.
A switch is used to turn an LED on and off, and a potentiometer sets the
intensity of a second LED.
When the potentiometer exceeds a raw value of 1000, the program is terminated.

There are some major problems with PySerial 2.7 running on Python 3.4.
Polling should only be used with Python 2.7
"""

import sys
import time
import signal

from PyMata.pymata import PyMata

# Digital pins
GREEN_LED = 6
RED_LED = 9
PUSH_BUTTON = 12

# Analog pin
POTENTIOMETER = 2

count = 0

# Create a PyMata instance
board = PyMata("/dev/ttyACM0", verbose=True)


def signal_handler(sig, frame):
    print('You pressed Ctrl+C')
    if board is not None:
        board.reset()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

# Set pin modes
board.set_pin_mode(GREEN_LED, board.OUTPUT, board.DIGITAL)
board.set_pin_mode(RED_LED, board.PWM, board.DIGITAL)
board.set_pin_mode(PUSH_BUTTON, board.INPUT, board.DIGITAL)
board.set_pin_mode(POTENTIOMETER, board.INPUT, board.ANALOG)
board.set_analog_latch(POTENTIOMETER, board.ANALOG_LATCH_GTE, 1000)

# Do nothing loop - program exits when latch data event occurs for
# potentiometer
while 1:
    count += 1
    if count == 300:
        print('Terminated')
        board.close()
    analog = board.analog_read(POTENTIOMETER)
    board.analog_write(RED_LED, analog // 4)

    digital = board.digital_read(PUSH_BUTTON)
    board.digital_write(GREEN_LED, digital)
    latch = board.get_analog_latch_data(POTENTIOMETER)
    if latch[1] == board.LATCH_LATCHED:
        board.analog_write(RED_LED, 0)
        board.digital_write(GREEN_LED, 0)
        print('Latching Event Occurred at: ' + \
              time.asctime(time.gmtime(latch[3])))
        board.close()
        sys.exit(0)
