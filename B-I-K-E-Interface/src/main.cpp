#include <Arduino.h>
#include <Wire.h>
#include <InterfaceLibrary.h>

// PCA9554 panel1(PANEL_1_ADDRESS);
// PCA9554 panel2(PANEL_2_ADDRESS);
// PCA9554 panel3(PANEL_3_ADDRESS);
// PCA9554 panel4(PANEL_4_ADDRESS);

Pca9554Class panel4;

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

/**
 * @brief Reads the data over I2C, expecting 8 bytes, and returns the index of the button that was pressed
 *
 * @return uint8_t The index of the button that was pressed
 */
uint8_t findButtonBit() {
  int length = 64;
  byte data[length];
  int i = 0;
  while (Wire.available() > 0) {
    data[i++] = Wire.read();
  }
  Serial.println("Received data: ");
  for (int i = 0; i < length; i++) {
    Serial.print(data[i]);
    Serial.print(" ");
  }
  // Find the index of the button that was pressed by finding the 1
  // This only supports 1 button press at a time
  for (int i = 0; i < length; i++) {
    if (data[i] == 1) {
      Serial.println("Found button: " + String(i));
      return i;
    }
  }
  Serial.println("No button was pressed");
  return -1; // No button was pressed
}

int readI2CRegister(uint8_t i2cAddress, uint8_t reg) {
  int value = 0;
  Wire.beginTransmission(i2cAddress);
  Wire.write(reg);
  uint8_t error = Wire.endTransmission();
  if (error == 0) {
    Wire.requestFrom(i2cAddress, 1, true);
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
  // Wire.requestFrom(PANEL_1_ADDRESS, 8);
  uint8_t button = findButtonBit();
  writeButtonInfo(1, button);
}

void panel2Interrupt(void) {
  Serial.println("Panel 2 Interrupt");
  // Wire.requestFrom(PANEL_2_ADDRESS, 8);
  uint8_t button = findButtonBit();
  writeButtonInfo(2, button);
}

void panel3Interrupt(void) {
  Serial.println("Panel 3 Interrupt");
  // Wire.requestFrom(PANEL_3_ADDRESS, 8);
  uint8_t button = findButtonBit();
  writeButtonInfo(3, button);
}

void panel4Interrupt(void) {
  Serial.println("Panel 4 Interrupt");
  int readData = readI2CRegister(0x37, 0);
  Serial.println("Read data: " + String(readData));
  //Wire.requestFrom(PANEL_4_ADDRESS, 8);
  //uint8_t button = findButtonBit();
  //writeButtonInfo(4, button);
}

void setup() {
  // Start Serial and I2C
  Serial.begin(115200);
  panel4.begin();
  Wire.begin(A4, A5);
  // Set all the panels to input mode
  // panel1.portMode(ALLINPUT);
  // panel2.portMode(ALLINPUT);
  // panel3.portMode(ALLINPUT);
  // panel4.portMode(ALLINPUT);
  // Set the interrupt pins to input mode
  pinMode(PANEL_1_INTERRUPT_PIN, INPUT);
  pinMode(PANEL_2_INTERRUPT_PIN, INPUT);
  pinMode(PANEL_3_INTERRUPT_PIN, INPUT);
  pinMode(PANEL_4_INTERRUPT_PIN, INPUT);
  // Attach the interrupt handlers
  //attachInterrupt(digitalPinToInterrupt(PANEL_1_INTERRUPT_PIN), panel1Interrupt, RISING);
  // attachInterrupt(digitalPinToInterrupt(PANEL_2_INTERRUPT_PIN), panel2Interrupt, RISING);
  // attachInterrupt(digitalPinToInterrupt(PANEL_3_INTERRUPT_PIN), panel3Interrupt, RISING);
  attachInterrupt(digitalPinToInterrupt(PANEL_4_INTERRUPT_PIN), panel4Interrupt, RISING);
}

void loop() {
  delay(15);
}