# 🎨 FunnyWebsite - Multi-functional AI Interactive Website
Simply open FunnyWebsite to see all features.

## 📖 Project Overview

**FunnyWebsite** is an AI interactive website integrating three core functions: AI image generation, real-time face recognition, and voice-controlled gaming. Built with Streamlit framework, it supports bilingual Chinese-English interface.

---

## ✨ Core Features

### 1. 🎨 AI Image Generator
Text-to-image generation system based on Stable Diffusion v1.5
- 📝 **Text-to-Image Generation**: Input text descriptions, AI automatically generates high-quality images
- 🎯 **Preset Templates**: 6 built-in common prompts (cute puppy, beautiful landscape, futuristic city, etc.)
- ⚙️ **Parameter Adjustment**: Customize image dimensions (512x512/768x512/512x768) and inference steps
- 💾 **One-Click Download**: Generated images can be directly downloaded and saved
- 🚀 **GPU Acceleration**: Support CUDA acceleration for faster generation
- 📚 **History Records**: Save the last 10 generated images

### 2. 📹 Smart Face Recognition
Real-time video processing system based on OpenCV + WebRTC
- 👤 **Real-time Detection**: Automatically recognize multiple faces in the frame
- 🎭 **Falling Effects**: Detected faces are copied and fall from the top
- 🏗️ **Physics Simulation**: Realistic gravity, bounce, and friction effects
- 📚 **Vertical Stacking**: Falling faces can stack layer by layer like building blocks
- ⏱️ **10-Second Disappearance**: Each falling face displays countdown and auto-clears after 10 seconds
- 🎨 **Custom Settings**: Adjustable detection box color, sensitivity, and falling speed
<img width="2559" height="1343" alt="image" src="https://github.com/user-attachments/assets/3e56dfd2-6d5d-462a-b492-21e7bc4509e8" />

### 3. 🐟 FishJump Voice-Controlled Game
Jump game controlled by microphone sound
- 🎤 **Voice Control**: Control fish jumping through microphone sound
- 📢 **Volume Response**: Louder sound means higher jump
- 🦈 **Avoid Obstacles**: Dodge red piranha obstacles
- 🏆 **Record Saving**: Automatically save high score records
- 🎮 **Independent Window**: Game runs in separate Pygame window
<img width="1202" height="646" alt="image" src="https://github.com/user-attachments/assets/64d5bd2b-4a14-40ad-a947-a9b6cccee50b" />

---

## 🚀 Quick Start

### Requirements
- Python 3.8+
- Camera device (for face recognition)
- Microphone device (for FishJump game)
- CUDA-compatible GPU (optional, for accelerating image generation)

### Installation Steps

1. **Clone the Project**
   ```bash
   git clone https://github.com/Majiayin1113/Interactive_Ai_website.git
   cd Interactive_Ai_website
   ```

2. **Create Virtual Environment (Recommended)**
   
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

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   streamlit run Website1/week05/FunnyWebsite.py
   ```

5. **Access the Application**
   - Browser will open automatically, or manually visit: `http://localhost:8501`

---

## 🎮 User Guide

### AI Image Generator
1. Click "🎨 Image Generation" in the sidebar
2. Enter description in text box or select preset template
3. Adjust image dimensions and inference steps
4. Click "Generate Image" button
5. Wait for generation to complete (10-30 seconds)
6. Download or regenerate

### Face Recognition Camera
1. Click "📹 Face Recognition" in the sidebar
2. Click "START" button to launch camera
3. Allow browser camera permissions
4. Adjust detection sensitivity and falling effects
5. Face the camera to observe real-time detection and falling effects
6. Multiple people can observe stacking effects simultaneously

### FishJump Game
1. Click "🐟 FishJump" in the sidebar
2. View game instructions and controls
3. Click "Start Game" button
4. Game launches in new window
5. Make sounds into microphone to control fish jumping
6. Avoid obstacles and achieve high scores

---

## 📦 Core Dependencies

```
streamlit>=1.28.0          # Web application framework
streamlit-webrtc>=0.45.0   # Real-time video stream processing
diffusers>=0.21.0          # Stable Diffusion models
torch>=2.0.0               # Deep learning framework
opencv-python>=4.8.0       # Computer vision library
transformers>=4.30.0       # Transformer models
pygame>=2.5.0              # Game development library
pyaudio>=0.2.13            # Audio processing
```

---

## 🛠️ Technical Architecture

```
FunnyWebsite
├── Streamlit Frontend Framework
│   ├── Multi-page Navigation System
│   ├── Chinese-English Bilingual Switching
│   └── Responsive Layout Design
│
├── AI Image Generation Module
│   ├── Stable Diffusion v1.5
│   ├── Diffusers Pipeline
│   └── PyTorch + CUDA
│
├── Face Recognition Module
│   ├── OpenCV Face Detection
│   ├── WebRTC Video Stream
│   ├── Custom Physics Engine
│   └── Collision Stacking System
│
└── Voice-Controlled Game Module
    ├── PyAudio Audio Capture
    ├── Pygame Game Engine
    └── Real-time Volume Analysis
```

---

## 🐛 Common Issues

### Camera Won't Start
- Check browser camera permissions
- Confirm no other programs are using the camera
- Refresh page to re-authorize

### Slow Image Generation
- Confirm if GPU acceleration is enabled
- Reduce inference steps to improve speed
- Lower image resolution

### Game Won't Start
- Check if PyAudio and Pygame are installed
- Confirm microphone permissions are granted
- View terminal error messages

---

## 📂 Project Structure

```
Interactive_Ai_website/
├── README.md                    # Project documentation
├── requirements.txt             # Python dependencies list
├── create_venv.ps1             # Windows virtual environment creation script
├── create_venv.sh              # Linux/Mac virtual environment creation script
├── voice_parkour.py            # FishJump game main program
├── highscore.txt               # Game high score record
│
├── Website1/week05/
│   ├── FunnyWebsite.py         # Main application
│   ├── requirements.txt        # Module dependencies
│   └── ...                     # Other auxiliary files
│
├── Game/                       # Game-related files
└── Sound/                      # Audio processing files
```

---

## 🌐 Language Support

- 🇨🇳 **Simplified Chinese**: Complete Chinese interface and prompt support
- 🇺🇸 **English**: Complete English interface and prompt support

Switch languages anytime in the sidebar, all features support bilingual operation.

---

## 📝 Development Log

### v2.0.0 (2025-10-16)
- ✨ Added FishJump voice-controlled game module
- ✨ Improved three-module navigation system
- 🎨 Optimized UI interface and icon display
- 🌐 Enhanced bilingual support

### v1.5.0 (2025-10-02)
- ✨ Added face vertical stacking functionality
- 🔧 Optimized physics engine stability
- 📱 Improved mobile compatibility

### v1.0.0 (2025-09-30)
- 🎉 Initial release
- ✨ AI image generation functionality
- ✨ Basic face detection

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

---

## 👥 Contributing

Issues and Pull Requests are welcome!

1. Fork the project
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📧 Contact

- Project Maintainer: Majiayin1113
- GitHub: [https://github.com/Majiayin1113](https://github.com/Majiayin1113)
- Project Link: [https://github.com/Majiayin1113/Interactive_Ai_website](https://github.com/Majiayin1113/Interactive_Ai_website)

---

⭐ If this project helps you, please give us a star!
