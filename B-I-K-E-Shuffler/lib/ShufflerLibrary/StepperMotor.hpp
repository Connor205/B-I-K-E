#pragma once

class StepperMotor {
public:
    StepperMotor() = default;
    StepperMotor(int stepPin, int dirPin, int calibratePin, int maxSpeed);

    // Initialize
    void init();
    void calibrate(bool CW);

    // Getters
    float getTarget();
    float getSpeed();
    long getDelay();

    // Setters
    void setSpeed(float speed);
    void setDirection(bool CW);
    void setTarget(int targetStep);

    // State Methods
    bool isMoving();

    // Movement Methods
    void stepMotor();
    void update();
    void moveToTarget(long targetStep);
    void moveToTargetAccel(long targetStep);

    bool updateToTarget();

private:
    // Constructor Arguments
    int stepPin;
    int dirPin;
    int calibratePin;
    // Control Variables
    bool currentDir; // True -> CW, False -> CCW
    long current;
    long target;
    long previous;
    long previousChangeTime;
    bool currentlyRunning;
    long maxSpeed;
    float currentSpeed;
    long currentDelay;
    // Private methods
    long getDelayFromSpeed(float s);
};