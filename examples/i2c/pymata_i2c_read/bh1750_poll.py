import time

from PyMata.pymata import PyMata

board = PyMata("/dev/ttyACM0")

# for leonardo
board.i2c_config(0, board.DIGITAL, 3, 2)

# for uno
# board.i2c_config(0, board.ANALOG, 4, 5)


while True:
    try:
        board.i2c_write(0x23, board.I2C_READ_CONTINUOUSLY)  # same results with board.I2C_READ
        time.sleep(.2)
        board.i2c_read(0x23, 0, 2, board.I2C_READ)  # same results with board.I2C_READ_CONTINUOUSLY
        time.sleep(.3)

        data = board.i2c_get_read_data(0x23)
        print('Got read data: %s' % data)
        lux = (data[1] << 8 | data[2]) >> 4
        lux /= 1.2
        print(str(lux) + ' lux')
    except KeyboardInterrupt:
        board.close()
