#include <Arduino.h>
#include <ShufflerLibrary.hpp>

Shuffler shuffler = Shuffler();

void stopForever() {
    while (true) {
        delay(100);
    }
}

void setup() {
    Serial.begin(9600);
    shuffler.init();
    shuffler.calibrate();
}

void loop() {
    delay(100);
}