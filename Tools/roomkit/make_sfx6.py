"""Sounds for the eighth batch, synthesised (SFX\\Indev\\*.wav, mono 16-bit 22050 Hz):
   choir        SCP-2983's marshmallows: five voices, bass to soprano, a short song in C
   geiger1/2    a Geiger counter, slow and fast (loopable)
   zap          a criticality flash: a hard electric snap and a hum that dies
   teletype     SCP-3355's printer        beep        a terminal beep
   bells        sleigh bells (SCP-4255)   timewarp    a temporal echo arriving
   fire         an incinerator roaring (loopable)
   crinkle      paper-mache moving (SCP-956)   thump   a package landing in a chute"""
import numpy as np
from make_sfx5 import save, t_, SR, lowpass, fft_band, formant, env, glide, harmonic, VOWELS, rng


def voice(f0, vowel, sec, bright=1.0):
    t = t_(sec)
    ph = np.cumsum(2 * np.pi * (f0 * (1 + 0.012 * np.sin(2 * np.pi * 5.2 * t))) / SR)
    src = harmonic(ph, [1 / (k + 1) ** (1.2 / bright) for k in range(16)])
    fr, bw = VOWELS[vowel]
    return formant(src, fr, bw, [1.0, 0.55, 0.22]) * env(len(t), 0.04, 0.12)


def choir():
    """the marshmallows sing: I - IV - V - I, five parts (fish bass ... candy soprano)"""
    C = 261.63
    chords = [[-24, -12, -5, 4, 12], [-19, -12, -3, 5, 12], [-17, -10, -5, 2, 11], [-24, -12, -8, 4, 16]]
    words = ['a', 'o', 'e', 'a']
    sec = 1.15
    out = []
    for ch, w in zip(chords, words):
        y = sum(voice(C * 2 ** (s / 12.0), w, sec, bright=1.0 + 0.15 * k) * (1.0 if k else 1.3) for k, s in enumerate(ch))
        out.append(y)
    # a little melodic tag on top, the soprano alone
    for s, w in ((16, 'i'), (14, 'e'), (12, 'a')):
        out.append(voice(C * 2 ** (s / 12.0), w, 0.32, 1.4) * 0.8)
    return save('choir', np.concatenate(out), 0.7)


def geiger(name, rate, sec=4.0):
    n = int(sec * SR)
    x = np.zeros(n)
    k = 0.0
    while True:
        k += rng.exponential(1.0 / rate)
        if k >= sec - 0.01:
            break
        i = int(k * SR)
        L = 160
        c = np.zeros(L)
        c[:6] = [1, -0.9, 0.7, -0.5, 0.3, -0.1]
        x[i:i + L] += lowpass(c * 1.0, 6000) * 3 + rng.normal(0, 0.05, L) * np.exp(-np.arange(L) / 30.0)
    return save(name, x, 0.6)


def zap():
    sec = 2.2
    t = t_(sec)
    snap = fft_band(rng.normal(0, 1, len(t)), 1500, 9000) * np.exp(-t / 0.05)
    hum = harmonic(2 * np.pi * 120 * t, [1, 0.6, 0.4, 0.3]) * np.exp(-t / 0.7) * 0.6
    return save('zap', snap * 1.5 + hum)


def teletype():
    sec = 2.4
    n = int(sec * SR)
    x = np.zeros(n)
    k = 0.0
    while k < sec - 0.05:
        i = int(k * SR)
        L = 700
        c = fft_band(rng.normal(0, 1, L), 900, 4000) * np.exp(-np.arange(L) / 120.0)
        x[i:i + L] += c
        k += rng.uniform(0.045, 0.09) + (0.3 if rng.random() < 0.06 else 0.0)
    return save('teletype', x, 0.6)


def beep():
    t = t_(0.22)
    return save('beep', np.sign(np.sin(2 * np.pi * 880 * t)) * env(len(t), 0.003, 0.02) * 0.5, 0.45)


def bells():
    sec = 2.6
    n = int(sec * SR)
    x = np.zeros(n)
    for k in range(26):
        s = k * 0.09 + rng.uniform(0, 0.03)
        i = int(s * SR)
        tt = t_(0.5)
        f = rng.choice([2300.0, 2650.0, 3100.0])
        b = (np.sin(2 * np.pi * f * tt) + 0.5 * np.sin(2 * np.pi * f * 2.76 * tt) + 0.3 * fft_band(rng.normal(0, 1, len(tt)), 4000, 9000)) * np.exp(-tt / 0.08)
        L = min(len(b), n - i)
        x[i:i + L] += b[:L] * (1 - k / 30.0)
    return save('bells', x, 0.6)


def timewarp():
    sec = 2.5
    t = t_(sec)
    sweep = np.sin(glide(1800, 90, sec, 0.6)) * np.exp(-((t - 1.0) / 0.7) ** 2)
    rev = fft_band(rng.normal(0, 1, len(t)), 300, 5000) * np.clip(t / 1.2, 0, 1) ** 2 * np.exp(-np.clip(t - 1.2, 0, None) / 0.15)
    return save('timewarp', sweep + rev * 0.8)


def fire():
    sec = 4.0
    t = t_(sec)
    x = lowpass(rng.normal(0, 1, len(t)), 400) * 4 + fft_band(rng.normal(0, 1, len(t)), 600, 3000) * (0.6 + 0.4 * np.sin(2 * np.pi * 1.7 * t) ** 2)
    for _ in range(60):
        i = int(rng.uniform(0, sec - 0.05) * SR)
        x[i:i + 600] += fft_band(rng.normal(0, 1, 600), 2000, 8000) * np.exp(-np.arange(600) / 80.0) * 3
    k = int(0.3 * SR)
    x[:k] = x[:k] * np.linspace(0, 1, k) + x[-k:] * np.linspace(1, 0, k)
    return save('fire', x[:-k])


def crinkle():
    sec = 1.2
    n = int(sec * SR)
    x = np.zeros(n)
    for _ in range(90):
        i = int(rng.uniform(0, sec - 0.02) * SR)
        L = int(rng.uniform(0.002, 0.008) * SR)
        x[i:i + L] += fft_band(rng.normal(0, 1, L), 2500, 9000) if L > 64 else rng.normal(0, 1, L)
    return save('crinkle', x * env(n, 0.05, 0.2), 0.5)


def thump():
    t = t_(0.7)
    body = np.sin(2 * np.pi * 70 * t) * np.exp(-t / 0.09)
    slap = lowpass(rng.normal(0, 1, len(t)), 1200) * np.exp(-t / 0.03)
    rattle = fft_band(rng.normal(0, 1, len(t)), 2000, 6000) * np.exp(-((t - 0.12) / 0.06) ** 2) * 0.3
    return save('thump', body + slap * 2 + rattle)


if __name__ == '__main__':
    print('choir', choir())
    print('geiger1', geiger('geiger1', 4.0))
    print('geiger2', geiger('geiger2', 40.0))
    for fn in (zap, teletype, beep, bells, timewarp, fire, crinkle, thump):
        print(fn.__name__, fn())
