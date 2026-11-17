#!/usr/bin/env python3
"""Gera os fundos e sprites de Ponto Morto (pixel art + pós-processamento).

Grade interna 640x360, ampliada 2x para 1280x720.
A UI (gui/main_menu.png, gui/game_menu.png, gui/window_icon.png e afins)
NÃO é regenerada: está finalizada e é preservada como está.
"""

import math
import os
import random

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "game", "images")
FONTS = os.path.join(ROOT, "game", "fonts")

LOW_W, LOW_H = 640, 360
SCALE = 2
FULL_W, FULL_H = LOW_W * SCALE, LOW_H * SCALE

# Paleta
SIL = (6, 8, 11)
RIM_L = (52, 72, 88)          # luz fria (lado esquerdo)
RIM_R = (176, 108, 40)        # luz quente (lado direito)
AMBER = (255, 196, 110)
AMBER_DIM = (150, 100, 44)
ASPHALT = (15, 17, 19)
GROUND = (9, 12, 14)

os.makedirs(IMG, exist_ok=True)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vgrad(w, h, top, bottom):
    img = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(img)
    for y in range(h):
        d.line([(0, y), (w, y)], fill=lerp(top, bottom, y / max(1, h - 1)))
    return img


# ----------------------------------------------------------------------
#  CÉU / ATMOSFERA
# ----------------------------------------------------------------------

def draw_sky(d, w, horizon, top, bottom):
    for y in range(horizon):
        d.line([(0, y), (w, y)], fill=lerp(top, bottom, y / max(1, horizon - 1)))


def stars(d, w, horizon, seed, count=150, max_y=None):
    rnd = random.Random(seed)
    max_y = max_y or horizon - 8
    for _ in range(count):
        x = rnd.randint(2, w - 3)
        y = rnd.randint(4, max_y)
        r = rnd.random()
        if r < 0.72:
            b = rnd.randint(40, 90)
            d.point((x, y), fill=(b, b, min(255, b + 12)))
        elif r < 0.94:
            b = rnd.randint(110, 170)
            d.point((x, y), fill=(b, b, min(255, b + 22)))
        else:
            b = rnd.randint(180, 235)
            d.point((x, y), fill=(b, b, min(255, b + 20)))
            d.point((x - 1, y), fill=(b // 2, b // 2, b // 2))
            d.point((x + 1, y), fill=(b // 2, b // 2, b // 2))


def moon(d, cx, cy, r, phase=0.0):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(204, 213, 218))
    if phase:
        off = int(r * 0.55)
        d.ellipse([cx - r + off, cy - r, cx + r + off, cy + r], fill=(176, 188, 196))
    d.ellipse([cx - r // 3, cy - r // 3, cx - r // 3 + 3, cy - r // 3 + 3], fill=(150, 162, 170))
    d.ellipse([cx + r // 4, cy + r // 6, cx + r // 4 + 2, cy + r // 6 + 2], fill=(150, 162, 170))


def fog(d, w, horizon, band=22, color=(24, 36, 44)):
    for i in range(band):
        t = i / band
        a = 1.0 - (i / band)
        d.line([(0, horizon - band // 2 + i), (w, horizon - band // 2 + i)],
               fill=lerp(color, (0, 0, 0), 0.0) if False else
               tuple(int(c * (0.35 + 0.65 * t)) for c in color))


def hills(d, w, horizon, seed, base, amp, jag=6):
    rnd = random.Random(seed)
    pts = [(0, horizon)]
    x = 0
    y = horizon - rnd.randint(4, 10)
    while x <= w:
        y = max(horizon - amp, min(horizon - 3, y + rnd.randint(-jag, jag)))
        pts.append((x, y))
        x += rnd.randint(26, 60)
    pts += [(w, horizon)]
    d.polygon(pts, fill=base)


# ----------------------------------------------------------------------
#  CHÃO / ESTRADA
# ----------------------------------------------------------------------

def ground(d, w, h, horizon, base=GROUND):
    d.rectangle([0, horizon, w, h], fill=base)


def road(d, w, h, horizon, vp=(320, 224), asphalt=ASPHALT):
    d.polygon([(vp[0] - 8, horizon), (vp[0] + 9, horizon), (w + 160, h), (-160, h)], fill=asphalt)

    # acostamento (linhas laterais)
    for side in (-1, 1):
        x0 = vp[0] + side * 9
        x1 = 320 + side * 400
        d.line([(x0, horizon), (x1, h)], fill=(58, 52, 42), width=1)

    # faixa central tracejada
    t = 0.04
    while t < 1.0:
        y = horizon + int((h - horizon) * (t ** 1.5))
        y2 = horizon + int((h - horizon) * (min(1.0, t + 0.06) ** 1.5))
        cx = int(vp[0] + (320 - vp[0]) * (t ** 1.25))
        wdt = max(1, int(1 + 7 * (t ** 1.6)))
        d.rectangle([cx - wdt // 2, y, cx + wdt // 2, y2], fill=(150, 134, 96))
        t += 0.12

    # desgaste do asfalto (manchas sutis)
    rnd = random.Random(77)
    for _ in range(40):
        x = rnd.randint(0, w - 1)
        y = rnd.randint(horizon + 4, h - 1)
        d.point((x, y), fill=(11, 13, 15))


# ----------------------------------------------------------------------
#  POSTO DE GASOLINA (fachada externa)
# ----------------------------------------------------------------------

def gas_station(d, w, h, horizon=224):
    rnd = random.Random(7)

    # base de concreto sob a estação
    d.polygon([(400, horizon + 4), (w, horizon - 8), (w, h), (380, h)], fill=(15, 16, 18))

    # loja ao fundo
    d.rectangle([522, 140, w, 226], fill=(9, 11, 14))
    d.rectangle([516, 134, w, 140], fill=(6, 8, 10))
    # vitrine acesa
    d.rectangle([530, 158, 606, 206], fill=(96, 56, 22))
    d.rectangle([534, 162, 602, 202], fill=(232, 150, 66))
    d.rectangle([538, 166, 598, 198], fill=(255, 186, 92))
    # prateleira visível na vitrine
    for sy in (172, 184, 196):
        d.line([(540, sy), (596, sy)], fill=(120, 74, 30), width=1)
        for bx in range(542, 594, 7):
            d.rectangle([bx, sy - 5, bx + 4, sy], fill=rnd.choice([(90, 60, 30), (70, 50, 34), (40, 40, 44)]))
    # divisória da vitrine
    d.line([(568, 158), (568, 206)], fill=(28, 22, 14), width=2)
    # porta
    d.rectangle([608, 180, 634, 226], fill=(7, 9, 11))
    d.rectangle([610, 182, 632, 226], fill=(22, 20, 16))
    # placa "24H"
    d.rectangle([558, 148, 588, 158], fill=(26, 17, 10))
    d.text((573, 153), "24H", fill=(220, 150, 60), font=ImageFont.truetype(os.path.join(FONTS, "JetBrainsMono-Bold.ttf"), 8), anchor="mm")

    # cobertura
    d.rectangle([372, 116, w, 138], fill=(10, 12, 15))
    d.rectangle([372, 138, w, 144], fill=(38, 34, 26))
    # barras de luz âmbar sob a cobertura
    for lx in (392, 468, 544, 614):
        d.rectangle([lx, 140, lx + 26, 145], fill=AMBER)
    # colunas
    d.rectangle([378, 138, 386, 302], fill=(11, 13, 16))
    d.rectangle([630, 138, 638, 302], fill=(11, 13, 16))

    # bombas
    for px in (402, 468, 534):
        d.rectangle([px, 214, px + 34, 302], fill=(13, 15, 18))
        d.rectangle([px, 214, px + 34, 222], fill=(48, 46, 38))
        d.rectangle([px + 4, 226, px + 30, 240], fill=(120, 88, 34))
        d.rectangle([px + 5, 228, px + 29, 238], fill=(190, 150, 60))
        d.rectangle([px + 7, 246, px + 27, 256], fill=(22, 24, 26))
        d.rectangle([px + 7, 262, px + 27, 266], fill=(18, 20, 22))
        d.line([(px + 6, 258), (px + 6, 292), (px + 26, 300)], fill=(34, 32, 28), width=2)

    # poça de luz no chão (reflexo úmido)
    d.polygon([(380, 300), (w, 300), (w + 30, h), (360, h)], fill=(22, 19, 12))
    for x in range(392, w, 13):
        d.line([(x, 304), (x + rnd.randint(-2, 2), h)], fill=(66, 44, 16), width=1)

    # letreiro alto "POSTO"
    d.rectangle([236, 52, 242, 224], fill=(8, 10, 12))
    d.rectangle([212, 48, 266, 96], fill=(10, 12, 14))
    d.rectangle([215, 51, 263, 93], fill=(18, 15, 10))
    d.text((239, 72), "POSTO", fill=(235, 170, 74), font=ImageFont.truetype(os.path.join(FONTS, "JetBrainsMono-Bold.ttf"), 16), anchor="mm")


def utility_pole(d, w, horizon):
    pole = (7, 9, 11)
    d.rectangle([52, 72, 58, horizon + 8], fill=pole)
    d.rectangle([30, 96, 80, 102], fill=pole)
    d.rectangle([38, 108, 74, 112], fill=pole)
    # fios bambos
    for base_y in (94, 100):
        pts = []
        for x in range(30, w + 16, 6):
            t = (x - 30) / (w - 30)
            y = base_y + 13 * math.sin(math.pi * min(1.0, t))
            pts.append((x, int(y)))
        d.line(pts, fill=(10, 12, 14), width=1)
    d.rectangle([48, 190, 62, 208], fill=(12, 14, 16))


# ----------------------------------------------------------------------
#  CENAS
# ----------------------------------------------------------------------

def exterior(seed=5, dark=1.0, figure=False):
    w, h = LOW_W, LOW_H
    img = Image.new("RGB", (w, h), (5, 8, 13))
    d = ImageDraw.Draw(img)
    horizon = 224

    draw_sky(d, w, horizon, (3, 6, 12), (20, 34, 46))
    stars(d, w, horizon, seed)
    moon(d, 500, 74, 16, phase=0.25)
    fog(d, w, horizon, band=24)
    hills(d, w, horizon, seed + 1, (8, 13, 18), 14, jag=5)
    hills(d, w, horizon, seed + 2, (6, 10, 14), 24, jag=6)
    ground(d, w, h, horizon)
    road(d, w, h, horizon, vp=(320, 224))
    gas_station(d, w, h, horizon)
    utility_pole(d, w, horizon)

    if figure:
        # vulto parado no acostamento
        fx, fy = 236, 230
        d.ellipse([fx - 4, fy - 32, fx + 4, fy - 22], fill=(3, 4, 6))
        d.polygon([(fx - 8, fy - 22), (fx + 8, fy - 22), (fx + 10, fy), (fx - 10, fy)], fill=(3, 4, 6))
        d.rectangle([fx - 6, fy, fx - 2, fy + 10], fill=(3, 4, 6))
        d.rectangle([fx + 2, fy, fx + 6, fy + 10], fill=(3, 4, 6))

    if dark != 1.0:
        img = Image.eval(img, lambda v: int(v * dark))

    glows = [
        (500, 74, 60, (190, 200, 205), 34),   # lua
        (239, 72, 70, (235, 170, 74), 60),    # letreiro POSTO
        (470, 142, 80, (255, 190, 96), 70),   # barras de luz
        (568, 182, 90, (255, 176, 84), 70),   # vitrine
    ]
    return finalize(img, glows=glows, vignette=0.62, grain=11, scan=12, dither=True)


def interior(seed=21):
    w, h = LOW_W, LOW_H
    img = vgrad(w, h, (9, 15, 19), (6, 9, 12)).convert("RGB")
    d = ImageDraw.Draw(img)
    rnd = random.Random(seed)

    # ------- janela (à esquerda) -------
    wx0, wy0, wx1, wy1 = 28, 74, 300, 208
    d.rectangle([wx0 - 6, wy0 - 6, wx1 + 6, wy1 + 6], fill=(8, 10, 12))
    # céu noturno
    for y in range(wy0, wy0 + 52):
        t = (y - wy0) / 52
        d.line([(wx0, y), (wx1, y)], fill=lerp((4, 8, 14), (18, 30, 42), t))
    for _ in range(24):
        d.point((rnd.randint(wx0, wx1), rnd.randint(wy0, wy0 + 26)), fill=(90, 90, 104))
    moon(ImageDraw.Draw(img), 260, 96, 9)
    hz = wy0 + 44
    # asfalto + faixa
    d.rectangle([wx0, hz, wx1, wy1], fill=(11, 14, 16))
    d.polygon([(wx0 + 112, hz), (wx0 + 120, hz), (wx1, wy1), (wx0 + 80, wy1)], fill=(20, 22, 24))
    d.line([(wx0 + 114, hz + 8), (wx1 - 56, wy1)], fill=(140, 128, 90), width=1)
    # brilho do posto ao longe
    d.rectangle([wx0 + 12, hz - 36, wx0 + 92, hz - 28], fill=(150, 108, 46))
    d.rectangle([wx0 + 20, hz - 28, wx1 - 60, hz - 4], fill=(28, 26, 22))
    d.rectangle([wx0 + 32, hz - 52, wx1 - 72, hz - 44], fill=(14, 16, 18))
    # caixilhos
    d.line([(wx0 + 136, wy0), (wx0 + 136, wy1)], fill=(8, 10, 12), width=2)
    d.line([(wx0, wy0 + 52), (wx1, wy0 + 52)], fill=(8, 10, 12), width=1)

    # ------- prateleiras (à direita) -------
    sx0, sx1 = 352, 632
    for sy in (104, 152, 200):
        d.rectangle([sx0, sy, sx1, sy + 2], fill=(16, 18, 19))
        x = sx0 + 6
        while x < sx1 - 8:
            bw = rnd.randint(6, 9)
            bh = rnd.randint(14, 22)
            col = rnd.choice([(40, 52, 48), (66, 46, 30), (30, 32, 38), (70, 60, 36), (44, 38, 54)])
            d.rectangle([x, sy - bh, x + bw, sy], fill=col)
            d.rectangle([x + 1, sy - bh - 1, x + bw - 1, sy - bh], fill=(84, 84, 72))
            x += bw + rnd.randint(1, 4)

    # ------- luminária fluorescente -------
    d.rectangle([224, 30, 416, 36], fill=(235, 242, 228))
    d.rectangle([224, 37, 416, 39], fill=(96, 106, 100))
    d.rectangle([224, 30, 416, 30], fill=(60, 70, 66))

    # ------- relógio (marca ~3:07) -------
    cx, cy, cr = 334, 72, 22
    d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(188, 176, 140))
    d.ellipse([cx - cr + 3, cy - cr + 3, cx + cr - 3, cy + cr - 3], fill=(20, 22, 22))
    d.point((cx, cy), fill=(210, 200, 160))
    d.line([(cx, cy), (cx + 11, cy - 2)], fill=(210, 200, 160), width=2)   # ponteiro hora (~3h)
    d.line([(cx, cy), (cx - 7, cy + 13)], fill=(210, 200, 160), width=1)   # ponteiro minuto (~7min)

    # ------- cartaz de desaparecido -------
    d.rectangle([340, 58, 392, 128], fill=(178, 172, 152))
    d.rectangle([344, 61, 388, 100], fill=(46, 48, 50))
    d.ellipse([352, 70, 366, 84], fill=(30, 32, 34))
    d.polygon([(356, 86), (376, 86), (380, 80), (352, 80)], fill=(30, 32, 34))
    d.line([(344, 104), (388, 104)], fill=(60, 58, 52), width=1)
    for yy in (108, 113, 118, 123):
        d.line([(346, yy), (386, yy)], fill=(60, 58, 52), width=1)
    d.rectangle([344, 61, 388, 63], fill=(110, 30, 24))

    # ------- balcão -------
    d.rectangle([0, 256, w, h], fill=(12, 14, 15))
    d.rectangle([0, 256, w, 264], fill=(52, 46, 34))
    d.rectangle([0, 262, w, 263], fill=(90, 80, 56))
    d.rectangle([0, 300, w, 302], fill=(20, 22, 23))
    # reflexo do relógio/luz no tampo
    for x in range(0, w, 5):
        d.point((x, 266 + (x % 3)), fill=(40, 38, 30))

    # ------- caixa registradora -------
    d.rectangle([500, 206, 604, 264], fill=(15, 17, 18))
    d.rectangle([508, 214, 568, 236], fill=(40, 44, 42))
    d.rectangle([510, 216, 566, 234], fill=(104, 120, 92))
    d.rectangle([514, 220, 562, 230], fill=(150, 168, 132))
    d.rectangle([508, 240, 596, 252], fill=(36, 36, 32))
    for kx in range(512, 592, 6):
        d.rectangle([kx, 242, kx + 2, 244], fill=(70, 66, 54))

    # ------- bilhete no balcão -------
    d.rectangle([396, 268, 464, 300], fill=(196, 188, 160))
    for yy in (274, 278, 282, 286):
        d.line([(402, yy), (458, yy)], fill=(70, 66, 58), width=1)

    glows = [
        (320, 40, 120, (220, 235, 215), 46),   # fluorescente
        (539, 222, 60, (150, 168, 132), 44),   # visor do caixa
        (58, 120, 90, (255, 186, 96), 30),     # brilho externo da janela
    ]
    return finalize(img, glows=glows, vignette=0.72, grain=11, scan=12, dither=True)


def road_scene(dawn=False):
    w, h = LOW_W, LOW_H
    img = Image.new("RGB", (w, h), (5, 8, 13))
    d = ImageDraw.Draw(img)
    horizon = 208

    if dawn:
        draw_sky(d, w, horizon, (22, 32, 58), (232, 130, 58))
        moon(ImageDraw.Draw(img), 120, 96, 0)  # no-op, só pra clareza
        d.ellipse([208, 150, 272, 214], fill=(255, 180, 96))
        d.ellipse([212, 154, 268, 210], fill=(255, 196, 112))
    else:
        draw_sky(d, w, horizon, (3, 6, 11), (14, 24, 32))
        stars(d, w, horizon, 3)
        moon(d, 170, 80, 14, phase=0.2)

    hills(d, w, horizon, 5, (8, 13, 18), 14, jag=5)
    ground(d, w, h, horizon)
    road(d, w, h, horizon, vp=(316, 208))

    # mourões de cerca ao longo do acostamento
    for i in range(1, 10):
        t = i / 10.0
        x = int(316 + (500 - 316) * t)
        y = int(horizon + (h - horizon) * (t ** 1.4))
        hh = int(4 + 24 * t)
        d.rectangle([x, y - hh, x + 2, y], fill=(34, 32, 26))

    if dawn:
        glows = [(240, 180, 160, (255, 170, 80), 80)]
        return finalize(img, glows=glows, vignette=0.5, grain=10, scan=10, dither=True)
    glows = [(170, 80, 60, (180, 188, 194), 34), (316, 208, 60, (150, 140, 100), 26)]
    return finalize(img, glows=glows, vignette=0.78, grain=12, scan=13, dither=True)


# ----------------------------------------------------------------------
#  SPRITES DO CLIENTE
# ----------------------------------------------------------------------

def _cliente_corpo(d):
    """Silhueta do homem de boné e casaco, molhado."""
    w, h = 180, 340
    # cabeça
    d.ellipse([74, 20, 106, 52], fill=SIL)
    # aba do boné (esconde o rosto)
    d.polygon([(58, 44), (122, 44), (112, 50), (68, 50)], fill=(3, 4, 6))
    d.ellipse([72, 16, 108, 42], fill=(4, 5, 8))
    # pescoço
    d.rectangle([82, 50, 98, 66], fill=SIL)
    # tronco / casaco
    d.polygon([(58, 66), (122, 66), (134, 150), (46, 150)], fill=SIL)
    # ombros / braços
    d.polygon([(58, 66), (42, 72), (38, 122), (60, 122)], fill=SIL)
    d.polygon([(122, 66), (138, 72), (142, 122), (120, 122)], fill=SIL)
    d.rectangle([40, 122, 58, 198], fill=SIL)
    d.rectangle([122, 122, 140, 198], fill=SIL)
    d.ellipse([42, 198, 58, 212], fill=SIL)
    d.ellipse([122, 198, 138, 212], fill=SIL)
    # pernas
    d.rectangle([66, 152, 90, 320], fill=SIL)
    d.rectangle([90, 152, 114, 320], fill=SIL)
    # pés
    d.rectangle([64, 320, 90, 336], fill=SIL)
    d.rectangle([90, 320, 116, 336], fill=SIL)


def _cliente_rim(d):
    """Luz de contorno fria/quente + brilho úmido + goteiras."""
    # contorno frio (esquerda)
    d.line([(58, 68), (52, 110), (50, 196)], fill=RIM_L, width=1)
    d.line([(74, 22), (70, 34), (68, 46)], fill=RIM_L, width=1)
    d.line([(40, 122), (38, 162), (40, 198)], fill=RIM_L, width=1)
    d.line([(66, 154), (64, 240), (66, 318)], fill=RIM_L, width=1)
    # contorno quente (direita)
    d.line([(122, 68), (128, 110), (130, 196)], fill=RIM_R, width=1)
    d.line([(104, 22), (108, 34), (110, 46)], fill=RIM_R, width=1)
    d.line([(140, 122), (142, 162), (140, 198)], fill=RIM_R, width=1)
    d.line([(114, 154), (116, 240), (114, 318)], fill=RIM_R, width=1)
    # brilho úmido no casaco
    for x in (66, 80, 94, 108, 120):
        d.line([(x, 72), (x, 142)], fill=(22, 28, 32), width=1)
    # goteiras
    d.line([(52, 150), (52, 158)], fill=(34, 44, 50), width=1)
    d.line([(128, 150), (128, 162)], fill=(66, 50, 32), width=1)
    d.line([(94, 150), (94, 156)], fill=(28, 34, 38), width=1)


def cliente(rosto=False):
    w, h = 180, 340
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # sombra de contato
    d.ellipse([56, 332, 124, 342], fill=(0, 0, 0, 110))

    if rosto:
        # cabeça com rosto pálido e úmido
        d.ellipse([74, 20, 106, 52], fill=(168, 156, 138))
        d.ellipse([72, 16, 108, 42], fill=(4, 5, 8))                 # coroa do boné
        d.polygon([(58, 42), (122, 42), (112, 48), (68, 48)], fill=(3, 4, 6))  # aba
        # olhos: órbitas escuras e afundadas
        d.ellipse([80, 34, 90, 42], fill=(7, 7, 7))
        d.ellipse([96, 34, 106, 42], fill=(7, 7, 7))
        d.point((85, 38), fill=(30, 24, 20))
        d.point((101, 38), fill=(30, 24, 20))
        # nariz: sombra vertical
        d.line([(90, 40), (88, 48)], fill=(120, 108, 92), width=1)
        # boca: larga demais, torta
        d.line([(78, 52), (102, 50)], fill=(40, 12, 10), width=2)
        d.line([(78, 52), (102, 50)], fill=(84, 22, 16), width=1)
        # brilho úmido na pele
        d.line([(80, 26), (82, 32)], fill=(214, 204, 182), width=1)
        d.line([(100, 26), (100, 34)], fill=(214, 204, 182), width=1)
        d.line([(84, 46), (84, 50)], fill=(200, 190, 170), width=1)
        d.line([(96, 46), (96, 50)], fill=(200, 190, 170), width=1)
        # tom enferrujado nas bordas (cheira a ferro)
        for i in range(8):
            d.point((76 + i, 26), fill=(150, 40, 26))
            d.point((100 + i, 40), fill=(150, 40, 26))
        d.rectangle([82, 50, 98, 66], fill=SIL)  # pescoço
    else:
        d.ellipse([74, 20, 106, 52], fill=SIL)
        d.polygon([(58, 44), (122, 44), (112, 50), (68, 50)], fill=(3, 4, 6))
        d.ellipse([72, 16, 108, 42], fill=(4, 5, 8))
        d.rectangle([82, 50, 98, 66], fill=SIL)

    # tronco + braços + pernas (reaproveita o corpo)
    _cliente_corpo(d)
    _cliente_rim(d)

    img = img.resize((w * SCALE, h * SCALE), Image.NEAREST)

    if rosto:
        # pós: dither + contraste para textura perturbadora
        img = _dither_rgba(img, 10)
        rnd = random.Random(99)
        px = img.load()
        for _ in range(260):
            x = rnd.randint(78, 104)
            y = rnd.randint(22, 54)
            c = rnd.choice([(216, 204, 176, 255), (150, 138, 116, 255), (92, 30, 26, 255)])
            px[x, y] = c
    return img


# ----------------------------------------------------------------------
#  PÓS-PROCESSAMENTO
# ----------------------------------------------------------------------

_BAYER = [[0, 32, 8, 40], [48, 16, 56, 24], [12, 44, 4, 36], [60, 28, 52, 20]]


def _dither(img, amp=6):
    w, h = img.size
    px = img.load()
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            th = (_BAYER[y & 3][x & 3] - 31.5) / 31.5
            px[x, y] = (
                min(255, max(0, int(r + th * amp))),
                min(255, max(0, int(g + th * amp))),
                min(255, max(0, int(b + th * amp))),
            )
    return img


def _dither_rgba(img, amp=6):
    w, h = img.size
    px = img.load()
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            th = (_BAYER[y & 3][x & 3] - 31.5) / 31.5
            px[x, y] = (
                min(255, max(0, int(r + th * amp))),
                min(255, max(0, int(g + th * amp))),
                min(255, max(0, int(b + th * amp))),
                a,
            )
    return img


def finalize(low, glows=None, vignette=0.55, grain=12, scan=10, dither=True):
    if dither:
        low = _dither(low)

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
        layer = layer.filter(ImageFilter.GaussianBlur(16))
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
        img = Image.blend(img.convert("RGB"), noise, 0.045).convert("RGBA")

    if scan:
        sl = Image.new("RGBA", (FULL_W, FULL_H), (0, 0, 0, 0))
        d = ImageDraw.Draw(sl)
        for y in range(0, FULL_H, 3):
            d.line([(0, y), (FULL_W, y)], fill=(0, 0, 0, scan))
        img.alpha_composite(sl)

    return img.convert("RGB")


def make_glitch(base):
    r, g, b = base.split()
    r = ImageChops.offset(r, 12, 0)
    b = ImageChops.offset(b, -12, 0)
    out = Image.merge("RGB", (r, g, b))
    rnd = random.Random(13)
    for _ in range(26):
        y = rnd.randint(0, out.height - 14)
        hh = rnd.randint(2, 12)
        band = out.crop((0, y, out.width, y + hh))
        band = ImageChops.offset(band, rnd.randint(-40, 40), 0)
        out.paste(band, (0, y))
    out = Image.eval(out, lambda v: int(v * 0.88))
    return out


# ----------------------------------------------------------------------
#  ÍCONE ANDROID (adaptive icon) + PRESPLASH
# ----------------------------------------------------------------------
# RAPT lê estes dois arquivos na RAIZ do projeto (mesma pasta do game/):
#   android-icon_foreground.png  432x432, transparente
#   android-icon_background.png  432x432, opaco
# e gera os tamanhos/ícones estáticos automaticamente.

def _draw_figure_icon(d, cx, feet_y):
    top = feet_y - 92
    ink = (3, 4, 6, 255)
    # cabeça + boné
    d.ellipse([cx - 7, top, cx + 7, top + 18], fill=ink)
    d.polygon([(cx - 9, top + 12), (cx + 9, top + 12), (cx + 6, top + 17), (cx - 6, top + 17)], fill=(2, 3, 5, 255))
    # tronco / casaco
    d.polygon([(cx - 9, top + 20), (cx + 9, top + 20), (cx + 13, feet_y - 30), (cx - 13, feet_y - 30)], fill=ink)
    # braços
    d.polygon([(cx - 9, top + 22), (cx - 14, top + 42), (cx - 13, feet_y - 34), (cx - 8, feet_y - 40)], fill=ink)
    d.polygon([(cx + 9, top + 22), (cx + 14, top + 42), (cx + 13, feet_y - 34), (cx + 8, feet_y - 40)], fill=ink)
    # pernas
    d.rectangle([cx - 9, feet_y - 32, cx - 2, feet_y], fill=ink)
    d.rectangle([cx + 2, feet_y - 32, cx + 9, feet_y], fill=ink)
    # pés
    d.rectangle([cx - 10, feet_y, cx - 1, feet_y + 7], fill=ink)
    d.rectangle([cx + 1, feet_y, cx + 10, feet_y + 7], fill=ink)
    # luz de contorno (frio à esquerda, quente à direita)
    d.line([(cx - 8, top + 22), (cx - 13, top + 50), (cx - 12, feet_y - 34)], fill=(52, 72, 88, 230), width=2)
    d.line([(cx + 8, top + 22), (cx + 13, top + 50), (cx + 12, feet_y - 34)], fill=(176, 108, 40, 230), width=2)


def android_background(s=432):
    img = vgrad(s, s, (4, 6, 10), (15, 22, 28)).convert("RGBA")
    d = ImageDraw.Draw(img)
    cx, cy = s // 2, 150
    # brilho âmbar (letreiro/horizonte)
    glow = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for i in range(24, 0, -1):
        frac = i / 24
        rr = 170 * frac
        a = int(80 * (1 - frac) ** 1.4)
        gd.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=(255, 178, 88, a))
    glow = glow.filter(ImageFilter.GaussianBlur(20))
    img.alpha_composite(glow)
    # estrelas fracas
    rnd = random.Random(5)
    d = ImageDraw.Draw(img)
    for _ in range(46):
        x = rnd.randint(6, s - 6)
        y = rnd.randint(6, cy - 8)
        b = rnd.randint(28, 80)
        d.point((x, y), fill=(b, b, min(255, b + 16), 255))
    # vinheta (escurece bordas, bom pra qualquer máscara)
    mask = Image.new("L", (s, s))
    mp = mask.load()
    for y in range(s):
        for x in range(s):
            dx = (x - s / 2) / (s / 2)
            dy = (y - s / 2) / (s / 2)
            dist = min(1.0, math.sqrt(dx * dx + dy * dy) / 1.414)
            mp[x, y] = int(150 * max(0.0, (dist - 0.35) / 0.65) ** 1.4)
    black = Image.new("RGBA", (s, s), (0, 0, 0, 255))
    black.putalpha(mask)
    img.alpha_composite(black)
    return img.convert("RGB")


def android_foreground(s=432):
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx = s // 2
    vp_y = 150
    # estrada em perspectiva
    d.polygon([(cx - 13, vp_y), (cx + 14, vp_y), (s - 8, s), (8, s)], fill=(18, 20, 22, 255))
    d.line([(cx - 12, vp_y), (12, s)], fill=(120, 106, 72, 255), width=2)
    d.line([(cx + 13, vp_y), (s - 12, s)], fill=(120, 106, 72, 255), width=2)
    # faixa central tracejada
    t = 0.06
    while t < 1.0:
        y = vp_y + int((s - vp_y) * (t ** 1.4))
        y2 = vp_y + int((s - vp_y) * (min(1.0, t + 0.06) ** 1.4))
        wdt = max(1, int(1 + 9 * (t ** 1.5)))
        d.rectangle([cx - wdt // 2, y, cx + wdt // 2, y2], fill=(196, 176, 120, 255))
        t += 0.13
    # vulto no meio da estrada
    _draw_figure_icon(d, cx, feet_y=304)
    return img


def presplash(w=1280, h=720):
    img = Image.new("RGB", (w, h), (6, 9, 13))
    d = ImageDraw.Draw(img)
    for y in range(h):
        d.line([(0, y), (w, y)], fill=lerp((4, 6, 10), (16, 24, 30), y / (h - 1)))

    vp = (w // 2, h // 2 - 40)
    d.polygon([(vp[0] - 10, vp[1]), (vp[0] + 11, vp[1]), (w + 140, h), (-140, h)], fill=(18, 20, 22))
    t = 0.05
    while t < 1.0:
        y = vp[1] + int((h - vp[1]) * (t ** 1.4))
        y2 = vp[1] + int((h - vp[1]) * (min(1.0, t + 0.05) ** 1.4))
        wdt = max(1, int(1 + 12 * (t ** 1.5)))
        d.rectangle([vp[0] - wdt // 2, y, vp[0] + wdt // 2, y2], fill=(150, 134, 96))
        t += 0.1

    # brilho âmbar no horizonte
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for i in range(30, 0, -1):
        frac = i / 30
        rr = 420 * frac
        a = int(70 * (1 - frac) ** 1.5)
        gd.ellipse([vp[0] - rr, vp[1] - rr * 0.4, vp[0] + rr, vp[1] + rr * 0.4], fill=(255, 178, 88, a))
    glow = glow.filter(ImageFilter.GaussianBlur(30))
    img = img.convert("RGBA")
    img.alpha_composite(glow)
    img = img.convert("RGB")
    d = ImageDraw.Draw(img)

    # título
    tf = ImageFont.truetype(os.path.join(FONTS, "JetBrainsMono-ExtraBold.ttf"), 92)
    sf = ImageFont.truetype(os.path.join(FONTS, "JetBrainsMono-Regular.ttf"), 26)
    d.text((w // 2, h // 2 - 40), "PONTO MORTO", fill=(238, 226, 198), font=tf, anchor="mm")
    d.line([(w // 2 - 220, h // 2 + 14), (w // 2 + 220, h // 2 + 14)], fill=(96, 78, 44), width=1)
    d.text((w // 2, h // 2 + 42), "KM 42  ·  BR-116  ·  03:07", fill=(150, 134, 100), font=sf, anchor="mm")

    # borda de 1px monocor (Ren'Py usa como cor de fundo da tela)
    d.rectangle([0, 0, w - 1, h - 1], outline=(6, 9, 13), width=1)
    return img


# ----------------------------------------------------------------------
#  UI (NÃO regenerar — já está finalizada)
# ----------------------------------------------------------------------
# main_menu.png, game_menu.png e window_icon.png ficam preservados como
# estão no repositório.

def main():
    exterior(seed=5).save(os.path.join(IMG, "bg_posto.png"))
    exterior(seed=5, dark=0.55).save(os.path.join(IMG, "bg_posto_escuro.png"))
    interior(seed=21).save(os.path.join(IMG, "bg_balcao.png"))

    make_glitch(interior(seed=21)).save(os.path.join(IMG, "bg_balcao_glitch.png"))
    make_glitch(exterior(seed=5)).save(os.path.join(IMG, "bg_posto_glitch.png"))

    road_scene(dawn=False).save(os.path.join(IMG, "bg_estrada.png"))
    road_scene(dawn=True).save(os.path.join(IMG, "bg_amanhecer.png"))

    cliente(False).save(os.path.join(IMG, "cliente.png"))
    cliente(True).save(os.path.join(IMG, "cliente_rosto.png"))

    # Ícone Android (adaptive) + presplash, na raiz do projeto
    android_background().save(os.path.join(ROOT, "android-icon_background.png"))
    android_foreground().save(os.path.join(ROOT, "android-icon_foreground.png"))
    presplash().save(os.path.join(ROOT, "android-presplash.jpg"), quality=90)

    print("imagens geradas em", IMG)
    print("ícones android + presplash na raiz do projeto")


if __name__ == "__main__":
    main()
