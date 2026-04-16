def calculate_survival_score(
    time_remaining_min: int,
    progress_pct: float,
    known_pct: float,
    sleep_hours: float,
    americano_count: int,
    energy_drink_count: int,
) -> dict:
    """입력값을 기반으로 생존 점수(0~100)와 구성 요소를 반환한다."""

    # 1. 기본 점수: 진도율 + 이해도 가중 평균
    base_score = progress_pct * 0.5 + known_pct * 0.5

    # 2. 시간 압박 페널티
    # 남은 시간이 60분 미만이면 급격히 감소
    if time_remaining_min >= 180:
        time_modifier = 1.0
    elif time_remaining_min >= 60:
        time_modifier = 0.7 + (time_remaining_min - 60) / 400
    else:
        time_modifier = max(0.2, time_remaining_min / 300)

    # 3. 수면 보정
    if sleep_hours >= 7:
        sleep_modifier = 1.05
    elif sleep_hours >= 5:
        sleep_modifier = 1.0
    elif sleep_hours >= 3:
        sleep_modifier = 0.85
    else:
        sleep_modifier = 0.65

    # 4. 카페인 보정
    total_caffeine = americano_count + energy_drink_count * 1.5
    if total_caffeine <= 2:
        caffeine_modifier = 1.0 + total_caffeine * 0.03
    else:
        # 초과분 "뇌세포 침식" 페널티
        caffeine_modifier = 1.06 - (total_caffeine - 2) * 0.08
        caffeine_modifier = max(0.5, caffeine_modifier)

    score = base_score * time_modifier * sleep_modifier * caffeine_modifier
    score = round(min(100.0, max(0.0, score)), 1)

    return {
        "score": score,
        "base_score": round(base_score, 1),
        "time_modifier": round(time_modifier, 2),
        "sleep_modifier": round(sleep_modifier, 2),
        "caffeine_modifier": round(caffeine_modifier, 2),
    }


def get_survival_grade(score: float) -> tuple[str, str]:
    """점수에 따른 등급과 한줄 평을 반환한다."""
    if score >= 80:
        return "A", "기적의 생존자"
    elif score >= 60:
        return "B", "희망이 보인다"
    elif score >= 40:
        return "C", "운에 맡겨라"
    elif score >= 20:
        return "D", "조상님도 포기"
    else:
        return "F", "이미 저세상"
