# BME280/680 temperature logger
# 2024 Akkiesoft / MIT License

# Following libraries are required:
#     adafruit_bme280 or adafruit_bme680
#     adafruit_httpserver
#     adafruit_ntp
#     adafruit_requests.mpy

import os
import sys
import rtc
import time
import microcontroller
import storage
import board
from busio import I2C
from digitalio import DigitalInOut, Direction, Pull

# networking
from akkie_wifi import akkie_wifi
from akkie_wifi_config import ap_list
from adafruit_httpserver import Server, Request, Response, JSONResponse
import mdns
import adafruit_ntp
import adafruit_requests

# set timezone
UTC_OFFSET = 9 * 3600
# select bme280 or bme680
seonsor_model = "bme280"

# misskey configuration
token = ''
url = ''

# button
btn = DigitalInOut(board.GP2)
btn.direction = Direction.INPUT
btn.pull = Pull.UP

# i2c sensor
i2c = I2C(board.GP5, board.GP4)
if seonsor_model == "bme280":
    from adafruit_bme280 import basic as adafruit_bme280
    sensor = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)
elif seonsor_model == "bme680":
    import adafruit_bme680
    sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c, address=0x76)
else:
    print("An invalid sensor type was specified.")
    sys.exit()

# init variables
indexhtml = """
<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><style>body {font-family:sans-serif;}</style></head><body><h2>🌡 <span id="t"></span> ℃</h2><h2>💧 <span id="h"></span> %</h2><h2>🌀 <span id="p"></span> hPa</h2><div><span id="date"></span> <span id="time"></span><div style="margin-top:1em;"><button id="btn" onclick="post();">Post to Misskey</button><span id="post_result"></span></div></body>
<script>
  function update_now() { fetch("/now.json").then(function(r){ return r.json(); }).then(function(j){ document.getElementById("t").innerText = j.temperature; document.getElementById("h").innerText = j.humidity; document.getElementById("p").innerText = j.pressure; document.getElementById("date").innerText = j.date; document.getElementById("time").innerText = j.time; }); setTimeout("update_now()", 3000); }
  function post() { let result = document.getElementById("post_result"); result.innerText = ""; let btn = document.getElementById("btn"); btn.disabled = true; fetch("/post", {method:"POST"}).then(function(r){ return r.text(); }).then(function(j){ result.innerText = j; btn.disabled = false; }); }
  window.onload = function(){ update_now(); }
</script></html>
"""
filename = ""
pressed = False
zero_flag = False

def get_data():
    try:
        now = time.localtime(time.time() + UTC_OFFSET)
        return {
            "date": "%02i/%02i/%02i" % (now[0], now[1], now[2]),
            "time": "%02i:%02i:%02i" % (now[3], now[4], now[5]),
            "filesystem_logging_mode": fs_programmable_mode,
            "temperature": round(sensor.temperature, 2),
            "humidity": round(sensor.humidity, 2),
            "pressure": round(sensor.pressure, 2)
        }
    except Exception as e:
        print("failed to get sensor data: %s" % e)

def get_filename(now, filename):
    filename_new = "/%02i%02i%02i.csv" % (now[0], now[1], now[2])
    if filename != filename_new:
        # 起動直後もしくは日付が変わったか
        filename = filename_new
        try:
            os.stat(filename)
        except OSError:
            # ファイルがないので新しいファイルを作る
            write_line(filename, 'Date,Time,Temperature,Humidity,Pressure')
    return filename

def write_line(filename, line):
    try:
        with open(filename, 'a') as f:
            f.write("%s\n" % line)
    except Exception as e:
        print("Failed to write text to file: %s" % e)

def record_log(filename):
    try:
        data = get_data()
        row = "%s,%s,%s,%s,%s" % (data["date"], data["time"], data["temperature"], data["humidity"], data["pressure"])
        print(row)
        if not fs_programmable_mode:
            write_line(filename, row)
    except Exception as e:
        print("failed to record sensor data: %s" % e)

try:
    fs_programmable_mode = storage.getmount("/").readonly
    print("fs_programmable_mode is %s" % fs_programmable_mode)

    wifi = akkie_wifi(ap_list, hostname="temp-logger")
    wifi.connect()
    requests = adafruit_requests.Session(wifi.pool, wifi.ssl_context)
    server = Server(wifi.pool)
    print(str(wifi.ipv4_address))
    ntp = adafruit_ntp.NTP(wifi.pool, tz_offset=0, server="ntp.nict.jp")
    source = rtc.RTC()
    source.datetime = ntp.datetime
    now = time.localtime(time.time() + UTC_OFFSET)
    filename = get_filename(now, filename)
except Exception as e:
    print("(network) %s" % e)
    print("Resetting in 10 seconds.")
    time.sleep(10)
    # ハードリセット
    microcontroller.reset()

@server.route("/")
def root(request: Request):
    return Response(request, indexhtml, content_type="text/html")

@server.route("/now.json")
def now(request: Request):
    return JSONResponse(request, get_data())

@server.route("/today.csv")
def csv_download(request: Request):
    if fs_programmable_mode:
        result = "Boot mode is programmable. To access this URL, please restart in logging mode."
    else:
        with open(filename) as f:
            result = f.read()
    return Response(request, result, content_type="text/plain")

@server.route("/post", "POST")
def post_data(request: Request):
    data = get_data()
    send_data = {
        "i": token,
        "text": """気温: %0.1f C
湿度: %0.1f %%
気圧: %0.1f hPa
(%s %s)""" % (data["temperature"], data["humidity"], data["pressure"], data["date"], data["time"])
    }
    response = requests.post(url, json=send_data)
    return Response(request, "OK")

server.start(str(wifi.ipv4_address), port=80)

while True:
    try:
        server.poll()
    except:
        pass

    try:
        # Recording
        now = time.localtime(time.time() + UTC_OFFSET)
        if now.tm_sec == 0:
            if not zero_flag:
                zero_flag = True
                filename = get_filename(now, filename)
                record_log(filename)
        else:
            if zero_flag:
                zero_flag = False

        if not btn.value:
            if not pressed:
                pressed = True
        else:
            pressed = False
        time.sleep(0.1)
    except Exception as e:
        try:
            print("(mainloop) %s" % e)
            write_line(filename, "%s" % e)
        except:
            # これすらエラーになる分はどうしようもないのでパス
            pass
        print("Resetting in 10 seconds.")
        time.sleep(10)
        # ハードリセット
        microcontroller.reset()