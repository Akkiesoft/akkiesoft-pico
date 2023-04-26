# Current wattage usage monitor by the smart meter B-route service
# 2023 @Akkiesoft
#
# Based on: https://qiita.com/kanon700/items/d4df13d45c2a9d16b8b0

import sys
import board
import busio
import digitalio
import time
import broute_config

debug = broute_config.debug

# Display setup
import displayio
from terminalio import FONT
from adafruit_st7789 import ST7789
displayio.release_displays()
tft_cs    = board.GP17
#CE1: 17
#CE0: 22
tft_dc    = board.GP16
spi_mosi  = board.GP19
spi_clk   = board.GP18
backlight = board.GP20
spi = busio.SPI(spi_clk, spi_mosi)
while not spi.try_lock():
    pass
spi.configure(baudrate=24000000) # Configure SPI for 24MHz
spi.unlock()
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)
display = ST7789(
    display_bus, rotation=180, width=240, height=240, rowstart=80, backlight_pin=backlight
)

def readline_str():
    while not uart.in_waiting:
        pass
    r = uart.readline()
    if debug:
        print("receive:", str(r, 'utf-8').rstrip())
    return str(r, 'utf-8').rstrip()

def send_str(command, echoback=False, raw = False):
    send_command = command if raw else str.encode(command + "\r\n")
    if debug:
        print("send:", send_command)
    uart.write(send_command)
    if echoback:
        readline_str()
    result = readline_str()
    return result

# PANA authentication
def pana_auth():
    connected = False
    print("[PANA] Start PANA authentication.")

    # Set password
    send_str("SKSETPWD C %s" % broute_config.password, echoback=True)
    # Set ID
    send_str("SKSETRBID %s" % broute_config.id, echoback=True)
    # Set channel
    send_str("SKSREG S2 %s" % broute_config.channel, echoback=True)
    # Set pan ID
    send_str("SKSREG S3 %s" % broute_config.pan_id, echoback=True)
    # Start PANA authentication
    send_str("SKJOIN %s" % broute_config.address, echoback=True)

    while not connected:
        line = readline_str()
        if line.startswith("EVENT 24"):
            print("[PANA] Connection failed.")
            return False
        elif line.startswith("EVENT 25") :
            print("[PANA] Connection successfull.")
            connected = True
    return connected

# Open UART port
uart = busio.UART(board.GP0, board.GP1, baudrate=115200)

# Reset Wi-SUN module
reset = digitalio.DigitalInOut(board.GP15)
reset.direction = digitalio.Direction.OUTPUT
for i in range(1, 4):
    reset.value = i % 2
    time.sleep(0.1)

# Command to request current watts in use
echonetLiteFrame = b'\x10\x81\x00\x01\x05\xFF\x01\x02\x88\x01\x62\x01\xE7\x00'

pana_connected = False
while True:
    if not pana_connected:
        while not pana_connected:
            pana_connected = pana_auth()

    # Send command
    if debug:
        print("[echonetLiteFrame] Send command")
    result = send_str(
        str.encode("SKSENDTO 1 {0} 0E1A 1 0 {1:04X} ".format(broute_config.address, len(echonetLiteFrame))) + echonetLiteFrame,
        echoback=True, raw = True)
    if not result.startswith("EVENT 21"):
        print("[echonetLiteFrame] Failed to send command")
        print("[echonetLiteFrame]" + result) # TODO: OKじゃないのがのかを見たい
        time.sleep(5)
        continue
    readline_str() # OK

    received_data = readline_str()
    if received_data.startswith("ERXUDP"):
        cols = received_data.strip().split(' ')
        if len(cols) < 10:
            print("[echonetLiteFrame] Received data was corrupted. We will retry soon.")
            time.sleep(5)
            continue
        body = cols[-1]      # data body
        seoj = body[8:8+6]   # Source Echonet-lite ObJect: It sould be 028801(smart meter)
        esv  = body[20:20+2] # Echonet-lite SerVice: It sould be 72(response)
        if seoj == "028801" and esv == "72":
            epc = body[24:24+2] # Echonet-lite Property: It should be E7(Value of instantaneous power measurement)
            if epc == "E7":
                hexPower = body[-8:]
                intPower = int(hexPower, 16)
                print("[Current watts used] %s W" % intPower)
        else:
            print("[echonetLiteFrame] Received data was corrupted. We will retry soon.")
            time.sleep(5)
            continue
    else:
        print("[echonetLiteFrame] Cannot get ERXUDP data!")
        print("[PANA] Reconnect at next time.")
        # TODO 単にechonetLiteFrameの再送をすればいい気がする
        # pana_connected = False
        time.sleep(5)

    # Request every 10 minutes.
    print("sleep for 10 minutes.")
    time.sleep(600)