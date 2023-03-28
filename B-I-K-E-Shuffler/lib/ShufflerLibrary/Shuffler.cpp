#include "Shuffler.hpp"
#include "ShufflerConstants.hpp"

Shuffler::Shuffler() {
    this->dispenserMotor =
        StepperMotor(DISPENSER_RAIL_STEP_PIN, DISPENSER_RAIL_DIR_PIN, DISPENSER_RAIL_LIMIT_SWITCH_PIN, DISPENSER_RAIL_MAX_STEPS_PER_SECOND);
    this->beltMotor =
        StepperMotor(BELT_STEP_PIN, BELT_DIR_PIN, CONVEYER_HALL_EFFECT_PIN, BELT_MOTOR_MAX_STEPS_PER_SECOND);
    this->dropperMotor =
        StepperMotor(DROPPER_MOTOR_STEP_PIN, DROPPER_MOTOR_DIR_PIN, -1, DROPPER_MOTOR_MAX_STEPS_PER_SECOND);
    this->elevatorMotor =
        StepperMotor(ELEVATOR_STEP_PIN, ELEVATOR_DIR_PIN, ELEVATOR_LIMIT_SWITCH_PIN, ELEVATOR_MOTOR_MAX_STEPS_PER_SECOND);
}

void Shuffler::init() {
    this->dispenserMotor.init();
    this->beltMotor.init();
    this->dropperMotor.init();
    this->elevatorMotor.init();
    this->calibrate();
    this->dispenserMotor.moveToTarget(DISPENSER_STEPS_TO_FIRST_LINK);
}

void Shuffler::calibrate() {
    this->dispenserMotor.calibrate();
    this->beltMotor.calibrate();
    this->dropperMotor.calibrate();
    this->elevatorMotor.calibrate();
}

void Shuffler::moveDispenserToSlot(int slotNumber) {
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

void Shuffler::moveDispenserToMM(float targetMM) { this->dispenserMotor.moveToTarget(targetMM * DISPENSER_STEPS_PER_MM); }

void Shuffler::moveBeltToMM(float targetMM) { this->beltMotor.moveToTarget(targetMM * BELT_STEPS_PER_MM); }

void Shuffler::ejectCards() { this->beltMotor.moveToTarget(BELT_LENGTH_STEPS); }

void Shuffler::resetBelt() { this->beltMotor.moveToTarget(DISPENSER_STEPS_TO_FIRST_LINK); }

// TODO:: This is not the way we are going to do this, but it works for now
void Shuffler::dropCard() {
    this->dropperMotor.setDirection(true); // Drop card direction
    for (int i = 0; i < DROPPER_STEPS_PER_CARD; i++) {
        this->dropperMotor.stepMotor();
    }
    this->dropperMotor.setDirection(false); // Pull cards up after drop
    int resetSteps = DROPPER_STEPS_PER_CARD / 2;
    for (int i = 0; i < resetSteps; i++) {
        this->dropperMotor.stepMotor();
    }
}
