import streamlit as st
import os
import json
from io import BytesIO
import tempfile 
from pathlib import Path 
from session_state import init_session_state
from frontend.ui_components import upload_section, summary_section, chat_section

# 1. 页面配置 (必须在最顶部)
st.set_page_config(page_title="AI 视频助手 - 核心解析", layout="wide")
init_session_state()

# 2. 权限拦截与跳转按钮
if not st.session_state.get("is_logged_in", False):
    col1, col2 = st.columns([3, 1])
    with col1:
        st.warning("⚠️ 会话已过期或未登录，请重新登录。")
    with col2:
        if st.button("👉 点击跳转登录"):
            st.switch_page("app.py")
    st.stop() # 停止后续代码运行

# 3. 侧边栏：用户信息与退出登录
with st.sidebar:
    st.markdown(f"### 👤 当前用户: **{st.session_state.username}**")
    if st.button("🚪 退出登录", use_container_width=True):
        st.session_state.is_logged_in = False
        st.session_state.username = None
        st.switch_page("app.py")
    st.divider()
    
    # 加载历史记录 (从 data/history.json)
    st.title("📜 历史解析记录")
    history_path = "data/history.json"
    if os.path.exists(history_path):
        with open(history_path, "r", encoding="utf-8") as f:
            all_history = json.load(f)
            # 获取当前用户的特定历史
            user_history = all_history.get(st.session_state.username, [])
            
            if not user_history:
                st.write("暂无历史记录")
            for item in user_history:
                # 使用唯一 key 防止 ID 冲突
                st.button(f"📹 {item['title']}", key=f"hist_{item['title']}")
    else:
        st.write("未找到历史数据库")

st.title("🎬 视频解析助手")

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
            try:
                if st.session_state.processing_mode == "memory":
                    st.session_state.video_data.seek(0)
                    video_bytes = st.session_state.video_data.read()
                    st.video(video_bytes)
                else:
                    if os.path.exists(st.session_state.video_data):
                        st.video(st.session_state.video_data)
            except Exception as e:
                st.error(f"视频渲染失败: {e}")

        # --- 在这里添加“重新上传”按钮 ---
        st.write("") # 添加一点间距
        if st.button("🔄 重新上传", use_container_width=True):
            # 1. 如果是磁盘模式，删除临时文件防止占用空间
            if st.session_state.processing_mode == "disk" and os.path.exists(st.session_state.video_data):
                try:
                    os.remove(st.session_state.video_data)
                except Exception as e:
                    print(f"清理临时文件失败: {e}")
            
            # 2. 重置所有相关的 session_state
            st.session_state.file_uploaded = False
            st.session_state.video_data = None
            st.session_state.processing_mode = None
            
            # 3. 强制页面重绘，回到上传逻辑
            st.rerun()

    with right_col:
        summary_section(st.session_state.summary)
        st.divider()
        chat_section()

# 模拟添加历史记录（在视频上传成功后调用）
if st.session_state.file_uploaded and not st.session_state.history:
    st.session_state.history.append({"title": "最新上传视频", "date": "2026-01-12"})