PyMata
======

Version 1.54
------------
Support for monitoring up to 6 simultaneous HC-SR04 Ping Devices. This feature requires the supplied Arduino sketch
called FirmataPlus.

To compile FirmataPlus, the NewPing library needs to be installed: https://code.google.com/p/arduino-new-ping/

After downloading, one of the library files needs modification to successfully compile:
https://code.google.com/p/arduino-new-ping/wiki/HELP_Error_Vector_7_When_Compiling

FirmataPlus requires the use of the Arduino IDE version 1.5.5 or newer.

FirmataPlus removed support for rotary encoder, because the library was limited to the Uno. It is still
available with the supplied NotSoStandardFirmata Arduino sketch.

Version 1.53
------------
Corrected digital write  to only affect one bit in the port register. Previously all bits were affected
as the result of a write.

Support for the additional pins of the Mega 2560 R3 has been added.

Version 1.52
------------

Fixed IGNORE pin mode to be correct value in pymata.py

Version 1.51
------------

Two new features have been added.

1. The PyMata version number can be retrieved using get_pymata_version().

2. Analog and Digital Software Data Latches have been added.
   Firmata normally reports changes to values in input data for both analog and digital pins. The data latch feature allows the user to specify a threshold value for the pin and to have the data value stored and time stamped.
   When latched data is read, the latch registers are cleared and the user can re-arm the latching mechanism.

   The new methods for latched data contained in pymata.py are:

       set_analog_latch(pin, threshold_type, threshold_value) - arm latching for the selected pin and select the threshold type (>=, <=, >, <) and the threshold value (0-1023) to be detected and stored.

       set_digital_latch(pin, threshold_type)  - arm latching by selecting the pin and the threshold type (HIGH or LOW) to be detected and stored.

       get_analog_latch_data(pin) - returns a list with: [pin number, latching_state (ignore, armed, or latched), the latched data, time stamp of latching event]

       get_digital_latch_data(pin) - returns a list with: [pin number, latching_state (ignore, armed, or latched), the latched data, time stamp of latching event]


       This feature is useful when the client program is blocked or is polling too slowly to detect a data change. For example, with a momentary switch, the switch may have been closed, but when the client goes to read the switch value it has opened again.
       For analog data, the client may want to keep track of the occasional data threshold crossing and does not wish to constantly poll to detect this change.


Also, the entire package is now fully documented in HTML. Go to the documentation/html directory and open up index.html in your browser to view it.


What is PyMata ?
--------------

Harness the raw power of Standard Firmata without having to master the complexities of Standard Firmata's communication protocol. The PyMata class library is an easy to use, high performance abstraction layer for Standard Firmata. A fully documented, straight forward API is provided so that you can quickly code your application.

Epydoc generated API documentation is provided in html format. The source code is fully commented to help make extending PyMata a straight forward task.


Fully commented example applications are provided to help accelerate your development efforts.

Before using PyMata, PySerial needs to be installed. PySerial installation instructions may be found at http://pyserial.sourceforge.net/.

If you are CodeShield user, an enhanced version of Standard Firmata, called NotSoStandard Firmata is provided as part of this package. It adds tone generation and rotary support functionality. NOTE: currently, rotary encoder support is not available for the Arduino Leonardo. To install the libraries in Arduino for rotary encoder support, please visit these links:

http://code.google.com/p/adaencoder/

http://code.google.com/p/oopinchangeint/




Included Examples
-----------------

pymata_basics - a simple client application to communicate with an Arduino board

pymata_i2c_write - this contains both a control layer for the Adafruit Bi-Color 8x8 LED Matrix and a demo program

pymata_i2c_read -  a demo program to read from a SparkFun TMP102 Breakout temperature device.

pymata_software_data_latch - demo program that illustrates the use of the data latching feature


Standard PyMata Import Line
---------------------------
from PyMata.pymata import PyMata



