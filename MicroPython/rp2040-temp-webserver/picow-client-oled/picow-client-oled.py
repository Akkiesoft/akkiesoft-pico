#!/usr/bin/env python3
# coding: UTF-8

from io import BytesIO
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import urllib.request
import json
import time

url = "http://192.168.100.2:5123/temp.json"

# Init SSD1306 OLED display
disp = Adafruit_SSD1306.SSD1306_128_64(rst=None)
disp.begin()
disp.clear()
disp.display()
width = disp.width
height = disp.height

image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
fpath = "/usr/share/fonts/MajorMonoDisplay-Regular.ttf"
font = ImageFont.truetype(fpath, 12)
draw.text((0,30), "temperature:\n          c", font=font, fill=255)

def get_picow():
    j = json.loads(urllib.request.urlopen(url).read())
    return (j["time"].replace(" ","\n"), j["temperature"])

while True:
    # Memo: 1-character == 9x15px
    (now, temp) = get_picow()
    draw.rectangle((0,0,128,29), outline=0, fill=0)
    draw.rectangle((0,45,81,60), outline=0, fill=0)
    draw.text((0,0), now, font=font, fill=255)
    draw.text((0,45), temp, font=font, fill=255)
    disp.image(image)
    disp.display()
    time.sleep(1)
