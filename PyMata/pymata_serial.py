__author__ = 'Copyright (c) 2013 Alan Yorinks All rights reserved.'
"""

@author: Alan Yorinks
Copyright (c) 2013-15 Alan Yorinks All rights reserved.

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

import threading
import time
import sys

import serial


class PyMataSerial(threading.Thread):
    """
     This class manages the serial port for Arduino serial communications
    """

    # class variables
    arduino = serial.Serial()

    port_id = ""
    baud_rate = 57600
    timeout = 1
    command_deque = None

    def __init__(self, port_id, command_deque):
        """
        Constructor:
        @param command_deque: A reference to the deque shared with the _command_handler
        """
        self.port_id = port_id
        self.command_deque = command_deque

        threading.Thread.__init__(self)
        self.daemon = True
        self.arduino = serial.Serial(self.port_id, self.baud_rate,
                                     timeout=int(self.timeout), writeTimeout=0)

        self.stop_event = threading.Event()

        # without this, running python 3.4 is extremely sluggish
        if sys.platform == 'linux':
            # noinspection PyUnresolvedReferences
            self.arduino.nonblocking()

    def stop(self):
        self.stop_event.set()

    def is_stopped(self):
        return self.stop_event.is_set()

    def open(self, verbose):
        """
        open the serial port using the configuration data
        returns a reference to this instance
        """
        # open a serial port
        if verbose:
            print('\nOpening Arduino Serial port %s ' % self.port_id)

        try:

            # in case the port is already open, let's close it and then
            # reopen it
            self.arduino.close()
            time.sleep(1)
            self.arduino.open()
            time.sleep(1)
            return self.arduino

        except Exception:
            # opened failed - will report back to caller
            raise

    def close(self):
        """
            Close the serial port
            return: None
        """
        try:
            self.arduino.close()
        except OSError:
            pass

    def write(self, data):
        """
            write the data to the serial port
            return: None
        """
        if sys.version_info[0] < 3:
            self.arduino.write(data)
        else:
            self.arduino.write(bytes([ord(data)]))

    # noinspection PyExceptClausesOrder
    def run(self):
        """
        This method continually runs. If an incoming character is available on the serial port
        it is read and placed on the _command_deque
        @return: Never Returns
        """
        while not self.is_stopped():
            # we can get an OSError: [Errno9] Bad file descriptor when shutting down
            # just ignore it
            try:
                if self.arduino.inWaiting():
                    c = self.arduino.read()
                    self.command_deque.append(ord(c))
            except OSError:
                pass
            except IOError:
                self.stop()
        self.close()











