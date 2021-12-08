# TOTP表示機

## ブログ

[Raspberry Pi PicoでTOTP表示機をつくりたい (1)](https://akkiesoft.hatenablog.jp/entry/20211205/1638635777)
[Raspberry Pi PicoでTOTP表示機をつくりたい (2)](https://akkiesoft.hatenablog.jp/entry/20211209/1638976467)

## 必要な物品

* Raspberry Pi Pico
* [Breakout Garden Pack](https://shop.pimoroni.com/products/pico-breakout-garden-pack)
* いずれかのBreakout GardenのLCDモジュール
    * [1.3" SPI Colour Round LCD (240x240) Breakout](https://shop.pimoroni.com/products/1-3-spi-colour-round-lcd-240x240-breakout)
    * [1.3" SPI Colour Square LCD (240x240) Breakout](https://shop.pimoroni.com/products/1-3-spi-colour-lcd-240x240-breakout)
* [DS3231 RTCモジュール](https://www.switch-science.com/catalog/5335/)
    * [I2C Garden Extenders (pack of 3)](https://shop.pimoroni.com/products/garden-extender)
* ボタンとピンヘッダー2つ

## 必要なCircuitPythonライブラリ

* adafruit_bitmap_font
* adafruit_display_text
* adafruit_ds3231
* adafruit_hashlib
* adafruit_hid
* adafruit_progressbar
* adafruit_register
* adafruit_st7789

## その他必要なもの

* secrcode_28.bdf
    * 元にしたスクリプトのページからProject Codeに移動して「Download Project Bundle」からダウンロード

## 元にしたスクリプト

[MacroPad 2FA TOTP Authentication Friend](https://learn.adafruit.com/macropad-2fa-totp-authentication-friend)