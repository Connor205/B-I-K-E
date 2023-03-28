#include <Arduino.h>
#include <Wire.h>
#include <InterfaceLibrary.h>

// PCA9554 panel1(PANEL_1_ADDRESS);
// PCA9554 panel2(PANEL_2_ADDRESS);
// PCA9554 panel3(PANEL_3_ADDRESS);
// PCA9554 panel4(PANEL_4_ADDRESS);

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
  int readData = readI2CRegister(PANEL_1_ADDRESS, 0);
  Serial.println("Read data: " + String(readData));
}

void panel2Interrupt(void) {
  Serial.println("Panel 2 Interrupt");
}

void panel3Interrupt(void) {
  Serial.println("Panel 3 Interrupt");
}

void panel4Interrupt(void) {
  Serial.println("Panel 4 Interrupt");
  int readData = readI2CRegister(PANEL_4_ADDRESS, 0);
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
  Wire.begin((uint32_t)PA_5, (uint32_t)PA_6);
  // Wire.begin(A4, A5);
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