# Send mouse codes by web api.
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
from adafruit_hid.mouse import Mouse

indexhtml = """<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><meta charset="utf-8"><title>Web mouse cursor API</title><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous"><script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js" integrity="sha384-geWF76RCwLtnZ8qwWowPQNguL3RmwHVBC9FhGdlKrxdiJJigb/j/68SIy3Te4Bkz" crossorigin="anonymous"></script><script>function s(p){let url=location.href;if (url.slice(-1) != "/") { url = url + "/"; };fetch(url + "mouse/" + p).then(function(r){return r.text()}).then(function(t){document.getElementById('r').innerText=t;});}</script></head><body><main class="px-3 col-6 mx-auto text-center"><h1 class="mt-2">Web mouse cursor API</h1><div class="container"><div class="row"><button class="btn btn-primary mt-3 mb-3" onclick="s('up');">👆</button></div><div class="row d-flex justify-content-between"><button class="btn btn-primary col-5 mt-3 mb-3" onclick="s('left');">👈</button><button class="btn btn-primary col-5 mt-3 mb-3" onclick="s('right');">👉</button></div><div class="row"><button class="btn btn-primary col-12 mt-3 mb-3" onclick="s('down');">👇</button></div><div class="row d-flex justify-content-between"><button class="btn btn-primary col-5 mt-3 mb-3" onclick="s('scroll-up');">⤴</button><button class="btn btn-primary col-5 mt-3 mb-3" onclick="s('scroll-down');">⤵</button></div></div><div id="r" class="m-3"></div></main></body></html>"""

mouse = 0
while not mouse:
    try:
        mouse = Mouse(usb_hid.devices)
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
#print("MAC Address:", [hex(i) for i in eth.mac_address])
print("My IP address is:", eth.pretty_ip(eth.ip_address))

socket.set_interface(eth)
server = Server(socket)

@server.route("/")
def root(request: Request):
    print("GET /")
    return Response(request, indexhtml, content_type="text/html")

@server.route("/mouse/<direction>")
def move_mouse(request: Request, direction: str):
    print("GET /mouse/%s" % direction)
    if direction == "up":
        mouse.move(x=0, y=-20)
    elif direction == "down":
        mouse.move(x=0, y=20)
    elif direction == "left":
        mouse.move(x=-20, y=0)
    elif direction == "right":
        mouse.move(x=20, y=0)
    elif direction == "scroll-up":
        mouse.move(wheel=20)
    elif direction == "scroll-down":
        mouse.move(wheel=-20)
    else:
        return Response(request, "invalid parameter")
    return Response(request, "moved mouse cursor to %s side" % direction)

server.serve_forever(str(eth.pretty_ip(eth.ip_address)))