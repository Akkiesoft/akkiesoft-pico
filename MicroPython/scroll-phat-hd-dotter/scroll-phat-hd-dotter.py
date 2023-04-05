# Scroll pHAT HD Dotter

# You'll need:
# Raspberry Pi Pico W
# Pimoroni Scroll pHAT HD


import config
import utime
import socket
import ujson
from machine import I2C, Pin
import is31fl3731

html = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<title>Dot Editor for Scroll pHAT HD and Pico W</title>
<script>
function toggle_pixel(e) {
    let x = e.cellIndex;
    let y = e.parentElement.rowIndex;
    var b, color;
    if (e.style.backgroundColor == '') {
        color = 'blue';
        b = 50;
    } else {
        color = '';
        b = 0;
    }
    fetch(`/led/${x}/${y}/${b}`)
        .then(function(r){ return r.text(); })
        .then(function(t){ e.style.backgroundColor = color; });
}
function scrollPhatTable() {
    var canvas = document.getElementById("canvas");
    let y = 7;
    let x = 17;
    for (var i = 0; i < y; i++) {
        var row = canvas.insertRow(-1);
        for (var j = 0; j < x; j++) {
            var cell = row.insertCell(-1);
            cell.onclick = function() { toggle_pixel(this); };
        }
    }
}
window.onload = function() { scrollPhatTable(); }
</script>
<style>
table {
  border-collapse: collapse;
  margin-bottom: 16px;
}
td {
  border: 1px solid gray;
  width: 32px;
  height: 32px;
  cursor: pointer;
}
</style>
</head>
<body>
<table id="canvas"></table>
<p>GET /led/[x(0-16)]/[y(0-6)]/[brightness(0-255)]</p>
</body>
</html>
"""

def scrollphathd_pixel(x, y, b):
    py = 6 - y
    if (x < 9):
        px = 8 - x
    else:
        px = x - 9
        py = y + 8
    display.pixel(py, px, b)

def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(config.ssid, config.password)
        while not sta_if.isconnected():
            print(".")
            utime.sleep(1)
            pass
    print('network config:', sta_if.ifconfig())

i2c = I2C(0, scl=Pin(5), sda=Pin(4))
display = is31fl3731.Matrix(i2c)

print("sleep for 5 seconds.")
utime.sleep(5)

do_connect()

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(1)

while True:
    cl, addr = s.accept()
    req = str(cl.recv(1024), "utf-8").split("\r\n")
    for l in req:
        if "GET" in l:
            path = l.split(" ")[1]
            break
    code = "200 OK"
    ct = "text/html"
    if path == "/":
        response = html
    elif path.startswith("/led"):
        path_split = path.split('/')
        x = int(path_split[2])
        y = int(path_split[3])
        b = int(path_split[4])
        if x < 0 or y < 0 or b < 0 or 16 < x or 6 < y or 255 < b:
            code = "400 Bad request"
            response = "any parameter out of range"
        else:
            scrollphathd_pixel(x, y, b)
            response = "%s(%s, %s)" % (b, x, y)
    else:
        code = "404 Not Found"
        response = "Not Found"

    cl.send('HTTP/1.0 %s\r\nContent-type: %s\r\n\r\n' % (code,ct))
    cl.send(response)
    cl.close()