"""Sounds for the seventh batch, synthesised (no recordings were available for any of these):
   SFX\\Indev\\*.wav   mono 16-bit 22050 Hz, so the game can play them in 3D (LoadSound reads WAV)

   train_arrive  SCP-052 coming out of nowhere: rumble, a long brake squeal, the air letting go
   train_chime   the two-tone door chime          train_ride    a loopable rumble with the rail joints
   train_depart  the rumble going away            bark          two barks (the Hallway 99 kennels)
   foxhiss       SCP-953 dropping the disguise    applause      a studio audience nobody can see
   buzzer        wrong                            ding          right
   jingle        the SCP-024 theme                wind          confined wind (SCP-2701, before it takes you)
   pen           somebody writing on the INTAKE form
   puppet0..2    SCP-3325-1 "lines" (sing-song, formant-synthesised)
   creak         the building giving way round SCP-1440
   muffle        somebody struggling under a sheet (SCP-6096)
   doorbell      Freddy's door                    jukebox       a 50s loop for the diner"""
import os
import wave
import numpy as np

OUT = r"I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9\SFX\Indev"
SR = 22050
rng = np.random.default_rng(7)


def t_(sec):
    return np.arange(int(sec * SR)) / SR


def save(name, x, peak=0.85):
    x = np.asarray(x, dtype=np.float64)
    m = np.max(np.abs(x)) or 1.0
    x = x / m * peak
    # 4 ms fades so nothing clicks
    n = int(0.004 * SR)
    x[:n] *= np.linspace(0, 1, n)
    x[-n:] *= np.linspace(1, 0, n)
    os.makedirs(OUT, exist_ok=True)
    with wave.open(os.path.join(OUT, name + '.wav'), 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((x * 32767).astype('<i2').tobytes())
    return len(x) / SR


def lowpass(x, cut):
    """one-pole low pass, cut in Hz"""
    a = np.exp(-2 * np.pi * cut / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i, v in enumerate(x):
        acc = (1 - a) * v + a * acc
        y[i] = acc
    return y


def fft_band(x, lo, hi, soft=0.15):
    """band pass in the frequency domain (smooth edges)"""
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    g = np.clip((f - lo * (1 - soft)) / max(1.0, lo * soft * 2), 0, 1) * np.clip((hi * (1 + soft) - f) / max(1.0, hi * soft * 2), 0, 1)
    return np.fft.irfft(X * g, len(x))


def formant(x, freqs, bws, gains):
    """sum of resonances (frequency-domain gaussians) applied to x"""
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    g = np.zeros_like(f)
    for fc, bw, gn in zip(freqs, bws, gains):
        g += gn * np.exp(-0.5 * ((f - fc) / bw) ** 2)
    return np.fft.irfft(X * g, len(x))


def env(n, a, d):
    e = np.ones(n)
    na, nd = int(a * SR), int(d * SR)
    if na:
        e[:na] = np.linspace(0, 1, na)
    if nd:
        e[-nd:] *= np.linspace(1, 0, nd) ** 2
    return e


def glide(f0, f1, sec, shape=1.0):
    t = t_(sec)
    k = (t / sec) ** shape
    f = f0 + (f1 - f0) * k
    return np.cumsum(2 * np.pi * f / SR)


def harmonic(phase, amps):
    return sum(a * np.sin(phase * (i + 1)) for i, a in enumerate(amps))


# ------------------------------------------------------------------ the train
def rumble(sec, level=1.0):
    n = int(sec * SR)
    x = lowpass(rng.normal(0, 1, n), 90) * 6
    x += 0.5 * lowpass(rng.normal(0, 1, n), 300)
    return x * level


def clack(sec, rate):
    n = int(sec * SR)
    x = np.zeros(n)
    k = 0.0
    while k < sec:
        for off in (0.0, 0.11):           # two axles over each joint
            i = int((k + off) * SR)
            if i < n - 2000:
                b = rng.normal(0, 1, 1800) * np.exp(-np.arange(1800) / 260.0)
                x[i:i + 1800] += lowpass(b, 900) * 2.5
        k += 1.0 / rate
    return x


def train_arrive():
    sec = 6.0
    t = t_(sec)
    lvl = np.clip(t / 2.0, 0, 1) * np.clip((sec - t) / 1.2, 0.25, 1)
    x = rumble(sec) * lvl
    x += clack(sec, 2.2) * np.clip(t / 2.5, 0, 1) * np.clip((4.6 - t) / 2.0, 0, 1)
    # brake squeal: a thin tone that wanders, 2.2 s .. 5.0 s
    sq = np.zeros_like(t)
    m = (t > 2.2) & (t < 5.0)
    ph = np.cumsum(2 * np.pi * (2900 + 260 * np.sin(t * 7.0) + 120 * np.sin(t * 23.0)) / SR)
    sq[m] = np.sin(ph[m]) + 0.4 * np.sin(2.01 * ph[m])
    sq *= np.clip((t - 2.2) / 0.3, 0, 1) * np.clip((5.0 - t) / 0.4, 0, 1)
    x += sq * 0.35 * np.max(np.abs(x))
    # the air going out of the brakes at the stop
    m = t > 5.0
    hiss = fft_band(rng.normal(0, 1, len(t)), 2500, 7000)
    x[m] += hiss[m] * np.exp(-(t[m] - 5.0) / 0.35) * 0.6 * np.max(np.abs(x))
    return save('train_arrive', x)


def train_chime():
    t = t_(1.6)
    x = np.zeros_like(t)
    for (f, start) in ((659.3, 0.0), (523.3, 0.55)):
        m = t >= start
        tt = t[m] - start
        x[m] += (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(2 * np.pi * 2 * f * tt)) * np.exp(-tt / 0.45)
    return save('train_chime', x, 0.7)


def train_ride():
    sec = 4.0
    x = rumble(sec) + clack(sec, 2.0) * 0.8
    # make it loop: crossfade the end into the start
    n = int(0.25 * SR)
    x[:n] = x[:n] * np.linspace(0, 1, n) + x[-n:] * np.linspace(1, 0, n)
    return save('train_ride', x[:-n])


def train_depart():
    sec = 4.5
    t = t_(sec)
    x = rumble(sec) * np.clip(1 - t / sec, 0, 1) ** 1.5
    x += clack(sec, 2.6) * np.clip(1 - t / 3.0, 0, 1)
    whoosh = fft_band(rng.normal(0, 1, len(t)), 200, 1800) * np.exp(-((t - 1.2) / 0.6) ** 2) * 1.5
    return save('train_depart', x + whoosh * np.max(np.abs(x)) * 0.4)


# ------------------------------------------------------------------ animals
def one_bark(f0=520.0, sec=0.22):
    t = t_(sec)
    ph = glide(f0 * 1.15, f0 * 0.7, sec, 0.7)
    src = harmonic(ph, [1, 0.8, 0.7, 0.55, 0.4, 0.3, 0.22, 0.15])
    src += rng.normal(0, 0.6, len(t))
    e = np.minimum(t / 0.012, 1) * np.exp(-t / 0.075)
    y = formant(src * e, [700, 1300, 2400, 3300], [160, 220, 300, 400], [1.0, 0.7, 0.35, 0.2])
    return y


def bark():
    x = np.zeros(int(0.75 * SR))
    for start, f0 in ((0.0, 540.0), (0.36, 500.0)):
        b = one_bark(f0)
        i = int(start * SR)
        x[i:i + len(b)] += b
    return save('bark', x)


def foxhiss():
    sec = 1.3
    t = t_(sec)
    n = fft_band(rng.normal(0, 1, len(t)), 1800, 8000) * np.exp(-t / 0.5) * np.minimum(t / 0.03, 1)
    sc = harmonic(glide(1300, 900, sec, 0.5), [1, 0.5, 0.3]) * np.exp(-((t - 0.45) / 0.22) ** 2) * 0.5
    return save('foxhiss', n + sc)


# ------------------------------------------------------------------ the game show
def applause():
    sec = 4.0
    n = int(sec * SR)
    x = np.zeros(n)
    t = t_(sec)
    dens = np.clip(t / 0.4, 0, 1) * np.clip((sec - t) / 1.6, 0, 1)
    for _ in range(4200):
        p = rng.random() * sec
        if rng.random() > dens[min(n - 1, int(p * SR))]:
            continue
        i = int(p * SR)
        L = int(rng.uniform(0.004, 0.012) * SR)
        if i + L >= n:
            continue
        c = rng.normal(0, 1, L) * np.exp(-np.arange(L) / (L / 4.0))
        x[i:i + L] += fft_band(c, rng.uniform(600, 1500), rng.uniform(2500, 6000)) if L > 64 else c
    return save('applause', x, 0.7)


def buzzer():
    t = t_(0.8)
    ph = 2 * np.pi * 110 * t
    sq = np.sign(np.sin(ph)) * 0.6 + np.sign(np.sin(ph * 1.5 + 0.3)) * 0.4
    return save('buzzer', lowpass(sq, 2500) * env(len(t), 0.005, 0.05), 0.75)


def ding():
    t = t_(1.0)
    x = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t / d) for (f, a, d) in ((1046.5, 1, 0.5), (2093, 0.4, 0.25), (3140, 0.2, 0.12)))
    return save('ding', x, 0.7)


def jingle():
    notes = [(523.3, 0.0), (659.3, 0.18), (784.0, 0.36), (1046.5, 0.54), (784.0, 0.9), (1046.5, 1.08)]
    sec = 2.6
    t = t_(sec)
    x = np.zeros_like(t)
    for f, s in notes:
        m = t >= s
        tt = t[m] - s
        x[m] += (np.sin(2 * np.pi * f * tt) + 0.5 * np.sin(4 * np.pi * f * tt) + 0.25 * np.sign(np.sin(2 * np.pi * f * tt))) * np.exp(-tt / 0.35)
    # a brass-ish chord under the last two notes
    m = t > 0.9
    tt = t[m] - 0.9
    for f in (261.6, 329.6, 392.0):
        x[m] += 0.35 * np.sign(np.sin(2 * np.pi * f * tt)) * np.exp(-tt / 0.9)
    return save('jingle', lowpass(x, 5000), 0.7)


# ------------------------------------------------------------------ the rest
def wind():
    sec = 4.0
    t = t_(sec)
    n = rng.normal(0, 1, len(t))
    x = fft_band(n, 180, 900) * (0.6 + 0.4 * np.sin(2 * np.pi * t / sec) ** 2)
    x += 0.3 * fft_band(rng.normal(0, 1, len(t)), 1200, 2600) * (0.5 + 0.5 * np.sin(2 * np.pi * 3 * t / sec))
    k = int(0.3 * SR)
    x[:k] = x[:k] * np.linspace(0, 1, k) + x[-k:] * np.linspace(1, 0, k)
    return save('wind', x[:-k])


def pen():
    sec = 1.6
    t = t_(sec)
    x = fft_band(rng.normal(0, 1, len(t)), 2000, 7000)
    strokes = (np.sin(2 * np.pi * 5.5 * t + np.sin(2 * np.pi * 1.3 * t)) > 0.1).astype(float)
    return save('pen', x * lowpass(strokes, 40) * 1.0, 0.5)


VOWELS = {'a': ([800, 1200, 2600], [80, 90, 120]), 'e': ([400, 2200, 2900], [70, 100, 120]),
          'i': ([300, 2600, 3300], [60, 100, 120]), 'o': ([500, 900, 2500], [70, 80, 120]),
          'u': ([350, 800, 2400], [60, 80, 120])}


def sing(syllables, base):
    """formant-synthesised syllables: [(vowel, semitone, seconds)] - a high, too-bright puppet voice"""
    out = []
    for v, semi, sec in syllables:
        t = t_(sec)
        f0 = base * 2 ** (semi / 12.0)
        ph = np.cumsum(2 * np.pi * (f0 * (1 + 0.025 * np.sin(2 * np.pi * 6.5 * t))) / SR)
        src = harmonic(ph, [1 / (k + 1) for k in range(14)])
        fr, bw = VOWELS[v]
        fr = [f * 1.25 for f in fr]               # a smaller vocal tract than anyone's
        y = formant(src, fr, bw, [1.0, 0.6, 0.25]) * env(len(t), 0.02, 0.06)
        out.append(y)
        out.append(np.zeros(int(0.03 * SR)))
    return np.concatenate(out)


def puppets():
    lines = [[('e', 0, 0.16), ('i', 4, 0.16), ('a', 7, 0.28), ('o', 4, 0.16), ('a', 0, 0.4)],   # "let's-be-REAL to-day"
             [('u', 5, 0.18), ('a', 7, 0.14), ('a', 9, 0.14), ('u', 7, 0.5)],                    # "who wants a HUG"
             [('e', 0, 0.15), ('e', 0, 0.15), ('i', 2, 0.15), ('i', 4, 0.15), ('o', 7, 0.6)]]     # "say it with ME"
    for i, ln in enumerate(lines):
        save('puppet%d' % i, sing(ln, 330.0 + 30 * i), 0.7)


def creak():
    sec = 3.0
    t = t_(sec)
    ph = glide(70, 46, sec, 1.3)
    x = harmonic(ph, [1, 0.6, 0.5, 0.4, 0.3, 0.2]) * (0.5 + 0.5 * (rng.random(len(t)) > 0.97))
    x = lowpass(x, 600) * env(len(t), 0.4, 0.8)
    x += lowpass(rng.normal(0, 1, len(t)), 200) * 0.5 * env(len(t), 0.1, 1.0)
    return save('creak', x)


def muffle():
    sec = 3.0
    n = int(sec * SR)
    x = np.zeros(n)
    t = t_(sec)
    # muffled cries: a voice through a sheet
    for (s, d, f0) in ((0.1, 0.7, 260), (1.1, 0.9, 300), (2.2, 0.6, 240)):
        tt = t_(d)
        v = harmonic(glide(f0, f0 * 1.3, d, 0.6), [1, 0.7, 0.5, 0.3, 0.2]) * env(len(tt), 0.05, 0.2)
        i = int(s * SR)
        x[i:i + len(v)] += lowpass(v, 500)
    # thrashing
    for _ in range(9):
        i = int(rng.uniform(0, sec - 0.2) * SR)
        b = lowpass(rng.normal(0, 1, 3000), 300) * np.exp(-np.arange(3000) / 500.0) * 2
        x[i:i + 3000] += b
    return save('muffle', x, 0.7)


def doorbell():
    t = t_(1.2)
    x = np.zeros_like(t)
    for k in range(4):
        s = k * 0.07
        m = t >= s
        tt = t[m] - s
        x[m] += (np.sin(2 * np.pi * 2350 * tt) + 0.6 * np.sin(2 * np.pi * 3410 * tt)) * np.exp(-tt / 0.3) * (1 - 0.2 * k)
    return save('doorbell', x, 0.55)


def jukebox():
    bpm = 132.0
    beat = 60.0 / bpm
    prog = [(261.6, [0, 4, 7]), (220.0, [0, 3, 7]), (174.6, [0, 4, 7]), (196.0, [0, 4, 7])]   # I vi IV V in C
    sec = beat * 16
    t = t_(sec)
    x = np.zeros_like(t)
    for bar, (root, chord) in enumerate(prog):
        for b in range(4):
            s = (bar * 4 + b) * beat
            m = (t >= s) & (t < s + beat)
            tt = t[m] - s
            for iv in chord:     # chord stabs on every beat (piano-ish)
                f = root * 2 * 2 ** (iv / 12.0)
                x[m] += 0.25 * (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(4 * np.pi * f * tt)) * np.exp(-tt / 0.18)
            bf = root / 2 * (1.5 if b % 2 else 1.0)       # walking bass, root - fifth
            x[m] += 0.5 * np.sin(2 * np.pi * bf * tt) * np.exp(-tt / 0.3)
            if b % 2:            # backbeat brush
                x[m] += 0.15 * fft_band(rng.normal(0, 1, m.sum()), 3000, 8000) * np.exp(-tt / 0.05)
    # a little melody on top
    mel = [12, 14, 16, 19, 16, 14, 12, 9, 12, 9, 7, 9, 11, 14, 12, 11]
    for k, semi in enumerate(mel):
        s = k * beat
        m = (t >= s) & (t < s + beat * 0.9)
        tt = t[m] - s
        f = 261.6 * 2 ** (semi / 12.0)
        x[m] += 0.22 * np.sign(np.sin(2 * np.pi * f * tt)) * np.exp(-tt / 0.35) * (1 + 0.02 * np.sin(2 * np.pi * 5 * tt))
    x = lowpass(x, 3500)        # through an old cabinet
    return save('jukebox', x, 0.6)


if __name__ == '__main__':
    for fn in (train_arrive, train_chime, train_ride, train_depart, bark, foxhiss, applause, buzzer, ding, jingle,
               wind, pen, creak, muffle, doorbell, jukebox):
        print('%-14s %.2fs' % (fn.__name__, fn()))
    puppets()
    print('puppet0..2')
