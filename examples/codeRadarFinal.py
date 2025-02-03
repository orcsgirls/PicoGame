import displayio
import terminalio
import pwmio
import board
import math
from picogame import *
from adafruit_motor import servo
from adafruit_hcsr04 import HCSR04
from adafruit_display_shapes.line import Line
from adafruit_display_shapes.circle import Circle
from adafruit_display_text.label import Label

def get_distance():
    """Measures distance using HCSR04 ultrasonic sensor."""
    try:
        distance = sonar.distance
        return distance
    except RuntimeError:
        return 1000  # Return max range on error

def draw_static_radar():
    """Draws static radar grid lines."""
    static_group = displayio.Group()
    for r in range(40, radar.display.height, 40):
        static_group.append(Circle(center_x, center_y, r, outline=0xFFFF00))
        static_group.append(Label(terminalio.FONT, color=0xFFFF00, scale=2, text=str(int(r/sonar_scale)),
                                 anchor_point=(0.5,0.0), anchored_position=(center_x,center_y-r)))

    return static_group

def draw_radar(angle, distance, sweep_group):
    """Draws the radar scan result on the ST7789 display."""
    print (f"Angle: {angle} - Distance: {distance} cm")
    # Convert polar to Cartesian coordinates
    radians = math.radians(angle)
    scaled_distance = min(sonar_scale*distance, radar.display.width/2)
    target_x = int(center_x + scaled_distance * math.cos(radians))
    target_y = int(center_y - scaled_distance * math.sin(radians))

    # Draw sweeping line
    sweep_x = int(center_x + radar.display.width/2 * math.cos(radians))
    sweep_y = int(center_y - radar.display.width/2 * math.sin(radians))
    sweep_group.append(Line(center_x, center_y, target_x, target_y, color=0x00FF00))
    sweep_group.append(Line(target_x, target_y, sweep_x, sweep_y, color=0xFF0000))

# Setup the game
radar=Picogame()

# Settings
center_x, center_y = radar.display.width//2, radar.display.height  # Radar center

# Sonar
sonar = HCSR04(trigger_pin=board.GP0, echo_pin=board.GP1)
sonar_scale = 1.0  # Length scale for radar display

# Set up servo
pwm = pwmio.PWMOut(board.GP19, duty_cycle=2 ** 15, frequency=50)
servo_motor = servo.Servo(pwm)

# Draw the grid
static_group = draw_static_radar()
radar.append(static_group)
sweep_group = displayio.Group()
radar.append(sweep_group)

# Control variables
angle = 0
step_angle = 5
running = True

while True:
    if running:
        angle = angle + step_angle
        servo_motor.angle = angle
        distance = get_distance()
        draw_radar(angle, distance, sweep_group)

        if(angle==0 or angle==180):
            radar.remove(sweep_group)
            sweep_group = displayio.Group()
            radar.append(sweep_group)
            step_angle = -step_angle

        for t in range(100):
            if radar.buttonB.isPressed():
                running = not running
            time.sleep(0.01)
    else:
        if radar.joystickUp.isPressed() and sonar_scale > 0.25:
            sonar_scale = sonar_scale / 2.0
            radar.remove(sweep_group)
            sweep_group = displayio.Group()
            radar.append(sweep_group)
            radar.remove(static_group)
            static_group = draw_static_radar()
            radar.append(static_group)

        if radar.joystickDown.isPressed() and sonar_scale < 4.0:
            sonar_scale = sonar_scale * 2.0
            radar.remove(sweep_group)
            sweep_group = displayio.Group()
            radar.append(sweep_group)
            radar.remove(static_group)
            static_group = draw_static_radar()
            radar.append(static_group)

        if radar.buttonB.isPressed():
            running = not running
        time.sleep(0.01)
