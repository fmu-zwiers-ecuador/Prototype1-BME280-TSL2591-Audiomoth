import board
import digitalio  # Add this import
import busio
import time
import adafruit_tsl2591
import adafruit_bme280
import datetime

# Open the file with the date as its name in append mode to avoid overwriting data
file_path = "/media/pi/BEAMdrive/" + open("Node_ID").read().strip() + ": " + datetime.datetime.now().strftime("%m-%d-%y") + ".json"

# Create the objects needed to instantiate the sensors
i2c = busio.I2C(board.SCL, board.SDA)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.D5)  # Use digitalio for CS pin

# Declare light sensing variables
lux = -1.0
ir = -1.0
vis = -1.0

# Declare environmental sensing variables
hum = -1.0
temp = -1.0
press = -1.0

try:
    # Initialize the TSL2561 light sensor
    sensor = adafruit_tsl2561.TSL2561(i2c)
    lux = sensor.lux
    ir = sensor.infrared
    broadband = sensor.broadband
    vis = broadband - ir  # Calculate visible light
except Exception as e:
    print(f"Error reading from TSL2561: {e}")

try:
    # Initialize the BME280 environmental sensor
    bme280 = adafruit_bme280.Adafruit_BME280_SPI(spi, cs)
    hum = bme280.humidity
    temp = bme280.temperature
    press = bme280.pressure
except Exception as e:
    print(f"Error reading from BME280: {e}")

# Write the data to the file with automatic closure
with open(file_path, "a") as file:
    file.write("{\n")
    file.write("\t\"time\": \"" + datetime.datetime.now().strftime("%H:%M:%S") + "\",\n")
    file.write("\t\"temperature\": %0.1f" % temp + ",\n")
    file.write("\t\"humidity\": %0.1f" % hum + ",\n")
    file.write("\t\"pressure\": %0.1f" % press + ",\n")
    file.write("\t\"lux\": {}".format(lux) + ",\n")
    file.write("\t\"visible\": {}".format(vis) + ",\n")
    file.write("\t\"infrared\": {}".format(ir) + "\n")
    file.write("}\n")

