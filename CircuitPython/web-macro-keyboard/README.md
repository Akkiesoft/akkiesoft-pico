# Web macro keyboard

(TBW)

## Demo

[![](https://img.youtube.com/vi/PhV_Oo09gBc/0.jpg)](https://www.youtube.com/watch?v=PhV_Oo09gBc)

[![](https://img.youtube.com/vi/BCKGSaURxd0/3.jpg)](https://www.youtube.com/watch?v=BCKGSaURxd0)

## Things necessary

* Raspberry Pi Pico ( https://www.raspberrypi.org/products/raspberry-pi-pico/ )
    * or other Pico compatible boards
* Pimoroni Pico Wireless Pack ( https://shop.pimoroni.com/products/pico-wireless-pack )
* CircuitPython ( https://circuitpython.org/ )
* adafruit_sdcard library from Adafruit_CircuitPython_Bundle ( https://github.com/adafruit/Adafruit_CircuitPython_Bundle )
* adafruit_esp32spi, adafruit_hid library from Adafruit_CircuitPython_Bundle ( https://github.com/adafruit/Adafruit_CircuitPython_Bundle )

## secrets.py example

```
secrets = [
  {
    "ssid": "my-home-wifi",
    "password": "Password!092749",
    "timezone": "Asia/Tokyo",  # Check http://worldtimeapi.org/timezones
  },
  {
    "ssid": "my-office-wifi",
    "password": "Secure#865981",
    "timezone": "Asia/Tokyo",  # Check http://worldtimeapi.org/timezones
  }
]
```

# blog

https://akkiesoft.hatenablog.jp/entry/20210605/1622863906
