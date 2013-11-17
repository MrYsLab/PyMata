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
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


This file demonstrates how to use some of the basic PyMata operations

"""

# import the API class
import time

from pymata import PyMata


# Define some devices and their pin numbers and desired mode

RED_LED = 11 #  a digital output to control an LED
WHITE_LED = 6 # a PWM output to control LED
BUTTON_SWITCH = 12 # a digital input to read a push button switch
POTENTIOMETER = 2 # this A2, an analog input
BEEPER = 3 # A digital output connected to a piezo device
SERVO_MOTOR = 5


# Create an instance of PyMata.

# The PyMata constructor will print status to the console and will return
# when PyMata is ready to accept commands or will exit if unsuccessful
firmata = PyMata("/dev/ttyACM0")

# Retrieve and print Arduino Firmware version information

firmata.refresh_report_firmware()

print firmata.get_firmata_firmware_version()


# Set the pin mode for a digital output pin
firmata.set_pin_mode(RED_LED, firmata.OUTPUT, firmata.DIGITAL)

# Turn on the RED LED
firmata.digital_write(RED_LED, 1)

# Wait 3 seconds and turn it off
time.sleep(3)
firmata.digital_write(RED_LED, 0)

# Set the white led for pwm operation
firmata.set_pin_mode(WHITE_LED, firmata.PWM, firmata.DIGITAL)

# Set the white led to full brightness (255) for 1 second
firmata.analog_write(WHITE_LED, 255)
time.sleep(1)

# now set it to half brightness for 1 second
firmata.analog_write(WHITE_LED, 128)
time.sleep(1)

# and finally extinguish it
firmata.analog_write(WHITE_LED, 0)

# set potentiometer pin as an analog input
firmata.set_pin_mode(POTENTIOMETER, firmata.INPUT, firmata.ANALOG)

# allow some time for the first data to arrive from the Arduino and be
# processed.
time.sleep(.2)
print firmata.analog_read(POTENTIOMETER)

# set the button switch as a digital input
firmata.set_pin_mode(BUTTON_SWITCH, firmata.INPUT, firmata.DIGITAL)

# wait for the button switch to be pressed

while not firmata.digital_read(BUTTON_SWITCH):
    time.sleep(.1)
    pass
print firmata.digital_read(BUTTON_SWITCH)

# send out a beep in celebration of detecting the button press
# note that you don't need to set pin mode for play_tone
firmata.play_tone(BEEPER, firmata.TONE_TONE, 1000, 500)

# control the servo - note that you don't need to set pin mode
# configure the servo
firmata.servo_config(SERVO_MOTOR)

# move the servo to 20 degrees
firmata.analog_write(SERVO_MOTOR, 20)
time.sleep(.5)

# move the servo to 100 degrees
firmata.analog_write(SERVO_MOTOR, 100)
time.sleep(.5)

# move the servo to 20 degrees
firmata.analog_write(SERVO_MOTOR, 20)

# close the interface down cleanly
firmata.close()

