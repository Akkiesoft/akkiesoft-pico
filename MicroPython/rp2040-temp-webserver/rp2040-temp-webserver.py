import config
import utime
import socket
import ujson

html = """<!DOCTYPE html><html><head><title>Pico W temperature server</title></head>
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

print("sleep for 10 seconds.")
utime.sleep(10)

do_connect()

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(1)

# https://github.com/raspberrypi/pico-micropython-examples/blob/master/adc/temperature.py
sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)

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
        reading = sensor_temp.read_u16() * conversion_factor
        temperature = 27 - (reading - 0.706)/0.001721
        now = utime.localtime()
        response = ujson.dumps({
            "time": "%4d/%02d/%02d %2d:%02d:%02d" % (now[0:6]),
            "temp": temperature
        })
        ct = "application/json"
    else:
        code = "404 Not Found"
        response = "Not Found"

    cl.send('HTTP/1.0 %s\r\nContent-type: %s\r\n\r\n' % (code,ct))
    cl.send(response)
    cl.close()