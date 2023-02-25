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
    void powerFlywheel(bool on);
    void powerIndexer(bool on);

    // Sensor Control
    float getTurretAngle();
    int getBarrelReading();
    bool cardInMagazine();
    bool cardInFlywheelBarrel();

    void dealSingleCard();

private:
    StepperMotor turretMotor;
};
