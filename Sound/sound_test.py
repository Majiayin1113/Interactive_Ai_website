"""Simple audio playback test using PyAudio

Plays a 440Hz sine wave for 2 seconds to test audio output.
"""
import math
import struct
import time

import pyaudio

def play_sine(frequency=440.0, duration=2.0, rate=44100, volume=0.5):
    p = pyaudio.PyAudio()
    try:
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=rate,
                        output=True)

        frames = []
        for i in range(int(rate * duration)):
            sample = volume * math.sin(2 * math.pi * frequency * (i / rate))
            # 16-bit signed int
            frames.append(struct.pack('<h', int(sample * 32767)))

        stream.write(b''.join(frames))
        stream.stop_stream()
        stream.close()
        print(f"Played {frequency} Hz for {duration} seconds")
    finally:
        p.terminate()


if __name__ == '__main__':
    print("Starting audio test...")
    play_sine()
    print("Audio test finished")
