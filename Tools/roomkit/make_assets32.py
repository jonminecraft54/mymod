r"""Textures of the thirty-second batch, Gate V (original, drawn here): the GATE V sign (in the style of the game's gate
signs: a black plate, our emblem, white letters), green emergency-exit signs, stairwell level markers, the mountain
view through the exit portal (sky, clouds, snowfields, jagged peaks), the skylight's sky, the alarm breaker box, the
break-glass release, the exit console screen, the red frame band, dark gallery windows.
   python make_assets32.py"""
import math
import os
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from make_assets5 import MAPDIR
from make_assets30 import F, FR, FM, emblem

RND = random.Random(32)


def save(im, name):
    im.save(os.path.join(MAPDIR, name))


def gate_sign():
    im = Image.new('RGB', (1024, 256), (18, 18, 20))
    d = ImageDraw.Draw(im)
    for _ in range(3000):                                       # worn paint
        x, y = RND.randrange(1024), RND.randrange(256)
        c = RND.randint(28, 46)
        d.point((x, y), fill=(c, c, c))
    d.rectangle([6, 6, 1017, 249], outline=(70, 70, 74), width=6)
    cx, cy, r, col = 150, 128, 92, (225, 225, 225)                # our emblem: a ring and three inward arrows
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=10)
    d.ellipse([cx - r * 0.42, cy - r * 0.42, cx + r * 0.42, cy + r * 0.42], outline=col, width=8)
    for k in range(3):
        a = math.radians(90 + k * 120)
        x0, y0 = cx + math.cos(a) * r * 0.95, cy - math.sin(a) * r * 0.95
        x1, y1 = cx + math.cos(a) * r * 0.5, cy - math.sin(a) * r * 0.5
        d.line([(x0, y0), (x1, y1)], fill=col, width=10)
        b1, b2 = a + 2.5, a - 2.5
        d.polygon([(x1, y1), (x1 + math.cos(b1) * 22, y1 - math.sin(b1) * 22), (x1 + math.cos(b2) * 22, y1 - math.sin(b2) * 22)], fill=col)
    d.text((620, 128), 'GATE V', font=F(150), fill=(235, 235, 235), anchor='mm')
    save(im.filter(ImageFilter.GaussianBlur(0.5)), 'indev_gatev_sign.png')


def exit_signs():
    im = Image.new('RGB', (512, 192), (20, 140, 70))
    d = ImageDraw.Draw(im)
    d.rectangle([6, 6, 505, 185], outline=(240, 255, 240), width=6)
    d.text((300, 70), 'EMERGENCY EXIT', font=F(46), fill=(255, 255, 255), anchor='mm')
    d.text((300, 132), 'GATE V  -  UNDERGROUND', font=F(28), fill=(220, 255, 230), anchor='mm')
    d.polygon([(30, 96), (90, 50), (90, 76), (140, 76), (140, 116), (90, 116), (90, 142)], fill=(255, 255, 255))
    save(im, 'indev_gatev_exit.png')
    im = Image.new('RGB', (512, 256), (230, 190, 30))
    d = ImageDraw.Draw(im)
    d.rectangle([6, 6, 505, 249], outline=(20, 20, 20), width=8)
    d.text((256, 70), 'AUTHORISED EVACUATION', font=F(36), fill=(20, 20, 20), anchor='mm')
    d.text((256, 120), 'ONLY', font=F(42), fill=(20, 20, 20), anchor='mm')
    d.text((256, 190), 'break glass = security alert', font=F(26, FR), fill=(120, 20, 20), anchor='mm')
    save(im, 'indev_gatev_warn.png')
    sheet = Image.new('RGB', (1024, 256), (230, 230, 226))
    d = ImageDraw.Draw(sheet)
    for k, t in enumerate(('LEVEL 0', '-1', '-2', '-3')):
        x0 = k * 256
        d.rectangle([x0 + 8, 8, x0 + 248, 248], outline=(20, 20, 20), width=8)
        d.text((x0 + 128, 128), t, font=F(70 if k else 46), fill=(20, 20, 20), anchor='mm')
    save(sheet, 'indev_gatev_levels.png')


def mountains():
    """the view through the exit portal: a high sky, clouds, two ranges of snowy peaks, a snowfield"""
    W, H = 1024, 768
    a = np.zeros((H, W, 3), np.float32)
    for y in range(H):
        k = y / H
        a[y] = (40 + 140 * k, 100 + 120 * k, 200 + 40 * k)
    im = Image.fromarray(a.clip(0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im, 'RGBA')
    for _ in range(26):                                         # clouds
        cx, cy = RND.randrange(W), RND.randint(20, 300)
        for _ in range(9):
            r = RND.randint(14, 40)
            ox, oy = RND.randint(-60, 60), RND.randint(-12, 12)
            d.ellipse([cx + ox - r * 1.6, cy + oy - r * 0.7, cx + ox + r * 1.6, cy + oy + r * 0.7], fill=(255, 255, 255, 90))

    a = np.asarray(im, np.float32)
    rng = np.random.default_rng(32)

    def profile(base, amp, seed):
        r = np.random.default_rng(seed)
        n = 1025
        h = np.zeros(n)
        step, scale = n - 1, amp
        h[0], h[-1] = r.uniform(-1, 1) * amp * 0.5, r.uniform(-1, 1) * amp * 0.5
        while step > 1:                                          # midpoint displacement: a jagged ridge line
            half = step // 2
            for i in range(half, n - 1, step):
                h[i] = (h[i - half] + h[i + half]) / 2 + r.uniform(-1, 1) * scale
            step, scale = half, scale * 0.55
        return base - (h - h.min()) * 0.9
    yy = np.arange(H)[:, None].astype(np.float32)
    for base, amp, rock, snowline, seed in ((520, 300, (104, 112, 130), 0.55, 11), (600, 200, (74, 80, 94), 0.45, 12)):
        top = profile(base, amp, seed)[:W][None, :]
        sm = np.convolve(top[0], np.ones(21) / 21, mode='same')
        slope = np.gradient(sm)[None, :]
        mask = yy >= top
        shade = np.clip(0.85 + slope * 0.35, 0.5, 1.2) * np.clip(1.0 - (yy - top) / 900.0, 0.6, 1.0)   # sun from the left
        grain = np.asarray(Image.fromarray((rng.random((H, W)) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2.5)), np.float32)[..., None] / 255.0
        col = np.array(rock, np.float32)[None, None, :] * shade[..., None] * (0.8 + 0.4 * grain)
        depth = (yy - top) / max(1.0, amp)
        line = snowline * (0.45 + 0.35 * np.sin(np.arange(W)[None, :] / 37.0 + seed) ** 2) + 0.08 * (grain[..., 0] - 0.5)
        snow = (depth < line) & mask & (slope < 3.5)
        snowc = np.array((240, 244, 250), np.float32)[None, None, :] * np.clip(shade, 0.7, 1.05)[..., None]
        a = np.where(mask[..., None], np.where(snow[..., None], snowc, col), a)
    im = Image.fromarray(a.clip(0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im, 'RGBA')
    d.rectangle([0, 640, W, H], fill=(244, 246, 250, 255))   # the snowfield
    for _ in range(160):
        x, y = RND.randrange(W), RND.randint(600, H)
        d.ellipse([x, y, x + RND.randint(6, 30), y + 3], fill=(210, 216, 228, 255))
    save(im.filter(ImageFilter.GaussianBlur(0.8)), 'indev_gatev_mountains.png')
    sky = Image.new('RGB', (512, 512), (90, 150, 220))
    d = ImageDraw.Draw(sky, 'RGBA')
    for _ in range(40):
        cx, cy, r = RND.randrange(512), RND.randrange(512), RND.randint(20, 60)
        d.ellipse([cx - r * 1.5, cy - r * 0.6, cx + r * 1.5, cy + r * 0.6], fill=(255, 255, 255, 110))
    save(sky.filter(ImageFilter.GaussianBlur(2)), 'indev_gatev_sky.png')


def panels():
    b = Image.new('RGB', (256, 384), (150, 150, 140))
    d = ImageDraw.Draw(b)
    d.rectangle([6, 6, 249, 377], outline=(60, 60, 56), width=6)
    d.text((128, 40), 'GATE V ALARM', font=F(26), fill=(30, 30, 30), anchor='mm')
    d.text((128, 70), 'CIRCUIT 7-V', font=F(20, FR), fill=(30, 30, 30), anchor='mm')
    d.rectangle([90, 110, 166, 270], fill=(40, 40, 40))
    d.rectangle([100, 120, 156, 180], fill=(200, 40, 30))    # the breaker handle, up
    d.text((128, 300), 'DO NOT CUT', font=F(26), fill=(160, 20, 20), anchor='mm')
    d.text((128, 336), 'DURING DRILLS', font=F(20, FR), fill=(30, 30, 30), anchor='mm')
    save(b, 'indev_gatev_breaker.png')
    g = Image.new('RGB', (256, 256), (190, 20, 20))
    d = ImageDraw.Draw(g)
    d.rectangle([6, 6, 249, 249], outline=(255, 255, 255), width=6)
    d.rectangle([40, 60, 216, 196], fill=(230, 240, 245))
    d.ellipse([98, 98, 158, 158], fill=(200, 30, 30))
    d.text((128, 34), 'EMERGENCY RELEASE', font=F(20), fill=(255, 255, 255), anchor='mm')
    d.text((128, 224), 'BREAK GLASS', font=F(24), fill=(255, 255, 255), anchor='mm')
    save(g, 'indev_gatev_glass.png')
    c = Image.new('RGB', (384, 256), (10, 20, 14))
    d = ImageDraw.Draw(c)
    for k, (t, col) in enumerate((('GATE V  STATUS', (140, 240, 150)), ('HATCH: OPEN', (140, 240, 150)),
                                  ('SEAL CHARGES: ARMED', (240, 200, 90)), ('ALARM CIRCUIT 7-V', (140, 240, 150)),
                                  ('> DETONATE ONLY IF', (240, 90, 80)), ('  HOSTILES AT HATCH', (240, 90, 80)))):
        d.text((18, 16 + k * 38), t, font=F(24, FM), fill=col)
    save(c, 'indev_gatev_console.png')
    band = Image.new('RGB', (256, 64), (120, 20, 22))
    d = ImageDraw.Draw(band)
    for x in range(0, 256, 8):
        d.line([(x, 0), (x, 64)], fill=(100, 16, 18))
    save(band, 'indev_gatev_band.png')
    win = Image.new('RGB', (256, 192), (16, 20, 24))
    d = ImageDraw.Draw(win)
    d.rectangle([0, 0, 255, 191], outline=(70, 72, 76), width=10)
    d.line([(30, 150), (110, 40)], fill=(40, 48, 56), width=6)
    save(win, 'indev_gatev_window.png')


if __name__ == '__main__':
    gate_sign()
    exit_signs()
    mountains()
    panels()
    print('batch 32 textures written')
