#include <Arduino.h>
#include <TurretLibrary.hpp>

Turret turret = Turret();

void testTurretRotate() {
  turret.turnToAngle(45);
  delay(2000);
  turret.turnToAngle(0);
  delay(2000);
  turret.turnToAngle(-90);
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

  delay(3000);
}

void loop() {
  testDCMotors();
}