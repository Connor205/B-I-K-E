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
	pinMode(ULTRASONIC_TRIG_PIN, OUTPUT);
	pinMode(ULTRASONIC_ECHO_PIN, INPUT);

	// Turn off motors
	killAllPower();
}

void Turret::calibrate() {
	this->turretMotor.calibrate();
}


void Turret::killAllPower() {
	// Kill DC Motors
	digitalWrite(INDEXER_MOTOR_PLUS_PIN, LOW);
	digitalWrite(INDEXER_MOTOR_MINUS_PIN, LOW);
	digitalWrite(FLYWHEEL_MOTOR_PLUS_PIN, LOW);
	digitalWrite(FLYWHEEL_MOTOR_MINUS_PIN, LOW);

	// Kill Stepper Motor
	this->turretMotor.killPower();
}

/**
 * @brief Turns the turret motor to face the target angle
 *
 * @param targetDegrees the target angle in degrees [0, 360)
 */
void Turret::turnToAngle(float targetDegrees) {
	this->turretMotor.moveToAngle(targetDegrees);
}

/**
 * @brief Sets the PWM for the Indexer Motor
 *
 * @param power the PWM value [0, 255]
 */
void Turret::setIndexerPower(int power) {
	analogWrite(INDEXER_MOTOR_EN_PIN, power);
}

/**
 * @brief Sets the PWM for the Flywheel Motor
 *
 * @param power the PWM value [0, 255]
 */
void Turret::setFlywheelPower(int power) {
	analogWrite(FLYWHEEL_MOTOR_EN_PIN, power);
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

/**
 * @brief Gets the distance the ultrasonic sensor is reading [cm]
 *
 * @return float in centimeters representing the distance
 */
float Turret::getDistance() {
	long duration, cm;
	digitalWrite(ULTRASONIC_TRIG_PIN, LOW);
	delayMicroseconds(2);
	digitalWrite(ULTRASONIC_TRIG_PIN, HIGH);
	delayMicroseconds(10);
	digitalWrite(ULTRASONIC_TRIG_PIN, LOW);
	duration = pulseIn(ULTRASONIC_ECHO_PIN, HIGH);
	cm = duration / 29 / 2;
	return cm;
}

bool Turret::cardInMagazine() {
	return digitalRead(MAGAZINE_SENSOR_PIN);
}