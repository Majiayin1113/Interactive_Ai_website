"""Record or load audio and visualize waveform and spectrogram.

Usage examples:
  python voice_visualize.py --record 3
  python voice_visualize.py --file path/to/file.wav
"""
import argparse
import tempfile
import wave
import os
import sys
import time

import numpy as np
import matplotlib.pyplot as plt
import pyaudio


def record_to_wav(seconds, out_path, rate=44100, frames_per_buffer=1024):
    p = pyaudio.PyAudio()
    try:
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=rate,
                        input=True,
                        frames_per_buffer=frames_per_buffer)

        frames = []
        for _ in range(0, int(rate / frames_per_buffer * seconds)):
            data = stream.read(frames_per_buffer, exception_on_overflow=False)
            frames.append(data)

        stream.stop_stream()
        stream.close()

        wf = wave.open(out_path, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
        wf.close()
    finally:
        p.terminate()


def visualize_wav(path):
    with wave.open(path, 'rb') as wf:
        rate = wf.getframerate()
        n_frames = wf.getnframes()
        data = wf.readframes(n_frames)
        samples = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0

    times = np.linspace(0, n_frames / rate, num=n_frames)

    plt.figure(figsize=(12, 6))

    plt.subplot(2, 1, 1)
    plt.plot(times, samples)
    plt.title('Waveform')
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')

    plt.subplot(2, 1, 2)
    # Spectrogram
    plt.specgram(samples, NFFT=1024, Fs=rate, noverlap=512, cmap='inferno')
    plt.title('Spectrogram')
    plt.xlabel('Time [s]')
    plt.ylabel('Frequency [Hz]')

    plt.tight_layout()
    plt.show()


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--record', type=int, help='Record seconds from default mic')
    group.add_argument('--file', type=str, help='Path to WAV file')
    parser.add_argument('--base-dir', type=str, default=r'F:\\PolyU\\Sem1\\5913Programming', help='Base directory for temporary output')
    args = parser.parse_args()

    if args.record:
        # use base-dir for temp wav if available
        out_dir = args.base_dir
        os.makedirs(out_dir, exist_ok=True)
        tmp_path = os.path.join(out_dir, f'tmp_record_{int(time.time())}.wav')
        print(f'Recording {args.record}s to {tmp_path}...')
        record_to_wav(args.record, tmp_path)
        visualize_wav(tmp_path)
        os.remove(tmp_path)
    else:
        if not os.path.exists(args.file):
            print('File not found:', args.file)
            sys.exit(1)
        visualize_wav(args.file)


if __name__ == '__main__':
    main()
