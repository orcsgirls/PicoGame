import terminalio
import displayio
import time
import random
from picodisplay import Picodisplay
from adafruit_display_text import label
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label

score = 0
running = True

pico = Picodisplay()

game = displayio.Group()
pico.display.root_group = game

pillar = displayio.Group()
hole = 30
top = Rect(0, hole, 10, 300, fill=0x0000FF)
bottom = Rect(0, -hole-300, 10, 300, fill=0x0000FF)
pillar.append(top)
pillar.append(bottom)

ball = Circle(10, int(pico.display.height/2), 10, fill=0x00FF00)
game.append(ball)
game.append(pillar)

pillar.x = pico.display.width
pillar.y = int(pico.display.height/2)

scoretext = label.Label(terminalio.FONT, color=0xFFFF00, scale=3)
scoretext.x = pico.display.width - 50
scoretext.y = 20
scoretext.text = str(score)
game.append(scoretext)

while True:
    if (running):
        if pico.joystickUp.isPressed():
            ball.y = ball.y-5
        elif pico.joystickDown.isPressed():
            ball.y = ball.y+5
    
        pillar.x = pillar.x-1
        if(pillar.x<20):
            if (ball.y > pillar.y-25 and ball.y < pillar.y+25):
                pillar.x=pico.display.width
                pillar.y=random.randint(hole, pico.display.height-hole)
                score = score + 1
                scoretext.text = str(score)
            else:
                running = False
       
        time.sleep(0.01)
        
    else:
        if pico.buttonA.isPressed():
            pillar.x = pico.display.width
            pillar.y = int(pico.display.height/2)
            ball.x = 10
            ball.y = int(pico.display.height/2)
            score = 0
            scoretext.text = str(score)
            running = True
            
        
