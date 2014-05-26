__author__ = 'Alan Yorinks'
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

This file was created to work with the Mega 2560. Modify the pin numbers
to use this file with any other Arduino Boards.

This

See the README.md file for instructions on compiling
"""

# import the API class
import time

from PyMata.pymata import PyMata

# instantiate PyMata
firmata = PyMata("/dev/ttyACM0")
time.sleep(2)

# configure a group of pins to control 8 LEDs
firmata.set_pin_mode(46,firmata.OUTPUT,firmata.DIGITAL)
firmata.set_pin_mode(47,firmata.OUTPUT,firmata.DIGITAL)
firmata.set_pin_mode(48,firmata.OUTPUT,firmata.DIGITAL)
firmata.set_pin_mode(49,firmata.OUTPUT,firmata.DIGITAL)
firmata.set_pin_mode(50,firmata.OUTPUT,firmata.DIGITAL)
firmata.set_pin_mode(51,firmata.OUTPUT,firmata.DIGITAL)
firmata.set_pin_mode(52,firmata.OUTPUT,firmata.DIGITAL)
firmata.set_pin_mode(53,firmata.OUTPUT,firmata.DIGITAL)

# configure 4 pins for 4 SONAR modules
firmata.sonar_config(6,6)
time.sleep(.1)
firmata.sonar_config(7,7)
time.sleep(.1)
firmata.sonar_config(37,37)
time.sleep(.1)
firmata.sonar_config(39,39)
time.sleep(1)

# create a forever loop that will sequentially turn on all LEDS,
# then print out the sonar data for the 4 PING devices
# then sequentially turns off all LEDS and print PING data again
print firmata.get_digital_response_table()
while 1:
    for i in range(46,54):
        time.sleep(.1)
        firmata.digital_write(i, 1)
        print firmata.get_sonar_data()

    for i in range(46,54):
        time.sleep(.1)
        firmata.digital_write(i, 0)
        print firmata.get_sonar_data()



