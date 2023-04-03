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
constexpr uint8_t PANEL_2_ADDRESS = 0x27; // L L L 
constexpr uint8_t PANEL_3_ADDRESS = 0x20; // H H H 
constexpr uint8_t PANEL_4_ADDRESS = 0x25; // H L H

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
    Serial.print("Error reading register at address 0x" + String(i2cAddress, HEX) + ": ");
    Serial.println(error);
  }
  return value;
}

void panel1Interrupt(void) {
  Serial.println("1");
  int readData = readI2CRegister(PANEL_1_ADDRESS, PCA9554_REG_INP);
  Serial.println("Read data: " + String(readData));
}

void panel2Interrupt(void) {
  Serial.println("2");
  int readData = readI2CRegister(PANEL_2_ADDRESS, PCA9554_REG_INP);
  Serial.println("Read data: " + String(readData));
}

void panel3Interrupt(void) {
  Serial.println("3");
  int readData = readI2CRegister(PANEL_3_ADDRESS, PCA9554_REG_INP);
  Serial.println("Read data: " + String(readData));
}

void panel4Interrupt(void) {
  Serial.println("4");
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

void setupInterrupts() {
  // Set the interrupt pins to input mode
  pinMode(PANEL_1_INTERRUPT_PIN, INPUT);
  pinMode(PANEL_2_INTERRUPT_PIN, INPUT);
  pinMode(PANEL_3_INTERRUPT_PIN, INPUT);
  pinMode(PANEL_4_INTERRUPT_PIN, INPUT);
  // Attach the interrupt handlers
  // attachInterrupt(digitalPinToInterrupt(PANEL_1_INTERRUPT_PIN), panel1Interrupt, FALLING);
  // attachInterrupt(digitalPinToInterrupt(PANEL_2_INTERRUPT_PIN), panel2Interrupt, FALLING);
  // attachInterrupt(digitalPinToInterrupt(PANEL_3_INTERRUPT_PIN), panel3Interrupt, FALLING);
  // attachInterrupt(digitalPinToInterrupt(PANEL_4_INTERRUPT_PIN), panel4Interrupt, FALLING);
}

void getAllPanelValues() {
  // Read the input register of each panel
  int panel1Value = readI2CRegister(PANEL_1_ADDRESS, PCA9554_REG_INP);
  int panel2Value = readI2CRegister(PANEL_2_ADDRESS, PCA9554_REG_INP);
  int panel3Value = readI2CRegister(PANEL_3_ADDRESS, PCA9554_REG_INP);
  int panel4Value = readI2CRegister(PANEL_4_ADDRESS, PCA9554_REG_INP);
  // Print the values to the serial port on one line
  Serial.println("Panel 1: " + String(panel1Value) + " | " +
    "Panel 2: " + String(panel2Value) + " | " +
    "Panel 3: " + String(panel3Value) + " | " +
    "Panel 4: " + String(panel4Value));
}

void setup() {
  // Start Serial and I2C
  Serial.begin(115200);
  Serial.println("Initializing I2C bus...");
  Serial.println(F("\nI2C PINS"));
  Serial.print(F("\tSDA = ")); Serial.println(SDA);
  Serial.print(F("\tSCL = ")); Serial.println(SCL);
  Serial.println();
  // Start I2C
  Wire.begin();
  Serial.println("Attaching interrupt handlers...");
  setupInterrupts();
  Serial.println("Setup complete");
}

void loop() {
  getAllPanelValues();
  delay(50);
  // i2cScanner();
}