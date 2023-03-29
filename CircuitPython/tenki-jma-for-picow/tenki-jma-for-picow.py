# Tenki-jma for Pick Inky Pack on Pico W
# 2022 @Akkiesoft
# MIT License
# Based on my script for RPi: 
#   https://github.com/Akkiesoft/RPi-tools/blob/master/scripts/tenki/tenki_jma.py

# What you'll need:
# * Raspberry Pi Pico W
# * Pico Inky Pack( https://shop.pimoroni.com/products/pico-inky-pack )
# * ToshibaSat_8x16 font( https://int10h.org/oldschool-pc-fonts/fontlist/ )
#    * You'll need to convert otb to bdf with FontForge yourself

# System/Wi-Fi
import os
from time import localtime
import wifi
import socketpool
from json import loads as json_loads
# HTTP(S)  client
import ssl
import adafruit_requests
# NTP
import adafruit_ntp
import rtc
# Inky
import board
from busio import SPI
from digitalio import DigitalInOut, Direction, Pull
import displayio
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
import adafruit_uc8151d

# 天気リスト(3つまで)
weather_list = [
    {
        # エリアコード: Kanagawa
        'area_code': "140000",
        # サブエリアコード: East
        'area_sub_code': "140010",
        # 市町村コード: Yokohama-shi
        'area_city_code': "46106",
        # Label
        'area_label': "Yokohama-shi"
    },
    {
        # エリアコード: Kushiro
        'area_code': "014100",
        # サブエリアコード: Nemuro
        'area_sub_code': "014010",
        # 市町村コード: Nemuro-shi
        'area_city_code': "18273",
        # Label
        'area_label': "Nemuro-shi"
    },
]
startup_weather = 0

# -----

displayio.release_displays()

# 天気コードをアイコンに変えるためのやつ
# 0: 晴れ, 1: 曇り, 2: 雨, 3: 雪
weather_codes = {100: 0, 101: 0, 102: 2, 103: 2, 104: 3, 105: 3, 106: 2, 107: 2, 108: 2, 110: 0, 111: 0, 112: 2, 113: 2, 114: 2, 115: 3, 116: 3, 117: 3, 118: 2, 119: 2, 120: 2, 121: 2, 122: 2, 123: 0, 124: 0, 125: 2, 126: 2, 127: 2, 128: 2, 130: 0, 131: 0, 132: 0, 140: 2, 160: 3, 170: 3, 181: 3, 200: 1, 201: 1, 202: 2, 203: 2, 204: 3, 205: 3, 206: 2, 207: 2, 208: 2, 209: 1, 210: 1, 211: 1, 212: 2, 213: 2, 214: 2, 215: 3, 216: 3, 217: 3, 218: 2, 219: 2, 220: 2, 221: 2, 222: 2, 223: 1, 224: 2, 225: 2, 226: 2, 228: 3, 229: 3, 230: 3, 231: 1, 240: 2, 250: 3, 260: 3, 270: 3, 281: 3, 300: 2, 301: 2, 302: 2, 303: 3, 304: 2, 306: 2, 308: 2, 309: 3, 311: 2, 313: 2, 314: 3, 315: 3, 316: 2, 317: 2, 320: 2, 321: 2, 322: 3, 323: 2, 324: 2, 325: 2, 326: 3, 327: 3, 328: 2, 329: 2, 340: 3, 350: 2, 361: 3, 371: 3, 400: 3, 401: 3, 402: 3, 403: 3, 405: 3, 406: 3, 407: 3, 409: 3, 411: 3, 413: 3, 414: 3, 420: 3, 421: 3, 422: 3, 423: 3, 425: 3, 426: 3, 427: 3, 450: 3}
# 天気アイコン
statuses = ['sunny', 'cloudy', 'rain', 'snow']

# Init Pico Inky Pack
# ( https://forums.adafruit.com/viewtopic.php?p=952021&sid=11b380a8ffb1262bd009b3ab04878767#p952021 )
spi = SPI(clock=board.GP18, MOSI=board.GP19, MISO=board.GP16)
display_bus = displayio.FourWire(
    spi,
    command=board.GP20,
    chip_select=board.GP17,
    reset=board.GP21,
    baudrate=1000000
)
display = adafruit_uc8151d.UC8151D(
    display_bus,
    width=296,
    height=128,
    rotation=270,
    black_bits_inverted=False,
    color_bits_inverted=False,
    grayscale=True,
    refresh_time=1
)
display.root_group = displayio.Group()

print("Connecting to Wi-Fi...")
wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))
print("Connected.")
pool = socketpool.SocketPool(wifi.radio)
# to DISABLE to verifying ssl certs
# https://github.com/adafruit/circuitpython/issues/7656
ssl_context = ssl.create_default_context()
ssl_context.load_verify_locations(cadata="")
requests = adafruit_requests.Session(pool, ssl_context)

ntp_addr = os.getenv('NTP_ADDRESS')
if ntp_addr:
    print("Get the time from NTP...")
    ntp = adafruit_ntp.NTP(pool, tz_offset=9, server=os.getenv('NTP_ADDRESS'))
    r = rtc.RTC()
    r.datetime = ntp.datetime
    rtc.set_time_source(r)

# -----

def show_forecast(display, w):
    global label_title, label_temp
    print("Get %s forecast" % w['area_label'])
    # 夜の回は明日の天気を出したい
    if 20 <= localtime().tm_hour:
      when = "tommorow"
      day = 1
    else:
      when = "today"
      day = 0

    # Get forecast data
    url = "https://www.jma.go.jp/bosai/forecast/data/forecast/%s.json" % w['area_code']
    response = requests.get(url)
    data = json_loads(response.text)
    response.close()
    for i in data:
      for j in i['timeSeries']:
        # 出力順序は変わらないと信じてるけど信じてないので必要なさそうな回はパス
        if 4 < len(j['timeDefines']):
          continue
        # 使えそうな回はareasでループ
        for area in j["areas"]:
          # 今日明日の天気が含まれる回。発表元と発表時刻はここで見ることにする
          if area['area']['code'] == w['area_sub_code']:
            if "weatherCodes" in area:
              forecast_date = i['reportDatetime'].replace('T', ' ').replace('-','/').split(':00+')[0]
              weather_code = weather_codes[int(area["weatherCodes"][day])]
              status = statuses[weather_code]
          # 今日明日の気温が含まれる回
          if area['area']['code'] == w['area_city_code']:
            if "temps" in area:
              temp_max = area["temps"][1]
              # 夜は1セットしかないので固定でOK
              temp_min = "-" if area["temps"][0] == area["temps"][1] else area["temps"][0]
    title = "Weather forecast for %s\n%s (%s)" % (when, w['area_label'], forecast_date)
    temp = "Max %sC / Min %sC" % (temp_max, temp_min)
    print(title)
    print(status)
    print(temp)
    if len(display.root_group) == 4:
        display.root_group.pop()
    bmp_forecast = displayio.OnDiskBitmap("/tenki-img/%s.bmp" % status)
    forecast = displayio.TileGrid(bmp_forecast, pixel_shader=bmp_forecast.pixel_shader, x=40, y=50)
    display.root_group.append(forecast)
    label_title.text = title
    label_temp.text = temp
    print("Waiting %s seconds until e-paper can be updated" % int(display.time_to_refresh))
    display.refresh()
    print("Please wait for %s seconds for e-paper to be ready for update" % int(display.time_to_refresh))

# Draw to Pico Inky Pack
font = bitmap_font.load_font("ToshibaSat_8x16.bdf")
label_title = label.Label(font, text="", color=0xFFFFFF, x=5, y=10)
display.root_group.append(label_title)
label_temp = label.Label(font, text="", color=0xFFFFFF, x=30, y=115)
display.root_group.append(label_temp)
bmp_mi = displayio.OnDiskBitmap("/tenki-img/miku.bmp")
mi = displayio.TileGrid(bmp_mi, pixel_shader=bmp_mi.pixel_shader, x=175, y=51)
display.root_group.append(mi)

if not startup_weather is None:
    show_forecast(display, weather_list[startup_weather])

# Buttons
buttons = [
    DigitalInOut(board.GP12),
    DigitalInOut(board.GP13),
    DigitalInOut(board.GP14)
]
for b in buttons:
    b.switch_to_input(pull=Pull.UP)

# LED
led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT

while True:
    led.value = 1 if display.time_to_refresh else 0
    for i,b in enumerate(buttons):
        if not b.value and not display.time_to_refresh:
            if len(weather_list) <= i:
                continue
            show_forecast(display, weather_list[i])