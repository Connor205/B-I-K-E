#pragma once

// Control Constants
constexpr float STEPS_PER_REV = 3200.0f;
constexpr float MAX_RPM = 100.0f;
constexpr float INDEXER_ONE_CARD_DELAY_MS = 2500; // TODO: Tune this value

// Stepper Motor Constants
constexpr float TURRET_OUTPUT_GEAR_RATIO = 1.0f;
constexpr float TURRET_STEP_PIN = 3;
constexpr float TURRET_DIR_PIN = 4;

// DC Motor Constants
constexpr int INDEXER_MOTOR_PLUS_PIN = 8;
constexpr int INDEXER_MOTOR_MINUS_PIN = 10;
constexpr int FLYWHEEL_MOTOR_PLUS_PIN = 9;
constexpr int FLYWHEEL_MOTOR_MINUS_PIN = 11;

// Sensor Constants
constexpr int INDEXER_ENCODER_A_PLUS_PIN = -1;
constexpr int INDEXER_ENCODER_A_MINUS_PIN = -1;
constexpr int INDEXER_ENCODER_B_PLUS_PIN = -1;
constexpr int INDEXER_ENCODER_B_MINUS_PIN = -1;
constexpr int MAGAZINE_SENSOR_PIN = -1; // Photoresistor
constexpr int FLYWHEEL_BARREL_SENSOR_PIN = -1; // Photoresistor