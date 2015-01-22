__author__ = 'Copyright (c) 2013 Alan Yorinks All rights reserved.'

"""
Copyright (c) 2013 Alan Yorinks All rights reserved.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU  General Public
License as published by the Free Software Foundation; either
version 3 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 General Public License for more details.

You should have received a copy of the GNU  General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


This file demonstrates using PyMata to read temperature values from a SparkFun Digital Temperature Sensor
Breakout for the TMP102 device - SparkFun part #SEN-11931

The code is based on a bildr article: http://bildr.org/2011/01/tmp102-arduino/
"""

# import the API class
import time
import sys
import signal

from PyMata.pymata import PyMata


def temp_callback(data):
    # do some calculations on the raw data returned
    temperature_sum = (data[2][1] << 8 | data[2][2]) >> 4

    celsius = temperature_sum * 0.0625
    print(celsius)

    fahrenheit = (1.8 * celsius) + 32
    print(fahrenheit)

# create a PyMata instance
board = PyMata("/dev/ttyACM0")


def signal_handler(sig, frame):
    print('You pressed Ctrl+C!!!!')
    if board is not None:
        board.reset()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# configure firmata for i2c on an UNO
board.i2c_config(0, board.ANALOG, 4, 5)

# configure the I2C pins. This code is for the Leonardo
#board.i2c_config(0, board.DIGITAL, 3, 2)

# read i2c device at address 0x48, with no register specified. Expect 2 bytes to be returned
# and the operation is a single shot read
board.i2c_read(0x48, 0, 2, board.I2C_READ, temp_callback)

# give the serial interface time to send a read, for the device to execute the read
# and to get things back across the interface
time.sleep(2)

board.close()
