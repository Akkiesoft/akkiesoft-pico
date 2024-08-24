import board
from digitalio import DigitalInOut, Direction, Pull
import busio
import displayio
import adafruit_displayio_ssd1306
from adafruit_display_text import label
from terminalio import FONT
import time
import random

displayio.release_displays()
i2c = busio.I2C(board.GP21, board.GP20)
display_bus = displayio.I2CDisplay(i2c, device_address=0x3c)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64, rotation=180)
display.root_group = displayio.Group()
splash = display.root_group

btn_black = DigitalInOut(board.GP7)
btn_black.direction = Direction.INPUT
btn_black.pull = Pull.UP
pressed_black = False
btn_white = DigitalInOut(board.GP17)
btn_white.direction = Direction.INPUT
btn_white.pull = Pull.UP
pressed_white = False

game = False
ready = -1
score = 0
ready_time = 3
game_time = 10
direction = 0
next_force_change = False
LAST_TIME = -1
FINGER_LAST_TIME = -1

START_MSG = "<-PUSH"
label_msg = label.Label(FONT, text=START_MSG, color=0xFFFFFF, x=0, y=4)
splash.append(label_msg)
label_score = label.Label(FONT, text="", color=0xFFFFFF, x=68, y=4)
splash.append(label_score)

def update_score():
    label_score.text = "SCORE:%04d" % score

def check_finger(finger):
    global score
    if finger.hidden:
        score -= 1
    else:
        score += 1
    update_score()

update_score()

uiiin = displayio.OnDiskBitmap("/uiiin.bmp")
tile_grid = displayio.TileGrid(uiiin, pixel_shader=uiiin.pixel_shader, x=3, y=24)
splash.append(tile_grid)

finger = displayio.OnDiskBitmap("/finger.bmp")
finger_left = displayio.TileGrid(finger, pixel_shader=finger.pixel_shader, x=16, y=24)
finger_right = displayio.TileGrid(finger, pixel_shader=finger.pixel_shader, x=110, y=24)
splash.append(finger_left)
splash.append(finger_right)

while True:
    now = time.monotonic()

    if not game:
        if 0 <= ready and (LAST_TIME + 1) <= now:
            LAST_TIME = now
            ready -= 1
            if ready < 0:
                game = True
                LAST_TIME = -1
                continue
            label_msg.text = "READY[%d]" % (ready + 1)
        if not btn_black.value and ready < 0:
            ready = ready_time
            timeup = game_time
            score = 0
            update_score()
        continue

    if (FINGER_LAST_TIME + 0.1) <= now:
        FINGER_LAST_TIME = now
        nyan = int(random.random() * 100)
        if nyan % 90 == 0 or next_force_change:
            next_force_change = False
            direction = int(random.random() * 2)
        if direction:
            finger_left.hidden = False
            finger_right.hidden = True
        else:
            finger_left.hidden = True
            finger_right.hidden = False

    if not btn_black.value:
        if not pressed_black:
            pressed_black = True
            check_finger(finger_left)
            next_force_change = True
    else:
        pressed_black = False

    if not btn_white.value:
        if not pressed_white:
            pressed_white = True
            check_finger(finger_right)
            next_force_change = True
    else:
        pressed_white = False

    if LAST_TIME + 1 <= now:
        LAST_TIME = now
        timeup -= 1
        if timeup < 0:
            finger_left.hidden = False
            finger_right.hidden = False
            label_msg.text = "TIME UP!"
            game = False
            time.sleep(5)
            label_msg.text = START_MSG
        else:
            label_msg.text = "%02d" % (timeup + 1)
