#include <Arduino.h>

void writeMessage(String type, String message);

void writeInfo(String message);

void writeError(String message);

void writeDebug(String message);

void writeState(String state);

void waitForSerialInput();