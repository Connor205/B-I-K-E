#include <Arduino.h>
#include <TurretLibrary.hpp>
#include <Vector.h>

Turret turret = Turret();
long now = millis();

void testTurretRotate(Vector<float> angles) {
  for (int i = 0; i < angles.size(); i++) {
    turret.turnToAngle(angles[i]);
    delay(2000);
  }
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
}

void loop() {
  // testDCMotors();
  Vector<float> angles = Vector<float>();
  angles.push_back(90);
  angles.push_back(180);
  angles.push_back(270);
  angles.push_back(0);
  testTurretRotate(angles);
}