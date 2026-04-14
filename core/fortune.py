from datetime import date

ZODIAC_ANIMALS = ["쥐", "소", "호랑이", "토끼", "용", "뱀", "말", "양", "원숭이", "닭", "개", "돼지"]
ZODIAC_SIGNS = ["염소자리", "물병자리", "물고기자리", "양자리", "황소자리", "쌍둥이자리",
                "게자리", "사자자리", "처녀자리", "천칭자리", "전갈자리", "사수자리"]

ZODIAC_RANGES = [
    (1, 20), (2, 19), (3, 21), (4, 20), (5, 21), (6, 21),
    (7, 23), (8, 23), (9, 23), (10, 23), (11, 22), (12, 22),
]


def get_zodiac_animal(birth_date: date) -> str:
    base_year = 2008  # 쥐띠 기준년도
    idx = (birth_date.year - base_year) % 12
    return ZODIAC_ANIMALS[idx]


def get_zodiac_sign(birth_date: date) -> str:
    month = birth_date.month
    day = birth_date.day
    cutoff_month, cutoff_day = ZODIAC_RANGES[month - 1]
    if day >= cutoff_day:
        sign_idx = month - 1
    else:
        sign_idx = (month - 2) % 12
    return ZODIAC_SIGNS[sign_idx]


def get_fortune_context(birth_date: date) -> dict:
    return {
        "zodiac_animal": get_zodiac_animal(birth_date),
        "zodiac_sign": get_zodiac_sign(birth_date),
    }
