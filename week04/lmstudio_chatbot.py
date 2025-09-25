import streamlit as st
import streamlit.components.v1
from openai import OpenAI
import datetime

# 侧边栏配置
with st.sidebar:
    st.header("🔧 设置")
    
    # 服务器配置
    st.subheader("🌐 服务器配置")
    base_url = st.text_input("LMStudio URL", value="http://localhost:1234/v1")
    api_key = st.text_input("API Key", value="lm-studio", type="password")
    
    # 模型配置
    st.subheader("🤖 模型配置")
    model_name = st.text_input("模型名称", 
                              value="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF")
    
    # 高级设置
    st.subheader("⚙️ 高级设置")
    temperature = st.slider("创造性 (Temperature)", 0.0, 2.0, 0.7, 0.1)
    max_tokens = st.slider("最大回复长度", 50, 4000, 2000, 50)
    
    # 聊天历史管理
    st.subheader("💾 聊天管理")
    if st.button("🗑️ 清除聊天记录"):
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
        st.rerun()
    
    # 显示聊天统计
    if "messages" in st.session_state:
        total_messages = len(st.session_state["messages"])
        user_messages = sum(1 for msg in st.session_state["messages"] if msg["role"] == "user")
        st.metric("总消息数", total_messages)
        st.metric("用户消息数", user_messages)
    
    # 系统状态
    st.subheader("📊 系统状态")
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.text(f"当前时间: {current_time}")
    
    # 预设提示词
    st.subheader("💡 快速提示")
    quick_prompts = [
        "解释一个编程概念",
        "帮我写代码",
        "翻译这段文字",
        "总结一段内容",
        "创意写作"
    ]
    
    selected_prompt = st.selectbox("选择快速提示", [""] + quick_prompts)
    if selected_prompt and st.button("使用此提示"):
        st.session_state["quick_prompt"] = selected_prompt

# Point to the local server
client = OpenAI(base_url=base_url, api_key=api_key)
st.title("💬 Chatbot")
st.caption("🚀 A Streamlit chatbot powered by LMStudio")

# 小人跳跃游戏 - 居中显示
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.subheader("🎮 小人跳跃游戏")
    st.caption("按空格键让小人跳跃！避开仙人掌获得高分！")
    
    # 游戏HTML/CSS/JavaScript代码 - 放大版本
    game_html = """
    <div id="gameContainer" style="width: 100%; max-width: 500px; height: 300px; border: 3px solid #333; position: relative; background: linear-gradient(to bottom, #87CEEB 0%, #98FB98 70%); overflow: hidden; margin: 20px auto; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
        <!-- 云朵 -->
        <div style="position: absolute; top: 30px; left: 80px; width: 50px; height: 25px; background: white; border-radius: 50px; opacity: 0.8;"></div>
        <div style="position: absolute; top: 50px; left: 250px; width: 40px; height: 20px; background: white; border-radius: 50px; opacity: 0.6;"></div>
        <div style="position: absolute; top: 20px; left: 350px; width: 35px; height: 18px; background: white; border-radius: 50px; opacity: 0.7;"></div>
        
        <!-- 太阳 -->
        <div style="position: absolute; top: 15px; right: 30px; width: 35px; height: 35px; background: #FFD700; border-radius: 50%; box-shadow: 0 0 20px #FFD700;"></div>
        
        <!-- 地面 -->
        <div id="ground" style="position: absolute; bottom: 0; width: 100%; height: 50px; background: #8B4513; border-top: 5px solid #228B22;"></div>
        
        <!-- 小草装饰 -->
        <div style="position: absolute; bottom: 50px; left: 30px; width: 3px; height: 10px; background: #32CD32; border-radius: 2px;"></div>
        <div style="position: absolute; bottom: 50px; left: 35px; width: 3px; height: 8px; background: #32CD32; border-radius: 2px;"></div>
        <div style="position: absolute; bottom: 50px; left: 150px; width: 3px; height: 12px; background: #32CD32; border-radius: 2px;"></div>
        <div style="position: absolute; bottom: 50px; left: 300px; width: 3px; height: 9px; background: #32CD32; border-radius: 2px;"></div>
        
        <!-- 小人 -->
        <div id="player" style="position: absolute; bottom: 50px; left: 80px; width: 30px; height: 45px; background: #FF6B6B; border-radius: 15px 15px 8px 8px; transition: bottom 0.3s ease;">
            <!-- 头 -->
            <div style="position: absolute; top: -12px; left: 3px; width: 24px; height: 24px; background: #FFB6C1; border-radius: 50%;"></div>
            <!-- 眼睛 -->
            <div style="position: absolute; top: -7px; left: 8px; width: 4px; height: 4px; background: black; border-radius: 50%;"></div>
            <div style="position: absolute; top: -7px; left: 18px; width: 4px; height: 4px; background: black; border-radius: 50%;"></div>
            <!-- 嘴巴 -->
            <div style="position: absolute; top: -2px; left: 12px; width: 6px; height: 3px; background: #FF69B4; border-radius: 0 0 6px 6px;"></div>
            <!-- 胳膊 -->
            <div style="position: absolute; top: 10px; left: -5px; width: 8px; height: 15px; background: #FFB6C1; border-radius: 4px;"></div>
            <div style="position: absolute; top: 10px; right: -5px; width: 8px; height: 15px; background: #FFB6C1; border-radius: 4px;"></div>
            <!-- 腿 -->
            <div style="position: absolute; bottom: -8px; left: 6px; width: 6px; height: 12px; background: #FF6B6B; border-radius: 3px;"></div>
            <div style="position: absolute; bottom: -8px; right: 6px; width: 6px; height: 12px; background: #FF6B6B; border-radius: 3px;"></div>
        </div>
        
        <!-- 障碍物 -->
        <div id="obstacle" style="position: absolute; bottom: 50px; right: -30px; width: 25px; height: 40px; background: #654321; border-radius: 5px; animation: moveLeft 4s linear infinite;">
            <!-- 仙人掌刺 -->
            <div style="position: absolute; top: 8px; left: -5px; width: 10px; height: 3px; background: #228B22; border-radius: 3px;"></div>
            <div style="position: absolute; top: 15px; right: -5px; width: 10px; height: 3px; background: #228B22; border-radius: 3px;"></div>
            <div style="position: absolute; top: 22px; left: -3px; width: 8px; height: 3px; background: #228B22; border-radius: 3px;"></div>
            <div style="position: absolute; top: 30px; right: -4px; width: 9px; height: 3px; background: #228B22; border-radius: 3px;"></div>
        </div>
        
        <!-- 分数显示 -->
        <div id="score" style="position: absolute; top: 15px; left: 15px; color: #333; font-weight: bold; font-size: 18px; background: rgba(255,255,255,0.8); padding: 5px 10px; border-radius: 10px;">得分: 0</div>
        <div id="highScore" style="position: absolute; top: 15px; right: 15px; color: #333; font-weight: bold; font-size: 14px; background: rgba(255,255,255,0.8); padding: 3px 8px; border-radius: 8px;">最高: 0</div>
        <div id="gameOver" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: red; font-weight: bold; font-size: 24px; display: none; background: rgba(255,255,255,0.9); padding: 20px; border-radius: 15px; text-align: center;">🎮 游戏结束! 🎮</div>
    </div>
    
    <style>
        @keyframes moveLeft {
            from { right: -30px; }
            to { right: 530px; }
        }
        
        @keyframes jump {
            0% { bottom: 50px; }
            50% { bottom: 120px; }
            100% { bottom: 50px; }
        }
        
        .jumping {
            animation: jump 0.8s ease !important;
        }
        
        #gameContainer:hover {
            box-shadow: 0 6px 20px rgba(0,0,0,0.4);
            transition: box-shadow 0.3s ease;
        }
    </style>
    
    <script>
        (function() {
            let isJumping = false;
            let score = 0;
            let highScore = localStorage.getItem('jumpGameHighScore') || 0;
            let gameRunning = true;
            const player = document.getElementById('player');
            const obstacle = document.getElementById('obstacle');
            const scoreElement = document.getElementById('score');
            const highScoreElement = document.getElementById('highScore');
            const gameOverElement = document.getElementById('gameOver');
            
            // 初始化最高分显示
            highScoreElement.textContent = '最高: ' + highScore;
            
            // 跳跃函数
            function jump() {
                if (!isJumping && gameRunning) {
                    isJumping = true;
                    player.classList.add('jumping');
                    
                    setTimeout(() => {
                        player.classList.remove('jumping');
                        isJumping = false;
                    }, 800);
                }
            }
            
            // 键盘事件监听
            document.addEventListener('keydown', function(event) {
                if (event.code === 'Space') {
                    event.preventDefault();
                    jump();
                }
            });
            
            // 点击游戏区域也可以跳跃
            document.getElementById('gameContainer').addEventListener('click', jump);
            
            // 碰撞检测
            function checkCollision() {
                if (!gameRunning) return;
                
                const playerRect = player.getBoundingClientRect();
                const obstacleRect = obstacle.getBoundingClientRect();
                
                if (playerRect.right > obstacleRect.left && 
                    playerRect.left < obstacleRect.right && 
                    playerRect.bottom > obstacleRect.top) {
                    
                    gameRunning = false;
                    gameOverElement.style.display = 'block';
                    obstacle.style.animationPlayState = 'paused';
                    
                    // 更新最高分
                    if (score > highScore) {
                        highScore = score;
                        localStorage.setItem('jumpGameHighScore', highScore);
                        highScoreElement.textContent = '最高: ' + highScore;
                    }
                    
                    setTimeout(() => {
                        if (confirm('🎮 游戏结束! 🎮\\n本次得分: ' + score + '\\n最高得分: ' + highScore + '\\n\\n点击确定重新开始')) {
                            restartGame();
                        }
                    }, 100);
                }
            }
            
            // 重启游戏
            function restartGame() {
                gameRunning = true;
                score = 0;
                scoreElement.textContent = '得分: ' + score;
                gameOverElement.style.display = 'none';
                obstacle.style.animation = 'none';
                setTimeout(() => {
                    obstacle.style.animation = 'moveLeft 4s linear infinite';
                }, 10);
            }
            
            // 计分
            function updateScore() {
                if (gameRunning) {
                    score += 1;
                    scoreElement.textContent = '得分: ' + score;
                }
            }
            
            // 游戏循环
            setInterval(checkCollision, 50);
            setInterval(updateScore, 200);
            
        })();
    </script>
    """
    
    # 显示游戏
    st.components.v1.html(game_html, height=350)
    
    st.markdown("""
    <div style='text-align: center; margin-top: 10px;'>
        <p style='color: #666; font-size: 14px;'>💡 操作提示：点击游戏区域或按空格键让小人跳跃！</p>
        <p style='color: #666; font-size: 12px;'>🎯 目标：避开移动的仙人掌，挑战最高分！</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# 初始化会话状态
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# 处理快速提示
if "quick_prompt" in st.session_state and st.session_state["quick_prompt"]:
    prompt = st.session_state["quick_prompt"]
    st.session_state["quick_prompt"] = ""  # 清除快速提示
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 显示用户消息
    st.chat_message("user").write(prompt)
    
    # 生成AI回复
    with st.chat_message("assistant"):
        with st.spinner("AI正在思考..."):
            try:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=st.session_state.messages,
                    stream=True,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )

                msg = ""
                def stream_response():
                    global msg
                    for chunk in response:
                        part = chunk.choices[0].delta.content
                        if part:
                            msg += part
                            yield part

                st.write_stream(stream_response)
                st.session_state.messages.append({"role": "assistant", "content": msg})
            except Exception as e:
                st.error(f"连接LMStudio时出错: {e}")
                st.info("请确保LMStudio正在运行并在指定端口提供服务")
    st.rerun()

# 显示聊天历史
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 聊天输入
if prompt := st.chat_input("在这里输入您的消息..."):
    # 添加用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    # 生成AI回复
    with st.chat_message("assistant"):
        with st.spinner("AI正在思考..."):
            try:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=st.session_state.messages,
                    stream=True,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )

                msg = ""
                def stream_response():
                    global msg
                    for chunk in response:
                        part = chunk.choices[0].delta.content
                        if part:
                            msg += part
                            yield part

                st.write_stream(stream_response)
                st.session_state.messages.append({"role": "assistant", "content": msg})
                
            except Exception as e:
                st.error(f"连接LMStudio时出错: {e}")
                st.info("请确保LMStudio正在运行并在指定端口提供服务")
