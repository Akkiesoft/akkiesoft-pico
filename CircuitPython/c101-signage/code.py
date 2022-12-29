# Kokuda-land signage for Comiket101
# made with Breakout Garden

import board
from busio import I2C, SPI
from time import sleep
from adafruit_bme280 import basic as adafruit_bme280

# display
import displayio
from terminalio import FONT
from adafruit_st7789 import ST7789
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
from digitalio import DigitalInOut, Direction, Pull
import adafruit_imageload

btn = DigitalInOut(board.GP3)
btn.direction = Direction.INPUT
btn.pull = Pull.UP

# Display setup
displayio.release_displays()
tft_cs    = board.GP17
#CE1: 17
#CE0: 22
tft_dc    = board.GP16
spi_mosi  = board.GP19
spi_clk   = board.GP18
backlight = board.GP20
spi = SPI(spi_clk, spi_mosi)
while not spi.try_lock():
    pass
spi.configure(baudrate=24000000) # Configure SPI for 24MHz
spi.unlock()
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)
display = ST7789(
    display_bus, rotation=180, width=240, height=240, rowstart=80, backlight_pin=backlight
)
center = display.width // 2

i2c = I2C(board.GP5, board.GP4)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)

splash_bme = displayio.Group()
name2 = label.Label(FONT, text="", color=0xFFFFFF, scale=2)
splash_bme.append(name2)
name2.x = 5
name2.y = 10

splash = displayio.Group()
#bitmap = displayio.OnDiskBitmap("")
bitmap, palette = adafruit_imageload.load(
    "/c101.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette
)
grid = 0
tiles = bitmap.width / 240
tile_grid = displayio.TileGrid(
    bitmap,
    #pixel_shader=bitmap.pixel_shader,
    pixel_shader=palette,
    tile_width = 240,
    tile_height = 240
)
splash.append(tile_grid)
display.show(splash)

show_count = 0
show_mode = 0

def slide_picture():
    global grid
    grid += 1
    if tiles <= grid:
        grid = 0
    tile_grid[0] = grid

while True:
    if not btn.value:
        show_mode = 1 - show_mode
        if show_mode:
            # bme280 mode
            splash_bme.hidden = False
            splash.hidden = True
            display.show(splash_bme)
        else:
            splash_bme.hidden = True
            splash.hidden = False
            display.show(splash)
    if show_count == 60:
        if not show_mode:
            slide_picture()
        show_count = 0
    if show_mode:
        name2.text = "Temp: %0.1f C\nHumi: %0.1f %%\nPres: %0.1f hPa" % (bme280.temperature, bme280.humidity, bme280.pressure)
    show_count += 1
    sleep(0.1)