#include <Arduino.h>
#include <Wire.h>
#include <Pca9554.h>

/*
PCA9554 Addressing (These may be incorrect)
Address     A2  A1  A0
0x20        L   L   L
0x21        L   L   H
0x22        L   H   L
0x23        L   H   H
0x24        H   L   L
0x25        H   L   H
0x26        H   H   L
0x27        H   H   H
*/

// Panel 1 is the leftmost panel when looking at the front of the table
constexpr uint8_t PANEL_1_ADDRESS = 0x26; // L L H
constexpr uint8_t PANEL_2_ADDRESS = 0x20; // L L L 
constexpr uint8_t PANEL_3_ADDRESS = 0x27; // H H H 
constexpr uint8_t PANEL_4_ADDRESS = 0x37; // H L H

constexpr uint8_t PANEL_1_INTERRUPT_PIN = 2;
constexpr uint8_t PANEL_2_INTERRUPT_PIN = 3;
constexpr uint8_t PANEL_3_INTERRUPT_PIN = 4;
constexpr uint8_t PANEL_4_INTERRUPT_PIN = 5;

Pca9554 panel1(PANEL_1_ADDRESS);
Pca9554 panel2(PANEL_2_ADDRESS);
Pca9554 panel3(PANEL_3_ADDRESS);
Pca9554 panel4(PANEL_4_ADDRESS);

/**
 * @brief Writes the given panel ID and button index to the serial port
 *        to be obtained by the main program in Python
 *
 * @param panelId the panel ID [1, 4]
 * @param buttonIndex the button index [0, 7]
 */
void writeButtonInfo(uint8_t panelId, uint8_t buttonIndex) {
  if (buttonIndex == -1) { return; }
  // TODO: Write to python using serial and
  // define how the data is formatted on the python side
  //Serial.write(panelId);
  //Serial.write(buttonIndex);
}

int readI2CRegister(uint8_t i2cAddress, uint8_t reg) {
  int value = 0;
  Wire.beginTransmission(i2cAddress);
  Wire.write(reg);
  uint8_t error = Wire.endTransmission();
  if (error == 0) {
    Wire.requestFrom(i2cAddress, (uint8_t)1);
    while (Wire.available() < 1);
    value = Wire.read();
  } else {
    Serial.println("Error reading register");
    Serial.println(error);
  }
  return value;
}

void panel1Interrupt(void) {
  Serial.println("Panel 1 Interrupt");
  int readData = readI2CRegister(PANEL_1_ADDRESS, PCA9554_REG_INP);
  Serial.println("Read data: " + String(readData));
}

void panel2Interrupt(void) {
  Serial.println("Panel 2 Interrupt");
  int readData = readI2CRegister(PANEL_2_ADDRESS, PCA9554_REG_INP);
  Serial.println("Read data: " + String(readData));
}

void panel3Interrupt(void) {
  Serial.println("Panel 3 Interrupt");
  int readData = readI2CRegister(PANEL_3_ADDRESS, PCA9554_REG_INP);
  Serial.println("Read data: " + String(readData));
}

void panel4Interrupt(void) {
  Serial.println("Panel 4 Interrupt");
  int readData = readI2CRegister(PANEL_4_ADDRESS, PCA9554_REG_INP);
  Serial.println("Read data: " + String(readData));
}

void i2cScanner() {
  // Scan I2C bus for devices
  Serial.println("Scanning I2C bus...");
  byte error, address;
  int nDevices = 0;
  for (address = 1; address < 127; address++) {
    Wire.beginTransmission(address);
    error = Wire.endTransmission();
    if (error == 0) {
      Serial.print("I2C device found at address 0x");
      if (address < 16) {
        Serial.print("0");
      }
      Serial.println(address, HEX);
      nDevices++;
    } else if (error == 4) {
      Serial.print("Unknown error at address 0x");
      if (address < 16) {
        Serial.print("0");
      }
      Serial.println(address, HEX);
    }
  }
  if (nDevices == 0) {
    Serial.println("No I2C devices found");
  } else {
    Serial.println("done");
  }
  delay(5000);
}

void setup() {
  // Start Serial and I2C
  Serial.begin(115200);
  Serial.println(F("\nI2C PINS"));
  Serial.print(F("\tSDA = ")); Serial.println(SDA);
  Serial.print(F("\tSCL = ")); Serial.println(SCL);
  Serial.println();
  panel1.begin();
  panel2.begin();
  panel3.begin();
  panel4.begin();
  // Set all the panels to input mode
  for (int i = 0; i < 8; i++) {
    panel1.pinMode(i, INPUT);
    panel2.pinMode(i, INPUT);
    panel3.pinMode(i, INPUT);
    panel4.pinMode(i, INPUT);
  }
  // Start I2C
  Wire.begin();
  // Set the interrupt pins to input mode
  pinMode(PANEL_1_INTERRUPT_PIN, INPUT);
  pinMode(PANEL_2_INTERRUPT_PIN, INPUT);
  pinMode(PANEL_3_INTERRUPT_PIN, INPUT);
  pinMode(PANEL_4_INTERRUPT_PIN, INPUT);
  // Attach the interrupt handlers
  attachInterrupt(digitalPinToInterrupt(PANEL_1_INTERRUPT_PIN), panel1Interrupt, RISING);
  attachInterrupt(digitalPinToInterrupt(PANEL_2_INTERRUPT_PIN), panel2Interrupt, RISING);
  attachInterrupt(digitalPinToInterrupt(PANEL_3_INTERRUPT_PIN), panel3Interrupt, RISING);
  attachInterrupt(digitalPinToInterrupt(PANEL_4_INTERRUPT_PIN), panel4Interrupt, RISING);
}

void loop() {
  i2cScanner();
}