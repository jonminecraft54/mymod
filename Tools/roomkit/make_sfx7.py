"""Sounds for the ninth batch, synthesised (SFX\\Indev\\*.wav, mono 16-bit 22050 Hz):
   scream457   SCP-457: superheated air forced through something like a throat
   mist        the misting sprinklers (loopable)        hose      an emergency hose opening up
   shutter     the blast shutter rattling down and seating
   clicks      D-016-1's echolocation                    uvhum     the UV decontamination lamps (loopable)
   page        a heavy vellum page turning (SCP-152)     drone280  SCP-280 close by (loopable)
   poof        something that was there no longer being there"""
import numpy as np
from make_sfx5 import save, t_, SR, lowpass, fft_band, env, glide, harmonic, rng


def loopable(x, sec=0.3):
    k = int(sec * SR)
    x = x.copy()
    x[:k] = x[:k] * np.linspace(0, 1, k) + x[-k:] * np.linspace(1, 0, k)
    return x[:-k]


def scream457():
    sec = 1.9
    t = t_(sec)
    whistle = np.sin(glide(1900, 3400, sec, 0.5)) * 0.5 + np.sin(glide(2850, 5100, sec, 0.5)) * 0.25
    air = fft_band(rng.normal(0, 1, len(t)), 2200, 8000)
    crack = np.zeros(len(t))
    for _ in range(40):
        i = int(rng.uniform(0, sec - 0.03) * SR)
        crack[i:i + 400] += fft_band(rng.normal(0, 1, 400), 1500, 7000) * np.exp(-np.arange(400) / 60.0) * 2
    shape = np.clip(t / 0.15, 0, 1) * np.exp(-np.clip(t - 1.3, 0, None) / 0.2)
    return save('scream457', (whistle * (0.7 + 0.3 * np.sin(2 * np.pi * 31 * t)) + air * 0.9 + crack * 0.5) * shape)


def mist():
    sec = 3.3
    t = t_(sec)
    x = fft_band(rng.normal(0, 1, len(t)), 3000, 9500) * (0.85 + 0.15 * np.sin(2 * np.pi * 0.7 * t))
    x += lowpass(rng.normal(0, 1, len(t)), 500) * 0.6
    return save('mist', loopable(x), 0.4)


def hose():
    sec = 2.4
    t = t_(sec)
    x = fft_band(rng.normal(0, 1, len(t)), 500, 5000) * 1.2 + lowpass(rng.normal(0, 1, len(t)), 200) * 3
    shape = np.clip(t / 0.08, 0, 1) * np.exp(-np.clip(t - 1.8, 0, None) / 0.2)
    return save('hose', x * shape)


def shutter():
    sec = 1.5
    n = int(sec * SR)
    x = np.zeros(n)
    k = 0.0
    while k < 1.0:
        i = int(k * SR)
        L = 500
        x[i:i + L] += fft_band(rng.normal(0, 1, L), 700, 3500) * np.exp(-np.arange(L) / 90.0)
        k += 0.045
    t = t_(0.45)
    slam = (np.sin(2 * np.pi * 62 * t) * 2 + lowpass(rng.normal(0, 1, len(t)), 900) * 2) * np.exp(-t / 0.09)
    i = int(1.02 * SR)
    x[i:i + len(slam)] += slam[:n - i] * 2.2
    return save('shutter', x)


def clicks():
    sec = 1.3
    n = int(sec * SR)
    x = np.zeros(n)
    k = 0.02
    gap = 0.16
    while k < sec - 0.02:
        i = int(k * SR)
        L = 90
        c = np.sin(2 * np.pi * 5200 * np.arange(L) / SR) * np.exp(-np.arange(L) / 14.0)
        x[i:i + L] += c
        gap = max(0.018, gap * 0.82)
        k += gap
    return save('clicks', x, 0.6)


def uvhum():
    sec = 3.3
    t = t_(sec)
    x = harmonic(2 * np.pi * 100 * t, [1, 0.5, 0.7, 0.2, 0.3, 0.1]) + fft_band(rng.normal(0, 1, len(t)), 6000, 9000) * 0.25
    x *= 0.9 + 0.1 * np.sin(2 * np.pi * 3 * t)
    return save('uvhum', loopable(x), 0.5)


def page():
    sec = 0.7
    t = t_(sec)
    x = fft_band(rng.normal(0, 1, len(t)), 1200, 7000) * np.exp(-((t - 0.25) / 0.16) ** 2)
    x += lowpass(rng.normal(0, 1, len(t)), 300) * np.exp(-((t - 0.52) / 0.03) ** 2) * 5
    return save('page', x, 0.5)


def drone280():
    sec = 4.3
    t = t_(sec)
    x = np.sin(2 * np.pi * 47 * t) + 0.8 * np.sin(2 * np.pi * 49.3 * t) + 0.4 * np.sin(2 * np.pi * 94 * t + np.sin(2 * np.pi * 0.4 * t))
    x += lowpass(rng.normal(0, 1, len(t)), 180) * 1.5
    breath = fft_band(rng.normal(0, 1, len(t)), 400, 1400) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.47 * t)) ** 3 * 0.35
    return save('drone280', loopable(x + breath), 0.7)


def poof():
    sec = 0.9
    t = t_(sec)
    x = fft_band(rng.normal(0, 1, len(t)), 200, 2500) * np.exp(-((t - 0.18) / 0.14) ** 2)
    x += np.sin(glide(240, 50, sec, 0.5)) * np.exp(-t / 0.25) * 0.8
    return save('poof', x, 0.6)


if __name__ == '__main__':
    for fn in (scream457, mist, hose, shutter, clicks, uvhum, page, drone280, poof):
        print(fn.__name__, round(fn(), 2))
