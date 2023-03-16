#pragma once

class StepperMotor {
public:
    StepperMotor() = default;
    StepperMotor(int stepPin, int dirPin, float outputGearRatio, int maxSpeed);

    // Initialize
    void init();
    void calibrate();

    // Getters
    float getTarget();
    float getSpeed();
    long getDelay();
    float getOutputGearRatio();

    // Setters
    void setSpeed(float speed);
    void setDirection(bool CW);
    void setTarget(int targetStep);

    // State Methods
    bool isMoving();

    // Movement Methods
    void stepMotor();
    void update();
    void moveToTarget(int targetStep);
    void moveToTargetAccel(int targetStep);

    bool updateToTarget();

private:
    // Constructor Arguments
    int stepPin;
    int dirPin;
    float outputGearRatio;
    // Control Variables
    bool currentDir; // True -> CW, False -> CCW
    int current;
    float currentAngle;
    int target;
    int previous;
    long previousChangeTime;
    bool currentlyRunning;
    long maxSpeed;
    float currentSpeed;
    long currentDelay;
    // Private methods
    void setAngle();
    float degreeToSteps(float targetAngleDegrees);
    long getDelayFromSpeed(float s);
};