#pragma once
#include <Arduino.h>

// Panel 1 is the leftmost panel when looking at the front of the table
constexpr uint8_t PANEL_1_ADDRESS = 0x20;
constexpr uint8_t PANEL_2_ADDRESS = 0x21;
constexpr uint8_t PANEL_3_ADDRESS = 0x22;
constexpr uint8_t PANEL_4_ADDRESS = 0x23;

constexpr uint8_t PANEL_1_INTERRUPT_PIN = PA_0;
constexpr uint8_t PANEL_2_INTERRUPT_PIN = PA_1;
constexpr uint8_t PANEL_3_INTERRUPT_PIN = PA_3;
constexpr uint8_t PANEL_4_INTERRUPT_PIN = PA_4;