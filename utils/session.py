import streamlit as st

# 구름 문양 SVG (구름 두 개가 타일링)
_CLOUD_SVG = (
    "<svg xmlns='http://www.w3.org/2000/svg' width='240' height='160'>"
    "<g fill='%23F1C40F' fill-opacity='0.03' stroke='%23F1C40F' stroke-width='0.8' stroke-opacity='0.13'>"
    "<ellipse cx='70' cy='102' rx='56' ry='22'/>"
    "<ellipse cx='36' cy='83' rx='25' ry='23'/>"
    "<ellipse cx='58' cy='70' rx='23' ry='21'/>"
    "<ellipse cx='82' cy='65' rx='25' ry='23'/>"
    "<ellipse cx='106' cy='75' rx='21' ry='19'/>"
    "<ellipse cx='185' cy='32' rx='30' ry='13'/>"
    "<ellipse cx='164' cy='23' rx='17' ry='15'/>"
    "<ellipse cx='183' cy='15' rx='19' ry='16'/>"
    "<ellipse cx='201' cy='22' rx='15' ry='13'/>"
    "</g>"
    "</svg>"
)


def apply_theme():
    """전체 앱에 무당집 테마를 적용한다."""
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;700;900&display=swap');

        /* ── Deploy 버튼 숨기기 ── */
        [data-testid="stAppDeployButton"],
        [data-testid="stToolbar"],
        #MainMenu,
        header {{ visibility: hidden; }}

        /* ── 배경: 라디알 그라데이션 + 구름 패턴 ── */
        .stApp {{
            background: #0F081A !important;
        }}
        [data-testid="stAppViewContainer"] {{
            background:
                url("data:image/svg+xml,{_CLOUD_SVG}") repeat,
                radial-gradient(ellipse at 50% 28%, #2D1B4E 0%, #1A0F2E 48%, #0F081A 82%) !important;
            background-size: 240px 160px, cover !important;
            background-attachment: fixed, fixed !important;
        }}
        [data-testid="stSidebar"] {{
            background-color: #0A050F !important;
        }}
        .block-container {{
            background: transparent !important;
        }}

        /* ── 제목 폰트 & 금색 ── */
        h1 {{
            font-family: 'Noto Serif KR', serif !important;
            color: #F1C40F !important;
            text-shadow:
                0 0 18px rgba(241,196,15,0.7),
                0 0 40px rgba(241,196,15,0.3) !important;
            letter-spacing: 0.06em !important;
        }}
        h2, h3 {{
            font-family: 'Noto Serif KR', serif !important;
            color: #D4AF37 !important;
            letter-spacing: 0.04em !important;
        }}

        /* ── 본문 텍스트 ── */
        p, li, .stMarkdown p {{
            color: #E8D5B7 !important;
        }}
        label, .stRadio label, .stSelectbox label {{
            color: #D4AF37 !important;
            font-family: 'Noto Serif KR', serif !important;
        }}
        .stCaption, [data-testid="stCaptionContainer"] {{
            color: #A89060 !important;
        }}

        /* ── 입력 필드 ── */
        [data-testid="stTextInput"] input,
        [data-testid="stNumberInput"] input,
        .stSelectbox select {{
            background: rgba(26,15,46,0.8) !important;
            color: #E8D5B7 !important;
            border: 1px solid rgba(212,175,55,0.4) !important;
        }}
        [data-testid="stSlider"] {{
            color: #F1C40F !important;
        }}

        /* ── 정보 박스 ── */
        [data-testid="stInfo"] {{
            background: rgba(45,27,78,0.82) !important;
            border: 1px solid rgba(241,196,15,0.45) !important;
            color: #E8D5B7 !important;
        }}
        [data-testid="stSuccess"] {{
            background: rgba(15,50,25,0.85) !important;
            border: 1px solid rgba(100,200,100,0.5) !important;
        }}
        [data-testid="stWarning"] {{
            background: rgba(55,38,8,0.85) !important;
            border: 1px solid rgba(212,175,55,0.6) !important;
        }}
        [data-testid="stError"] {{
            background: rgba(55,10,10,0.85) !important;
            border: 1px solid rgba(200,50,50,0.6) !important;
        }}

        /* ── 버튼 ── */
        .stButton > button {{
            background: rgba(45,27,78,0.88) !important;
            color: #D4AF37 !important;
            border: 1px solid rgba(212,175,55,0.55) !important;
            font-family: 'Noto Serif KR', serif !important;
            transition: all 0.2s ease !important;
        }}
        .stButton > button:hover {{
            background: rgba(75,45,120,0.92) !important;
            border-color: rgba(241,196,15,0.85) !important;
            box-shadow: 0 0 14px rgba(241,196,15,0.4) !important;
            color: #F1C40F !important;
        }}
        .stButton > button[kind="primary"] {{
            background: linear-gradient(135deg, #5B2D8C 0%, #2D1B4E 100%) !important;
            color: #F1C40F !important;
            border: 1px solid rgba(241,196,15,0.7) !important;
            font-weight: 700 !important;
        }}
        .stButton > button[kind="primary"]:hover {{
            background: linear-gradient(135deg, #7040AA 0%, #3D2560 100%) !important;
            box-shadow: 0 0 20px rgba(241,196,15,0.55) !important;
        }}

        /* ── metric 카드 ── */
        [data-testid="stMetricValue"] {{
            color: #F1C40F !important;
            opacity: 1 !important;
        }}
        [data-testid="stMetricLabel"] {{
            color: #D4AF37 !important;
            opacity: 1 !important;
        }}

        /* ── 구분선 ── */
        hr {{
            border-color: rgba(212,175,55,0.35) !important;
        }}

        /* ── 왼쪽 navbar 완전 숨김 ── */
        [data-testid="stSidebarNav"],
        [data-testid="stSidebar"],
        [data-testid="collapsedControl"] {{
            display: none !important;
        }}
        </style>
    """, unsafe_allow_html=True)


def hide_deploy_button():
    apply_theme()

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
