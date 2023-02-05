#pragma once
#include "StepperMotor.hpp"

class Turret {
public:
	Turret();

	void init();
	void calibrate();
	void killAllPower();

	void turnToAngle(float targetDegrees);
	void setIndexerPower(int power);
	void setFlywheelPower(int power);
	void powerFlywheel(bool on);
	void powerIndexer(bool on);

private:
	StepperMotor turretMotor;
	/* DC Motors*/
	/* Sensors*/
};