__author__ =  'Copyright (c) 2013 Alan Yorinks All rights reserved.'

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
"""

from  pymata_serial import PyMataSerial
from pymata_command_handler import PyMataCommandHandler
from collections import deque
import threading
import sys
import time

 # A general note: the construct SOMEVALUE & 0x7f, SOMEVALUE >> 7
 # translates an integer into 2 one byte
 # values required by the Firmata protocol

class PyMata:
    """
    This class contains the API for the PyMata library

    This code is designed to be used with StandardFirmata,
    If you require support for CodeShield on an Arduino UNO,
    please use the included custom Arduino sketch called NoSoStandardFirmata.
    """

    # pin modes
    INPUT = 0x00
    OUTPUT = 0x01
    ANALOG = 0x02  # analog pin in analogInput mode
    PWM = 0x03  # digital pin in PWM output mode
    SERVO = 0x04  # digital pin in Servo output mode
    ENCODER = 0x07  # Analog pin output pin in ENCODER mode
    TONE = 0x08  # Any pin in TONE mode
    DIGITAL = 0x20

    HIGH = 1  # digital pin state high value
    LOW = 0  # digital pin state low value

    REPORTING_ENABLE = 1  # enable reporting for REPORT_ANALOG or REPORT_DIGITAL message sent to firmata
    REPORTING_DISABLE = 0  # disable reporting for REPORT_ANALOG or REPORT_DIGITAL message sent to firmata



    # commands and data from firmata are received in this deque and processed in a separate class
    _command_deque = deque()

    # this is the instance reference to the _command_handler
    _command_handler = None

    # this is the instance reference to the communications port object
    _arduino = None

    # communications port id (i.e. COM3 or /dev/ttyACM0
    _port_id = ''

    # this is  a lock to assure data integrity when reading or writing to the data response tables
    # defined in the CommandHandler class
    _data_lock = threading.Lock()

    def __init__(self, port_id = '/dev/ttyACM0', number_digital_pins = 20, number_analog_pins = 6):
        """
        The constructor builds the entire interface, connects to Firmata and awaits user commands
        @param port_id: Communications port specifier (COM3, /dev/ttyACM0, etc)
        @param number_digital_pins: Number of digital pins that the _arduino contains
        @param number_digital_pins: Number of analog pins that the _arduino contains
        @return: This function does not return
        """
        # communications port
        self._port_id = port_id

        # currently only serial communication over USB is supported, but in the future
        # wifi support is anticipated

        # instantiate the serial support class
        self._arduino = PyMataSerial(self._port_id, self._command_deque)

        # attempt opening communications with the Arduino micro-controller
        self._arduino.open()

        #start the data receive thread
        self._arduino.start()

        # instantiate the command handler
        self._command_handler = PyMataCommandHandler(self._arduino, self._command_deque,
                                              self._data_lock, number_digital_pins, number_analog_pins)
        # start its command processing thread
        self._command_handler.start()

    def analog_read(self,pin):
        """
        Read the value for the specified pin.
        @param pin: Selected pin
        @return: The last value entered in the response table if returned.
        """
        self._data_lock.acquire(True)
        data = self._command_handler.analog_response_table[pin][self._command_handler.RESPONSE_TABLE_PIN_DATA_VALUE]
        self._data_lock.release()
        return data

    def analog_write(self, pin, value):
        """
        Set the specified pin to the specified value
        @param pin: Pin number
        @param value: Pin value
        @return: No return value
        """
        command = [self._command_handler.ANALOG_MESSAGE + pin, value & 0x7f, value >> 7]
        self._command_handler.send_command(command)

    def close(self):
        """
        This method will close the transport (serial port) and exit
        @return: No return value.
        """
        self._arduino.close()
        print "PyMata close(): Calling sys.exit(0): Hope to see you soon!"
        sys.exit(0)

    def digital_read(self, pin):
        """
        Read the value for the specified pin.
        NOTE: This command will return values for digital, pwm, and encoder pin types
        @param pin: Selected pin
        @return: The last value entered in the response table if returned.
        """
        self._data_lock.acquire(True)
        data = self._command_handler.digital_response_table[pin][self._command_handler.RESPONSE_TABLE_PIN_DATA_VALUE]
        self._data_lock.release()
        return data

    def digital_write(self, pin, value):
        """
        Set the specified pin to the specified value
        @param pin: pin number
        @param value: pin value
        @return: No return value
        """
        command = []

        port = pin / 8
        calculated_command = self._command_handler.DIGITAL_MESSAGE + port

        # set the pin position in the byte for the pin to write
        if value == 1:
            mask = 1 << (pin % 8)
        else:
            mask = 0

        command.append(calculated_command)
        command.append(mask & 0x7f)
        command.append(mask >> 7)
        self._command_handler.send_command(command)


    def disable_analog_reporting(self, pin):
        """
        Disables analog reporting for a single analog pin.
        @param pin: Analog pin number. For example for A0, the number is 0.
        @return: No return value
        """
        command = [self._command_handler.REPORT_ANALOG + pin, self.REPORTING_DISABLE]
        self._command_handler.send_command(command)

    def disable_digital_reporting(self, pin):
        """
        Disables digital reporting. By turning reporting off for this pin, reporting
        is disabled for all 8 bits in the "port" - this is part of Firmata's design
        @param pin: Pin and all pins for this port
        @return: No return value
        """
        command = []
        port = pin / 8
        command.append(self._command_handler.REPORT_DIGITAL + port)
        command.append(self.REPORTING_DISABLE)
        self._command_handler.send_command(command)

    def enable_analog_reporting(self, pin):
        """
        Enables analog reporting. By turning reporting on for a single pin,
        @param pin: Analog pin number. For example for A0, the number is 0.
        @return: No return value
        """
        command = [self._command_handler.REPORT_ANALOG + pin, self.REPORTING_ENABLE]
        self._command_handler.send_command(command)

    def enable_digital_reporting(self, pin):
        """
        Enables digital reporting. By turning reporting on for a pin, reporting
        is enabled for all 8 bits in the "port" - this is part of Firmata's design
        @param pin: Pin and all pins for this port
        @return: No return value
        """
        command = []

        port = pin / 8
        command.append(self._command_handler.REPORT_DIGITAL + port)
        command.append(self.REPORTING_ENABLE)
        self._command_handler.send_command(command)


    def encoder_config(self, pin_a, pin_b):
        """
        This command enables the rotary encoder (2 pin + ground) and will
        enable encoder reporting.
        It is intended to be used with NotSoStandardFirmata.
        @param pin_a: Encoder pin 1.
        @param pin_b: Encoder pin 2.
        @return: No return value
        """
        data = [pin_a, pin_b]
        self._command_handler.digital_response_table[pin_a][self. _command_handler.RESPONSE_TABLE_MODE] \
            = self._command_handler.ENCODER
        self._command_handler.digital_response_table[pin_b][self. _command_handler.RESPONSE_TABLE_MODE] \
            = self._command_handler.ENCODER
        self._command_handler.send_sysex(self._command_handler.ENCODER_CONFIG, data)

    def get_analog_response_table(self):
        """
        This method returns a list of lists representing the current pin mode and associated data for all
        analog pins.
        All pin types, both input and output will be listed. Output pin data will contain zero.
        @return: The last update of the digital response table
        """
        return self._command_handler.get_analog_response_table()

    def get_digital_response_table(self):
        """
        This method returns a list of lists representing the current pin mode and associated data for all
        digital pins.
        All pin types, both input and output will be listed. Output pin data will contain zero.
        @return: The last update of the digital response table
        """
        return self._command_handler.get_digital_response_table()

    def get_firmata_version(self):
        """
        Get the firmata version information
        NOTE: For Leonardo Boards it will return None
        @return: Firmata_version list [major, minor] or None
         """
        return self._command_handler.firmata_version


    def get_firmata_firmware_version(self):
        """
        Get the firmware id information
        NOTE: For Leonardo Boards it will return None
        @return: Firmata_firmware  list [major, minor, file_name] or None
        """
        return self._command_handler.firmata_firmware

    def is_firmata_ready(self, timeout = 0):
        """
        This method checks to see if Firmata is ready to accept commands
        @param timeout: If zero, will check for version string, else
                        will wait for the timeout in seconds
        @return: True if ready, False if not ready
        """
        if timeout:
            time.sleep(timeout)
        else:
            while len(self.get_firmata_firmware_version()) == 0:
                return False
        return True

    def play_tone(self, pin, frequency, duration):
        """
        This method will call the Tone library for the selected pin.
        It is intended to be used with NotSoStandardFirmata.
        @param pin: Pin number
        @param frequency: Frequency of tone
        @param duration: Duration of tone in milliseconds
        @return: No return value
        """
        # convert the integer values to bytes
        data = [pin, frequency & 0x7f, frequency >> 7, duration & 0x7f, frequency >> 7]

        self._command_handler.digital_response_table[pin][self. _command_handler.RESPONSE_TABLE_MODE] = \
            self._command_handler.TONE
        self._command_handler.send_sysex(self._command_handler.TONE_PLAY, data)

    def reset(self):
        """
        This command sends a reset message to the Arduino. The response tables will be reinitialized
        @return: No return value.
        """

        # set all output pins to a value of 0
        for pin in range(0,self._command_handler.number_digital_pins):
            if self._command_handler.digital_response_table[self._command_handler.RESPONSE_TABLE_MODE] \
                    == self._command_handler.PWM:
                self.analog_write(pin, 0)
            elif self._command_handler.digital_response_table[self._command_handler.RESPONSE_TABLE_MODE] \
                    == self._command_handler.SERVO:
                self.analog_write(pin,0)
            else:
                self.digital_write(pin,0)
        self._command_handler.system_reset()

    def set_pin_mode(self, pin, mode, pin_type):
        """
        This method sets a pin to the desired pin mode for the pin_type.
        It automatically enables data reporting..
        @param pin: Pin number (for analog use the analog number, for example A4: use 4
        @param mode: INPUT, OUTPUT, PWM, SERVO, ENCODER or TONE
        @param pin_type: ANALOG or DIGITAL
        @return: No return value
        """
        command = [self._command_handler.SET_PIN_MODE, pin, mode]
        self._command_handler.send_command(command)
        #enable reporting for input pins
        if mode == self.INPUT:
            command = []
            if pin_type == self.ANALOG:

                # set analog response table to show this pin is an input pin

                self._command_handler.analog_response_table[pin][self. _command_handler.RESPONSE_TABLE_MODE] = self.INPUT
                self.enable_analog_reporting(pin)

                # the pin number is added to the report analog command
                command.append(self._command_handler.REPORT_ANALOG + pin)
                command.append(self.REPORTING_ENABLE)

            # if not analog it has to be digital
            else:
                self._command_handler.digital_response_table[pin][self. _command_handler.RESPONSE_TABLE_MODE] = self.INPUT
                self.enable_digital_reporting(pin)

        else:  # must be output - so set the tables accordingly
            if pin_type == self.ANALOG:
                self._command_handler.analog_response_table[pin][self. _command_handler.RESPONSE_TABLE_MODE] = mode
            else:
                self._command_handler.digital_response_table[pin][self. _command_handler.RESPONSE_TABLE_MODE] = mode

    def set_sampling_interval(self, interval):
        """
        This method sends the desired sampling interval to Firmata.
        Note: Standard Firmata (and NotSoStandardFirmata) will ignore any interval less than 10 milliseconds
        @param interval: integer value for desired sampling interval in milliseconds
        @return: No return value.
        """
        data = [ interval & 0x7f, interval >> 7]
        self._command_handler.send_sysex(self._command_handler.SAMPLING_INTERVAL, data)


    def servo_config(self, pin, min_pulse=544, max_pulse=2400):
        """
        Configure a pin as a servo pin. Set pulse min, max in ms.
        @param pin: Servo Pin.
        @param min_pulse: Min pulse width in ms.
        @param max_pulse: Max pulse width in ms.
        @return: No return value
        """
        self.set_pin_mode(pin, self.SERVO, self._command_handler.OUTPUT)
        command = [self._command_handler.SERVO_CONFIG, pin, min_pulse & 0x7f, min_pulse >> 7, max_pulse & 0x7f,
                   max_pulse >> 7]

        self._command_handler.send_command(command)









