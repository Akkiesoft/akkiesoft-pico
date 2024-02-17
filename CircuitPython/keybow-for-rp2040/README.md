# Pimoroni Keybow & Keybow mini for RP2040

This script is for using Keybow & Keybow mini with Raspberry Pi Pico and CircuitPython. It can reduce boot time and power.

## Things necessary

* Raspberry Pi Pico ( https://www.raspberrypi.org/products/raspberry-pi-pico/ )
    * or other Pico compatible boards
* Keybow or Keybow mini
    * https://shop.pimoroni.com/products/keybow
    * https://shop.pimoroni.com/products/keybow-mini-3-key-macro-pad-kit
* CircuitPython ( https://circuitpython.org/ )
* adafruit_hid, adafruit_dotstar libraries from Adafruit_CircuitPython_Bundle ( https://github.com/adafruit/Adafruit_CircuitPython_Bundle )

## Wiring

* Reference
    * [Keybow pinout](https://pinout.xyz/pinout/keybow)
    * [Keybow mini pinout](https://pinout.xyz/pinout/keybow_mini)

| Raspberry Pi GPIO | Raspberry Pi Pico GPIO | Keybow Key | Keybow mini key |
| ----------------- | ---------------------- | ---------- | --------------- |
| GPIO17            | GP11                   | 1          | 1               |
| GPIO27            | GP12                   | 2          |                 |
| GPIO23            | GP13                   | 3          |                 |
| GPIO22            | GP14                   | 4          | 2               |
| GPIO24            | GP15                   | 5          |                 |
| GPIO5             | GP16                   | 6          |                 |
| GPIO6             | GP17                   | 7          | 3               |
| GPIO12            | GP18                   | 8          |                 |
| GPIO13            | GP19                   | 9          |                 |
| GPIO20            | GP20                   | 10         |                 |
| GPIO16            | GP21                   | 11         |                 |
| GPIO26            | GP22                   | 12         |                 |
| GPIO10(LED data)  | GP3                    |            |                 |
| GPIO11(LED clock) | GP2                    |            |                 |

## Files

* code.py: Main program
* config.py: Config file for key and led color assignment
    * sample-3keys-config.py: Sample for Keybow mini
    * sample-12keys-config.py: Sample for Keybow
* boot.py: (only for CircuitPython => 7.0.0) A program that disables usb msd.
    *  To enable usb msd, hold down 1-key while connecting the USB.

## blog

https://akkiesoft.hatenablog.jp/entry/20210815/1629001574

(Written in Japanese. Please use the translate service.)