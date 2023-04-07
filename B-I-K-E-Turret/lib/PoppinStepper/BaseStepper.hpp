#pragma once

class BaseStepper {
public:
    BaseStepper() = default;
    BaseStepper(int stepPin, int dirPin);

    void init();
    void calibrate();

    long getTarget();
    float getSpeed();

    void setDirection(bool CW);
    void setTarget(long targetStep);

    bool isMoving();

    void stepMotor();
    void update();
    void moveToTarget(long targetStep);

private:
    int stepPin;
    int dirPin;
    bool currentDir; // True -> CW, False -> CCW
    long current;
    long target;
    long previous;
    long intendedLastChange;
    long actualLastChange;

    long currentDelay;
    bool currentlyHigh;
};
