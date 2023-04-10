#include "Turret.hpp"
#include "TurretConstants.hpp"
#include <Arduino.h>
#include <Utils.h>

Turret::Turret()
{
    this->turretMotor = StepperMotor(TURRET_STEP_PIN, TURRET_DIR_PIN, TURRET_HALL_EFFECT_PIN, TURRET_MAX_SPEED);
}

void Turret::init()
{
    // Init Turret StepperMotor
    this->turretMotor.init();

    // Initialize DC Motor Pins
    pinMode(INDEXER_MOTOR_PLUS_PIN, OUTPUT);
    pinMode(INDEXER_MOTOR_MINUS_PIN, OUTPUT);
    pinMode(FLYWHEEL_MOTOR_PLUS_PIN, OUTPUT);
    pinMode(FLYWHEEL_MOTOR_MINUS_PIN, OUTPUT);
    pinMode(INDEXER_SPEED_PIN, OUTPUT);

    // // Intialize Sensor Pins
    // pinMode(INDEXER_ENCODER_A_PLUS_PIN, INPUT);
    // pinMode(INDEXER_ENCODER_A_MINUS_PIN, INPUT);
    // pinMode(INDEXER_ENCODER_B_PLUS_PIN, INPUT);
    // pinMode(INDEXER_ENCODER_B_MINUS_PIN, INPUT);
    pinMode(FLYWHEEL_BARREL_SENSOR_PIN, INPUT);
    analogWrite(INDEXER_SPEED_PIN, 255);

    // Turn off motors
    killAllPower();
}

void Turret::calibrate()
{
    this->turretMotor.calibrate();
    this->turretMotor.current = this->turretMotor.degreeToSteps(90);
}

void Turret::killAllPower()
{
    digitalWrite(INDEXER_MOTOR_PLUS_PIN, LOW);
    digitalWrite(INDEXER_MOTOR_MINUS_PIN, LOW);
    digitalWrite(FLYWHEEL_MOTOR_PLUS_PIN, LOW);
    digitalWrite(FLYWHEEL_MOTOR_MINUS_PIN, LOW);
}

/**
 * @brief Turns the turret motor to face the target angle
 *
 * @param targetDegrees the target angle in degrees [90, -90])
 */
void Turret::turnToAngle(float targetDegrees)
{
    if (targetDegrees > 180.0f) {
        writeError("Target angle too large, clamping to 180 degrees:" + String(targetDegrees));
        targetDegrees = 180.0f;
    } else if (targetDegrees < 0.0f) {
        writeError("Target angle too small, clamping to 0 degrees:" + String(targetDegrees));
        targetDegrees = 0.0f;
    }
    this->turretMotor.moveToAngle(targetDegrees);
}

/**
 * @brief Powers the flywheel motor on or off
 *
 * @param on true -> on, false -> off
 */
void Turret::powerFlywheel(bool on)
{
    if (on) {
        digitalWrite(FLYWHEEL_MOTOR_PLUS_PIN, LOW);
        digitalWrite(FLYWHEEL_MOTOR_MINUS_PIN, HIGH);
    } else {
        digitalWrite(FLYWHEEL_MOTOR_PLUS_PIN, LOW);
        digitalWrite(FLYWHEEL_MOTOR_MINUS_PIN, LOW);
    }
}

/**
 * @brief Powers the indexer motor on or off
 *
 * @param on true -> on, false -> off
 * @param reverse true -> reversed, false -> forward, false by default
 */
void Turret::powerIndexer(bool on, bool reverse)
{
    if (on && !reverse) {
        digitalWrite(INDEXER_MOTOR_PLUS_PIN, LOW);
        digitalWrite(INDEXER_MOTOR_MINUS_PIN, HIGH);
    } else if (on && reverse) {
        digitalWrite(INDEXER_MOTOR_PLUS_PIN, HIGH);
        digitalWrite(INDEXER_MOTOR_MINUS_PIN, LOW);
    } else {
        digitalWrite(INDEXER_MOTOR_PLUS_PIN, LOW);
        digitalWrite(INDEXER_MOTOR_MINUS_PIN, LOW);
    }
}

float Turret::getTurretAngle() { return this->turretMotor.getCurrentAngle(); }

bool Turret::cardInFlywheelBarrel() { return this->getBarrelReading() > FLYWHEEL_BARREL_SENSOR_THRESHOLD; }

/*Generates a value between 0 and 1023 for the barrel sensor */
int Turret::getBarrelReading()
{
    int sensorValue = analogRead(FLYWHEEL_BARREL_SENSOR_PIN);
    return map(sensorValue, 0, 1023, 0, 255);
}

void Turret::dealSingleCard(bool player)
{
    analogWrite(INDEXER_SPEED_PIN, 1023);
    this->powerFlywheel(true);
    delay(100);
    this->powerIndexer(true);
    while (this->cardInFlywheelBarrel()) {
        // writeInfo("Waiting for card to leave barrel" + String(this->getBarrelReading()));
        delay(5);
    }
    this->powerIndexer(true, true);
    delay(500);
    this->powerIndexer(false);
}

void Turret::dealToCommunity()
{
    analogWrite(INDEXER_SPEED_PIN, 210);
    this->powerFlywheel(true);
    delay(100);
    this->powerIndexer(true);
    while (this->cardInFlywheelBarrel()) {
        // writeInfo("Waiting for card to leave barrel" + String(this->getBarrelReading()));
        delay(5);
    }
    this->powerIndexer(true, true);
    delay(500);
    this->powerIndexer(false);
}

void Turret::dealFlop()
{
    this->turnToAngle(120);
    delay(100);
    this->dealToCommunity();
    this->turnToAngle(105);
    delay(100);
    this->dealToCommunity();
    this->turnToAngle(90);
    delay(100);
    this->dealToCommunity();
}

void Turret::dealTurn()
{
    this->turnToAngle(75);
    delay(100);
    this->dealToCommunity();
}

void Turret::dealRiver()
{
    this->turnToAngle(60);
    delay(100);
    this->dealToCommunity();
}

void Turret::dealToPlayer(int playerNumber)
{
    if (playerNumber < 0 || playerNumber > 3) {
        writeError("Invalid player number, must be between 0 and 3");
        return;
    }
    this->turnToAngle(PLAYER_ANGLES[playerNumber]);
    delay(100);
    this->dealSingleCard();
}

void Turret::discard()
{
    this->turnToAngle(180);
    delay(100);
    this->dealToCommunity();
}

void Turret::dealToAllPlayers()
{
    for (int i = 0; i < 4; i++) {
        this->dealToPlayer(i);
    }
}