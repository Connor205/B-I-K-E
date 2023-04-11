#include <Arduino.h>
#include <TurretLibrary.hpp>
#include <Utils.h>

Turret turret = Turret();

void stopForever()
{
    while (true) {
        delay(1000);
    }
}

void sprayCards()
{
    turret.turnToAngle(180);
    turret.powerFlywheel(true);
    turret.powerIndexer(true);
    turret.turnToAngle(0);
    turret.powerIndexer(false);
    turret.powerFlywheel(false);
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
    } else if (input.equals("move")) {
        waitForSerialInput();
        int x = Serial.parseInt();
        // Write info to serial
        writeInfo("Moving to " + String(x));
        turret.turnToAngle(x);
    } else if (input.equals("player")) {
        waitForSerialInput();
        int x = Serial.parseInt();
        // Write info to serial
        turret.dealToPlayer(x);
    } else if (input.equals("deal")) {
        turret.dealSingleCard();
    } else if (input.equals("players")) {
        turret.dealToAllPlayers();
    } else if (input.equals("flop")) {
        turret.dealFlop();
    } else if (input.equals("turn")) {
        turret.dealTurn();
    } else if (input.equals("river")) {
        turret.dealRiver();
    } else if (input.equals("discard")) {
        turret.discard();
    } else if (input.equals("spray")) {
        sprayCards();
    } else if (input.equals("eject")) {
        writeState("Ejecting");
        turret.powerFlywheel(true);
        turret.turnToAngle(180);
        turret.powerIndexer(true);
        delay(8000);
        turret.powerIndexer(false);
        turret.powerFlywheel(false);
    } else if (input.equals("waitForConfirmation")) {
        writeState("Waiting For Confirmation");
        while (digitalRead(CONFIRMATION_BUTTON_PIN) == HIGH) {
            delay(50);
        }
    } else if (input.equals("spray")) {
        sprayCards();
    } else {
        writeError("Invalid Command");
    }
}

void setup()
{
    Serial.begin(9600);
    turret.init();
    turret.calibrate();
    pinMode(CONFIRMATION_BUTTON_PIN, INPUT_PULLUP);
}

void loop() { serialReactions(); }