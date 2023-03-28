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
    void powerFlywheel(bool on);
    void powerIndexer(bool on);
    void reverseIndexer();

    // Sensor Control
    float getTurretAngle();
    int getBarrelReading();
    bool cardInMagazine();
    bool cardInFlywheelBarrel();

    // Turret Actions
    void dealSingleCard();

private:
    StepperMotor turretMotor;
};
