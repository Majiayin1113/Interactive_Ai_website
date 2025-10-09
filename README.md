# 🎨 Interactive AI Website - FunnyWebsite

## 🎪 FunnyWebsite Overview

**FunnyWebsite** is an innovative interactive AI website that combines artificial intelligence image generation with real-time face recognition technology, providing users with unique visual experiences and entertainment features. Built with the Streamlit framework, it features a modern bilingual user interface that makes technology fun and creative.

### 🎯 Project Highlights
- **Dual Core Features**: AI Image Generation + Smart Face Recognition
- **Innovative Visual Effects**: Unique gravity-falling animation system
- **Real-time Interaction**: Instant camera processing based on WebRTC
- **Physics Simulation**: Realistic gravity, collision, and stacking effects
- **Internationalization Support**: Complete bilingual interface in Chinese and English

---

## 🚀 FunnyWebsite Core Features

### 💡 Feature 1: AI Intelligent Image Generator

**Technical Core**: Text-to-image generation system based on Stable Diffusion v1.5

#### 📋 Feature Highlights
- **🎨 Creative Generation**: Generate high-quality artistic images from text descriptions
- **🌍 Multi-language Support**: Support for both Chinese and English prompts
- **⚙️ Adjustable Parameters**: Customize image size, inference steps, guidance scale
- **💾 Easy Saving**: One-click download of generated artworks
- **🚀 GPU Acceleration**: CUDA acceleration support for faster generation

#### 🎮 Usage Instructions

1. **Launch Feature**
   ```
   📍 Navigation → Select "AI Image Generator"
   ```

2. **Input Creativity**
   ```
   ✏️ Enter descriptive text in the input box
   Examples: "A unicorn running on a rainbow bridge"
            "A cute robot playing with children in a park"
   ```

3. **Adjust Generation Parameters**
   ```
   📐 Image Size: 512x512 / 768x768 / 1024x1024
   🔢 Inference Steps: 20-50 (more steps = better quality, longer time)
   📏 Guidance Scale: 7.5-15 (higher values = closer to description)
   ```

4. **Start Generation**
   ```
   🎯 Click "Generate Image" button
   ⏳ Wait 10-30 seconds for processing
   📥 Click "Download Image" to save artwork
   ```

---

### 🎭 Feature 2: Smart Face Recognition & Interactive System

**Technical Core**: OpenCV Face Detection + Custom Physics Engine + WebRTC Real-time Video Stream

#### 🌟 Innovative Features
- **👤 Multi-face Detection**: Real-time recognition of multiple faces in the frame
- **🎪 Gravity Falling Effect**: Detected faces are copied and fall from the top
- **🏗️ Vertical Stacking System**: Falling faces stack like building blocks layer by layer
- **⏰ 10-second Survival Mechanism**: Falling faces show countdown and disappear after 10 seconds
- **🎯 Physics Simulation**: Realistic simulation of gravity, bouncing, and friction
- **🎨 Visual Feedback**: Green detection boxes and dynamic effect indicators

#### 🕹️ Usage Instructions

1. **Activate Camera**
   ```
   📍 Navigation → Select "Camera Face Detection"
   📷 Click "Start" button to activate camera
   ✅ Allow browser access to camera permissions
   ```

2. **Adjust Detection Parameters**
   ```
   🎚️ Detection Sensitivity: Slider to adjust recognition accuracy
   🎪 Falling Effect: Toggle to enable/disable falling animation
   ⚡ Falling Speed: Adjust the speed of face descent
   🎨 Visual Settings: Customize detection box color and transparency
   ```

3. **Experience Interactive Effects**
   ```
   👤 Single Person Mode:
      - Face the camera and observe green detection box
      - Detected faces automatically copy and fall
      - Falling faces bounce on the ground and stop

   👥 Multi-person Mode:
      - Multiple people can be detected simultaneously
      - Each person's face falls and stacks separately
      - Forms interesting face tower structures
   ```

4. **Advanced Interactive Tips**
   ```
   🎯 Create Stacking Effects:
      - Quickly enter/exit frame to trigger multiple detections
      - Observe vertical stacking physics effects
      - Watch 10-second countdown cleanup effects

   🎪 Debugging & Optimization:
      - Adjust lighting for clear detection
      - Maintain appropriate distance for better recognition
      - Test detection range from different angles
   ```

---

## 🔧 FunnyWebsite Technical Architecture

### 🏗️ System Components
```
FunnyWebsite Architecture:
┌─────────────────────────────────────────┐
│            Frontend Interface Layer      │
├─────────────────────────────────────────┤
│  Streamlit Web UI + Bilingual System    │
└─────────────────────────────────────────┘
          ↓                    ↓
┌──────────────────┐  ┌──────────────────┐
│  AI Image Module │  │ Face Detection   │
├──────────────────┤  ├──────────────────┤
│• Stable Diffusion│  │• OpenCV Detection│
│• Model Loading   │  │• WebRTC Stream   │
│• Parameter Control│  │• Physics Engine  │
│• Image Processing│  │• Collision System│
└──────────────────┘  └──────────────────┘
```

### ⚙️ Core Technology Stack
- **Frontend Framework**: Streamlit (v1.28+)
- **AI Model**: Stable Diffusion v1.5 + Diffusers
- **Video Processing**: streamlit-webrtc + WebRTC
- **Computer Vision**: OpenCV (v4.8+)
- **Deep Learning**: PyTorch (v2.0+) + CUDA
- **Physics Engine**: Custom gravity simulation system

An interactive web application integrating **AI Image Generation** and **Real-time Face Detection** functionalities.

## 🌟 Main Features

### 📸 **AI Image Generator**
- Generate high-quality images using Stable Diffusion v1.5 model
- Support for Chinese and English prompts
- Adjustable image dimensions and generation parameters
- One-click download of generated images

### 🎭 **Smart Camera Face Detection**
- Real-time face detection and tracking
- Innovative **Gravity Falling Effect**: Detected faces are copied and fall from the top
- **Physics Engine**: Realistic gravity, bounce, and friction simulation
- **Vertical Stacking**: Falling faces can stack like building blocks
- **10-second Survival Mechanism**: Falling faces automatically disappear after 10 seconds
- **Multi-face Support**: Simultaneous detection and processing of multiple faces

### 🌐 **Bilingual Interface**
- Complete Chinese-English interface switching
- All features support bilingual operation

## 🚀 Quick Start

### Requirements

- Python 3.8+
- Camera device
- CUDA-compatible GPU (recommended for AI image generation acceleration)

### Installation Steps

1. **Clone Project**
   ```bash
   git clone https://github.com/Majiayin1113/Interactive_Ai_website.git
   cd Interactive_Ai_website/Website1/week05
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install streamlit-webrtc av
   ```

3. **Run Application**
   ```bash
   streamlit run FunnyWebsite.py
   ```

4. **Access Application**
   - Open in browser: `http://localhost:8501`

## 📋 Dependencies

### Core Dependencies
```
streamlit>=1.28.0          # Web application framework
streamlit-webrtc>=0.45.0   # Real-time video stream processing
diffusers>=0.21.0          # Stable Diffusion models
torch>=2.0.0               # Deep learning framework
opencv-python>=4.8.0       # Computer vision library
transformers>=4.30.0       # Transformer models
accelerate>=0.20.0         # Model acceleration
av>=10.0.0                 # Audio/video processing
```

### Optional Dependencies (GPU Acceleration)
```
torch[cuda]                # CUDA support
xformers                   # Memory optimization
```

## 🎮 Usage Guide

### AI Image Generator Usage

1. **Select Feature**
   - Click "AI Image Generator" in the sidebar

2. **Input Prompts**
   - Enter description in text box (supports Chinese and English)
   - Example: "A cute puppy playing in a garden"

3. **Adjust Parameters**
   - **Image Size**: Choose generation image resolution
   - **Inference Steps**: Control generation quality (more steps = better quality but slower)
   - **Guidance Scale**: Control adherence to prompts

4. **Generate Image**
   - Click "Generate Image" button
   - Wait for processing completion (usually 10-30 seconds)

### Face Detection Camera Usage

1. **Select Feature**
   - Click "Camera Face Detection" in the sidebar

2. **Start Camera**
   - Click "Start" button
   - Allow browser camera permissions

3. **Adjust Detection Parameters**
   - **Detection Sensitivity**: Adjust face detection sensitivity
   - **Falling Effect Toggle**: Enable/disable face falling animation
   - **Falling Speed**: Control face falling speed

4. **Experience Interactive Effects**
   - Face the camera and observe green detection boxes
   - With falling effects enabled, detected faces will be copied and fall
   - Multiple people can see stacking effects simultaneously

## 🎯 Feature Details

### Gravity Physics System
- **Realistic Gravity**: Falling faces accelerate downward under gravity
- **Bounce Effects**: Natural bouncing when hitting ground or other faces
- **Friction**: Ground friction gradually stops face movement
- **Collision Detection**: Collision and stacking effects between faces

### Vertical Stacking Mechanism
- **Smart Detection**: Automatically detect horizontal overlap between faces
- **Layer Stacking**: Later-falling faces stop above earlier-landed faces
- **Stable Structure**: Stacked faces form stable tower-like structures
- **Overlap Prevention**: Avoid face overlap on the same layer

### Survival Time System
- **10-second Countdown**: Each falling face shows remaining survival time
- **Fade Effects**: Borders gradually become transparent as disappearance approaches
- **Automatic Cleanup**: Automatically removed from screen after timeout

## 🔧 Advanced Configuration

### Performance Optimization Settings

```python
# Adjustable parameters in code
face_detection_settings = {
    'enabled': True,
    'color': (0, 255, 0),        # Detection box color
    'confidence': 0.3,           # Detection confidence
    'falling_effect': True,      # Falling effect toggle
    'falling_speed': 3.0         # Falling speed
}

# Physics engine parameters
gravity = 0.5           # Gravity acceleration
bounce_factor = 0.3     # Bounce coefficient
friction = 0.95         # Friction coefficient
lifetime = 10.0         # Face survival time (seconds)
```

### GPU Acceleration Configuration

If you have an NVIDIA GPU, you can enable CUDA acceleration with:

```bash
# Install CUDA version of PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

## 📂 Project Structure

```
Interactive_Ai_website/
├── README.md                          # Project documentation
├── Website1/week05/
│   ├── FunnyWebsite.py               # Main application
│   ├── streamlit_image_generator.py   # Image generator module
│   ├── requirements.txt               # Python dependencies
│   ├── camera_face_detection.py       # Face detection module
│   ├── simple_camera_test.py         # Camera testing
│   └── generate_puppy.py             # Image generation example
└── Game/                             # Game-related files
```

## 🐛 Troubleshooting

### Common Issues

1. **Camera Won't Start**
   - Ensure browser has granted camera permissions
   - Check if other programs are using the camera
   - Try refreshing the page to re-authorize

2. **Slow Image Generation**
   - Confirm if GPU acceleration is enabled
   - Reduce inference steps to improve speed
   - Lower image resolution

3. **Inaccurate Face Detection**
   - Adjust detection sensitivity parameters
   - Ensure sufficient lighting
   - Keep faces clearly visible

4. **Abnormal Falling Effects**
   - Check if browser supports WebRTC
   - Try reducing falling speed parameters
   - Restart the application

### Performance Optimization Recommendations

- **Hardware Requirements**: GPU recommended for AI image generation
- **Memory Management**: Restart application after extended use to free memory
- **Network Requirements**: Initial run requires downloading model files (~4GB)

## 🔄 Change Log

### v2.0.0 (2025-10-02)
- ✨ Added vertical stacking functionality
- 🔧 Optimized physics engine stability
- 🐛 Fixed face immediate disappearance issue
- 📱 Improved mobile compatibility

### v1.5.0 (2025-10-01)
- ✨ Added gravity physics system
- ✨ Implemented 10-second survival mechanism
- 🎨 Optimized user interface

### v1.0.0 (2025-09-30)
- 🎉 Initial release
- ✨ AI image generation functionality
- ✨ Basic face detection
- 🌐 Bilingual interface support

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## 🤝 Contributing

Issues and Pull Requests are welcome!

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Contact

- Project Maintainer: Majiayin1113
- GitHub: [https://github.com/Majiayin1113](https://github.com/Majiayin1113)
- Project Link: [https://github.com/Majiayin1113/Interactive_Ai_website](https://github.com/Majiayin1113/Interactive_Ai_website)

---

## 🧰 Environment (新增)

本仓库已添加用于快速创建 Python 虚拟环境的脚本：

- `create_venv.ps1`（Windows PowerShell）
- `create_venv.sh`（Unix / macOS bash）
- 顶层 `requirements.txt` 已合并自项目子目录并去重，用于统一安装依赖。

使用示例（Windows PowerShell）：

```powershell
# 在仓库根目录运行（需要 PowerShell）：
.\create_venv.ps1 -VenvName .venv
# 然后在当前会话激活虚拟环境：
& .\.venv\Scripts\Activate.ps1
```

使用示例（Unix / macOS）：

```bash
# 在仓库根目录运行：
./create_venv.sh .venv
# 激活：
source .venv/bin/activate
```

安装完成后即可运行项目中的示例或 Streamlit 应用，例如：

```bash
streamlit run Website1/week05/FunnyWebsite.py
```


⭐ If this project helps you, please give us a star!
