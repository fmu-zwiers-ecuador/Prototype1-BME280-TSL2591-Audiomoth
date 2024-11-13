'''
PIR Motion sensor activated night vision camera script

Written by Aaron Fulmer for Dr. Zwiers and the FMU Ecuador Project Aug-2019
Using camera code and file processing written by Loreal Anderson Sept-2018
'''

from gpiozero import MotionSensor
import datetime
import os
import subprocess
import time
import picamera
import picamera.array
import shutil
import subprocess
import sys
from fractions import Fraction



pir = MotionSensor(4)			# Make the reference object for the PIR motion sensor
rootFolder = "/home/pi/Desktop/"        # Define the root folder for convenience later

tempFolder = rootFolder + "temp"        # Define the reference folder for placement of images and videos
#print(tempFolder)

while True:
    pir.wait_for_motion()		# Using the PIR sensor, wait for motion before continuing
    #print("Motion Detected")		# Print a notice to the console for debugging

    # Turn on IR array here

    # Create date timestamps for files
    timestamp  = datetime.datetime.now().strftime("%Y%m%d-%H%M%S") # method calls date/time cast str$
    timestamp_jpg  = tempFolder + "/" + timestamp + ".jpg"
    timestamp_mp4  = tempFolder + "/" + timestamp + ".mp4"

    # Capture image
    print("Capturing image...")
    subprocess.call(["raspistill", "-t", "1", "-n", "-o", timestamp_jpg])

    # Move image to 'images' folder
    os.rename(timestamp_jpg, timestamp_jpg.replace("temp", "images"))

    # Capture video
    print("Capturing video...")
    # subprocess.call(["raspivid ", "-t", "10000", "-o", timestamp_mp4])
    subprocess.call(["raspivid", "-t", "15000", "-n", "-o", timestamp_mp4])

    # Move video to 'videos' folder
    os.rename(timestamp_mp4, timestamp_mp4.replace("temp", "videos"))

    # Turn off IR array here

    pir.wait_for_no_motion()		# Wait until the PIR sensor no longer detects motion before continuing

    #print("Motion no longer detected")	# Print a notice to the console for debugging

