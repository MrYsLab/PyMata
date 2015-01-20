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


"""

# import the API class
import time

from PyMata.pymata import PyMata

# ping callback function
def cb_ping(data):
    print(str(data[2]) + ' centimeters')

# instantiate PyMata
firmata = PyMata("/dev/ttyACM0")

# configure 4 pins for 4 SONAR modules
firmata.sonar_config(12,12, cb_ping)

time.sleep(10)
firmata.close()




