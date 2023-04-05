# based on: https://learn.adafruit.com/macropad-2fa-totp-authentication-friend/project-code

import board
import time
import adafruit_ds3231
import rtc
from  totp import generate_otp
# display
from busio import I2C, SPI
from displayio import release_displays, FourWire, Group, OnDiskBitmap, TileGrid
from terminalio import FONT
from adafruit_st7789 import ST7789
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
from adafruit_progressbar.horizontalprogressbar import HorizontalProgressBar
# HID keyboard
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from digitalio import DigitalInOut, Pull

# Config
from config import totp1, totp2, rowstart
UTC_OFFSET = 9   # time zone offset
DISPLAY_RATE = 1 # screen refresh rate

# RTC setup
i2c    = I2C(board.GP5, board.GP4)
ds3231 = adafruit_ds3231.DS3231(i2c)
rtc.set_time_source(ds3231)
def timebase(timetime):
    return (timetime - (UTC_OFFSET*3600)) // 30

# Display setup
release_displays()
tft_cs    = board.GP17
tft_dc    = board.GP16
spi_mosi  = board.GP19
spi_clk   = board.GP18
backlight = board.GP20
spi = SPI(spi_clk, spi_mosi)
display_bus = FourWire(spi, command=tft_dc, chip_select=tft_cs)
display = ST7789(
    display_bus, rotation=180, width=240, height=240, rowstart=rowstart, backlight_pin=backlight
)
center = display.width // 2
display.root_group = Group()

btn = DigitalInOut(board.GP3)
btn.switch_to_input(pull=Pull.UP)
totp = totp1 if btn.value else totp2
if 'bgimg' in totp:
    bitmap = OnDiskBitmap(totp['bgimg'])
    tile_grid = TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)
    display.root_group.append(tile_grid)

# Secret Code font by Matthew Welch
# http://www.squaregear.net/fonts/
font_code = bitmap_font.load_font("/secrcode_28.bdf")

name1 = label.Label(FONT, text=totp['label1'], color=0xFFFFFF, scale=2)
name1.anchor_point = (0.5, 0.0)
name1.anchored_position = (center, 10)
display.root_group.append(name1)
name2 = label.Label(FONT, text=totp['label2'], color=0xFFFFFF, scale=2)
name2.anchor_point = (0.5, 0.0)
name2.anchored_position = (center, 30)
display.root_group.append(name2)

code = label.Label(font_code, text="000000", color=0xFFFFFF)
code.anchor_point = (0.5, 0.0)
code.anchored_position = (center, 90)
display.root_group.append(code)

rtc_date = label.Label(FONT, text="----/--/--", scale=2)
rtc_date.anchor_point = (0.5, 0.5)
rtc_date.anchored_position = (center, 180)
display.root_group.append(rtc_date)

rtc_time = label.Label(FONT, text="--:--:--", scale=2)
rtc_time.anchor_point = (0.5, 0.5)
rtc_time.anchored_position = (center, 200)
display.root_group.append(rtc_time)

progress_bar = HorizontalProgressBar((55, 130), (130, 17), bar_color=0xFFFFFF, min_value=0, max_value=30)
display.root_group.append(progress_bar)

#HID setup
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)
code_sent = False

last_compute = last_update = time.time()
totp_code = generate_otp(timebase(last_compute), totp['key'])

while True:
    now = time.time()
    # update progress bar
    bar_value = now % 30
    progress_bar.value = bar_value
    if 25 < bar_value:
        progress_bar.bar_color = 0xFF0000
    elif 20 < bar_value:
        progress_bar.bar_color = 0xFFFF00
    else: 
        progress_bar.bar_color = 0x00FF00
    # update codes
    if bar_value < 0.5 and now - last_compute > 2:
        totp_code = generate_otp(timebase(now), totp['key'])
        last_compute = now
    # update display
    if now - last_update > DISPLAY_RATE:
        tt = time.localtime()
        rtc_date.text = "{:04}/{:02}/{:02}".format(tt.tm_year, tt.tm_mon, tt.tm_mday)
        rtc_time.text = "{:02}:{:02}:{:02}".format(tt.tm_hour, tt.tm_min, tt.tm_sec)
        last_update = now
        code.text = totp_code
    # send totp_code if button pressed
    if not btn.value:
        if not code_sent:
            code_sent = True
            keyboard_layout.write("%s\n" % totp_code)
    else:
        code_sent = False