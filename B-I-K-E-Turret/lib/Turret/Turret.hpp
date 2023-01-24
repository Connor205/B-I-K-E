#pragma once
#include "StepperMotor.hpp"

class Turret {
public:
	Turret();

	// Initalize
	void init();
	void calibrate();

	// Getters
private:
	StepperMotor turretMotor;
	/* DC Motors*/
};
