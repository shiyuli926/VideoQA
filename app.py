import streamlit as st
import os
from io import BytesIO
import tempfile # 用于创建临时文件
from pathlib import Path # 用于获取文件后缀
from session_state import init_session_state
from frontend.ui_components import upload_section, summary_section, chat_section

# 页面配置
st.set_page_config(page_title="AI 视频助手", layout="wide")
init_session_state()

# 侧边栏（可选，用于存放设置）
with st.sidebar:
    st.title("ZX-CE AI Assistant")
    st.info("基于 Whisper + LangChain 的视频问答系统 ")

# 定义阈值: 100MB
MAX_MEMORY_SIZE = 100 * 1024 * 1024 

if not st.session_state.file_uploaded:
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        uploaded_file = upload_section()
        if uploaded_file:
            # 获取文件大小
            file_size = uploaded_file.size
            
            if file_size < MAX_MEMORY_SIZE:
                # 方式1：直接存入内存 (BytesIO)
                st.session_state.video_data = BytesIO(uploaded_file.read())
                st.session_state.processing_mode = "memory"
                st.success(f"小文件预览：已载入内存 ({file_size / 1024 / 1024:.2f} MB)")
            else:
                # 方式2：保存到临时磁盘路径 (tempfile)
                # suffix确保浏览器和后端能识别格式
                suffix = os.path.splitext(uploaded_file.name)[-1]
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    tmp.write(uploaded_file.read())
                    st.session_state.video_data = tmp.name
                st.session_state.processing_mode = "disk"
                st.warning(f"大文件预览：已转存临时磁盘 ({file_size / 1024 / 1024:.2f} MB)")
            
            st.session_state.file_uploaded = True
            st.rerun()
else:
    left_col, right_col = st.columns([1, 1])
    with left_col:
        st.subheader("📹 原始视频")
    
        if st.session_state.video_data:
        # 无论内存还是磁盘模式，我们都尝试获取一个可靠的字节流
            try:
                if st.session_state.processing_mode == "memory":
                # 重新获取字节数据
                    st.session_state.video_data.seek(0)
                    video_bytes = st.session_state.video_data.read()
                # 尝试直接传字节数组（通常比传 BytesIO 更稳定）
                    st.video(video_bytes)
                else:
                # 磁盘模式：检查文件并读取
                    if os.path.exists(st.session_state.video_data):
                        st.video(st.session_state.video_data)
            except Exception as e:
                st.error(f"视频渲染失败: {e}")

    with right_col:
        summary_section(st.session_state.summary)
        st.divider()
        chat_section()