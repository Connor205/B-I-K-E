#pragma once
#include "BaseStepper.hpp"

/*
So what can rotation steppers do. They are very simple. All they can do is rotate to a specific angle. This means that
we need to be able to calibrate them, we need to be able to set the 0 position. Then we need to be able to rotate in
various directions.
Notably these steppers will not rotate behind 180degrees. If you want something that moves in a continuous circle then
this is probaby not the right stepper class for you.
*/
class RotationStepper {
public:
    RotationStepper() = default;
    RotationStepper(int stepPin, int dirPin, int stepsPerRevolution);

    void init();
    void calibrate();

    void moveToAngle(float targetAngleDegrees);
    void setAngle(float targetAngleDegrees);
    void update();
    bool isMoving();

private:
    int stepsPerRevolution;
    BaseStepper stepper;
    int convertAngleToSteps(float targetAngleDegrees);
};
