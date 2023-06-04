import time
import board
import pwmio
from digitalio import DigitalInOut, Direction

import mywifi
import mdns
from adafruit_httpserver.server import HTTPServer
from adafruit_httpserver.request import HTTPRequest
from adafruit_httpserver.response import HTTPResponse
from adafruit_httpserver.methods import HTTPMethod
from adafruit_httpserver.mime_type import MIMEType
from html import html

class Plarail:
    def __init__(self, forward, backward):
        self.gpio = [forward, backward]
        self.speed = float(0)
        self.direction = -1
        self.set_direction(0)

    def set_direction(self, direction):
        if direction == self.direction:
            return
        if 0 <= self.direction:
            self.pwm_a.deinit()
        self.pwm_a = pwmio.PWMOut(self.gpio[direction], variable_frequency=True)
        self.pwm_b = DigitalInOut(self.gpio[1 - direction])
        self.pwm_b.direction = Direction.OUTPUT
        self.pwm_b.value = 0
        self.direction = direction

    def power(self, command, brake = 0):
      self.command = command
      if self.speed == 0 and not brake:
          self.speed = 0.2
          self.__duty(self.speed)
      if self.speed < command:
          # print("speedup.")
          while self.speed < command:
              if self.command != command:
                  print("Command has been changed.")
                  break
              self.speed += 0.002
              self.__duty(self.speed)
              time.sleep(0.05)
      else:
          # print("slowdown.")
          while command < self.speed:
              if self.command != command:
                  print("Command has been changed.")
                  break
              if self.speed <= 0.15:
                  self.speed = 0
                  self.__duty(self.speed)
                  break
              if brake:
                  self.speed -= 0.002 * (brake - 0.3)
              else:
                  self.speed -= 0.002
              self.__duty(self.speed)
              time.sleep(0.05)

    def stop(self):
        self.pwm_a.duty_cycle = 0
        self.speed = 0

    def __duty(self, i):
        duty_cycle = int(0xFFFF * abs(i))
        print("duty: %s" % duty_cycle)
        self.pwm_a.duty_cycle = duty_cycle
        self.__set_freq(i)

    def __set_freq(self, s):
      if 0 <= s and s < 0.48:
        self.pwm_a.frequency = 1050
      if 0.48 <= s:
        self.pwm_a.frequency = 329 + int(s*20)

    def __set_freq_doremifa(self, s):
      if 0 <= s and s < 0.08:
        self.pwm_a.frequency = 349
      elif 0.08 <= s and s < 0.12:
        self.pwm_a.frequency = 392
      elif 0.12 <= s and s < 0.16:
        self.pwm_a.frequency = 440
      elif 0.16 <= s and s < 0.20:
        self.pwm_a.frequency = 466
      elif 0.20 <= s and s < 0.24:
        self.pwm_a.frequency = 523
      elif 0.24 <= s and s < 0.28:
        self.pwm_a.frequency = 587
      elif 0.28 <= s and s < 0.32:
        self.pwm_a.frequency = 622
      elif 0.32 <= s and s < 0.36:
        self.pwm_a.frequency = 698
      elif 0.36 <= s:
        self.pwm_a.frequency = 784

    def __set_freq_keikyu1000_siemens(self, s):
      if 0 <= s and s < 0.12:
        self.pwm_a.frequency = 590
      elif 0.12 <= s and s < 0.4:
        print(int(481 + s * 1430))
        self.pwm_a.frequency = int(481 + s * 1430)
      elif 0.4 <= s and s < 0.52:
        self.pwm_a.frequency = 1050
      else:
        self.pwm_a.frequency = 250

plarail = Plarail(board.GP2, board.GP3)

server = HTTPServer(mywifi.pool)
mdns = mdns.Server(mywifi.radio)
mdns.hostname = "plarail"

@server.route("/")
def root(request: HTTPRequest):
    with HTTPResponse(request, content_type=MIMEType.TYPE_HTML) as response:
        response.send(html())

@server.route("/EB")
def EB(request: HTTPRequest):
    with HTTPResponse(request, content_type=MIMEType.TYPE_HTML) as response:
        response.send("EB")
    plarail.stop()
@server.route("/B4")
def B4(request: HTTPRequest):
    with HTTPResponse(request, content_type=MIMEType.TYPE_HTML) as response:
        response.send("B4")
    plarail.power(0, brake=4)
@server.route("/B3")
def B3(request: HTTPRequest):
    with HTTPResponse(request, content_type=MIMEType.TYPE_HTML) as response:
        response.send("B3")
    plarail.power(0, brake=3)
@server.route("/B2")
def B2(request: HTTPRequest):
    with HTTPResponse(request, content_type=MIMEType.TYPE_HTML) as response:
        response.send("B2")
    plarail.power(0, brake=2)
@server.route("/B1")
def B1(request: HTTPRequest):
    with HTTPResponse(request, content_type=MIMEType.TYPE_HTML) as response:
        response.send("B1")
    plarail.power(0, brake=1)
@server.route("/-")
def NO(request: HTTPRequest):
    with HTTPResponse(request, content_type=MIMEType.TYPE_HTML) as response:
        response.send("-")
@server.route("/P1")
def P1(request: HTTPRequest):
    with HTTPResponse(request, content_type=MIMEType.TYPE_HTML) as response:
        response.send("P1")
    plarail.power(0.30)
@server.route("/P2")
def P2(request: HTTPRequest):
    with HTTPResponse(request, content_type=MIMEType.TYPE_HTML) as response:
        response.send("P2")
    plarail.power(0.34)
@server.route("/P3")
def P3(request: HTTPRequest):
    with HTTPResponse(request, content_type=MIMEType.TYPE_HTML) as response:
        response.send("P3")
    plarail.power(0.38)
@server.route("/P4")
def P4(request: HTTPRequest):
    with HTTPResponse(request, content_type=MIMEType.TYPE_HTML) as response:
        response.send("P4")
    plarail.power(0.42)

print("Starting server...")
try:
    server.start(str(mywifi.radio.ipv4_address))
    print("Listening on http://%s:80" % mywifi.radio.ipv4_address)
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
