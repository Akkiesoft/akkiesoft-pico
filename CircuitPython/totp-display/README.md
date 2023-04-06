# TOTP表示機

## ブログ

* [Raspberry Pi PicoでTOTP表示機をつくりたい (1)](https://akkiesoft.hatenablog.jp/entry/20211205/1638635777)
* [Raspberry Pi PicoでTOTP表示機をつくりたい (2)](https://akkiesoft.hatenablog.jp/entry/20211209/1638976467)

## 必要な物品

* Raspberry Pi Pico もしくは Raspberry Pi Pico W
* [Breakout Garden Pack](https://shop.pimoroni.com/products/pico-breakout-garden-pack)
* いずれかのBreakout GardenのLCDモジュール
    * [1.3" SPI Colour Round LCD (240x240) Breakout](https://shop.pimoroni.com/products/1-3-spi-colour-round-lcd-240x240-breakout)
    * [1.3" SPI Colour Square LCD (240x240) Breakout](https://shop.pimoroni.com/products/1-3-spi-colour-lcd-240x240-breakout)
* RTCモジュールを使う場合、下記いずれか
    * [DS3231 RTCモジュール](https://www.switch-science.com/catalog/5335/)
        * [I2C Garden Extenders (pack of 3)](https://shop.pimoroni.com/products/garden-extender)
    * [RV3028 RTCモジュール](https://shop.pimoroni.com/products/rv3028-real-time-clock-rtc-breakout)
* ボタンとピンヘッダー2つ

## 必要なCircuitPythonライブラリ

* adafruit_bitmap_font
* adafruit_display_text
* adafruit_hashlib
* adafruit_hid
* adafruit_progressbar
* adafruit_st7789
* (DS3231 RTCモジュールを使用する場合)
    * adafruit_register
    * adafruit_ds3231
* (RV3028 RTCモジュールを使用する場合)
    * [pimoroni_circuitpython_adapter](https://github.com/pimoroni/circuitpython_adapter)
    * [i2cdevice](https://github.com/pimoroni/i2cdevice-python) (要修正)
    * [RV3028](https://github.com/pimoroni/rv3028-python)
    * ※[RV3028 RTCモジュールをCircuitPythonで動かす](https://akkiesoft.hatenablog.jp/entry/20220611/1654879661)を参考に
* (Pico WでNTPから時刻を取得する場合)
    * adafruit_ntp

## その他必要なもの

* secrcode_28.bdf
    * 元にしたスクリプトのページからProject Codeに移動して「Download Project Bundle」からダウンロード

## 元にしたスクリプト

[MacroPad 2FA TOTP Authentication Friend](https://learn.adafruit.com/macropad-2fa-totp-authentication-friend)