#pragma once
#include <Arduino.h>

// Stepper Motor Constants
constexpr uint8_t TURRET_STEP_PIN = 2;
constexpr uint8_t TURRET_DIR_PIN = 3;

constexpr uint16_t STEPS_PER_REV = 3200;
constexpr float MAX_RPM = 100.0f;

// DC Motor Constants
constexpr int INDEXER_MOTOR_PLUS_PIN = 11;
constexpr int INDEXER_MOTOR_MINUS_PIN = 10;
constexpr int FLYWHEEL_MOTOR_PLUS_PIN = 9;
constexpr int FLYWHEEL_MOTOR_MINUS_PIN = 8;

// Sensor Constants
constexpr uint8_t INDEXER_ENCODER_A_PLUS_PIN = 4;
constexpr uint8_t INDEXER_ENCODER_A_MINUS_PIN = 5;
constexpr uint8_t INDEXER_ENCODER_B_PLUS_PIN = 6;
constexpr uint8_t INDEXER_ENCODER_B_MINUS_PIN = 7;
constexpr uint8_t MAGAZINE_SENSOR_PIN = A1; // Photoresistor
constexpr uint8_t FLYWHEEL_BARREL_SENSOR_PIN = A0; // Photoresistor
constexpr uint8_t FLYWHEEL_BARREL_SENSOR_THRESHOLD = 3;