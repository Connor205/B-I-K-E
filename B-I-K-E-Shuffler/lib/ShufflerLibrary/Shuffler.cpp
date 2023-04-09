#include "Shuffler.hpp"
#include "ShufflerConstants.hpp"
#include <Utils.h>

Shuffler::Shuffler()
{
    this->dispenserMotor = StepperMotor(DISPENSER_RAIL_STEP_PIN, DISPENSER_RAIL_DIR_PIN,
        DISPENSER_RAIL_LIMIT_SWITCH_PIN, DISPENSER_RAIL_MAX_STEPS_PER_SECOND);
    this->beltMotor
        = StepperMotor(BELT_STEP_PIN, BELT_DIR_PIN, CONVEYER_HALL_EFFECT_PIN, BELT_MOTOR_MAX_STEPS_PER_SECOND);
    this->dropperMotor
        = StepperMotor(DROPPER_MOTOR_STEP_PIN, DROPPER_MOTOR_DIR_PIN, -1, DROPPER_MOTOR_MAX_STEPS_PER_SECOND);
}

void Shuffler::init()
{
    this->dispenserMotor.init();
    this->beltMotor.init();
    this->dropperMotor.init();
}

void Shuffler::calibrate()
{
    writeInfo("Calibrating Shuffler Motors");
    this->dispenserMotor.calibrate(false);
    this->dispenserMotor.moveToTargetAccel(6400);
    this->beltMotor.calibrate(true);
    this->beltMotor.moveToTargetAccel(-1000);
}

void Shuffler::moveDispenserToSlot(int slotNumber)
{
    int steps = DISPENSER_STEPS_TO_FIRST_LINK;
    if (slotNumber < NUM_THREE_WIDE_LINKS) {
        steps += (slotNumber / 3) * STEPS_PER_LINK;
        steps += (slotNumber % 3) * (STEPS_PER_THREE_WIDE_SLOT + STEPS_PER_WALL) + STEPS_PER_THREE_WIDE_SLOT / 2;
    } else {
        steps += NUM_THREE_WIDE_LINKS * STEPS_PER_LINK;
        steps += ((slotNumber - NUM_THREE_WIDE_LINKS * 3) / 2) * STEPS_PER_LINK;
        steps += (slotNumber % 2) * (STEPS_PER_TWO_WIDE_SLOT + STEPS_PER_WALL) + STEPS_PER_TWO_WIDE_SLOT / 2;
    }
    this->dispenserMotor.moveToTarget(steps);
}

void Shuffler::moveDispenserToMM(float targetMM)
{
    this->dispenserMotor.moveToTarget(targetMM * DISPENSER_STEPS_PER_MM);
}

void Shuffler::moveBeltToMM(float targetMM) { this->beltMotor.moveToTarget(targetMM * BELT_STEPS_PER_MM); }

void Shuffler::ejectCards() { this->beltMotor.moveToTarget(BELT_LENGTH_STEPS); }

void Shuffler::resetBelt() { this->beltMotor.moveToTarget(BELT_DEFAULT_POSITION); }

// TODO:: This is not the way we are going to do this, but it works for now
void Shuffler::dropCard()
{
    this->dropperMotor.setDirection(false); // Drop card direction

    // Set the speed to max speed
    this->dropperMotor.setSpeed(DROPPER_MOTOR_MAX_STEPS_PER_SECOND);
    // Make sure that we are like at least halfway done
    for (uint16_t i = 0; i < DROPPER_STEPS_PER_CARD / 4 * 3; i++) {
        this->dropperMotor.stepMotor();
    }

    // Set the speed to half the max speed
    this->dropperMotor.setSpeed(DROPPER_MOTOR_MAX_STEPS_PER_SECOND / 2);
    writeInfo("Moving To Detection For Dispense");
    // Then we read the photo sensor until it is light enough to mean that the card has fallen
    int val = 0;
    while (val < 90) { // TODO:: Tune this value
        this->dropperMotor.stepMotor();
        val = analogRead(DISPENSER_PHOTOSENSOR_PIN);
    }
}
