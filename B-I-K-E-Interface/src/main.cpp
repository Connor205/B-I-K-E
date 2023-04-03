#include <Arduino.h>
#include <Wire.h>
// #include <Pca9554.h>

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

constexpr uint8_t PCA9554_REG_INP = 0;
constexpr uint8_t PCA9554_REG_OUT = 1;
constexpr uint8_t PCA9554_REG_POL = 2;
constexpr uint8_t PCA9554_REG_CTRL = 3;

void panel1Interrupt(void) {
  Serial.println("1");
  // int readData = readI2CRegister(PANEL_1_ADDRESS, PCA9554_REG_INP);
  // Serial.println("Read data: " + String(readData));
}

void panel2Interrupt(void) {
  Serial.println("2");
  // int readData = readI2CRegister(PANEL_2_ADDRESS, PCA9554_REG_INP);
  // Serial.println("Read data: " + String(readData));
}

void panel3Interrupt(void) {
  Serial.println("3");
  // int readData = readI2CRegister(PANEL_3_ADDRESS, PCA9554_REG_INP);
  // Serial.println("Read data: " + String(readData));
}

void panel4Interrupt(void) {
  Serial.println("4");
  // int readData = readI2CRegister(PANEL_4_ADDRESS, PCA9554_REG_INP);
  // Serial.println("Read data: " + String(readData));
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
  Serial.println("Attaching interrupt handlers...");
  // Attach the interrupt handlers
  attachInterrupt(digitalPinToInterrupt(PANEL_1_INTERRUPT_PIN), panel1Interrupt, FALLING);
  attachInterrupt(digitalPinToInterrupt(PANEL_2_INTERRUPT_PIN), panel2Interrupt, FALLING);
  attachInterrupt(digitalPinToInterrupt(PANEL_3_INTERRUPT_PIN), panel3Interrupt, FALLING);
  attachInterrupt(digitalPinToInterrupt(PANEL_4_INTERRUPT_PIN), panel4Interrupt, FALLING);
}

/**
 * @brief Writes the given panel ID and button index to the serial port
 *        to be obtained by the main program in Python
 *
 * @param panelId the panel ID [1, 4]
 * @param buttonIndex the button index [0, 7]
 * @param print whether or not to print the data to the serial monitor
 */
void writeButtonInfo(uint8_t panelId, uint8_t buttonIndex, bool print = true) {
  // TODO: Write to python using serial and
  // define how the data is formatted on the python side
  if (print) {
    Serial.println("[" + String(panelId) + ", " + String(buttonIndex) + "]");
  }
  // Serial.write(panelId);
  // Serial.write(buttonIndex);
}

/**
 * @brief Reads the given register from the given I2C address
 *
 * @param i2cAddress the I2C address of the device
 * @param reg the address of the register to read
 * @return int the value of the register
 */
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

void getAllPanelValues(bool print = false) {
  // Read the input register of each panel
  int panel1Value = readI2CRegister(PANEL_1_ADDRESS, PCA9554_REG_INP);
  int panel2Value = readI2CRegister(PANEL_2_ADDRESS, PCA9554_REG_INP);
  int panel3Value = readI2CRegister(PANEL_3_ADDRESS, PCA9554_REG_INP);
  int panel4Value = readI2CRegister(PANEL_4_ADDRESS, PCA9554_REG_INP);
  if (print) {
    Serial.println("Panel 1: " + String(panel1Value) + " | " +
      "Panel 2: " + String(panel2Value) + " | " +
      "Panel 3: " + String(panel3Value) + " | " +
      "Panel 4: " + String(panel4Value));
  }
  // Check if any buttons have been pressed, default value is 255
  int panel1Button = 255;
  int panel2Button = 255;
  int panel3Button = 255;
  int panel4Button = 255;
  // Check if any buttons have been pressed
  if (panel1Value != 255) {
    // Get the button index
    panel1Button = 7 - log(panel1Value);
    // Write the button info to the serial port
    writeButtonInfo(1, panel1Button);
  } else if (panel2Value != 255) {
    // Get the button index
    panel2Button = 7 - log(panel2Value);
    // Write the button info to the serial port
    writeButtonInfo(2, panel2Button);
  } else if (panel3Value != 255) {
    // Get the button index
    panel3Button = 7 - log(panel3Value);
    // Write the button info to the serial port
    writeButtonInfo(3, panel3Button);
  } else if (panel4Value != 255) {
    // Get the button index
    panel4Button = 7 - log(panel4Value);
    // Write the button info to the serial port
    writeButtonInfo(4, panel4Button);
  }
}

void setup() {
  // Start Serial
  Serial.begin(115200);
  Serial.println("Initializing I2C bus...");
  Serial.println(F("\nI2C PINS"));
  Serial.print(F("\tSDA = ")); Serial.println(SDA);
  Serial.print(F("\tSCL = ")); Serial.println(SCL);
  Serial.println();
  // Start I2C
  Wire.begin();
  // setupInterrupts();
}

void loop() {
  getAllPanelValues(true);
  delay(10);
  // i2cScanner();
}