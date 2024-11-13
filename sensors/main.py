import multiprocessing
from gpiozero import Button
import os
import pyaudio
import wave
import time
import board
import digitalio
import busio
import adafruit_tsl2561
import adafruit_bme280
import datetime

BUTTON_PIN = 21  # GPIO pin number

file_path = "/media/pi/BEAMdrive/" + open("Node_ID").read().strip() + ": " + datetime.datetime.now().strftime("%m-%d-%y") + ".json"

# Create the objects needed to instantiate the sensors
i2c = busio.I2C(board.SCL, board.SDA)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.D5)

def record_audio():
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 48000
    CHUNK = 1024
    RECORD_SECONDS = 5  # Adjust as needed
    AUDIO_DEVICE_INDEX = None
    audio = pyaudio.PyAudio()

    try:
        while True:
            timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"/media/pi/BEAMdrive/{timestamp}.wav"
            stream = audio.open(format=FORMAT, channels=CHANNELS,
                                rate=RATE, input=True, input_device_index=AUDIO_DEVICE_INDEX,
                                frames_per_buffer=CHUNK)

            frames = []
            for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                frames.append(data)

            stream.stop_stream()
            stream.close()

            with wave.open(filename, 'wb') as waveFile:
                waveFile.setnchannels(CHANNELS)
                waveFile.setsampwidth(audio.get_sample_size(FORMAT))
                waveFile.setframerate(RATE)
                waveFile.writeframes(b''.join(frames))

            # Initialize sensors and capture data
            sensor = adafruit_tsl2561.TSL2561(i2c)
            bme280 = adafruit_bme280.Adafruit_BME280_SPI(spi, cs)
            
            lux, ir, vis = sensor.lux, sensor.infrared, sensor.broadband - sensor.infrared
            hum, temp, press = bme280.humidity, bme280.temperature, bme280.pressure

            with open(file_path, "a") as file:
                file.write("{\n")
                file.write(f"\t\"time\": \"{datetime.datetime.now().strftime('%H:%M:%S')}\",\n")
                file.write(f"\t\"temperature\": {temp:.1f},\n")
                file.write(f"\t\"humidity\": {hum:.1f},\n")
                file.write(f"\t\"pressure\": {press:.1f},\n")
                file.write(f"\t\"lux\": {lux},\n")
                file.write(f"\t\"visible\": {vis},\n")
                file.write(f"\t\"infrared\": {ir}\n")
                file.write("}\n")

            time.sleep(55 * 60)  # 55 minutes pause between recordings

    except KeyboardInterrupt:
        print("\nRecording stopped.")
    finally:
        audio.terminate()

def button_listener():
    button = Button(BUTTON_PIN)

    def eject_usb():
        print("Button pressed! Ejecting the USB drive...")
        os.system("sudo umount /media/pi/BEAMdrive")
        os.system("sudo eject /dev/sda")

    button.when_pressed = eject_usb
    button.wait_for_press()  # Keep the button listening

if __name__ == '__main__':
    record_process = multiprocessing.Process(target=record_audio)
    button_process = multiprocessing.Process(target=button_listener)

    record_process.start()
    button_process.start()

    try:
        while True:
            time.sleep(1)  # Keep the main thread alive
    except KeyboardInterrupt:
        print("Terminating processes...")
        record_process.terminate()
        button_process.terminate()
        record_process.join()
        button_process.join()