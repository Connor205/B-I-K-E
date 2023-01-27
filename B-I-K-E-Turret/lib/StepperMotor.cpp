#include "StepperMotor.hpp"
#include "TurretConstants.hpp"


float StepperMotor::degreeToSteps(float degree) {
	// Steps per revolution (set on driver)
	// Steps per revolution (SPR) -> angle (Degrees)
	// SPR * 1 / 360 = steps per degree * degree
	return (STEPS_PER_REV / 360.0f) * degree;
}