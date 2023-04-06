totp1 = {
    'label1': 'dokoka no',
    'label2': 'service',
    'key'   : 'MIKUMIKUMOFUMOFU',
    'bgimg' : ''
}

totp2 = {
    'label1': 'dokoka no',
    'label2': 'service2',
    'key'   : 'MIKUMOFUMIKUMOFU',
    'bgimg' : ''
}

# 240x240 rectangle lcd: rowstart=80
# 240x240 rounded lcd  : rowstart=40
rowstart = 40

# Sync time with NTP(for Pico W)
import os
time_sync = {
    'type': 'ntp',
    'ssid': os.getenv('CIRCUITPY_WIFI_SSID')
    'password': os.getenv('CIRCUITPY_WIFI_PASSWORD')
    'ntp_server': 'pool.ntp.org'
}

# Sync time with ds3231 RTC module
#time_sync = { 'type': 'ds3231' }

# Sync time with rv3231 RTC module
# * Probably not enough RAM since CircuitPython 8.0.0
#time_sync = { 'type': 'rv3028' }