PyMata
======
PyMata is a high performance, multi-threaded, non-blocking Python client for the Firmata Protocol that supports
the complete StandardFirmata protocol.


###Major features
* Python 2.7+ and Python 3.4+ compatibility through a shared code set.
* Easy to use and intuitive API. You can view the [PyMata API Documentation here](https://drive.google.com/uc?id=0B4Qt0LRbWv31eXFhd3Etb0VNclU&authuser=0) or view in the Documentation/html directory.
* Optional callbacks provide asynchronous notification of data updates.
* Polling methods and callbacks are available simultaneously and can be used in a mixed polled/callback environment.

####Additional features:
* Custom support for stepper motors, Sonar Ping Devices (HC-SRO4), Piezo devices and Rotary Encoders (Uno only).
* Callback granularity is on a per pin basis or I2C address basis
* Latched data support
* Establish a comparison value for the latch to fire upon.
* For polled environments, latching detects and stores transient analog and digital data changes and time stamps their occurrences.
* In an asynchronous callback environment, latches can provide a one-shot notification of a qualified data event. A time stamp is provided within the callback.

####Data update callbacks are available for:
* Digital input pins.
* Analog input pins.
* Encoder changes.
* I2C read data changes.
* SONAR (HC-SR04) distance changes.
* Analog latch condition achieved.
* Digital latch condition achieved.

    
###Callbacks return data in a single list. The callback return list format is as follows:

| Callback Type | List Element 0 | List Element 1 | List Element 2 | List Element 3 |
| ------------- | -------------- | -------------- | -------------- | -------------- |
| Analog| ANALOG MODE|Pin Number|Data Value|Not Applicable
| Digital|DIGITAL MODE|Pin Number|Data Value|Not Applicable
|I2C|I2C MODE|I2C Device Address|Data Value|Not Applicable
|SONAR|Pin 1|Pin 2|Distance in Centimeters
| Encoder|Encoder MODE|Pin Number|Data Value|Not Applicable
| Latched Analog| LATCHED ANALOG MODE|Pin Number|Data Value|Time Stamp
| Latched Digital|LATCHED DIGITAL MODE|Pin Number|Data Value|Time Stamp

##Wiring diagrams are provided for all examples

##Want to extend PyMata? See [Our Instructables Article](http://www.instructables.com/id/Going-Beyond-StandardFirmata-Adding-New-Device-Sup/)

[Check Out Our Blog](http://mryslab.blogspot.com/)
------------------


##Special Note For Linux Users Wishing to Use Python 3.4
Python 3.4 for Linux appears to run slower than Python 2.7.
[See This Article For a Discussion On The Subject](http://www.reddit.com/r/Python/comments/272bao/python_34_slow_compared_to_27_whats_your_mileage/)

There is no performance issues between Python 2.7 and Python 3.4 when running Windows.
