import io
import os
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
TEMPLATE_PATH = os.path.join(ASSETS_DIR, "charm_template.png")
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")

# 기본 폰트 크기
TITLE_FONT_SIZE = 48
PHRASE_FONT_SIZE = 28
SCORE_FONT_SIZE = 22

# 부적 배경 색상 (템플릿 없을 때 폴백)
BG_COLOR = (180, 30, 30)
TEXT_COLOR = (255, 215, 0)
BORDER_COLOR = (255, 215, 0)


def _load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for font_file in ["NanumBrush.ttf", "NanumMyeongjo.ttf", "NanumGothic.ttf"]:
        path = os.path.join(FONTS_DIR, font_file)
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def _create_fallback_background(width: int, height: int) -> Image.Image:
    img = Image.new("RGB", (width, height), BG_COLOR)
    draw = ImageDraw.Draw(img)
    border = 12
    draw.rectangle([border, border, width - border, height - border],
                   outline=BORDER_COLOR, width=3)
    draw.rectangle([border + 8, border + 8, width - border - 8, height - border - 8],
                   outline=BORDER_COLOR, width=1)
    return img


def generate_charm_image(
    user_name: str,
    subject: str,
    phrases: list[str],
    survival_score: float,
    width: int = 400,
    height: int = 600,
) -> bytes:
    """부적 이미지를 생성하고 PNG bytes를 반환한다."""
    if os.path.exists(TEMPLATE_PATH):
        img = Image.open(TEMPLATE_PATH).convert("RGB").resize((width, height))
    else:
        img = _create_fallback_background(width, height)

    draw = ImageDraw.Draw(img)
    title_font = _load_font(TITLE_FONT_SIZE)
    phrase_font = _load_font(PHRASE_FONT_SIZE)
    score_font = _load_font(SCORE_FONT_SIZE)

    # 제목
    title = "합격부적"
    bbox = draw.textbbox((0, 0), title, font=title_font)
    tw = bbox[2] - bbox[0]
    draw.text(((width - tw) / 2, 60), title, font=title_font, fill=TEXT_COLOR)

    # 이름 + 과목
    sub_text = f"{user_name} · {subject}"
    bbox = draw.textbbox((0, 0), sub_text, font=score_font)
    sw = bbox[2] - bbox[0]
    draw.text(((width - sw) / 2, 130), sub_text, font=score_font, fill=TEXT_COLOR)

    # 구분선
    draw.line([(40, 170), (width - 40, 170)], fill=TEXT_COLOR, width=1)

    # 부적 문구
    y = 200
    for phrase in phrases[:3]:
        phrase = phrase.strip()
        if not phrase:
            continue
        bbox = draw.textbbox((0, 0), phrase, font=phrase_font)
        pw = bbox[2] - bbox[0]
        draw.text(((width - pw) / 2, y), phrase, font=phrase_font, fill=TEXT_COLOR)
        y += 60

    # 생존 점수
    draw.line([(40, height - 100), (width - 40, height - 100)], fill=TEXT_COLOR, width=1)
    score_text = f"생존 점수: {survival_score}점"
    bbox = draw.textbbox((0, 0), score_text, font=score_font)
    scw = bbox[2] - bbox[0]
    draw.text(((width - scw) / 2, height - 80), score_text, font=score_font, fill=TEXT_COLOR)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf.read()
