# 🎨 Interactive AI Website

一个集成了 **AI 图像生成** 和 **实时人脸检测** 功能的交互式 Web 应用程序。

## 🌟 主要功能

### 📸 **AI 图像生成器**
- 使用 Stable Diffusion v1.5 模型生成高质量图像
- 支持中英文提示词
- 可调节图像尺寸和生成参数
- 一键下载生成的图像

### 🎭 **智能摄像头人脸检测**
- 实时人脸检测和追踪
- 创新的**重力掉落效果**：检测到的人脸会复制并从顶部掉落
- **物理引擎**：真实的重力、弹跳和摩擦力模拟
- **垂直堆叠**：掉落的人脸可以像积木一样堆叠
- **10秒生存机制**：掉落的人脸会在10秒后自动消失
- **多人脸支持**：可同时检测和处理多个人脸

### 🌐 **双语界面**
- 完整的中英文界面切换
- 所有功能都支持双语操作

## 🚀 快速开始

### 环境要求

- Python 3.8+
- 摄像头设备
- CUDA 兼容的 GPU（推荐，用于加速 AI 图像生成）

### 安装步骤

1. **克隆项目**
   ```bash
   git clone https://github.com/Majiayin1113/Interactive_Ai_website.git
   cd Interactive_Ai_website/Website1/week05
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   pip install streamlit-webrtc av
   ```

3. **运行应用**
   ```bash
   streamlit run streamlit_image_generator.py
   ```

4. **访问应用**
   - 在浏览器中打开: `http://localhost:8501`

## 📋 依赖包说明

### 核心依赖
```
streamlit>=1.28.0          # Web 应用框架
streamlit-webrtc>=0.45.0   # 实时视频流处理
diffusers>=0.21.0          # Stable Diffusion 模型
torch>=2.0.0               # 深度学习框架
opencv-python>=4.8.0       # 计算机视觉库
transformers>=4.30.0       # Transformer 模型
accelerate>=0.20.0         # 模型加速
av>=10.0.0                 # 音视频处理
```

### 可选依赖（GPU加速）
```
torch[cuda]                # CUDA 支持
xformers                   # 内存优化
```

## 🎮 使用指南

### AI 图像生成器使用

1. **选择功能**
   - 在侧边栏点击"AI 图像生成器"

2. **输入提示词**
   - 在文本框中输入描述（支持中英文）
   - 例如："一只可爱的小狗在花园里玩耍"

3. **调整参数**
   - **图像尺寸**: 选择生成图像的分辨率
   - **推理步数**: 控制生成质量（步数越多质量越好但速度越慢）
   - **引导比例**: 控制对提示词的遵循程度

4. **生成图像**
   - 点击"生成图像"按钮
   - 等待处理完成（通常需要10-30秒）

### 人脸检测摄像头使用

1. **选择功能**
   - 在侧边栏点击"摄像头人脸检测"

2. **启动摄像头**
   - 点击"开始"按钮
   - 允许浏览器访问摄像头权限

3. **调整检测参数**
   - **检测敏感度**: 调整人脸检测的敏感程度
   - **掉落效果开关**: 启用/禁用人脸掉落动画
   - **掉落速度**: 控制人脸掉落的速度

4. **体验互动效果**
   - 面向摄像头，观察绿色检测框
   - 启用掉落效果后，检测到的人脸会复制并掉落
   - 多人同时使用可看到堆叠效果

## 🎯 特色功能详解

### 重力物理系统
- **真实重力**: 掉落的人脸受重力影响加速下降
- **弹跳效果**: 撞击地面或其他人脸时产生自然弹跳
- **摩擦力**: 地面摩擦使人脸逐渐停止移动
- **碰撞检测**: 人脸之间的碰撞和堆叠效果

### 垂直堆叠机制
- **智能检测**: 自动检测人脸间的水平重叠
- **层级堆叠**: 后掉落的人脸会停在先落地人脸的上方
- **稳定结构**: 堆叠后的人脸形成稳定的塔状结构
- **防重叠**: 避免人脸在同一层重叠

### 生存时间系统
- **10秒倒计时**: 每个掉落的人脸显示剩余存活时间
- **渐变效果**: 接近消失时边框逐渐变透明
- **自动清理**: 超时后自动从画面中移除

## 🔧 高级配置

### 性能优化设置

```python
# 在代码中可调整的参数
face_detection_settings = {
    'enabled': True,
    'color': (0, 255, 0),        # 检测框颜色
    'confidence': 0.3,           # 检测置信度
    'falling_effect': True,      # 掉落效果开关
    'falling_speed': 3.0         # 掉落速度
}

# 物理引擎参数
gravity = 0.5           # 重力加速度
bounce_factor = 0.3     # 弹跳系数
friction = 0.95         # 摩擦系数
lifetime = 10.0         # 人脸生存时间（秒）
```

### GPU 加速配置

如果您有 NVIDIA GPU，可以通过以下方式启用 CUDA 加速：

```bash
# 安装 CUDA 版本的 PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

## 📂 项目结构

```
Interactive_Ai_website/
├── README.md                          # 项目说明文档
├── Website1/week05/
│   ├── streamlit_image_generator.py   # 主应用程序
│   ├── requirements.txt               # Python 依赖
│   ├── camera_face_detection.py       # 人脸检测模块
│   ├── simple_camera_test.py         # 摄像头测试
│   └── generate_puppy.py             # 图像生成示例
└── Game/                             # 游戏相关文件
```

## 🐛 故障排除

### 常见问题

1. **摄像头无法启动**
   - 确保浏览器已授予摄像头权限
   - 检查是否有其他程序占用摄像头
   - 尝试刷新页面重新授权

2. **图像生成速度慢**
   - 确认是否启用了 GPU 加速
   - 减少推理步数以提高速度
   - 降低图像分辨率

3. **人脸检测不准确**
   - 调整检测敏感度参数
   - 确保光线充足
   - 保持人脸清晰可见

4. **掉落效果异常**
   - 检查浏览器是否支持 WebRTC
   - 尝试降低掉落速度参数
   - 重启应用程序

### 性能优化建议

- **硬件要求**: 推荐使用 GPU 进行 AI 图像生成
- **内存管理**: 长时间使用后可重启应用释放内存
- **网络要求**: 初次运行需要下载模型文件（约4GB）

## 🔄 更新日志

### v2.0.0 (2025-10-02)
- ✨ 新增垂直堆叠功能
- 🔧 优化物理引擎稳定性
- 🐛 修复人脸立即消失的问题
- 📱 改进移动端兼容性

### v1.5.0 (2025-10-01)
- ✨ 添加重力物理系统
- ✨ 实现10秒生存机制
- 🎨 优化用户界面

### v1.0.0 (2025-09-30)
- 🎉 初始发布
- ✨ AI 图像生成功能
- ✨ 基础人脸检测
- 🌐 双语界面支持

## 📝 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🤝 贡献指南

欢迎提交 Issues 和 Pull Requests！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📧 联系方式

- 项目维护者: Majiayin1113
- GitHub: [https://github.com/Majiayin1113](https://github.com/Majiayin1113)
- 项目链接: [https://github.com/Majiayin1113/Interactive_Ai_website](https://github.com/Majiayin1113/Interactive_Ai_website)

---

⭐ 如果这个项目对您有帮助，请给我们一个星标！
