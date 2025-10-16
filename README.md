# 🎨 FunnyWebsite - 多功能AI互动网站

## 📖 项目简介

**FunnyWebsite** 是一个集成了三大核心功能的AI互动网站，包括AI图像生成、实时人脸识别和声控游戏。采用Streamlit框架构建，支持中英文双语界面。

---

## ✨ 核心功能

### 1. 🎨 AI图像生成器
基于 Stable Diffusion v1.5 的文本生成图像系统
- 📝 **文本生成图像**：输入文字描述，AI自动生成高质量图片
- 🎯 **预设模板**：内置6种常用提示词（可爱小狗、美丽风景、未来城市等）
- ⚙️ **参数调节**：自定义图像尺寸（512x512/768x512/512x768）和生成步数
- 💾 **一键下载**：生成的图片可直接下载保存
- 🚀 **GPU加速**：支持CUDA加速，提升生成速度
- 📚 **历史记录**：保存最近10次生成的图像

### 2. 📹 智能人脸识别
基于 OpenCV + WebRTC 的实时视频处理系统
- 👤 **实时检测**：自动识别画面中的多个人脸
- 🎭 **掉落特效**：检测到的人脸会复制并从顶部掉落
- 🏗️ **物理模拟**：真实的重力、弹跳、摩擦效果
- 📚 **垂直堆叠**：掉落的人脸可以像积木一样层层堆叠
- ⏱️ **10秒消失**：每个掉落人脸显示倒计时，10秒后自动清除
- 🎨 **自定义设置**：可调节检测框颜色、灵敏度、掉落速度

### 3. 🐟 FishJump 声控游戏
麦克风声音控制的跳跃类游戏
- 🎤 **声音控制**：通过麦克风声音控制小鱼跳跃
- 📢 **音量响应**：声音越大，跳得越高
- 🦈 **躲避障碍**：避开红色食人鱼障碍物
- 🏆 **记录保存**：自动保存最高分记录
- 🎮 **独立窗口**：游戏在独立Pygame窗口运行

---

## 🚀 快速开始

### 环境要求
- Python 3.8+
- 摄像头设备（用于人脸识别）
- 麦克风设备（用于FishJump游戏）
- CUDA兼容GPU（可选，用于加速图像生成）

### 安装步骤

1. **克隆项目**
   ```bash
   git clone https://github.com/Majiayin1113/Interactive_Ai_website.git
   cd Interactive_Ai_website
   ```

2. **创建虚拟环境（推荐）**
   
   Windows PowerShell:
   ```powershell
   .\create_venv.ps1 -VenvName .venv
   .\.venv\Scripts\Activate.ps1
   ```
   
   Linux/macOS:
   ```bash
   ./create_venv.sh .venv
   source .venv/bin/activate
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **运行应用**
   ```bash
   streamlit run Website1/week05/FunnyWebsite.py
   ```

5. **访问应用**
   - 浏览器自动打开，或手动访问：`http://localhost:8501`

---

## 🎮 使用指南

### AI图像生成器
1. 点击侧边栏"🎨 图像生成"
2. 在文本框输入描述或选择预设模板
3. 调整图像尺寸和生成步数
4. 点击"生成图像"按钮
5. 等待生成完成（10-30秒）
6. 下载或重新生成

### 人脸识别摄像头
1. 点击侧边栏"📹 人脸识别"
2. 点击"START"按钮启动摄像头
3. 允许浏览器访问摄像头权限
4. 调整检测灵敏度和掉落效果
5. 面向摄像头观察实时检测和掉落效果
6. 多人同时检测可观察堆叠效果

### FishJump游戏
1. 点击侧边栏"🐟 FishJump"
2. 查看游戏说明和操作方式
3. 点击"启动游戏"按钮
4. 游戏在新窗口启动
5. 对着麦克风发声控制小鱼跳跃
6. 躲避障碍，获取高分

---

## 📦 核心依赖

```
streamlit>=1.28.0          # Web应用框架
streamlit-webrtc>=0.45.0   # 实时视频流处理
diffusers>=0.21.0          # Stable Diffusion模型
torch>=2.0.0               # 深度学习框架
opencv-python>=4.8.0       # 计算机视觉库
transformers>=4.30.0       # Transformer模型
pygame>=2.5.0              # 游戏开发库
pyaudio>=0.2.13            # 音频处理
```

---

## 🛠️ 技术架构

```
FunnyWebsite
├── Streamlit前端框架
│   ├── 多页面导航系统
│   ├── 中英文双语切换
│   └── 响应式布局设计
│
├── AI图像生成模块
│   ├── Stable Diffusion v1.5
│   ├── Diffusers Pipeline
│   └── PyTorch + CUDA
│
├── 人脸识别模块
│   ├── OpenCV人脸检测
│   ├── WebRTC视频流
│   ├── 自定义物理引擎
│   └── 碰撞堆叠系统
│
└── 声控游戏模块
    ├── PyAudio音频采集
    ├── Pygame游戏引擎
    └── 实时音量分析
```

---

## 🐛 常见问题

### 摄像头无法启动
- 检查浏览器摄像头权限
- 确认其他程序未占用摄像头
- 刷新页面重新授权

### 图像生成速度慢
- 确认是否启用GPU加速
- 减少生成步数提高速度
- 降低图像分辨率

### 游戏无法启动
- 检查是否安装PyAudio和Pygame
- 确认麦克风权限已授予
- 查看终端错误信息

---

## 📂 项目结构

```
Interactive_Ai_website/
├── README.md                    # 项目说明文档
├── requirements.txt             # Python依赖列表
├── create_venv.ps1             # Windows虚拟环境创建脚本
├── create_venv.sh              # Linux/Mac虚拟环境创建脚本
├── voice_parkour.py            # FishJump游戏主程序
├── highscore.txt               # 游戏最高分记录
│
├── Website1/week05/
│   ├── FunnyWebsite.py         # 主应用程序
│   ├── requirements.txt        # 模块依赖
│   └── ...                     # 其他辅助文件
│
├── Game/                       # 游戏相关文件
└── Sound/                      # 音频处理文件
```

---

## 🌐 语言支持

- 🇨🇳 **简体中文**：完整的中文界面和提示词支持
- 🇺🇸 **English**：Complete English interface and prompt support

可在侧边栏随时切换语言，所有功能均支持双语操作。

---

## 📝 开发日志

### v2.0.0 (2025-10-16)
- ✨ 新增FishJump声控游戏模块
- ✨ 完善三模块导航系统
- 🎨 优化UI界面和图标显示
- 🌐 增强双语支持

### v1.5.0 (2025-10-02)
- ✨ 添加人脸垂直堆叠功能
- 🔧 优化物理引擎稳定性
- 📱 改进移动端兼容性

### v1.0.0 (2025-09-30)
- 🎉 初始版本发布
- ✨ AI图像生成功能
- ✨ 基础人脸检测

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 👥 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📧 联系方式

- 项目维护者：Majiayin1113
- GitHub：[https://github.com/Majiayin1113](https://github.com/Majiayin1113)
- 项目链接：[https://github.com/Majiayin1113/Interactive_Ai_website](https://github.com/Majiayin1113/Interactive_Ai_website)

---

⭐ 如果这个项目对你有帮助，请给我们一个星标！
