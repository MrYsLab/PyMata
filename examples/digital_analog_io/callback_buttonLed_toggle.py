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
This example illustrates using callbacks to toggle an LED. Each time the button switch is pressed the LED
state will toggle to the opposite state. The latch is rearmed within the callback routing


"""

import time
import signal
import sys

from PyMata.pymata import PyMata
#import PyMata from PyMata.pymata


# digital pins
GREEN_LED = 6
PUSH_BUTTON = 12

# switch states
ON = 1
OFF = 0

led_state = OFF

def get_led_state():
    global led_state
    return led_state

def set_led_state(state):
    global led_state
    led_state = state

# callback functions
# set the LED to current state of the pushbutton switch
def cb_push_button(data):
    print(data)
    if get_led_state() == OFF:
        board.digital_write(GREEN_LED, ON)
        set_led_state(ON)
    else:
        board.digital_write(GREEN_LED, OFF)
        set_led_state(OFF)

    # re-arm the latch to fire on the next transition to high
    board.set_digital_latch(PUSH_BUTTON, board.DIGITAL_LATCH_HIGH, cb_push_button)



def signal_handler(sig, frame):
    print('You pressed Ctrl+C!!!!')
    if board is not None:
        board.reset()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

# create a PyMata instance
board = PyMata("/dev/ttyACM0")


# set pin modes
# set the pin to light the green led
board.set_pin_mode(GREEN_LED, board.OUTPUT, board.DIGITAL)

# set the pin to receive button presses
board.set_pin_mode(PUSH_BUTTON, board.INPUT, board.DIGITAL)

# arm the digital latch to detect when the button is pressed
board.set_digital_latch(PUSH_BUTTON, board.DIGITAL_LATCH_HIGH, cb_push_button)

while 1:
    pass
