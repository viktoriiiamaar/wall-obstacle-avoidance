let left: number;
let front: number;
let right: number;
//  Enter the maze (get to the middle of the grid)
CutebotPro.distanceRunning(CutebotProOrientation.Advance, 14, CutebotProDistanceUnits.Cm)
basic.pause(1000)
let path = []
let first_move_done = false
function check_distance(): number {
    return CutebotPro.ultrasonic(SonarUnit.Centimeters)
}

function turn_left() {
    CutebotPro.trolleySteering(CutebotProTurn.LeftInPlace, 95)
    basic.pause(100)
}

function turn_right() {
    CutebotPro.trolleySteering(CutebotProTurn.RightInPlace, 95)
    basic.pause(100)
}

function move_forward() {
    CutebotPro.distanceRunning(CutebotProOrientation.Advance, 25, CutebotProDistanceUnits.Cm)
    basic.pause(100)
}

while (true) {
    if (!first_move_done) {
        move_forward()
        path.push(1)
        first_move_done = true
        continue
    }
    
    // Look left
    turn_left()
    left = check_distance()
    basic.pause(100)
    // Face forward again
    turn_right()
    front = check_distance()
    basic.pause(100)
    // Stop if maze ends (huge opening ahead)
    if (front > 100) {
        serial.writeLine("Maze end detected! Stopping.")
        break
    }
    
    // Look right
    turn_right()
    right = check_distance()
    basic.pause(100)
    // Face forward again
    turn_left()
    basic.pause(100)
    // Maze logic
    if (left > 15) {
        turn_left()
        move_forward()
        path.push(2)
    } else if (front > 15) {
        move_forward()
        path.push(1)
    } else if (right > 15) {
        turn_right()
        move_forward()
        path.push(3)
    } else {
        // Dead end  - have not tested it out yet
        turn_left()
        turn_left()
        move_forward()
        path.push(0)
    }
    
}
// Output path after reaching end
if (input.buttonIsPressed(Button.A) == true) {
    serial.writeLine("Maze path taken:")
    for (let step of path) {
        if (step == 1) {
            serial.writeLine("Forward")
        } else if (step == 2) {
            serial.writeLine("Left")
        } else if (step == 3) {
            serial.writeLine("Right")
        } else if (step == 0) {
            serial.writeLine("Backtrack")
        }
        
    }
}

