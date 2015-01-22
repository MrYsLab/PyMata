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
This demo polls the current values returned from a rotary encoder.

It will only work on an Arduino Uno and requires the PyMataPlus sketch to be installed on the Arduino
"""

import sys
import signal

from PyMata.pymata import PyMata

ENCODER_A = 14
ENCODER_B = 15
prev_value = 0

# create a PyMata instance
board = PyMata("/dev/ttyACM0")


def signal_handler(sig, frame):
    print('You pressed Ctrl+C!!!!')
    if board is not None:
        board.reset()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# configure the pins for the encoder
board.encoder_config(ENCODER_B, ENCODER_A)

while 1:
    value = board.digital_read(ENCODER_B)
    if value != prev_value:
        prev_value = value
        print(board.digital_read(ENCODER_B))
    pass
