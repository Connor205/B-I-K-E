#pragma once
#include <Arduino.h>

// Stepper Motor Constants
constexpr uint8_t TURRET_STEP_PIN = 2;
constexpr uint8_t TURRET_DIR_PIN = 3;
constexpr uint16_t STEPS_PER_REV = 6400;
constexpr float TURRET_BASE_RPM = 30.0f; // RPM of the base motor
constexpr int TURRET_MAX_SPEED = STEPS_PER_REV * TURRET_BASE_RPM / 60.0f;

// DC Motor Constants
constexpr int INDEXER_MOTOR_PLUS_PIN = 11;
constexpr int INDEXER_MOTOR_MINUS_PIN = 10;
constexpr int FLYWHEEL_MOTOR_PLUS_PIN = 9;
constexpr int FLYWHEEL_MOTOR_MINUS_PIN = 8;

// Sensor Constants
constexpr uint8_t TURRET_HALL_EFFECT_PIN = 4;
// constexpr uint8_t INDEXER_ENCODER_A_PLUS_PIN = 4;
// constexpr uint8_t INDEXER_ENCODER_A_MINUS_PIN = 5;
// constexpr uint8_t INDEXER_ENCODER_B_PLUS_PIN = 6;
// constexpr uint8_t INDEXER_ENCODER_B_MINUS_PIN = 7;
constexpr uint8_t FLYWHEEL_BARREL_SENSOR_PIN = A0; // Photoresistor
constexpr uint8_t FLYWHEEL_BARREL_SENSOR_THRESHOLD = 10; // Below this value is considered a card
constexpr uint8_t CONFIRMATION_BUTTON_PIN = 12;

constexpr uint8_t INDEXER_SPEED_PIN = 5;

constexpr float PLAYER0_ANGLE = 180.0f;
constexpr float PLAYER1_ANGLE = 110.0f;
constexpr float PLAYER2_ANGLE = 60.0f;
constexpr float PLAYER3_ANGLE = 0.0f;

constexpr float PLAYER_ANGLES[] = { PLAYER0_ANGLE, PLAYER1_ANGLE, PLAYER2_ANGLE, PLAYER3_ANGLE };
