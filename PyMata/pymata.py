__author__ = 'Copyright (c) 2013 Alan Yorinks All rights reserved.'

"""
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

from collections import deque
import threading
import sys
import time

from .pymata_serial import PyMataSerial
from .pymata_command_handler import PyMataCommandHandler


# For report data formats refer to http://firmata.org/wiki/Protocol


# noinspection PyPep8
class PyMata:
    """
    This class contains the complete set of API methods that permit control of an Arduino
    Micro-Controller utilizing Firmata or its derivatives.

    For information about the Firmata protocol, refer to: http://firmata.org/wiki/Protocol
    """
    # some state variables
    HIGH = 1  # digital pin state high value
    LOW = 0  # digital pin state low value

    REPORTING_ENABLE = 1  # enable reporting for REPORT_ANALOG or REPORT_DIGITAL message sent to firmata
    REPORTING_DISABLE = 0  # disable reporting for REPORT_ANALOG or REPORT_DIGITAL message sent to firmata

    # Shared Resources - data structures, controlling mechanisms, and reference variables

    # Commands and data received from Firmata via the serial interface are placed into the command deque.
    # The pymata_command_handler class removes and processes this information.
    command_deque = deque()

    # This is the instance reference to the communications port object
    arduino = None

    # This is  a thread lock to assure data integrity when reading or writing to the data response tables
    # (defined in the CommandHandler class). It shared by the pymata class and the pymata_command_handler class.
    data_lock = threading.RLock()

    # This is the instance reference to the _command_handler
    _command_handler = None

    # pin modes
    INPUT = 0x00  # pin set as input
    OUTPUT = 0x01  # pin set as output
    ANALOG = 0x02  # analog pin in analogInput mode
    PWM = 0x03  # digital pin in PWM output mode
    SERVO = 0x04  # digital pin in Servo output mode
    I2C = 0x06  # pin included in I2C setup
    ONEWIRE = 0x07  # possible future feature
    STEPPER = 0x08  # any pin in stepper mode
    TONE = 0x09  # Any pin in TONE mode
    ENCODER = 0x0a
    SONAR = 0x0b  # Any pin in SONAR mode
    IGNORE = 0x7f
    LATCH_MODE = 0xE0  # this value is or'ed with pin modes for latched data callback

    # the following pin modes are not part of or defined by Firmata
    # but used by PyMata
    DIGITAL = 0x20

    # I2C command operation modes
    I2C_WRITE = 0B00000000
    I2C_READ = 0B00001000
    I2C_READ_CONTINUOUSLY = 0B00010000
    I2C_STOP_READING = 0B00011000
    I2C_READ_WRITE_MODE_MASK = 0B00011000

    # Tone commands
    TONE_TONE = 0  # play a tone
    TONE_NO_TONE = 1  # turn off tone

    # Stepper Motor Sub-commands
    STEPPER_CONFIGURE = 0  # configure a stepper motor for operation
    STEPPER_STEP = 1  # command a motor to move at the provided speed
    STEPPER_LIBRARY_VERSION = 2  # used to get stepper library version number

    # each byte represents a digital port and its value contains the current port settings
    digital_output_port_pins = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

    # noinspection PyPep8Naming
    def __init__(self, port_id='/dev/ttyACM0', bluetooth=True):
        """
        The "constructor" instantiates the entire interface. It starts the operational threads for the serial
        interface as well as for the command handler.
        @param port_id: Communications port specifier (COM3, /dev/ttyACM0, etc)
        @param bluetooth: Sets start up delays for bluetooth connectivity. Set to False for faster start up.
        """
        # Currently only serial communication over USB is supported, but in the future
        # wifi and other transport mechanism support is anticipated

        try:

            print("\nPython Version %s" % sys.version)
            print('\nPyMata version 2.04   Copyright(C) 2013-15 Alan Yorinks    All rights reserved.')

            # Instantiate the serial support class
            self.transport = PyMataSerial(port_id, self.command_deque)

            # wait for HC-06 Bluetooth slave to initialize in case it is being used.
            if bluetooth:
                time.sleep(5)

            # Attempt opening communications with the Arduino micro-controller
            self.transport.open()

            # additional wait for HC-06 if it is being used
            if bluetooth:
                time.sleep(2)
            else:
                # necessary to support Arduino Mega
                time.sleep(1)

            # Start the data receive thread
            self.transport.start()

            # Instantiate the command handler
            self._command_handler = PyMataCommandHandler(self)
            self._command_handler.system_reset()

            ########################################################################
            # constants defined locally from values contained in the command handler
            ########################################################################

            # Data latch state constants to be used when accessing data returned from get_latch_data methods.
            # The get_latch data methods return [pin_number, latch_state, latched_data, time_stamp]
            # These three constants define possible values for the second item in the list, latch_state

            # this pin will be ignored for latching - table initialized with this value
            self.LATCH_IGNORE = self._command_handler.LATCH_IGNORE
            # When the next pin value change is received for this pin, if it matches the latch criteria
            # the data will be latched.
            self.LATCH_ARMED = self._command_handler.LATCH_ARMED
            # Data has been latched. Read the data to re-arm the latch.
            self.LATCH_LATCHED = self._command_handler.LATCH_LATCHED

            #
            # These constants are used when setting a data latch.
            # Latch threshold types
            #
            self.DIGITAL_LATCH_HIGH = self._command_handler.DIGITAL_LATCH_HIGH
            self.DIGITAL_LATCH_LOW = self._command_handler.DIGITAL_LATCH_LOW

            self.ANALOG_LATCH_GT = self._command_handler.ANALOG_LATCH_GT
            self.ANALOG_LATCH_LT = self._command_handler.ANALOG_LATCH_LT
            self.ANALOG_LATCH_GTE = self._command_handler.ANALOG_LATCH_GTE
            self.ANALOG_LATCH_LTE = self._command_handler.ANALOG_LATCH_LTE

            # constants to be used to parse the data returned from calling
            # get_X_latch_data()

            self.LATCH_PIN = 0
            self.LATCH_STATE = 1
            self.LATCHED_DATA = 2
            self.LATCHED_TIME_STAMP = 3

            # Start the command processing thread
            self._command_handler.start()

            # Command handler should now be prepared to receive replies from the Arduino, so go ahead
            # detect the Arduino board

            print('Please wait while Arduino is being detected. This can take up to 30 seconds ...')

            # perform board auto discovery
            if not self._command_handler.auto_discover_board():
                # board was not found so shutdown
                print("Board Auto Discovery Failed!, Shutting Down")
                self._command_handler.stop()
                self.transport.stop()
                self._command_handler.join()
                self.transport.join()
                time.sleep(2)

        except KeyboardInterrupt:
            print("Program Aborted Before PyMata Instantiated")
            sys.exit()

    def analog_mapping_query(self):
        """
        Send an analog mapping query message via sysex. Client retrieves the results with a
        call to get_analog_mapping_request_results()
        """
        self._command_handler.send_sysex(self._command_handler.ANALOG_MAPPING_QUERY, None)

    def analog_read(self, pin):
        """
        Retrieve the last analog data value received for the specified pin.
        @param pin: Selected pin
        @return: The last value entered into the analog response table.
        """
        with self.data_lock:
            data = self._command_handler.analog_response_table[pin][self._command_handler.RESPONSE_TABLE_PIN_DATA_VALUE]
        return data

    def analog_write(self, pin, value):
        """
        Set the specified pin to the specified value.
        @param pin: Pin number
        @param value: Pin value
        @return: No return value
        """

        if self._command_handler.ANALOG_MESSAGE + pin < 0xf0:
            command = [self._command_handler.ANALOG_MESSAGE + pin, value & 0x7f, value >> 7]
            self._command_handler.send_command(command)
        else:
            self.extended_analog(pin, value)

    def capability_query(self):
        """
        Send a Firmata capability query message via sysex. Client retrieves the results with a
        call to get_capability_query_results()
        The Arduino can be rather slow in responding to this command. For 
        the Mega 2560 R3 it has taken up to 25 seconds for a response.   
        """
        self._command_handler.send_sysex(self._command_handler.CAPABILITY_QUERY, None)

    def close(self):
        """
        This method will close the transport (serial port) and exit
        @return: No return value, but sys.exit(0) is called.
        """

        self._command_handler.system_reset()
        self._command_handler.stop()
        self.transport.stop()
        self.transport.close()

        print("PyMata close(): Calling sys.exit(0): Hope to see you soon!")
        sys.exit(0)

    def digital_read(self, pin):
        """
        Retrieve the last digital data value received for the specified pin.
        NOTE: This command will return values for digital, pwm, etc,  pin types
        @param pin: Selected pin
        @return: The last value entered into the digital response table.
        """
        with self.data_lock:
            data = \
                self._command_handler.digital_response_table[pin][self._command_handler.RESPONSE_TABLE_PIN_DATA_VALUE]
        return data

    def digital_write(self, pin, value):
        """
        Set the specified pin to the specified value.
        @param pin: pin number
        @param value: pin value
        @return: No return value
        """
        # The command value is not a fixed value, but needs to be calculated using the
        # pin's port number
        #
        #
        port = pin // 8

        calculated_command = self._command_handler.DIGITAL_MESSAGE + port
        mask = 1 << (pin % 8)
        # Calculate the value for the pin's position in the port mask
        if value == 1:
            self.digital_output_port_pins[port] |= mask

        else:
            self.digital_output_port_pins[port] &= ~mask

        # Assemble the command
        command = (calculated_command, self.digital_output_port_pins[port] & 0x7f,
                   self.digital_output_port_pins[port] >> 7)

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
        is disabled for all 8 bits in the "port" -
        @param pin: Pin and all pins for this port
        @return: No return value
        """
        port = pin // 8
        command = [self._command_handler.REPORT_DIGITAL + port, self.REPORTING_DISABLE]
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
        Enables digital reporting. By turning reporting on for all 8 bits in the "port" -
        this is part of Firmata's protocol specification.
        @param pin: Pin and all pins for this port
        @return: No return value
        """
        port = pin // 8
        command = [self._command_handler.REPORT_DIGITAL + port, self.REPORTING_ENABLE]
        self._command_handler.send_command(command)

    def encoder_config(self, pin_a, pin_b, cb=None):
        """
        This command enables the rotary encoder (2 pin + ground) and will
        enable encoder reporting.

        NOTE: This command is not currently part of standard arduino firmata, but is provided for legacy
        support of CodeShield on an Arduino UNO.

        Encoder data is retrieved by performing a digital_read from pin a (encoder pin 1)

        @param pin_a: Encoder pin 1.
        @param pin_b: Encoder pin 2.
        @param cb: callback function to report encoder changes
        @return: No return value
        """
        data = [pin_a, pin_b]
        self._command_handler.digital_response_table[pin_a][self._command_handler.RESPONSE_TABLE_MODE] \
            = self.ENCODER
        self._command_handler.digital_response_table[pin_a][self._command_handler.RESPONSE_TABLE_CALLBACK] = cb
        self.enable_digital_reporting(pin_a)

        self._command_handler.digital_response_table[pin_b][self._command_handler.RESPONSE_TABLE_MODE] \
            = self.ENCODER
        self._command_handler.digital_response_table[pin_b][self._command_handler.RESPONSE_TABLE_CALLBACK] = cb
        self.enable_digital_reporting(pin_b)

        self._command_handler.send_sysex(self._command_handler.ENCODER_CONFIG, data)

    def extended_analog(self, pin, data):
        """
        This method will send an extended data analog output command to the selected pin
        @param pin: 0 - 127
        @param data: 0 - 0xfffff
        """
        analog_data = [pin, data & 0x7f, (data >> 7) & 0x7f, data >> 14]
        self._command_handler.send_sysex(self._command_handler.EXTENDED_ANALOG, analog_data)

    def get_analog_latch_data(self, pin):
        """
        A list is returned containing the latch state for the pin, the latched value, and the time stamp
        [pin_num, latch_state, latched_value, time_stamp]
        If the the latch state is LATCH_LATCHED, the table is reset (data and timestamp set to zero)
        @param pin: Pin number.
        @return: [pin, latch_state, latch_data_value, time_stamp]
        """
        return self._command_handler.get_analog_latch_data(pin)

    def get_analog_mapping_request_results(self):
        """
        Call this method after calling analog_mapping_query() to retrieve its results
        @return: raw data returned by firmata
        """
        return self._command_handler.analog_mapping_query_results

    def get_analog_response_table(self):
        """
        This method returns a list of lists representing the current pin mode and
        associated data values for all analog pins.
        All configured pin types, both input and output will be listed. Output pin data will contain zero.
        @return: The last update of the digital response table
        """
        return self._command_handler.get_analog_response_table()

    def get_capability_query_results(self):
        """
        Retrieve the data returned by a previous call to capability_query()
        @return: Raw capability data returned by firmata
        """
        return self._command_handler.capability_query_results

    def get_digital_latch_data(self, pin):
        """
        A list is returned containing the latch state for the pin, the latched value, and the time stamp
        [pin_num, latch_state, latched_value, time_stamp]
        If the the latch state is LATCH_LATCHED, the table is reset (data and timestamp set to zero)
        @param pin: Pin number.
        @return: [pin, latch_state, latch_data_value, time_stamp]
        """
        return self._command_handler.get_digital_latch_data(pin)

    def get_digital_response_table(self):
        """
        This method returns a list of lists representing the current pin mode
        and associated data for all digital pins.
        All pin types, both input and output will be listed. Output pin data will contain zero.
        @return: The last update of the digital response table
        """
        return self._command_handler.get_digital_response_table()

    def get_firmata_version(self):
        """
        Retrieve the firmata version information returned by a previous call to refresh_report_version()
        @return: Firmata_version list [major, minor] or None
         """
        return self._command_handler.firmata_version

    def get_firmata_firmware_version(self):
        """
        Retrieve the firmware id information returned by a previous call to refresh_report_firmware()
        @return: Firmata_firmware  list [major, minor, file_name] or None
        """
        return self._command_handler.firmata_firmware

    def get_pin_state_query_results(self):
        """
        This method returns the results of a previous call to pin_state_query() and then resets
        the pin state query data to None

        @return: Raw pin state query data
        """
        r_data = self._command_handler.last_pin_query_results
        self._command_handler.last_pin_query_results = []
        return r_data

    # noinspection PyMethodMayBeStatic
    def get_pymata_version(self):
        """
        Returns the PyMata version number in a list: [Major Number, Minor Number]

        @return:
        """
        return [1, 57]

    # noinspection PyMethodMayBeStatic
    def get_sonar_data(self):
        """
        Retrieve Ping (HC-SR04 type) data. The data is presented as a dictionary.
        The 'key' is the trigger pin specified in sonar_config() and the 'data' is the
        current measured distance (in centimeters)
        for that pin. If there is no data, the value is set to IGNORE (127).

        @return: active_sonar_map
        """
        return self._command_handler.active_sonar_map

    def get_stepper_version(self, timeout=20):
        """
        @param timeout: specify a time to allow arduino to process and return a version
        @return: the stepper version number if it was set.
        """
        # get current time
        start_time = time.time()

        # wait for up to 20 seconds for a successful capability query to occur

        while self._command_handler.stepper_library_version <= 0:
            if time.time() - start_time > timeout:
                print("Stepper Library Version Request timed-out. "
                      "Did you send a stepper_request_library_version command?")
                return
            else:
                pass
        return self._command_handler.stepper_library_version

    def i2c_config(self, read_delay_time=0, pin_type=None, clk_pin=0, data_pin=0):
        """
        NOTE: THIS METHOD MUST BE CALLED BEFORE ANY I2C REQUEST IS MADE
        This method initializes Firmata for I2c operations.
        It allows setting of a read time delay amount, and to optionally track
        the pins as I2C in the appropriate response table.
        To track pins: Set the pin_type to ANALOG or DIGITAL and provide the pin numbers.
        If using ANALOG, pin numbers use the analog number, for example A4: use 4.

        @param read_delay_time: an optional parameter, default is 0
        @param pin_type: ANALOG or DIGITAL to select response table type to track pin numbers
        @param clk_pin: pin number (see comment above).
        @param data_pin: pin number (see comment above).
        @return: No Return Value
        """
        data = [read_delay_time & 0x7f, read_delay_time >> 7]
        self._command_handler.send_sysex(self._command_handler.I2C_CONFIG, data)

        # If pin type is set, set pin mode in appropriate response table for these pins
        if pin_type:
            if pin_type == self.DIGITAL:
                self._command_handler.digital_response_table[clk_pin][self._command_handler.RESPONSE_TABLE_MODE] \
                    = self.I2C
                self._command_handler.digital_response_table[data_pin][self._command_handler.RESPONSE_TABLE_MODE] \
                    = self.I2C
            else:
                self._command_handler.analog_response_table[clk_pin][self._command_handler.RESPONSE_TABLE_MODE] \
                    = self.I2C
                self._command_handler.analog_response_table[data_pin][self._command_handler.RESPONSE_TABLE_MODE] \
                    = self.I2C

    def i2c_read(self, address, register, number_of_bytes, read_type, cb=None):
        """
        This method requests the read of an i2c device. Results are retrieved by a call to
        i2c_get_read_data().
        If a callback method is provided, when data is received from the device it will be sent to the callback method
        @param address: i2c device address
        @param register: register number (can be set to zero)
        @param number_of_bytes: number of bytes expected to be returned
        @param read_type: I2C_READ  or I2C_READ_CONTINUOUSLY
        @param cb: Optional callback function to report i2c data as result of read command
        """
        data = [address, read_type, register & 0x7f, register >> 7,
                number_of_bytes & 0x7f, number_of_bytes >> 7]

        # add or update entry in i2c_map for reply
        self._command_handler.i2c_map[address] = [cb, None]

        self._command_handler.send_sysex(self._command_handler.I2C_REQUEST, data)

    def i2c_write(self, address, *args):
        """
        Write data to an i2c device.
        @param address: i2c device address
        @param args: A variable number of bytes to be sent to the device
        """
        data = [address, self.I2C_WRITE]
        for item in args:
            data.append(item)
        self._command_handler.send_sysex(self._command_handler.I2C_REQUEST, data)

    def i2c_stop_reading(self, address):
        """
        This method stops an I2C_READ_CONTINUOUSLY operation for the i2c device address specified.
        @param address: address of i2c device
        """
        data = [address, self.I2C_STOP_READING]
        self._command_handler.send_sysex(self._command_handler.I2C_REQUEST, data)

    def i2c_get_read_data(self, address):
        """
        This method retrieves the i2c read data as the result of an i2c_read() command.
        @param address: i2c device address
        @return: raw data read from device
        """
        if address in self._command_handler.i2c_map:
            map_entry = self._command_handler.i2c_map[address]
            return map_entry[1]

    def pin_state_query(self, pin):
        """
        This method issues a pin state query command. Data returned is retrieved via
        a call to get_pin_state_query_results()
        @param pin: pin number
        """
        self._command_handler.send_sysex(self._command_handler.PIN_STATE_QUERY, [pin])

    def play_tone(self, pin, tone_command, frequency, duration):
        """
        This method will call the Tone library for the selected pin.
        If the tone command is set to TONE_TONE, then the specified tone will be played.
        Else, if the tone command is TONE_NO_TONE, then any currently playing tone will be disabled.
        It is intended for a future release of Arduino Firmata
        @param pin: Pin number
        @param tone_command: Either TONE_TONE, or TONE_NO_TONE
        @param frequency: Frequency of tone
        @param duration: Duration of tone in milliseconds
        @return: No return value
        """

        # convert the integer values to bytes
        if tone_command == self.TONE_TONE:
            # duration is specified
            if duration:
                data = [tone_command, pin, frequency & 0x7f, frequency >> 7, duration & 0x7f, duration >> 7]

            else:
                data = [tone_command, pin, frequency & 0x7f, frequency >> 7, 0, 0]

            self._command_handler.digital_response_table[pin][self._command_handler.RESPONSE_TABLE_MODE] = \
                self.TONE
        # turn off tone
        else:
            data = [tone_command, pin]
        self._command_handler.send_sysex(self._command_handler.TONE_PLAY, data)

    def refresh_report_version(self):
        """
        This method will query firmata for the report version.
        Retrieve the report version via a call to get_firmata_version()
        """
        command = [self._command_handler.REPORT_VERSION]
        self._command_handler.send_command(command)

    def refresh_report_firmware(self):
        """
        This method will query firmata to report firmware. Retrieve the report via a
        call to get_firmata_firmware_version()
        """
        self._command_handler.send_sysex(self._command_handler.REPORT_FIRMWARE, None)

    def reset(self):
        """
        This command sends a reset message to the Arduino. The response tables will be reinitialized
        @return: No return value.
        """
        # set all output pins to a value of 0
        for pin in range(0, self._command_handler.total_pins_discovered):
            if self._command_handler.digital_response_table[self._command_handler.RESPONSE_TABLE_MODE] \
                    == self.PWM:
                self.analog_write(pin, 0)
            elif self._command_handler.digital_response_table[self._command_handler.RESPONSE_TABLE_MODE] \
                    == self.SERVO:
                self.analog_write(pin, 0)
            elif self._command_handler.digital_response_table[self._command_handler.RESPONSE_TABLE_MODE] \
                    == self.TONE:
                data = [self.TONE_NO_TONE, pin]
                self._command_handler.send_sysex(self._command_handler.TONE_PLAY, data)
            else:
                self.digital_write(pin, 0)
        self._command_handler.system_reset()

    def set_analog_latch(self, pin, threshold_type, threshold_value, cb=None):
        """
        This method "arms" an analog pin for its data to be latched and saved in the latching table
        If a callback method is provided, when latching criteria is achieved, the callback function is called
        with latching data notification. In that case, the latching table is not updated.
        @param pin: Analog pin number (value following an 'A' designator, i.e. A5 = 5
        @param threshold_type: ANALOG_LATCH_GT | ANALOG_LATCH_LT  | ANALOG_LATCH_GTE | ANALOG_LATCH_LTE
        @param threshold_value: numerical value - between 0 and 1023
        @param cb: callback method
        @return: True if successful, False if parameter data is invalid
        """
        if self.ANALOG_LATCH_GT <= threshold_type <= self.ANALOG_LATCH_LTE:
            if 0 <= threshold_value <= 1023:
                self._command_handler.set_analog_latch(pin, threshold_type, threshold_value, cb)
                return True
        else:
            return False

    def set_digital_latch(self, pin, threshold_type, cb=None):
        """
        This method "arms" a digital pin for its data to be latched and saved in the latching table
        If a callback method is provided, when latching criteria is achieved, the callback function is called
        with latching data notification. In that case, the latching table is not updated.
        @param pin: Digital pin number
        @param threshold_type: DIGITAL_LATCH_HIGH | DIGITAL_LATCH_LOW
        @param cb: callback function
        @return: True if successful, False if parameter data is invalid
        """
        if 0 <= threshold_type <= 1:
            self._command_handler.set_digital_latch(pin, threshold_type, cb)
            return True
        else:
            return False

    def set_pin_mode(self, pin, mode, pin_type, cb=None):
        """
        This method sets a pin to the desired pin mode for the pin_type.
        It automatically enables data reporting.
        NOTE: DO NOT CALL THIS METHOD FOR I2C. See i2c_config().
        @param pin: Pin number (for analog use the analog number, for example A4: use 4)
        @param mode: INPUT, OUTPUT, PWM
        @param pin_type: ANALOG or DIGITAL
        @param cb: This is an optional callback function to report data changes to the user
        @return: No return value
        """
        command = [self._command_handler.SET_PIN_MODE, pin, mode]
        self._command_handler.send_command(command)

        # enable reporting for input pins
        if mode == self.INPUT:
            if pin_type == self.ANALOG:

                # set analog response table to show this pin is an input pin

                self._command_handler.analog_response_table[pin][self._command_handler.RESPONSE_TABLE_MODE] = \
                    self.INPUT
                self._command_handler.analog_response_table[pin][self._command_handler.RESPONSE_TABLE_CALLBACK] = cb
                self.enable_analog_reporting(pin)
            # if not analog it has to be digital
            else:
                self._command_handler.digital_response_table[pin][self._command_handler.RESPONSE_TABLE_MODE] = \
                    self.INPUT
                self._command_handler.digital_response_table[pin][self._command_handler.RESPONSE_TABLE_CALLBACK] = cb

                self.enable_digital_reporting(pin)

        else:  # must be output - so set the tables accordingly
            if pin_type == self.ANALOG:
                self._command_handler.analog_response_table[pin][self._command_handler.RESPONSE_TABLE_MODE] = mode

            else:
                self._command_handler.digital_response_table[pin][self._command_handler.RESPONSE_TABLE_MODE] = mode

    def set_sampling_interval(self, interval):
        """
        This method sends the desired sampling interval to Firmata.
        Note: Standard Firmata  will ignore any interval less than 10 milliseconds
        @param interval: Integer value for desired sampling interval in milliseconds
        @return: No return value.
        """
        data = [interval & 0x7f, interval >> 7]
        self._command_handler.send_sysex(self._command_handler.SAMPLING_INTERVAL, data)

    def servo_config(self, pin, min_pulse=544, max_pulse=2400):
        """
        Configure a pin as a servo pin. Set pulse min, max in ms.
        @param pin: Servo Pin.
        @param min_pulse: Min pulse width in ms.
        @param max_pulse: Max pulse width in ms.
        @return: No return value
        """
        self.set_pin_mode(pin, self.SERVO, self.OUTPUT)
        command = [pin, min_pulse & 0x7f, min_pulse >> 7, max_pulse & 0x7f,
                   max_pulse >> 7]

        self._command_handler.send_sysex(self._command_handler.SERVO_CONFIG, command)

    def sonar_config(self, trigger_pin, echo_pin, cb=None, ping_interval=50, max_distance=200):
        """
        Configure the pins,ping interval and maximum distance for an HC-SR04 type device.
        Single pin configuration may be used. To do so, set both the trigger and echo pins to the same value.
        Up to a maximum of 6 SONAR devices is supported
        If the maximum is exceeded a message is sent to the console and the request is ignored.
        NOTE: data is measured in centimeters
        @param trigger_pin: The pin number of for the trigger (transmitter).
        @param echo_pin: The pin number for the received echo.
        @param ping_interval: Minimum interval between pings. Lowest number to use is 33 ms.Max is 127
        @param max_distance: Maximum distance in cm. Max is 200.
        @param cb: optional callback function to report sonar data changes
        """
        if max_distance > 200:
            max_distance = 200
        max_distance_lsb = max_distance & 0x7f
        max_distance_msb = max_distance >> 7
        data = [trigger_pin, echo_pin, ping_interval, max_distance_lsb, max_distance_msb]
        self.set_pin_mode(trigger_pin, self.SONAR, self.INPUT)
        self.set_pin_mode(echo_pin, self.SONAR, self.INPUT)
        # update the ping data map for this pin
        if len(self._command_handler.active_sonar_map) > 6:
            print("sonar_config: maximum number of devices assigned - ignoring request")
            return
        else:
            with self.data_lock:

                # self._command_handler.active_sonar_map[trigger_pin] = self.IGNORE
                self._command_handler.active_sonar_map[trigger_pin] = [cb, [self.IGNORE]]
        self._command_handler.send_sysex(self._command_handler.SONAR_CONFIG, data)

    def stepper_config(self, steps_per_revolution, stepper_pins):
        """
        Configure stepper motor prior to operation.
        @param steps_per_revolution: number of steps per motor revolution
        @param stepper_pins: a list of control pin numbers - either 4 or 2
        """
        data = [self.STEPPER_CONFIGURE, steps_per_revolution & 0x7f, steps_per_revolution >> 7]
        for pin in range(len(stepper_pins)):
            data.append(stepper_pins[pin])
        self._command_handler.send_sysex(self._command_handler.STEPPER_DATA, data)

    def stepper_step(self, motor_speed, number_of_steps):
        """
        Move a stepper motor for the number of steps at the specified speed
        @param motor_speed: 21 bits of data to set motor speed
        @param number_of_steps: 14 bits for number of steps & direction
                                positive is forward, negative is reverse
        """
        if number_of_steps > 0:
            direction = 1
        else:
            direction = 0
        abs_number_of_steps = abs(number_of_steps)
        data = [self.STEPPER_STEP, motor_speed & 0x7f, (motor_speed >> 7) & 0x7f, motor_speed >> 14,
                abs_number_of_steps & 0x7f, abs_number_of_steps >> 7, direction]
        self._command_handler.send_sysex(self._command_handler.STEPPER_DATA, data)

    def stepper_request_library_version(self):
        """
        Request the stepper library version from the Arduino.
        To retrieve the version after this command is called, call
        get_stepper_version
        """
        data = [self.STEPPER_LIBRARY_VERSION]
        self._command_handler.send_sysex(self._command_handler.STEPPER_DATA, data)


