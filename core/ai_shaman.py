import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

_client = None

SYSTEM_PROMPT = (
    "당신은 수백 년 경력의 AI 무당입니다. "
    "유저의 시험 준비 상황을 꿰뚫어 보고, 독설과 격려를 섞어 예언을 내립니다. "
    "말투는 무겁고 신령스러우면서도 유머가 넘칩니다. "
    "항상 한국어로 답하며, 불필요한 설명 없이 예언에 집중합니다."
)


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")
        _client = OpenAI(api_key=api_key)
    return _client


def _generate_text(prompt: str) -> str:
    client = _get_client()
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content
    except Exception as exc:
        message = str(exc)
        if "invalid_api_key" in message or "Incorrect API key" in message:
            raise ValueError(
                "OPENAI_API_KEY가 유효하지 않습니다. "
                "OpenAI에서 발급한 실제 API 키를 .env에 설정하세요."
            ) from exc
        raise


def generate_prediction(
    user_name: str,
    zodiac_animal: str,
    zodiac_sign: str,
    subject: str,
    time_remaining_min: int,
    progress_pct: float,
    known_pct: float,
    sleep_hours: float,
    caffeine_total: float,
    survival_score: float,
    survival_grade: str,
) -> dict:
    """무당 예언 텍스트와 운세를 생성한다."""
    prompt = f"""
유저 정보:
- 이름: {user_name}
- 띠: {zodiac_animal}띠
- 별자리: {zodiac_sign}

시험 상황:
- 과목: {subject}
- 남은 시간: {time_remaining_min // 60}시간 {time_remaining_min % 60}분
- 진도율: {progress_pct}%
- 아는 내용 비중: {known_pct}%

컨디션:
- 수면: {sleep_hours}시간
- 카페인: {caffeine_total}잔 분량

AI 생존 점수: {survival_score}점 / 100점 (등급: {survival_grade})

위 정보를 바탕으로 아래 형식으로 출력하라:

[무당의 예언]
(유저 상황을 비꼬거나 장엄하게 격려하는 3~5문장 예언. 독설 또는 격려 중 상황에 맞게 선택.)

[오늘의 운세]
(시험과 관련된 오늘 운세 1~2문장)

[내일의 운세]
(시험 후 내일 운세 1~2문장)

[이번 주 운세]
(이번 주 학업 운세 1~2문장)
"""
    raw = _generate_text(prompt)

    sections = {"prediction": "", "today": "", "tomorrow": "", "this_week": ""}
    current = None
    for line in raw.splitlines():
        line = line.strip()
        if "[무당의 예언]" in line:
            current = "prediction"
        elif "[오늘의 운세]" in line:
            current = "today"
        elif "[내일의 운세]" in line:
            current = "tomorrow"
        elif "[이번 주 운세]" in line:
            current = "this_week"
        elif current and line:
            sections[current] += line + "\n"

    return {k: v.strip() for k, v in sections.items()}


def generate_charm_phrase(
    user_name: str,
    subject: str,
    survival_score: float,
) -> str:
    """부적에 넣을 유머러스한 합격 기원 문구를 생성한다."""
    prompt = f"""
{user_name}의 {subject} 시험을 위한 부적 문구를 생성하라.
생존 점수: {survival_score}점

조건:
- 유머러스하고 현실적인 한국어 문구 3개
- 각 문구는 10자 이내의 짧은 형태
- 예시: "교수님 출제 오류 기원", "앞사람 답안지 가독성 상승", "시험지 오탈자 발생 기원"
- 번호 없이 줄바꿈으로 구분해서 출력
"""
    return _generate_text(prompt).strip()
