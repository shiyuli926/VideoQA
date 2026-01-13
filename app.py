import streamlit as st
import json
import os
from session_state import init_session_state

# 必须是第一个 Streamlit 命令
st.set_page_config(page_title="AI 视频助手 - 登录", layout="centered")
init_session_state()

# 后端工具函数：从 JSON 加载用户
def load_users():
    # 优先读取物理文件
    if os.path.exists("data/users.json"):
        with open("data/users.json", "r", encoding="utf-8") as f:
            return json.load(f)
    # 如果文件不存在，使用 session_state 中的模拟数据作为备选
    return st.session_state.get("user_db", {"1": "1"})

# --- 1. 自动跳转逻辑 ---
if st.session_state.is_logged_in:
    st.switch_page("pages/01_Main_App.py")

# --- 2. 登录界面渲染 ---
st.title("📽️ AI 视频助手系统")
tab1, tab2 = st.tabs(["用户登录", "新用户注册"])

with tab1:
    input_user = st.text_input("用户名", key="login_user_id")
    input_pwd = st.text_input("密码", type="password", key="login_pwd_id")
    
    # if st.button("立即登录", use_container_width=True):
    #     users = load_users()
    #     if input_user in users and users[input_user] == input_pwd:
    #         st.session_state.is_logged_in = True
    #         st.session_state.username = input_user
    #         st.switch_page("pages/01_Main_App.py") # 关键：登录成功立即跳转
    #     else:
    #         st.error("用户名或密码错误")

    if st.button("立即登录", use_container_width=True):
        users = load_users()
    
    # 后端防御性编程：确保两端都是纯净的字符串
        input_u = str(input_user).strip()
        input_p = str(input_pwd).strip()
    
    # 校验
        if input_u in users and str(users[input_u]) == input_p:
            st.session_state.is_logged_in = True
            st.session_state.username = input_u
            st.success("登录成功！")
            st.switch_page("pages/01_Main_App.py")
        else:
            st.error("用户名或密码错误")

with tab2:
    reg_user = st.text_input("创建用户名", key="reg_user_id")
    reg_pwd = st.text_input("创建密码", type="password", key="reg_pwd_id")
    if st.button("提交注册", use_container_width=True):
        # 此处可添加写入 data/users.json 的逻辑
        st.info("注册功能开发中...")