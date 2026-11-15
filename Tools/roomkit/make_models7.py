"""Models for the ninth batch (GFX\\npcs, room units, front = +z, origin on the floor unless noted):
   scp457.b3d     the burning man: a human shape built out of tongues of flame (drawn additive, fullbright)
   scp0161.b3d    D-016-1: what SCP-016 made of a man in a flooding room (origin at its middle, it swims along +z)
   scp152.b3d     the book, lying open at its last page (origin under the middle of the spine)
   scp280.b3d     the black figure: no legs, arms held out, very long fingers
   scp280e.b3d    its two white eyes (hung on the body, shown only when it retreats)
   python make_models7.py view   also writes out\\models7.png"""
import math
import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from b3dkit import Mesh, write_b3d
from make_models5 import tones, band, ellipsoid, tail
from make_models4 import sphere
from make_assets5 import ft, noise

NPCDIR = r"I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9\GFX\npcs"


# ---------------------------------------------------------------------------------- textures
def flame_tex():
    """v = 0 (tips): dark red, v = 1 (the core): yellow-white; streaked along u"""
    W, H = 256, 256
    t = np.linspace(0, 1, H)[:, None]
    stops = [(0.0, (40, 4, 0)), (0.35, (200, 50, 6)), (0.65, (255, 140, 20)), (0.88, (255, 220, 90)), (1.0, (255, 250, 220))]
    a = np.zeros((H, W, 3))
    for c in range(3):
        a[..., c] = np.interp(t, [s[0] for s in stops], [s[1][c] for s in stops])
    streak = noise(H, W, 4570, 3, 1.2)
    streak = np.repeat(streak[:1, :], H, axis=0) * 0.5 + streak * 0.5
    a *= (0.55 + 0.75 * streak)[..., None]
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8)).save(os.path.join(NPCDIR, 'indev_flame.png'))


def book_tex():
    """left half: a vellum page of close black script; right half: old leather"""
    W, H = 256, 128
    im = Image.new('RGB', (W, H), (0, 0, 0))
    a = np.asarray(im).astype(float)
    n = noise(H, W, 1521, 6, 2.0)
    a[:, :128] = np.array([224, 212, 180.0]) * (0.88 + 0.2 * n[:, :128, None])
    a[:, 128:] = np.array([84, 52, 34.0]) * (0.7 + 0.6 * n[:, 128:, None])
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    rng = np.random.default_rng(1522)
    for row in range(15):
        y = 10 + row * 7.4
        x = 10
        while x < 116:
            w = int(rng.integers(4, 13))
            if row == 14 and x > 70:
                break
            d.line([(x, y), (min(116, x + w), y)], fill=(26, 22, 18), width=2)
            x += w + 3
    d.rectangle([134, 6, 250, 122], outline=(150, 110, 60), width=2)
    im.save(os.path.join(NPCDIR, 'indev_book152.png'))


# ---------------------------------------------------------------------------------- models
def flame_man():
    m = Mesh()
    U = [(k / 8.0 + 0.01, 0.02, (k + 1) / 8.0 - 0.01, 0.98) for k in range(8)]

    def tongue(base, tip, r, k, sides=7):
        m.cyl(base, tip, r, r * 0.08, sides=sides, uvrect=U[k % 8], caps=False)

    # a skirt of flames at the floor, the two legs rising out of it
    for i in range(10):
        a = 2 * math.pi * i / 10
        bx, bz = 30 * math.cos(a), 26 * math.sin(a)
        tongue((bx, 0, bz), (bx * 1.5, 46 + 22 * (i % 3), bz * 1.5), 15, i)
    for s in (-1, 1):
        m.cyl((s * 15, 0, 0), (s * 13, 112, 0), 16, 12, sides=8, uvrect=U[1 + (s > 0)], caps=False)
        tongue((s * 20, 50, -6), (s * 34, 120, -22), 10, 3 + (s > 0))
    # torso: the brightest part, two overlapping bodies of flame
    U_core = (0.02, 0.84, 0.98, 0.99)
    ellipsoid(m, (0, 150, 0), 30, 48, 20, U_core, seg=10, rings=6)
    ellipsoid(m, (0, 176, 0), 34, 30, 22, U_core, seg=10, rings=6)
    # arms hanging a little out from the body, ending in ragged fingers of flame
    for s in (-1, 1):
        sh = (s * 34, 190, 0)
        el = (s * 50, 146, 8)
        ha = (s * 54, 106, 18)
        m.cyl(sh, el, 11, 9, sides=7, uvrect=U[5], caps=False)
        m.cyl(el, ha, 9, 7, sides=7, uvrect=U[6], caps=False)
        for k, (dx, dz) in enumerate(((0, 10), (6, 2), (-6, 4))):
            tongue(ha, (ha[0] + s * dx, 76 - 4 * k, ha[2] + dz), 5, k + 2, sides=5)
        tongue((s * 36, 196, -4), (s * 54, 236, -16), 9, 7)            # flames streaming off the shoulders
    # the head and its crest
    ellipsoid(m, (0, 222, 2), 17, 21, 18, U_core, seg=10, rings=6)
    for k, (dx, dz, h, r) in enumerate(((0, -4, 60, 12), (-10, 0, 42, 9), (10, 2, 46, 9), (0, 8, 34, 8), (-5, -10, 50, 8), (6, -8, 38, 7))):
        tongue((dx, 232, dz), (dx * 1.6, 232 + h, dz * 2.2 - 8), r, k)
    # the eyes: two darker hollows are not possible in additive light, so two hotter points instead
    for s in (-1, 1):
        sphere(m, (s * 7, 226, 17), 3.5, seg=6, rings=4, uv=(0.4, 0.97, 0.6, 0.99))
    return m


def swimmer():
    """D-016-1, horizontal: head at +z"""
    m = Mesh()
    Sk, Gi, Fn, Dk = band(0, 4), band(1, 4), band(2, 4), band(3, 4)
    ellipsoid(m, (0, 0, 0), 26, 22, 70, Sk, seg=12, rings=8)                    # the trunk
    ellipsoid(m, (0, 4, 78), 17, 17, 22, Sk, seg=10, rings=6)                   # the head: no eyes
    m.cyl((0, 0, 92), (0, -3, 104), 9, 5, sides=8, uvrect=Dk)                   # the jaw
    for s in (-1, 1):
        for k in range(4):                                                      # gill slits down the neck
            m.box((s * 16.5, 6 - k * 5, 56 - k * 2), 1.2, 1.4, 7, uvrect=Gi)
        # the arms: flattened into fins
        tail(m, [(s * 24, -4, 34), (s * 52, -10, 20), (s * 78, -14, -6)], 7, 2, Sk, sides=6)
        for (a, b, c) in (((s * 30, -5, 30), (s * 76, -14, -6), (s * 44, -12, -30)), ((s * 44, -12, -30), (s * 76, -14, -6), (s * 60, -14, -34))):
            for flip in (False, True):
                pts = [a, b, c][::-1] if flip else [a, b, c]
                m.poly(pts, [(Fn[0], Fn[3]), (Fn[2], Fn[3]), (Fn[2], Fn[1])])
        m.cyl((s * 9, 6, 90), (s * 9, 7, 93), 3.2, sides=6, uvrect=Sk)           # skin grown over the sockets
    # the legs, fused into a fluke
    tail(m, [(0, 0, -60), (0, -2, -100), (0, -2, -128)], 18, 7, Sk, sides=8)
    for s in (-1, 1):
        a, b, c, d = (0, -2, -120), (s * 46, -2, -150), (s * 40, -2, -168), (0, -2, -140)
        for flip in (False, True):
            pts = [a, b, c, d][::-1] if flip else [a, b, c, d]
            m.poly(pts, [(Fn[0], Fn[3]), (Fn[2], Fn[3]), (Fn[2], Fn[1]), (Fn[0], Fn[1])])
    # a low ridge down the back
    for flip in (False, True):
        pts = [(0, 20, 40), (0, 36, 0), (0, 20, -50)]
        m.poly(pts[::-1] if flip else pts, [(Fn[0], Fn[3]), (Fn[2], Fn[1]), (Fn[2], Fn[3])])
    return m


def book():
    """open at the last page: nearly every leaf lies on the left"""
    m = Mesh()
    PG, LE = (0.02, 0.04, 0.48, 0.96), (0.54, 0.06, 0.96, 0.94)
    EDGE = (0.03, 0.9, 0.2, 0.96)
    m.box((0, 1.5, 0), 62, 1.5, 40, uvrect=LE)                                   # the boards and spine
    # left block: the whole book
    x0, x1, y0, y1 = -58.0, -1.0, 3.0, 21.0
    m.quad((x0, y1, -37), (x1, y1 - 3, -37), (x1, y1 - 3, 37), (x0, y1, 37), uvrect=PG)          # the open page
    m.quad((x0, y0, -37), (x1, y0, -37), (x1, y1 - 3, -37), (x0, y1, -37), uvrect=EDGE)          # fore edges
    m.quad((x1, y0, 37), (x0, y0, 37), (x0, y1, 37), (x1, y1 - 3, 37), uvrect=EDGE)
    m.quad((x0, y0, 37), (x0, y0, -37), (x0, y1, -37), (x0, y1, 37), uvrect=EDGE)
    # right: only the last leaf and the back board
    m.quad((1.0, 3.6, -37), (58, 3.2, -37), (58, 3.2, 37), (1.0, 3.6, 37), uvrect=(0.06, 0.5, 0.44, 0.96))
    return m


def figure280():
    m = Mesh()
    B = band(0, 2)
    # no legs: the body thins out above the floor into a ragged hem
    prof = [(18, 3), (40, 12), (80, 20), (130, 25), (170, 27), (196, 24)]
    for (ya, ra), (yb, rb) in zip(prof[:-1], prof[1:]):
        m.cyl((0, ya, 0), (0, yb, 0), ra, rb, sides=10, uvrect=B, caps=False)
    for i in range(7):
        a = 2 * math.pi * i / 7
        m.cyl((10 * math.cos(a), 46, 10 * math.sin(a)), (16 * math.cos(a), 12 + (i % 3) * 5, 16 * math.sin(a)), 5, 0.5, sides=5, uvrect=B, caps=False)
    ellipsoid(m, (0, 198, 0), 30, 14, 18, B, seg=10, rings=4)                    # shoulders
    m.cyl((0, 204, 0), (0, 218, 2), 8, 7, sides=8, uvrect=B, caps=False)
    ellipsoid(m, (0, 234, 4), 15, 19, 16, B, seg=10, rings=6)                    # the head
    # the sleepwalker's arms, and fingers twice as long as they should be
    for s in (-1, 1):
        sh, el, wr = (s * 28, 198, 4), (s * 30, 186, 52), (s * 26, 184, 98)
        m.cyl(sh, el, 7, 5.5, sides=7, uvrect=B, caps=False)
        m.cyl(el, wr, 5.5, 4, sides=7, uvrect=B, caps=False)
        for k in range(5):
            spread = (k - 2) * 5
            kn = (wr[0] + s * 1 + spread, wr[1] - 3 - abs(k - 2), wr[2] + 20)
            tp = (wr[0] + spread * 1.9, wr[1] - 16 - abs(k - 2) * 3, wr[2] + 44)
            m.cyl(wr, kn, 1.5, 1.2, sides=4, uvrect=B, caps=False)
            m.cyl(kn, tp, 1.2, 0.3, sides=4, uvrect=B, caps=False)
    return m


def eyes280():
    m = Mesh()
    Wt = band(1, 2)
    for s in (-1, 1):
        sphere(m, (s * 6.5, 238, 18.5), 5.0, seg=8, rings=6, uv=Wt)
    return m


def write_all():
    flame_tex()
    book_tex()
    tones('indev_d0161.png', [(196, 176, 168), (120, 40, 44), (150, 150, 160), (60, 50, 56)], 161, fur=0.25)
    tones('indev_280.png', [(4, 4, 5), (250, 250, 246)], 280, size=(64, 64))
    out = [('scp457.b3d', 'indev_flame.png', flame_man()), ('scp0161.b3d', 'indev_d0161.png', swimmer()),
           ('scp152.b3d', 'indev_book152.png', book()), ('scp280.b3d', 'indev_280.png', figure280()),
           ('scp280e.b3d', 'indev_280.png', eyes280())]
    for fn, tex, mesh in out:
        nv, nt = write_b3d(os.path.join(NPCDIR, fn), tex, mesh, name=fn.split('.')[0])
        print('%-14s %5d verts %5d tris' % (fn, nv, nt))
    return out


if __name__ == '__main__':
    out = write_all()
    if 'view' in sys.argv:
        from view_models import render
        M = {fn: (tex, mesh) for fn, tex, mesh in out}
        both = Mesh()
        b, e = M['scp280.b3d'][1], M['scp280e.b3d'][1]
        both.v = list(b.v) + list(e.v)
        both.t = list(b.t) + [(i + len(b.v), j + len(b.v), k + len(b.v)) for (i, j, k) in e.t]
        views = [('scp457.b3d', M['scp457.b3d'][1], (150, 190, 330), (0, 140, 0), True, (10, 8, 8)),
                 ('scp457.b3d (side)', M['scp457.b3d'][1], (330, 170, 60), (0, 140, 0), True, (10, 8, 8)),
                 ('scp0161.b3d', M['scp0161.b3d'][1], (190, 110, 150), (0, 0, 0), False, (30, 50, 60)),
                 ('scp152.b3d', M['scp152.b3d'][1], (20, 110, -120), (0, 6, 0), False, (60, 50, 44)),
                 ('scp280.b3d + eyes', both, (150, 200, 330), (0, 140, 30), True, (70, 70, 74)),
                 ('scp280.b3d (side)', both, (340, 190, 60), (0, 150, 30), True, (70, 70, 74))]
        tiles = []
        for name, mesh, eye, look, fb, bg in views:
            key = name.split(' ')[0]
            im = render(mesh, M[key][0], eye, look, fullbright=fb, bg=bg)
            ImageDraw.Draw(im).text((6, 4), name, fill=(240, 220, 120))
            tiles.append(im)
        sheet = Image.new('RGB', (420 * 3, 320 * 2))
        for i, t in enumerate(tiles):
            sheet.paste(t, ((i % 3) * 420, (i // 3) * 320))
        os.makedirs('out', exist_ok=True)
        sheet.save('out/models7.png')
        print('out/models7.png')
