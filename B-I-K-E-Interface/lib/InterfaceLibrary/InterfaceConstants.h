#pragma once
#include <Arduino.h>

/*
PCA9554 Addressing
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
constexpr uint8_t PANEL_1_ADDRESS = 0x21; // L L H
constexpr uint8_t PANEL_2_ADDRESS = 0x20; // L L L 
constexpr uint8_t PANEL_3_ADDRESS = 0x27; // H H H 
constexpr uint8_t PANEL_4_ADDRESS = 0x25; // H L H

constexpr uint8_t PANEL_1_INTERRUPT_PIN = PA_0;
constexpr uint8_t PANEL_2_INTERRUPT_PIN = PA_1;
constexpr uint8_t PANEL_3_INTERRUPT_PIN = PA_3;
constexpr uint8_t PANEL_4_INTERRUPT_PIN = PA_4;