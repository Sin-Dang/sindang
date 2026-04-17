import base64
import streamlit as st
from utils.session import init_session_state, get, set, is_input_complete, apply_theme
from utils.loading_image import generate_loading_gif
from core.survival_score import calculate_survival_score, get_survival_grade
from core.ai_shaman import generate_prediction


@st.cache_data(show_spinner=False)
def _cached_loading_gif() -> str:
    return base64.b64encode(generate_loading_gif()).decode()

st.set_page_config(page_title="예언 결과 | 벼락치기 무당", page_icon="🔮", layout="centered")
init_session_state()
apply_theme()

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

    loading_slot = st.empty()
    gif_b64 = _cached_loading_gif()
    loading_slot.markdown(
        f'<div style="text-align:center;padding:16px 0;">'
        f'<img src="data:image/gif;base64,{gif_b64}" '
        f'style="max-width:400px;width:100%;border-radius:16px;">'
        f'</div>',
        unsafe_allow_html=True,
    )

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
    except Exception as e:
        loading_slot.empty()
        st.error(f"AI 예언 생성 실패: {e}")
        st.stop()

    loading_slot.empty()

score = get("survival_score")
grade = get("survival_grade")
grade_label = get("survival_grade_label")
prediction = get("prediction_data") or {}

st.divider()
st.subheader(f"🎯 {get('user_name')}님의 학점 신내림 지수")

col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    st.metric("성적 점수", f"{score}점")
with col2:
    st.metric("등급", grade)
    st.caption(grade_label)
with col3:
    st.progress(int(score), text=f"{score}% 학점 상승 영험도")

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
