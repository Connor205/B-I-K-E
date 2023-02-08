#include <Arduino.h>
#include <TurretLibrary.hpp>

Turret turret = new Turret();

void setup() {
  // put your setup code here, to run once:
  turret.init();
  turret.calibrate();

  turret.turnToAngle(45);
  turret.turnToAngle(0);
  turret.turnToAngle(-90);
  turret.turnToAngle(0);
}

void loop() {
  // put your main code here, to run repeatedly:
  turret.powerFlywheel(true);
  turret.powerIndexer(true);
  delay(1000);
  turret.powerFlywheel(false);
  turret.powerIndexer(false);
  delay(1000);
}