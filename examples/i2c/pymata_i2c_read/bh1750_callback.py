from PyMata.pymata import PyMata
import sys
import time
import signal

board = PyMata("/dev/ttyACM0")

# for leonardo
board.i2c_config(0, board.DIGITAL, 3, 2)


# for uno
# board.i2c_config(0, board.ANALOG, 4, 5)

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!!!!')
    if board is not None:
        board.reset()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


def lux_callback(data):
    datax = data[2]
    print 'Got read data: %s' % data
    lux = (datax[1] << 8 | datax[2]) >> 4
    lux /= 1.2
    print str(lux) + ' lux'


while True:
    try:
        board.i2c_write(0x23, board.I2C_READ_CONTINUOUSLY)  # same results with board.I2C_READ
        time.sleep(.3)
        board.i2c_read(0x23, 0, 2, board.I2C_READ, lux_callback)  # same results with board.I2C_READ_CONTINUOUSLY
        time.sleep(.3)
    except KeyboardInterrupt:
        board.close()
