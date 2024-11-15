# Prototype1-Audio-and-Environmental-

## Overview
This prototype is designed to automate the collection of audio recordings and environmental data, such as temperature, humidity, and pressure, on a Raspberry Pi. Data is stored on an external USB drive (BEAMdrive), enabling easy access and management of recorded audio and environmental logs.

## Hardware Setup
The system includes:
1. **Audio Recording Device**: A microphone connected to the Raspberry Pi.
2. **BME280 Environmental Sensor**: For temperature, humidity, and pressure measurements, connected over SPI.

### Connections for BME280 Sensor (SPI)
- **VCC**: Connect to Pin 1 (3.3V)
- **GND**: Connect to Pin 6 (Ground)
- **SDA/MOSI**: Connect to Pin 19 (SPI MOSI)
- **SCL/SCK**: Connect to Pin 23 (SPI SCLK)
- **ADDR/MISO**: Connect to Pin 21 (SPI MISO)
- **CS**: Connect to Pin 29 (GPIO Pin 5) _(This can be changed if needed, but the script assumes this configuration.)_

## Software Setup
The project includes two Python scripts:
1. **Audio Recording Script**
2. **Environmental Data Collection Script**

Both scripts save data to an external USB drive named `BEAMdrive`.

### Prerequisites
- Python installed on the Raspberry Pi
- Required libraries: `pyaudio`, `wave`, `board`, `digitalio`, `busio`, `adafruit_bme280`
- **Note**: Install the libraries via `pip` or from source, if needed.

## Scripts

### 1. Audio Recording Script
This script records a 5-minute audio sample at the beginning of each hour and saves it to `BEAMdrive` as a `.wav` file.

**Key Configuration**:
- **Format**: 16-bit Mono
- **Sample Rate**: 48kHz
- **Duration**: 5 minutes

If `BEAMdrive` is not mounted, the script will display an error message.

**File Path**: Audio files are named with a timestamp, e.g., `YYYY-MM-DD_HH-MM-SS.wav`.

### 2. Environmental Data Collection Script
This script logs environmental data from the BME280 sensor at specified intervals (configurable in an extended script version) and appends the readings to a JSON file on `BEAMdrive`.

**Key Variables**:
- **Temperature**: Measured in Celsius
- **Humidity**: Percentage
- **Pressure**: hPa

Each log entry is timestamped, and the data is stored in a JSON-like format in a file named based on the node ID and date, e.g., `Node_1_MM-DD-YY.json`.

## Running the Prototype
1. **Setup Hardware**: Connect the BME280 sensor as specified above.
2. **Mount the USB Drive**: Ensure `BEAMdrive` is mounted at `/media/pi/BEAMdrive`.
3. **Execute Scripts**:
   - Run the audio recording script at the top of every hour.
   - Schedule the environmental data collection script to run periodically (e.g., every hour).
4. **Verify Outputs**:
   - Check for `.wav` files in `BEAMdrive` for audio recordings.
   - Inspect the JSON file for environmental data logs.

## Error Handling
- **Audio Recording**: If the microphone or `BEAMdrive` is not available, the script will exit and print an error message.
- **Sensor Data**: If the BME280 sensor is not accessible, the environmental data script logs an error message and skips the entry.
