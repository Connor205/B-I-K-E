#include <Arduino.h>
#include <Wire.h>
#include <InterfaceLibrary.h>

/**
 * @brief The event that is triggered when data is received from the I2C bus
 *
 * @param howMany The number of bytes received
 */
void receiveEvent(int howMany) {
  byte data[howMany];
  int i = 0;
  while (Wire.available() > 0) {
    data[i++] = Wire.read();
  }
}

void requestEvent() {
  // A device has requested data from this device
}

void setup() {
  Serial.begin(115200);
  Wire.begin();
  Wire.onReceive(receiveEvent);
  Wire.onRequest(requestEvent);
}

void loop() {
  delay(100);
}