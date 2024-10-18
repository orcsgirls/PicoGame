import os
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
date=Text(game, font_size=2, x=game.display.width//2, y=85, color=0x0000ff, anchor=(0.5,0.5))
date.text="Connecting .."

# Connect to WiFi and NTP server (network time protocol)
wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))
pool = socketpool.SocketPool(wifi.radio)
ntp = adafruit_ntp.NTP(pool, tz_offset=-4, cache_seconds=3600)

# Days and months
day=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
month=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']



while True:
    try:
        now=ntp.datetime
        current.text=f"{now.tm_hour:02}:{now.tm_min:02}:{now.tm_sec:02}"
        date.text=f"{day[now.tm_wday]} {month[now.tm_mon-1]} {now.tm_mday}, {now.tm_year}"
        time.sleep(1)
    except TimeoutError:
        date.text="Timed out"
        time.sleep(10)
