# Environmental Data Collection Script for Raspberry Pi
# Author: Raiz Mohammed
# Description: This script collects environmental data (temperature, humidity, pressure)
# from a BME280 sensor connected to the Raspberry Pi. It logs the readings, along with
# timestamps, to a JSON file saved on an external USB drive (BEAMdrive).

# Import necessary libraries for interacting with the board and sensors
import board
import digitalio  # Library for digital input/output
import busio      # Library for I2C and SPI communication protocols
import time
import adafruit_bme280  # Library to interface with the BME280 environmental sensor
import datetime
import os

# Define the path for the data file where readings will be saved.
# The file name includes the Node ID and the current date to keep track of data files by day.
node_id = "Node_1"  # Identifier for the node (replaceable by actual Node ID as needed)
file_path = f"/media/pi/BEAMdrive/{node_id}_{datetime.datetime.now().strftime('%m-%d-%y')}.json"

# Create the objects needed to communicate with sensors via I2C and SPI
i2c = busio.I2C(board.SCL, board.SDA)  # Set up I2C communication (though not used further in this code)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)  # Set up SPI communication
cs = digitalio.DigitalInOut(board.D5)  # Configure the Chip Select (CS) pin using digital I/O for SPI

# Initialize variables to store sensor data. Default to -1.0 in case sensor readings fail.
hum = -1.0      # Humidity
temp = -1.0     # Temperature
press = -1.0    # Pressure

try:
    # Initialize the BME280 sensor using SPI communication and CS pin.
    bme280 = adafruit_bme280.Adafruit_BME280_SPI(spi, cs)
    
    # Retrieve sensor readings for humidity, temperature, and pressure
    hum = bme280.humidity
    temp = bme280.temperature
    press = bme280.pressure
except Exception as e:
    # Print error message if sensor initialization or reading fails
    print(f"Error reading from BME280: {e}")

# Open the specified file in append mode, write the data, and automatically close it after writing.
with open(file_path, "a") as file:
    # Write sensor data as a JSON-like structure
    file.write("{\n")
    file.write("\t\"time\": \"" + datetime.datetime.now().strftime("%H:%M:%S") + "\",\n")  # Current time
    file.write("\t\"temperature\": %0.1f" % temp + ",\n")  # Temperature in degrees with one decimal place
    file.write("\t\"humidity\": %0.1f" % hum + ",\n")      # Humidity in percentage with one decimal place
    file.write("\t\"pressure\": %0.1f" % press + ",\n")    # Pressure in hPa with one decimal place
    file.write("}\n")  # Close the JSON-like structure