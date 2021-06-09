import board
import busio
from digitalio import DigitalInOut
# for ESP32 SPI
import adafruit_requests
from adafruit_esp32spi import adafruit_esp32spi
# for SD card
import adafruit_sdcard
import storage


# ESP test
print("[ESP32 SPI hardware test]")

esp32_cs = DigitalInOut(board.GP7)
esp32_ready = DigitalInOut(board.GP10)
esp32_reset = DigitalInOut(board.GP11)
spi = busio.SPI(board.GP18, board.GP19, board.GP16)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

if esp.status == adafruit_esp32spi.WL_IDLE_STATUS:
    print("ESP32 found and in idle mode")
print("Firmware vers.", esp.firmware_version)
print("MAC addr:", [hex(i) for i in esp.MAC_address])
for ap in esp.scan_networks():
    print("\t%s\t\tRSSI: %d" % (str(ap['ssid'], 'utf-8'), ap['rssi']))

# SD test
print("\r\n[SD card test]")
try:
  print("Init SD...")
  cs = DigitalInOut(board.GP22)
  sdcard = adafruit_sdcard.SDCard(spi, cs)
  vfs = storage.VfsFat(sdcard)
  print("Mount SD...")
  storage.mount(vfs, "/sd")
  print("Write to file.")
  with open("/sd/test.txt", "w") as f:
    f.write("Hello world!\r\n")
  with open("/sd/test.txt", "r") as f:
    print("Read line from file:")
    print(f.readline())
except OSError:
  print("No SD card found. skip.")
