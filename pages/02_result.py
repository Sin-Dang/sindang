import streamlit as st
from utils.session import init_session_state, get, set, is_input_complete
from utils.loading_messages import get_all_messages
from core.survival_score import calculate_survival_score, get_survival_grade
from core.ai_shaman import generate_prediction

st.set_page_config(page_title="예언 결과 | 벼락치기 무당", page_icon="🔮", layout="centered")
init_session_state()

if not is_input_complete():
    st.warning("먼저 정보를 입력해주세요.")
    if st.button("입력 페이지로 이동"):
        st.switch_page("pages/01_input.py")
    st.stop()

st.title("🔮 Step 2: 무당의 예언")

# 생존 점수 계산 (캐시: session_state에 없을 때만)
if get("survival_score") is None:
    caffeine_total = get("americano_count") + get("energy_drink_count") * 1.5
    result = calculate_survival_score(
        time_remaining_min=get("time_remaining_min"),
        progress_pct=get("progress_pct"),
        known_pct=get("known_pct"),
        sleep_hours=get("sleep_hours"),
        americano_count=get("americano_count"),
        energy_drink_count=get("energy_drink_count"),
    )
    grade, grade_label = get_survival_grade(result["score"])
    set("survival_score", result["score"])
    set("survival_grade", grade)
    set("survival_grade_label", grade_label)
    set("score_detail", result)

    # AI 예언 생성
    with st.status("신령님을 깨우는 중...", expanded=True) as status:
        for msg in get_all_messages():
            st.write(msg)
        try:
            prediction = generate_prediction(
                user_name=get("user_name"),
                zodiac_animal=get("zodiac_animal"),
                zodiac_sign=get("zodiac_sign"),
                subject=get("subject"),
                time_remaining_min=get("time_remaining_min"),
                progress_pct=get("progress_pct"),
                known_pct=get("known_pct"),
                sleep_hours=get("sleep_hours"),
                caffeine_total=caffeine_total,
                survival_score=result["score"],
                survival_grade=grade,
            )
            set("prediction_data", prediction)
            status.update(label="예언 완료!", state="complete")
        except Exception as e:
            status.update(label="오류 발생", state="error")
            st.error(f"AI 예언 생성 실패: {e}")
            st.stop()

score = get("survival_score")
grade = get("survival_grade")
grade_label = get("survival_grade_label")
prediction = get("prediction_data") or {}

st.divider()
st.subheader(f"🎯 {get('user_name')}님의 시험 생존 확률")

col1, col2 = st.columns([1, 2])
with col1:
    st.metric("생존 점수", f"{score}점")
    st.metric("등급", f"{grade} — {grade_label}")
with col2:
    st.progress(int(score), text=f"{score}% 생존 가능성")

st.divider()

if prediction.get("prediction"):
    st.subheader("📜 무당의 예언")
    st.info(prediction["prediction"])

if prediction.get("today") or prediction.get("tomorrow") or prediction.get("this_week"):
    st.subheader("🗓️ 운세")
    tab1, tab2, tab3 = st.tabs(["오늘", "내일", "이번 주"])
    with tab1:
        st.write(prediction.get("today", ""))
    with tab2:
        st.write(prediction.get("tomorrow", ""))
    with tab3:
        st.write(prediction.get("this_week", ""))

st.divider()
if st.button("🧧 부적 생성하러 가기", use_container_width=True, type="primary"):
    st.switch_page("pages/03_charm.py")
if st.button("↩️ 다시 입력하기", use_container_width=True):
    st.switch_page("pages/01_input.py")
