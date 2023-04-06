# RTC
import rtc
import board
from busio import I2C
import adafruit_ds3231
# Wi-Fi
import wifi
import socketpool
# NTP
import adafruit_ntp

# RTC setup
i2c = I2C(board.GP5, board.GP4)
ds3231 = adafruit_ds3231.DS3231(i2c)

# Wi-Fi setup
print("Wi-Fi connecting")
wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))
pool = socketpool.SocketPool(wifi.radio)

# NTP setup
print("Syncing RTC with NTP")
ntp = adafruit_ntp.NTP(pool, tz_offset=0, server=time_sync['ntp_server'])
ds3231.datetime = ntp.datetime

print(ds3231.datetime)