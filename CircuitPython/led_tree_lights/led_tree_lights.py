import board
from digitalio import DigitalInOut, Direction, Pull
import random
import time

lights = (board.GP11, board.GP12, board.GP13, board.GP20, board.GP14, )
ll = []

for l in lights:
    ll.append(DigitalInOut(l))
    ll[-1].direction = Direction.OUTPUT
    ll[-1].value = 1

while True:
    i = random.randrange(0, 5)
    ll[i].value = 1 - ll[i].value
    time.sleep(0.25)