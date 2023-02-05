#pragma once

// Control Constants
constexpr float TURRET_STEPS_PER_REV = 400.0f;
constexpr float MAX_RPM = 75.0f;

// Motor Constants
constexpr float TURRET_OUTPUT_GEAR_RATIO = 1.0f;
constexpr float TURRET_STEP_PIN = 3;
constexpr float TURRET_DIR_PIN = 4;

/* DC Motor stuff */
constexpr int INDEXER_MOTOR_EN_PIN = 5;
constexpr int INDEXER_MOTOR_PLUS_PIN = 9;
constexpr int INDEXER_MOTOR_MINUS_PIN = 11;
constexpr int FLYWHEEL_MOTOR_EN_PIN = 6;
constexpr int FLYWHEEL_MOTOR_PLUS_PIN = 8;
constexpr int FLYWHEEL_MOTOR_MINUS_PIN = 10;

/* Sensor stuff */
constexpr int INDEXER_ENCODER_A_PLUS_PIN = -1;
constexpr int INDEXER_ENCODER_A_MINUS_PIN = -1;
constexpr int INDEXER_ENCODER_B_PLUS_PIN = -1;
constexpr int INDEXER_ENCODER_B_MINUS_PIN = -1;