#include "Utils.h"
#include <Arduino.h>
#include <ShufflerLibrary.hpp>

Shuffler shuffler = Shuffler();

// Lets move the elevator out of the shuffler so we can drive it here in main
StepperMotor elevator
    = StepperMotor(ELEVATOR_STEP_PIN, ELEVATOR_DIR_PIN, ELEVATOR_LIMIT_SWITCH_PIN, ELEVATOR_MOTOR_MAX_STEPS_PER_SECOND);

void stopForever()
{
    while (true) {
        delay(100);
    }
}

void serialReactions()
{
    writeState("ready");
    // Wait for an input from the serial port
    waitForSerialInput();
    // Read the input
    String input = Serial.readStringUntil('\n');
    writeInfo("Received - " + input);
    // Check if string is equal to yAxis
    if (input.equals("resetConveyor")) {
        shuffler.resetBelt();
    } else if (input.equals("ejectCards")) {
        shuffler.ejectCards();
    } else if (input.equals("drop")) {
        shuffler.dropCard();
    } else if (input.equals("slot")) {
        waitForSerialInput();
        int x = Serial.parseInt();
        // Write info to serial
        writeInfo("Moving to slot" + String(x));
        shuffler.moveDispenserToSlot(x);
    } else if (input.equals("elevatorUp")) {
        elevator.moveToTarget(ELEVATOR_TOP_STEP);
    } else if (input.equals("elevatorDown")) {
        elevator.moveToTarget(100);
    } else {
        writeError("Invalid Command");
    }
}

void setup()
{
    Serial.begin(9600);
    shuffler.init();
    shuffler.calibrate();
    elevator.init();
    elevator.calibrate(true); // TODO:: Make sure this is the correct direction
}

void loop() { serialReactions(); }
