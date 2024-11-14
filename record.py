# Audio Recording Script for Raspberry Pi
# Author: Raiz Mohammed
# Description: This script records audio using a connected microphone and saves 
# the recording to an external USB drive (BEAMdrive) on the Raspberry Pi.

import os         # To interact with the operating system for checking mount status
import pyaudio    # For audio recording
import wave       # To save recorded audio in .wav format
import time       # To timestamp the audio file


def record_audio():
    """
    Records audio for a specified duration and saves it to the BEAMdrive.
    Audio settings and duration are configurable in the function.
    """
    
    # Audio format configuration
    FORMAT = pyaudio.paInt16       # Sample format: 16-bit audio
    CHANNELS = 1                   # Number of audio channels: Mono
    RATE = 48000                   # Sample rate: 48kHz (common for high-quality audio)
    CHUNK = 1024                   # Buffer size for reading audio data
    RECORD_SECONDS = 5 * 60        # Duration of the recording (5 minutes)
    AUDIO_DEVICE_INDEX = None        # Index for the audio input device

    audio = pyaudio.PyAudio()      # Initialize PyAudio object for audio recording

    try:
        # Generate a unique filename based on the current timestamp
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"/media/pi/BEAMdrive/{timestamp}.wav"  # File path on BEAMdrive

        # Check if the BEAMdrive is mounted; exit if not
        if not os.path.ismount("/media/pi/BEAMdrive"):
            print("BEAMdrive not mounted.")
            return

        # Open an audio input stream with specified settings
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True, input_device_index=AUDIO_DEVICE_INDEX,
                            frames_per_buffer=CHUNK)

        print("Recording audio...")  # Notify the user that recording has started

        frames = []  # List to store chunks of recorded audio data

        # Loop to read audio data in chunks and store it in frames
        for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK, exception_on_overflow = False)  # Read a chunk of audio data
            frames.append(data)        # Append it to the frames list

        # Stop and close the audio stream once recording is complete
        stream.stop_stream()
        stream.close()

        # Save recorded audio data to a .wav file
        with wave.open(filename, 'wb') as waveFile:
            waveFile.setnchannels(CHANNELS)                    # Set number of channels
            waveFile.setsampwidth(audio.get_sample_size(FORMAT))  # Set sample width
            waveFile.setframerate(RATE)                        # Set frame rate
            waveFile.writeframes(b''.join(frames))             # Write audio frames to file

        print(f"Recording saved to {filename}")  # Confirm file save to the user

    except (IOError, OSError) as e:
        # Handle file or audio device errors and print a message
        print(f"File or audio device error: {e}")

    except Exception as e:
        # General exception handler for any unexpected errors
        print(f"Unexpected error occurred: {e}")

    finally:
        # Terminate PyAudio instance to release audio resources
        audio.terminate()

# Invoke the record_audio function to start recording
record_audio()
