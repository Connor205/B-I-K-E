#include "Turret.hpp"
#include "TurretConstants.hpp"
#include <Arduino.h>

Turret::Turret() {
	this->turretMotor = StepperMotor(TURRET_STEP_PIN, TURRET_DIR_PIN, TURRET_OUTPUT_GEAR_RATIO);
}

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
 * @param targetDegrees the target angle in degrees [0, 360)
 */
void Turret::turnToAngle(float targetDegrees) { this->turretMotor.moveToAngle(targetDegrees); }

/**
 * @brief Indexes one card into the flywheel barrel by
 * 				powering the indexer motor for a certain amount of time
 *
 */
void Turret::indexOneCard() {
	if (this->cardInMagazine()) {
		this->powerIndexer(true);
		delay(INDEXER_ONE_CARD_DELAY_MS);
		this->powerIndexer(false);
	} else {
		Serial.println("No card in magazine, cannot index a card");
	}
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
bool Turret::cardInFlywheelBarrel() { return digitalRead(FLYWHEEL_BARREL_SENSOR_PIN); }