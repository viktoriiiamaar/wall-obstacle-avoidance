# Enter the maze (get to the middle of the grid)
CutebotPro.distance_running(CutebotProOrientation.ADVANCE, 14, CutebotProDistanceUnits.CM)
basic.pause(1000)

path = []
first_move_done = False

def check_distance():
    return CutebotPro.ultrasonic(SonarUnit.CENTIMETERS)

def turn_left():
    CutebotPro.trolley_steering(CutebotProTurn.LEFT_IN_PLACE, 95)
    basic.pause(100)

def turn_right():
    CutebotPro.trolley_steering(CutebotProTurn.RIGHT_IN_PLACE, 95)
    basic.pause(100)

def move_forward():
    CutebotPro.distance_running(CutebotProOrientation.ADVANCE, 30, CutebotProDistanceUnits.CM)
    basic.pause(100)

while True:
    if not first_move_done:
        move_forward()
        path.append(1)
        first_move_done = True
        continue

    #Look left
    turn_left()
    left = check_distance()
    basic.pause(100)

    #Face forward again
    turn_right()
    front = check_distance()
    basic.pause(100)

    #Stop if maze ends (huge opening ahead)
    if front > 100:
        serial.write_line("Maze end detected! Stopping.")
        break

    #Look right
    turn_right()
    right = check_distance()
    basic.pause(100)

    #Face forward again
    turn_left()
    basic.pause(100)

    #Maze logic
    if left > 15:
        turn_left()
        move_forward()
        path.append(2)
    elif front > 15:
        move_forward()
        path.append(1)
    elif right > 15:
        turn_right()
        move_forward()
        path.append(3)
    else:
        #Dead end  - have not tested it out yet
        turn_left()
        turn_left()
        move_forward()
        path.append(0)

#Output path after reaching end
serial.write_line("Maze path taken:")
    for step in path:
        if step == 1:
            serial.write_line("Forward")
        elif step == 2:
            serial.write_line("Left")
        elif step == 3:
            serial.write_line("Right")
        elif step == 0:
            serial.write_line("Backtrack")

# Simulates data from a second micro:bit
def on_button_pressed_a():
    for i in range (length(path)):
    radio.send_value("Directions to the maze", path[i])
input.on_button_pressed(Button.A, on_button_pressed_a)

radio.set_group(1)

def on_every_interval():
    radio.send_value("t1", input.temperature())
loops.every_interval(60000, on_every_interval)

