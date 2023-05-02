import board
from busio import I2C
from time import sleep

class LCD():
    def __init__(self, addr = 0x3e, contrast = 0x5d, light_pin = False):
        self.addr      = addr
        self.contrast  = contrast
        self.light_pin = light_pin
        self.i2c       = I2C(board.GP5, board.GP4)
        if self.light_pin:
            self.light = digitalio.DigitalInOut(self.light_pin)
            self.light.direction = digitalio.Direction.OUTPUT

    def reset(self):
        self.i2c.try_lock()
        self.i2c.writeto(self.addr, bytes([0, 0x38, 0x39, 0x14, 0x78, self.contrast, 0x6c]))
        sleep(0.25)
        self.i2c.writeto(self.addr, bytes([0, 0x0c, 0x01, 0x06]))
        sleep(0.25)
        self.i2c.unlock()

    def clear(self):
        self.i2c.try_lock()
        self.i2c.writeto(self.addr, bytes([0, 1]))
        self.i2c.unlock()

    def set_cursor(self, x, y):
        self.i2c.try_lock()
        self.i2c.writeto(self.addr, bytes([0, 128 + 64 * y + x]))
        self.i2c.unlock()

    def print(self, string):
        s = string.encode('shift_jis')
        self.i2c.try_lock()
        for x in s:
            print(hex(x))
            self.i2c.writeto(self.addr, bytes([0x40, x]))
        self.i2c.unlock()

if __name__ == "__main__":
    # for https://ssci.to/1405
    lcd = LCD()
    # for https://strawberry-linux.com/catalog/items?code=27021
    # lcd = LCD(contrast = 0x5e)

    lcd.reset()
    lcd.clear()
    lcd.print("Hello")
    lcd.set_cursor(2, 1)
    lcd.print("World!")