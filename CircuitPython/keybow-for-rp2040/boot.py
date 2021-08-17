import storage
import board
import digitalio
from time import sleep
import adafruit_dotstar as dotstar
import usb_hid

usb_hid.enable((usb_hid.Device.KEYBOARD,))
dots = dotstar.DotStar(board.GP2, board.GP3, 30, brightness=0.5)

button = digitalio.DigitalInOut(board.GP11)
button.pull = digitalio.Pull.UP
if button.value:
    storage.disable_usb_drive()
    dots[2] = (0, 255, 0)
    sleep(0.1)
else:
    dots[2] = (0, 0, 255)
    sleep(1)
dots[2] = (0, 0, 0)