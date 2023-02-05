#include "Turret.hpp
#include <Arduino.h>
#include "TurretConstants.hpp"

Turret::Turret() {
	turretMotor = StepperMotor(TURRET_STEP_PIN, TURRET_DIR_PIN, TURRET_OUTPUT_GEAR_RATIO);
}

void Turret::init() {
	// Init Turret StepperMotor
	turretMotor.init();

	// Initialize DC Motor Pins
	pinMode(INDEXER_MOTOR_PLUS_PIN, OUTPUT);
	pinMode(INDEXER_MOTOR_MINUS_PIN, OUTPUT);
	pinMode(FLYWHEEL_MOTOR_PLUS_PIN, OUTPUT);
	pinMode(FLYWHEEL_MOTOR_MINUS_PIN, OUTPUT);

	// Turn off motors
	killAllPower();
}

void Turret::calibrate() {
	turretMotor.calibrate();
}


void Turret::killAllPower() {
	// Kill DC Motors
	digitalWrite(INDEXER_MOTOR_PLUS_PIN, LOW);
	digitalWrite(INDEXER_MOTOR_MINUS_PIN, LOW);
	digitalWrite(FLYWHEEL_MOTOR_PLUS_PIN, LOW);
	digitalWrite(FLYWHEEL_MOTOR_MINUS_PIN, LOW);

	// Kill Stepper Motor
	turretMotor.killPower();
}

/**
 * @brief Turns the turret to the target angle
 *
 * @param targetDegrees the target angle in degrees [0, 360)
 */
void Turret::turnToAngle(float targetDegrees) {
	turretMotor.stepMotorToAngle(targetDegrees);
}

/**
 * @brief Sets the PWM for the Indexer Motor
 *
 * @param power the PWM value [0, 255]
 */
void Turret::setIndexerPower(int power) {
	// analogWrite(INDEXER_MOTOR_EN_PIN, power);
}

/**
 * @brief Sets the PWM for the Flywheel Motor
 *
 * @param power the PWM value [0, 255]
 */
void Turret::setFlywheelPower(int power) {
	// analogWrite(FLYWHEEL_MOTOR_EN_PIN, power);
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