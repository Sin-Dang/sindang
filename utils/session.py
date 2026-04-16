import streamlit as st


def hide_deploy_button():
    st.markdown("""
        <style>
        [data-testid="stAppDeployButton"],
        [data-testid="stToolbar"],
        #MainMenu,
        header { visibility: hidden; }
        </style>
    """, unsafe_allow_html=True)

SESSION_KEYS = {
    "user_name": "",
    "birth_date": None,
    "zodiac_animal": "",
    "zodiac_sign": "",
    "subject": "",
    "time_remaining_min": 0,
    "progress_pct": 0,
    "known_pct": 0,
    "sleep_hours": 0.0,
    "americano_count": 0,
    "energy_drink_count": 0,
    "survival_score": None,
    "prediction_text": "",
    "fortune_text": "",
    "charm_phrase": "",
    "charm_image_bytes": None,
}


def init_session_state():
    for key, default in SESSION_KEYS.items():
        if key not in st.session_state:
            st.session_state[key] = default


def get(key: str):
    return st.session_state.get(key, SESSION_KEYS.get(key))


def set(key: str, value):
    st.session_state[key] = value


def is_input_complete() -> bool:
    return bool(
        st.session_state.get("user_name")
        and st.session_state.get("birth_date")
        and st.session_state.get("subject")
    )


def is_result_ready() -> bool:
    return st.session_state.get("survival_score") is not None
