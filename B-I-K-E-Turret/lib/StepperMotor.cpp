#include "StepperMotor.hpp"
#include <Arduino.h>
#include "TurretConstants.hpp"

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


float StepperMotor::degreeToSteps(float degree) {
	// Steps per revolution (set on driver)
	// Steps per revolution (SPR) -> angle (Degrees)
	// SPR * 1 / 360 = steps per degree * degree
	return (TURRET_STEPS_PER_REV / 360.0f) * degree;
}