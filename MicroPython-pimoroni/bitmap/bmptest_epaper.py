import time
from picographics import PicoGraphics, DISPLAY_INKY_PACK
import bitmap

display = PicoGraphics(display=DISPLAY_INKY_PACK)
display.set_update_speed(0)

bmp = bitmap.bitmap("/uhatporter.bmp", display)
bmp.decode()
display.update()
time.sleep(0.5)