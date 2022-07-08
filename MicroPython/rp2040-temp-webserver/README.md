# rp2040-temp-webserver

This script runs the web server that provide the json file including datetime in RP2040 and temperature in RP2040.

This was written for the below blog entry. It is written in Japanese, so please use the translation service ;)

[Raspberry Pi Pico Wを電池で動かすとどのくらい動くか試す(Check how long we can run the Pico W with the 2x AA Ni-MH battery)](https://www.raspi.jp/2022/07/202207-pico-w-with-ni-mh-battery/)

## picow-client-oled

This script requests above json data from the Pico W and show it on the OLED display.

It is required the normal Raspberry Pi not Pico.