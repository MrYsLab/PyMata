PyMata
======
PyMata is a high performance, multi-threaded, non-blocking Python client for the Firmata Protocol that supports
the complete StandardFirmata protocol.


###Major features
* __Implements the entire Firmata 2.4 protocol.__
* __Python 2.7+ and Python 3.4+__ compatibility through a shared code set.
* Easy to use and intuitive __API__. You can view the [PyMata API Documentation here](https://drive.google.com/uc?id=0B4Qt0LRbWv31eXFhd3Etb0VNclU&authuser=0) or view in the Documentation/html directory.
* Custom support for __stepper motors, Sonar Ping Devices (HC-SRO4), Piezo devices and Rotary Encoders__.
* __Wiring diagrams__ are provided for all examples in the examples directory.
* Digial and Analog __Transient Signal Monitoring Via Data Latches:__
  * They provide "one-shot" notification when either a digital or analog pin meets a user defined threshold.
  * Analog latches compare each data change to a user specified value.
    * Comparison operators are <, >, <= and >=
  * Digital latches compare a data change to either a high or low, specified by the user.
  * Latches can easily be re-armed to detect the next transient data change.
  * Latches can be either manually read or a callback can be associated with a latch for immediate notification.
* Optional __callbacks__ provide asynchronous notification of data updates:
  * Digital input pins.
  * Analog input pins.
  * Encoder changes.
  * I2C read data changes.
  * SONAR (HC-SR04) distance changes.
  * Analog latch condition achieved.
  * Digital latch condition achieved.
  * Callbacks return data reports in a single list format.
  * Polling methods and callbacks are available simultaneously and can be used in a mixed polled/callback environment.
  * Callbacks return data in a single list.
  
  ###The callback data return values:
  
| Callback Type | List Element 0 | List Element 1 | List Element 2 | List Element 3 |
| ------------- | -------------- | -------------- | -------------- | -------------- |
| Analog| ANALOG MODE|Pin Number|Data Value|Not Applicable
| Digital|DIGITAL MODE|Pin Number|Data Value|Not Applicable
|I2C|I2C MODE|I2C Device Address|Data Value|Not Applicable
|Sonar|Trigger Pin|Distance in Centimeters|Not Applicable|Not Applicatble
| Encoder|Encoder MODE|Pin Number|Data Value|Not Applicable
| Latched Analog| LATCHED ANALOG MODE|Pin Number|Data Value|Time Stamp
| Latched Digital|LATCHED DIGITAL MODE|Pin Number|Data Value|Time Stamp



### Control-C Signal Handler
Below is a sample Control-C signal handler that can be added to a PyMata Application.
It suppresses exceptions being reported as a result of the user entering a Control-C to abort the application.

```python
import sys
import signal
# followed by another imports your application requires

# create a PyMata instance
# set the COM port string specifically for your platform
board = PyMata("/dev/ttyACM0")

# signal handler function called when Control-C occurs
def signal_handler(signal, frame):
    print('You pressed Ctrl+C!!!!')
    if board != None:
        board.reset()
    sys.exit(0)

# listen for SIGINT
signal.signal(signal.SIGINT, signal_handler)

# Your Application Continues Below This Point
```

####Want to extend PyMata? See [Our Instructables Article](http://www.instructables.com/id/Going-Beyond-StandardFirmata-Adding-New-Device-Sup/) explaining how stepper motor support was added. Use it as a guide to customize PyMata for your own needs.
###[Check Out Mr. Y's Blog Here](http://mryslab.blogspot.com/) for all the latest news!


##Special Note For Linux Users Wishing to Use Python 3.4
Python 3.4 for Linux appears to run slower than Python 2.7.
We will be investigating further and monitoring for a solution.
The problem has been reported to python.org and may be tracked here: [http://bugs.python.org/issue23324] (http://bugs.python.org/issue2332)


There are no performance issues between Python 2.7 and Python 3.4 when running Windows.
