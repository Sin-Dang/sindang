import io
import os
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
FONTS_DIR  = os.path.join(ASSETS_DIR, "fonts")


# ── 등급별 테마 ───────────────────────────────────────────────────────────────
THEMES = {
    "A": {
        "bg":     (255, 214,   0),   # 황금 노랑
        "c":      (200,  20,  20),   # 진한 빨강
        "header": ("행", "운"),
        "footer": ("합", "격"),
        "mood":   "triumphant",
    },
    "B": {
        "bg":     (255, 232,  55),   # 따뜻한 노랑
        "c":      (190,  40,  10),   # 주황빨강
        "header": ("행", "운"),
        "footer": ("합", "격"),
        "mood":   "happy",
    },
    "C": {
        "bg":     (235, 215, 115),   # 연한 황토
        "c":      (138,  72,   5),   # 황토 갈색
        "header": ("운", "명"),
        "footer": ("부", "적"),
        "mood":   "nervous",
    },
    "D": {
        "bg":     (145, 135, 105),   # 탁한 베이지
        "c":      ( 60,  28,   8),   # 어두운 갈색
        "header": ("수", "난"),
        "footer": ("부", "적"),
        "mood":   "sad",
    },
    "F": {
        "bg":     ( 18,  10,  10),   # 칠흑 검정
        "c":      (180,  20,  20),   # 핏빛 빨강
        "header": ("망", "했"),
        "footer": ("포", "기"),
        "mood":   "dead",
    },
}

GRADE_LABEL = {
    "A": "기적의 생존자",
    "B": "희망이 보인다",
    "C": "운에 맡겨라",
    "D": "조상님도 포기",
    "F": "이미 저세상",
}


# ── 폰트 ──────────────────────────────────────────────────────────────────────
def _load_font(size: int):
    for font_file in ["NanumBrush.ttf", "NanumMyeongjo.ttf", "NanumGothic.ttf"]:
        path = os.path.join(FONTS_DIR, font_file)
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                try:
                    return ImageFont.truetype(path, size, index=0)
                except Exception:
                    continue
    for sys_font in [
        "/System/Library/Fonts/AppleSDGothicNeo.ttc",
        "/System/Library/Fonts/Supplemental/AppleGothic.ttf",
        "/System/Library/Fonts/Supplemental/NotoSansGothic-Regular.ttf",
    ]:
        if os.path.exists(sys_font):
            try:
                return ImageFont.truetype(sys_font, size, index=0)
            except Exception:
                continue
    return ImageFont.load_default()


# ── 등급 도출 ─────────────────────────────────────────────────────────────────
def _derive_grade(score: float) -> str:
    if score >= 80:   return "A"
    elif score >= 60: return "B"
    elif score >= 40: return "C"
    elif score >= 20: return "D"
    else:             return "F"


# ── 장식 요소 ─────────────────────────────────────────────────────────────────
def _draw_heart(draw, cx, cy, size, color):
    r = size // 2
    draw.ellipse([cx - r, cy - r,  cx,      cy + r // 2], fill=color)
    draw.ellipse([cx,      cy - r,  cx + r,  cy + r // 2], fill=color)
    draw.polygon([(cx - r, cy + r // 3), (cx + r, cy + r // 3),
                  (cx, cy + r + r // 2)], fill=color)


def _draw_star4(draw, cx, cy, size, color):
    s, s3 = size, size // 3
    draw.polygon([
        (cx,      cy - s),  (cx + s3, cy - s3),
        (cx + s,  cy),      (cx + s3, cy + s3),
        (cx,      cy + s),  (cx - s3, cy + s3),
        (cx - s,  cy),      (cx - s3, cy - s3),
    ], fill=color)


def _draw_clover(draw, cx, cy, size, color):
    r = size // 2
    for dx, dy in [(0, -r), (r, 0), (0, r), (-r, 0)]:
        draw.ellipse([cx + dx - r//2, cy + dy - r//2,
                      cx + dx + r//2, cy + dy + r//2], fill=color)
    draw.line([cx, cy + r//2, cx, cy + size], fill=color, width=max(2, size // 8))


def _draw_sparkle(draw, cx, cy, size, color):
    w  = max(2, size // 4)
    s2 = int(size * 0.65)
    draw.line([cx - size, cy,       cx + size, cy],       fill=color, width=w)
    draw.line([cx,        cy - size, cx,       cy + size], fill=color, width=w)
    draw.line([cx - s2,   cy - s2,  cx + s2,  cy + s2],  fill=color, width=max(1, w - 1))
    draw.line([cx + s2,   cy - s2,  cx - s2,  cy + s2],  fill=color, width=max(1, w - 1))


def _draw_plus(draw, cx, cy, size, color):
    w = max(2, size // 3)
    draw.line([cx - size, cy, cx + size, cy], fill=color, width=w)
    draw.line([cx, cy - size, cx, cy + size], fill=color, width=w)


def _draw_x_mark(draw, cx, cy, size, color):
    lw = max(3, size // 3)
    s  = int(size * 0.7)
    draw.line([cx - s, cy - s, cx + s, cy + s], fill=color, width=lw)
    draw.line([cx + s, cy - s, cx - s, cy + s], fill=color, width=lw)


def _draw_skull(draw, cx, cy, size, color, bg):
    r = size
    draw.ellipse([cx - r, cy - r, cx + r, cy + int(r * 0.7)], fill=color)
    er = max(2, r // 4)
    for ex, ey in [(cx - r // 3, cy - r // 6), (cx + r // 3, cy - r // 6)]:
        draw.ellipse([ex - er, ey - er, ex + er, ey + er], fill=bg)
    nr = max(1, r // 7)
    draw.ellipse([cx - nr, cy + r//5 - nr, cx + nr, cy + r//5 + nr], fill=bg)
    ty = cy + int(r * 0.55)
    tw = r // 3
    th = max(3, r // 4)
    draw.rectangle([cx - tw * 2, ty, cx + tw * 2, ty + th], fill=color)
    for tx in range(cx - tw * 2 + tw // 2, cx + tw * 2, tw):
        draw.rectangle([tx, ty, tx + tw // 2, ty + th], fill=bg)


def _draw_lightning(draw, cx, cy, size, color):
    lw = max(2, size // 5)
    draw.line([
        (cx + size // 3, cy - size),
        (cx - size // 6, cy),
        (cx + size // 3, cy),
        (cx - size // 3, cy + size),
    ], fill=color, width=lw)


def _draw_tombstone(draw, cx, cy, w, h, color, bg):
    lw = 3
    draw.rectangle([cx - w//2, cy - h//3, cx + w//2, cy + h//2],
                   outline=color, fill=bg, width=lw)
    draw.arc([cx - w//2, cy - h, cx + w//2, cy - h//3 + w//2],
             180, 0, fill=color, width=lw)
    draw.line([cx, cy - h//3, cx, cy + h//4], fill=color, width=lw)
    draw.line([cx - w//4, cy - h//6, cx + w//4, cy - h//6], fill=color, width=lw)


def _draw_crown(draw, cx, cy, w, h, color):
    draw.polygon([
        (cx - w//2, cy + h//2), (cx - w//2, cy),
        (cx - w//4, cy - h//3), (cx,         cy),
        (cx + w//4, cy - h//3), (cx + w//2,  cy),
        (cx + w//2, cy + h//2),
    ], fill=color)


def _draw_tear(draw, cx, cy, size, color):
    draw.ellipse([cx - size, cy, cx + size, cy + size * 2], fill=color)
    draw.polygon([(cx - size, cy + size), (cx + size, cy + size), (cx, cy - size // 2)],
                 fill=color)


def _draw_sweat(draw, cx, cy, size, color):
    _draw_tear(draw, cx, cy, size, color)


# ── 테두리 ────────────────────────────────────────────────────────────────────
def _draw_border(draw, width, height, grade, c, bg):
    if grade == "A":
        draw.rectangle([10, 10, width - 10, height - 10], outline=c, width=6)
        draw.rectangle([20, 20, width - 20, height - 20], outline=c, width=2)
        draw.rectangle([27, 27, width - 27, height - 27], outline=c, width=1)
        cs = 46
        for bx, by in [(10, 10), (width-10, 10), (10, height-10), (width-10, height-10)]:
            draw.arc([bx-cs, by-cs, bx+cs, by+cs], 0, 360, fill=c, width=3)

    elif grade == "B":
        draw.rectangle([12, 12, width-12, height-12], outline=c, width=5)
        draw.rectangle([22, 22, width-22, height-22], outline=c, width=2)
        cs = 40
        for bx, by in [(12, 12), (width-12, 12), (12, height-12), (width-12, height-12)]:
            draw.arc([bx-cs, by-cs, bx+cs, by+cs], 0, 360, fill=c, width=2)

    elif grade == "C":
        draw.rectangle([12, 12, width-12, height-12], outline=c, width=4)
        draw.rectangle([22, 22, width-22, height-22], outline=c, width=1)

    elif grade == "D":
        draw.rectangle([12, 12, width-12, height-12], outline=c, width=3)
        notch = 22
        for bx, by, dx, dy in [
            (12, 12, 1, 1), (width-12, 12, -1, 1),
            (12, height-12, 1, -1), (width-12, height-12, -1, -1),
        ]:
            draw.line([bx, by, bx + dx*notch, by + dy*notch], fill=bg, width=6)

    elif grade == "F":
        m, amp, step = 12, 8, 22
        def zigzag_h(y_base, flip=False):
            pts = []
            toggle = 1
            x = m
            while x <= width - m:
                pts.append((x, y_base + toggle * amp * (1 if not flip else -1)))
                x += step
                toggle *= -1
            pts.append((width - m, y_base))
            return pts

        def zigzag_v(x_base, flip=False):
            pts = []
            toggle = 1
            y = m
            while y <= height - m:
                pts.append((x_base + toggle * amp * (1 if not flip else -1), y))
                y += step
                toggle *= -1
            pts.append((x_base, height - m))
            return pts

        lw = 4
        draw.line(zigzag_h(m),         fill=c, width=lw)
        draw.line(zigzag_h(height - m, flip=True), fill=c, width=lw)
        draw.line(zigzag_v(m),         fill=c, width=lw)
        draw.line(zigzag_v(width - m, flip=True),  fill=c, width=lw)


# ── 고양이 얼굴 ───────────────────────────────────────────────────────────────
def _draw_cat(draw, cx, cy, r, c, bg, mood):
    lw  = max(3, r // 20)
    ex_off = r // 3
    ey     = cy - r // 5

    # 얼굴 원
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=c, width=lw)

    # 귀
    ear = r // 2
    for side in (-1, 1):
        ear_pts = [
            (cx + side * 8,        cy - r + 10),
            (cx + side * (r // 2), cy - r - ear),
            (cx + side * (r - 8),  cy - r + 10),
        ]
        draw.polygon(ear_pts, fill=bg)
        draw.line(ear_pts + [ear_pts[0]], fill=c, width=lw)

    if mood in ("triumphant", "happy"):
        # ^ ^ 초승달 눈
        arc_r = r // 5
        for side in (-1, 1):
            ex = cx + side * ex_off
            draw.arc([ex - arc_r, ey - arc_r, ex + arc_r, ey + arc_r],
                     200, 340, fill=c, width=lw + 1)
        # 활짝 웃는 입
        sm = r // 2
        draw.arc([cx - sm, cy + 5, cx + sm, cy + sm + 15], 15, 165, fill=c, width=lw)
        # 볼 홍조 (작은 원)
        br = r // 7
        for side in (-1, 1):
            bx = cx + side * (r * 2 // 3)
            draw.ellipse([bx - br, cy + r//5 - br, bx + br, cy + r//5 + br], fill=c)
        # S등급 눈에 별 추가
        if mood == "triumphant":
            for side in (-1, 1):
                _draw_star4(draw, cx + side * ex_off, ey - r // 8, 5, c)

    elif mood == "nervous":
        # 동그랗고 약간 큰 눈
        er = max(5, r // 7)
        for side in (-1, 1):
            draw.ellipse([cx + side*ex_off - er, ey - er,
                          cx + side*ex_off + er, ey + er], fill=c)
        # 코
        nr = max(3, r // 12)
        draw.ellipse([cx - nr, cy + r//6 - nr, cx + nr, cy + r//6 + nr], fill=c)
        # W 형태 불안한 입
        step_w = r // 4
        my = cy + r // 3
        mouth_pts = [(cx - step_w*2, my),
                     (cx - step_w,   my - r//10),
                     (cx,            my),
                     (cx + step_w,   my - r//10),
                     (cx + step_w*2, my)]
        draw.line(mouth_pts, fill=c, width=lw)
        # 땀방울
        _draw_sweat(draw, cx + r * 3//4, cy - r//2, max(3, r//10), c)
        # 수염
        wy = cy + r // 8
        for side in (-1, 1):
            for dy in (-r//12, r//12):
                draw.line([cx + side*(r//4 + r//2), wy + dy,
                           cx + side * r//4,         wy],
                          fill=c, width=max(1, lw - 1))

    elif mood == "sad":
        # 처진 눈 (슬픈 호)
        arc_r = r // 5
        for side in (-1, 1):
            ex = cx + side * ex_off
            draw.arc([ex - arc_r, ey - arc_r//2, ex + arc_r, ey + arc_r + arc_r//2],
                     20, 160, fill=c, width=lw + 1)
        # 코
        nr = max(3, r // 12)
        draw.ellipse([cx - nr, cy + r//6 - nr, cx + nr, cy + r//6 + nr], fill=c)
        # 입꼬리 내려간 입
        sm = r // 3
        draw.arc([cx - sm, cy + r//5, cx + sm, cy + r//5 + sm], 200, 340, fill=c, width=lw)
        # 눈물
        _draw_tear(draw, cx - ex_off + r//8, ey + arc_r, max(3, r//12), c)
        # 수염
        wy = cy + r // 8
        for side in (-1, 1):
            for dy in (-r//12, r//12):
                draw.line([cx + side*(r//4 + r//2), wy + dy,
                           cx + side * r//4,         wy],
                          fill=c, width=max(1, lw - 1))

    elif mood == "dead":
        # X X 눈
        for side in (-1, 1):
            _draw_x_mark(draw, cx + side * ex_off, ey, r // 7, c)
        # 코
        nr = max(3, r // 12)
        draw.ellipse([cx - nr, cy + r//6 - nr, cx + nr, cy + r//6 + nr], fill=c)
        # 구불구불한 괴로운 입
        pts = []
        for i in range(7):
            x = cx - r//2 + i * (r // 6)
            y = cy + r//3 + (r//12) * (1 if i % 2 == 0 else -1)
            pts.append((x, y))
        draw.line(pts, fill=c, width=lw)
        # 눈물 두 방울
        for side in (-1, 1):
            _draw_tear(draw, cx + side*ex_off + side*(r//8),
                       ey + r//8, max(3, r//10), c)
        # 귀 안에 X
        for side in (-1, 1):
            _draw_x_mark(draw, cx + side * r//2, cy - r - r//4, max(3, r//12), c)


# ── 사이드 장식 (등급별) ──────────────────────────────────────────────────────
def _draw_side_deco(draw, width, grade, c, bg):
    side_x = [46, width - 46]

    if grade == "A":
        ys = [175, 240, 295, 340, 400, 460]
        funcs = [
            lambda x, y: _draw_star4(draw, x, y, 10, c),
            lambda x, y: _draw_sparkle(draw, x, y, 13, c),
            lambda x, y: _draw_star4(draw, x, y, 9, c),
            lambda x, y: _draw_heart(draw, x, y, 15, c),
            lambda x, y: _draw_clover(draw, x, y, 18, c),
            lambda x, y: _draw_heart(draw, x, y, 11, c),
        ]
        for sx in side_x:
            for y, fn in zip(ys, funcs):
                fn(sx, y)

    elif grade == "B":
        ys    = [175, 245, 335, 415]
        funcs = [
            lambda x, y: _draw_plus(draw, x, y, 9, c),
            lambda x, y: _draw_sparkle(draw, x, y, 12, c),
            lambda x, y: _draw_heart(draw, x, y, 14, c),
            lambda x, y: _draw_clover(draw, x, y, 16, c),
        ]
        for sx in side_x:
            for y, fn in zip(ys, funcs):
                fn(sx, y)

    elif grade == "C":
        for sx in side_x:
            _draw_plus(draw, sx, 175, 9, c)
            _draw_plus(draw, sx, 248, 12, c)
            _draw_plus(draw, sx, 415, 10, c)
        # 한쪽은 하트, 반대쪽은 X
        _draw_heart(draw,  side_x[0], 335, 12, c)
        _draw_x_mark(draw, side_x[1], 335, 12, c)

    elif grade == "D":
        for sx in side_x:
            _draw_x_mark(draw,    sx, 175, 10, c)
            _draw_skull(draw,     sx, 248, 14, c, bg)
            _draw_lightning(draw, sx, 340, 18, c)
            _draw_skull(draw,     sx, 420, 12, c, bg)

    elif grade == "F":
        for sx in side_x:
            _draw_x_mark(draw,    sx, 175, 12, c)
            _draw_skull(draw,     sx, 248, 16, c, bg)
            _draw_tombstone(draw, sx, 360, 28, 36, c, bg)
            _draw_lightning(draw, sx, 435, 18, c)
            _draw_skull(draw,     sx, 492, 10, c, bg)


# ── 상단 중앙 장식 ────────────────────────────────────────────────────────────
def _draw_header_deco(draw, cx, grade, c, bg):
    if grade == "A":
        _draw_heart(draw,    cx - 28, 58,  12, c)
        _draw_star4(draw,    cx,      46,  11, c)
        _draw_sparkle(draw,  cx + 30, 62,   8, c)
        _draw_plus(draw,     cx - 65, 78,   8, c)
        _draw_sparkle(draw,  cx + 68, 80,   7, c)
    elif grade == "B":
        _draw_heart(draw,   cx - 25, 60, 11, c)
        _draw_star4(draw,   cx,      48, 10, c)
        _draw_sparkle(draw, cx + 28, 63,  8, c)
    elif grade == "C":
        _draw_plus(draw,  cx - 30, 62, 9, c)
        _draw_plus(draw,  cx + 30, 62, 9, c)
        _draw_star4(draw, cx,      50, 8, c)
    elif grade == "D":
        _draw_x_mark(draw,    cx - 30, 62, 10, c)
        _draw_x_mark(draw,    cx + 30, 62, 10, c)
        _draw_lightning(draw, cx,      50, 12, c)
    elif grade == "F":
        _draw_skull(draw, cx - 38, 62, 12, c, bg)
        _draw_skull(draw, cx + 38, 62, 12, c, bg)
        _draw_skull(draw, cx,      50, 10, c, bg)


# ── 하단 중앙 장식 ────────────────────────────────────────────────────────────
def _draw_footer_deco(draw, cx, cy, grade, c, bg):
    if grade == "A":
        _draw_clover(draw,  cx,       cy,      22, c)
        _draw_heart(draw,   cx - 58,  cy + 12, 12, c)
        _draw_heart(draw,   cx + 58,  cy + 12, 12, c)
        _draw_star4(draw,   cx - 88,  cy,       9, c)
        _draw_star4(draw,   cx + 88,  cy,       9, c)
    elif grade == "B":
        _draw_clover(draw, cx,      cy,      20, c)
        _draw_heart(draw,  cx - 54, cy + 10, 11, c)
        _draw_heart(draw,  cx + 54, cy + 10, 11, c)
    elif grade == "C":
        _draw_clover(draw, cx,      cy,      18, c)
        _draw_plus(draw,   cx - 50, cy + 10, 10, c)
        _draw_plus(draw,   cx + 50, cy + 10, 10, c)
    elif grade == "D":
        _draw_skull(draw,     cx,       cy - 5,  16, c, bg)
        _draw_lightning(draw, cx - 52,  cy + 10, 14, c)
        _draw_lightning(draw, cx + 52,  cy + 10, 14, c)
    elif grade == "F":
        _draw_skull(draw, cx,       cy - 5,  18, c, bg)
        _draw_skull(draw, cx - 58,  cy + 5,  10, c, bg)
        _draw_skull(draw, cx + 58,  cy + 5,  10, c, bg)


# ── 메인 생성 함수 ────────────────────────────────────────────────────────────
def generate_charm_image(
    user_name: str,
    subject: str,
    phrases: list[str],
    survival_score: float,
    survival_grade: str | None = None,
    width: int = 420,
    height: int = 630,
) -> bytes:
    grade = (survival_grade or _derive_grade(survival_score)).upper()
    if grade not in THEMES:
        grade = "B"

    theme = THEMES[grade]
    bg    = theme["bg"]
    c     = theme["c"]
    mood  = theme["mood"]

    img  = Image.new("RGB", (width, height), bg)
    draw = ImageDraw.Draw(img)

    f_big   = _load_font(64)
    f_med   = _load_font(26)
    f_tiny  = _load_font(17)

    # ── 테두리 ──
    _draw_border(draw, width, height, grade, c, bg)

    # ── 상단 헤더 텍스트 ──
    h_left, h_right = theme["header"]
    draw.text((42, 34), h_left, font=f_big, fill=c)
    bbox = draw.textbbox((0, 0), h_right, font=f_big)
    draw.text((width - 42 - (bbox[2] - bbox[0]), 34), h_right, font=f_big, fill=c)

    _draw_header_deco(draw, width // 2, grade, c, bg)

    # A등급에만 왕관
    if grade == "A":
        _draw_crown(draw, width // 2, 28, 40, 22, c)

    # ── AI 생성 첫 번째 문구 ──
    p0 = phrases[0].strip() if phrases else f"{subject} 합격 기원"
    bbox = draw.textbbox((0, 0), p0, font=f_med)
    draw.text(((width - (bbox[2] - bbox[0])) // 2, 116), p0, font=f_med, fill=c)

    draw.line([48, 155, width - 48, 155], fill=c, width=2)

    # ── 고양이 ──
    _draw_cat(draw, width // 2, 295, 88, c, bg, mood)

    # ── 사이드 장식 ──
    _draw_side_deco(draw, width, grade, c, bg)

    # ── AI 생성 2·3번째 문구 ──
    for i, py in [(1, 438), (2, 466)]:
        if i < len(phrases) and phrases[i].strip():
            p = phrases[i].strip()
            bbox = draw.textbbox((0, 0), p, font=f_tiny)
            draw.text(((width - (bbox[2] - bbox[0])) // 2, py), p, font=f_tiny, fill=c)

    draw.line([48, 494, width - 48, 494], fill=c, width=2)

    # ── 하단 푸터 텍스트 ──
    f_left, f_right = theme["footer"]
    draw.text((48, 504), f_left, font=f_big, fill=c)
    bbox = draw.textbbox((0, 0), f_right, font=f_big)
    draw.text((width - 48 - (bbox[2] - bbox[0]), 504), f_right, font=f_big, fill=c)

    _draw_footer_deco(draw, width // 2, 540, grade, c, bg)

    # ── 이름·과목·등급·점수 ──
    info = f"{user_name} · {subject} · {GRADE_LABEL.get(grade, '')} ({survival_score:.0f}점)"
    bbox = draw.textbbox((0, 0), info, font=f_tiny)
    draw.text(((width - (bbox[2] - bbox[0])) // 2, 574), info, font=f_tiny, fill=c)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf.read()
