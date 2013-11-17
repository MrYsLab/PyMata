PyMata
======


Harness the raw power of Standard Firmata without having to master the complexities of Standard Firmata's communication protocol. The PyMata class library is an easy to use, high performance abstraction layer for Standard Firmata. A fully documented, straight forward API is provided so that you can quickly code your application.

Pydoc generated API documentation is provided in both PDF and HTML formats. The source code is fully commented to help make extending PyMata a straight forward task.

A fully commented example application is provided to help accelerate your development efforts.

Before using PyMata, PySerial needs to be installed. PySerial installation instructions may be found at http://pyserial.sourceforge.net/.

If you are CodeShield user, an enhanced version of Standard Firmata, called NotSoStandard Firmata is provided as part of this package. It adds tone generation and rotary support functionality. NOTE: currently, rotary encoder support is not available for the Arduino Leonardo. To install the libraries in Arduino for rotary encoder support, please visit these links:

http://code.google.com/p/adaencoder/

http://code.google.com/p/oopinchangeint/


Included Examples
=================

pymata_basics - a simple client application to communicate with an Arduino board

pymata_i2c_write - this contains both a control layer for the Adafruit Bi-Color 8x8 LED Matrix and a demo program

pymata_i2c_read -  a demo program to read from a SparkFun TMP102 Breakout temperature device.



