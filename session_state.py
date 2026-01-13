import streamlit as st

def init_session_state():
    if "file_uploaded" not in st.session_state:
        st.session_state.file_uploaded = False
    if "video_data" not in st.session_state:
        st.session_state.video_data = None  # 存储 BytesIO 或 文件路径
    if "processing_mode" not in st.session_state:
        st.session_state.processing_mode = None # "memory" 或 "disk"
    if "summary" not in st.session_state:
        st.session_state.summary = ""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []