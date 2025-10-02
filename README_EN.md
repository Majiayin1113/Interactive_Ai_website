# 🎨 Interactive AI Website

An interactive web application that integrates **AI Image Generation** and **Real-time Face Detection** capabilities.

## 🌟 Key Features

### 📸 **AI Image Generator**
- Generate high-quality images using Stable Diffusion v1.5
- Support for both Chinese and English prompts
- Adjustable image dimensions and generation parameters
- One-click download of generated images

### 🎭 **Smart Camera Face Detection**
- Real-time face detection and tracking
- Innovative **Gravity Falling Effect**: Detected faces are copied and fall from the top
- **Physics Engine**: Realistic gravity, bouncing, and friction simulation
- **Vertical Stacking**: Falling faces stack like building blocks
- **10-Second Lifetime**: Falling faces automatically disappear after 10 seconds
- **Multi-Face Support**: Simultaneous detection and processing of multiple faces

### 🌐 **Bilingual Interface**
- Complete Chinese/English interface switching
- All features support bilingual operation

## 🚀 Quick Start

### System Requirements

- Python 3.8+
- Camera device
- CUDA-compatible GPU (recommended for AI image generation acceleration)

### Installation Steps

1. **Clone the Project**
   ```bash
   git clone https://github.com/Majiayin1113/Interactive_Ai_website.git
   cd Interactive_Ai_website/Website1/week05
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install streamlit-webrtc av
   ```

3. **Run the Application**
   ```bash
   streamlit run streamlit_image_generator.py
   ```

4. **Access the Application**
   - Open in browser: `http://localhost:8501`

## 📋 Dependencies

### Core Dependencies
```
streamlit>=1.28.0          # Web application framework
streamlit-webrtc>=0.45.0   # Real-time video streaming
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

## 🎮 User Guide

### AI Image Generator Usage

1. **Select Feature**
   - Click "AI Image Generator" in the sidebar

2. **Enter Prompt**
   - Type description in the text box (supports Chinese/English)
   - Example: "A cute puppy playing in a garden"

3. **Adjust Parameters**
   - **Image Size**: Choose generated image resolution
   - **Inference Steps**: Control generation quality (more steps = better quality but slower)
   - **Guidance Scale**: Control adherence to the prompt

4. **Generate Image**
   - Click "Generate Image" button
   - Wait for processing (usually 10-30 seconds)

### Face Detection Camera Usage

1. **Select Feature**
   - Click "Camera Face Detection" in the sidebar

2. **Start Camera**
   - Click "Start" button
   - Allow camera access in browser

3. **Adjust Detection Parameters**
   - **Detection Sensitivity**: Adjust face detection sensitivity
   - **Falling Effect Toggle**: Enable/disable face falling animation
   - **Falling Speed**: Control the speed of face falling

4. **Experience Interactive Effects**
   - Face the camera and observe green detection boxes
   - With falling effect enabled, detected faces will be copied and fall
   - Multiple users can create stacking effects

## 🎯 Feature Highlights

### Gravity Physics System
- **Realistic Gravity**: Falling faces accelerate under gravity
- **Bouncing Effect**: Natural bouncing when hitting ground or other faces
- **Friction**: Ground friction gradually stops face movement
- **Collision Detection**: Collision and stacking effects between faces

### Vertical Stacking Mechanism
- **Smart Detection**: Automatic detection of horizontal overlap between faces
- **Layered Stacking**: Later-falling faces stop on top of earlier-landed faces
- **Stable Structure**: Stacked faces form stable tower-like structures
- **Anti-Overlap**: Prevents faces from overlapping on the same layer

### Lifetime System
- **10-Second Countdown**: Each falling face displays remaining survival time
- **Fade Effect**: Border gradually becomes transparent as expiration approaches
- **Auto Cleanup**: Automatically removes faces after timeout

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
lifetime = 10.0         # Face lifetime (seconds)
```

### GPU Acceleration Configuration

If you have an NVIDIA GPU, enable CUDA acceleration with:

```bash
# Install CUDA version of PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

## 📂 Project Structure

```
Interactive_Ai_website/
├── README.md                          # Project documentation
├── README_EN.md                       # English documentation
├── Website1/week05/
│   ├── streamlit_image_generator.py   # Main application
│   ├── requirements.txt               # Python dependencies
│   ├── camera_face_detection.py       # Face detection module
│   ├── simple_camera_test.py         # Camera testing
│   └── generate_puppy.py             # Image generation example
└── Game/                             # Game-related files
```

## 🐛 Troubleshooting

### Common Issues

1. **Camera Won't Start**
   - Ensure browser has camera permission
   - Check if other programs are using the camera
   - Try refreshing the page to re-authorize

2. **Slow Image Generation**
   - Confirm GPU acceleration is enabled
   - Reduce inference steps for faster generation
   - Lower image resolution

3. **Inaccurate Face Detection**
   - Adjust detection sensitivity parameters
   - Ensure adequate lighting
   - Keep face clearly visible

4. **Falling Effect Anomalies**
   - Check if browser supports WebRTC
   - Try reducing falling speed parameters
   - Restart the application

### Performance Optimization Tips

- **Hardware Requirements**: GPU recommended for AI image generation
- **Memory Management**: Restart application after extended use to free memory
- **Network Requirements**: Initial run requires downloading model files (~4GB)

## 🔄 Changelog

### v2.0.0 (2025-10-02)
- ✨ Added vertical stacking functionality
- 🔧 Optimized physics engine stability
- 🐛 Fixed immediate face disappearing issue
- 📱 Improved mobile compatibility

### v1.5.0 (2025-10-01)
- ✨ Added gravity physics system
- ✨ Implemented 10-second lifetime mechanism
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
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Contact

- Project Maintainer: Majiayin1113
- GitHub: [https://github.com/Majiayin1113](https://github.com/Majiayin1113)
- Project Link: [https://github.com/Majiayin1113/Interactive_Ai_website](https://github.com/Majiayin1113/Interactive_Ai_website)

---

⭐ If this project helps you, please give us a star!