#include <Arduino.h>
#include <TurretLibrary.hpp>

Turret turret;

void setup() {
  // put your setup code here, to run once:
  turret.init();
  turret.calibrate();
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