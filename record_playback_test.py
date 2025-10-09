"""Record from input device and play back through output device for verification.

Usage:
  python record_playback_test.py --in 1 --out 3 --seconds 3
"""
import argparse
import wave
import sys

import pyaudio


def record_and_play(in_dev, out_dev, seconds=3, rate=44100, frames_per_buffer=1024):
    p = pyaudio.PyAudio()
    try:
        print(f'Recording {seconds}s from device {in_dev}...')
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=rate,
                        input=True,
                        input_device_index=in_dev,
                        frames_per_buffer=frames_per_buffer)

        frames = []
        for _ in range(0, int(rate / frames_per_buffer * seconds)):
            data = stream.read(frames_per_buffer, exception_on_overflow=False)
            frames.append(data)

        stream.stop_stream()
        stream.close()

        print('Playing back...')
        out = p.open(format=pyaudio.paInt16,
                     channels=1,
                     rate=rate,
                     output=True,
                     output_device_index=out_dev,
                     frames_per_buffer=frames_per_buffer)

        for chunk in frames:
            out.write(chunk)

        out.stop_stream()
        out.close()
        print('Done playback')
    finally:
        p.terminate()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--in', dest='in_dev', type=int, default=1)
    parser.add_argument('--out', dest='out_dev', type=int, default=3)
    parser.add_argument('--seconds', type=int, default=3)
    args = parser.parse_args()

    record_and_play(args.in_dev, args.out_dev, seconds=args.seconds)


if __name__ == '__main__':
    main()
