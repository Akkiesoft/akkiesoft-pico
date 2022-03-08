# cursor move test for CircuitPython

import board
import digitalio
from time import sleep
import random
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.mouse import Mouse
from adafruit_hid.keycode import Keycode

mouse = Mouse(usb_hid.devices)

button = digitalio.DigitalInOut(board.GP6)
button.switch_to_input(pull=digitalio.Pull.UP)

leds = [[board.LED_R], [board.LED_G], [board.LED_B]]
for led in leds:
    led.append(digitalio.DigitalInOut(led[0]))
    led[1].direction = digitalio.Direction.OUTPUT
     # tiny2040 LED is active low
    led[1].value = 1

def uro2mouse():
    x = 0
    y = 0
    i = random.randint(0, 3)
    for led in leds:
        led[1].value = 1
    if i == 0:
        y = 5
    elif i == 1:
        x = 5
    elif i == 2:
        y = -5
    elif i == 3:
        x = -5
        leds[1][1].value = 0
        leds[2][1].value = 0
    leds[i % 3][1].value = 0
    mouse.move(x = x, y = y)

while True:
    if not button.value:
        uro2mouse()
    else:
        for led in leds:
            led[1].value = 1
    sleep(0.1)