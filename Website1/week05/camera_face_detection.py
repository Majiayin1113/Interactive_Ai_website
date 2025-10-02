import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration
import cv2
import numpy as np
import av
from typing import Union

# 语言文本字典
CAMERA_LANGUAGES = {
    'zh': {
        'page_title': 'AI摄像头人脸识别',
        'app_title': '📹 AI摄像头人脸识别',
        'camera_settings': '📹 摄像头设置',
        'detection_settings': '🔍 检测设置',
        'face_detection': '人脸检测',
        'face_detection_help': '开启后将在视频中标记检测到的人脸',
        'confidence_threshold': '检测置信度',
        'confidence_help': '置信度越高，检测越严格',
        'detection_color': '检测框颜色',
        'start_camera': '📹 启动摄像头',
        'stop_camera': '⏹️ 停止摄像头',
        'camera_status': '📊 摄像头状态',
        'status_ready': '🟢 就绪',
        'status_running': '🟡 运行中',
        'status_stopped': '🔴 已停止',
        'detection_stats': '📈 检测统计',
        'faces_detected': '检测到的人脸数量',
        'processing_fps': '处理帧率',
        'instructions_title': '📋 使用说明',
        'instructions_1': '1. 点击"启动摄像头"开始视频流',
        'instructions_2': '2. 调整检测设置来优化识别效果',
        'instructions_3': '3. 绿色框表示检测到的人脸',
        'instructions_4': '4. 可以调整置信度阈值来改变检测灵敏度',
        'privacy_notice': '🔒 隐私提醒：视频流仅在本地处理，不会上传到服务器',
        'language_switch': '🌐 Language',
        'lang_zh': '🇨🇳 中文',
        'lang_en': '🇺🇸 English'
    },
    'en': {
        'page_title': 'AI Camera Face Detection',
        'app_title': '📹 AI Camera Face Detection',
        'camera_settings': '📹 Camera Settings',
        'detection_settings': '🔍 Detection Settings',
        'face_detection': 'Face Detection',
        'face_detection_help': 'Enable to mark detected faces in video',
        'confidence_threshold': 'Detection Confidence',
        'confidence_help': 'Higher confidence means stricter detection',
        'detection_color': 'Detection Box Color',
        'start_camera': '📹 Start Camera',
        'stop_camera': '⏹️ Stop Camera',
        'camera_status': '📊 Camera Status',
        'status_ready': '🟢 Ready',
        'status_running': '🟡 Running',
        'status_stopped': '🔴 Stopped',
        'detection_stats': '📈 Detection Stats',
        'faces_detected': 'Faces Detected',
        'processing_fps': 'Processing FPS',
        'instructions_title': '📋 Instructions',
        'instructions_1': '1. Click "Start Camera" to begin video stream',
        'instructions_2': '2. Adjust detection settings to optimize recognition',
        'instructions_3': '3. Green boxes indicate detected faces',
        'instructions_4': '4. Adjust confidence threshold to change sensitivity',
        'privacy_notice': '🔒 Privacy Notice: Video stream is processed locally only, not uploaded to server',
        'language_switch': '🌐 语言',
        'lang_zh': '🇨🇳 中文',
        'lang_en': '🇺🇸 English'
    }
}

# 获取当前语言文本
def get_camera_text(key, lang='zh'):
    return CAMERA_LANGUAGES.get(lang, CAMERA_LANGUAGES['zh']).get(key, key)

# 初始化语言设置
if 'camera_language' not in st.session_state:
    st.session_state.camera_language = 'zh'

# 初始化检测统计
if 'face_count' not in st.session_state:
    st.session_state.face_count = 0
if 'processing_fps' not in st.session_state:
    st.session_state.processing_fps = 0

class FaceDetectionTransformer(VideoTransformerBase):
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.confidence_threshold = 0.3
        self.detection_color = (0, 255, 0)  # Green
        self.face_detection_enabled = True
        self.frame_count = 0
        self.last_fps_time = cv2.getTickCount()
        
    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        
        if self.face_detection_enabled:
            # 转换为灰度图进行人脸检测
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # 检测人脸
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            
            # 更新人脸数量统计
            st.session_state.face_count = len(faces)
            
            # 绘制人脸框
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), self.detection_color, 2)
                
                # 添加置信度文本（简化版）
                cv2.putText(img, 'Face', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.detection_color, 1)
        
        # 计算FPS
        self.frame_count += 1
        if self.frame_count % 30 == 0:  # 每30帧计算一次FPS
            current_time = cv2.getTickCount()
            fps = 30.0 / ((current_time - self.last_fps_time) / cv2.getTickFrequency())
            st.session_state.processing_fps = round(fps, 1)
            self.last_fps_time = current_time
        
        return av.VideoFrame.from_ndarray(img, format="bgr24")
    
    def update_settings(self, confidence_threshold, detection_color, face_detection_enabled):
        self.confidence_threshold = confidence_threshold
        self.detection_color = detection_color
        self.face_detection_enabled = face_detection_enabled

# WebRTC配置
RTC_CONFIGURATION = RTCConfiguration({
    "iceServers": [
        {"urls": ["stun:stun.l.google.com:19302"]},
    ]
})

def main():
    # 页面配置
    st.set_page_config(
        page_title=get_camera_text('page_title', st.session_state.camera_language),
        page_icon="📹",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # 左侧边栏
    with st.sidebar:
        # 语言切换按钮
        st.subheader(get_camera_text('language_switch', st.session_state.camera_language))
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button(get_camera_text('lang_zh', st.session_state.camera_language), use_container_width=True):
                st.session_state.camera_language = 'zh'
                st.rerun()
                
        with col2:
            if st.button(get_camera_text('lang_en', st.session_state.camera_language), use_container_width=True):
                st.session_state.camera_language = 'en'
                st.rerun()
        
        st.markdown("---")
        
        st.title(get_camera_text('app_title', st.session_state.camera_language))
        st.markdown("---")
        
        # 摄像头设置
        st.subheader(get_camera_text('camera_settings', st.session_state.camera_language))
        
        # 人脸检测开关
        face_detection_enabled = st.checkbox(
            get_camera_text('face_detection', st.session_state.camera_language),
            value=True,
            help=get_camera_text('face_detection_help', st.session_state.camera_language)
        )
        
        st.markdown("---")
        
        # 检测设置
        st.subheader(get_camera_text('detection_settings', st.session_state.camera_language))
        
        # 置信度阈值
        confidence_threshold = st.slider(
            get_camera_text('confidence_threshold', st.session_state.camera_language),
            min_value=0.1,
            max_value=1.0,
            value=0.3,
            step=0.05,
            help=get_camera_text('confidence_help', st.session_state.camera_language)
        )
        
        # 检测框颜色选择
        st.write(get_camera_text('detection_color', st.session_state.camera_language))
        color_option = st.selectbox(
            "",
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
        
        st.markdown("---")
        
        # 摄像头状态
        st.subheader(get_camera_text('camera_status', st.session_state.camera_language))
        
        if 'webrtc_ctx' in st.session_state and st.session_state.webrtc_ctx:
            if st.session_state.webrtc_ctx.state.playing:
                st.success(get_camera_text('status_running', st.session_state.camera_language))
            else:
                st.info(get_camera_text('status_ready', st.session_state.camera_language))
        else:
            st.warning(get_camera_text('status_stopped', st.session_state.camera_language))
        
        st.markdown("---")
        
        # 检测统计
        st.subheader(get_camera_text('detection_stats', st.session_state.camera_language))
        
        col_faces, col_fps = st.columns(2)
        with col_faces:
            st.metric(
                get_camera_text('faces_detected', st.session_state.camera_language),
                st.session_state.face_count
            )
        
        with col_fps:
            st.metric(
                get_camera_text('processing_fps', st.session_state.camera_language),
                f"{st.session_state.processing_fps}"
            )
    
    # 主内容区域
    st.title(get_camera_text('app_title', st.session_state.camera_language))
    
    # 创建两列布局
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # WebRTC摄像头流
        webrtc_ctx = webrtc_streamer(
            key="face-detection",
            mode="sendrecv",
            rtc_configuration=RTC_CONFIGURATION,
            video_processor_factory=FaceDetectionTransformer,
            media_stream_constraints={"video": True, "audio": False},
            async_processing=True,
        )
        
        # 存储webrtc context到session state
        st.session_state.webrtc_ctx = webrtc_ctx
        
        # 更新transformer设置
        if webrtc_ctx.video_processor:
            webrtc_ctx.video_processor.update_settings(
                confidence_threshold,
                detection_color,
                face_detection_enabled
            )
    
    with col2:
        # 使用说明
        st.subheader(get_camera_text('instructions_title', st.session_state.camera_language))
        
        st.markdown(f"""
        {get_camera_text('instructions_1', st.session_state.camera_language)}
        
        {get_camera_text('instructions_2', st.session_state.camera_language)}
        
        {get_camera_text('instructions_3', st.session_state.camera_language)}
        
        {get_camera_text('instructions_4', st.session_state.camera_language)}
        """)
        
        st.info(get_camera_text('privacy_notice', st.session_state.camera_language))
        
        # 实时统计显示
        if face_detection_enabled:
            st.success(f"✅ {get_camera_text('face_detection', st.session_state.camera_language)}: ON")
        else:
            st.warning(f"⚠️ {get_camera_text('face_detection', st.session_state.camera_language)}: OFF")

if __name__ == "__main__":
    main()