#pragma once

class StepperMotor {
public:
	StepperMotor() = default;
	StepperMotor(int stepPin, int dirPin, float outputGearRatio);

	// Initialize
	void init();
	void calibrate();
	void killPower();

	// Getters
	float getTarget();
	float getSpeed();
	long getDelay();
	float getOutputGearRatio();
	float getCurrentAngle();

	// Setters
	void setSpeed(float speed);
	void setDirection(bool CW);
	void setTarget(int targetStep);

	// Updating Methods
	void updateAngle();
	void updateMotor();
	void updateUntilTarget();

	// StepperMotor Methods
	void stepMotorOnce();
	void stepMotorToTarget(int targetStep);
	void stepMotorToAngle(float targetAngleDegrees);

	// Math Methods
	float degreeToSteps(float targetAngleDegrees);

private:
	// Constructor Arguments
	int stepPin;
	int dirPin;
	float outputGearRatio;
	// Control Variables
	bool currentDir;  // True -> CW, False -> CCW
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
	long getDelayFromSpeed(float s);
};