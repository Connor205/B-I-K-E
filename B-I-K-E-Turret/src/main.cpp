#include <Arduino.h>
#include <TurretConstants.hpp>
#include <Turret.hpp>

Turret turret = new Turret();

void setup() {
  // put your setup code here, to run once:
  turret.init();
  turret.calibrate();
}

void loop() {
  // put your main code here, to run repeatedly:
  turret.powerFlywheel(true);
  turret.powerIndexer(true);
  delay(2000);
  turret.powerFlywheel(false);
  turret.powerIndexer(false);
}