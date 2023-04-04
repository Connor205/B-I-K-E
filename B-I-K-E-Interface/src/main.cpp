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

// Panel 1 is the leftmost panel (near the shuffler)
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

int previousPanel1State = 255;
int previousPanel2State = 255;
int previousPanel3State = 255;
int previousPanel4State = 255;

void panel1Interrupt(void)
{
    Serial.println("1");
    // int readData = readI2CRegister(PANEL_1_ADDRESS, PCA9554_REG_INP);
    // Serial.println("Read data: " + String(readData));
}

void panel2Interrupt(void)
{
    Serial.println("2");
    // int readData = readI2CRegister(PANEL_2_ADDRESS, PCA9554_REG_INP);
    // Serial.println("Read data: " + String(readData));
}

void panel3Interrupt(void)
{
    Serial.println("3");
    // int readData = readI2CRegister(PANEL_3_ADDRESS, PCA9554_REG_INP);
    // Serial.println("Read data: " + String(readData));
}

void panel4Interrupt(void)
{
    Serial.println("4");
    // int readData = readI2CRegister(PANEL_4_ADDRESS, PCA9554_REG_INP);
    // Serial.println("Read data: " + String(readData));
}

void i2cScanner()
{
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

void setupInterrupts()
{
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
 * @param panelId the panel ID [0, 3]
 * @param buttonIndex the button index [0, 7]
 */
void writeButtonInfo(uint8_t panelId, uint8_t buttonIndex)
{
    // TODO: Write to python using serial and
    // define how the data is formatted on the python side
    if (panelId == -1 || buttonIndex == -1) {
        return;
    }
    Serial.println("Button:" + String(panelId) + "," + String(buttonIndex));
}

/**
 * @brief Reads the given register from the given I2C address
 *
 * @param i2cAddress the I2C address of the device
 * @param reg the address of the register to read
 * @return int the value of the register
 */
int readI2CRegister(uint8_t i2cAddress, uint8_t reg)
{
    int value = 255; // Default to 255 so we default to no buttons pressed
    Wire.beginTransmission(i2cAddress);
    Wire.write(reg);
    uint8_t error = Wire.endTransmission();
    if (error == 0) {
        Wire.requestFrom(i2cAddress, (uint8_t)1);
        while (Wire.available() < 1)
            ;
        value = Wire.read();
    }
    // else {
    //   Serial.print("Error reading register at address 0x" + String(i2cAddress, HEX) + ": ");
    //   Serial.println(error);
    // }
    return value;
}

/**
 * @brief Given a panelValue, return the index of the button that was pressed
 * @note The buttons are indexed from [0, 7] where each one represents a bit in the full 8-bit representation
 *      of the panel value. For example, if the panel value is 1111 1110, then the button at index 0 was pressed.
 *
 * @param panelValue the value of the panel as an integer
 * @return uint8_t the index of the button that was pressed
 */
uint8_t getButtonIndex(uint8_t panelValue)
{
    // We do this by finding the first 0 in the binary representation of the panel value
    for (uint8_t i = 7; i >= 0; i--) {
        if (panelValue % 2 == 0) {
            return i;
        } else {
            panelValue = panelValue >> 1;
        }
    }
    return -1;
}

void getAllPanelValues(bool print = false)
{
    // Read the input register of each panel
    int panel1Value = readI2CRegister(PANEL_1_ADDRESS, PCA9554_REG_INP);
    int panel2Value = readI2CRegister(PANEL_2_ADDRESS, PCA9554_REG_INP);
    int panel3Value = readI2CRegister(PANEL_3_ADDRESS, PCA9554_REG_INP);
    int panel4Value = readI2CRegister(PANEL_4_ADDRESS, PCA9554_REG_INP);
    if (print) {
        Serial.println("Panel 1: " + String(panel1Value) + " | " + "Panel 2: " + String(panel2Value) + " | "
            + "Panel 3: " + String(panel3Value) + " | " + "Panel 4: " + String(panel4Value));
    }
    // Check if any buttons have been pressed, default value is 255
    int panelIndex = -1;
    int buttonIndex = -1;
    // Check if any buttons have been pressed (only one button can be pressed at a time)
    if (panel1Value != 255 && previousPanel1State == 255) {
        panelIndex = 0;
        buttonIndex = getButtonIndex(panel1Value);
        writeButtonInfo(panelIndex, buttonIndex);
    }
    if (panel2Value != 255 && previousPanel2State == 255) {
        panelIndex = 1;
        buttonIndex = getButtonIndex(panel2Value);
        writeButtonInfo(panelIndex, buttonIndex);
    }
    if (panel3Value != 255 && previousPanel3State == 255) {
        panelIndex = 2;
        buttonIndex = getButtonIndex(panel3Value);
        writeButtonInfo(panelIndex, buttonIndex);
    }
    if (panel4Value != 255 && previousPanel4State == 255) {
        panelIndex = 3;
        buttonIndex = getButtonIndex(panel4Value);
        writeButtonInfo(panelIndex, buttonIndex);
    }
    // Update the previous states
    previousPanel1State = panel1Value;
    previousPanel2State = panel2Value;
    previousPanel3State = panel3Value;
    previousPanel4State = panel4Value;
}

void setup()
{
    // Start Serial
    Serial.begin(115200);
    Wire.begin();
    // Serial.println("Initializing I2C bus...");
    // Serial.println(F("\nI2C PINS"));
    // Serial.print(F("\tSDA = ")); Serial.println(SDA);
    // Serial.print(F("\tSCL = ")); Serial.println(SCL);
    // Serial.println();
    // Start I2C
    // setupInterrupts();
}

void loop()
{
    getAllPanelValues(false);
    delay(50);
}