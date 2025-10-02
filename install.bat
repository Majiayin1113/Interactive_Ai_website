@echo off
REM 安装脚本 - Interactive AI Website (Windows)
REM Installation Script - Interactive AI Website (Windows)

echo 🎨 Interactive AI Website - 安装脚本
echo ======================================

REM 检查 Python 版本
echo 1. 检查 Python 版本...
python --version
if errorlevel 1 (
    echo ❌ Python 未安装或版本过低，请安装 Python 3.8+
    pause
    exit /b 1
)

REM 创建虚拟环境（可选）
set /p create_venv="是否创建虚拟环境? (y/n): "
if /i "%create_venv%"=="y" (
    echo 2. 创建虚拟环境...
    python -m venv ai_website_env
    call ai_website_env\Scripts\activate.bat
    echo ✅ 虚拟环境已激活
)

REM 安装依赖
echo 3. 安装依赖包...
python -m pip install --upgrade pip
cd Website1\week05
pip install -r requirements.txt

REM 检查 GPU 支持
echo 4. 检查 GPU 支持...
set /p enable_cuda="是否有 NVIDIA GPU 并希望启用 CUDA 加速? (y/n): "
if /i "%enable_cuda%"=="y" (
    echo 安装 CUDA 版本的 PyTorch...
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
)

echo 5. 安装完成!
echo ======================================
echo 🚀 运行命令:
echo    streamlit run streamlit_image_generator.py
echo.
echo 📱 访问地址:
echo    http://localhost:8501
echo.
echo 📚 更多帮助请查看 README.md
echo ======================================
pause