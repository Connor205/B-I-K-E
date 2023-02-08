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
	void indexOneCard();

	// Sensor Control
	float getTurretAngle();
	bool cardInMagazine();
	bool cardInFlywheelBarrel();

private:
	StepperMotor turretMotor;

	void setIndexerPower(int power);
	void setFlywheelPower(int power);
	void powerFlywheel(bool on);
	void powerIndexer(bool on);
};
