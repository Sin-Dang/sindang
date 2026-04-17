import io
import math
import os
from PIL import Image, ImageDraw, ImageFont

_FONTS_DIR = os.path.join(os.path.dirname(__file__), "..", "charm", "assets", "fonts")


def _font(size: int) -> ImageFont.FreeTypeFont:
    for name in ("NanumBrush.ttf", "NanumMyeongjo.ttf", "NanumGothic.ttf"):
        try:
            return ImageFont.truetype(os.path.join(_FONTS_DIR, name), size)
        except Exception:
            pass
    return ImageFont.load_default()


def _draw_frame(bounce: int, flame_mult: float) -> Image.Image:
    W, H = 400, 500
    img = Image.new("RGB", (W, H), (15, 8, 26))
    draw = ImageDraw.Draw(img)
    cx = W // 2

    # ── 배경 보랏빛 글로우 ──
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for r in range(150, 0, -10):
        a = int(45 * (1 - r / 150))
        od.ellipse([cx - r, 190 - r, cx + r, 190 + r], fill=(80, 35, 120, a))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # ── 별 장식 ──
    for sx, sy in [(38,42),(362,58),(22,178),(375,138),(65,308),(328,285),
                   (142,398),(258,390),(92,108),(308,102),(178,52),(222,455)]:
        draw.ellipse([sx-2, sy-2, sx+2, sy+2], fill=(241, 196, 15))

    # ── 캐릭터 (bounce 로 통통 움직임) ──
    cy = 162 + bounce

    # 치마
    draw.ellipse([cx-76, cy+34, cx+76, cy+150], fill=(195, 42, 65))
    for i in range(8):
        x = cx - 66 + i * 19
        draw.ellipse([x-7, cy+135, x+7, cy+151], fill=(241, 196, 15))

    # 몸/머리 (크림색)
    draw.ellipse([cx-60, cy-86, cx+60, cy+52], fill=(255, 250, 232))

    # 토끼 귀
    draw.ellipse([cx-55, cy-106, cx-28, cy-62], fill=(255, 250, 232))
    draw.ellipse([cx+28, cy-106, cx+55, cy-62], fill=(255, 250, 232))
    draw.ellipse([cx-51, cy-102, cx-32, cy-67], fill=(255, 180, 192))
    draw.ellipse([cx+32, cy-102, cx+51, cy-67], fill=(255, 180, 192))

    # 저고리
    draw.ellipse([cx-66, cy+10, cx+66, cy+80], fill=(228, 92, 112))

    # 노리개
    draw.polygon([
        (cx-7, cy+20),(cx+7, cy+20),
        (cx+4, cy+48),(cx, cy+54),(cx-4, cy+48),
    ], fill=(241, 196, 15))

    # 왼팔
    draw.ellipse([cx-102, cy+16, cx-40, cy+52], fill=(228, 92, 112))
    # 부채
    fan_cx, fan_cy = cx-114, cy+18
    cols = [(0,168,84),(30,200,108),(0,152,72),(20,188,98),(0,168,84),(30,200,108)]
    for i in range(6):
        ang = math.radians(138 + i * 16)
        x2 = fan_cx + int(42 * math.cos(ang))
        y2 = fan_cy + int(42 * math.sin(ang))
        draw.line([(fan_cx, fan_cy), (x2, y2)], fill=cols[i], width=5)
        draw.line([(fan_cx, fan_cy), (x2, y2)], fill=(110, 85, 30), width=1)
    draw.ellipse([fan_cx-5, fan_cy-5, fan_cx+5, fan_cy+5], fill=(200, 162, 42))

    # 오른팔
    draw.ellipse([cx+40, cy+16, cx+102, cy+52], fill=(228, 92, 112))
    # 방울
    bx, by = cx+114, cy+18
    draw.ellipse([bx-11, by-11, bx+11, by+11], fill=(208, 172, 44))
    draw.line([(bx, by+11),(bx, by+23)], fill=(208, 172, 44), width=2)
    draw.ellipse([bx-6, by+21, bx+6, by+31], fill=(208, 172, 44))

    # 화관
    crown = [
        (cx-30, cy-84),(cx-22, cy-100),
        (cx-11, cy-86),(cx, cy-104),
        (cx+11, cy-86),(cx+22, cy-100),
        (cx+30, cy-84),
    ]
    draw.polygon(crown, fill=(241, 196, 15))
    draw.ellipse([cx-5, cy-109, cx+5, cy-99], fill=(218, 48, 48))

    # 눈 (초승달)
    draw.arc([cx-43, cy-56, cx-16, cy-30], 0, 180, fill=(40, 25, 15), width=4)
    draw.arc([cx+16, cy-56, cx+43, cy-30], 0, 180, fill=(40, 25, 15), width=4)

    # 볼터치
    draw.ellipse([cx-54, cy-27, cx-28, cy-11], fill=(255, 150, 150))
    draw.ellipse([cx+28, cy-27, cx+54, cy-11], fill=(255, 150, 150))

    # 미소
    draw.arc([cx-22, cy-20, cx+22, cy+8], 0, 180, fill=(40, 25, 15), width=3)

    # ── 작두 ──
    blade_y = cy + 160 - bounce
    blade_pts = [
        (cx-142, blade_y),(cx+142, blade_y),
        (cx+142, blade_y+14),(cx+158, blade_y+7),
        (cx+142, blade_y+22),
        (cx-142, blade_y+22),(cx-158, blade_y+7),
    ]
    draw.polygon(blade_pts, fill=(162, 168, 188))
    draw.line([(cx-132, blade_y+3),(cx+132, blade_y+3)], fill=(228, 234, 252), width=2)
    draw.line([(cx-132, blade_y),(cx+132, blade_y)],     fill=(245, 248, 255), width=1)
    draw.rectangle([cx-158, blade_y, cx-140, blade_y+22], fill=(138, 98, 42))
    draw.rectangle([cx+140, blade_y, cx+158, blade_y+22], fill=(138, 98, 42))

    # ── 불꽃 ──
    fb_y = blade_y + 22
    flame_defs = [
        (cx-108, 24),(cx-78, 36),(cx-48, 30),
        (cx-18, 46),(cx+12, 40),(cx+42, 33),
        (cx+72, 38),(cx+102, 26),
    ]
    for fx, fh_base in flame_defs:
        fh = int(fh_base * flame_mult)
        draw.ellipse([fx-13, fb_y, fx+13, fb_y+fh],           fill=(255, 72, 0))
        draw.ellipse([fx-8,  fb_y+2, fx+8, fb_y+max(1,fh-7)], fill=(255, 200, 28))

    # ── 텍스트 박스 ──
    ty = fb_y + 52
    draw.rounded_rectangle([cx-178, ty-6, cx+178, ty+32], radius=8, fill=(33, 14, 52))
    draw.rounded_rectangle([cx-178, ty-6, cx+178, ty+32], radius=8,
                            outline=(212, 175, 55), width=1)

    f_main = _font(20)
    main_txt = "무당님이 작두 타는 중..."
    bb = draw.textbbox((0, 0), main_txt, font=f_main)
    draw.text((cx - (bb[2]-bb[0])//2, ty+4), main_txt, font=f_main, fill=(241, 196, 15))

    f_sub = _font(13)
    sub_txt = "신령님께서 운명을 살피고 계십니다"
    sb = draw.textbbox((0, 0), sub_txt, font=f_sub)
    draw.text((cx - (sb[2]-sb[0])//2, ty+40), sub_txt, font=f_sub, fill=(168, 144, 96))

    return img


def generate_loading_gif() -> bytes:
    """캐릭터가 통통 튀는 8프레임 로딩 GIF"""
    bounces      = [0, -3, -5, -3,  0,  3,  5,  3]
    flame_scales = [1.0, 1.1, 0.9, 1.2, 1.0, 0.85, 1.1, 0.95]

    frames = [_draw_frame(b, f) for b, f in zip(bounces, flame_scales)]

    buf = io.BytesIO()
    frames[0].save(
        buf, format="GIF",
        save_all=True, append_images=frames[1:],
        duration=160, loop=0, optimize=True,
    )
    buf.seek(0)
    return buf.getvalue()
