#pragma once

#include <Arduino.h>

// Stepper Motor Constants
constexpr int DISPENSER_STEP_PIN = 2;
constexpr int DISPENSER_DIR_PIN = 3;
constexpr float DISPENSER_OUTPUT_GEAR_RATIO = 1.0f;
constexpr int DISPENSER_MOTOR_MAX_STEPS_PER_SECOND = 1000;

constexpr int BELT_STEP_PIN = 4;
constexpr int BELT_DIR_PIN = 5;
constexpr float BELT_OUTPUT_GEAR_RATIO = 1.0f;
constexpr int BELT_MOTOR_MAX_STEPS_PER_SECOND = 1000;

// DC Motor Constants
constexpr int DISPENSER_MOTOR_PLUS_PIN = 11;
constexpr int DISPENSER_MOTOR_MINUS_PIN = 10;

// Sensor Constants
constexpr int DISPENSER_PHOTORESISTOR_PIN = A0;
constexpr int DISPENSER_MOTOR_ENCODER_A_PIN = 6;
constexpr int DISPENSER_MOTOR_ENCODER_B_PIN = 7;

// Shuffler Constants
constexpr int NUM_THREE_WIDE_LINKS = 10;
constexpr int NUM_TWO_WIDE_LINKS = (52 - NUM_THREE_WIDE_LINKS * 3) / 2;

// Fuck it lets measure everything in steps

constexpr int STEPS_TO_FIRST_LINK = 0;
constexpr int STEPS_PER_MM = 1; // This number should be pretty large

constexpr int STEPS_PER_LINK = STEPS_PER_MM * 11;

constexpr int STEPS_PER_WALL = STEPS_PER_MM;
constexpr int STEPS_PER_THREE_WIDE_SLOT = STEPS_PER_MM * 2;
constexpr int STEPS_PER_TWO_WIDE_SLOT = STEPS_PER_MM * 3.5;

constexpr int STEPS_PER_MM_BELT = 1; // This number should be pretty large

constexpr int BELT_LENGTH_MM = 1000;
constexpr int BELT_LENGTH_STEPS = BELT_LENGTH_MM * STEPS_PER_MM_BELT;