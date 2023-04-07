#pragma once
#include "RotationStepper.hpp"
#include <Arduino.h>

RotationStepper::RotationStepper(int stepPin, int dirPin, int stepsPerRevolution)
{
    this->stepsPerRevolution = stepsPerRevolution;
    this->stepper = BaseStepper(stepPin, dirPin);
}

void RotationStepper::init() { this->stepper.init(); }

void RotationStepper::calibrate() { this->stepper.calibrate(); }

int RotationStepper::convertAngleToSteps(float targetAngleDegrees)
{
    return (targetAngleDegrees / 360.0) * this->stepsPerRevolution;
}

void RotationStepper::moveToAngle(float targetAngleDegrees)
{
    this->stepper.setTarget(convertAngleToSteps(targetAngleDegrees));
    while (this->stepper.isMoving()) {
        this->stepper.update();
    }
}

void RotationStepper::setAngle(float targetAngleDegrees)
{
    this->stepper.setTarget(convertAngleToSteps(targetAngleDegrees));
}

void RotationStepper::update() { this->stepper.update(); }

bool RotationStepper::isMoving() { return this->stepper.isMoving(); }
