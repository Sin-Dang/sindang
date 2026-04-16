import streamlit as st
from utils.session import init_session_state, hide_deploy_button

st.set_page_config(
    page_title="벼락치기 무당",
    page_icon="🔮",
    layout="centered",
    initial_sidebar_state="collapsed",
)

init_session_state()
hide_deploy_button()

st.title("🔮 벼락치기 무당")
st.subheader("시험 생존 확률 예언 서비스")

st.markdown("""
> **조상님이 당신의 처참한 시험 준비 상황을 꿰뚫어 보고 있습니다.**

당신의 시험 정보를 입력하면, AI 무당이 생존 확률과 예언을 내려드립니다.
""")

st.divider()

col1, col2, col3 = st.columns(3)
with col1:
    st.info("**Step 1**\n\n📋 정보 입력")
with col2:
    st.info("**Step 2**\n\n🔮 AI 예언 확인")
with col3:
    st.info("**Step 3**\n\n🧧 부적 생성")

st.divider()

if st.button("🚀 운명 감정 시작하기", use_container_width=True, type="primary"):
    st.switch_page("pages/01_input.py")
