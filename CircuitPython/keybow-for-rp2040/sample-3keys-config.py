from adafruit_hid.keycode import Keycode

# 0 = Keybow, 1 = Keybow mini.
keybow_type = 1

colors = [
    (255,   0,   0),
    (  0, 255,   0),
    (  0,   0, 255),
]
keycodes = [
    [Keycode.LEFT_SHIFT, Keycode.ONE],
    [Keycode.TWO],
    [Keycode.THREE]
]