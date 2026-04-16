import streamlit as st
from datetime import date
from utils.session import init_session_state, set, apply_theme
from core.fortune import get_fortune_context

st.set_page_config(page_title="정보 입력 | 벼락치기 무당", page_icon="📋", layout="centered")
init_session_state()
apply_theme()

st.title("📋 Step 1: 운명 데이터 입력")
st.caption("정확할수록 예언의 정밀도가 높아집니다. (거짓말하면 조상님이 압니다)")
st.divider()

with st.form("input_form"):
    st.subheader("🧑 기본 신상 정보")
    user_name = st.text_input("이름", placeholder="홍길동")
    birth_date = st.date_input(
        "생년월일",
        value=date(2000, 1, 1),
        min_value=date(1950, 1, 1),
        max_value=date.today(),
    )

    st.divider()
    st.subheader("📚 시험 정보")
    subject = st.text_input("과목명", placeholder="예: 자료구조, 미적분학")
    time_remaining_hours = st.number_input(
        "시험 시작까지 남은 시간 (시간)",
        min_value=0, max_value=72, value=2, step=1,
    )

    st.divider()
    st.subheader("📖 공부 상태")
    progress_pct = st.slider("현재 진도율 (%)", 0, 100, 30)
    known_pct = st.slider("아는 내용 비중 (%)", 0, 100, 20)

    st.divider()
    st.subheader("💪 신체 컨디션")
    sleep_hours = st.number_input(
        "마지막 수면 시간 (시간)",
        min_value=0, max_value=24, value=5, step=1,
    )
    col1, col2 = st.columns(2)
    with col1:
        americano_count = st.number_input("아메리카노 ☕", min_value=0, max_value=20, value=1)
    with col2:
        energy_drink_count = st.number_input("에너지드링크 ⚡", min_value=0, max_value=20, value=0)

    submitted = st.form_submit_button("🔮 무당 호출하기", use_container_width=True, type="primary")

if submitted:
    if not user_name or not subject:
        st.error("이름과 과목명은 필수입니다.")
    else:
        fortune = get_fortune_context(birth_date)
        set("user_name", user_name)
        set("birth_date", birth_date)
        set("zodiac_animal", fortune["zodiac_animal"])
        set("zodiac_sign", fortune["zodiac_sign"])
        set("subject", subject)
        set("time_remaining_min", time_remaining_hours * 60)
        set("progress_pct", progress_pct)
        set("known_pct", known_pct)
        set("sleep_hours", sleep_hours)
        set("americano_count", americano_count)
        set("energy_drink_count", energy_drink_count)
        # 이전 결과 초기화
        set("survival_score", None)
        set("prediction_text", "")
        set("charm_phrase", "")
        set("charm_image_bytes", None)

        st.success(f"✅ {user_name}님의 데이터가 입력되었습니다. 예언을 기다리세요...")
        st.switch_page("pages/02_result.py")
