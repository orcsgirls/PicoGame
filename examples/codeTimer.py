import time
import ssl
import wifi
import socketpool
import rtc
import adafruit_ntp
from picogame import *

# Creating the sign
game=Picogame()
current=Text(game, font_size=4, x=game.display.width//2, y=40, anchor=(0.5,0.5))
timer=Timer()

while True:
    if game.buttonA.isPressed():
        timer.start()
    if game.buttonB.isPressed():
        timer.stop()

    current.text = f"{timer.value:.4f}"
    time.sleep(0.001)
