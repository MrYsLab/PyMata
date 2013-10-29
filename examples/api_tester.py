

from pymata import PyMata
import sys
import time

# pin assignments for CodeShield

#digital outputs
RELAY = 2
PIEZO = 3
SERVO_MOTOR = 5
WHITE_LED = 6
BLUE_LED = 9
GREEN_LED = 10
RED_LED = 11


#digital inputs
BUTTON = 12
SLIDE = 13
ENCODER_A = 14  # this is A0 being used as a digital pin
ENCODER_B = 15  # this is A1 being used as a digital pin

#analog inputs
POT = 2
HALL = 3
THERM = 4
PHOTO = 5


# create an instance of PyMata - we are using an Arduino UNO
firmata = PyMata("/dev/ttyACM0", 20, 6)

#check to see when the board is available for communication
print("Waiting for firmata ...")
while not firmata.is_firmata_ready():
    pass
print("firmata ready")

# show the firmware version
print firmata.get_firmata_firmware_version()


# here are all the digital output pins
digital_output_pins = [RELAY,PIEZO,SERVO_MOTOR,WHITE_LED,BLUE_LED,GREEN_LED,RED_LED ]

# set the pin mode for each of the digital output pins
for pin in digital_output_pins:
    firmata.set_pin_mode(pin, firmata.OUTPUT, firmata.DIGITAL)

# turn each pin on for 1 second and then turn off
for pin in digital_output_pins:
    firmata.digital_write(pin, 1)
    time.sleep(1)
    firmata.digital_write(pin, 0)

# reconfigure pins controlling LEDS as pwm pins
pwm_pins = [WHITE_LED,BLUE_LED,GREEN_LED,RED_LED]
for pin in pwm_pins:
    firmata.set_pin_mode(pin, firmata.PWM, firmata.DIGITAL)

# fade each pin up and down
for pin in pwm_pins:
    for value in range(0,255):
        firmata.analog_write(pin, value)
    for value in range(255,-1,-1):
        firmata.analog_write(pin, value)

# set all LED pins to zero
#for pin in pwm_pins:
#    firmata.analog_write(pin, 0)

# mix red and blue
firmata.set_pin_mode(RED_LED, firmata.OUTPUT, firmata.DIGITAL)
firmata.digital_write(RED_LED,1)
time.sleep(2)
for value in range(0,255):
    firmata.analog_write(BLUE_LED, value)

# kill some time
time.sleep(1)

# turn all LEDs off
firmata.digital_write(RED_LED,0)
firmata.analog_write(BLUE_LED,0)

# set the pin mode for the 2 digital switch input devices
firmata.set_pin_mode(BUTTON, firmata.INPUT, firmata.DIGITAL)
firmata.set_pin_mode(SLIDE, firmata.INPUT, firmata.DIGITAL)

print("Slide switch and watch the values. When you are done, press the button")
# keep reading and printing out the slide switches value until the user
# presses the button switch
while not firmata.digital_read(BUTTON):
    print "\r", firmata.digital_read(SLIDE),

# debounce the switch
time.sleep(.5)

# set the pin mode for the potentiometer
firmata.set_pin_mode(POT, firmata.INPUT, firmata.ANALOG)


print("Turn the Pot and press the button when done")

# keep reading and displaying the pot value until the user presses the button
while not firmata.digital_read(BUTTON):
    print "\r", firmata.analog_read(POT),

# debounce switch
time.sleep(.5)

print("Turn the Encoder and press the button when done")

# configure the encoder pins
firmata.encoder_config(ENCODER_B, ENCODER_A)

# keep reading and displaying the encoder value until the user presses the button
while not firmata.digital_read(BUTTON):
    print "\r", firmata.digital_read(ENCODER_B),

# debounce
time.sleep(.5)

# play a tone and then move the servo
print(" Tone will be played and then servo will be moved")

# play a 1000 hz tone for 500 ms
firmata.play_tone(PIEZO, 1000, 500)

# kill some time
time.sleep(2)

# configure the servo
firmata.servo_config(SERVO_MOTOR)
# move the servo to 20 degrees
firmata.analog_write(SERVO_MOTOR,20)
time.sleep(.5)

# move the servo to 100 degrees
firmata.analog_write(SERVO_MOTOR,100)
time.sleep(.5)

# move the servo to 20 degrees
firmata.analog_write(SERVO_MOTOR,20)

# print the digital response table
print firmata.get_digital_response_table()

# now reset the board
firmata.reset()

# print the digital response table again
print firmata.get_digital_response_table()

sys.exit(0)



