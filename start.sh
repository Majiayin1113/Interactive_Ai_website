#!/bin/bash
# 快速启动脚本 - Interactive AI Website
# Quick Start Script - Interactive AI Website

echo "🚀 启动 Interactive AI Website..."

# 检查是否在正确目录
if [ ! -f "Website1/week05/streamlit_image_generator.py" ]; then
    echo "❌ 请在项目根目录运行此脚本"
    exit 1
fi

# 激活虚拟环境（如果存在）
if [ -d "ai_website_env" ]; then
    echo "📦 激活虚拟环境..."
    source ai_website_env/bin/activate
fi

# 切换到应用目录
cd Website1/week05

# 启动应用
echo "🎨 启动 Streamlit 应用..."
echo "访问地址: http://localhost:8501"
echo "按 Ctrl+C 停止应用"
echo "=================================="

streamlit run streamlit_image_generator.py