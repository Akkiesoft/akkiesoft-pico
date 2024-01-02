# Send key codes(web meeting mute hotkeys) by web api. 		
# @Akkiesoft		
#
# What will you need device:
#   Raspberry Pi Pico + Wiznet W5500 module
#   or Wiznet W5500-EVB-Pico
#   or any other devices adafruit_wiznet5k supports.

# for W5500
import board
import busio
import digitalio
import time
from adafruit_wiznet5k.adafruit_wiznet5k import WIZNET5K
import adafruit_wiznet5k.adafruit_wiznet5k_socket as socket
# for Web Server
from adafruit_httpserver import Server, Request, Response
# for USB HID
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

indexhtml = """
<!DOCTYPE html><html lang="en"><head><meta name="viewport" content="width=device-width,initial-scale=1"><meta charset="utf-8"><title>Web Hotkey</title><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous"><script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js" integrity="sha384-geWF76RCwLtnZ8qwWowPQNguL3RmwHVBC9FhGdlKrxdiJJigb/j/68SIy3Te4Bkz" crossorigin="anonymous"></script><script>function s(p){let url=location.href;if (url.slice(-1) != "/") { url = url + "/"; };fetch(url + p).then(function(r){return r.text()}).then(function(t){document.getElementById('r').innerText=t;});}</script></head><body><div class="px-3 col-12 col-md-10 mx-auto text-center"><main><h1> Mute hotkeys for Web meeting</h1><div class="d-grid gap-2"><button class="btn btn-primary btn-lg m-3" onclick="s('slack');">Slack</button><button class="btn btn-primary btn-lg m-3" onclick="s('webex');">WebEx</button><button class="btn btn-primary btn-lg m-3" onclick="s('zoom');">Zoom</button></div><div id="r" class="m-3"></div></main></div></body></html>
"""

keyboard = 0
while not keyboard:
    try:
        keyboard = Keyboard(usb_hid.devices)
    except:
        pass
    time.sleep(1)

SPI_SCK = board.GP18
SPI_TX = board.GP19
SPI_RX = board.GP16
SPI_CSn = board.GP17
W5500_RSTn = board.GP20
cs = digitalio.DigitalInOut(SPI_CSn)
spi_bus = busio.SPI(SPI_SCK, MOSI=SPI_TX, MISO=SPI_RX)

# Reset W5500 first
ethernetRst = digitalio.DigitalInOut(W5500_RSTn)
ethernetRst.direction = digitalio.Direction.OUTPUT
ethernetRst.value = False
time.sleep(1)
ethernetRst.value = True

eth = WIZNET5K(spi_bus, cs, is_dhcp=True)
print("My IP address is:", eth.pretty_ip(eth.ip_address))

socket.set_interface(eth)
server = Server(socket)

@server.route("/")
def root(request: Request):
    print("GET /")
    return Response(request, indexhtml, content_type="text/html")

@server.route("/slack")
def slack(request: Request):
    keyboard.send(Keycode.M)
    return Response(request, "Slack mute hotkey sent.")

@server.route("/webex")
def webex(request: Request):
    keyboard.press(Keycode.GUI)
    keyboard.press(Keycode.LEFT_SHIFT)
    keyboard.send(Keycode.M)
    keyboard.release(Keycode.LEFT_SHIFT)
    keyboard.release(Keycode.GUI)
    return Response(request, "WebEx mute hotkey sent.")

@server.route("/zoom")
def zoom(request: Request):
    keyboard.press(Keycode.GUI)
    keyboard.press(Keycode.LEFT_SHIFT)
    keyboard.send(Keycode.A)
    keyboard.release(Keycode.LEFT_SHIFT)
    keyboard.release(Keycode.GUI)
    return Response(request, "Zoom mute hotkey sent.")

server.serve_forever(str(eth.pretty_ip(eth.ip_address)))