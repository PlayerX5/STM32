/*
 * Everything.h
 *
 *  Created on: Nov 20, 2023
 *      Author: sai_R
 */


#ifndef SRC_EVERYTHING_H_
#define SRC_EVERYTHING_H_


#include "stm32f1xx_hal.h"
#include "stdint.h"
#define SHT_ADDR 0x81
#define SHT_TEMP 0xF3
#define REG_HUMIDITY 0xF5


void read_sh21(void);
float sht21_get_temperature(void);
float sht21_get_humidity(void);
uint16_t read_sensor(uint8_t register_address);


void slider();


#endif /* SRC_EVERYTHING_H_ */
