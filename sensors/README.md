# sensors
Scripts and libraries used to read the sensors and store data in a usable format

To use WaveShare BME280, Adafruit TSL2591, and HC-sr501:
(Sensor Connection then Raspberry pi pin)

Connect TSL2591 to Raspberry Pi:
1. Connect VIn to Pin 1 (3v3)
2. Connect GND to Pin 6 (Ground)
3. Connect SCL to Pin 5 (I2C SCL)
4. Connect SDA to Pin 3 (I2C SDA)

Connect BME280 to Raspberry Pi (Uses SPI because I2C is in use by the TSL2591 and this is easier than readdressing):
1. Connect VCC to Pin 1 (3v3)
2. Connect GND to Pin 6 (Ground)
3. Connect SDA/MOSI to Pin 19 (SPI MOSI)
4. Connect SCL/SCK to Pin 23 (SPI SCLK)
5. Connect ADDR/MISO to Pin 21 (SPI MISO)
6. Connect CS to Pin 29 (GPIO Pin 5; This is changeable, but my script uses it like this)

Connect HC-sr501 (PIR Sensor) to Raspberry Pi:
1. Connect VCC to Pin 2 (5v)
2. Connect GND to Pin 6 (Ground)
3. Connect OUT to Pin 7 (GPIO Pin 4; this is changeable, but my test script uses this one)

--------------------------------------------------------

To use the script:
1. Install CircuitPython
2. Ensure sensors are connected as described above
3. Place the script, Node_ID, and libraries into the same folder. It does not matter where they are as long as you can reference them
4. Edit Node_ID to hold the current node's name
5. Run the script.

The script sets a default value of -1.0 for all readings until this value gets overridden by the script reading the appropriate sensor. If the script cannot use the sensor, the default value of -1.0 is intended as an error state to let you know there is something wrong without breaking anything on the supervisor end.
