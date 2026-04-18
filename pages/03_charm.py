import streamlit as st
from utils.session import init_session_state, get, set, is_result_ready, apply_theme
from core.ai_shaman import generate_charm_phrase
from charm.charm_generator import generate_charm_image

st.set_page_config(page_title="부적 생성 | 벼락치기 무당", page_icon="🧧", layout="centered")
init_session_state()
apply_theme()

if not is_result_ready():
    st.warning("먼저 예언을 확인해주세요.")
    if st.button("예언 페이지로 이동"):
        st.switch_page("pages/02_result.py")
    st.stop()

st.title("🧧 Step 3: 합격 부적 생성")
st.caption("조상님의 기운을 담은 맞춤 부적을 제작해 드립니다.")

if not get("charm_phrase"):
    with st.spinner("부적 문구 점지 중..."):
        try:
            phrase = generate_charm_phrase(
                user_name=get("user_name"),
                subject=get("subject"),
                survival_score=get("survival_score"),
            )
            set("charm_phrase", phrase)
        except Exception as e:
            st.error(f"부적 문구 생성 실패: {e}")
            st.stop()

charm_phrase = get("charm_phrase")
st.subheader("📝 부적 문구")
st.info(charm_phrase)

if not get("charm_image_bytes"):
    with st.spinner("부적 제작 중..."):
        try:
            img_bytes = generate_charm_image(
                user_name=get("user_name"),
                subject=get("subject"),
                phrases=charm_phrase.splitlines(),
                survival_score=get("survival_score"),
            )
            set("charm_image_bytes", img_bytes)
        except Exception as e:
            st.error(f"부적 이미지 생성 실패: {e}")
            st.stop()

img_bytes = get("charm_image_bytes")
if img_bytes:
    st.subheader("🖼️ 나만의 합격 부적")
    st.image(img_bytes, use_container_width=True)

    st.download_button(
        label="💾 부적 다운로드 (PNG)",
        data=img_bytes,
        file_name=f"{get('user_name')}_합격부적.png",
        mime="image/png",
        use_container_width=True,
        type="primary",
    )

st.divider()
if st.button("🔄 처음으로 돌아가기", use_container_width=True):
    st.switch_page("app.py")
