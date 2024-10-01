/*
 * Everything.c
 *
 *  Created on: Nov 20, 2023
 *      Author: sai_R
 */




#include "main.h"
#include "Everything.h"
#include "stdio.h"
#include "string.h"


extern I2C_HandleTypeDef hi2c1;
extern UART_HandleTypeDef huart1;
extern TIM_HandleTypeDef htim3;


////////////////////To Read and send the Temperature values////////////////////
void read_sh1(void)
{
	int temperature;
	char buff[100]; // Buffer to store received data


	HAL_UART_Receive(&huart1, (uint8_t *)buff, sizeof(buff), 1000);
	buff[sizeof(buff)] = '\0';
	// Read Temperature from SHT21
	temperature = sht21_get_temperature();


	/*Load the Temperature into Buff */
	sprintf(buff,"Temperature: %d\r\n", temperature); // @suppress("Float formatting support")
	HAL_Delay(500);


	// Send out buffer (Temperature or error message)
	HAL_UART_Transmit(&huart1, (uint8_t*)buff, strlen(buff), 1000);
}


////////////////////To Read and send the Humidity values////////////////////
void read_sh2(void)
{
	int humidity;
	char buff[100]; // Buffer to store received data


	HAL_UART_Receive(&huart1, (uint8_t *)buff, sizeof(buff), 1000);
	buff[sizeof(buff)] = '\0';


	// Read Humidity from SHT21
	humidity = sht21_get_humidity();


	/*Load the Humidity into Buff */
	sprintf(buff,"Humidity: %d\r\n",humidity); // @suppress("Float formatting support")
	HAL_Delay(500);


	// Send out buffer (Humidity or error message)
	HAL_UART_Transmit(&huart1, (uint8_t*)buff, strlen(buff), 1000);
}


//Function to capture temperature from sensor
float sht21_get_temperature()
{
	uint16_t response;
	float final_temperature;


	response = read_sensor(SHT_TEMP);


	//Use formula as per datasheet
	final_temperature = ((float)response)/65535;
	final_temperature = final_temperature * 175.72;
	final_temperature = final_temperature -46.85;


	return (int)final_temperature;
}


// Function to measure Humidity
float sht21_get_humidity(void) {
	uint16_t response;
 	float final_humidity;


	response = read_sensor(REG_HUMIDITY);
	//Use formula as per datasheet
	final_humidity = (float)response/65535;
	final_humidity = final_humidity * (-6+125);


	return final_humidity;
}


//Read from I2C_Device and send back response
uint16_t read_sensor(uint8_t register_address)
{
 	uint8_t data_SHT[3];
 	uint16_t retVal;


	// send master request to the temperature sensor
 	HAL_I2C_Master_Transmit(&hi2c1,SHT_ADDR ,&register_address,1,10);
	// give a delay for the sensor to process
 	HAL_Delay(100);
	// Receive data from the sensor by reading from the communication bus
	HAL_I2C_Master_Receive (&hi2c1,SHT_ADDR ,data_SHT,3,3000);


	retVal = 0;
	retVal = data_SHT[0] << 8;
	retVal = retVal | data_SHT[1];
	retVal = retVal & 0xFFFC;


	return retVal;
}


////////////////////To Adjust the Brightness of LED////////////////////
void led()
{
	uint8_t rx_data[2];


	HAL_UART_Receive(&huart1, rx_data, sizeof(rx_data), HAL_MAX_DELAY);
	uint16_t brightness  = (rx_data[1] << 8) | rx_data[0];
    __HAL_TIM_SetCompare(&htim3, TIM_CHANNEL_1, brightness );
    HAL_TIM_PWM_Start(&htim3, TIM_CHANNEL_1);
}
