#include "StepperMotor.hpp"
#include "TurretConstants.hpp"
#include <Arduino.h>

StepperMotor::StepperMotor(int stepPin, int dirPin, float outputGearRatio) {
	this->stepPin = stepPin;
	this->dirPin = dirPin;
	this->outputGearRatio = outputGearRatio;
}

void StepperMotor::init() {
	pinMode(stepPin, OUTPUT);
	pinMode(dirPin, OUTPUT);
}

void StepperMotor::calibrate() {}

void StepperMotor::killPower() {
	this->currentlyRunning = false;
}


float StepperMotor::degreeToSteps(float degree) {
	// Steps per revolution (set on driver)
	// Steps per revolution (SPR) -> angle (Degrees)
	// SPR * 1 / 360 = steps per degree * degree
	return (TURRET_STEPS_PER_REV / 360.0f) * degree;
}