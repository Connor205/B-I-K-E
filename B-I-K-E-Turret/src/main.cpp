#include <Arduino.h>
#include <TurretLibrary.hpp>
#include <Utils.h>

Turret turret = Turret();

void stopForever() {
    while (true) {
        delay(1000);
    }
}

void testTurretAccuracy() {

}

void photoTest() {
    while (true) {
        int reading = turret.getBarrelReading();
        writeInfo("Photoresistor reading: " + String(reading));
        // if (reading < FLYWHEEL_BARREL_SENSOR_THRESHOLD) {
        //     writeInfo("Card Firing");
        //     turret.powerFlywheel(false);
        //     turret.powerIndexer(false);
        //     break;
        // }
    }
}

void sprayCards() {
    turret.powerFlywheel(true);
    turret.turnToAngle(45);
    turret.powerIndexer(true);
    turret.turnToAngle(-45);
    turret.powerIndexer(false);
    turret.powerFlywheel(false);
    turret.turnToAngle(0);
}

void serialReactions() {
    writeState("ready");
    // Wait for an input from the serial port
    waitForSerialInput();
    // Read the input
    String input = Serial.readStringUntil('\n');
    writeInfo("Received - " + input);
    // Check if string is equal to yAxis
    if (input.equals("indexerOn")) {
        turret.powerIndexer(true);
    } else if (input.equals("indexerOff")) {
        turret.powerIndexer(false);
    } else if (input.equals("flywheelOn")) {
        turret.powerFlywheel(true);
    } else if (input.equals("flywheelOff")) {
        turret.powerFlywheel(false);
    } else if (input.equals("on")) {
        turret.powerFlywheel(true);
        turret.powerIndexer(true);
    } else if (input.equals("off")) {
        turret.powerFlywheel(false);
        turret.powerIndexer(false);
    } else if (input.equals("test")) {
        testTurretAccuracy();
    } else if (input.equals("move")) {
        waitForSerialInput();
        int x = Serial.parseInt();
        // Write info to serial
        writeInfo("Moving to " + String(x));
        turret.turnToAngle(x);
    } else if (input.equals("photoTest")) {
        photoTest();
    } else if (input.equals("deal")) {
        turret.dealSingleCard();
    } else {
        writeError("Invalid Command");
    }
}

void setup() {
    Serial.begin(9600);
    turret.init();
    turret.calibrate();
}

void loop() {
    // serialReactions();
    // turret.dealSingleCard();
    turret.powerFlywheel(true);
    turret.powerIndexer(true);
    stopForever();
}