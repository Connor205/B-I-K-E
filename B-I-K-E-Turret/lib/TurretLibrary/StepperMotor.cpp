#include "StepperMotor.hpp"
#include "TurretConstants.hpp"
#include <Arduino.h>

StepperMotor::StepperMotor(int stepPin, int dirPin, float outputGearRatio) {
	this->stepPin = stepPin;
	this->dirPin = dirPin;
	this->outputGearRatio = outputGearRatio;
}

void StepperMotor::init() {
	// Setup pins
	pinMode(stepPin, OUTPUT);
	pinMode(dirPin, OUTPUT);

	// Setup default values
	this->current = 0;
	this->currentAngle = 0.0f;
	this->target = 0;
	this->currentSpeed = STEPS_PER_REV * MAX_RPM * (1.0f / 60.0f);
	this->currentDelay = getDelayFromSpeed(this->currentSpeed);
	this->previousChangeTime = micros();
	this->currentlyRunning = false;
}

void StepperMotor::calibrate() {/* TODO */ }

/**
 * @brief Regardless of the current state of the motor, this method will stop the motor
 *
 */
void StepperMotor::killPower() {
	digitalWrite(this->stepPin, LOW);
	this->target = this->current;
}

float StepperMotor::getTarget() { return this->target; }
float StepperMotor::getSpeed() { return this->currentSpeed; }
long StepperMotor::getDelay() { return this->currentDelay; }
float StepperMotor::getOutputGearRatio() { return this->outputGearRatio; }
float StepperMotor::getCurrentAngle() { return this->currentAngle; }

/**
 * @brief Sets the speed [steps per sec] and calculates the required pulse delay
 *
 * @param speed speed in steps per second
 */
void StepperMotor::setSpeed(float speed) {
	this->currentSpeed = speed;
	this->currentDelay = getDelayFromSpeed(this->currentSpeed);
}

/**
 * @brief Sets the direction of the motor's direction pin
 *
 * @param CW True -> CW, False -> CCW
 */
void StepperMotor::setDirection(bool CW) {
	// TODO: Ensure directions are correct
	if (CW) {
		digitalWrite(this->dirPin, HIGH);
	} else { // CCW
		digitalWrite(this->dirPin, LOW);
	}
	this->currentDir = CW;
}

/**
 * @brief Sets the target to the given target step. Also sets direction.
 *
 * @note This metod does not move the motor. It only sets the target and direction.
 * 			 This method will not update the target if the motor is currently moving.
 *
 * @param targetStep the absolute target step
 */
void StepperMotor::setTarget(int targetStep) {
	if (this->current != this->target) {
		return; // Motor is currently moving
	}
	this->previous = this->current;
	this->target = targetStep * this->outputGearRatio;
	setDirection(this->target > this->current); // True -> CW, False -> CCW
}

/**
 * @brief Sets the target to the given target angle. Also sets direction.
 * 			 	This method converts the given target angle to steps and then calls
 * 				setTarget(int targetStep)
 *
 * @note This metod does not move the motor. It only sets the target and direction.
 * 			 This method will not update the target if the motor is currently moving.
 *
 * @param targetAngleDegrees the absolute target angle
 */
void StepperMotor::setTargetAngle(float targetAngleDegrees) {
	int steps = round(degreeToSteps(targetAngleDegrees));
	setTarget(steps);
}

/**
 * @brief Sets the current angle of the motor based on the current step
 *
 */
void StepperMotor::setAngle() {
	// TODO: Verify this math
	this->currentAngle = (this->current / (STEPS_PER_REV * this->outputGearRatio)) * 360.0f;
}

bool StepperMotor::isMoving() { return this->current != this->target; }

/**
 * @brief Provides a pulse to the motor using the current delay calculated from the current speed
 *
 */
void StepperMotor::stepMotor() {
	digitalWrite(this->stepPin, HIGH);
	delayMicroseconds(this->currentDelay);
	digitalWrite(this->stepPin, LOW);
	delayMicroseconds(this->currentDelay);
}

/**
 * @brief Primary function to be used for non-blocking motion.
 * This method will be called multiple times per second and will
 * determine when to step the motor given the current time of the program
 * and the time the motor was last pulsed. Updates current and currentAngle
 * as motion occurs.
 *
 */
void StepperMotor::update() {
	// If the motor has reached its target, do nothing
	if (this->current == this->target) { return; }
	// Determine time since last step
	long currentTime = micros();
	long timeSinceLastStep = currentTime - this->previousChangeTime;
	if (timeSinceLastStep > this->currentDelay) {
		// Swap HIGH/LOW pulse on every occurance of passing the delay
		this->currentlyRunning = !this->currentlyRunning;
		if (this->currentlyRunning) {
			digitalWrite(this->stepPin, HIGH);
		} else {
			digitalWrite(this->stepPin, LOW);
		}
		this->previousChangeTime = currentTime;
		// Speed can be reset here provided an speed curve
		// long newSpeed = getSpeedCurve(stepsMoved, totalSteps);
		// setSpeed(newSpeed);
		if (!this->currentlyRunning) {
			// Increment steps during LOW pulse
			if (this->current < this->target) { // CW
				this->current++;
			} else { // CCW
				this->current--;
			}
			setAngle(); // Recalculate angle as steps are incremented
		}
	}
}

/**
 * @brief Given a target step (negative steps allowed), calculates the number of steps and direction,
 *        and steps the motor towards the target.
 * @note This is a blocking function and will only allow for this movement to be executed.
 *
 * @param targetStep the target step to acheive. Represents an absolute position
 */
void StepperMotor::moveToTarget(int targetStep) {
	setDirection(targetStep > this->current); // True -> CW, False -> CCW
	int stepsToMove = abs(targetStep - this->current);
	for (int i = 0; i < stepsToMove; i++) { stepMotor(); }
	this->current = targetStep;
	setAngle();
}

/**
 * @brief A more practical moveTo() function taking in a target angle.
 * This method calls moveTo(int targetStep) after translating the given angle to steps.
 *
 * @param targetAngle the target angle in degrees
 */
void StepperMotor::moveToAngle(float targetAngleDegrees) {
	float stepsInAngle = round(degreeToSteps(targetAngleDegrees));
	moveToTarget(stepsInAngle);
}

/**
 * @brief Calls update() until the current step has met the target step
 *
 * @note This method is blocking and will not return until the motor has reached its target.
 * 			 This method simply runs update() until the current step meets the target step.
 *
 * @return true on function termination
 */
bool StepperMotor::updateToTarget() {
	if (this->current == this->target) { return true; }
	while (this->current != this->target) { update(); }
	return true;
}

/**
 * @brief Given a speed in steps per second, calculates the delay in microseconds
 * 			  between steps required to achieve that speed
 *
 * @param speed speed of the motor [steps per second]
 * @return long representing the delay in microseconds between steps
 */
long StepperMotor::getDelayFromSpeed(float speed) {
	return (long)(1000000.0f / s);
}

/**
 * @brief Given an angle in degrees, converts it to a number of steps for the output
 *
 * @param degree angle to convert to steps to accomplish that angle [0,360)
 * @return float representing the number of steps to accomplish that angle
 */
float StepperMotor::degreeToSteps(float degree) {
	// Steps per revolution (set on driver)
	// Steps per revolution (SPR) -> angle (Degrees)
	// SPR * 1 / 360 = steps per degree * degree
	return ((STEPS_PER_REV / 360.0f) * degree) * this->outputGearRatio;
}