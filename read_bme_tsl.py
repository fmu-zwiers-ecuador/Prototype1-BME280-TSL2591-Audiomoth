import time
import board
import digitalio
import adafruit_tsl2591
from adafruit_bme280 import basic as adafruit_bme280

cs = digitalio.DigitalInOut(board.D5)
spi = board.SPI()
bme280 = adafruit_bme280.Adafruit_BME280_SPI(spi, cs)
bme280.sea_level_pressure = 1013.25


i2c = board.I2C()
sensor = adafruit_tsl2591.TSL2591(i2c)

while True:
  print("Total light: {0}lux".format(sensor.lux))
  print("Infrared light: {0}".format(sensor.infrared))
  print("Visible light: {0}".format(sensor.visible))
  print("Full spectrum (IR + visible) light: {0}".format(sensor.full_spectrum))
  print("\n")
  print("\nTemperature: %0.1f C" % bme280.temperature)
  print("Humidity: %0.1f %%" % bme280.relative_humidity)
  print("Pressure: %0.1f hPa" % bme280.pressure)
  print("Altitude = %0.2f meters" % bme280.altitude)
  print("\n")
  time.sleep(2)
