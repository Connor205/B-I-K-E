#include <Arduino.h>
#include <Utils.h>

void writeMessage(String type, String message)
{
    Serial.print(type);
    Serial.print(":");
    Serial.println(message);
}

void writeInfo(String message) { writeMessage("INFO", message); }

void writeError(String message) { writeMessage("ERROR", message); }

void writeDebug(String message) { writeMessage("DEBUG", message); }
void writeState(String state) { writeMessage("STATE", state); }

void waitForSerialInput()
{
    while (Serial.available() == 0) {
        delay(50);
    }
}