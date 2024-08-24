# below libralies are required:
#     adafruit_wiznet5k
#     adafruit_onewire
#     adafruit_ds18x20.mpy
#     adafruit_displayio_ssd1306.mpy
#     adafruit_display_text

import board
import busio
import digitalio
import time
import json
import struct
# Ethernet
from adafruit_wiznet5k.adafruit_wiznet5k import WIZNET5K
from adafruit_wiznet5k.adafruit_wiznet5k_socket import socket
# 1-wire
from adafruit_onewire.bus import OneWireBus
import adafruit_ds18x20
# OLED
import displayio
import adafruit_displayio_ssd1306
from adafruit_display_text import label
from terminalio import FONT

SPI1_SCK = board.GP2
SPI1_TX = board.GP3
SPI1_RX = board.GP0
SPI1_CSn = board.GP1
W5500_RSTn = board.GP7
ONE_WIRE = board.GP6
I2C_SDA = board.GP4
I2C_SCL = board.GP5

zabbix_server = ""

# Setup your network configuration below
# random MAC, later should change this value on your vendor ID
MY_MAC = (0x00, 0x01, 0x02, 0x03, 0x04, 0x05)
USE_DHCP = True
#IP_ADDRESS = (192, 168, 0, 111)
#SUBNET_MASK = (255, 255, 0, 0)
#GATEWAY_ADDRESS = (192, 168, 0, 1)
#DNS_SERVER = (8, 8, 8, 8)


def zabbix_send(ip, data, port=10051, timeout=5):
    data_len = struct.pack('<Q', len(data))
    http_request = b'ZBXD\x01' + data_len + data

    print("Sending data...")
    host_address = (ip, port)
    client_sock = socket()
    client_sock.settimeout(timeout)
    client_sock.sendto(http_request, host_address)

    result = b''
    while True:
        data = client_sock.recv(512)
        if len(data) <= 0:
            break
        result += data
    client_sock.close()
    print(result.decode('utf-8'))


# Init W5500

# Reset W5500 first
ethernetRst = digitalio.DigitalInOut(W5500_RSTn)
ethernetRst.direction = digitalio.Direction.OUTPUT
ethernetRst.value = False
time.sleep(1)
ethernetRst.value = True

spi_bus = busio.SPI(SPI1_SCK, MOSI=SPI1_TX, MISO=SPI1_RX)
cs = digitalio.DigitalInOut(SPI1_CSn)

eth = WIZNET5K(spi_bus, cs, mac=MY_MAC, is_dhcp=USE_DHCP)
if not USE_DHCP:
    eth.ifconfig = (IP_ADDRESS, SUBNET_MASK, GATEWAY_ADDRESS, DNS_SERVER)

my_ip = eth.pretty_ip(eth.ip_address)
print("Chip Version:", eth.chip)
print("MAC Address:", [hex(i) for i in eth.mac_address])
print("My IP address is:", my_ip)


# Init 1-wire
ow_bus = OneWireBus(ONE_WIRE)
devices = ow_bus.scan()
ds18b20 = adafruit_ds18x20.DS18X20(ow_bus, devices[0])


# Init OLED
displayio.release_displays()
i2c = busio.I2C(I2C_SCL, I2C_SDA)
display_bus = displayio.I2CDisplay(i2c, device_address=0x3c)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=32)
display.root_group = displayio.Group()
splash = display.root_group
text_myip = label.Label(FONT, text="IP: %s" % my_ip, color=0xFFFFFF, x=0, y=4)
splash.append(text_myip)
text_temp = label.Label(FONT, text="Temp: ", color=0xFFFFFF, x=0, y=20)
splash.append(text_temp)

while True:
    temperature = '{0:0.3f}'.format(ds18b20.temperature)
    text_temp.text = "Temp: %s C" % (temperature)
    if time.time() % 60 == 0 and zabbix_server:
        data = json.dumps({
            "request":"sender data",
            "data":[
                {"host":"pico-w5500","key":"ds18b20.temp","value":temperature}
            ]
        })
        zabbix_send(zabbix_server, data)
    time.sleep(1)