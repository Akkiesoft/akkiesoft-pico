# Network Test

from adafruit_requests import Session
import adafruit_ntp
from rtc import RTC
import time

# WIZNET5K
#from networks.akkie_wiznet5k import akkie_wiznet5k as network
#network = network()
# (OR you can change pin assigns)
#import board
#network = network(cs=board.GP9, sck=board.GP26, mosi=board.GP27, miso=board.GP8)

# Wi-Fi
from networks.akkie_wifi import akkie_wifi as network
ap_list = (
  ('SSID', 'PASSPHRASE'),
)

network = network(ap_list)

network.connect()

ntp = adafruit_ntp.NTP(network.pool, tz_offset=0, server="0.pool.ntp.org")
source = RTC()
source.datetime = ntp.datetime

url = "http://checkip.amazonaws.com/"
requests = Session(network.pool, network.ssl_context)
result = requests.get(url).text

now = time.localtime(time.time() + 3600 * 9)
print("%04i/%02i/%02i %02i:%02i:%02i" % (now[0], now[1], now[2], now[3], now[4], now[5]))
print(result)