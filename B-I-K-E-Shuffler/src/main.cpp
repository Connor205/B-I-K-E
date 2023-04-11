#include "Utils.h"
#include <Arduino.h>
#include <ShufflerLibrary.hpp>

Shuffler shuffler = Shuffler();

// Lets move the elevator out of the shuffler so we can drive it here in main
StepperMotor elevator
    = StepperMotor(ELEVATOR_STEP_PIN, ELEVATOR_DIR_PIN, ELEVATOR_LIMIT_SWITCH_PIN, ELEVATOR_MOTOR_MAX_STEPS_PER_SECOND);

void serialReactions()
{
    writeState("ready");
    // Wait for an input from the serial port
    waitForSerialInput();
    // Read the input
    String input = Serial.readStringUntil('\n');
    writeInfo("Received - " + input);
    // Check if string is equal to yAxis
    if (input.equals("reset")) {
        shuffler.resetBelt();
        shuffler.moveDispenserToSlot(1);
    } else if (input.equals("eject")) {
        shuffler.ejectCards();
    } else if (input.equals("dispense")) {
        writeState("dispensing");
        shuffler.dropCard();
    } else if (input.equals("move")) {
        waitForSerialInput();
        int x = Serial.parseInt();
        // Write info to serial
        writeInfo("Moving to slot" + String(x));
        shuffler.moveDispenserToSlot(x);
    } else if (input.equals("up")) {
        elevator.moveToTarget(ELEVATOR_TOP_STEP);
    } else if (input.equals("down")) {
        elevator.moveToTarget(-1000);
        elevator.moveToTarget(ELEVATOR_TOP_STEP);
    } else if (input.equals("wait")) {
        writeInfo("Waiting for confirmation button press");
        while (digitalRead(CONFIRMATION_BUTTON_PIN) == HIGH) {
            delay(50);
        }
    } else if (input.equals("test")) {
        while (true) {
            writeInfo("Photoresistor value: " + String(analogRead(DISPENSER_PHOTOSENSOR_PIN)));
            delay(100);
        }
    } else if (input.equals("demo")) {
        for (int i = 0; i < 5; i++) {
            long s = SLOT_CONSTANTS[i];
            shuffler.dispenserMotor.moveToTargetAccel(s);
            shuffler.dropCard();
        }
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
    elevator.calibrate(true);
    digitalWrite(DROPPER_MOTOR_DIR_PIN, HIGH);
    elevator.moveToTarget(-1000);
}

void loop() { serialReactions(); }
