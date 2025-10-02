@echo off
REM 快速启动脚本 - Interactive AI Website (Windows)
REM Quick Start Script - Interactive AI Website (Windows)

echo 🚀 启动 Interactive AI Website...

REM 检查是否在正确目录
if not exist "Website1\week05\streamlit_image_generator.py" (
    echo ❌ 请在项目根目录运行此脚本
    pause
    exit /b 1
)

REM 激活虚拟环境（如果存在）
if exist "ai_website_env" (
    echo 📦 激活虚拟环境...
    call ai_website_env\Scripts\activate.bat
)

REM 切换到应用目录
cd Website1\week05

REM 启动应用
echo 🎨 启动 Streamlit 应用...
echo 访问地址: http://localhost:8501
echo 按 Ctrl+C 停止应用
echo ==================================

streamlit run streamlit_image_generator.py