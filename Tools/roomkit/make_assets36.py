r"""Textures of the thirty-sixth batch (original, drawn here), after the user's reference images 115-131 and their
brief: 1024 HD concrete walls, 1024 industrial metal floors, 512 metal panels, dirt / scratch / warning decals.
  indev_b36conc.png    1024  poured concrete: formwork seams, tie holes, water stains, scuffs at the foot
  indev_b36floor.png   1024  industrial floor: worn diamond plate in bays, weld seams, oil, grime
  indev_b36panel.png    512  riveted steel wall panels, scratched, rust at the seams
  indev_b36scp.png      512  the red stencilled "SCP" (ref. 121) on concrete
  indev_b36grime.png    512  dirt and damp at the base of a wall (blends into the concrete)
  indev_b36warn.png     512  four warning labels (HIGH VOLTAGE, AUTHORIZED PERSONNEL, BIOHAZARD, NO NAKED FLAME)
  indev_b36feeds.png   1024  a monitor wall of 4 x 3 camera feeds (ref. 126)
  indev_b36road.png     512  bay floor: asphalt with lane markings and a hatched crossing (ref. 122)
  indev_b36bay.png      512  the big vehicle door: corrugated steel, hazard frame (ref. 122)
  indev_b36forest.png  1024  SCP-1479's taiga at night through fog (walls of the pocket space, ref. 131)
  indev_b36sky.png      256  the night sky, overcast
  indev_b36ground.png   512  taiga ground: needles, moss, mud
  indev_b36needle.png   256  pine needle masses (for the trees)
  indev_b36eyes.png     128  a pair of glowing eyes in the dark (alpha)
  indev_b36choc.png     256  SCP-3409-A: the chocolate fungus
   python make_assets36.py"""
import math
import os
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from make_assets5 import MAPDIR
from make_assets30 import F, FR

RND = random.Random(36)


def save(im, name):
    im.save(os.path.join(MAPDIR, name))


def noise(w, h, base, amp, seed, blur=1.0):
    a = np.random.default_rng(seed).normal(0, amp, (h, w, 1)).astype(np.float32) + np.array(base, np.float32)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(blur))


def stains(im, n, col, seed, alpha=50, rmax=80, streak=True):
    rnd = random.Random(seed)
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    W, H = im.size
    for _ in range(n):
        x, y = rnd.randrange(W), rnd.randrange(H)
        r = rnd.randint(10, rmax)
        d.ellipse([x - r, y - r * 0.6, x + r, y + r * 0.6], fill=col + (rnd.randint(alpha // 3, alpha),))
        if streak and rnd.random() < 0.4:
            d.rectangle([x - r // 6, y, x + r // 6, y + rnd.randint(60, 300)], fill=col + (rnd.randint(alpha // 4, alpha // 2),))
    return Image.alpha_composite(im.convert('RGBA'), ov.filter(ImageFilter.GaussianBlur(12))).convert('RGB')


def concrete():
    W = 1024
    im = noise(W, W, (124, 122, 116), 10, 3601, 1.4)
    fine = noise(W, W, (128, 128, 128), 16, 3602, 0.5)
    im = Image.blend(im, Image.composite(fine, im, Image.new('L', im.size, 70)), 0.4)
    d = ImageDraw.Draw(im)
    for y in range(0, W, 256):                                                  # formwork seams and tie holes
        d.line([(0, y + RND.randint(-2, 2)), (W, y + RND.randint(-2, 2))], fill=(96, 94, 88), width=3)
        for x in range(64, W, 256):
            d.ellipse([x - 7, y + 120, x + 7, y + 134], fill=(62, 60, 56))
            d.ellipse([x - 4, y + 123, x + 3, y + 130], fill=(44, 42, 40))
    for x in range(0, W, 512):
        d.line([(x, 0), (x, W)], fill=(100, 98, 92), width=2)
    im = stains(im, 40, (70, 64, 52), 3603, alpha=60)
    d = ImageDraw.Draw(im)
    for _ in range(300):                                                        # scuffs near the foot
        x, y = RND.randrange(W), RND.randint(W - 140, W - 2)
        d.line([(x, y), (x + RND.randint(-30, 30), y + RND.randint(-4, 4))], fill=(92, 90, 84), width=1)
    save(im, 'indev_b36conc.png')


def floor():
    W = 1024
    im = noise(W, W, (84, 86, 88), 8, 3604, 0.8)
    d = ImageDraw.Draw(im)
    for by in range(0, W, 256):                                                 # bays of diamond plate
        for bx in range(0, W, 256):
            for y in range(by + 8, by + 248, 22):
                for x in range(bx + 8 + ((y // 22) % 2) * 11, bx + 248, 22):
                    d.line([(x, y), (x + 8, y + 5)], fill=(116, 118, 120), width=3)
                    d.line([(x + 1, y + 1), (x + 9, y + 6)], fill=(60, 62, 64), width=1)
            d.rectangle([bx, by, bx + 255, by + 255], outline=(52, 52, 54), width=4)
            for (cx, cy) in ((bx + 10, by + 10), (bx + 246, by + 10), (bx + 10, by + 246), (bx + 246, by + 246)):
                d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(140, 140, 140))
    im = stains(im, 30, (30, 26, 20), 3605, alpha=90, rmax=90, streak=False)     # oil
    im = stains(im, 40, (96, 82, 60), 3606, alpha=50, rmax=60, streak=False)     # grime
    save(im, 'indev_b36floor.png')


def panel():
    im = noise(512, 512, (100, 104, 106), 9, 3607, 1.0)
    d = ImageDraw.Draw(im)
    for k in range(0, 512, 256):
        d.rectangle([k + 2, 2, k + 253, 509], outline=(60, 62, 64), width=4)
        for y in range(16, 512, 48):
            for x in (k + 14, k + 242):
                d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=(140, 142, 140))
                d.ellipse([x - 2, y - 2, x + 3, y + 3], fill=(70, 70, 70))
    for _ in range(120):
        x, y = RND.randrange(512), RND.randrange(512)
        d.line([(x, y), (x + RND.randint(-40, 40), y + RND.randint(-6, 6))], fill=(150, 152, 150), width=1)
    im = stains(im, 18, (120, 60, 30), 3608, alpha=70, rmax=40)                 # rust at the seams
    save(im, 'indev_b36panel.png')


def stencil():
    im = Image.new('RGBA', (512, 256), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.text((256, 128), 'SCP', font=F(200), fill=(170, 40, 34, 230), anchor='mm')
    a = np.array(im)
    rng = np.random.default_rng(3609)
    mask = rng.random(a.shape[:2]) < 0.18                                       # worn paint
    a[mask, 3] = (a[mask, 3] * 0.35).astype(np.uint8)
    save(Image.fromarray(a), 'indev_b36scp.png')


def grime():
    im = Image.new('RGBA', (512, 256), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for _ in range(80):
        x = RND.randrange(512)
        h = RND.randint(30, 200)
        d.ellipse([x - RND.randint(10, 40), 256 - h, x + RND.randint(10, 40), 280], fill=(40, 36, 28, RND.randint(30, 80)))
    save(im.filter(ImageFilter.GaussianBlur(8)), 'indev_b36grime.png')


def warnings():
    sheet = Image.new('RGB', (512, 512), (0, 0, 0))
    rows = [((240, 200, 20), 'HIGH VOLTAGE', 'DANGER OF DEATH'), ((240, 240, 236), 'AUTHORIZED', 'PERSONNEL ONLY'),
            ((240, 200, 20), 'BIOHAZARD', 'SEALED CONTAINMENT'), ((200, 30, 30), 'NO NAKED FLAME', 'SUGAR DUST')]
    for k, (bg, a, b) in enumerate(rows):
        im = Image.new('RGB', (256, 256), bg)
        d = ImageDraw.Draw(im)
        d.rectangle([6, 6, 249, 249], outline=(20, 20, 20), width=8)
        d.polygon([(128, 30), (196, 140), (60, 140)], outline=(20, 20, 20), fill=None, width=8)
        d.text((128, 104), '!', font=F(60), fill=(20, 20, 20), anchor='mm')
        fg = (20, 20, 20) if bg != (200, 30, 30) else (255, 255, 255)
        d.text((128, 180), a, font=F(26), fill=fg, anchor='mm')
        d.text((128, 214), b, font=F(18), fill=fg, anchor='mm')
        im = Image.blend(im, noise(256, 256, (120, 110, 90), 20, 3610 + k, 1.5), 0.18)
        sheet.paste(im, ((k % 2) * 256, (k // 2) * 256))
    save(sheet, 'indev_b36warn.png')


def feeds():
    sheet = Image.new('RGB', (1024, 768), (10, 10, 12))
    for k in range(12):
        x0, y0 = (k % 4) * 256, (k // 4) * 256
        im = noise(240, 180, (60, 64, 62), 14, 3620 + k, 1.2)
        d = ImageDraw.Draw(im)
        vp = (120 + RND.randint(-30, 30), 70)
        for (a, b) in (((0, 180), vp), ((240, 180), vp), ((0, 0), vp), ((240, 0), vp)):
            d.line([a, b], fill=(110, 114, 110), width=2)
        d.rectangle([vp[0] - 18, vp[1] - 14, vp[0] + 18, vp[1] + 14], fill=(30, 30, 30))
        if k in (3, 8):
            d.rectangle([vp[0] - 4, vp[1] + 14, vp[0] + 4, vp[1] + 40], fill=(16, 16, 16))     # someone standing
        if k == 6:
            im = noise(240, 180, (14, 14, 14), 30, 3640, 0.3)                    # a dead feed
            d = ImageDraw.Draw(im)
        d.text((8, 6), 'CAM %02d' % (k + 1), font=F(14), fill=(220, 220, 220))
        d.text((8, 160), '03:17:%02d' % (k * 4), font=F(12, FR), fill=(200, 200, 200))
        frame = Image.new('RGB', (256, 256), (16, 16, 18))
        frame.paste(im, (8, 38))
        sheet.paste(frame, (x0, y0))
    save(sheet, 'indev_b36feeds.png')


def road():
    im = noise(512, 512, (52, 52, 54), 8, 3650, 0.8)
    d = ImageDraw.Draw(im)
    for y in range(20, 512, 80):
        d.rectangle([250, y, 262, y + 40], fill=(210, 210, 200))
    im = stains(im, 20, (20, 18, 14), 3651, alpha=80, rmax=60, streak=False)
    save(im, 'indev_b36road.png')
    h = noise(512, 128, (52, 52, 54), 8, 3652, 0.8)
    d = ImageDraw.Draw(h)
    for x in range(-60, 512, 40):
        d.polygon([(x, 0), (x + 20, 0), (x + 60, 128), (x + 40, 128)], fill=(205, 205, 196))
    save(h, 'indev_b36cross.png')


def baydoor():
    im = noise(512, 512, (120, 122, 120), 6, 3653, 0.8)
    d = ImageDraw.Draw(im)
    for y in range(40, 512, 18):
        d.line([(40, y), (472, y)], fill=(80, 82, 80), width=3)
        d.line([(40, y + 3), (472, y + 3)], fill=(150, 152, 150), width=1)
    for k in range(0, 1024, 40):                                                # hazard frame
        d.polygon([(k - 512, 0), (k - 492, 0), (k - 532, 40), (k - 552, 40)], fill=(20, 20, 20))
    d.rectangle([0, 0, 511, 40], fill=(230, 190, 20))
    d.rectangle([0, 0, 40, 511], fill=(230, 190, 20))
    d.rectangle([472, 0, 511, 511], fill=(230, 190, 20))
    for k in range(-40, 600, 30):
        d.line([(k, 0), (k - 40, 40)], fill=(20, 20, 20), width=10)
        d.line([(0, k), (40, k - 40)], fill=(20, 20, 20), width=10)
        d.line([(472, k), (512, k - 40)], fill=(20, 20, 20), width=10)
    d.text((256, 470), 'VEHICLE BAY 3 - KEEP CLEAR', font=F(28), fill=(240, 240, 240), anchor='mm')
    save(stains(im, 14, (60, 50, 40), 3654, alpha=60), 'indev_b36bay.png')


def forest():
    """ref. 131: black pines in layers of fog, a few lighter trunks, the ground line"""
    W, H = 1024, 512
    im = Image.new('RGB', (W, H), (40, 42, 44))
    d = ImageDraw.Draw(im)
    for y in range(H):
        g = int(26 + 26 * (y / H))
        d.line([(0, y), (W, y)], fill=(g, g + 2, g + 2))
    for layer, (col, n, hmin) in enumerate((((54, 58, 58), 22, 260), ((34, 38, 36), 18, 330), ((16, 18, 17), 14, 420))):
        for _ in range(n):
            x = RND.randrange(-40, W + 40)
            h = RND.randint(hmin, H)
            base = H - RND.randint(10, 40) + layer * 10
            w = RND.randint(50, 110) + layer * 20
            for k in range(7):                                                  # tiers of a pine
                yy = base - h + k * h / 8
                ww = w * (k + 1) / 7
                d.polygon([(x, yy - 20), (x - ww / 2, yy + h / 7), (x + ww / 2, yy + h / 7)], fill=col)
            d.rectangle([x - 4 - layer * 2, base - h * 0.2, x + 4 + layer * 2, base], fill=col)
        im = im.filter(ImageFilter.GaussianBlur(2.5 - layer))
        d = ImageDraw.Draw(im)
    d.rectangle([0, H - 30, W, H], fill=(14, 16, 14))
    save(im, 'indev_b36forest.png')
    save(noise(256, 256, (22, 24, 26), 6, 3660, 4.0), 'indev_b36sky.png')
    g = noise(512, 512, (46, 42, 32), 14, 3661, 1.0)
    d = ImageDraw.Draw(g)
    for _ in range(1600):
        x, y = RND.randrange(512), RND.randrange(512)
        d.line([(x, y), (x + RND.randint(-6, 6), y + RND.randint(-6, 6))], fill=(70, 58, 38), width=1)
    g = stains(g, 30, (40, 60, 34), 3662, alpha=90, rmax=60, streak=False)
    save(g, 'indev_b36ground.png')
    nd = noise(256, 256, (28, 44, 30), 18, 3663, 0.6)
    save(nd, 'indev_b36needle.png')


def eyes():
    im = Image.new('RGBA', (128, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for x in (34, 94):
        d.ellipse([x - 16, 22, x + 16, 42], fill=(255, 230, 160, 255))
        d.ellipse([x - 5, 26, x + 5, 38], fill=(40, 20, 10, 255))
    save(im.filter(ImageFilter.GaussianBlur(1.2)), 'indev_b36eyes.png')


def choc():
    im = noise(256, 256, (70, 40, 24), 18, 3670, 1.0)
    d = ImageDraw.Draw(im)
    for _ in range(60):
        x, y = RND.randrange(256), RND.randrange(256)
        d.line([(x, y), (x + RND.randint(-60, 60), y + RND.randint(-60, 60))], fill=(110, 66, 40), width=RND.randint(2, 6))
    save(im, 'indev_b36choc.png')


if __name__ == '__main__':
    concrete(); floor(); panel(); stencil(); grime(); warnings(); feeds(); road(); baydoor(); forest(); eyes(); choc()
    print('batch 36 textures written')
