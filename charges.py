import time
import board
import adafruit_ina260
from adafruit_lc709203f import LC709203F

print("simple test")
print("Make sure LiPoly battery is plugged into the board!")

i2c = board.I2C()  # uses board.SCL and board.SDA
ina260 = adafruit_ina260.INA260(i2c)
sensor = LC709203F(i2c)


while True:
	try:
		print("Current: %.2f mA Voltage: %.2f V Power:%.2f mW"
        		% (ina260.current, ina260.voltage, ina260.power))
		print("Battery: %0.3f Volts / %0.1f %%"
            		% (sensor.cell_voltage, sensor.cell_percent))

	except OSError:
		print("retry reads")

	time.sleep(300)





##### Slow baud rate to 10k on rasp pi zero for LC709203F #####
