import time
import board
import digitalio
import adafruit_tsl2591
import datetime
from adafruit_bme280 import basic as adafruit_bme280

# Open the file with the date as its name in append mode to avoid overwriting data
file_path = "/media/pi/BEAMdrive/" + open("Node_ID.txt").read().strip() + "_" + datetime.datetime.now().strftime("%m-%d-%y") + ".json"

cs = digitalio.DigitalInOut(board.D5)
spi = board.SPI()
i2c = board.I2C()


# Declare light sensing variables
lux = -1.0
ir = -1.0
vis = -1.0
full_spec = -1.0

# Declare environmental sensing variables
hum = -1.0
temp = -1.0
press = -1.0

try:
    sensor = adafruit_tsl2591.TSL2591(i2c)
    lux = sensor.lux
    ir = sensor.infrared
    vis = sensor.visible
    full_spec = sensor.full_spectrum
except Exception as e:
    print(f"Error reading from TSL2591: {e}")

try:
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
    file.write("\t\"full-spectrum\": {}".format(full_spec) + "\n")
    file.write("}\n")
