import streamlit as st
from diffusers import DiffusionPipeline
import torch
from io import BytesIO
import time
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration, WebRtcMode
import cv2
import numpy as np
import av

# 语言文本字典
LANGUAGES = {
    'zh': {
        'page_title': 'AI智能工具集',
        'app_title': '🎨 AI图像生成器',
        'system_info': '⚙️ 系统信息',
        'pytorch_info': f'🔧 PyTorch: {torch.__version__}',
        'device_gpu': '🖥️ 设备: GPU (CUDA)',
        'device_cpu': '🖥️ 设备: CPU',
        'image_settings': '📝 图像设置',
        'image_description': '图像描述',
        'image_description_help': '详细描述您想要生成的图像',
        'default_prompt': 'a beautiful landscape with mountains',
        'generation_steps': '生成步数',
        'steps_help': '更高的步数通常产生更好的质量，但需要更长时间',
        'image_dimensions': '📐 图像尺寸',
        'select_size': '选择尺寸',
        'size_512x512': '512x512 (标准)',
        'size_768x512': '768x512 (宽屏)',
        'size_512x768': '512x768 (竖屏)',
        'quick_select': '🎯 快速选择',
        'preset_puppy': '🐕 可爱小狗',
        'preset_landscape': '🏔️ 美丽风景',
        'preset_city': '🌃 未来城市',
        'preset_forest': '🌲 梦幻森林',
        'preset_abstract': '🎨 抽象艺术',
        'preset_sakura': '🌸 樱花季节',
        'generate_button': '🎨 生成图像',
        'image_display': '🖼️ 图像展示区域',
        'generating': '🎨 正在生成图像，请稍候...',
        'loading_model': '📥 加载模型...',
        'generating_image': '🎨 生成图像中...',
        'generation_complete': '✅ 生成完成！',
        'generation_success': '🎉 图像生成成功！',
        'generation_failed': '❌ 生成失败: ',
        'latest_image': '📸 最新生成的图像',
        'prompt_label': '提示词: ',
        'prompt_info': '📝 **提示词**: ',
        'steps_info': '🔢 **生成步数**: ',
        'size_info': '📐 **尺寸**: ',
        'time_info': '🕐 **生成时间**: ',
        'download_button': '📥 下载高清图像',
        'regenerate_button': '🔄 重新生成',
        'clear_history': '🗑️ 清除历史',
        'history_title': '📚 历史生成记录',
        'view_details': '查看详情 #',
        'empty_state': '👈 请在左侧边栏中输入提示词并点击生成按钮开始创作！',
        'features_title': '✨ 功能特色',
        'feature_quality': '### 🎨 高质量生成\n- 使用Stable Diffusion v1.5\n- 支持多种图像尺寸\n- 可调节生成步数',
        'feature_gpu': '### 🚀 GPU加速\n- 自动检测CUDA支持\n- 快速生成响应\n- 优化内存使用',
        'feature_ui': '### 📱 友好界面\n- 预设提示词选择\n- 实时进度显示\n- 历史记录管理',
        'language_switch': '🌐 Language',
        'lang_zh': '🇨🇳 中文',
        'lang_en': '🇺🇸 English',
        'navigation': '🧭 导航',
        'page_image_gen': '🎨 图像生成器',
        'page_camera': '📹 摄像头识别',
        'page_fishjump': '🐟 FishJump游戏',
        'nav_image_gen': '图像生成',
        'nav_camera': '人脸识别',
        'nav_fishjump': 'FishJump',
        'fishjump_title': '🐟 FishJump - 声控跳跃游戏',
        'fishjump_desc': '使用麦克风控制小鱼跳跃，躲避障碍物！',
        'fishjump_instruction': '游戏说明',
        'fishjump_instruction_1': '🎤 游戏通过麦克风声音控制',
        'fishjump_instruction_2': '🐟 小鱼会自动向前游动',
        'fishjump_instruction_3': '📢 发出声音让小鱼跳跃',
        'fishjump_instruction_4': '🔊 声音越大，跳得越高',
        'fishjump_instruction_5': '⚠️ 躲避红色的食人鱼障碍物',
        'fishjump_instruction_6': '🏆 尽可能获得更高分数',
        'fishjump_start': '🎮 启动游戏',
        'fishjump_note': '📝 注意：游戏将在新窗口中启动',
        'fishjump_controls': '🎮 控制方式',
        'fishjump_tips': '💡 游戏提示',
        'fishjump_tip_1': '• 保持麦克风在合适的距离',
        'fishjump_tip_2': '• 可以用口哨、拍手等声音控制',
        'fishjump_tip_3': '• 声音需要达到一定音量才能跳跃',
        'fishjump_tip_4': '• 分数会自动保存为最高分',
        'fishjump_requirements': '⚙️ 系统要求',
        'fishjump_req_1': '✓ 需要麦克风权限',
        'fishjump_req_2': '✓ 需要安装 PyAudio',
        'fishjump_req_3': '✓ 需要安装 Pygame'
    },
    'en': {
        'page_title': 'AI Smart Tools',
        'app_title': '🎨 AI Image Generator',
        'system_info': '⚙️ System Info',
        'pytorch_info': f'🔧 PyTorch: {torch.__version__}',
        'device_gpu': '🖥️ Device: GPU (CUDA)',
        'device_cpu': '🖥️ Device: CPU',
        'image_settings': '📝 Image Settings',
        'image_description': 'Image Description',
        'image_description_help': 'Describe the image you want to generate in detail',
        'default_prompt': 'a beautiful landscape with mountains',
        'generation_steps': 'Generation Steps',
        'steps_help': 'Higher steps usually produce better quality but take longer',
        'image_dimensions': '📐 Image Dimensions',
        'select_size': 'Select Size',
        'size_512x512': '512x512 (Standard)',
        'size_768x512': '768x512 (Widescreen)',
        'size_512x768': '512x768 (Portrait)',
        'quick_select': '🎯 Quick Select',
        'preset_puppy': '🐕 Cute Puppy',
        'preset_landscape': '🏔️ Beautiful Landscape',
        'preset_city': '🌃 Futuristic City',
        'preset_forest': '🌲 Magical Forest',
        'preset_abstract': '🎨 Abstract Art',
        'preset_sakura': '🌸 Cherry Blossoms',
        'generate_button': '🎨 Generate Image',
        'image_display': '🖼️ Image Display Area',
        'generating': '🎨 Generating image, please wait...',
        'loading_model': '📥 Loading model...',
        'generating_image': '🎨 Generating image...',
        'generation_complete': '✅ Generation complete!',
        'generation_success': '🎉 Image generated successfully!',
        'generation_failed': '❌ Generation failed: ',
        'latest_image': '📸 Latest Generated Image',
        'prompt_label': 'Prompt: ',
        'prompt_info': '📝 **Prompt**: ',
        'steps_info': '🔢 **Steps**: ',
        'size_info': '📐 **Size**: ',
        'time_info': '🕐 **Generated**: ',
        'download_button': '📥 Download HD Image',
        'regenerate_button': '🔄 Regenerate',
        'clear_history': '🗑️ Clear History',
        'history_title': '📚 Generation History',
        'view_details': 'View Details #',
        'empty_state': '👈 Please enter a prompt in the left sidebar and click generate to start creating!',
        'features_title': '✨ Features',
        'feature_quality': '### 🎨 High Quality Generation\n- Uses Stable Diffusion v1.5\n- Multiple image sizes supported\n- Adjustable generation steps',
        'feature_gpu': '### 🚀 GPU Acceleration\n- Auto-detect CUDA support\n- Fast generation response\n- Optimized memory usage',
        'feature_ui': '### 📱 User-Friendly Interface\n- Preset prompt selection\n- Real-time progress display\n- History management',
        'language_switch': '🌐 语言',
        'lang_zh': '🇨🇳 中文',
        'lang_en': '🇺🇸 English',
        'navigation': '🧭 Navigation',
        'page_image_gen': '🎨 Image Generator',
        'page_camera': '📹 Camera Detection',
        'page_fishjump': '🐟 FishJump Game',
        'nav_image_gen': 'Image Generation',
        'nav_camera': 'Face Recognition',
        'nav_fishjump': 'FishJump',
        'fishjump_title': '🐟 FishJump - Voice Controlled Jump Game',
        'fishjump_desc': 'Control the fish to jump with your microphone and avoid obstacles!',
        'fishjump_instruction': 'Game Instructions',
        'fishjump_instruction_1': '🎤 Game is controlled by microphone sounds',
        'fishjump_instruction_2': '🐟 The fish swims forward automatically',
        'fishjump_instruction_3': '📢 Make sounds to make the fish jump',
        'fishjump_instruction_4': '🔊 Louder sounds = higher jumps',
        'fishjump_instruction_5': '⚠️ Avoid red piranha obstacles',
        'fishjump_instruction_6': '🏆 Try to get the highest score possible',
        'fishjump_start': '🎮 Start Game',
        'fishjump_note': '📝 Note: Game will launch in a new window',
        'fishjump_controls': '🎮 Controls',
        'fishjump_tips': '💡 Game Tips',
        'fishjump_tip_1': '• Keep microphone at appropriate distance',
        'fishjump_tip_2': '• Use whistles, claps, or other sounds',
        'fishjump_tip_3': '• Sound needs to reach certain volume to jump',
        'fishjump_tip_4': '• Score is automatically saved as high score',
        'fishjump_requirements': '⚙️ System Requirements',
        'fishjump_req_1': '✓ Microphone permission required',
        'fishjump_req_2': '✓ PyAudio must be installed',
        'fishjump_req_3': '✓ Pygame must be installed'
    }
}

# 预设提示词字典
PRESET_PROMPTS = {
    'zh': {
        "🐕 可爱小狗": "a cute little puppy, fluffy fur, adorable eyes, sitting on grass, high quality, detailed, photorealistic",
        "🏔️ 美丽风景": "a beautiful landscape with mountains, blue sky, green trees, peaceful lake, sunrise, detailed, photorealistic",
        "🌃 未来城市": "futuristic city, neon lights, flying cars, cyberpunk style, high tech buildings, night scene, detailed",
        "🌲 梦幻森林": "magical forest, glowing mushrooms, fairy lights, mystical atmosphere, enchanted trees, fantasy art",
        "🎨 抽象艺术": "abstract art, colorful, geometric shapes, modern art style, vibrant colors, artistic",
        "🌸 樱花季节": "cherry blossoms, sakura trees, pink petals falling, peaceful garden, spring season, detailed"
    },
    'en': {
        "🐕 Cute Puppy": "a cute little puppy, fluffy fur, adorable eyes, sitting on grass, high quality, detailed, photorealistic",
        "🏔️ Beautiful Landscape": "a beautiful landscape with mountains, blue sky, green trees, peaceful lake, sunrise, detailed, photorealistic",
        "🌃 Futuristic City": "futuristic city, neon lights, flying cars, cyberpunk style, high tech buildings, night scene, detailed",
        "🌲 Magical Forest": "magical forest, glowing mushrooms, fairy lights, mystical atmosphere, enchanted trees, fantasy art",
        "🎨 Abstract Art": "abstract art, colorful, geometric shapes, modern art style, vibrant colors, artistic",
        "🌸 Cherry Blossoms": "cherry blossoms, sakura trees, pink petals falling, peaceful garden, spring season, detailed"
    }
}

# 获取当前语言文本
def get_text(key, lang='zh'):
    return LANGUAGES.get(lang, LANGUAGES['zh']).get(key, key)

# 初始化语言设置
if 'language' not in st.session_state:
    st.session_state.language = 'zh'

# 初始化页面选择
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'image_gen'

# 初始化游戏运行状态
if 'game_running' not in st.session_state:
    st.session_state.game_running = False

# 初始化摄像头相关状态
if 'face_count' not in st.session_state:
    st.session_state.face_count = 0
if 'processing_fps' not in st.session_state:
    st.session_state.processing_fps = 0

# WebRTC配置
RTC_CONFIGURATION = RTCConfiguration({
    "iceServers": [
        {"urls": ["stun:stun.l.google.com:19302"]},
    ]
})

# 全局变量存储设置
face_detection_settings = {
    'enabled': True,
    'color': (0, 255, 0),
    'confidence': 0.3,
    'falling_effect': True,
    'falling_speed': 3.0
}

# 掉落人脸数据结构
falling_faces = []
last_face_capture_time = 0

class FallingFace:
    def __init__(self, face_img, x_start, frame_width, frame_height):
        self.face_img = face_img
        self.x = x_start + (face_img.shape[1] // 2)  # 从人脸中心开始
        self.y = -face_img.shape[0]  # 从顶部开始
        self.width = face_img.shape[1]
        self.height = face_img.shape[0]
        
        # 物理属性
        self.velocity_y = 0  # 垂直速度
        self.gravity = 0.5  # 重力加速度
        self.bounce_factor = 0.3  # 弹跳系数
        self.friction = 0.95  # 摩擦力
        self.is_on_ground = False
        
        # 随机水平速度
        import random
        self.velocity_x = random.uniform(-1, 1)
        
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.rotation = 0
        self.rotation_speed = random.uniform(-2, 2)
        
        # 生存时间（10秒）
        import time
        self.birth_time = time.time()
        self.lifetime = 10.0  # 10秒后消失
        
    def update(self, other_faces=None):
        import time
        current_time = time.time()
        
        # 检查是否超时
        if current_time - self.birth_time > self.lifetime:
            return False
        
        # 如果other_faces是None，设为空列表
        if other_faces is None:
            other_faces = []
        
        # 物理更新
        if not self.is_on_ground:
            # 应用重力
            self.velocity_y += self.gravity
            
            # 更新位置
            self.y += self.velocity_y
            self.x += self.velocity_x
            
            # 检查是否触地或撞到其他人脸
            ground_level = self.frame_height - self.height
            collision_level = ground_level
            
            # 简化的垂直堆叠检测
            if other_faces and len(other_faces) > 0:
                for other_face in other_faces:
                    if (other_face != self and 
                        hasattr(other_face, 'is_on_ground') and other_face.is_on_ground and
                        hasattr(other_face, 'x') and hasattr(other_face, 'y') and
                        hasattr(other_face, 'width') and hasattr(other_face, 'height')):
                        
                        # 检查水平重叠
                        if (abs(self.x - other_face.x) < (self.width + other_face.width) / 2):
                            # 计算可以停留的位置
                            possible_landing = other_face.y - self.height
                            if possible_landing >= 0 and possible_landing < collision_level:
                                collision_level = possible_landing
            
            if self.y >= collision_level:
                self.y = collision_level
                
                # 弹跳效果
                if abs(self.velocity_y) > 2:  # 只有速度够大才弹跳
                    self.velocity_y = -self.velocity_y * self.bounce_factor
                    self.velocity_x *= self.friction
                else:
                    # 速度太小，停下来
                    self.velocity_y = 0
                    self.velocity_x *= 0.8  # 摩擦
                    self.is_on_ground = True
            
            # 检查左右边界
            if self.x - self.width//2 <= 0:
                self.x = self.width//2
                self.velocity_x = -self.velocity_x * 0.7
            elif self.x + self.width//2 >= self.frame_width:
                self.x = self.frame_width - self.width//2
                self.velocity_x = -self.velocity_x * 0.7
        else:
            # 在停止状态时的物理处理
            # 地面上的微小摆动
            if abs(self.velocity_x) > 0.1:
                self.x += self.velocity_x
                self.velocity_x *= 0.95  # 逐渐减速
        
        # 旋转更新（在地面上时旋转变慢）
        if self.is_on_ground:
            self.rotation_speed *= 0.98
        self.rotation += self.rotation_speed
        
        return True
    
    def get_position(self):
        return int(self.x - self.width//2), int(self.y), int(self.width), int(self.height)
    
    def get_age(self):
        import time
        return time.time() - self.birth_time
    
    def check_horizontal_overlap(self, other_face, tolerance=5):
        """检查两个人脸是否在水平方向上重叠"""
        self_left = self.x - self.width // 2 - tolerance
        self_right = self.x + self.width // 2 + tolerance
        other_left = other_face.x - other_face.width // 2
        other_right = other_face.x + other_face.width // 2
        
        return not (self_right <= other_left or self_left >= other_right)

# 增强的人脸检测回调函数（带掉落效果）
def face_detection_callback(frame):
    global falling_faces, last_face_capture_time
    import time
    
    img = frame.to_ndarray(format="bgr24")
    frame_height, frame_width = img.shape[:2]
    current_time = time.time()
    
    if face_detection_settings['enabled']:
        try:
            # 初始化人脸检测器
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # 检测人脸
            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )
            
            # 更新人脸数量统计
            try:
                st.session_state.face_count = len(faces)
            except:
                pass
            
            # 绘制人脸框并捕获人脸（每1秒一次）
            if faces is not None and len(faces) > 0:
                # 记录是否在这一帧中创建了新的掉落人脸
                faces_captured_this_frame = False
                
                for i, (x, y, w, h) in enumerate(faces):
                    # 绘制检测框
                    cv2.rectangle(img, (x, y), (x + w, y + h), face_detection_settings['color'], 2)
                    cv2.putText(img, f'Face {i+1}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, face_detection_settings['color'], 1)
                    
                    # 每1秒捕获一次人脸用于掉落效果（支持多人脸）
                    if (face_detection_settings['falling_effect'] and 
                        current_time - last_face_capture_time > 1.0 and 
                        not faces_captured_this_frame):
                        
                        # 提取人脸区域
                        face_roi = img[y:y+h, x:x+w].copy()
                        
                        # 调整人脸大小（变小一点用于掉落）
                        face_size = min(w, h, 60)  # 最大60像素
                        if face_size > 20:  # 最小20像素
                            face_roi_resized = cv2.resize(face_roi, (face_size, face_size))
                            
                            # 为每个检测到的人脸创建掉落对象
                            new_falling_face = FallingFace(
                                face_roi_resized, 
                                x, 
                                frame_width, 
                                frame_height
                            )
                            falling_faces.append(new_falling_face)
                
                # 每1秒只处理一次，但会处理当前帧的所有人脸
                if (face_detection_settings['falling_effect'] and 
                    current_time - last_face_capture_time > 1.0 and 
                    len(faces) > 0):
                    
                    faces_captured_this_frame = True
                    last_face_capture_time = current_time
                    
                    # 限制同时掉落的人脸数量
                    if len(falling_faces) > 15:
                        falling_faces = falling_faces[-15:]
        
        except Exception as e:
            # 如果检测失败，至少返回原图像
            pass
    
    # 更新和绘制掉落的人脸
    if face_detection_settings['falling_effect']:
        try:
            # 更新掉落人脸位置（传入其他人脸用于碰撞检测）
            active_faces = []
            for falling_face in falling_faces:
                # 传入其他人脸进行堆叠检测
                other_faces = [f for f in falling_faces if f != falling_face]
                if falling_face.update(other_faces):  # 如果还活着
                    active_faces.append(falling_face)
                    
                    # 在图像上绘制掉落的人脸
                    fx, fy, fw, fh = falling_face.get_position()
                    
                    # 确保坐标在有效范围内
                    if (fx >= 0 and fy >= 0 and 
                        fx + fw <= frame_width and 
                        fy + fh <= frame_height):
                        
                        # 简单地叠加人脸图像（不做旋转，保持性能）
                        try:
                            img[fy:fy+fh, fx:fx+fw] = falling_face.face_img
                            
                            # 添加一个半透明边框效果表示年龄
                            age = falling_face.get_age()
                            alpha = max(0.3, 1.0 - age / 10.0)  # 随时间变透明
                            border_color = (int(255 * alpha), int(255 * alpha), int(255 * alpha))
                            cv2.rectangle(img, (fx-1, fy-1), (fx+fw+1, fy+fh+1), border_color, 1)
                            
                            # 显示剩余时间
                            remaining_time = int(10 - age)
                            if remaining_time > 0:
                                cv2.putText(img, f'{remaining_time}s', (fx, fy-5), 
                                           cv2.FONT_HERSHEY_SIMPLEX, 0.3, border_color, 1)
                        except:
                            pass  # 如果绘制失败，跳过这个人脸
            
            falling_faces = active_faces
            
        except Exception as e:
            # 如果掉落效果出错，清空掉落列表
            falling_faces = []
    
    return av.VideoFrame.from_ndarray(img, format="bgr24")

# 页面配置
st.set_page_config(
    page_title=get_text('page_title', st.session_state.language),
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化模型
@st.cache_resource
def load_model():
    pipe = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16)
    pipe.to("cuda" if torch.cuda.is_available() else "cpu")
    return pipe

def main():
    # 左侧边栏
    with st.sidebar:
        # 语言切换按钮
        st.subheader(get_text('language_switch', st.session_state.language))
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button(get_text('lang_zh', st.session_state.language), use_container_width=True):
                st.session_state.language = 'zh'
                st.rerun()
                
        with col2:
            if st.button(get_text('lang_en', st.session_state.language), use_container_width=True):
                st.session_state.language = 'en'
                st.rerun()
        
        st.markdown("---")
        
        # 页面导航
        st.subheader(get_text('navigation', st.session_state.language))
        
        # 图像生成器按钮
        if st.button(get_text('nav_image_gen', st.session_state.language), 
                    type="primary" if st.session_state.current_page == 'image_gen' else "secondary",
                    use_container_width=True):
            st.session_state.current_page = 'image_gen'
            st.rerun()
        
        # 摄像头识别按钮
        if st.button(get_text('nav_camera', st.session_state.language),
                    type="primary" if st.session_state.current_page == 'camera' else "secondary", 
                    use_container_width=True):
            st.session_state.current_page = 'camera'
            st.rerun()
        
        # FishJump游戏按钮
        if st.button(get_text('nav_fishjump', st.session_state.language),
                    type="primary" if st.session_state.current_page == 'fishjump' else "secondary",
                    use_container_width=True):
            st.session_state.current_page = 'fishjump'
            st.rerun()
        
        st.markdown("---")
    
    # 根据当前页面显示内容
    if st.session_state.current_page == 'image_gen':
        image_generator_page()
    elif st.session_state.current_page == 'camera':
        camera_page()
    elif st.session_state.current_page == 'fishjump':
        fishjump_page()

def image_generator_page():
    # 左侧边栏 - 图像生成设置
    with st.sidebar:
        
        # 系统信息
        st.subheader(get_text('system_info', st.session_state.language))
        st.info(get_text('pytorch_info', st.session_state.language))
        device_info = get_text('device_gpu', st.session_state.language) if torch.cuda.is_available() else get_text('device_cpu', st.session_state.language)
        st.info(device_info)
        st.markdown("---")
        
        # 图像尺寸选择
        st.subheader(get_text('image_dimensions', st.session_state.language))
        size_options = {
            get_text('size_512x512', st.session_state.language): (512, 512),
            get_text('size_768x512', st.session_state.language): (768, 512),
            get_text('size_512x768', st.session_state.language): (512, 768)
        }
        selected_size = st.selectbox(get_text('select_size', st.session_state.language), list(size_options.keys()))
        width, height = size_options[selected_size]
        
        steps = st.slider(get_text('generation_steps', st.session_state.language), min_value=10, max_value=50, value=20, help=get_text('steps_help', st.session_state.language))
        
        st.markdown("---")
        
        # 预设提示词
        st.subheader(get_text('quick_select', st.session_state.language))
        preset_prompts = PRESET_PROMPTS[st.session_state.language]
        
        for name, preset_prompt in preset_prompts.items():
            if st.button(name, use_container_width=True):
                st.session_state.selected_prompt = preset_prompt
    
    # 主内容区域
    st.title(get_text('app_title', st.session_state.language))
    
    # 图片描述输入区域（放在中间）
    st.subheader(get_text('image_settings', st.session_state.language))
    prompt = st.text_area(
        get_text('image_description', st.session_state.language), 
        value=get_text('default_prompt', st.session_state.language),
        height=100,
        help=get_text('image_description_help', st.session_state.language),
        key="prompt_input"
    )
    
    # 更新提示词（如果从预设选择）
    if 'selected_prompt' in st.session_state:
        prompt = st.session_state.selected_prompt
        # 清除session state以避免持续更新
        del st.session_state.selected_prompt
        st.rerun()
    
    # 生成按钮
    generate_button = st.button(get_text('generate_button', st.session_state.language), type="primary", use_container_width=True)
    
    st.markdown("---")
    st.title(get_text('image_display', st.session_state.language))
    
    # 创建两列布局用于显示结果
    col1, col2 = st.columns([1, 1])
    
    # 初始化session state
    if 'generated_images' not in st.session_state:
        st.session_state.generated_images = []
    if 'generation_history' not in st.session_state:
        st.session_state.generation_history = []
    
    # 处理生成按钮点击
    if generate_button and prompt.strip():
        with st.spinner(get_text('generating', st.session_state.language)):
            try:
                # 显示进度信息
                progress_text = st.empty()
                progress_bar = st.progress(0)
                
                progress_text.text(get_text('loading_model', st.session_state.language))
                progress_bar.progress(20)
                pipe = load_model()
                
                progress_text.text(get_text('generating_image', st.session_state.language))
                progress_bar.progress(50)
                
                # 生成图像
                image = pipe(prompt, num_inference_steps=steps, width=width, height=height).images[0]
                
                progress_text.text(get_text('generation_complete', st.session_state.language))
                progress_bar.progress(100)
                time.sleep(0.5)  # 短暂显示完成状态
                
                # 清除进度显示
                progress_text.empty()
                progress_bar.empty()
                
                # 保存到session state
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                st.session_state.generated_images.insert(0, {
                    'image': image,
                    'prompt': prompt,
                    'steps': steps,
                    'size': f"{width}x{height}",
                    'timestamp': timestamp
                })
                
                # 保持最多10张图像
                if len(st.session_state.generated_images) > 10:
                    st.session_state.generated_images = st.session_state.generated_images[:10]
                
                st.success(get_text('generation_success', st.session_state.language))
                
            except Exception as e:
                st.error(get_text('generation_failed', st.session_state.language) + str(e))
    
    # 显示生成的图像
    if st.session_state.generated_images:
        st.subheader(get_text('latest_image', st.session_state.language))
        
        # 显示最新图像
        latest_image = st.session_state.generated_images[0]
        
        with col1:
            st.image(
                latest_image['image'], 
                caption=get_text('prompt_label', st.session_state.language) + latest_image['prompt'][:50] + "...", 
                use_container_width=True
            )
            
            # 图像信息
            st.info(f"""
            {get_text('prompt_info', st.session_state.language)}{latest_image['prompt']}
            {get_text('steps_info', st.session_state.language)}{latest_image['steps']}
            {get_text('size_info', st.session_state.language)}{latest_image['size']}
            {get_text('time_info', st.session_state.language)}{latest_image['timestamp']}
            """)
        
        with col2:
            # 下载按钮
            img_buffer = BytesIO()
            latest_image['image'].save(img_buffer, format='PNG')
            img_buffer.seek(0)
            
            st.download_button(
                label=get_text('download_button', st.session_state.language),
                data=img_buffer.getvalue(),
                file_name=f"ai_generated_{int(time.time())}.png",
                mime="image/png",
                use_container_width=True
            )
            
            # 重新生成按钮
            if st.button(get_text('regenerate_button', st.session_state.language), use_container_width=True):
                st.rerun()
            
            # 清除历史按钮
            if st.button(get_text('clear_history', st.session_state.language), use_container_width=True):
                st.session_state.generated_images = []
                st.rerun()
        
        # 历史图像展示
        if len(st.session_state.generated_images) > 1:
            st.subheader(get_text('history_title', st.session_state.language))
            
            # 使用网格布局显示历史图像
            cols_per_row = 3
            for i in range(1, len(st.session_state.generated_images)):
                if (i - 1) % cols_per_row == 0:
                    cols = st.columns(cols_per_row)
                
                with cols[(i - 1) % cols_per_row]:
                    img_data = st.session_state.generated_images[i]
                    st.image(img_data['image'], caption=f"{img_data['timestamp']}", use_container_width=True)
                    
                    if st.button(get_text('view_details', st.session_state.language) + str(i), key=f"detail_{i}"):
                        st.session_state.selected_detail = i
    
    else:
        # 空状态显示
        st.info(get_text('empty_state', st.session_state.language))
        
        # 显示示例图像区域
        st.subheader(get_text('features_title', st.session_state.language))
        feature_cols = st.columns(3)
        
        with feature_cols[0]:
            st.markdown(get_text('feature_quality', st.session_state.language))
        
        with feature_cols[1]:
            st.markdown(get_text('feature_gpu', st.session_state.language))
        
        with feature_cols[2]:
            st.markdown(get_text('feature_ui', st.session_state.language))

def camera_page():
    # 左侧边栏 - 摄像头设置
    with st.sidebar:
        st.title(get_text('page_camera', st.session_state.language))
        st.markdown("---")
        
        # 摄像头设置
        st.subheader("📹 " + get_text('camera_settings', st.session_state.language) if st.session_state.language == 'zh' else "📹 Camera Settings")
        
        # 人脸检测开关
        face_detection_enabled = st.checkbox(
            get_text('face_detection', st.session_state.language) if st.session_state.language == 'zh' else "Face Detection",
            value=True,
            help=get_text('face_detection_help', st.session_state.language) if st.session_state.language == 'zh' else "Enable to mark detected faces in video"
        )
        
        # 人脸掉落效果开关
        falling_effect_enabled = st.checkbox(
            "🎭 人脸掉落效果" if st.session_state.language == 'zh' else "🎭 Face Falling Effect",
            value=True,
            help="启用后检测到的人脸会从顶部掉落" if st.session_state.language == 'zh' else "Detected faces will fall from top when enabled"
        )
        
        st.markdown("---")
        
        # 检测设置
        st.subheader("🔍 " + ("检测设置" if st.session_state.language == 'zh' else "Detection Settings"))
        
        # 置信度阈值
        confidence_threshold = st.slider(
            "检测置信度" if st.session_state.language == 'zh' else "Detection Confidence",
            min_value=0.1,
            max_value=1.0,
            value=0.3,
            step=0.05,
            help="置信度越高，检测越严格" if st.session_state.language == 'zh' else "Higher confidence means stricter detection"
        )
        
        # 检测框颜色选择
        color_option = st.selectbox(
            "检测框颜色" if st.session_state.language == 'zh' else "Detection Box Color",
            ["Green", "Red", "Blue", "Yellow", "Purple"],
            index=0
        )
        
        color_map = {
            "Green": (0, 255, 0),
            "Red": (0, 0, 255),
            "Blue": (255, 0, 0),
            "Yellow": (0, 255, 255),
            "Purple": (255, 0, 255)
        }
        detection_color = color_map[color_option]
        
        # 掉落效果设置
        if falling_effect_enabled:
            st.subheader("🎭 " + ("掉落效果设置" if st.session_state.language == 'zh' else "Falling Effect Settings"))
            
            # 掉落速度控制
            falling_speed = st.slider(
                "掉落速度" if st.session_state.language == 'zh' else "Falling Speed",
                min_value=1.0,
                max_value=10.0,
                value=3.0,
                step=0.5,
                help="调整人脸掉落的速度" if st.session_state.language == 'zh' else "Adjust the speed of falling faces"
            )
        else:
            falling_speed = 3.0
        
        st.markdown("---")
        
        # 摄像头状态
        st.subheader("📊 " + ("摄像头状态" if st.session_state.language == 'zh' else "Camera Status"))
        
        if 'webrtc_ctx' in st.session_state and st.session_state.webrtc_ctx:
            if st.session_state.webrtc_ctx.state.playing:
                st.success("🟡 " + ("运行中" if st.session_state.language == 'zh' else "Running"))
            else:
                st.info("🟢 " + ("就绪" if st.session_state.language == 'zh' else "Ready"))
        else:
            st.warning("🔴 " + ("已停止" if st.session_state.language == 'zh' else "Stopped"))
        
        st.markdown("---")
        
        # 检测统计
        st.subheader("📈 " + ("检测统计" if st.session_state.language == 'zh' else "Detection Stats"))
        
        col_faces, col_fps = st.columns(2)
        with col_faces:
            st.metric(
                "检测到的人脸" if st.session_state.language == 'zh' else "Faces Detected",
                st.session_state.face_count
            )
        
        with col_fps:
            st.metric(
                "处理帧率" if st.session_state.language == 'zh' else "Processing FPS",
                f"{st.session_state.processing_fps}"
            )
    
    # 主内容区域
    st.title("📹 " + ("AI摄像头人脸识别" if st.session_state.language == 'zh' else "AI Camera Face Detection"))
    
    # 创建两列布局
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # 更新设置
        face_detection_settings['enabled'] = face_detection_enabled
        face_detection_settings['color'] = detection_color
        face_detection_settings['confidence'] = confidence_threshold
        face_detection_settings['falling_effect'] = falling_effect_enabled
        face_detection_settings['falling_speed'] = falling_speed
        
        # WebRTC摄像头流
        webrtc_ctx = webrtc_streamer(
            key="face-detection",
            video_frame_callback=face_detection_callback,
            rtc_configuration=RTC_CONFIGURATION,
            media_stream_constraints={"video": True, "audio": False},
        )
        
        # 存储webrtc context到session state
        st.session_state.webrtc_ctx = webrtc_ctx
    
    with col2:
        # 使用说明
        st.subheader("📋 " + ("使用说明" if st.session_state.language == 'zh' else "Instructions"))
        
        if st.session_state.language == 'zh':
            st.markdown("""
            1. 点击"START"按钮启动摄像头
            
            2. 调整检测设置来优化识别效果
            
            3. 绿色框表示检测到的人脸
            
            4. 🎭 开启掉落效果，人脸会每秒复制并掉落
            
            5. 可以调整掉落速度和检测灵敏度
            """)
            
            st.info("🔒 隐私提醒：视频流仅在本地处理，不会上传到服务器")
        else:
            st.markdown("""
            1. Click "START" button to launch camera
            
            2. Adjust detection settings to optimize recognition
            
            3. Green boxes indicate detected faces
            
            4. 🎭 Enable falling effect to make faces fall every second
            
            5. Adjust falling speed and detection sensitivity
            """)
            
                        
            st.info("🔒 Privacy Notice: Video stream is processed locally only, not uploaded to server")

def fishjump_page():
    """FishJump游戏页面"""
    import subprocess
    import sys
    
    # 主标题
    st.title(get_text('fishjump_title', st.session_state.language))
    st.markdown(get_text('fishjump_desc', st.session_state.language))
    st.markdown("---")
    
    # 创建三列布局
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        # 游戏说明
        st.subheader(get_text('fishjump_instruction', st.session_state.language))
        st.markdown(f"""
        {get_text('fishjump_instruction_1', st.session_state.language)}
        
        {get_text('fishjump_instruction_2', st.session_state.language)}
        
        {get_text('fishjump_instruction_3', st.session_state.language)}
        
        {get_text('fishjump_instruction_4', st.session_state.language)}
        
        {get_text('fishjump_instruction_5', st.session_state.language)}
        
        {get_text('fishjump_instruction_6', st.session_state.language)}
        """)
    
    with col2:
        # 控制方式和提示
        st.subheader(get_text('fishjump_tips', st.session_state.language))
        st.markdown(f"""
        {get_text('fishjump_tip_1', st.session_state.language)}
        
        {get_text('fishjump_tip_2', st.session_state.language)}
        
        {get_text('fishjump_tip_3', st.session_state.language)}
        
        {get_text('fishjump_tip_4', st.session_state.language)}
        """)
        
        # 显示最高分
        HS_PATH = 'highscore.txt'
        try:
            with open(HS_PATH, 'r', encoding='utf-8') as f:
                high_score = int(f.read().strip() or '0')
                st.metric("🏆 " + ("最高分" if st.session_state.language == 'zh' else "High Score"), high_score)
        except Exception:
            st.metric("🏆 " + ("最高分" if st.session_state.language == 'zh' else "High Score"), 0)
    
    with col3:
        # 系统要求
        st.subheader(get_text('fishjump_requirements', st.session_state.language))
        st.markdown(f"""
        {get_text('fishjump_req_1', st.session_state.language)}
        
        {get_text('fishjump_req_2', st.session_state.language)}
        
        {get_text('fishjump_req_3', st.session_state.language)}
        """)
        
        st.markdown("---")
        
        # 启动游戏按钮
        if st.button(get_text('fishjump_start', st.session_state.language), 
                    type="primary", 
                    use_container_width=True):
            try:
                # 获取voice_parkour.py的路径
                parkour_path = r'f:\PolyU\Sem1\5913Programming\Interactive_Website\Interactive_Ai_website-3\voice_parkour.py'
                
                # 在新进程中启动游戏
                subprocess.Popen([sys.executable, parkour_path], 
                               creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0)
                
                st.success("🎮 " + ("游戏已启动！请查看新窗口。" if st.session_state.language == 'zh' else "Game started! Check the new window."))
            except Exception as e:
                st.error(f"❌ " + ("启动失败：" if st.session_state.language == 'zh' else "Failed to start: ") + str(e))
        
        st.info(get_text('fishjump_note', st.session_state.language))
    
    st.markdown("---")
    
    # 游戏预览图片区域
    st.subheader("🖼️ " + ("游戏预览" if st.session_state.language == 'zh' else "Game Preview"))
    
    preview_col1, preview_col2 = st.columns(2)
    
    with preview_col1:
        st.markdown("""
        ### 🐟 游戏特色
        - **声控操作**：使用麦克风声音控制跳跃
        - **动态难度**：随机生成的障碍物
        - **实时反馈**：显示音量和分数
        - **最高分记录**：自动保存你的最佳成绩
        """ if st.session_state.language == 'zh' else """
        ### 🐟 Game Features
        - **Voice Control**: Use microphone to control jumps
        - **Dynamic Difficulty**: Randomly generated obstacles
        - **Real-time Feedback**: Display volume and score
        - **High Score**: Automatically saves your best score
        """)
    
    with preview_col2:
        st.markdown("""
        ### 🎮 游戏画面
        - 🌊 美丽的波浪背景
        - 🐟 可爱的小鱼角色
        - 🦈 危险的食人鱼障碍
        - 📊 实时音量显示
        """ if st.session_state.language == 'zh' else """
        ### 🎮 Game Graphics
        - 🌊 Beautiful wave background
        - 🐟 Cute fish character
        - 🦈 Dangerous piranha obstacles
        - 📊 Real-time volume display
        """)

if __name__ == "__main__":
    main()

