#!/usr/bin/env python3
"""Gera os fundos e sprites de Ponto Morto (pixel art + pós-processamento)."""

import math
import os
import random

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "game", "images")
GUI = os.path.join(ROOT, "game", "gui")
FONTS = os.path.join(ROOT, "game", "fonts")

LOW_W, LOW_H = 320, 180
SCALE = 4
FULL_W, FULL_H = LOW_W * SCALE, LOW_H * SCALE

SIL = (5, 7, 10)
RIM_L = (44, 62, 74)
RIM_R = (104, 72, 28)
AMBER = (255, 198, 118)
AMBER_DIM = (168, 112, 48)

os.makedirs(IMG, exist_ok=True)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vgrad(w, h, top, bottom):
    img = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(img)
    for y in range(h):
        d.line([(0, y), (w, y)], fill=lerp(top, bottom, y / max(1, h - 1)))
    return img


def draw_sky(d, w, h, top, bottom, horizon):
    for y in range(horizon):
        d.line([(0, y), (w, y)], fill=lerp(top, bottom, y / max(1, horizon - 1)))


def stars(d, w, horizon, seed, count=70, max_y=None):
    rnd = random.Random(seed)
    max_y = max_y or horizon - 4
    for _ in range(count):
        x = rnd.randint(0, w - 1)
        y = rnd.randint(2, max_y)
        b = rnd.randint(60, 180)
        d.point((x, y), fill=(b, b, min(255, b + 18)))


def hills(d, w, horizon):
    rnd = random.Random(11)
    pts = [(0, horizon)]
    x = 0
    y = horizon - 6
    while x <= w:
        y = max(horizon - 14, min(horizon - 2, y + rnd.randint(-4, 4)))
        pts.append((x, y))
        x += rnd.randint(14, 30)
    pts += [(w, horizon)]
    d.polygon(pts, fill=(8, 14, 18))


def road(d, w, h, horizon, vp=(150, 112), asphalt=(20, 22, 24)):
    d.polygon([(vp[0] - 4, horizon), (vp[0] + 5, horizon), (w + 60, h), (-60, h)], fill=asphalt)
    # acostamento
    for side in (-1, 1):
        x0 = vp[0] + side * 5
        x1 = 160 + side * 190
        d.line([(x0, horizon), (x1, h)], fill=(46, 44, 38), width=1)
    # faixa central tracejada
    t = 0.04
    while t < 1.0:
        y = horizon + int((h - horizon) * (t ** 1.55))
        y2 = horizon + int((h - horizon) * (min(1.0, t + 0.07) ** 1.55))
        cx = int(vp[0] + (160 - vp[0]) * (t ** 1.3))
        wdt = max(1, int(1 + 4 * (t ** 1.6)))
        d.rectangle([cx - wdt // 2, y, cx + wdt // 2, y2], fill=(150, 138, 96))
        t += 0.14


def utility_pole(d, w, horizon):
    pole = (7, 9, 11)
    d.rectangle([26, 36, 29, horizon + 6], fill=pole)
    d.rectangle([15, 48, 40, 51], fill=pole)
    d.rectangle([19, 55, 36, 57], fill=pole)
    # fios bambos
    for base_y in (47, 50):
        pts = []
        for x in range(16, w + 8, 6):
            t = (x - 16) / (w - 16)
            y = base_y + 7 * math.sin(math.pi * min(1.0, t))
            pts.append((x, int(y)))
        d.line(pts, fill=(10, 12, 14), width=1)
    d.rectangle([24, 96, 31, 104], fill=(12, 14, 16))


def gas_station(d, w, h):
    # loja ao fundo
    d.rectangle([278, 94, w, 134], fill=(11, 13, 16))
    d.rectangle([284, 104, 312, 126], fill=(196, 150, 82))
    d.line([(298, 104), (298, 126)], fill=(40, 32, 22), width=1)
    d.rectangle([306, 112, 311, 126], fill=(70, 52, 30))
    # piso de concreto
    d.polygon([(196, 118), (w, 110), (w, h), (140, h)], fill=(17, 18, 19))
    # cobertura
    d.rectangle([190, 86, w, 97], fill=(9, 11, 14))
    d.rectangle([190, 97, w, 100], fill=(34, 32, 26))
    # luminárias
    for lx in (206, 240, 274, 308):
        d.rectangle([lx, 98, lx + 14, 101], fill=AMBER)
    # colunas
    d.rectangle([194, 99, 198, 150], fill=(11, 13, 16))
    d.rectangle([316, 99, 320, 150], fill=(11, 13, 16))
    # bombas
    for px in (206, 244, 282):
        d.rectangle([px, 118, px + 15, 147], fill=(13, 15, 18))
        d.rectangle([px, 118, px + 15, 121], fill=(44, 43, 38))
        d.rectangle([px + 3, 125, px + 12, 131], fill=(150, 108, 44))
        d.rectangle([px + 4, 135, px + 11, 141], fill=(38, 40, 40))
    # placa alta
    d.rectangle([236, 66, 300, 78], fill=(12, 14, 16))
    d.text((268, 72), "POSTO", fill=(150, 118, 60), font=ImageFont.truetype(os.path.join(FONTS, "JetBrainsMono-Bold.ttf"), 8), anchor="mm")


def exterior(seed=5, dark=1.0, figure=False):
    w, h = LOW_W, LOW_H
    img = Image.new("RGB", (w, h), (5, 8, 13))
    d = ImageDraw.Draw(img)
    horizon = 112
    draw_sky(d, w, h, (4, 7, 12), (18, 30, 38), horizon)
    stars(d, w, horizon, seed)
    hills(d, w, horizon)
    d.rectangle([0, horizon, w, h], fill=(9, 12, 14))
    road(d, w, h, horizon)
    gas_station(d, w, h)
    utility_pole(d, w, horizon)

    if figure:
        # vulto parado no acostamento
        fx, fy = 118, 118
        d.ellipse([fx - 2, fy - 16, fx + 2, fy - 11], fill=(3, 4, 6))
        d.polygon([(fx - 4, fy - 11), (fx + 4, fy - 11), (fx + 5, fy), (fx - 5, fy)], fill=(3, 4, 6))
        d.rectangle([fx - 3, fy, fx - 1, fy + 5], fill=(3, 4, 6))
        d.rectangle([fx + 1, fy, fx + 3, fy + 5], fill=(3, 4, 6))

    if dark != 1.0:
        img = Image.eval(img, lambda v: int(v * dark))

    glows = [
        (245, 96, 150, (255, 176, 84), 90),
        (213, 99, 44, (255, 205, 130), 110),
        (262, 99, 44, (255, 205, 130), 110),
        (305, 99, 40, (255, 205, 130), 90),
        (298, 114, 46, (255, 186, 96), 70),
    ]
    return finalize(img, glows=glows, vignette=0.6, grain=14, scan=14)


def finalize(low, glows=None, vignette=0.55, grain=12, scan=10):
    img = low.resize((FULL_W, FULL_H), Image.NEAREST).convert("RGBA")

    if glows:
        layer = Image.new("RGBA", (FULL_W, FULL_H), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        steps = 28
        for (cx, cy, r, color, alpha) in glows:
            cx, cy, r = cx * SCALE, cy * SCALE, r * SCALE
            for i in range(steps + 1):
                frac = i / steps
                rr = r * (1 - frac)
                a = int(alpha * (frac ** 2.2))
                if rr <= 0 or a <= 0:
                    continue
                d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=color + (a,))
        layer = layer.filter(ImageFilter.GaussianBlur(18))
        img.alpha_composite(layer)

    if vignette:
        mask = Image.new("L", (80, 45))
        px = mask.load()
        for y in range(45):
            for x in range(80):
                dx = (x - 39.5) / 40.0
                dy = (y - 22.5) / 23.0
                dist = math.sqrt(dx * dx + dy * dy) / 1.414
                a = max(0.0, (dist - 0.32) / 0.68)
                px[x, y] = int(255 * vignette * (a ** 1.5))
        mask = mask.resize((FULL_W, FULL_H), Image.BILINEAR)
        black = Image.new("RGBA", (FULL_W, FULL_H), (0, 0, 0, 255))
        black.putalpha(mask)
        img.alpha_composite(black)

    if grain:
        noise = Image.effect_noise((FULL_W, FULL_H), grain).convert("RGB")
        img = Image.blend(img.convert("RGB"), noise, 0.05).convert("RGBA")

    if scan:
        sl = Image.new("RGBA", (FULL_W, FULL_H), (0, 0, 0, 0))
        d = ImageDraw.Draw(sl)
        for y in range(0, FULL_H, 3):
            d.line([(0, y), (FULL_W, y)], fill=(0, 0, 0, scan))
        img.alpha_composite(sl)

    return img.convert("RGB")


def interior(seed=21):
    w, h = LOW_W, LOW_H
    img = vgrad(w, h, (10, 16, 20), (6, 9, 12)).convert("RGB")
    d = ImageDraw.Draw(img)

    # janela
    wx0, wy0, wx1, wy1 = 14, 38, 150, 104
    d.rectangle([wx0 - 3, wy0 - 3, wx1 + 3, wy1 + 3], fill=(9, 11, 13))
    # cena noturna pela janela
    for y in range(wy0, wy1):
        t = (y - wy0) / (wy1 - wy0)
        d.line([(wx0, y), (wx1, y)], fill=lerp((6, 10, 16), (20, 32, 40), t))
    rnd = random.Random(seed)
    for _ in range(18):
        d.point((rnd.randint(wx0, wx1), rnd.randint(wy0, wy0 + 28)), fill=(90, 90, 100))
    hz = wy0 + 42
    d.rectangle([wx0, hz, wx1, wy1], fill=(12, 15, 17))
    # asfalto e faixa
    d.polygon([(wx0 + 56, hz), (wx0 + 60, hz), (wx1, wy1), (wx0 + 40, wy1)], fill=(22, 24, 26))
    d.line([(wx0 + 57, hz + 4), (wx1 - 30, wy1)], fill=(140, 128, 90), width=1)
    # brilho do posto
    d.rectangle([wx0 + 6, hz - 18, wx0 + 46, hz - 14], fill=(150, 108, 46))
    d.rectangle([wx0 + 10, hz - 14, wx1 - 30, hz - 2], fill=(28, 26, 22))
    d.rectangle([wx0 + 16, hz - 26, wx1 - 36, hz - 22], fill=(14, 16, 18))
    # caixilhos
    d.line([(wx0 + 68, wy0), (wx0 + 68, wy1)], fill=(8, 10, 12), width=2)
    d.line([(wx0, wy0 + 36), (wx1, wy0 + 36)], fill=(8, 10, 12), width=1)

    # prateleiras
    sx0, sx1 = 176, 316
    for sy in (52, 76, 100):
        d.rectangle([sx0, sy, sx1, sy + 2], fill=(16, 18, 19))
        x = sx0 + 4
        while x < sx1 - 6:
            bw = rnd.randint(4, 6)
            bh = rnd.randint(8, 13)
            col = rnd.choice([(36, 44, 40), (52, 40, 30), (28, 30, 34), (60, 52, 34)])
            d.rectangle([x, sy - bh, x + bw, sy], fill=col)
            d.rectangle([x + 1, sy - bh - 1, x + bw - 1, sy - bh], fill=(70, 70, 62))
            x += bw + rnd.randint(1, 3)

    # luminária fluorescente
    d.rectangle([112, 16, 208, 19], fill=(235, 240, 225))
    d.rectangle([112, 20, 208, 21], fill=(90, 100, 96))

    # relógio
    d.ellipse([150, 28, 168, 46], fill=(188, 176, 140))
    d.ellipse([152, 30, 166, 44], fill=(20, 22, 22))
    d.line([(159, 37), (159, 31)], fill=(210, 200, 160), width=1)
    d.line([(159, 37), (164, 39)], fill=(210, 200, 160), width=1)

    # cartaz de desaparecido
    d.rectangle([170, 30, 196, 64], fill=(178, 172, 152))
    d.rectangle([174, 33, 192, 50], fill=(48, 50, 52))
    d.ellipse([180, 36, 186, 42], fill=(30, 32, 34))
    d.polygon([(178, 50), (188, 50), (190, 46), (176, 46)], fill=(30, 32, 34))
    for yy in (54, 58, 62):
        d.line([(173, yy), (193, yy)], fill=(60, 58, 52))

    # balcão
    d.rectangle([0, 128, w, h], fill=(13, 15, 16))
    d.rectangle([0, 128, w, 132], fill=(40, 36, 28))
    d.rectangle([0, 150, w, 151], fill=(20, 22, 23))

    # caixa registradora
    d.rectangle([250, 104, 302, 132], fill=(15, 17, 18))
    d.rectangle([254, 108, 284, 118], fill=(120, 92, 42))
    d.rectangle([254, 120, 298, 126], fill=(34, 34, 32))
    for kx in range(256, 296, 5):
        d.rectangle([kx, 121, kx + 2, 123], fill=(70, 66, 54))

    # bilhete no balcão
    d.rectangle([198, 134, 232, 150], fill=(196, 188, 160))
    for yy in (137, 140, 143, 146):
        d.line([(201, yy), (228, yy)], fill=(70, 66, 58))

    glows = [
        (160, 22, 110, (220, 235, 215), 55),
        (270, 112, 60, (255, 176, 84), 50),
        (56, 130, 90, (255, 186, 96), 35),
    ]
    out = finalize(img, glows=glows, vignette=0.72, grain=12, scan=12)
    return out


def road_scene(dawn=False):
    w, h = LOW_W, LOW_H
    img = Image.new("RGB", (w, h), (5, 8, 13))
    d = ImageDraw.Draw(img)
    horizon = 104
    if dawn:
        draw_sky(d, w, h, (22, 32, 58), (232, 130, 58), horizon)
        d.ellipse([104, 78, 136, 110], fill=(255, 180, 96))
    else:
        draw_sky(d, w, h, (3, 6, 11), (14, 24, 32), horizon)
        stars(d, w, horizon, 3)
    hills(d, w, horizon)
    d.rectangle([0, horizon, w, h], fill=(9, 12, 14))
    road(d, w, h, horizon, vp=(158, 104))
    # postes de cerca
    for i in range(9):
        t = (i + 1) / 10
        x = int(158 + (250 - 158) * t)
        y = int(horizon + (h - horizon) * (t ** 1.4))
        hh = int(2 + 12 * t)
        d.rectangle([x, y - hh, x + 1, y], fill=(34, 32, 26))
    if dawn:
        glows = [(120, 96, 140, (255, 160, 80), 80)]
        return finalize(img, glows=glows, vignette=0.5, grain=10, scan=10)
    glows = [(158, 104, 60, (150, 140, 100), 30)]
    return finalize(img, glows=glows, vignette=0.75, grain=14, scan=14)


def cliente(rosto=False):
    w, h = 90, 170
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    d.ellipse([37, 12, 53, 33], fill=SIL)
    d.rectangle([42, 31, 48, 38], fill=SIL)
    d.polygon([(30, 38), (60, 38), (67, 48), (23, 48)], fill=SIL)
    d.polygon([(23, 48), (67, 48), (71, 101), (66, 151), (52, 151),
               (48, 113), (42, 113), (38, 151), (24, 151), (19, 101)], fill=SIL)
    d.polygon([(23, 49), (16, 53), (11, 97), (18, 99), (26, 61)], fill=SIL)
    d.polygon([(67, 49), (74, 53), (79, 97), (72, 99), (64, 61)], fill=SIL)
    d.ellipse([11, 96, 19, 104], fill=SIL)
    d.ellipse([71, 96, 79, 104], fill=SIL)
    d.rectangle([38, 150, 44, 166], fill=SIL)
    d.rectangle([48, 150, 54, 166], fill=SIL)
    d.rectangle([35, 165, 45, 169], fill=SIL)
    d.rectangle([47, 165, 57, 169], fill=SIL)

    # luz de contorno
    d.line([(38, 13), (36, 20), (34, 30)], fill=RIM_L, width=1)
    d.line([(23, 49), (19, 62), (16, 96)], fill=RIM_L, width=1)
    d.line([(24, 60), (20, 100), (24, 149)], fill=RIM_L, width=1)
    d.line([(52, 13), (54, 22), (53, 31)], fill=RIM_R, width=1)
    d.line([(67, 49), (71, 62), (74, 96)], fill=RIM_R, width=1)
    d.line([(66, 60), (70, 100), (66, 149)], fill=RIM_R, width=1)

    if rosto:
        rnd = random.Random(99)
        for _ in range(70):
            x = rnd.randint(39, 51)
            y = rnd.randint(16, 30)
            c = rnd.choice([(216, 204, 176), (150, 138, 116), (92, 30, 26)])
            d.point((x, y), fill=c)
        d.line([(40, 26), (50, 26)], fill=(120, 26, 22), width=1)
        d.line([(41, 17), (45, 19)], fill=(30, 8, 8), width=1)
        d.line([(46, 19), (50, 17)], fill=(30, 8, 8), width=1)

    img = img.resize((w * SCALE, h * SCALE), Image.NEAREST)
    return img


def title_card():
    base = exterior(seed=5, dark=0.5, figure=True).resize((FULL_W, FULL_H), Image.LANCZOS).convert("RGBA")
    dark = Image.new("RGBA", (FULL_W, FULL_H), (2, 4, 7, 130))
    base.alpha_composite(dark)

    low = base.resize((LOW_W, LOW_H), Image.LANCZOS).convert("RGBA")
    tx, ty = 200, 62

    # painel escuro atrás do título, para os letreiros não competirem
    panel = Image.new("RGBA", (LOW_W, LOW_H), (0, 0, 0, 0))
    ImageDraw.Draw(panel).rectangle([tx - 104, ty - 28, tx + 104, ty + 54], fill=(3, 5, 8, 176))
    panel = panel.filter(ImageFilter.GaussianBlur(6))
    low.alpha_composite(panel)

    d = ImageDraw.Draw(low)
    title_font = ImageFont.truetype(os.path.join(FONTS, "JetBrainsMono-ExtraBold.ttf"), 24)
    sub_font = ImageFont.truetype(os.path.join(FONTS, "JetBrainsMono-Regular.ttf"), 8)

    d.text((tx - 2, ty), "PONTO", fill=(196, 38, 32), font=title_font, anchor="mm")
    d.text((tx + 2, ty - 1), "MORTO", fill=(38, 168, 188), font=title_font, anchor="mm")
    d.text((tx, ty), "PONTO", fill=(238, 226, 198), font=title_font, anchor="mm")
    d.text((tx, ty + 22), "MORTO", fill=(238, 226, 198), font=title_font, anchor="mm")
    d.text((tx, ty + 42), "KM 42  ·  BR-116", fill=(150, 134, 100), font=sub_font, anchor="mm")
    d.line([(tx - 86, ty + 33), (tx + 86, ty + 33)], fill=(96, 78, 44), width=1)

    out = low.resize((FULL_W, FULL_H), Image.NEAREST).convert("RGB")
    return out


def menu_bg():
    base = interior(seed=21).filter(ImageFilter.GaussianBlur(10))
    dark = Image.new("RGBA", base.size, (3, 5, 8, 150))
    base = base.convert("RGBA")
    base.alpha_composite(dark)
    return base.convert("RGB")


def icon():
    s = 256
    img = Image.new("RGBA", (s, s), (6, 9, 13, 255))
    d = ImageDraw.Draw(img)
    d.rectangle([6, 6, s - 7, s - 7], outline=(150, 110, 52, 255), width=4)
    # estrada em perspectiva
    d.polygon([(118, 96), (138, 96), (196, 208), (60, 208)], fill=(18, 20, 22, 255))
    d.line([(128, 100), (76, 208)], fill=(120, 106, 72, 255), width=3)
    d.line([(128, 100), (180, 208)], fill=(120, 106, 72, 255), width=3)
    t = 0.1
    while t < 1.0:
        y = 100 + int(108 * t)
        cx = 128
        d.line([(cx, y), (cx, y + max(2, int(10 * t)))], fill=(196, 176, 120, 255), width=max(1, int(3 * t)))
        t += 0.22
    # vulto
    d.ellipse([125, 128, 131, 134], fill=(3, 4, 6, 255))
    d.polygon([(124, 134), (132, 134), (134, 152), (122, 152)], fill=(3, 4, 6, 255))
    d.ellipse([104, 84, 152, 86], fill=(255, 198, 118, 60))
    return img


def make_glitch(base):
    r, g, b = base.split()
    r = ImageChops.offset(r, 7, 0)
    b = ImageChops.offset(b, -7, 0)
    out = Image.merge("RGB", (r, g, b))
    rnd = random.Random(13)
    for _ in range(18):
        y = rnd.randint(0, out.height - 14)
        hh = rnd.randint(2, 12)
        band = out.crop((0, y, out.width, y + hh))
        band = ImageChops.offset(band, rnd.randint(-30, 30), 0)
        out.paste(band, (0, y))
    return Image.eval(out, lambda v: int(v * 0.88))


def main():
    exterior(seed=5).save(os.path.join(IMG, "bg_posto.png"))
    exterior(seed=5, dark=0.55).save(os.path.join(IMG, "bg_posto_escuro.png"))
    interior(seed=21).save(os.path.join(IMG, "bg_balcao.png"))

    make_glitch(interior(seed=21)).save(os.path.join(IMG, "bg_balcao_glitch.png"))
    make_glitch(exterior(seed=5)).save(os.path.join(IMG, "bg_posto_glitch.png"))

    road_scene(dawn=False).save(os.path.join(IMG, "bg_estrada.png"))
    road_scene(dawn=True).save(os.path.join(IMG, "bg_amanhecer.png"))
    title_card().save(os.path.join(GUI, "main_menu.png"))
    menu_bg().save(os.path.join(GUI, "game_menu.png"))
    cliente(False).save(os.path.join(IMG, "cliente.png"))
    cliente(True).save(os.path.join(IMG, "cliente_rosto.png"))
    icon().save(os.path.join(GUI, "window_icon.png"))
    print("imagens geradas")


if __name__ == "__main__":
    main()
