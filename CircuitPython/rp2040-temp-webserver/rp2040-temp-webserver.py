# Based on: https://learn.adafruit.com/pico-w-http-server-with-circuitpython/code-the-pico-w-http-server

import os
import time
import ipaddress
import wifi
import socketpool
import microcontroller
import json
import adafruit_ntp
import rtc
from adafruit_httpserver.server import HTTPServer
from adafruit_httpserver.request import HTTPRequest
from adafruit_httpserver.response import HTTPResponse
from adafruit_httpserver.methods import HTTPMethod
from adafruit_httpserver.mime_type import MIMEType

print("Connecting to WiFi")
ipv4 =  ipaddress.IPv4Address(os.getenv('IP_ADDRESS'))
netmask =  ipaddress.IPv4Address(os.getenv('NETMASK'))
gateway =  ipaddress.IPv4Address(os.getenv('GATEWAY'))
wifi.radio.set_ipv4_address(ipv4=ipv4,netmask=netmask,gateway=gateway)
wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))

print("Connected.")
pool = socketpool.SocketPool(wifi.radio)

print("Sync the time by NTP")
ntp = adafruit_ntp.NTP(pool, tz_offset=9, server=os.getenv('NTP_ADDRESS'))
r = rtc.RTC()
r.datetime = ntp.datetime
rtc.set_time_source(r)

server = HTTPServer(pool)

def webpage():
    return """<!DOCTYPE html><html><head><title>Pico W temperature server</title></head>
<body><h1>Pico W temperature server</h1>
<dl><dt>Timestamp</dt><dd id="ti"></dd><dt>Temperature</dt><dd id="te"></dd></dl>
<script>
function l(){
  fetch("/temp.json").then(function(r){return r.json()}).then(function(j){
    document.getElementById("ti").innerText=j["time"];
    document.getElementById("te").innerText=j["temp"];
  });
  setTimeout("l()", 1000);
}
l()
</script>
</body></html>
"""

@server.route("/")
def base(request: HTTPRequest):
    with HTTPResponse(request, content_type=MIMEType.TYPE_HTML) as response:
        response.send(f"{webpage()}")

@server.route("/temp.json")
def base(request: HTTPRequest):
    with HTTPResponse(request, content_type=MIMEType.TYPE_JSON) as response:
        response.send(json.dumps({
            "time": "%4d/%02d/%02d %2d:%02d:%02d" % (time.localtime()[0:6]),
            "temp": microcontroller.cpu.temperature
        }))

print("Starting server...")
try:
    server.start(str(wifi.radio.ipv4_address))
    print("Listening on http://%s:80" % wifi.radio.ipv4_address)
except OSError:
    time.sleep(5)
    print("Failed start server. Restarting...")
    microcontroller.reset()

while True:
    try:
        server.poll()
    except Exception as e:
        print(e)
        continue