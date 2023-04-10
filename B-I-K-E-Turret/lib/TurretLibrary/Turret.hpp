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
    void powerIndexer(bool on, bool reverse = false);

    // Sensor Control
    float getTurretAngle();
    int getBarrelReading();
    bool cardInFlywheelBarrel();

    // Turret Actions
    void dealSingleCard(bool player = true);
    void dealToCommunity();

    void dealToPlayer(int playerNumber);
    void dealToAllPlayers();
    void dealFlop();
    void dealTurn();
    void dealRiver();
    void discard();

private:
    StepperMotor turretMotor;
};
