#pragma once
#include "StepperMotor.hpp"

class Turret {
public:
	Turret();

	// Initialize
	void init();
	void calibrate();
	void killAllPower();

	// Motor Control
	void turnToAngle(float targetDegrees);
	void setIndexerPower(int power);
	void setFlywheelPower(int power);
	void powerFlywheel(bool on);
	void powerIndexer(bool on);

	// Sensor Control
	float getTurretAngle();
	float getDistance();
	bool cardInMagazine();

private:
	StepperMotor turretMotor;
};
