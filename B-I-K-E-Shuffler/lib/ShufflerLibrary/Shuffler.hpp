#pragma once

#include "StepperMotor.hpp"

// We need to control 3 different stepper motors
// 1. The motor that move the dispenser
// 2. The motor that moves the belt that the cards are already on
// 3. The Dropper motor that drops the cards

class Shuffler {
public:
    Shuffler();

    // Initialize
    void init();
    void calibrate();
    void killAllPower();

    // Motor Control
    void moveDispenserToMM(float targetMM);
    void moveDispenserToSlot(int slotNumber);
    void moveBeltToMM(float targetMM);
    void ejectCards();
    void resetBelt();
    void dropCard();

    StepperMotor dispenserMotor; // Dispenser Rail
    StepperMotor beltMotor; // Conveyor Belt
    StepperMotor dropperMotor; // Card Dropper
};
