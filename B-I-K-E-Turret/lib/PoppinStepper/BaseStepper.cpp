#include "BaseStepper.hpp"
#include <Arduino.h>

BaseStepper::BaseStepper(int stepPin, int dirPin)
{
    this->stepPin = stepPin;
    this->dirPin = dirPin;
}

void BaseStepper::init()
{
    // Setup pins
    pinMode(stepPin, OUTPUT);
    pinMode(dirPin, OUTPUT);

    // Setup default values
    this->current = 0;
    this->target = 0;
    this->previous = 0;
    this->currentDir = true;
    this->intendedLastChange = micros();
}

// TODO:: Implement Calibration
void BaseStepper::calibrate() { }

long BaseStepper::getTarget() { return this->target; }

void BaseStepper::setDirection(bool CW)
{
    if (CW) {
        digitalWrite(this->dirPin, HIGH);
        this->currentDir = true;
    } else {
        digitalWrite(this->dirPin, LOW);
        this->currentDir = false;
    }
}

void BaseStepper::setTarget(long targetStep)
{
    if (isMoving()) {
        return; // Motor is currently moving
    }
    this->previous = this->current;
    this->target = targetStep;
    setDirection(this->target > this->current);
}

bool BaseStepper::isMoving() { return this->current != this->target; }

void BaseStepper::stepMotor()
{
    digitalWrite(this->stepPin, HIGH);
    delayMicroseconds(this->currentDelay);
    digitalWrite(this->stepPin, LOW);
    delayMicroseconds(this->currentDelay);
}

void BaseStepper::update()
{
    if (!isMoving()) {
        return;
    }
    long currentTime = micros();
    long timeSinceLastChange = currentTime - this->intendedLastChange;
    if (timeSinceLastChange >= this->currentDelay) {
        this->intendedLastChange = this->intendedLastChange + this->currentDelay;
        this->actualLastChange = currentTime;
        this->current += this->currentDir ? 1 : -1;
        if (this->currentlyHigh) {
            digitalWrite(this->stepPin, LOW);
        } else {
            digitalWrite(this->stepPin, HIGH);
        }
        this->currentlyHigh = !this->currentlyHigh;
    }
}

void BaseStepper::moveToTarget(long targetStep)
{
    setTarget(targetStep);
    while (isMoving()) {
        update();
    }
}
