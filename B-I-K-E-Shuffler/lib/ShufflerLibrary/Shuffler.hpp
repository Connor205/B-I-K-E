#pragma once

#include "StepperMotor.hpp"

class Shuffler {
public:
    Shuffler();

    // Initialize
    void init();
    void calibrate();
    void killAllPower();

    // We need to control 2 different stepper motors
    // 1. The motor that move the dispenser
    // 2. The motor that moves the belt that the cards are already on

    // We need to control a servo motor that moves the floor that the cards rest on

    // We need to control a dc motor that dispenses cards

    // Motor Control
    void moveDispenserToMM(float targetMM);
    void moveDispenserToSlot(int slotNumber);
    void moveBeltToMM(float targetMM);
    void ejectCards();
    void resetBelt();
    void powerDispenser(bool on);
    void dropCard();

private:
    StepperMotor dispenserMotor;
    StepperMotor beltMotor;
};
