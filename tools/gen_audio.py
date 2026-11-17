#!/usr/bin/env python3
"""Sintetiza a trilha e os efeitos de Ponto Morto (sem samples externos)."""

import array
import math
import os
import random
import subprocess
import tempfile
import wave

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "game", "audio")
os.makedirs(OUT, exist_ok=True)

SR = 44100
TAU = math.tau


def write_wav(path, samples, peak=0.85):
    top = max(1e-9, max(abs(s) for s in samples))
    scale = peak / top
    data = array.array("h", (int(max(-1.0, min(1.0, s * scale)) * 32767) for s in samples))
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(data.tobytes())


def to_ogg(wav_path, ogg_path, quality=4):
    subprocess.run(
        ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
         "-i", wav_path, "-c:a", "libvorbis", "-q:a", str(quality), ogg_path],
        check=True,
    )


def seamless_noise(n, fade):
    """Ruído com o final dobrado sobre o começo, para loop sem clique."""
    rnd = random.Random(1234)
    buf = [rnd.uniform(-1.0, 1.0) for _ in range(n)]
    for i in range(fade):
        t = i / fade
        buf[n - fade + i] = buf[n - fade + i] * (1 - t) + buf[i] * t
    return buf


def lowpass(buf, a):
    y = 0.0
    out = [0.0] * len(buf)
    for i, x in enumerate(buf):
        y += a * (x - y)
        out[i] = y
    return out


def ambient(seed=1, dark=False):
    dur = 16
    n = dur * SR
    rnd = random.Random(seed)

    noise = seamless_noise(n, SR // 2)
    rumble = lowpass(noise, 0.012)
    hiss = lowpass(noise, 0.22)

    out = [0.0] * n
    # drones (frequências inteiras => loop exato)
    drones = [(55.0, 0.16, 1), (110.0, 0.07, 2), (165.0, 0.028, 3), (33.0, 0.10, 1)]
    if not dark:
        drones.append((220.0, 0.012, 2))

    for freq, amp, mod in drones:
        w = TAU * freq / SR
        mw = TAU * mod / dur
        ph = rnd.uniform(0, TAU)
        for i in range(n):
            am = 0.75 + 0.25 * math.sin(mw * i / SR + ph)
            out[i] += amp * am * math.sin(w * i + ph)

    for i in range(n):
        t = i / SR
        swell = 0.55 + 0.45 * math.sin(TAU * t / dur - math.pi / 2)
        out[i] += 0.30 * rumble[i] * (0.7 + 0.3 * swell)
        out[i] += 0.035 * hiss[i] * swell

    # pulsação elétrica lenta
    for i in range(n):
        out[i] *= 0.82 + 0.18 * math.sin(TAU * 2 * i / n)

    return out


def tension():
    dur = 12
    n = dur * SR
    rnd = random.Random(9)
    noise = seamless_noise(n, SR // 2)
    hiss = lowpass(noise, 0.35)
    out = [0.0] * n
    for i in range(n):
        t = i / SR
        beat = 0.5 + 0.5 * math.sin(TAU * (t * 6.0 / dur) * dur / dur)
        out[i] = (
            0.20 * math.sin(TAU * 58.0 * t)
            + 0.16 * math.sin(TAU * 61.5 * t + 1.1)
            + 0.06 * math.sin(TAU * 233.0 * t + 0.3) * (0.5 + 0.5 * math.sin(TAU * t / 3.0))
            + 0.05 * hiss[i]
        )
    return out


def bell():
    dur = 2.2
    n = int(dur * SR)
    out = [0.0] * n

    def strike(start, freq, amp):
        s = int(start * SR)
        for i in range(s, n):
            t = (i - s) / SR
            env = math.exp(-t * 3.2)
            out[i] += amp * env * (
                math.sin(TAU * freq * t)
                + 0.45 * math.sin(TAU * freq * 2.01 * t)
                + 0.22 * math.sin(TAU * freq * 3.93 * t)
                + 0.10 * math.sin(TAU * freq * 5.4 * t)
            )

    strike(0.00, 987.77, 0.5)
    strike(0.42, 783.99, 0.45)
    return out


def click():
    dur = 0.16
    n = int(dur * SR)
    rnd = random.Random(3)
    out = [0.0] * n
    for i in range(n):
        t = i / SR
        env = math.exp(-t * 60)
        out[i] = env * (0.7 * math.sin(TAU * 1850 * t) + 0.5 * rnd.uniform(-1, 1) * math.exp(-t * 220))
    return out


def heartbeat():
    dur = 1.15
    n = int(dur * SR)
    out = [0.0] * n

    def thump(start, amp):
        s = int(start * SR)
        for i in range(s, min(n, s + int(0.28 * SR))):
            t = (i - s) / SR
            env = math.exp(-t * 16)
            f = 62 - 18 * min(1.0, t / 0.18)
            out[i] += amp * env * math.sin(TAU * f * t)

    thump(0.00, 0.9)
    thump(0.30, 0.62)
    return out


def static():
    dur = 1.4
    n = int(dur * SR)
    rnd = random.Random(41)
    out = [0.0] * n
    for i in range(n):
        t = i / SR
        env = min(1.0, t / 0.03) * math.exp(-max(0.0, t - 0.2) * 3.0)
        v = rnd.uniform(-1, 1)
        v = round(v * 14) / 14  # bitcrush
        out[i] = env * (0.6 * v + 0.25 * math.sin(TAU * 60 * t))
    return out


def main():
    tmp = tempfile.mkdtemp(prefix="pontomorto-audio-")
    tracks = [
        ("ambiente", ambient(1), 4),
        ("ambiente_menu", ambient(2, dark=True), 4),
        ("tensao", tension(), 5),
        ("campainha", bell(), 5),
        ("clique", click(), 4),
        ("coracao", heartbeat(), 5),
        ("estatica", static(), 4),
    ]
    for name, samples, q in tracks:
        wav = os.path.join(tmp, name + ".wav")
        write_wav(wav, samples)
        to_ogg(wav, os.path.join(OUT, name + ".ogg"), q)
        print("ok", name)

    print("áudio gerado em", OUT)


if __name__ == "__main__":
    main()
