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
This example illustrates using callbacks for digital input, analog input and analog latches, in addition
to demonstrating both writing to an LED using PWM and with digital outputs.

A switch is used to turn an LED on and off, and a potentiometer sets the intensity of a second LED.
When the potentiometer exceeds a raw value of 1000, the program is terminated.
"""

import time

from PyMata.pymata import PyMata


# digital pins
GREEN_LED = 6
RED_LED = 9
PUSH_BUTTON = 12

# analog pin
POTENTIOMETER = 2

# index to retrieve data from an analog or digital callback list
DATA_VALUE = 2

# switch states
ON = 1
OFF = 0

# indices for data list passed to latch callback
LATCH_TYPE = 0
LATCH_PIN = 1
LATCH_DATA_VALUE = 2
LATCH_TIME_STAMP = 3


# callback functions
# set the LED to current state of the pushbutton switch
def cb_push_button(data):
    board.digital_write(GREEN_LED, data[DATA_VALUE])


# maximum value of pot is 1024, and the maximum output value for pwm is 255
# so we divide the current pot value by 4 to keep it in pwm range
def cb_potentiometer(data):
    board.analog_write(RED_LED, data[DATA_VALUE] // 4)


def cb_potentiometer_latch(data):
    # turn off LEDs
    board.analog_write(RED_LED, 0)
    board.digital_write(GREEN_LED, 0)

    # print all data from the latch callback including time stamp
    print('Latching Event Mode:%x  Pin:%d  Data Value:%d Time of Event:%s' % (data[LATCH_TYPE], data[LATCH_PIN],
                                                                              data[LATCH_DATA_VALUE], time.asctime(
        time.gmtime(data[LATCH_TIME_STAMP]))))
    # shut things down
    board.close()

# create a PyMata instance
board = PyMata("/dev/ttyACM0")


# set pin modes
board.set_pin_mode(GREEN_LED, board.OUTPUT, board.DIGITAL)
board.set_pin_mode(RED_LED, board.PWM, board.DIGITAL)
board.set_pin_mode(PUSH_BUTTON, board.INPUT, board.DIGITAL, cb_push_button)
board.set_pin_mode(POTENTIOMETER, board.INPUT, board.ANALOG, cb_potentiometer)

# set the latch
board.set_analog_latch(POTENTIOMETER, board.ANALOG_LATCH_GTE, 1000, cb_potentiometer_latch)

# do nothing loop - program exits when latch data event occurs for potentiometer or timer expires
time.sleep(15)
print('Timer expired')
board.close()
