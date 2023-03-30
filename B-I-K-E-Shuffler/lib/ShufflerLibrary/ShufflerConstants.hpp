#pragma once

#include <Arduino.h>

// Stepper Motor Constants
constexpr uint8_t ELEVATOR_STEP_PIN = 2;
constexpr uint8_t ELEVATOR_DIR_PIN = 3;
constexpr uint16_t ELEVATOR_MOTOR_MAX_STEPS_PER_SECOND = 10000;
constexpr uint16_t ELEVATOR_STEPS_PER_REVOLUTION = 3200; // Set on the digital driver

constexpr uint8_t DISPENSER_RAIL_STEP_PIN = 4;
constexpr uint8_t DISPENSER_RAIL_DIR_PIN = 5;
constexpr uint16_t DISPENSER_RAIL_MAX_STEPS_PER_SECOND = 3200;
constexpr uint16_t DISPENSER_RAIL_STEPS_PER_REVOLUTION = 6400; // Set on the digital driver

constexpr uint8_t BELT_STEP_PIN = 6;
constexpr uint8_t BELT_DIR_PIN = 7;
constexpr uint16_t BELT_MOTOR_MAX_STEPS_PER_SECOND = 3200;
constexpr uint16_t BELT_STEPS_PER_REVOLUTION = 6400; // Set on the digital driver

constexpr uint8_t DROPPER_MOTOR_STEP_PIN = 9;
constexpr uint8_t DROPPER_MOTOR_DIR_PIN = 8;
constexpr uint16_t DROPPER_MOTOR_MAX_STEPS_PER_SECOND = 1000;
constexpr uint16_t DROPPER_MOTOR_STEPS_PER_REVOLUTION = 3200; // Set on the digital driver

// Sensor Constants
constexpr uint8_t CONVEYER_HALL_EFFECT_PIN = 11;
constexpr uint8_t DISPENSER_RAIL_LIMIT_SWITCH_PIN = 12;
constexpr uint8_t ELEVATOR_LIMIT_SWITCH_PIN = 13;
// constexpr uint8_t CONFIRMATION_BUTTON_PIN = 13;

// Shuffler Constants
constexpr uint8_t DROPPER_DIAMETER = 11; // [mm] TUNE THIS VALUE
constexpr float DROPPER_MM_PER_REV = PI * DROPPER_DIAMETER; // [mm]
constexpr uint8_t DROPPER_MM_PER_CARD = 63; // [mm] TUNE THIS VALUE
constexpr uint16_t DROPPER_STEPS_PER_CARD = (DROPPER_MM_PER_CARD / DROPPER_MM_PER_REV) * DROPPER_MOTOR_STEPS_PER_REVOLUTION; // [steps]

constexpr uint8_t NUM_THREE_WIDE_LINKS = 8;
constexpr uint8_t NUM_TWO_WIDE_LINKS = (52 - NUM_THREE_WIDE_LINKS * 3) / 2; // 12

// Fuck it lets measure everything in steps

constexpr int DISPENSER_STEPS_TO_FIRST_LINK = 0;
constexpr float DISPENSER_MM_PER_REVOLUTION = 40.25f; // Find this value by testing
constexpr int DISPENSER_STEPS_PER_MM = DISPENSER_RAIL_STEPS_PER_REVOLUTION / DISPENSER_MM_PER_REVOLUTION;
constexpr int STEPS_PER_LINK = DISPENSER_STEPS_PER_MM * 11;

constexpr int STEPS_PER_WALL = DISPENSER_STEPS_PER_MM;
constexpr int STEPS_PER_THREE_WIDE_SLOT = DISPENSER_STEPS_PER_MM * 2;
constexpr int STEPS_PER_TWO_WIDE_SLOT = DISPENSER_STEPS_PER_MM * 3.5;

constexpr float BELT_MM_PER_REVOLUTION = 88.0f; // Find this value by testing, the length of the belt travelled in 1 stepper motor revolution
constexpr int BELT_STEPS_PER_MM = BELT_STEPS_PER_REVOLUTION / BELT_MM_PER_REVOLUTION; // This number should be pretty large

constexpr int BELT_LENGTH_MM = 1000; // Find this value by testing, the length of the belt in mm
constexpr int BELT_LENGTH_STEPS = BELT_LENGTH_MM * BELT_STEPS_PER_MM;