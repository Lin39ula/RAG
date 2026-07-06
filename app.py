import streamlit as st
from backend.rag import ask

st.set_page_config(page_title="智能问答助手", page_icon="🤖")
st.title("🤖 我的第一个智能问答网页")

# 在侧边栏加个"上传文件"的占位
with st.sidebar:
    st.header("📁 知识库管理")
    st.info("等待上传文档...")

# 初始化聊天记录
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示历史聊天内容
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 接受用户输入
if prompt := st.chat_input("请问你想问什么？"):
    # 显示用户的问题
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("AI 正在检索知识库并思考中..."):
        try:
            response = ask(prompt)
        except Exception as e:
            response = f"【系统错误】后端调用失败，原因: {str(e)}"

    # 显示助手的回复
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})