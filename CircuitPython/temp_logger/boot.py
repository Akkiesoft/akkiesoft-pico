"""
  boot.py @Akkiesoft

  Original:
    CircuitPython Essentials Storage logging boot.py file
    Copyright 2017 Limor Fried for Adafruit Industries
    MIT License
"""
import board
import digitalio
import storage

switch = digitalio.DigitalInOut(board.GP2)

switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

i = 1 - switch.value
# 押してたらPC編集モード。押してなかったらロギングモード
storage.remount("/", readonly=i)
