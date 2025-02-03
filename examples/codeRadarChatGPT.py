import board
import busio
import digitalio
import pwmio
import time
import math
import displayio
import adafruit_st7789
import terminalio
import adafruit_hcsr04
from adafruit_motor import servo
from fourwire import FourWire
from adafruit_display_shapes.line import Line
from adafruit_display_shapes.circle import Circle
from adafruit_display_text.label import Label

# Initialize SPI display
displayio.release_displays()
spi = busio.SPI(clock=board.GP10, MOSI=board.GP11, MISO=None)
tft_cs = board.GP9
tft_dc = board.GP8
tft_rst = board.GP12
display_bus = FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)
display = adafruit_st7789.ST7789(display_bus, rotation=270, width=240, height=135, rowstart=40, colstart=53)

# Set up servo
pwm = pwmio.PWMOut(board.GP19, duty_cycle=2 ** 15, frequency=50)
servo_motor = servo.Servo(pwm)

# Display stuff
group = displayio.Group()
display.root_group = group  # Updated to use root_group

# Sensor
sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP0, echo_pin=board.GP1)

# Scale
sonar_scale = 2.0

# Radar sweep parameters
angle_step = 5
angle_range = range(0, 181, angle_step)  # Sweep from 0 to 180 degrees
center_x, center_y = display.width//2, display.height  # Radar center

def get_distance():
    """Measures distance using HCSR04 ultrasonic sensor."""
    try:
        distance = sonar.distance
        return distance
    except RuntimeError:
        return 250  # Return max range on error

def draw_static_radar(static_group):
    """Draws static radar grid lines."""
    for r in range(40, display.height, 40):
        static_group.append(Circle(center_x, center_y, r, outline=0xFFFFFF))
        static_group.append(Label(terminalio.FONT, color=0xFFFFFF, scale=2, text=str(int(r/sonar_scale)),
                                 anchor_point=(0.5,0.0), anchored_position=(center_x,center_y-r)))

def draw_radar(angle, distance, sweep_group):
    """Draws the radar scan result on the ST7789 display."""
    print (f"Angle: {angle} - Distance: {distance} cm")
    # Convert polar to Cartesian coordinates
    radians = math.radians(angle)
    scaled_distance = min(sonar_scale*distance, display.width/2)
    target_x = int(center_x + scaled_distance * math.cos(radians))
    target_y = int(center_y - scaled_distance * math.sin(radians))

    # Draw sweeping line
    sweep_x = int(center_x + display.width/2 * math.cos(radians))
    sweep_y = int(center_y - display.width/2 * math.sin(radians))
    sweep_group.append(Line(center_x, center_y, target_x, target_y, color=0x00FF00))
    sweep_group.append(Line(target_x, target_y, sweep_x, sweep_y, color=0xFF0000))

static_group = displayio.Group()
draw_static_radar(static_group)
group.append(static_group)

while True:
    sweep_group = displayio.Group()  # Reset sweep group after each full sweep
    group.append(sweep_group)

    for angle in angle_range:
        servo_motor.angle = angle
        distance = get_distance()
        time.sleep(1.0)
        draw_radar(angle, distance, sweep_group)

    group.remove(sweep_group)  # Clear old sweep lines to free memory
    sweep_group = displayio.Group()
    group.append(sweep_group)

    for angle in reversed(angle_range):
        servo_motor.angle = angle
        distance = get_distance()
        time.sleep(1.0)
        draw_radar(angle, distance, sweep_group)

    group.remove(sweep_group)  # Clear old sweep lines to free memory
