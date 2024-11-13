from gpiozero import MotionSensor

pin = 4                  # Define what GPIO pin the sensor will use -- I used GPIO4
pir = MotionSensor(pin)  # Create the sensor object using the pin that was defined

while True:
  pir.wait_for_motion()    # Tells the script to actively search for motion and pause until it finds it
  print("Motion Detected") # Output a notice to ensure the sensor is working
  pir.wait_for_no_motion() # Pause the script until motion is no longer detected
