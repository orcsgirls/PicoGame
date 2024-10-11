from picogame import *

# Setup the game
game=Picogame()

# Add game elements
player=Sprite(game)
wall=Wall(game, gap=2*player.height)
score=Score(game)

# Game loop
running=True
time_step = 0.01

while True:
    # Joystick check
    if game.joystickUp.value:
        player.y = player.y+1
    if game.joystickDown.value:
        player.y = player.y-1

    if running:
        # Check collision
        if(wall.x < player.width):

            # Check collision
            if(abs(wall.y-player.y) < (wall.height - player.height)/2):
                # We have passed through the hole :)
                # Put the wall back to the beginning and move the gap
                wall.x = game.display.width
                wall.y = random.randint(wall.gap, game.display.height-wall.gap)

                # Update score
                score.value = score.value + 1

                # Speed up every 10 points
                if ((score.value % 10) == 0):
                    time_step=0.90 * time_step
            else:
                # Crashed
                score.string="Boo"
                running=False

        # Move wall forward
        wall.x = wall.x-1

    if game.buttonA.isPressed():
        # Button A for a Reset
        score.reset()
        wall.reset()
        player.reset()
        running = True

    if game.buttonB.isPressed():
        # Button B to pause and restart
        running = not running

    time.sleep(time_step)
