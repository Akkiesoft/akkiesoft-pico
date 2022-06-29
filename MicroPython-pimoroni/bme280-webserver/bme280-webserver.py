import config
import time
import socket
import ujson
from breakout_bme280 import BreakoutBME280,FILTER_COEFF_OFF, STANDBY_TIME_0_5_MS, OVERSAMPLING_2X, OVERSAMPLING_4X, OVERSAMPLING_8X, NORMAL_MODE
from pimoroni_i2c import PimoroniI2C

html = """<!DOCTYPE html><html><head><title>BME280 test</title></head>
<body><h1>BME280 test</h1>
<dl><dt>Temperature</dt><dd id="t"></dd><dt>Humidity</dt><dd id="h"></dd><dt>Pressure</dt><dd id="p"></dd></dl>
<script>
function l(){
  fetch("/temp.json").then(function(r){return r.json()}).then(function(j){
    document.getElementById("t").innerText=j["temp"];
    document.getElementById("h").innerText=j["humidity"];
    document.getElementById("p").innerText=j["pressure"];
  });
  setTimeout("l()", 1000);
}
l()
</script>
</body></html>
"""

def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(config.ssid, config.password)
        while not sta_if.isconnected():
            print(".")
            time.sleep(1)
            pass
    print('network config:', sta_if.ifconfig())

do_connect()

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(1)

PINS_BREAKOUT_GARDEN = {"sda": 4, "scl": 5}
i2c = PimoroniI2C(**PINS_BREAKOUT_GARDEN)
bme = BreakoutBME280(i2c)
bme.configure(FILTER_COEFF_OFF, STANDBY_TIME_0_5_MS, OVERSAMPLING_8X, OVERSAMPLING_4X, OVERSAMPLING_2X, NORMAL_MODE)

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
    elif path == "/temp.json":
        temperature,pressure,humidity = bme.read()
        response = ujson.dumps({
            "temp": temperature,
            "humidity": humidity,
            "pressure": pressure / 100
        })
        ct = "application/json"
    else:
        code = "404 Not Found"
        response = "Not Found"

    cl.send('HTTP/1.0 %s\r\nContent-type: %s\r\n\r\n' % (code,ct))
    cl.send(response)
    cl.close()