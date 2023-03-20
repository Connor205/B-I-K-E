#include <Arduino.h>
#include <ShufflerLibrary.hpp>

Shuffler shuffler = Shuffler();

void testHallEffectSensor() {
  int sensorValue = digitalRead(CONVEYER_HALL_EFFECT_PIN);
  if (sensorValue == LOW) {
    digitalWrite(13, HIGH);
  } else {
    digitalWrite(13, LOW);
  }
}

void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT);
  pinMode(CONVEYER_HALL_EFFECT_PIN, INPUT);
}

void loop() {
  testHallEffectSensor();
}