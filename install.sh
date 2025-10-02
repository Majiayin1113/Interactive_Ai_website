#!/bin/bash
# 安装脚本 - Interactive AI Website
# Installation Script - Interactive AI Website

echo "🎨 Interactive AI Website - 安装脚本"
echo "======================================"

# 检查 Python 版本
echo "1. 检查 Python 版本..."
python --version
if [ $? -ne 0 ]; then
    echo "❌ Python 未安装或版本过低，请安装 Python 3.8+"
    exit 1
fi

# 创建虚拟环境（可选）
read -p "是否创建虚拟环境? (y/n): " create_venv
if [ "$create_venv" = "y" ] || [ "$create_venv" = "Y" ]; then
    echo "2. 创建虚拟环境..."
    python -m venv ai_website_env
    source ai_website_env/bin/activate
    echo "✅ 虚拟环境已激活"
fi

# 安装依赖
echo "3. 安装依赖包..."
pip install --upgrade pip
cd Website1/week05
pip install -r requirements.txt

# 检查 GPU 支持
echo "4. 检查 GPU 支持..."
read -p "是否有 NVIDIA GPU 并希望启用 CUDA 加速? (y/n): " enable_cuda
if [ "$enable_cuda" = "y" ] || [ "$enable_cuda" = "Y" ]; then
    echo "安装 CUDA 版本的 PyTorch..."
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
fi

echo "5. 安装完成!"
echo "======================================"
echo "🚀 运行命令:"
echo "   streamlit run streamlit_image_generator.py"
echo ""
echo "📱 访问地址:"
echo "   http://localhost:8501"
echo ""
echo "📚 更多帮助请查看 README.md"
echo "======================================"