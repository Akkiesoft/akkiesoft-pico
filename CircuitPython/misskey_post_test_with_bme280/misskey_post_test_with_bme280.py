import board
from busio import I2C, SPI
from digitalio import DigitalInOut, Direction, Pull
# client
import adafruit_requests
# sensor
from adafruit_bme280 import basic as adafruit_bme280
# display
import displayio
from terminalio import FONT
from adafruit_st7789 import ST7789
from terminalio import FONT
from adafruit_display_text import label

# Following libraries are required:
#     adafruit_bme280
#     adafruit_display_text
#     adafruit_requests.mpy
#     adafruit_st7789.mpy


token = '<SET YOUR TOKEN>'
url = 'https://<YOUR MISSKEY INSTANCE>/api/notes/create'


btn = DigitalInOut(board.GP3)
btn.direction = Direction.INPUT
btn.pull = Pull.UP

i2c = I2C(board.GP5, board.GP4)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)

# Display setup(tft_cs = CE1:GP17 / CE0:GP22)
displayio.release_displays()
tft_cs    = board.GP17
tft_dc    = board.GP16
spi_mosi  = board.GP19
spi_clk   = board.GP18
backlight = board.GP20
spi = SPI(spi_clk, spi_mosi)
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)
display = ST7789(
    display_bus, rotation=180, width=240, height=240, rowstart=40, backlight_pin=backlight
)
center = display.width // 2
display.root_group = displayio.Group()
igyo = displayio.OnDiskBitmap("/igyo.bmp")
tile_grid = displayio.TileGrid(igyo, pixel_shader=igyo.pixel_shader)
display.root_group.append(tile_grid)
msg = label.Label(FONT, text="", color=0xFFFFFF, scale=2)
msg.anchor_point = (0.5, 0.5)
msg.anchored_position = (center, center)
msg.hidden = True
display.root_group.append(msg)

wifi = akkie_wifi(ap_list)

def post_data(text):
    wifi.connect()
    if not wifi.connected:
        return "Failed to post."
    requests = adafruit_requests.Session(wifi.pool, wifi.ssl_context)
    data = {
        "i": token,
        "text": text
    }
    response = requests.post(url, json=data)
    return "Post successfully."

pressed = False
import time
while True:
    if not btn.value:
        if not pressed:
            pressed = True
            temp = bme280.temperature
            fhot = "  :fuckinhot:" if 30 <= temp else ""
            data = (temp, fhot, bme280.humidity, bme280.pressure)
            tile_grid.hidden = True
            msg.hidden = False
            msg.text = """TEMP: %0.1f C%s
HUMI: %0.1f %%
PRES: %0.1f hPa""" % data
            text = """温度: %0.1f ℃%s
湿度: %0.1f %%
気圧: %0.1f hPa""" % data
            ret = post_data(text)
            msg.text = ret
            time.sleep(3)
            msg.hidden = True
            tile_grid.hidden = False
    else:
        pressed = False