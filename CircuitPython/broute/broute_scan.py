# Scan the smart meter
# 2023 @Akkiesoft
#
# Based on: https://qiita.com/kanon700/items/d4df13d45c2a9d16b8b0

import sys
import board
import busio
import digitalio
import time
import broute_config

scan_duration = 6
scan_retry_limit = 2

debug = broute_config.debug

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

# Open UART port
uart = busio.UART(board.GP0, board.GP1, baudrate=115200)

# Reset Wi-SUN module
reset = digitalio.DigitalInOut(board.GP15)
reset.direction = digitalio.Direction.OUTPUT
for i in range(1, 4):
    reset.value = i % 2
    time.sleep(0.1)

# Set the Password for the B-route authentication
send_str("SKSETPWD C %s" % broute_config.password, echoback=True)
# Set the ID for the B-route authentication
send_str("SKSETRBID %s" % broute_config.id, echoback=True)

print("Scanning", end='')
scan_try = 0
scan_result = {}
while not 'Channel' in scan_result:
    print('.', end='')
    if scan_retry_limit < scan_try:
        print("Scan retry limit exceeded.")
        sys.exit()
    send_str("SKSCAN 2 FFFFFFFF %s 0" % (scan_duration + scan_try))
    while True:
        line = readline_str()
        if line.startswith("  "):
            try:
                cols = line.strip().split(':')
                scan_result[cols[0]] = cols[1]
            except:
                pass
        elif line.startswith("EVENT 22"):
            break
    scan_try += 1
print("\n")

ipv6Addr = send_str("SKLL64 %s" % scan_result["Addr"], echoback=True)

print("----- Scan result", "-" * 33)
print("channel = %s" % scan_result["Channel"])
print("pan_id = %s" % scan_result["Pan ID"])
print("address = \"%s\"" % ipv6Addr)
print("-" * 51)