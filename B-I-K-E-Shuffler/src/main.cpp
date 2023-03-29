#include <Arduino.h>
#include <ShufflerLibrary.hpp>

Shuffler shuffler = Shuffler();

void testHallEffectSensor()
{
    int sensorValue = digitalRead(CONVEYER_HALL_EFFECT_PIN);
    Serial.println(sensorValue);
    digitalWrite(13, sensorValue);
}

void setup()
{
    Serial.begin(9600);
    shuffler.init();
    shuffler.calibrate();
}

void loop()
{
    // Serial.println("Rotating full turn");
    // delay(5000);

    // for (int i = 0; i < 6400; i++) {
    //     shuffler.dispenserMotor.stepMotor();
    //     // digitalWrite(BELT_STEP_PIN, HIGH);
    //     // delayMicroseconds(1000);
    //     // digitalWrite(BELT_STEP_PIN, LOW);
    //     // delayMicroseconds(1000);
    // }

    // Serial.println("Finished Full Turn");

    // shuffler.moveDispenserToMM(140);
    while (true) {
        delay(100);
    }
}