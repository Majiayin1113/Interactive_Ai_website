import streamlit as st
from streamlit_webrtc import webrtc_streamer
import av
import cv2

st.title("📹 简化版摄像头测试")

def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    
    # 简单的图像翻转效果
    flipped = img[::-1, :, :]
    
    # 尝试添加人脸检测
    try:
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(flipped, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        for (x, y, w, h) in faces:
            cv2.rectangle(flipped, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(flipped, 'Face', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
    except:
        pass
    
    return av.VideoFrame.from_ndarray(flipped, format="bgr24")

st.write("点击下面的 START 按钮启动摄像头")

webrtc_streamer(
    key="simple-camera", 
    video_frame_callback=video_frame_callback,
    media_stream_constraints={"video": True, "audio": False}
)