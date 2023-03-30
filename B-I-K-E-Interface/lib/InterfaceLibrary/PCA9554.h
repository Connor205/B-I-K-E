/*
 * ----------------------------------------------------------------------------
 *            _____ _           _                   _
 *           | ____| | ___  ___| |_ _ __ ___  _ __ (_) ___
 *           |  _| | |/ _ \/ __| __| '__/ _ \| '_ \| |/ __|
 *           | |___| |  __/ (__| |_| | | (_) | | | | | (__
 *           |_____|_|\___|\___|\__|_|  \___/|_| |_|_|\___|
 *            ____                   _   ____
 *           / ___|_      _____  ___| |_|  _ \ ___  __ _ ___
 *           \___ \ \ /\ / / _ \/ _ \ __| |_) / _ \/ _` / __|
 *            ___) \ V  V /  __/  __/ |_|  __/  __/ (_| \__ \
 *           |____/ \_/\_/ \___|\___|\__|_|   \___|\__,_|___/
 *
 * ----------------------------------------------------------------------------
 * "THE BEER-WARE LICENSE" (Revision 42):
 * <pontus@sweetpeas.se> wrote this file. As long as you retain this notice you
 * can do whatever you want with this stuff. If we meet some day, and you think
 * this stuff is worth it, you can buy me a beer in return - Pontus Oldberg
 * ----------------------------------------------------------------------------
 */
#ifndef __GUARD_PCA9554_H__
#define __GUARD_PCA9554_H__

#include <Arduino.h>
#include <Wire.h>

#define PCA9554_REG_INP 0
#define PCA9554_REG_OUT 1
#define PCA9554_REG_POL 2
#define PCA9554_REG_CTRL 3

#define NORMAL 0
#define INVERTED 1

class Pca9554
{
protected:
public:
	Pca9554(uint8_t i2cAddress);
	void    begin(void);
#if defined(ARDUINO_ARCH_ESP8266)
	void    init(uint8_t sda, uint8_t scl);
#endif
	bool pinMode(uint8_t pin, uint8_t mode);
	bool pinPolarity(uint8_t pin, uint8_t polarity);
	bool digitalWrite(uint8_t pin, bool val);
	bool digitalRead(uint8_t pin);

private:
	uint8_t m_i2cAddress;
	uint8_t m_inp;
	uint8_t m_out;
	uint8_t m_pol;
	uint8_t m_ctrl;
};

#endif //ifndef __GUARD_PCA9554_H__

// EOF