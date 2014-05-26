
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


This file demonstrates using the software data latching features of PyMata
"""



# import the API class
import time

from PyMata.pymata import PyMata

# some constants
POTENTIOMETER = 2  # this A2, an analog input
BUTTON_SWITCH = 12 # a digital input to read a push button switch

# Instantiate PyMata - in this case using the default '/dev/ttyACM0' value.
firmata = PyMata()

# Refresh, Retrieve and print Arduino Firmware version information
firmata.refresh_report_firmware()
print firmata.get_firmata_version()

# Print PyMata's version number
print firmata.get_pymata_version()

# Setup pin A2 for input
firmata.set_pin_mode(POTENTIOMETER, firmata.INPUT, firmata.ANALOG)

# Setup pin pin 12 for the switch
firmata.set_pin_mode(BUTTON_SWITCH, firmata.INPUT, firmata.DIGITAL)

# Arm pin A2 for latching a value >= 678
firmata.set_analog_latch(POTENTIOMETER, firmata.ANALOG_LATCH_GTE, 678)

# Arm pin 12 for latching when the pin goes high
firmata.set_digital_latch(BUTTON_SWITCH, firmata.DIGITAL_LATCH_HIGH)

print "start waiting"
# wait for 5 seconds to allow user interaction with switch and pot
# during this time press and release the switch and turn the pot to maximum

time.sleep(5)

print 'end waiting'
# get and print the digital latched data
print firmata.get_digital_latch_data(BUTTON_SWITCH)

# get and print the analog data latched data
a_latch = firmata.get_analog_latch_data(POTENTIOMETER)
print a_latch
# print gmtime for the time stamp
print time.gmtime(a_latch[firmata.LATCHED_TIME_STAMP])

# wait 2 more seconds and see that the latch entry data is now cleared

time.sleep(2)
print firmata.get_digital_latch_data(BUTTON_SWITCH)
print firmata.get_analog_latch_data(POTENTIOMETER)

firmata.close()