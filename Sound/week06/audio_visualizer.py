import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 音频配置
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

class AudioVisualizer:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.volume_data = [0.0] * 50  # 保存最近50个音量值 (normalized 0..1 for display)
        self.line, = self.ax.plot(self.volume_data, lw=2)
        self.ax.set_ylim(0, 1)
        self.ax.set_title('实时音量可视化')
        # 文本显示实时 dB 值（右上角）
        self.db_text = self.ax.text(0.98, 0.95, '', transform=self.ax.transAxes,
                                     horizontalalignment='right', verticalalignment='top', fontsize=10,
                                     bbox=dict(facecolor='white', alpha=0.6, edgecolor='none'))

        # 初始化PyAudio
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK
        )
    
    def calculate_volume_db(self, data, min_db=-80.0):
        """计算音频数据的 RMS 并返回 dB 值及归一化 0..1 显示值"""
        audio_data = np.frombuffer(data, dtype=np.int16).astype(np.float32)
        if audio_data.size == 0:
            return min_db, 0.0
        rms = np.sqrt(np.mean(audio_data**2)) / 32768.0
        # 防止 log(0)
        if rms <= 1e-10:
            db = min_db
        else:
            db = 20.0 * np.log10(rms)
            if db < min_db:
                db = min_db

        # 归一化 dB -> 0..1（min_db -> 0, 0dB -> 1）并放大低音量变化
        norm = (db - min_db) / (-min_db)
        # 可选的非线性增强，让小幅变化更明显
        display_val = np.sqrt(norm)
        return db, float(display_val)
    
    def update(self, frame):
        """更新图表"""
        # 读取音频数据
        data = self.stream.read(CHUNK, exception_on_overflow=False)

        # 计算 dB 与用于显示的归一化值
        db, display_val = self.calculate_volume_db(data)

        # 更新数据队列
        self.volume_data.append(display_val)
        if len(self.volume_data) > 50:
            self.volume_data.pop(0)

        # 更新图表与文本（右上角显示 dB）
        self.line.set_ydata(self.volume_data)
        self.db_text.set_text(f'{db:.1f} dB')

        return self.line, self.db_text
    
    def start(self):
        """启动可视化"""
        print("开始声控可视化...")
        print("请对着麦克风说话或制造声音")
        print("关闭窗口以退出")
        
        ani = FuncAnimation(self.fig, self.update, blit=True, interval=50)
        plt.show()
    
    def close(self):
        """清理资源"""
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

if __name__ == "__main__":
    visualizer = AudioVisualizer()
    try:
        visualizer.start()
    finally:
        visualizer.close()
