"""Audio loopback utility using PyAudio

Features:
- List available audio devices
- Choose input and output device (or use defaults)
- Low-latency loopback using a callback

Usage:
  python audio_loopback.py            # use defaults
  python audio_loopback.py --in 1 --out 3
"""
import argparse
import sys
import time

import pyaudio
import numpy as np


def list_devices(p: pyaudio.PyAudio):
    info = p.get_host_api_info_by_index(0)
    device_count = info.get('deviceCount', 0)
    print('Available audio devices:')
    for i in range(device_count):
        dev = p.get_device_info_by_host_api_device_index(0, i)
        print(f"  {i}: {dev.get('name')} - input:{dev.get('maxInputChannels')} output:{dev.get('maxOutputChannels')}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--list', action='store_true', help='List audio devices and exit')
    parser.add_argument('--in', dest='in_dev', type=int, default=None, help='Input device index')
    parser.add_argument('--out', dest='out_dev', type=int, default=None, help='Output device index')
    parser.add_argument('--rate', type=int, default=44100, help='Sample rate')
    parser.add_argument('--frames-per-buffer', type=int, default=1024, help='Frames per buffer')
    parser.add_argument('--echo-delay', type=float, default=0.0, help='Echo delay in seconds (0 to disable)')
    parser.add_argument('--echo-decay', type=float, default=0.5, help='Echo decay factor (0..1)')
    parser.add_argument('--water', action='store_true', help='Enable underwater (artistic) echo effect')
    parser.add_argument('--water-taps', type=int, default=4, help='Number of underwater echo taps')
    parser.add_argument('--water-delay', type=float, default=0.12, help='Base delay (s) between underwater taps')
    parser.add_argument('--water-decay', type=float, default=0.6, help='Decay factor per tap for underwater effect')
    parser.add_argument('--water-lpf', type=float, default=0.6, help='Low-pass smoothing (0..1) for underwater muffling')
    parser.add_argument('--water-wet', type=float, default=0.8, help='Wet mix for underwater effect (0..1)')
    args = parser.parse_args()

    p = pyaudio.PyAudio()
    try:
        if args.list:
            list_devices(p)
            return

        # Choose defaults
        in_device = args.in_dev
        out_device = args.out_dev

        if in_device is None or out_device is None:
            # choose first input and first output if not specified
            default_in = None
            default_out = None
            for i in range(p.get_device_count()):
                dev = p.get_device_info_by_index(i)
                if default_in is None and dev.get('maxInputChannels', 0) > 0:
                    default_in = i
                if default_out is None and dev.get('maxOutputChannels', 0) > 0:
                    default_out = i
            in_device = in_device if in_device is not None else default_in
            out_device = out_device if out_device is not None else default_out

        if in_device is None or out_device is None:
            print('No suitable input/output devices found. Use --list to inspect devices.')
            return

        sample_rate = args.rate
        frames_per_buffer = args.frames_per_buffer

        print(f'Using input device {in_device}, output device {out_device}, rate {sample_rate}, buffer {frames_per_buffer}')

        # Open output stream first
        out_stream = p.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=sample_rate,
                            output=True,
                            output_device_index=out_device,
                            frames_per_buffer=frames_per_buffer)

        # If echo is enabled, create an echo buffer
        echo_buffer = []
        max_echo_frames = 0
        if args.echo_delay and args.echo_delay > 0:
            max_echo_frames = int(sample_rate * args.echo_delay / frames_per_buffer)

        # For underwater effect we will also keep a frame buffer (same structure)
        water_buffer = []
        water_max_delay_frames = 0
        if args.water and args.water_delay > 0:
            # base delay in frames for water taps
            water_max_delay_frames = int(sample_rate * args.water_delay / frames_per_buffer)

        def add_echo(audio_data: bytes, delay_frames: int, decay: float):
            """Simple frame-based echo: keep a rotating buffer of previous frames and mix older frame with current one."""
            nonlocal echo_buffer
            echo_buffer.append(audio_data)
            if delay_frames <= 0:
                return audio_data
            if len(echo_buffer) > delay_frames:
                old = echo_buffer.pop(0)
                # mix int16 arrays
                cur = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32)
                prev = np.frombuffer(old, dtype=np.int16).astype(np.float32)
                mixed = cur + prev * decay
                mixed = np.clip(mixed, -32768, 32767)
                return mixed.astype(np.int16).tobytes()
            return audio_data


        def add_underwater_echo(audio_data: bytes, base_delay_frames: int, taps: int, decay: float, lpf: float, wet: float):
            """Artistic 'underwater' echo implemented with multiple taps and low-pass filtering.
            - base_delay_frames: delay between taps in frames
            - taps: number of delayed echoes
            - decay: decay factor per tap
            - lpf: 0..1 smoothing factor, maps to moving-average kernel size
            - wet: wet mix (0..1)
            """
            nonlocal water_buffer
            # Convert current frame to float32 array
            cur = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32)
            out = cur.copy()

            # Append current frame to buffer for future taps
            water_buffer.append(audio_data)

            # Determine kernel size from lpf parameter
            kernel_size = max(1, int(lpf * 25))
            if kernel_size > 1:
                kernel = np.ones(kernel_size, dtype=np.float32) / kernel_size

            # Mix multiple taps
            for i in range(1, taps + 1):
                idx = - i * base_delay_frames
                if abs(idx) <= len(water_buffer):
                    prev_bytes = water_buffer[idx]
                    prev = np.frombuffer(prev_bytes, dtype=np.int16).astype(np.float32)
                    # apply simple low-pass (moving average) to simulate muffling
                    if kernel_size > 1:
                        prev_filtered = np.convolve(prev, kernel, mode='same')
                    else:
                        prev_filtered = prev
                    factor = (decay ** i) * wet
                    out += prev_filtered * factor

            out = np.clip(out, -32768, 32767)
            return out.astype(np.int16).tobytes()

        # Callback will write incoming (optionally processed) data to output stream
        def callback(in_data, frame_count, time_info, status):
            try:
                data_to_write = in_data
                # Underwater artistic effect (multiple muffled taps)
                if args.water:
                    if water_max_delay_frames <= 0:
                        # fallback: use single-frame delay
                        data_to_write = add_underwater_echo(in_data, 1, args.water_taps, args.water_decay, args.water_lpf, args.water_wet)
                    else:
                        data_to_write = add_underwater_echo(in_data, water_max_delay_frames, args.water_taps, args.water_decay, args.water_lpf, args.water_wet)
                # Regular simple echo
                elif max_echo_frames > 0 and args.echo_decay > 0:
                    data_to_write = add_echo(in_data, max_echo_frames, args.echo_decay)

                out_stream.write(data_to_write)
            except Exception as e:
                # If writing fails just ignore to avoid crashing the callback
                print('Output write error:', e, file=sys.stderr)
            return (None, pyaudio.paContinue)

        in_stream = p.open(format=pyaudio.paInt16,
                           channels=1,
                           rate=sample_rate,
                           input=True,
                           input_device_index=in_device,
                           frames_per_buffer=frames_per_buffer,
                           stream_callback=callback)

        print('Starting loopback. Press Ctrl+C to stop.')
        in_stream.start_stream()

        try:
            while in_stream.is_active():
                time.sleep(0.1)
        except KeyboardInterrupt:
            print('Interrupted by user. Stopping...')

        in_stream.stop_stream()
        in_stream.close()
        out_stream.stop_stream()
        out_stream.close()

    finally:
        p.terminate()


if __name__ == '__main__':
    main()
