import sys
import os
import time
import math
import queue
import threading
import numpy as np

try:
    import pyaudio
except Exception:
    print("pyaudio is required. Install with: python -m pip install pyaudio")
    raise

try:
    import pygame
except Exception:
    print("pygame is required. Install with: python -m pip install pygame")
    raise

"""
voice_parkour.py

Simple microphone-controlled runner/jumper game.

Controls (microphone):
- When the microphone input is silent, the player stands still.
- When the microphone volume increases, the player runs forward and can jump.
- Louder sounds produce higher jumps.

This is intentionally minimal and uses RMS over short frames to determine "loudness".
"""

WIDTH, HEIGHT = 800, 400
GROUND_Y = HEIGHT - 80

CHUNK = 1024
RATE = 16000
FORMAT = pyaudio.paInt16
CHANNELS = 1


def rms_from_bytes(data, width=2):
    # data is bytes from stream with int16 samples
    arr = np.frombuffer(data, dtype=np.int16).astype(np.float32)
    if arr.size == 0:
        return 0.0
    return math.sqrt(float((arr ** 2).mean()))


class MicrophoneReader(threading.Thread):
    def __init__(self, device_index=None):
        super().__init__(daemon=True)
        self.pa = pyaudio.PyAudio()
        self.device_index = device_index
        self.stream = None
        self.queue = queue.Queue()
        self.running = False

    def list_devices(self):
        info = self.pa.get_host_api_info_by_index(0)
        count = info.get('deviceCount', 0)
        devices = []
        for i in range(count):
            dev = self.pa.get_device_info_by_host_api_device_index(0, i)
            devices.append((i, dev.get('name'), dev.get('maxInputChannels')))
        return devices

    def start_stream(self):
        kwargs = dict(format=FORMAT, channels=CHANNELS, rate=RATE, input=True,
                      frames_per_buffer=CHUNK)
        if self.device_index is not None:
            kwargs['input_device_index'] = self.device_index
        self.stream = self.pa.open(**kwargs)
        self.running = True
        self.start()

    def run(self):
        while self.running:
            try:
                data = self.stream.read(CHUNK, exception_on_overflow=False)
            except Exception:
                continue
            rms = rms_from_bytes(data)
            # normalize RMS to 0..1 roughly (int16 full-scale ~32768)
            # use a more conservative divider so values are larger for typical mics
            norm = min(1.0, rms / 2000.0)
            self.queue.put((rms, norm))

    def read_level(self, default=0.0):
        # consume latest value if available
        last = (0.0, default)
        while not self.queue.empty():
            try:
                last = self.queue.get_nowait()
            except Exception:
                break
        return last

    def stop(self):
        self.running = False
        try:
            if self.stream is not None:
                self.stream.stop_stream()
                self.stream.close()
        except Exception:
            pass
        try:
            self.pa.terminate()
        except Exception:
            pass


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Voice Parkour - Louder = Higher Jump')
    clock = pygame.time.Clock()

    mic = MicrophoneReader()
    devices = mic.list_devices()
    print('Input devices:')
    for i, name, chans in devices:
        if chans > 0:
            print(f'  {i}: {name} (in-ch={chans})')
    mic.start_stream()

    # Player state (a little chick)
    player_x = 120
    player_y = GROUND_Y
    vel_y = 0.0
    on_ground = True

    # Game state
    scroll_x = 0
    base_speed = 180.0  # chick always runs forward
    speed = base_speed
    obstacles = []
    score = 0
    spawn_timer = 0.0
    spawn_interval = 1.2

    font = pygame.font.SysFont(None, 24)
    # try to load external fish sprite
    SPRITE_PATH = r'F:\\PolyU\\Sem1\\5913Programming\\Interactive_Website\\fish.png'
    fish_sprite = None
    try:
        if os.path.exists(SPRITE_PATH):
            fish_sprite = pygame.image.load(SPRITE_PATH).convert_alpha()
            # scale to reasonable in-game size (approx 56x28)
            fish_sprite = pygame.transform.smoothscale(fish_sprite, (56, 28))
    except Exception:
        fish_sprite = None
    try:
        running = True
        last_time = time.time()
        # smoothing for display and stability
        smooth_level = 0.0
        smooth_db = -120.0
        ema_alpha = 0.15
        sensitivity = 1.0  # multiplier for jump strength
        while running:
            dt = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # read microphone level (0..1)
            level = mic.read_level(0.0)

            # level is a tuple (rms, norm)
            rms_val, raw_level = level

            # apply smoothing (EMA) to the normalized level
            smooth_level = (1.0 - ema_alpha) * smooth_level + ema_alpha * raw_level

            # compute approximate dBFS from rms relative to int16 full-scale
            if rms_val <= 1e-6:
                frame_db = -120.0
            else:
                frame_db = 20.0 * math.log10(rms_val / 32768.0)
            smooth_db = (1.0 - ema_alpha) * smooth_db + ema_alpha * frame_db

            # Map smoothed level to jump impulse; chick always runs forward at base_speed
            speed = base_speed

            # jumping: louder -> higher jump; use a threshold to trigger
            jump_threshold = 0.12
            if smooth_level > jump_threshold and on_ground:
                strength = max(0.0, min(1.0, (smooth_level - jump_threshold) / (1.0 - jump_threshold)))
                # corrected impulse (do NOT multiply by dt here)
                impulse = - (0.85 + strength * 2.8) * 700.0 * sensitivity
                vel_y = impulse
                on_ground = False

            # physics
            gravity = 1800.0
            vel_y += gravity * dt
            player_y += vel_y * dt
            if player_y >= GROUND_Y:
                player_y = GROUND_Y
                vel_y = 0.0
                on_ground = True

            # horizontal movement: scroll world
            scroll_x += speed * dt

            # spawn obstacles
            spawn_timer += dt
            if spawn_timer >= spawn_interval:
                spawn_timer = 0.0
                # obstacles are tuples (x, w, h)
                ox = scroll_x + WIDTH + 50
                w = 36
                h = 36
                obstacles.append([ox, w, h, False])

            # move obstacles left relative to scroll
            for ob in obstacles:
                ob[0] -= speed * dt

            # remove passed obstacles and increase score
            new_obs = []
            for ob in obstacles:
                ox, w, h, passed = ob
                if ox + w < 0:
                    # scrolled off screen
                    if not passed:
                        score += 1
                    continue
                new_obs.append(ob)
            obstacles = new_obs

            # draw
            screen.fill((135, 206, 235))  # sky
            # ground
            pygame.draw.rect(screen, (80, 160, 60), (0, GROUND_Y + 40, WIDTH, HEIGHT - GROUND_Y))

            # draw layered wave background (vector style)
            for i, (wave_h, color, offset) in enumerate([(120, (100, 160, 220), 0), (80, (90, 150, 210), 30), (40, (70, 130, 200), 60)]):
                # draw a simple sinusoidal band using ellipses/polygons approximation
                step = 40
                points = []
                for x in range(-step, WIDTH + step, step):
                    y = int(GROUND_Y - wave_h + math.sin((x + scroll_x * 0.2 + offset) * 0.02) * 12)
                    points.append((x, y))
                # close polygon to bottom
                points.append((WIDTH, HEIGHT))
                points.append((0, HEIGHT))
                pygame.draw.polygon(screen, color, points)

            # draw obstacles as angry piranhas (vector shapes)
            fish_rect = pygame.Rect(player_x, player_y - 28, 56, 28)
            for ob in obstacles:
                ox, w, h, _ = ob
                # piranha body
                body_rect = pygame.Rect(int(ox), GROUND_Y - h, w, h)
                body_color = (180, 40, 40)
                pygame.draw.ellipse(screen, body_color, body_rect)
                # eye
                ex = int(ox + w * 0.65)
                ey = GROUND_Y - h + int(h * 0.3)
                pygame.draw.circle(screen, (255, 255, 255), (ex, ey), max(2, w // 8))
                pygame.draw.circle(screen, (0, 0, 0), (ex, ey), max(1, w // 16))
                # teeth (triangles)
                tx = int(ox + w * 0.15)
                ty = GROUND_Y - h + int(h * 0.35)
                for t in range(3):
                    p1 = (tx + t * (w // 6), ty + 2)
                    p2 = (tx + t * (w // 6) + (w // 12), ty - 6)
                    p3 = (tx + t * (w // 6) + (w // 6), ty + 2)
                    pygame.draw.polygon(screen, (255, 255, 255), [p1, p2, p3])

            # draw fish player: external sprite if available, otherwise vector fallback
            fx = player_x
            fy = player_y - 20
            if fish_sprite is not None:
                screen.blit(fish_sprite, (fx, fy - 8))
                fish_rect = pygame.Rect(fx, fy - 8, 56, 28)
            else:
                # body
                pygame.draw.ellipse(screen, (80, 200, 200), (fx, fy - 8, 56, 28))
                # tail
                pygame.draw.polygon(screen, (60, 170, 170), [(fx - 8, fy + 6), (fx - 8, fy - 6), (fx - 20, fy)])
                # eye
                pygame.draw.circle(screen, (255, 255, 255), (fx + 40, fy - 4), 5)
                pygame.draw.circle(screen, (0, 0, 0), (fx + 40, fy - 4), 2)
                # fin
                pygame.draw.polygon(screen, (70, 180, 180), [(fx + 12, fy - 8), (fx + 24, fy - 18), (fx + 36, fy - 8)])
                fish_rect = pygame.Rect(fx, fy - 8, 56, 28)

            # collision detection
            for ob in obstacles:
                ox, w, h, passed = ob
                ob_rect = pygame.Rect(int(ox), GROUND_Y - h, w, h)
                if fish_rect.colliderect(ob_rect):
                    # game over: show message and reset
                    msg = font.render(f'Hit! Score: {score}. Close window to quit or wait to restart.', True, (255, 0, 0))
                    screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 20))
                    pygame.display.flip()
                    time.sleep(1.2)
                    # reset
                    obstacles.clear()
                    scroll_x = 0
                    score = 0
                    spawn_timer = 0.0
                    break

            # mark obstacles as passed if chick passed
            for ob in obstacles:
                if not ob[3] and (ob[0] + ob[1]) < player_x:
                    ob[3] = True

            # HUD
            player_rect = fish_rect

            # HUD
            txt = font.render(f'Level: {smooth_level:.3f}  Score: {score}', True, (0, 0, 0))
            screen.blit(txt, (8, 8))
            instr = font.render('Chick auto-runs. Make sound to jump higher and clear obstacles.', True, (0, 0, 0))
            screen.blit(instr, (8, 32))

            # top-right: amplified numeric level + dB and a vertical meter
            meter_x = WIDTH - 120
            meter_y = 8
            meter_w = 16
            meter_h = 64

            # amplify small values for visibility (sqrt scaling)
            vis_level = math.sqrt(smooth_level)
            vis_level = max(0.0, min(1.0, vis_level * 1.05))

            # color by level
            if vis_level < 0.33:
                color = (30, 160, 30)
            elif vis_level < 0.66:
                color = (220, 180, 20)
            else:
                color = (200, 30, 30)

            # draw meter background
            pygame.draw.rect(screen, (200, 200, 200), (meter_x, meter_y, meter_w, meter_h))
            fill_h = int(meter_h * vis_level)
            pygame.draw.rect(screen, color, (meter_x, meter_y + (meter_h - fill_h), meter_w, fill_h))

            # bigger text for numeric readout
            big_font = pygame.font.SysFont(None, 28)
            right_txt = big_font.render(f'{smooth_level:.3f}', True, color)
            db_txt = font.render(f'{smooth_db:.1f} dB', True, (0, 0, 0))
            screen.blit(right_txt, (meter_x + meter_w + 8, meter_y))
            screen.blit(db_txt, (meter_x + meter_w + 8, meter_y + 26))

            pygame.display.flip()

    finally:
        mic.stop()
        pygame.quit()


if __name__ == '__main__':
    main()
