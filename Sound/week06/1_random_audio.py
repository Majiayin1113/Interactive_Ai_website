"""Play continuous random noise using PyAudio.

This script writes 32-bit float samples in range [-1.0, 1.0] to the default
output device. It supports an optional duration (seconds) and a random seed.
Press Ctrl-C to stop early.
"""

import argparse
import signal
import sys
import time

import numpy as np
import pyaudio


def main(duration: float | None, seed: int | None) -> int:
    if seed is not None:
        np.random.seed(seed)

    RATE = 44100
    FRAMES_PER_BUFFER = 1024

    p = pyaudio.PyAudio()
    try:
        stream = p.open(format=pyaudio.paFloat32, channels=1, rate=RATE, output=True, frames_per_buffer=FRAMES_PER_BUFFER)
    except Exception as e:
        print("Failed to open audio stream:", e)
        p.terminate()
        return 2

    stop = False

    def _on_sigint(signum, frame):
        nonlocal stop
        stop = True

    signal.signal(signal.SIGINT, _on_sigint)

    start = time.time()
    try:
        print("Starting random audio. Press Ctrl-C to stop.")
        while not stop:
            # If duration given, check elapsed time
            if duration is not None and (time.time() - start) >= duration:
                break

            # generate a small buffer of noise in range [-1, 1]
            buf = np.random.uniform(low=-1.0, high=1.0, size=FRAMES_PER_BUFFER).astype(np.float32)
            stream.write(buf.tobytes())

        print("Stopping playback")
    finally:
        try:
            stream.stop_stream()
            stream.close()
        except Exception:
            pass
        p.terminate()

    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Play random audio (noise) to the default output device")
    parser.add_argument("--duration", "-d", type=float, default=None, help="Duration in seconds (default: run until interrupted)")
    parser.add_argument("--seed", "-s", type=int, default=None, help="Optional RNG seed for reproducible noise")
    args = parser.parse_args()

    exit_code = main(args.duration, args.seed)
    sys.exit(exit_code)




