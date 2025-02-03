import board
import busio
import displayio
import terminalio
import adafruit_imageload
import time
from adafruit_display_text import label
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label
from fourwire import FourWire
from adafruit_st7789 import ST7789
from digitalio import DigitalInOut, Direction, Pull

displayio.release_displays()
spi = busio.SPI(clock=board.GP10, MOSI=board.GP11, MISO=None)
tft_cs = board.GP9
tft_dc = board.GP8
tft_rst = board.GP12
display_bus = FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)
display = ST7789(display_bus, rotation=270, width=240, height=135, rowstart=40, colstart=53)

# Create a bitmap with two colors
bitmap = displayio.Bitmap(display.width, display.height, 2)

# Create a two color palette
palette = displayio.Palette(2)
palette[0] = 0x000000
palette[1] = 0xffffff

# Create a TileGrid using the Bitmap and Palette
tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)

# Create a Group
group = displayio.Group()

# Add the TileGrid to the Group
group.append(tile_grid)

# Add the Group to the Display
display.root_group = group

# Draw a pixel
bitmap[80, 50] = 1

# Draw even more pixels
for x in range(150, 170):
    for y in range(100, 110):
        bitmap[x, y] = 1

time.sleep(0.5)
# Draw even more pixels
for x in range(150, 170):
    for y in range(100, 110):
        bitmap[x, y] = 0

# Loop forever so you can enjoy your image
while True:
    pass
# Write your code here :-)
