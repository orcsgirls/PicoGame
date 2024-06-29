# SPDX-FileCopyrightText: 2019 Carter Nelson for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import board
import busio
import displayio
from fourwire import FourWire
from adafruit_st7789 import ST7789
import adafruit_imageload
from digitalio import DigitalInOut, Direction, Pull


class button():
    def __init__(self, pin):
        self.btn = DigitalInOut(pin)
        self.btn.direction = Direction.INPUT
        self.btn.pull = Pull.UP
        self.lastState = self.btn.value

    def isPressed(self):
        currentState = self.btn.value
        if currentState != self.lastState:
            self.lastState=currentState
            return currentState
        else:
            return False

    @property
    def value(self):
        return self.btn.value
        
class picodisplay():
    def __init__(self):
        displayio.release_displays()       
        spi = busio.SPI(clock=board.GP10, MOSI=board.GP11, MISO=None)
        tft_cs = board.GP9
        tft_dc = board.GP8
        tft_rst = board.GP12
        display_bus = FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)
        
        self.width = 320
        self.height = 170
        self.display = ST7789(display_bus, width=self.width, height=self.height, colstart=35, rotation=90)

        self.joystickUp = button(board.GP2)
        self.joystickDown = button(board.GP18)
        self.joystickLeft = button(board.GP16)
        self.joystickRight = button(board.GP20)
        self.joystickCenter = button(board.GP3)
        self.buttonA = button(board.GP15)
        self.buttonB = button(board.GP17)


pico=picodisplay()

# Load the sprite sheet (bitmap)
sprite_sheet, palette = adafruit_imageload.load("/castle_sprite_sheet.bmp",
                                                bitmap=displayio.Bitmap,
                                                palette=displayio.Palette)

# Create the sprite TileGrid
sprite = displayio.TileGrid(sprite_sheet, pixel_shader=palette,
                            width = 1,
                            height = 1,
                            tile_width = 16,
                            tile_height = 16,
                            default_tile = 0)

# Create the castle TileGrid
castle = displayio.TileGrid(sprite_sheet, pixel_shader=palette,
                            width = 6,
                            height = 5,
                            tile_width = 16,
                            tile_height = 16)

# Create a Group to hold the sprite and add it
sprite_group = displayio.Group()
sprite_group.append(sprite)

# Create a Group to hold the castle and add it
castle_group = displayio.Group(scale=3)
castle_group.append(castle)

# Create a Group to hold the sprite and castle
group = displayio.Group()

# Add the sprite and castle to the group
group.append(castle_group)
group.append(sprite_group)

# Castle tile assignments
# corners
castle[0, 0] = 3  # upper left
castle[5, 0] = 5  # upper right
castle[0, 4] = 9  # lower left
castle[5, 4] = 11 # lower right
# top / bottom walls
for x in range(1, 5):
    castle[x, 0] = 4  # top
    castle[x, 4] = 10 # bottom
# left/ right walls
for y in range(1, 4):
    castle[0, y] = 6 # left
    castle[5, y] = 8 # right
# floor
for x in range(1, 5):
    for y in range(1, 4):
        castle[x, y] = 7 # floor

# put the sprite somewhere in the castleif not btn.value:
sprite.x = 110
sprite.y = 70

# Add the Group to the Display
pico.display.root_group = group

# Loop forever so you can enjoy your image
while True:
    if pico.joystickUp.isPressed():
        sprite.y = sprite.y+5
    elif pico.joystickDown.isPressed():
        sprite.y = sprite.y-5
    elif pico.joystickLeft.isPressed():
        sprite.x = sprite.x+5
    elif pico.joystickRight.isPressed():
        sprite.x = sprite.x-5
    elif pico.joystickCenter.isPressed():
        sprite.x = 110
        sprite.y = 70


