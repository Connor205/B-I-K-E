#include <Arduino.h>
#include <TurretLibrary.hpp>
#include <Vector.h>

Turret turret = Turret();
long now = millis();

Vector<float> angles = Vector<float>();


void testTurretRotate(Vector<float> angles) {
  // for (int i = 0; i < angles.size(); i++) {

  //   delay(2000);
  // }
  turret.turnToAngle(90);
  delay(2000);
  turret.turnToAngle(45);
  delay(2000);
  turret.turnToAngle(0);
  delay(2000);
}

void testDCMotors() {
  turret.powerFlywheel(true);
  turret.powerIndexer(true);
  delay(2000);
  turret.powerFlywheel(false);
  turret.powerIndexer(false);
  delay(2000);
}

void setup() {
  turret.init();
  turret.calibrate();

  angles.push_back(90);
  angles.push_back(180);
  angles.push_back(270);
  angles.push_back(0);
}

void loop() {
  // testDCMotors();
  testTurretRotate(angles);
}