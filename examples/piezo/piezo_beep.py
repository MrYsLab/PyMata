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



This is a demonstration of playing a tone on a piezo device.

FirmataPlus is required to be loaded on the Arduino for this to work
"""

import time
import sys
import signal

from PyMata.pymata import PyMata


BEEPER = 3  # pin that piezo device is attached to

# create a PyMata instance
board = PyMata("/dev/ttyACM0")


def signal_handler(sig, frm):
    print('You pressed Ctrl+C!!!!')
    if board is not None:
        board.reset()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

board.play_tone(BEEPER, board.TONE_TONE, 1000, 500)
time.sleep(2)

# play a continuous tone, wait 3 seconds and then turn tone off
board.play_tone(BEEPER, board.TONE_TONE, 1000, 0)
time.sleep(3)
board.play_tone(BEEPER, board.TONE_NO_TONE, 1000, 0)

board.close()


