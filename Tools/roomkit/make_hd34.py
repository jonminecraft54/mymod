r"""High-detail models for batch 34 (original work after the scp-wiki.wikidot.com articles, CC BY-SA 3.0).
Props (GFX\map\props, room units): Mr. Brass (629), a Troupe mannequin (5147), the Chore Buddy (1508), the calcified
infant in its cradle (5199), the cold rabbit doll (2792), the red fridge (1731), the Zenith set (1970), the rosewood
chair (1445), the disco ball (1969), the top (3016), the -2 kg weight (2597), the nine-faced trapezohedron (2414),
the bowl and spoon (1404), the LaserJet (1473), the photocopier (4566), the octopus (5582), a dodo (711-FR), the
shrub (324), the okapi (1807), a brass ovoid (1564), the Venus fountain (1575), the grey sphere (3085).
Items (GFX\items, cm): dice1974, pills3866, stapler3709, cards3803, book1841, grapes1255, caps4193, tabs5604,
cereal2983, camera5701.
   python make_hd34.py"""
import math
import os
import random
from PIL import Image, ImageDraw, ImageFilter
from make_hd29 import Model, tube, lathe, add, sub, render, ITEMS, PROPS, PREV
from make_hd30 import blob, quad, xform, rot, noise_tex, F, FR
from make_hd31 import boxq
from make_hd33 import ring, tex, solid_tex

RND = random.Random(34)


def T(folder, name, rgb, amp=8, seed=0, blur=0.8, size=128):
    return tex(noise_tex(size, rgb, amp, blur, seed), folder, name)


def biped(s, h=176.0, girth=1.0, head=True):
    """a human figure of blobs and tubes standing on y=0, facing -z (the mannequins, Mr. Brass)"""
    k = h / 176.0
    for e in (-1, 1):
        tube(s, [(e * 9 * k, 8 * k, 0), (e * 10 * k, 48 * k, -1), (e * 10 * k, 90 * k, 0)], lambda i: (5.5, 6.5, 8)[i] * k * girth, 12)
        blob(s, (e * 9 * k, 4 * k, -5 * k), (5 * k, 4 * k, 12 * k), rings=6, segs=10)
        tube(s, [(e * 19 * k, 142 * k, 0), (e * 23 * k, 116 * k, -2), (e * 22 * k, 90 * k, -6)], lambda i: (5, 4.4, 3.8)[i] * k * girth, 10)
        blob(s, (e * 22 * k, 84 * k, -7 * k), (3.5 * k, 6 * k, 4 * k), rings=6, segs=8)
    blob(s, (0, 98 * k, 0), (17 * k * girth, 14 * k, 11 * k * girth), rings=10, segs=16)
    blob(s, (0, 124 * k, 0), (19 * k * girth, 24 * k, 12 * k * girth), e=0.85, rings=12, segs=16)
    tube(s, [(0, 146 * k, 0), (0, 154 * k, 0)], lambda i: 5 * k, 10)
    if head:
        blob(s, (0, 165 * k, -1 * k), (9 * k, 11.5 * k, 10.5 * k), rings=12, segs=16)


# ============================================================================ A
def misterbrass():
    T(PROPS, 's629_bronze.png', (150, 106, 54), 14, 1, 1.2)
    M = Model()
    b = M.surf('bronze', 's629_bronze.png', shine=0.9)
    biped(b, 176, 1.05)
    blob(b, (0, 172, -1), (10, 6, 11), e=0.8, rings=6, segs=14)                 # the beanie
    tube(b, [(0, 150, -12), (0, 112, -13)], lambda i: (2.2, 1.0)[i], 6)         # the tie
    tube(b, [(-6, 152, -12), (6, 152, -12)], lambda i: 1.4, 6)                  # collar
    blob(b, (0, 158, -9), (7, 5, 3), rings=6, segs=10)                          # the beard
    for e in (-1, 1):
        tube(b, [(e * 18, 142, -4), (e * 18, 100, -6)], lambda i: 0.9, 6)       # jacket edges
    boxq(b, -30, 0, -24, 30, 4, 24, 0.02)
    return M


def mannequin():
    T(PROPS, 's5147_skin.png', (228, 222, 210), 4, 2, 1.4)
    M = Model()
    s = M.surf('skin', 's5147_skin.png', shine=0.7)
    biped(s, 180, 0.9)
    tube(s, [(0, 0, 0), (0, 70, 0)], lambda i: 1.4, 8)
    lathe(s, [(0, 0), (16, 0), (16, 2), (0, 2)], 16, lambda i: i / 3.0)
    return M


def chorebuddy():
    T(PROPS, 's1508_body.png', (150, 60, 190), 6, 3)
    sc = Image.new('RGB', (128, 128), (20, 30, 40))
    d = ImageDraw.Draw(sc)
    d.ellipse([28, 40, 50, 62], fill=(120, 255, 200)); d.ellipse([78, 40, 100, 62], fill=(120, 255, 200))
    d.arc([36, 60, 92, 100], 20, 160, fill=(120, 255, 200), width=5)
    tex(sc, PROPS, 's1508_face.png')
    T(PROPS, 's1508_metal.png', (190, 194, 200), 8, 4)
    M = Model()
    b = M.surf('body', 's1508_body.png', shine=0.8)
    f = M.surf('face', 's1508_face.png', fx=1)
    m = M.surf('metal', 's1508_metal.png', shine=1.0)
    lathe(b, [(0, 10), (34, 10), (38, 30), (36, 80), (30, 100), (0, 100)], 24, lambda i: i / 5.0)    # the body
    for a in range(3):
        x, z = math.cos(a * 2.09) * 24, math.sin(a * 2.09) * 24
        blob(m, (x, 6, z), (7, 7, 7), rings=6, segs=10)                          # castors
    blob(b, (0, 126, 0), (26, 22, 24), e=0.6, rings=10, segs=16)                # head
    quad(f, (-18, 112, -24.5), (18, 112, -24.5), (18, 140, -24.5), (-18, 140, -24.5))
    for e in (-1, 1):
        tube(m, [(e * 36, 84, 0), (e * 50, 70, -10), (e * 52, 50, -24)], lambda i: 3, 8)
        blob(m, (e * 52, 46, -26), (5, 5, 5), rings=6, segs=8)
    tube(m, [(52, 46, -26), (54, 10, -40)], lambda i: 1.2, 6)                    # a mop handle
    blob(M.surf('mop', 's5147_skin.png'), (54, 6, -42), (10, 6, 10), rings=6, segs=10)
    tube(m, [(0, 148, 0), (0, 166, 0)], lambda i: 1.2, 6)
    blob(M.surf('bulb', 's1508_face.png', fx=1), (0, 168, 0), (4, 4, 4), rings=6, segs=8)
    return M


def cradle():
    T(PROPS, 's5199_wood.png', (130, 90, 56), 12, 5)
    T(PROPS, 's5199_stone.png', (214, 208, 196), 10, 6, 1.4)
    T(PROPS, 's5199_cloth.png', (220, 220, 236), 5, 7)
    M = Model()
    w = M.surf('wood', 's5199_wood.png', shine=0.4)
    s = M.surf('stone', 's5199_stone.png', shine=0.2)
    c = M.surf('cloth', 's5199_cloth.png', shine=0.1)
    boxq(w, -30, 6, -18, 30, 9, 18, 0.05)
    for (x0, z0, x1, z1) in ((-30, -18, 30, -16), (-30, 16, 30, 18), (-30, -18, -28, 18), (28, -18, 30, 18)):
        boxq(w, x0, 9, z0, x1, 30, z1, 0.05)
    for e in (-1, 1):                                                           # rockers
        tube(w, [(e * 28, 2, -22), (e * 28, 0, 0), (e * 28, 2, 22)], lambda i: 1.4, 6)
    blob(c, (0, 11, 0), (26, 3, 14), e=0.5, rings=6, segs=12)
    blob(s, (-12, 18, 0), (6, 6, 6), rings=8, segs=12)                          # the stone infant
    blob(s, (2, 16, 0), (10, 6, 7), rings=8, segs=12)
    for e in (-1, 1):
        tube(s, [(10, 15, e * 4), (20, 14, e * 5)], lambda i: 2.4, 8)
        tube(s, [(-4, 17, e * 7), (-8, 20, e * 10)], lambda i: 2.0, 8)
    return M


def rabbitdoll():
    T(PROPS, 's2792_fur.png', (240, 240, 240), 6, 8, 1.2)
    solid_tex(PROPS, 's2792_red.png', (200, 30, 30), 6, 9)
    solid_tex(PROPS, 's2792_gauze.png', (220, 214, 196), 8, 10)
    solid_tex(PROPS, 's2792_frost.png', (210, 235, 255), 10, 11)
    M = Model()
    f = M.surf('fur', 's2792_fur.png', shine=0.1)
    r = M.surf('red', 's2792_red.png', shine=0.2)
    g = M.surf('gauze', 's2792_gauze.png', shine=0.1)
    ic = M.surf('frost', 's2792_frost.png', shine=1.0, alpha=0.6)
    blob(f, (0, 9, 0), (7, 9, 6), rings=10, segs=14)
    blob(f, (0, 22, 0), (6.5, 6, 6), rings=10, segs=14)
    for e in (-1, 1):
        tube(f, [(e * 2.5, 27, 0), (e * 3.5, 36, 1), (e * 4, 42, 2)], lambda i: (2, 1.8, 1.0)[i], 8)
        tube(r, [(e * 6, 13, -2), (e * 9, 8, -5)], lambda i: 2.0, 8)
        tube(r, [(e * 4, 2, -2), (e * 5, 0, -8)], lambda i: 2.4, 8)
        blob(M.surf('eye', 's3938_tyre.png', shine=1.0), (e * 2.4, 23, -5.6), (1, 1, 0.6), rings=4, segs=6)
    ring(g, (0, 22, 0), 6.6, 1.2, 'y', 16, 6)
    ring(g, (0, 18, 0), 4.5, 1.0, 'y', 16, 6)
    blob(ic, (0, 0, 0), (16, 1, 14), rings=4, segs=12)
    return M


# ============================================================================ B
def fridge():
    T(PROPS, 's1731_red.png', (190, 30, 30), 10, 12)
    solid_tex(PROPS, 's1731_phone.png', (40, 40, 44), 6, 13)
    T(PROPS, 's1731_bone.png', (222, 214, 190), 8, 14)
    M = Model()
    r = M.surf('red', 's1731_red.png', shine=0.6)
    p = M.surf('phone', 's1731_phone.png', shine=0.8)
    b = M.surf('bone', 's1731_bone.png', shine=0.2)
    boxq(r, -40, 0, -34, 40, 180, 34, 1 / 60.0)
    boxq(r, -40, 118, -36, 40, 120, -34, 0.05)
    tube(M.surf('handle', 's3938_chrome.png', shine=1.0), [(30, 130, -38), (30, 170, -38)], lambda i: 1.4, 6)
    for k in range(17):                                                         # the seventeen phones
        x, y = -32 + (k % 4) * 17 + RND.uniform(-3, 3), 20 + (k // 4) * 36 + RND.uniform(-4, 4)
        boxq(p, x, y, -37, x + 9, y + 16, -35, 0.1)
    for k in range(5):                                                          # bones
        y = 30 + k * 30
        tube(b, [(40.5, y, -20), (41, y + 8, 0), (40.5, y + 2, 20)], lambda i: 1.6, 6)
        blob(b, (41, y, -20), (2.5, 2.5, 2.5), rings=4, segs=6)
    blob(b, (-41, 140, 0), (3, 6, 12), rings=6, segs=10)                        # the foot
    return M


def tvset():
    T(PROPS, 's1970_wood.png', (110, 72, 40), 10, 15)
    st = Image.new('RGB', (128, 96), (0, 0, 0))
    d = ImageDraw.Draw(st)
    for _ in range(3000):
        x, y = RND.randrange(128), RND.randrange(96)
        g = RND.randint(40, 220)
        d.point((x, y), fill=(g, g, g))
    tex(st, PROPS, 's1970_screen.png')
    M = Model()
    w = M.surf('wood', 's1970_wood.png', shine=0.5)
    s = M.surf('screen', 's1970_screen.png', fx=1, shine=1.0)
    boxq(w, -42, 20, -30, 42, 80, 30, 1 / 60.0)
    quad(s, (-34, 28, -30.5), (16, 28, -30.5), (16, 74, -30.5), (-34, 74, -30.5))
    for y in (40, 56):
        lathe(M.surf('knob', 's3938_chrome.png', shine=1.0), [(0, 0), (3, 0), (3, 2), (0, 2)], 10, lambda i: i, cx=0)
        k = len(M.S['knob'].V) - 33
    for (x, z) in ((-36, -24), (36, -24), (-36, 24), (36, 24)):
        tube(w, [(x, 0, z), (x, 20, z)], lambda i: 2.2, 6)
    tube(M.S['knob'], [(28, 48, -31), (28, 48, -34)], lambda i: 3, 10)
    tube(M.S['knob'], [(28, 62, -31), (28, 62, -34)], lambda i: 3, 10)
    tube(M.S['knob'], [(-10, 80, 0), (-30, 110, 10)], lambda i: 0.6, 4)         # rabbit ears
    tube(M.S['knob'], [(10, 80, 0), (30, 110, 10)], lambda i: 0.6, 4)
    return M


def chair():
    T(PROPS, 's1445_wood.png', (110, 50, 30), 12, 16)
    T(PROPS, 's1445_base.png', (60, 40, 30), 14, 17)
    M = Model()
    w = M.surf('wood', 's1445_wood.png', shine=0.6)
    b = M.surf('base', 's1445_base.png', shine=0.1)
    boxq(b, -75, 0, -75, 75, 3, 75, 1 / 60.0)
    for (x, z) in ((-22, -20), (22, -20), (-22, 20), (22, 20)):
        tube(w, [(x, 3, z), (x, 48, z)], lambda i: 2.4, 8)
    boxq(w, -25, 46, -23, 25, 50, 23, 0.05)
    for x in (-22, 22):
        tube(w, [(x, 50, 20), (x * 1.05, 100, 22), (x * 0.9, 106, 20)], lambda i: 2.0, 8)
    tube(w, [(-26, 104, 21), (0, 108, 22), (26, 104, 21)], lambda i: 2.4, 8)    # the yoke rail
    boxq(w, -8, 50, 19, 8, 102, 22, 0.05)                                       # the splat
    for x in (-24, 24):                                                         # arms
        tube(w, [(x, 50, -18), (x, 70, -16), (x, 72, 18)], lambda i: 1.8, 8)
    return M


def discoball():
    mir = Image.new('RGB', (256, 256))
    d = ImageDraw.Draw(mir)
    for i in range(0, 256, 8):
        for j in range(0, 256, 8):
            g = RND.randint(120, 255)
            d.rectangle([i, j, i + 6, j + 6], fill=(g, g, min(255, g + 10)))
    tex(mir, PROPS, 's1969_mirror.png')
    M = Model()
    m = M.surf('mirror', 's1969_mirror.png', shine=1.0)
    blob(m, (0, 0, 0), (25, 25, 25), rings=20, segs=28, uv=(0, 0, 6, 3))
    tube(M.surf('chain', 's3938_chrome.png', shine=1.0), [(0, 25, 0), (0, 120, 0)], lambda i: 0.8, 6)
    return M


def top():
    M = Model()
    s = M.surf('steel', 's3938_chrome.png', shine=1.0)
    lathe(s, [(0, 0), (2, 1), (10, 7), (12, 10), (10, 12), (3, 13), (2.4, 20), (0, 20)], 32, lambda i: i / 7.0)
    return M


def weight():
    T(PROPS, 's2597_metal.png', (130, 130, 136), 10, 18)
    M = Model()
    s = M.surf('m', 's2597_metal.png', shine=0.9)
    lathe(s, [(0, 0), (6, 0), (6, 1), (5.4, 2), (5.4, 9), (3, 11), (2, 13), (3.2, 15), (0, 15.5)], 28, lambda i: i / 8.0)
    ring(s, (0, 17.5, 0), 2.2, 0.7, 'z', 16, 6)
    return M


def trapezohedron():
    T(PROPS, 's2414_metal.png', (120, 122, 126), 8, 19)
    M = Model()
    s = M.surf('m', 's2414_metal.png', shine=0.8, fx=16)
    n, r, h, tw = 4, 7.0, 7.0, 45
    top, bot = (0, h, 0), (0, -h, 0)
    up = [(r * math.cos(math.radians(k * 90)), 1.6, r * math.sin(math.radians(k * 90))) for k in range(4)]
    dn = [(r * math.cos(math.radians(k * 90 + tw)), -1.6, r * math.sin(math.radians(k * 90 + tw))) for k in range(4)]
    for k in range(4):                                                          # eight kite faces (as seen)
        a, b2, c = up[k], dn[k], up[(k + 1) % 4]
        quad(s, b2, c, top, a)
        a2, b3, c2 = dn[k], up[(k + 1) % 4], dn[(k + 1) % 4]
        quad(s, b3, a2, bot, c2)
    xform(s, 0, lambda p: (p[0], p[1] + 8, p[2]))
    return M


def bowl():
    T(PROPS, 's1404_black.png', (24, 24, 26), 4, 20)
    M = Model()
    b = M.surf('bowl', 's1404_black.png', shine=0.9)
    lathe(b, [(0, 0), (4, 0), (6.5, 2), (7.5, 7), (7, 7.2), (6, 2.4), (0, 1)], 28, lambda i: i / 6.0)
    sp = M.surf('spoon', 's3938_chrome.png', shine=1.0)
    tube(sp, [(10, 0.4, -6), (10, 0.6, 6)], lambda i: 0.5, 6)
    blob(sp, (10, 0.6, -8), (2.2, 0.6, 3), rings=6, segs=10)
    return M


def printer():
    T(PROPS, 's1473_plastic.png', (210, 204, 190), 5, 21)
    M = Model()
    p = M.surf('plastic', 's1473_plastic.png', shine=0.4)
    d = M.surf('dark', 's3938_tyre.png', shine=0.3)
    boxq(p, -28, 0, -24, 28, 30, 24, 1 / 40.0)
    boxq(p, -24, 30, -6, 24, 38, 24, 1 / 40.0)
    boxq(d, -20, 30, -20, 20, 31, -8, 0.1)
    boxq(M.surf('paper', 's4890_pages.png'), -16, 31, -20, 16, 31.5, -6, 0.1)
    boxq(d, 14, 34, -2, 26, 38.5, 10, 0.1)
    return M


def copier():
    T(PROPS, 's4566_body.png', (180, 178, 170), 6, 22)
    solid_tex(PROPS, 's4566_obsidian.png', (14, 10, 20), 6, 23)
    sg = noise_tex(128, (40, 30, 26), 10, 0.8, 24)
    d = ImageDraw.Draw(sg)
    for k in range(6):
        a = k * 1.05
        d.line([(64 + 40 * math.cos(a), 64 + 40 * math.sin(a)), (64 + 40 * math.cos(a + 2.1), 64 + 40 * math.sin(a + 2.1))], fill=(200, 190, 170), width=3)
    tex(sg, PROPS, 's4566_sigil.png')
    M = Model()
    b = M.surf('body', 's4566_body.png', shine=0.4)
    o = M.surf('obs', 's4566_obsidian.png', shine=1.0)
    sgl = M.surf('sigil', 's4566_sigil.png', fx=1)
    boxq(b, -50, 0, -34, 50, 90, 34, 1 / 50.0)
    quad(o, (-40, 90.2, -28), (30, 90.2, -28), (30, 90.2, 28), (-40, 90.2, 28))
    boxq(b, -44, 90, -30, 36, 96, 30, 1 / 50.0) if False else None
    boxq(b, 50, 50, -26, 76, 54, 26, 1 / 50.0)                                   # output tray
    quad(sgl, (52, 54.2, -24), (74, 54.2, -24), (74, 54.2, 24), (52, 54.2, 24))
    for y in (20, 44):
        boxq(b, -46, y, -36, 46, y + 18, -34, 1 / 50.0)
    boxq(M.surf('panel', 'indev_b34console.png' if False else 's1508_face.png', fx=1), 34, 90, -30, 48, 96, -14, 0.1)
    return M


def octopus():
    T(PROPS, 's5582_skin.png', (190, 110, 90), 12, 25, 1.2)
    M = Model()
    s = M.surf('skin', 's5582_skin.png', shine=0.9)
    blob(s, (0, 22, 4), (13, 15, 15), rings=12, segs=16)
    for e in (-1, 1):
        blob(M.surf('eye', 's3938_tyre.png', shine=1.0), (e * 7, 18, -9), (2.4, 2.4, 2.4), rings=6, segs=8)
    for k in range(8):
        a = k * math.pi / 4
        pts = [(math.cos(a) * 8, 10, math.sin(a) * 8)]
        for j in range(1, 6):
            rr = 8 + j * 9
            aa = a + math.sin(j * 0.9 + k) * 0.5
            pts.append((math.cos(aa) * rr, max(1.5, 10 - j * 3), math.sin(aa) * rr))
        tube(s, pts, lambda i: max(0.6, 4 - i * 0.65), 8)
    return M


def dodo():
    T(PROPS, 's711_feather.png', (120, 116, 110), 14, 26, 1.0)
    solid_tex(PROPS, 's711_beak.png', (200, 180, 120), 8, 27)
    M = Model()
    f = M.surf('feather', 's711_feather.png', shine=0.1)
    bk = M.surf('beak', 's711_beak.png', shine=0.3)
    blob(f, (0, 40, 4), (20, 22, 26), rings=12, segs=16)
    tube(f, [(0, 52, -14), (0, 66, -18), (0, 72, -20)], lambda i: (8, 7, 7)[i], 10)
    blob(f, (0, 76, -22), (8, 8, 9), rings=10, segs=12)
    tube(bk, [(0, 76, -28), (0, 74, -38), (0, 70, -42)], lambda i: (4, 3.4, 1.6)[i], 10)
    blob(bk, (0, 70, -42), (2.4, 3, 2.4), rings=6, segs=8)
    for e in (-1, 1):
        tube(bk, [(e * 7, 22, 4), (e * 7, 10, 2), (e * 7, 1, 0)], lambda i: (2.4, 1.8, 1.6)[i], 8)
        blob(bk, (e * 7, 1, -4), (3, 1, 5), rings=4, segs=8)
        blob(M.surf('eye', 's3938_tyre.png', shine=1.0), (e * 6, 79, -26), (1.4, 1.4, 1.4), rings=4, segs=6)
    blob(M.S['feather'], (0, 50, 28), (8, 8, 6), rings=6, segs=10)
    return M


def shrub():
    T(PROPS, 's324_leaf.png', (60, 110, 50), 16, 28, 1.0)
    T(PROPS, 's324_soil.png', (70, 52, 36), 12, 29)
    solid_tex(PROPS, 's324_berry.png', (240, 190, 200), 8, 30)
    solid_tex(PROPS, 's324_flower.png', (250, 250, 246), 4, 31)
    M = Model()
    l = M.surf('leaf', 's324_leaf.png', shine=0.4, fx=16)
    pot = M.surf('pot', 's1001_pot.png' if False else 's4566_body.png', shine=0.3)
    so = M.surf('soil', 's324_soil.png')
    lathe(pot, [(0, 0), (30, 0), (36, 40), (0, 40)], 20, lambda i: i / 3.0)
    lathe(so, [(0, 38), (34, 38)], 20, lambda i: i)
    tube(M.surf('bark', 's1445_wood.png'), [(0, 38, 0), (2, 70, 0), (-2, 100, 2)], lambda i: 3, 8)
    for k in range(70):
        y = 70 + RND.uniform(0, 80)
        a = RND.uniform(0, 6.28)
        rr = 40 * math.sin(math.pi * (y - 60) / 100) + 6
        c = (math.cos(a) * rr * RND.uniform(0.4, 1), y, math.sin(a) * rr * RND.uniform(0.4, 1))
        tip = add(c, (RND.uniform(-6, 6), RND.uniform(2, 8), RND.uniform(-6, 6)))
        quad(l, c, add(c, (2.5, 0, 0)), tip, add(tip, (-2.5, 0, 0)))
    for k in range(18):
        a = RND.uniform(0, 6.28)
        p = (math.cos(a) * 30, 90 + RND.uniform(-15, 30), math.sin(a) * 30)
        blob(M.surf('berry' if k % 2 else 'flower', 's324_berry.png' if k % 2 else 's324_flower.png', shine=0.8), p, (1.6, 1.6, 1.6), rings=4, segs=6)
    return M


def okapi():
    T(PROPS, 's1807_hide.png', (70, 40, 30), 10, 32, 1.0)
    st = Image.new('RGB', (128, 128), (230, 226, 216))
    d = ImageDraw.Draw(st)
    for y in range(0, 128, 14):
        d.rectangle([0, y, 128, y + 7], fill=(40, 24, 20))
    tex(st, PROPS, 's1807_stripes.png')
    solid_tex(PROPS, 's1807_flesh.png', (150, 50, 50), 10, 33)
    solid_tex(PROPS, 's1807_void.png', (4, 2, 2), 2, 34)
    M = Model()
    h = M.surf('hide', 's1807_hide.png', shine=0.2)
    st = M.surf('stripes', 's1807_stripes.png', shine=0.2)
    fl = M.surf('flesh', 's1807_flesh.png', shine=0.6)
    vd = M.surf('void', 's1807_void.png', fx=1)
    # lying on its side on a steel table (body along x)
    blob(h, (0, 22, 0), (55, 22, 26), rings=12, segs=18)
    tube(h, [(48, 26, 0), (70, 34, -4), (90, 40, -6)], lambda i: (12, 9, 7)[i], 12)
    blob(h, (98, 40, -6), (16, 9, 9), rings=10, segs=12)
    for e in (-1, 1):
        blob(h, (90, 50, -6 + e * 6), (3, 7, 2), rings=4, segs=6)
    for x in (-40, 30):
        for dz in (-8, 8):
            tube(st, [(x, 12, dz), (x + 20, 6, dz - 20), (x + 36, 4, dz - 34)], lambda i: (6, 4.5, 3.5)[i], 10)
    quad(vd, (-20, 40, -24.5), (20, 40, -24.5), (20, 14, -24.5), (-20, 14, -24.5))     # the opening
    for (a, b) in (((-20, 40), (20, 40)), ((20, 14), (-20, 14))):
        tube(fl, [(a[0], a[1], -25), (b[0], b[1], -25)], lambda i: 1.4, 6)
    quad(fl, (-22, 40, -26), (22, 40, -26), (22, 46, -40), (-22, 46, -40))             # the flap
    tube(M.surf('tag', 's1007_brass.png'), [(98, 52, 2), (98, 52, 6)], lambda i: 1.5, 6)
    return M


def ovoid():
    T(PROPS, 's1564_brass.png', (180, 140, 60), 14, 35, 1.0)
    M = Model()
    s = M.surf('brass', 's1564_brass.png', shine=1.0)
    lathe(s, [(0, 0), (20, 4), (34, 22), (38, 50), (34, 90), (22, 120), (0, 140)], 32, lambda i: i / 6.0)
    for y in (30, 70, 110):
        ring(M.surf('bronze', 's629_bronze.png', shine=0.9), (0, y, 0), {30: 33.5, 70: 37, 110: 27.5}[y], 1.2, 'y', 40, 6)
    return M


def venus():
    T(PROPS, 's1575_marble.png', (232, 230, 224), 6, 36, 1.6)
    M = Model()
    m = M.surf('marble', 's1575_marble.png', shine=0.7)
    lathe(m, [(0, 0), (90, 0), (90, 30), (70, 34), (70, 50), (0, 50)], 32, lambda i: i / 5.0)     # base and basin
    lathe(m, [(66, 50), (66, 60), (60, 60), (0, 52)], 32, lambda i: i / 3.0)
    lathe(m, [(0, 50), (36, 50), (30, 90), (28, 140)], 24, lambda i: i / 3.0)                    # the plinth
    k = len(m.V)
    biped(m, 270, 1.0)
    xform(m, k, lambda p: (p[0], p[1] + 140, p[2]))
    lathe(m, [(26, 140), (30, 200), (22, 270), (18, 280)], 24, lambda i: i / 3.0)                # the wrappings
    return M


def sphere():
    T(PROPS, 's3085_grey.png', (128, 128, 130), 3, 37, 2.0)
    M = Model()
    blob(M.surf('grey', 's3085_grey.png', fx=1), (0, 0, 0), (100, 100, 100), rings=24, segs=32)
    return M


# ============================================================================ items (cm)
def dice():
    im = Image.new('RGB', (128, 128), (200, 30, 40))
    d = ImageDraw.Draw(im)
    d.text((64, 64), '20', font=F(48), fill=(255, 255, 255), anchor='mm')
    tex(im, ITEMS, 's1974_face.png')
    M = Model()
    s = M.surf('d', 's1974_face.png', shine=0.9)
    blob(s, (0, 1.2, 0), (1.2, 1.2, 1.2), e=1.0, rings=4, segs=5, uv=(0.2, 0.2, 0.8, 0.8))
    blob(s, (2.8, 1.2, 0.6), (1.2, 1.2, 1.2), e=1.0, rings=4, segs=5, uv=(0.2, 0.2, 0.8, 0.8))
    return M


def pillbottle(name, rgb, label, pill):
    lb = Image.new('RGB', (256, 64), (240, 240, 236))
    d = ImageDraw.Draw(lb)
    d.text((128, 32), label, font=F(22), fill=(30, 30, 30), anchor='mm')
    tex(lb.transpose(Image.FLIP_TOP_BOTTOM), ITEMS, 's%s_label.png' % name)
    solid_tex(ITEMS, 's%s_bottle.png' % name, rgb, 6, hash(name) % 100)
    solid_tex(ITEMS, 's%s_pill.png' % name, pill, 4, hash(name) % 50)
    M = Model()
    b = M.surf('bottle', 's%s_bottle.png' % name, shine=0.9, alpha=0.75)
    l = M.surf('label', 's%s_label.png' % name, shine=0.3)
    c = M.surf('cap', 's3938_tyre.png', shine=0.4)
    lathe(b, [(0, 0), (2.4, 0), (2.5, 6), (1.8, 7), (0, 7)], 20, lambda i: i / 4.0)
    lathe(l, [(2.55, 1.5), (2.55, 5)], 24, lambda i: i)
    lathe(c, [(1.9, 7), (2.0, 8.4), (0, 8.4)], 16, lambda i: i / 2.0)
    for k in range(3):
        blob(M.surf('pill', 's%s_pill.png' % name, shine=0.6), (3.5 + k * 1.2, 0.3, -2 + k), (0.5, 0.3, 0.5), rings=4, segs=8)
    return M


def stapler():
    solid_tex(ITEMS, 's3709_black.png', (26, 26, 28), 4, 40)
    M = Model()
    b = M.surf('b', 's3709_black.png', shine=0.9)
    boxq(b, -1.8, 0, -8, 1.8, 0.8, 8, 0.2)
    k = len(b.V)
    boxq(b, -1.5, 0, -7.6, 1.5, 1.6, 7.4, 0.2)
    xform(b, k, lambda p: rot('x', -6, (0, 0, 7))((p[0], p[1] + 1.4, p[2])))
    tube(M.surf('pin', 's3938_chrome.png', shine=1.0), [(-1.8, 1.4, 7), (1.8, 1.4, 7)], lambda i: 0.4, 6)
    return M


def cardcase():
    M = Model()
    s = M.surf('al', 's3938_chrome.png', shine=1.0)
    boxq(s, -4.5, 0, -2.8, 4.5, 0.8, 2.8, 0.2)
    boxq(M.surf('card', 's4890_pages.png'), -4, 0.8, -2.6, 4.4, 0.9, 2.4, 0.2)
    return M


def travelbook():
    cv = Image.new('RGB', (256, 320), (30, 110, 150))
    d = ImageDraw.Draw(cv)
    d.text((128, 70), '1001 PLACES', font=F(30), fill=(255, 255, 255), anchor='mm')
    d.text((128, 110), 'TO BE BEFORE', font=F(24), fill=(255, 230, 140), anchor='mm')
    d.text((128, 140), 'YOU DIE', font=F(24), fill=(255, 230, 140), anchor='mm')
    d.ellipse([78, 180, 178, 280], fill=(240, 200, 60))
    d.text((128, 300), 'Rachel McPhee', font=F(18, FR), fill=(230, 230, 230), anchor='mm')
    tex(cv, ITEMS, 's1841_cover.png')
    M = Model()
    c = M.surf('cover', 's1841_cover.png', shine=0.4)
    boxq(M.surf('pages', 's4890_pages.png'), -7, 0.2, -10, 7, 3.6, 10, 0.1)
    quad(c, (-7.2, 3.8, -10.2), (7.2, 3.8, -10.2), (7.2, 3.8, 10.2), (-7.2, 3.8, 10.2))
    quad(c, (-7.2, 0, 10.2), (7.2, 0, 10.2), (7.2, 0, -10.2), (-7.2, 0, -10.2), (0, 0, 0.05, 0.05))
    boxq(c, -7.6, 0, -10.2, -7.0, 3.8, 10.2, 0.01)
    return M


def grapes():
    solid_tex(ITEMS, 's1255_grape.png', (200, 60, 90), 12, 41)
    M = Model()
    g = M.surf('g', 's1255_grape.png', shine=1.0)
    tube(M.surf('stem', 's1445_wood.png'), [(0, 14, 0), (0, 10, 0), (0, 2, 0)], lambda i: 0.3, 5)
    Image.open(os.path.join(PROPS, 's1445_wood.png')).save(os.path.join(ITEMS, 's1445_wood.png'))
    for k in range(18):
        y = 11 - k * 0.55
        rr = 3.2 * math.sin(math.pi * (k + 2) / 22) + 0.4
        a = k * 2.3
        blob(g, (math.cos(a) * rr, y, math.sin(a) * rr), (1.1, 1.2, 1.1), rings=6, segs=8)
    return M


def caplets():
    solid_tex(ITEMS, 's4193_foil.png', (200, 200, 206), 8, 42)
    solid_tex(ITEMS, 's4193_blue.png', (40, 90, 220), 6, 43)
    M = Model()
    boxq(M.surf('foil', 's4193_foil.png', shine=1.0), -4, 0, -6, 4, 0.2, 6, 0.2)
    for i in range(2):
        for j in range(4):
            blob(M.surf('cap', 's4193_blue.png', shine=0.9), (-2 + i * 4, 0.5, -4.5 + j * 3), (1.2, 0.4, 0.6), rings=6, segs=8)
    return M


def cereal():
    bx = Image.new('RGB', (256, 320), (110, 60, 30))
    d = ImageDraw.Draw(bx)
    d.text((128, 40), "JUDY'S", font=F(36), fill=(255, 220, 80), anchor='mm')
    d.text((128, 84), 'CHOCO-WONDER', font=F(28), fill=(255, 255, 255), anchor='mm')
    d.text((128, 118), 'EXPLOSION!', font=F(28), fill=(255, 120, 200), anchor='mm')
    cols = [(255, 120, 200), (120, 220, 255), (255, 240, 120), (160, 255, 160), (220, 160, 255), (255, 170, 120)]
    for k, c in enumerate(cols):
        a = math.pi * (0.1 + 0.16 * k)
        d.ellipse([128 - math.cos(a) * 90 - 12, 250 - math.sin(a) * 90 - 12, 128 - math.cos(a) * 90 + 12, 250 - math.sin(a) * 90 + 12], fill=c)
    d.text((128, 300), "Dr. Wondertainment", font=F(16), fill=(255, 255, 255), anchor='mm')
    tex(bx, ITEMS, 's2983_box.png')
    M = Model()
    s = M.surf('box', 's2983_box.png', shine=0.4)
    quad(s, (-10, 0, -3.5), (10, 0, -3.5), (10, 28, -3.5), (-10, 28, -3.5))
    quad(s, (10, 0, 3.5), (-10, 0, 3.5), (-10, 28, 3.5), (10, 28, 3.5))
    boxq(M.surf('side', 's3938_cover.png' if False else 's2983_box.png'), -10.1, 0, -3.4, 10.1, 28, 3.4, 0.0)
    return M


def polaroid():
    solid_tex(ITEMS, 's5701_body.png', (30, 30, 32), 6, 44)
    solid_tex(ITEMS, 's5701_white.png', (240, 240, 236), 4, 45)
    M = Model()
    b = M.surf('b', 's5701_body.png', shine=0.6)
    w = M.surf('w', 's5701_white.png', shine=0.4)
    boxq(b, -7, 0, -5, 7, 8, 5, 0.2)
    k = len(b.V)
    boxq(b, -7, 8, -5, 7, 11, 1, 0.2)
    lathe(M.surf('lens', 's3938_tyre.png', shine=1.0), [(0, 0), (2.4, 0), (2.4, 1.2), (0, 1.2)], 20, lambda i: i / 3.0)
    xform(M.S['lens'], 0, lambda p: (p[0] - 1, p[2] + 5, -p[1] - 5))
    boxq(w, -7.1, 0, -5.1, 7.1, 2, 5.1, 0.2)
    for x in (-4, 3):
        boxq(M.surf('rainbow', 's1974_face.png', fx=1), x, 6, -5.2, x + 1, 7, -5.1, 0.1)
    return M


PROP_MODELS = [('scp629', misterbrass), ('scp5147', mannequin), ('scp1508', chorebuddy), ('scp5199', cradle),
               ('scp2792', rabbitdoll), ('scp1731', fridge), ('scp1970', tvset), ('scp1445', chair),
               ('scp1969', discoball), ('scp3016', top), ('scp2597', weight), ('scp2414', trapezohedron),
               ('scp1404', bowl), ('scp1473', printer), ('scp4566', copier), ('scp5582', octopus), ('scp711', dodo),
               ('scp324', shrub), ('scp1807', okapi), ('scp1564', ovoid), ('scp1575', venus), ('scp3085', sphere)]
ITEM_MODELS = [('dice1974', dice), ('pills3866', lambda: pillbottle('3866', (230, 230, 230), 'NO LABEL', (240, 240, 240))),
               ('stapler3709', stapler), ('cards3803', cardcase), ('book1841', travelbook), ('grapes1255', grapes),
               ('caps4193', caplets), ('tabs5604', lambda: pillbottle('5604', (160, 110, 60), 'R-IN', (140, 20, 20))),
               ('cereal2983', cereal), ('camera5701', polaroid)]

if __name__ == '__main__':
    for f in ('s3938_tyre.png', 's3938_chrome.png', 's1007_brass.png', 's4890_pages.png', 's1445_wood.png', 's1508_face.png'):
        for folder in (PROPS, ITEMS):
            src = [os.path.join(x, f) for x in (PROPS, ITEMS) if os.path.exists(os.path.join(x, f))]
            if src and not os.path.exists(os.path.join(folder, f)):
                Image.open(src[0]).save(os.path.join(folder, f))
    out = {}
    for name, fn in PROP_MODELS:
        m = fn()
        m.write(os.path.join(PROPS, name + '.b3d'))
        out[name] = (m, PROPS)
    for f in ('s1445_wood.png', 's1508_face.png', 's4890_pages.png'):
        if not os.path.exists(os.path.join(ITEMS, f)):
            Image.open(os.path.join(PROPS, f) if os.path.exists(os.path.join(PROPS, f)) else os.path.join(ITEMS, f)).save(os.path.join(ITEMS, f))
    for name, fn in ITEM_MODELS:
        m = fn()
        m.write(os.path.join(ITEMS, name + '.b3d'))
        out[name] = (m, ITEMS)
    print('%d models, %d triangles' % (len(out), sum(m.tris() for m, _ in out.values())))
    tiles = []
    for name, (m, folder) in out.items():
        pts = [v[:3] for s in m.S.values() for v in s.V]
        lo = [min(p[i] for p in pts) for i in range(3)]
        hi = [max(p[i] for p in pts) for i in range(3)]
        c = [(lo[i] + hi[i]) / 2 for i in range(3)]
        r = max(hi[i] - lo[i] for i in range(3))
        eye = (c[0] + r * 0.9, c[1] + r * 0.7, c[2] - r * 1.3)
        im = render(m, folder, eye, c, size=(256, 256), fov=45, bg=(30, 30, 34))
        tiles.append(im)
        if folder == ITEMS:
            render(m, folder, eye, c, size=(256, 256), fov=45, bg=(0, 0, 0)).resize((64, 64), Image.LANCZOS).save(
                os.path.join(ITEMS, 'INV%s.png' % name))
    cols = 8
    sheet = Image.new('RGB', (256 * cols, 256 * ((len(tiles) + cols - 1) // cols)))
    for i, t in enumerate(tiles):
        sheet.paste(t, ((i % cols) * 256, (i // cols) * 256))
    sheet.save(os.path.join(PREV, 'hd34_models.png'))
    print('previews and icons written')
