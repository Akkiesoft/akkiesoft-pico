# Written in CircuitPython
# for Raspberry Pi Pico or Pimoroni Tiny2040

import board
import digitalio
from time import sleep
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse

mouse = Mouse(usb_hid.devices)
keyboard=Keyboard(usb_hid.devices)
keycodes = [Keycode.A, Keycode.D]

button = digitalio.DigitalInOut(board.GP2)
button.switch_to_input(pull=digitalio.Pull.UP)

# 0 = Pico / 1 = Tiny2040
tiny2040 = 1
if tiny2040:
  led = digitalio.DigitalInOut(board.LED_G)
  led.direction = digitalio.Direction.OUTPUT
  led_b = digitalio.DigitalInOut(board.LED_B)
  led_b.direction = digitalio.Direction.OUTPUT
  # tiny2040 LED is active low
  led.value = 1
  led_b.value = 1
else:
  led = digitalio.DigitalInOut(board.LED)
  led.direction = digitalio.Direction.OUTPUT
  led_b = None

i = 1
l = 1

while True:
  led.value = l
  if not button.value:
    if not led_b is None:
      led_b.value = l
    mouse.press(Mouse.LEFT_BUTTON)
    sleep(1.7)
    keyboard.press(keycodes[i])
    sleep(0.22)
    keyboard.release(keycodes[i])
    i = 1 - i
  else:
    if not led_b is None:
      led_b.value = 1
    mouse.release(Mouse.LEFT_BUTTON)
    i = 1
    sleep(2)
  l = 1 - l