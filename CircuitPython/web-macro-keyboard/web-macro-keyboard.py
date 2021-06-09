# Send key codes(web meeting mute hotkeys) by web api. 		
# @Akkiesoft		

# Used devices:		
#   Raspberry Pi Pico		
#   Pimoroni Pico Wireless Pack		
#     https://shop.pimoroni.com/products/pico-wireless-pack

import board
import busio
from digitalio import DigitalInOut
# for Web Server
from adafruit_wsgi.wsgi_app import WSGIApp
# for ESP32 SPI
import adafruit_requests
from adafruit_esp32spi import adafruit_esp32spi
import adafruit_esp32spi.adafruit_esp32spi_wsgiserver as server
import adafruit_esp32spi.adafruit_esp32spi_wifimanager as wifimanager
# for USB HID
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

keyboard=Keyboard(usb_hid.devices)

esp32_cs = DigitalInOut(board.GP7)
esp32_ready = DigitalInOut(board.GP10)
esp32_reset = DigitalInOut(board.GP11)
spi = busio.SPI(board.GP18, board.GP19, board.GP16)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)
wifi = wifimanager.ESPSPI_WiFiManager(esp, secrets)
wifi.connect()

print("open this IP in your browser: ", esp.pretty_ip(esp.ip_address))

status = {
  200: "200 OK",
  404: "404 Not Found",
  405: "405 Method Not Allowed"
}
content_type = {
  "html": "text/html",
  "text": "text/plain"
}

indexhtml = """
<!DOCTYPE html><html lang="en"><head><meta name="viewport" content="width=device-width,initial-scale=1"><meta charset="utf-8"><title>Web Hotkey</title><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-+0n0xVW2eSR5OomGNYDnhzAbDsOXxcvSN1TPprVMTNDbiYZCxYbOOl7+AMvyTG2x" crossorigin="anonymous"><script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/js/bootstrap.bundle.min.js" integrity="sha384-gtEjrD/SeCtmISkJkNUaaKMoLD0//ElJ19smozuHV6z3Iehds+3Ulb9Bn9Plx0x4" crossorigin="anonymous"></script><script>function s(p){fetch(p).then(function(r){return r.text()}).then(function(t){document.getElementById('r').innerText=t;});}</script></head><body><div class="px-3 col-12 col-md-10 mx-auto text-center"><main><h1> Mute hotkeys for Web meeting</h1><div class="d-grid gap-2"><button class="btn btn-primary btn-lg m-3" onclick="s('/slack');">Slack</button><button class="btn btn-primary btn-lg m-3" onclick="s('/webex');">WebEx</button><button class="btn btn-primary btn-lg m-3" onclick="s('/zoom');">Zoom</button></div><div id="r" class="m-3"></div></main></div></body></html>
"""

class SimpleWSGIApplication:
    def __init__(self):
        self._listeners = {}
        self._start_response = None

    def __call__(self, environ, start_response):
        self._start_response = start_response
        path = environ["PATH_INFO"]

        # Method not allowed except GET
        if environ["REQUEST_METHOD"] is not 'GET':
          status_code = 405
          resp_data = "Method Not Allowed"
        # define urls.
        elif path == "/":
          status_code = 200
          filetype = "html"
          resp_data = indexhtml
        elif path == "/slack":
          status_code = 200
          filetype = "text"
          keyboard.send(Keycode.M)
          resp_data = "Slack mute hotkey sent."
        elif path == "/webex":
          status_code = 200
          filetype = "text"
          keyboard.press(Keycode.GUI)
          keyboard.press(Keycode.LEFT_SHIFT)
          keyboard.send(Keycode.M)
          keyboard.release(Keycode.LEFT_SHIFT)
          keyboard.release(Keycode.GUI)
          resp_data = "WebEx mute hotkey sent."
        elif path == "/zoom":
          status_code = 200
          filetype = "text"
          keyboard.press(Keycode.GUI)
          keyboard.press(Keycode.LEFT_SHIFT)
          keyboard.send(Keycode.A)
          keyboard.release(Keycode.LEFT_SHIFT)
          keyboard.release(Keycode.GUI)
          resp_data = "Zoom mute hotkey sent."
        else:
          status_code = 404
          resp_data = "Not Found."

        # show log
        length = len(resp_data)
        print('"%s %s %s" %i %i' % (
          environ["REQUEST_METHOD"],
          environ["PATH_INFO"],
          environ["SERVER_PROTOCOL"],
          status_code,
          length))

        headers = [("Content-Type", content_type[filetype]), ("Content-Length", length)]
        self._start_response(status[status_code], headers)
        return resp_data

server.set_interface(esp)
wsgiServer = server.WSGIServer(80, application=SimpleWSGIApplication())
wsgiServer.start()
while True:
    # Our main loop where we have the server poll for incoming requests
    try:
        wsgiServer.update_poll()
        # Could do any other background tasks here, like reading sensors
    except (ValueError, RuntimeError) as e:
        print("Failed to update server, restarting ESP32\n", e)
        wifi.reset()
        continue
