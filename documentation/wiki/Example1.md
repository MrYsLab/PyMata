# Welcome to the PyMata wiki!

Below is a simple programming example that illustrates how to use callbacks to monitor an analog and digital input.

```python
"""
This example illustrates using callbacks for digital input, and analog input.
Monitor the current analog input and digital input of 2 pins.
"""

import signal
import sys

from PyMata.pymata import PyMata

# Pin definitions

# Digital Input Pin
PUSH_BUTTON = 12

# Analog Input Pin - A2
POTENTIOMETER = 2

# Indices for data passed to callback function

PIN_MODE = 0  # This is the PyMata Pin MODE = ANALOG = 2 and DIGITAL = 0x20:
PIN_NUMBER = 1
DATA_VALUE = 2

# Control-C signal handler to suppress exceptions if user presses Control C
# This is totally optional.

# noinspection PyUnusedLocal
def signal_handler(sig, frame):
    print('You pressed Ctrl+C!!!!')
    if board is not None:
        board.reset()
    sys.exit(0)

# data change callback functions
def cb_potentiometer(data):
    print("Analog Data: Pin Mode - ", data[PIN_MODE], " Pin Number -", data[PIN_NUMBER], " Data Value -  ",
          data[DATA_VALUE])

def cb_push_button(data):
    print("Digital Data: Pin Mode - ", data[PIN_MODE], " Pin Number -", data[PIN_NUMBER], " Data Value -  ",
          data[DATA_VALUE])

signal.signal(signal.SIGINT, signal_handler)  # Instantiate PyMata
board = PyMata("/dev/ttyACM1")

# set up pin modes for both pins with callbacks for each
board.set_pin_mode(PUSH_BUTTON, board.INPUT, board.DIGITAL, cb_push_button)
board.set_pin_mode(POTENTIOMETER, board.INPUT, board.ANALOG,
                   cb_potentiometer)  # A forever loop until user presses Control=c
while 1:
    pass
```
