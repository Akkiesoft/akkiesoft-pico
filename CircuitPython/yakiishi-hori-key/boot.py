import storage
import board
import digitalio
import usb_hid
from time import sleep

usb_hid.enable((usb_hid.Device.KEYBOARD,usb_hid.Device.MOUSE,))

button = digitalio.DigitalInOut(board.GP2)
button.switch_to_input(pull=digitalio.Pull.UP)

if button.value:
    storage.disable_usb_drive()
else:
    led = digitalio.DigitalInOut(board.LED_R)
    led.direction = digitalio.Direction.OUTPUT
    led.value = 1
    sleep(1)
    led.value = 0