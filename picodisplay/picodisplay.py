import board
import busio
import displayio
from fourwire import FourWire
from adafruit_st7789 import ST7789
from digitalio import DigitalInOut, Direction, Pull

class Button():
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
        
class Picodisplay():
    def __init__(self):
        displayio.release_displays()       
        spi = busio.SPI(clock=board.GP10, MOSI=board.GP11, MISO=None)
        tft_cs = board.GP9
        tft_dc = board.GP8
        tft_rst = board.GP12
        display_bus = FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)
        
        self.display = ST7789(display_bus, rotation=270, width=240, height=135, rowstart=40, colstart=53)

        self.joystickUp = Button(board.GP2)
        self.joystickDown = Button(board.GP18)
        self.joystickLeft = Button(board.GP16)
        self.joystickRight = Button(board.GP20)
        self.joystickCenter = Button(board.GP3)
        self.buttonA = Button(board.GP15)
        self.buttonB = Button(board.GP17)