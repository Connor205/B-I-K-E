#include <Arduino.h>
#include <ShufflerLibrary.hpp>

Shuffler shuffler = Shuffler();

void testHallEffectSensor() {
  int sensorValue = digitalRead(CONVEYER_HALL_EFFECT_PIN);
  digitalWrite(13, sensorValue);
}

void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT);
  pinMode(CONVEYER_HALL_EFFECT_PIN, INPUT);
}

void loop() {
  testHallEffectSensor();
}