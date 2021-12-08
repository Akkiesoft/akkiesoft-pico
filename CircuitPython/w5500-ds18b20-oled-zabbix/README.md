# W5500有線LANモジュールでLANに接続してDS18B20温度センサーの温度をSSD1306 OLEDディスプレイに表示したりZabbixに送るやつ

## ブログ

[Raspberry Pi Picoで1-Wireの温度センサーを使いつつZabbixに送りつける](https://akkiesoft.hatenablog.jp/entry/20211210/1639062000)

## 必要な物品

* Raspberry Pi Pico
* DS18B20センサー
* 4.7KΩ抵抗
* W5500有線LANモジュール
* SSD1306 OLEDディスプレイモジュール
* 配線するケーブル

## 必要なCircuitPythonライブラリ

* adafruit_wiznet5k
* adafruit_onewire
* adafruit_ds18x20.mpy
* adafruit_displayio_ssd1306.mpy
* adafruit_display_text
