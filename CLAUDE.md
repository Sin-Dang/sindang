# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 개요

**"생존 확률 기반 벼락치기 무당"** — 유저의 시험 준비 데이터를 Gemini AI가 분석해 생존 확률과 무당 예언을 제공하는 Streamlit 웹 서비스. 유머러스한 AI 예언 + 공유용 부적 이미지 생성을 결합한 인터랙티브 서비스.

## 기술 스택

| 역할 | 기술 |
|------|------|
| 프레임워크 | Streamlit |
| AI API | Google Gemini 1.5 Flash |
| 이미지 생성(부적) | Pillow (PIL) |
| 언어 | Python 3.10+ |

## 실행 방법

```bash
pip install -r requirements.txt
streamlit run app.py
```

환경 변수 설정 (`.env`):
```
GEMINI_API_KEY=your_gemini_api_key_here
```

## 아키텍처 및 데이터 흐름

```
[pages/01_input.py]
    │  유저 입력 (신상/시험/공부/컨디션) → st.session_state에 저장
    ▼
[core/survival_score.py]
    │  입력값 → 생존 점수(0~100) 계산
    ▼
[core/ai_shaman.py]  ←──── Gemini 1.5 Flash API
    │  생존 점수 + 원본 입력 → 프롬프트 구성
    │  → 예언 텍스트 + 운세 + 부적 문구 반환
    ▼
[pages/02_result.py]  →  예언 텍스트 출력
    ▼
[pages/03_charm.py]
    │  charm/charm_generator.py → 부적 이미지 합성
    └─ 다운로드 / SNS 공유 버튼 제공
```

### 입력 데이터 (`pages/01_input.py`)
- 기본 신상: 이름, 생년월일 → 띠/별자리 자동 계산
- 시험 정보: 과목명, 남은 시간(분)
- 공부 상태: 진도율(%), 아는 내용 비중(%)
- 신체 컨디션: 수면 시간(h), 아메리카노/에너지드링크 섭취 수

### 생존 점수 계산 로직 (`core/survival_score.py`)

| 입력 변수 | 반영 방식 |
|-----------|-----------|
| 남은 시간(분) | 시간 대비 범위 비율로 압박 지수 계산 |
| 진도율(%) | 기본 점수에 직접 반영 |
| 아는 내용 비중(%) | 실질 이해도 보정 계수 적용 |
| 수면 시간(h) | 6시간 기준, 부족 시 페널티 |
| 카페인 섭취 | 2잔까지 보너스, 초과 시 페널티 |

카페인 페널티 로직은 과학적 근거보다 유머 우선 — 수치는 웃음 포인트에 맞게 조정 가능.

### AI 예언 시스템 (`core/ai_shaman.py`)

Gemini에게 "사주 전문가 겸 독설 무당" 페르소나를 부여해 두 가지를 생성:
1. **예언 텍스트**: 유저 상황을 비꼬거나 격려하는 예언문 + 오늘/내일/이번 주 운세
2. **부적 문구**: 유머러스한 합격 기원 문구 (예: "교수님 출제 오류 기원")

무당 페르소나의 일관성 유지가 핵심 — `system_instruction` 또는 프롬프트 첫 문단에 페르소나를 명확히 고정할 것.

### 세션 상태 관리 (`utils/session.py`)

Streamlit 멀티페이지 환경에서 `st.session_state` 키 충돌 방지를 위해 `utils/session.py`에서 중앙 관리.

### 부적 생성기 (`charm/charm_generator.py`)

`charm/assets/charm_template.png` 위에 AI 생성 문구를 한자/한글 혼합 레이아웃으로 합성 후 PNG로 출력. 한국어 렌더링을 위해 `charm/assets/fonts/`에 `.ttf` 폰트 파일 필수 (Nanum 계열 권장).
