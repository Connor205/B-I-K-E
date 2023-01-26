#pragma once
#include "StepperMotor.hpp"

class Turret {
public:
	Turret();

	void init();
	void calibrate();

	void killAllPower();
	void turnToAngle(float targetDegrees);
	void powerFlywheel(float voltage);
	void powerIndexer(float voltage);
	void indexOneCard();

private:
	StepperMotor turretMotor;
	/* DC Motors*/
	/* Sensors*/
};