import board
import digitalio
from time import sleep
import adafruit_dotstar as dotstar
import usb_hid
from adafruit_hid.keyboard import Keyboard

from config import keybow_type, colors, keycodes

def led_position(p):
    if keybow_type:
        return 2 - p
    else:
        # i = 左からn個目-1
        i = p % 3
        # 横側のベースの数(i * 4) + 縦方向の数(下から1段〜4段)
        return i * 4 + (4 - int((p + 3 - i) / 3))

dots = dotstar.DotStar(board.GP2, board.GP3, 30, brightness=0.5)

keyboard=Keyboard(usb_hid.devices)
if keybow_type:
    buttons = [
        digitalio.DigitalInOut(board.GP11),
        digitalio.DigitalInOut(board.GP14),
        digitalio.DigitalInOut(board.GP17)
    ]
else:
    buttons = [
        digitalio.DigitalInOut(board.GP11),
        digitalio.DigitalInOut(board.GP12),
        digitalio.DigitalInOut(board.GP13),
        digitalio.DigitalInOut(board.GP14),
        digitalio.DigitalInOut(board.GP15),
        digitalio.DigitalInOut(board.GP16),
        digitalio.DigitalInOut(board.GP17),
        digitalio.DigitalInOut(board.GP18),
        digitalio.DigitalInOut(board.GP19),
        digitalio.DigitalInOut(board.GP20),
        digitalio.DigitalInOut(board.GP21),
        digitalio.DigitalInOut(board.GP22)
    ]
for b in buttons:
    b.switch_to_input(pull=digitalio.Pull.UP)

a = len(buttons) - 1
sw = [0] * len(buttons)

while True:
    for i,b in enumerate(buttons):
        if not b.value:
            if not sw[i]:
                try:
                    dots[led_position(i)] = colors[i]
                    for k in keycodes[i]:
                        keyboard.press(k)
                        sleep(0.05)
                    sw[i] = 1
                except:
                    pass
        else:
            if sw[i]:
                keyboard.release_all()
                dots[led_position(i)] = (0, 0, 0)
                sw[i] = 0
    sleep(0.02)