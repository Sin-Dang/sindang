import random

LOADING_MESSAGES = [
    "조상님 접신 중...",
    "작두 타는 중...",
    "카페인 농도 측정 중...",
    "내세의 성적표 열람 중...",
    "교수님 마음 훔쳐보는 중...",
    "사주팔자 대조 중...",
    "신령님 깨우는 중...",
    "전생 성적표 열람 중...",
    "시험지 미리보기 시도 중...",
    "운명의 실 꼬는 중...",
]


def get_random_message() -> str:
    return random.choice(LOADING_MESSAGES)


def get_all_messages() -> list[str]:
    return LOADING_MESSAGES
