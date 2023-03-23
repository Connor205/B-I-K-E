#include "Turret.hpp"
#include "TurretConstants.hpp"
#include <Arduino.h>
#include <Utils.h>

Turret::Turret() { this->turretMotor = StepperMotor(TURRET_STEP_PIN, TURRET_DIR_PIN); }

void Turret::init() {
    // Init Turret StepperMotor
    this->turretMotor.init();

    // Initialize DC Motor Pins
    pinMode(INDEXER_MOTOR_PLUS_PIN, OUTPUT);
    pinMode(INDEXER_MOTOR_MINUS_PIN, OUTPUT);
    pinMode(FLYWHEEL_MOTOR_PLUS_PIN, OUTPUT);
    pinMode(FLYWHEEL_MOTOR_MINUS_PIN, OUTPUT);

    // Intialize Sensor Pins
    pinMode(INDEXER_ENCODER_A_PLUS_PIN, INPUT);
    pinMode(INDEXER_ENCODER_A_MINUS_PIN, INPUT);
    pinMode(INDEXER_ENCODER_B_PLUS_PIN, INPUT);
    pinMode(INDEXER_ENCODER_B_MINUS_PIN, INPUT);
    pinMode(MAGAZINE_SENSOR_PIN, INPUT);
    pinMode(FLYWHEEL_BARREL_SENSOR_PIN, INPUT);

    // Turn off motors
    killAllPower();
}

void Turret::calibrate() { this->turretMotor.calibrate(); }

void Turret::killAllPower() {
    digitalWrite(INDEXER_MOTOR_PLUS_PIN, LOW);
    digitalWrite(INDEXER_MOTOR_MINUS_PIN, LOW);
    digitalWrite(FLYWHEEL_MOTOR_PLUS_PIN, LOW);
    digitalWrite(FLYWHEEL_MOTOR_MINUS_PIN, LOW);
}

/**
 * @brief Turns the turret motor to face the target angle
 *
 * @param targetDegrees the target angle in degrees [90, -90])
 */
void Turret::turnToAngle(float targetDegrees) {
    if (targetDegrees > 90.0f) {
        writeError("Target angle too large, clamping to 90 degrees");
        targetDegrees = 90.0f;
    } else if (targetDegrees < -90.0f) {
        writeError("Target angle too small, clamping to -90 degrees");
        targetDegrees = -90.0f;
    }
    this->turretMotor.moveToAngle(targetDegrees);
}

/**
 * @brief Powers the flywheel motor on or off
 *
 * @param on true -> on, false -> off
 */
void Turret::powerFlywheel(bool on) {
    if (on) { // TODO: Check direction
        digitalWrite(FLYWHEEL_MOTOR_PLUS_PIN, LOW);
        digitalWrite(FLYWHEEL_MOTOR_MINUS_PIN, HIGH);
    } else {
        digitalWrite(FLYWHEEL_MOTOR_PLUS_PIN, LOW);
        digitalWrite(FLYWHEEL_MOTOR_MINUS_PIN, LOW);
    }
}

/**
 * @brief Powers the indexer motor on or off
 *
 * @param on true -> on, false -> off
 */
void Turret::powerIndexer(bool on) {
    if (on) { // TODO: Check direction
        digitalWrite(INDEXER_MOTOR_PLUS_PIN, LOW);
        digitalWrite(INDEXER_MOTOR_MINUS_PIN, HIGH);
    } else {
        digitalWrite(INDEXER_MOTOR_PLUS_PIN, LOW);
        digitalWrite(INDEXER_MOTOR_MINUS_PIN, LOW);
    }
}

float Turret::getTurretAngle() { return this->turretMotor.getCurrentAngle(); }

bool Turret::cardInMagazine() { return digitalRead(MAGAZINE_SENSOR_PIN); }

bool Turret::cardInFlywheelBarrel() { return this->getBarrelReading() > FLYWHEEL_BARREL_SENSOR_THRESHOLD; }

/*Generates a value between 0 and 1023 for the barrel sensor */
int Turret::getBarrelReading() {
    int sensorValue = analogRead(FLYWHEEL_BARREL_SENSOR_PIN);
    return map(sensorValue, 0, 1023, 0, 255);
}

void Turret::dealSingleCard() {
    this->powerFlywheel(true);
    this->powerIndexer(true);
    while (this->getBarrelReading() > FLYWHEEL_BARREL_SENSOR_THRESHOLD) {
        delay(5);
    }
    this->powerIndexer(false);
}