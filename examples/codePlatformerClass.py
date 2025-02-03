import board
import simpleio
from picogame import *
PIEZO_PIN = board.GP21

# Setup the game
game=Picogame()

wall=Wall(game)
sprite=Sprite(game)
score=Score(game)

running=True

while True:
    if(game.buttonA.isPressed() and (not running)):
        wall.reset()
        score.reset()
        sprite.reset()
        running=True

    if (game.buttonB.isPressed()):
        running = not running

    if running:
        if(game.joystickUp.value):
            sprite.y = sprite.y + 1
        if(game.joystickDown.value):
            sprite.y = sprite.y - 1

        if(wall.x < 10):
            if(abs(wall.y - sprite.y) < 10):
                wall.y = random.randint(10,110)
                wall.x = game.display.width
                score.value = score.value + 1
                simpleio.tone(PIEZO_PIN, 300, duration=0.2)
            else:
                simpleio.tone(PIEZO_PIN, 300, duration=0.2)
                simpleio.tone(PIEZO_PIN, 200, duration=0.4)
                running = False
        else:
            wall.x = wall.x - 1
        time.sleep(0.01)# Write your code here :-)
