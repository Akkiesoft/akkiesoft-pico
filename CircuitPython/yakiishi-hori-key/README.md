# 焼石掘りキー (Stone dig key)

This is example of using the Raspberry Pi Pico as macro keyboard (or mouse).

When short the D2 pin and GND pin by the jumper wire, the Raspberry Pi Pico sends "press left button of the mouse". Then send "push a key" and "push d key" repeatly. It's useful to digging the stone that is made from stone making machine in the Minecraft's world. To stop the sending mouse and key codes, remove the jumper wire.

## Demo video

* with RPi Pico

[![](https://img.youtube.com/vi/kF1bkdniwUo/0.jpg)](https://www.youtube.com/watch?v=kF1bkdniwUo)

* with Pimoroni Tiny2040

[![](https://img.youtube.com/vi/P5iPPrDTLQ8/0.jpg)](https://www.youtube.com/watch?v=P5iPPrDTLQ8)

## Things necessary

* Raspberry Pi Pico ( https://www.raspberrypi.org/products/raspberry-pi-pico/ )
    * or Pimoroni Tiny2040 ( https://shop.pimoroni.com/products/tiny-2040 )
    * or other RP2040 boards
* CircuitPython ( https://circuitpython.org/ )
* adafruit_hid library from Adafruit_CircuitPython_Bundle ( https://github.com/adafruit/Adafruit_CircuitPython_Bundle )
* jumper wire

## Files

* code.py: Main program
* boot.py: (only for CircuitPython => 7.0.0) A program that disables usb msd.
    *  To enable usb msd, hold down 1-key while connecting the USB.

## blog

https://akkiesoft.hatenablog.jp/entry/20210523/1621778666

(Written in Japanese. Please use the translate service.)