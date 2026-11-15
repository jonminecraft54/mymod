r"""High-detail models for batch 31 (original work after scp-wiki.wikidot.com/scp-467, /scp-178, /scp-198, /scp-207,
/scp-1079 and /scp-1650, CC BY-SA 3.0):
Props (GFX\map\props, room units):
  scp467.b3d      the confessional phone booth: weathered green steel, a plinth, corner posts, a grid of glazed panes,
                  a folding door standing ajar, the lit roof sign, a shelf, and on the back wall the empty mounting
                  plate where the old phone hung, a cut cord and four screw holes
  scp178e.b3d     an SCP-178 entity: a gaunt, very tall biped, long arms, three long tapered claws on each hand, a
                  small eyeless head tilted in curiosity
  scp207crate.b3d the wooden crate of 24 bottles
Items (GFX\items, cm units):
  scp178.b3d      white cardboard 3-D glasses, red and blue lenses, temples folded out
  scp198.b3d      a white porcelain mug with blue vertical stripes
  scp207.b3d      a glass cola bottle, label SCP-207-B, cap
  scp1079.b3d     a packet of Dr. Wondertainment's Bubblebath Bonbons, torn open, pink sweets spilling out
  scp1650.b3d     a Hasmonean-period clay oil pot: a squat jar with a spout, a handle, a worn inscription band
   python make_hd31.py"""
import math
import os
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from make_hd29 import Model, grid, tube, lathe, card, nrm, cross, sub, add, render, ITEMS, PROPS, PREV
from make_hd30 import blob, quad, xform, rot, noise_tex, F, FB, FR

RND = random.Random(31)


def save(im, folder, name):
    im.save(os.path.join(folder, name))


def boxq(s, x0, y0, z0, x1, y1, z1, uvs=1.0):
    """a box of six quads (bl br tr tl as seen from outside each face)"""
    def uv(a, b):
        return (0, 0, a * uvs, b * uvs)
    w, h, d = x1 - x0, y1 - y0, z1 - z0
    quad(s, (x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), uv(w, h))      # -z face
    quad(s, (x1, y0, z1), (x0, y0, z1), (x0, y1, z1), (x1, y1, z1), uv(w, h))      # +z face
    quad(s, (x0, y0, z1), (x0, y0, z0), (x0, y1, z0), (x0, y1, z1), uv(d, h))      # -x face
    quad(s, (x1, y0, z0), (x1, y0, z1), (x1, y1, z1), (x1, y1, z0), uv(d, h))      # +x face
    quad(s, (x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1), uv(w, d))      # top
    quad(s, (x0, y0, z1), (x1, y0, z1), (x1, y0, z0), (x0, y0, z0), uv(w, d))      # bottom


# ============================================================================ SCP-467: the booth
def booth():
    g = noise_tex(256, (52, 84, 64), 8, 0.6, 467)
    d = ImageDraw.Draw(g)
    for _ in range(45):                                      # chipped paint and rust
        x, y = RND.randrange(256), RND.randrange(256)
        r = RND.randint(2, 7)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(96, 64, 40) if RND.random() < 0.6 else (110, 120, 108))
    save(g.filter(ImageFilter.GaussianBlur(0.5)), PROPS, 's467_paint.png')
    save(noise_tex(128, (200, 220, 220), 6, 1.0, 4671), PROPS, 's467_glass.png')
    sg = Image.new('RGB', (512, 96), (20, 24, 22))
    d = ImageDraw.Draw(sg)
    d.text((256, 48), 'TELEPHONE', font=F(60), fill=(255, 248, 220), anchor='mm')
    save(sg, PROPS, 's467_sign.png')
    pl = noise_tex(128, (150, 150, 146), 8, 0.5, 4672)
    d = ImageDraw.Draw(pl)
    for (x, y) in ((16, 16), (112, 16), (16, 112), (112, 112)):
        d.ellipse([x - 6, y - 6, x + 6, y + 6], fill=(30, 30, 30))
    d.rectangle([40, 20, 88, 100], outline=(110, 110, 104), width=3)                    # the ghost of the phone
    save(pl, PROPS, 's467_plate.png')
    save(noise_tex(64, (30, 30, 30), 6, 0.5, 4673), PROPS, 's467_dark.png')
    save(Image.new('RGB', (32, 32), (255, 244, 210)), PROPS, 's467_lamp.png')
    M = Model()
    paint = M.surf('paint', 's467_paint.png', shine=0.35)
    glass = M.surf('glass', 's467_glass.png', shine=1.0, alpha=0.3)
    sign = M.surf('sign', 's467_sign.png', fx=1)
    plate = M.surf('plate', 's467_plate.png', shine=0.6)
    dark = M.surf('dark', 's467_dark.png')
    lamp = M.surf('lamp', 's467_lamp.png', fx=1)
    W, H = 75.0, 330.0                                       # half width; height (room units, door on -z)
    boxq(paint, -W - 6, 0, -W - 6, W + 6, 12, W + 6, 1 / 64.0)                          # the plinth
    for (x, z) in ((-W, -W), (W, -W), (W, W), (-W, W)):                                 # corner posts
        boxq(paint, x - 6, 12, z - 6, x + 6, H - 30, z + 6, 1 / 64.0)
    boxq(paint, -W - 8, H - 30, -W - 8, W + 8, H - 6, W + 8, 1 / 64.0)                  # the roof band
    boxq(paint, -W + 4, H - 6, -W + 4, W - 4, H, W - 4, 1 / 64.0)                       # roof cap
    for side in range(4):                                                               # signs on all four faces
        f = rot('y', side * 90)
        k = len(sign.V)
        quad(sign, (-W + 6, H - 28, -W - 8.5), (W - 6, H - 28, -W - 8.5), (W - 6, H - 8, -W - 8.5), (-W + 6, H - 8, -W - 8.5))
        xform(sign, k, f)
    # three walls of glazed panes: 3 x 4 panes in glazing bars; the door (on -z) is two folding leaves, ajar
    def wall(f, door=False):
        k0, kg = len(paint.V), len(glass.V)
        for r in range(5):                                                              # horizontal bars
            y = 40 + r * (H - 80) / 4
            boxq(paint, -W + 6, y - 3, -W - 3, W - 6, y + 3, -W + 3, 1 / 64.0)
        for c in (-W / 3, W / 3):                                                       # vertical bars
            boxq(paint, c - 2.5, 40, -W - 3, c + 2.5, H - 40, -W + 3, 1 / 64.0)
        boxq(paint, -W + 6, 12, -W - 3, W - 6, 40, -W + 3, 1 / 64.0)                    # the kick panel
        quad(glass, (-W + 6, 40, -W), (W - 6, 40, -W), (W - 6, H - 40, -W), (-W + 6, H - 40, -W))
        quad(glass, (W - 6, 40, -W + 0.5), (-W + 6, 40, -W + 0.5), (-W + 6, H - 40, -W + 0.5), (W - 6, H - 40, -W + 0.5))
        xform(paint, k0, f)
        xform(glass, kg, f)
    for side in (1, 2, 3):
        wall(rot('y', side * 90))
    # the door: two leaves folded in a little, hinged on the left post
    for leaf, (ang, off) in enumerate(((-28, 0.0), (28, 0.0))):
        k0, kg = len(paint.V), len(glass.V)
        lw = W - 4
        boxq(paint, 0, 12, -2, lw, 22, 2, 1 / 64.0)
        boxq(paint, 0, H - 44, -2, lw, H - 36, 2, 1 / 64.0)
        boxq(paint, 0, 12, -2, 4, H - 36, 2, 1 / 64.0)
        boxq(paint, lw - 4, 12, -2, lw, H - 36, 2, 1 / 64.0)
        for r in range(1, 4):
            y = 22 + r * (H - 66) / 4
            boxq(paint, 0, y - 2, -2, lw, y + 2, 2, 1 / 64.0)
        quad(glass, (4, 22, 0), (lw - 4, 22, 0), (lw - 4, H - 44, 0), (4, H - 44, 0))
        quad(glass, (lw - 4, 22, 0.4), (4, 22, 0.4), (4, H - 44, 0.4), (lw - 4, H - 44, 0.4))
        if leaf == 0:
            tf = lambda p: rot('y', -35)((p[0] - W + 6, p[1], p[2] - W))
        else:
            tf = lambda p: rot('y', 35)((-(p[0]) + W - 6, p[1], p[2] - W + 0))
        xform(paint, k0, tf)
        xform(glass, kg, tf)
    # inside: the shelf, the empty mounting plate on the back wall, a cut cord, the roof light
    boxq(paint, -W + 6, 120, W - 30, W - 6, 126, W - 4, 1 / 64.0)
    quad(plate, (-22, 150, W - 4.5), (22, 150, W - 4.5), (22, 230, W - 4.5), (-22, 230, W - 4.5))
    k = len(plate.V)
    quad(plate, (22, 150, W - 4.5), (-22, 150, W - 4.5), (-22, 230, W - 4.5), (22, 230, W - 4.5))
    tube(dark, [(10, 160, W - 5), (12, 140, W - 8), (8, 125, W - 10)], lambda i: 0.9, 6)
    blob(lamp, (0, H - 34, 0), (14, 3, 14), rings=6, segs=12)
    return M


# ============================================================================ SCP-178: the glasses, an entity
def specs():
    c = noise_tex(256, (236, 234, 226), 5, 0.5, 178)
    d = ImageDraw.Draw(c)
    for _ in range(40):
        x, y = RND.randrange(256), RND.randrange(256)
        d.line([(x, y), (x + RND.randint(5, 30), y)], fill=(220, 214, 196), width=2)
    save(c, ITEMS, 's178_card.png')
    save(Image.new('RGB', (32, 32), (60, 120, 255)), ITEMS, 's178_blue.png')
    save(Image.new('RGB', (32, 32), (255, 50, 50)), ITEMS, 's178_red.png')
    M = Model()
    cb = M.surf('card', 's178_card.png', shine=0.1)
    bl = M.surf('blue', 's178_blue.png', fx=1, alpha=0.55)
    rd = M.surf('red', 's178_red.png', fx=1, alpha=0.55)
    t = 0.15
    # the front frame with two lens windows (x: -7.2..7.2, y: 0..4.2)
    for (x0, x1) in ((-7.2, -6.6), (-0.6, 0.6), (6.6, 7.2)):
        boxq(cb, x0, 0, -t, x1, 4.2, t, 0.1)
    boxq(cb, -7.2, 3.4, -t, 7.2, 4.2, t, 0.1)
    boxq(cb, -7.2, 0, -t, -0.6, 0.6, t, 0.1)
    boxq(cb, 0.6, 0, -t, 7.2, 0.6, t, 0.1)
    blob(cb, (0, 1.2, 0), (0.9, 0.9, t), e=0.6, rings=4, segs=8)                      # the bridge notch
    quad(bl, (-6.6, 0.6, 0), (-0.6, 0.6, 0), (-0.6, 3.4, 0), (-6.6, 3.4, 0))
    quad(bl, (-0.6, 0.6, 0.05), (-6.6, 0.6, 0.05), (-6.6, 3.4, 0.05), (-0.6, 3.4, 0.05))
    quad(rd, (0.6, 0.6, 0), (6.6, 0.6, 0), (6.6, 3.4, 0), (0.6, 3.4, 0))
    quad(rd, (6.6, 0.6, 0.05), (0.6, 0.6, 0.05), (0.6, 3.4, 0.05), (6.6, 3.4, 0.05))
    for e in (-1, 1):                                                                   # the temples, folded out
        boxq(cb, e * 7.2 - (0.3 if e > 0 else -0.0) - (0 if e > 0 else 0.3), 1.4, 0, e * 7.2 + (0.3 if e > 0 else 0), 3.0, 13.0, 0.1)
    return M


def entity():
    save(noise_tex(256, (60, 58, 66), 14, 1.2, 1781), PROPS, 's178e_skin.png')
    save(noise_tex(64, (200, 196, 186), 8, 0.6, 1782), PROPS, 's178e_claw.png')
    M = Model()
    sk = M.surf('skin', 's178e_skin.png', shine=0.2, alpha=0.85)
    cl = M.surf('claw', 's178e_claw.png', shine=0.6)
    # room units: about 420 tall (2.6 m), a hunched, gaunt figure
    for e in (-1, 1):
        tube(sk, [(e * 16, 0, 4), (e * 18, 90, -6), (e * 15, 180, 10), (e * 12, 230, 0)], lambda i: (9, 11, 13, 15)[i], 10)   # legs
        blob(sk, (e * 16, 4, -10), (8, 4, 18), rings=6, segs=10)                                              # feet
    blob(sk, (0, 290, 6), (30, 70, 20), rings=14, segs=18)                              # the torso, narrow and long
    blob(sk, (0, 236, 4), (22, 18, 16), rings=8, segs=12)                               # hips
    tube(sk, [(0, 352, 10), (0, 372, 4), (0, 384, -8)], lambda i: 6, 8)                 # the neck, craning forward
    blob(sk, (0, 392, -20), (13, 15, 17), rings=12, segs=16)                            # the small eyeless head
    for e in (-1, 1):                                                                   # long arms hanging forward
        path = [(e * 30, 340, 6), (e * 40, 290, -14), (e * 42, 220, -30), (e * 38, 160, -44)]
        tube(sk, path, lambda i: (7, 6, 5, 4.5)[i], 9)
        hand = path[-1]
        blob(sk, hand, (6, 8, 5), rings=6, segs=10)
        for k in (-1, 0, 1):                                                            # three long tapered claws
            tip = add(hand, (k * 4 + e * 2, -48 - 6 * abs(k), -10 + 3 * k))
            tube(cl, [add(hand, (k * 3, -4, 0)), add(hand, (k * 3.6, -26, -4)), tip], lambda i: (2.6, 1.6, 0.2)[i], 6)
    return M


# ============================================================================ SCP-198: the mug
def mug():
    im = Image.new('RGB', (512, 256), (246, 246, 242))
    d = ImageDraw.Draw(im)
    for x in range(0, 512, 64):
        d.rectangle([x + 20, 0, x + 40, 256], fill=(40, 80, 170))
    save(im.filter(ImageFilter.GaussianBlur(0.6)), ITEMS, 's198_mug.png')
    save(Image.new('RGB', (64, 64), (246, 246, 242)), ITEMS, 's198_white.png')
    save(noise_tex(64, (70, 44, 26), 8, 1.5, 198), ITEMS, 's198_coffee.png')
    M = Model()
    m = M.surf('mug', 's198_mug.png', shine=0.9)
    w = M.surf('white', 's198_white.png', shine=0.9)
    c = M.surf('coffee', 's198_coffee.png', shine=1.0)
    lathe(m, [(3.6, 0.3), (4.0, 0.6), (4.1, 4.0), (4.15, 8.6), (4.25, 9.4)], 36, lambda i: i / 4.0)        # outside
    lathe(w, [(0, 0), (3.2, 0), (3.6, 0.3)], 36, lambda i: i / 2.0)                                        # base
    k = len(w.V)
    lathe(w, [(3.75, 9.2), (3.75, 0.9), (0.0, 0.9)], 36, lambda i: i / 2.0)                                # inside
    for i in range(k, len(w.V)):                                                                           # face inwards
        v = w.V[i]
        w.V[i] = v[:3] + (-v[3], -v[4], -v[5]) + v[6:]
    w.T[len(w.T) - 36 * 4:] = [(a, cc, b) for (a, b, cc) in w.T[len(w.T) - 36 * 4:]]
    lathe(w, [(3.75, 9.2), (4.0, 9.55), (4.25, 9.4)], 36, lambda i: i / 2.0)                                # the rim
    lathe(c, [(0, 7.6), (3.74, 7.6)], 36, lambda i: i)                                                     # coffee
    tube(w, [(4.0, 7.6, 0), (6.6, 7.4, 0), (7.2, 4.8, 0), (6.2, 2.2, 0), (4.0, 2.0, 0)], lambda i: 0.65, 10)  # the handle
    return M


# ============================================================================ SCP-207: the bottle and the crate
def bottle():
    save(noise_tex(64, (40, 22, 14), 6, 1.0, 207), ITEMS, 's207_cola.png')
    lb = Image.new('RGB', (512, 128), (196, 24, 30))
    d = ImageDraw.Draw(lb)
    d.text((256, 50), 'COLA', font=F(64), fill=(255, 255, 255), anchor='mm')
    d.text((256, 104), 'SCP-207-B  -  DO NOT DRINK', font=F(22), fill=(255, 230, 230), anchor='mm')
    save(lb.transpose(Image.FLIP_TOP_BOTTOM), ITEMS, 's207_label.png')        # the lathe's v runs bottom-up
    save(noise_tex(64, (190, 30, 34), 10, 0.6, 2071), ITEMS, 's207_cap.png')
    save(noise_tex(64, (200, 220, 210), 4, 0.6, 2072), ITEMS, 's207_glass.png')
    M = Model()
    liq = M.surf('cola', 's207_cola.png', shine=0.6)
    lab = M.surf('label', 's207_label.png', shine=0.4)
    cap = M.surf('cap', 's207_cap.png', shine=0.7)
    gl = M.surf('glass', 's207_glass.png', shine=1.0, alpha=0.35, tint=(0.8, 1.0, 0.9))
    prof = [(0.0, 0.0), (2.9, 0.0), (3.1, 0.4), (3.2, 3.0), (2.8, 6.0), (3.15, 9.0), (3.2, 11.0), (2.6, 14.0),
            (1.5, 17.5), (1.2, 19.5), (1.35, 20.2)]
    lathe(gl, prof, 32, lambda i: i / 10.0)
    lathe(liq, [(0.0, 0.3), (2.85, 0.3), (2.95, 3.0), (2.55, 6.0), (2.9, 9.0), (2.9, 11.0), (2.3, 14.0), (0.0, 14.0)], 28, lambda i: i / 7.0)
    lathe(lab, [(3.24, 6.6), (3.24, 10.6)], 36, lambda i: i)
    lathe(cap, [(1.4, 19.8), (1.55, 20.0), (1.55, 21.0), (1.3, 21.3), (0.0, 21.3)], 18, lambda i: i / 4.0)
    return M


def crate():
    w = noise_tex(256, (150, 116, 72), 12, 0.8, 2073)
    d = ImageDraw.Draw(w)
    for y in range(0, 256, 64):
        d.line([(0, y), (256, y)], fill=(90, 66, 40), width=3)
    d.text((128, 160), 'SCP-207', font=F(36), fill=(60, 40, 20), anchor='mm')
    save(w, PROPS, 's207_wood.png')
    for f in ('s207_cola.png', 's207_cap.png', 's207_glass.png', 's207_label.png'):
        Image.open(os.path.join(ITEMS, f)).save(os.path.join(PROPS, f))
    M = Model()
    wd = M.surf('wood', 's207_wood.png', shine=0.1)
    boxq(wd, -100, 0, -70, 100, 8, 70, 1 / 120.0)
    for (x0, z0, x1, z1) in ((-100, -70, 100, -64), (-100, 64, 100, 70), (-100, -70, -94, 70), (94, -70, 100, 70)):
        boxq(wd, x0, 8, z0, x1, 40, z1, 1 / 120.0)
    for x in (-36, 33):
        boxq(wd, x, 8, -64, x + 3, 34, 64, 1 / 120.0)
    b = bottle()                                                                         # 24 slots, 23 bottles
    for name in ('cola', 'label', 'cap', 'glass'):
        s0 = b.S[name]
        s1 = M.surf(name, s0.tex, fx=s0.fx, shine=s0.shine, alpha=s0.alpha, tint=s0.tint)
        for i in range(6):
            for j in range(4):
                if (i, j) == (2, 1):
                    continue                                                             # -B is out for testing
                ox, oz = -84 + i * 33.6, -48 + j * 32
                base = len(s1.V)
                s1.V += [(v[0] * 2.3 + ox, v[1] * 2.3 + 8, v[2] * 2.3 + oz) + tuple(v[3:]) for v in s0.V]
                s1.T += [(a + base, bb + base, c + base) for (a, bb, c) in s0.T]
    return M


# ============================================================================ SCP-1079: the bonbons
def bonbons():
    im = Image.new('RGB', (512, 512), (255, 120, 190))
    d = ImageDraw.Draw(im)
    for k in range(0, 512, 40):
        d.ellipse([k % 300 + 20, (k * 7) % 480, k % 300 + 70, (k * 7) % 480 + 50], fill=(255, 200, 230))
    d.rectangle([0, 150, 512, 330], fill=(255, 245, 120))
    d.text((256, 190), "Dr. Wondertainment's", font=F(34), fill=(200, 30, 120), anchor='mm')
    d.text((256, 250), 'BUBBLEBATH', font=F(58), fill=(60, 120, 230), anchor='mm')
    d.text((256, 305), 'BONBONS!', font=F(58), fill=(60, 120, 230), anchor='mm')
    d.text((256, 400), 'Not suitable for children under 3 years', font=F(20, FR), fill=(80, 20, 60), anchor='mm')
    d.text((256, 430), 'Only one sweet is to be taken per sitting', font=F(20, FR), fill=(80, 20, 60), anchor='mm')
    save(im, ITEMS, 's1079_pack.png')
    save(noise_tex(64, (255, 150, 200), 12, 0.8, 1079), ITEMS, 's1079_sweet.png')
    M = Model()
    pk = M.surf('pack', 's1079_pack.png', shine=0.6)
    sw = M.surf('sweet', 's1079_sweet.png', shine=0.9)

    def pillow(i, j):                                                                    # a puffed packet
        u, v = i / 16.0, j / 32.0
        x = (u - 0.5) * 12
        y = (v - 0.0) * 16
        puff = math.sin(math.pi * u) * math.sin(math.pi * min(1, v * 1.15)) * 1.6
        return (x, y, -puff - 0.2)
    grid(pk, pillow, 16, 32, lambda i, j: (i / 16.0, 1 - j / 32.0))
    grid(pk, lambda i, j: (pillow(16 - i, j)[0], pillow(16 - i, j)[1], -pillow(16 - i, j)[2]), 16, 32,
         lambda i, j: ((16 - i) / 16.0, 1 - j / 32.0))
    for k in range(4):                                                                  # spilled sweets
        blob(sw, (-3.6 + k * 2.4, 15.2 + (k % 2) * 0.5, -1.4 - 0.3 * k), (1.0, 0.8, 1.0), rings=8, segs=12)
    return M


# ============================================================================ SCP-1650: the oil pot
def oilpot():
    cl = noise_tex(512, (168, 112, 74), 14, 1.0, 1650)
    d = ImageDraw.Draw(cl)
    for _ in range(300):
        x, y = RND.randrange(512), RND.randrange(512)
        d.line([(x, y), (x + RND.randint(-14, 14), y + RND.randint(-3, 3))], fill=(140, 92, 60), width=1)
    d.rectangle([0, 230, 512, 290], fill=(150, 100, 64))
    for x in range(10, 500, 26):                                            # a worn band of letters (illegible)
        h = RND.randint(16, 30)
        d.line([(x, 248), (x + 8, 248), (x + 8, 248 + h)], fill=(96, 60, 38), width=3)
    save(cl.filter(ImageFilter.GaussianBlur(0.6)), ITEMS, 's1650_clay.png')
    M = Model()
    c = M.surf('clay', 's1650_clay.png', shine=0.15)
    prof = [(0, 0), (3.6, 0), (4.4, 0.6), (6.2, 3.0), (6.8, 6.0), (6.4, 9.0), (4.6, 11.4), (2.6, 12.6), (2.4, 14.0),
            (3.0, 14.6), (2.7, 15.0), (2.2, 14.6), (2.0, 12.0)]
    lathe(c, prof, 40, lambda i: i / 12.0)
    tube(c, [(4.8, 11.0, 0), (8.4, 11.6, 0), (8.6, 7.4, 0), (6.4, 6.4, 0)], lambda i: 0.8, 10)        # the handle
    tube(c, [(-5.6, 8.8, 0), (-8.6, 10.4, 0), (-10.2, 11.0, 0)], lambda i: (1.6, 1.2, 0.9)[i], 12)    # the spout
    return M


if __name__ == '__main__':
    out = {}
    for name, fn, folder in (('scp467', booth, PROPS), ('scp178e', entity, PROPS), ('scp178', specs, ITEMS),
                             ('scp198', mug, ITEMS), ('scp207', bottle, ITEMS), ('scp207crate', crate, PROPS),
                             ('scp1079', bonbons, ITEMS), ('scp1650', oilpot, ITEMS)):
        m = fn()
        m.write(os.path.join(folder, name + '.b3d'))
        out[name] = (m, folder)
        print('%-12s %6d triangles' % (name, m.tris()))
    views = {'scp467': ((260, 260, -380), (0, 170, 0)), 'scp178e': ((300, 300, -560), (0, 220, 0)),
             'scp178': ((-6, 10, -16), (0, 2, 4)), 'scp198': ((10, 14, -16), (0, 5, 0)),
             'scp207': ((10, 16, -20), (0, 10, 0)), 'scp207crate': ((160, 200, -260), (0, 30, 0)),
             'scp1079': ((10, 14, -22), (0, 9, 0)), 'scp1650': ((16, 16, -24), (0, 7, 0))}
    tiles = []
    for name, (m, folder) in out.items():
        eye, look = views[name]
        tiles.append(render(m, folder, eye, look, size=(400, 400), fov=45, bg=(30, 30, 34)))
    sheet = Image.new('RGB', (1600, 800))
    for i, t in enumerate(tiles):
        sheet.paste(t, ((i % 4) * 400, (i // 4) * 400))
    sheet.save(os.path.join(PREV, 'hd31_models.png'))
    for name in ('scp178', 'scp198', 'scp207', 'scp1079', 'scp1650'):
        m, folder = out[name]
        eye, look = views[name]
        render(m, folder, eye, look, size=(256, 256), fov=45, bg=(0, 0, 0)).resize((64, 64), Image.LANCZOS).save(
            os.path.join(ITEMS, 'INV%s.png' % name))
    print('previews and icons written')
