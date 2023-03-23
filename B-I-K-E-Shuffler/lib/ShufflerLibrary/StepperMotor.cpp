#include "StepperMotor.hpp"
#include <Arduino.h>

StepperMotor::StepperMotor(int stepPin, int dirPin, int calibratePin, int maxSpeed) {
    this->stepPin = stepPin;
    this->dirPin = dirPin;
    this->calibratePin = calibratePin;
    this->maxSpeed = maxSpeed;
}

void StepperMotor::init() {
    // Setup pins
    pinMode(stepPin, OUTPUT);
    pinMode(dirPin, OUTPUT);
    // TODO: Remove pullup if Hall-Effect sensor is active low (and remove ! in calibrate() method)
    pinMode(calibratePin, INPUT_PULLUP);

    // Setup default values
    this->current = 0;
    this->target = 0;
    this->currentSpeed = 0;
    this->currentDelay = getDelayFromSpeed(this->currentSpeed);
    this->previousChangeTime = micros();
    this->currentlyRunning = false;
}

void StepperMotor::calibrate() {
    if (this->calibratePin == -1) {
        // No Calibration Pin
        return;
    }
    setDirection(true);
    setSpeed(this->maxSpeed / 4); // Run at slower speed
    while (!digitalRead(this->calibratePin)) {
        stepMotor();
    }
}

float StepperMotor::getTarget() { return this->target; }
float StepperMotor::getSpeed() { return this->currentSpeed; }
long StepperMotor::getDelay() { return this->currentDelay; }

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
    if (isMoving()) {
        return; // Motor is currently moving
    }
    this->previous = this->current;
    this->target = targetStep;
    setDirection(this->target > this->current); // True -> CW, False -> CCW
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
 * and the time the motor was last pulsed. Updates current step
 * as motion occurs.
 *
 */
void StepperMotor::update() {
    // If the motor has reached its target, do nothing
    if (this->current == this->target) {
        return;
    }
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
    for (int i = 0; i < stepsToMove; i++) {
        stepMotor();
    }
    this->current = targetStep;
}

void StepperMotor::moveToTargetAccel(int targetStep) {
    // So this shit is mad basic. We are going to do a trapazoidal velocity profile
    // We will start at 0 and accelerate to a max speed, then decelerate to 0
    setDirection(targetStep > this->current); // True -> CW, False -> CCW
    int stepsToMove = abs(targetStep - this->current);
    int quarterSteps = stepsToMove / 4;
    for (int i = 0; i < stepsToMove / 4; i++) {
        setSpeed(maxSpeed * (float(i) / quarterSteps));
        stepMotor();
    }

    for (int i = 0; i < stepsToMove / 2 + stepsToMove % 4; i++) {
        setSpeed(maxSpeed);
        stepMotor();
    }

    for (int i = 0; i < stepsToMove / 4; i++) {
        setSpeed(maxSpeed * (1.0 - (float(i) / quarterSteps)));
        stepMotor();
    }

    this->current = targetStep;
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
    if (this->current == this->target) {
        return true;
    }
    while (this->current != this->target) {
        update();
    }
    return true;
}

/**
 * @brief Given a speed in steps per second, calculates the delay in microseconds
 * 			  between steps required to achieve that speed
 *
 * @param speed speed of the motor [steps per second]
 * @return long representing the delay in microseconds between steps
 */
long StepperMotor::getDelayFromSpeed(float speed) { return (long)(1000000.0f / speed); }