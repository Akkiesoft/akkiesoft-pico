import os
import time
from adafruit_datetime import datetime
# RTC
import board
from pimoroni_circuitpython_adapter import not_SMBus as SMBus
from rv3028 import RV3028
import rtc
# Wi-Fi
import wifi
import socketpool
# NTP
import adafruit_ntp

# 1: Before using the rtc date/time
print("Local time(1): %s" % datetime.now())

# RTC setup
i2c = SMBus(SDA=board.GP4, SCL=board.GP5)
rv3028 = RV3028(i2c_dev=i2c)
rv3028.set_battery_switchover('level_switching_mode')

# 2: After using the rtc date/time
print("Local time(2): %s" % datetime.now())

# Wi-Fi setup
print("Wi-Fi connecting")
wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))
pool = socketpool.SocketPool(wifi.radio)

# NTP setup
print("Syncing RTC with NTP")
ntp = adafruit_ntp.NTP(pool, tz_offset=0, server="ntp.nict.jp")
t = ntp.datetime
rv3028.set_time_and_date((
    t.tm_year, t.tm_mon, t.tm_mday,
    t.tm_hour, t.tm_min, t.tm_sec))
rtc.set_time_source(rv3028)

# 3: After synced date/time of rtc with ntp
print("Local time(3): %s" % datetime.now())
print("NTP time     : %s" % datetime.fromtimestamp(time.mktime(ntp.datetime)))