#include "Shuffler.hpp"
#include "ShufflerConstants.hpp"

Shuffler::Shuffler() {
    this->dispenserMotor = StepperMotor(DISPENSER_STEP_PIN, DISPENSER_DIR_PIN, DISPENSER_MOTOR_MAX_STEPS_PER_SECOND);
    this->beltMotor = StepperMotor(BELT_STEP_PIN, BELT_DIR_PIN, BELT_MOTOR_MAX_STEPS_PER_SECOND);
}

void Shuffler::init() {
    this->dispenserMotor.init();
    this->beltMotor.init();
    this->calibrate();
    this->dispenserMotor.moveToTarget(STEPS_TO_FIRST_LINK);

    pinMode(DISPENSER_MOTOR_PLUS_PIN, OUTPUT);
    pinMode(DISPENSER_MOTOR_MINUS_PIN, OUTPUT);
}

void Shuffler::calibrate() {
    this->dispenserMotor.calibrate();
    this->beltMotor.calibrate();
}

void Shuffler::moveDispenserToSlot(int slotNumber) {
    int steps = STEPS_TO_FIRST_LINK;
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

void Shuffler::moveDispenserToMM(float targetMM) { this->dispenserMotor.moveToTarget(targetMM * STEPS_PER_MM); }

void Shuffler::moveBeltToMM(float targetMM) { this->beltMotor.moveToTarget(targetMM * STEPS_PER_MM_BELT); }

void Shuffler::ejectCards() { this->beltMotor.moveToTarget(BELT_LENGTH_STEPS); }

void Shuffler::resetBelt() { this->beltMotor.moveToTarget(STEPS_TO_FIRST_LINK); }

void Shuffler::powerDispenser(bool on) {
    if (on) {
        digitalWrite(DISPENSER_MOTOR_PLUS_PIN, HIGH);
        digitalWrite(DISPENSER_MOTOR_MINUS_PIN, LOW);
    } else {
        digitalWrite(DISPENSER_MOTOR_PLUS_PIN, LOW);
        digitalWrite(DISPENSER_MOTOR_MINUS_PIN, LOW);
    }
}

// TODO:: This is not the way we are going to do this, but it works for now
void Shuffler::dropCard() {
    this->powerDispenser(true);
    delay(1000);
    this->powerDispenser(false);
}
