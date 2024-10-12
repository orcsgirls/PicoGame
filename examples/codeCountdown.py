from picogame import *

# Setup the game
game=Picogame()
counter=Sign(game)

count_down = 10  # in seconds
counter.text = f"{count_down:.2f}"
running = False

while True:
    # Check the joystick buttons to increas/decreast the start time
    if(game.joystickUp.isPressed() and not running):
        count_down=count_down+1 
        counter.text = f"{count_down:.2f}"
    if(game.joystickDown.isPressed() and not running):
        if(count_down > 1):
            count_down=count_down-1 
        counter.text = f"{count_down:.2f}"

    # Button A - start the countdown
    if(game.buttonA.isPressed() and not running):
        start_time = time.monotonic()
        running = True

    # Button B - reset after it stopped
    if(game.buttonB.isPressed() and not running):
        counter.text = f"{count_down:.2f}"
        counter.switch()

    # Countdown update and check if it is done
    if running:
        current_time = count_down - (time.monotonic() - start_time)
        counter.text = f"{current_time:.2f}"
        if(current_time<=0):
            running = False
            counter.text = 'Done'
            counter.switch()
 
    time.sleep(0.001)