r"""High-detail models for batch 30, Site-42 (original work after the SCP articles on scp-wiki.wikidot.com, CC BY-SA 3.0).
Items (GFX\items, cm units):
  thermal4427.b3d   a hand-held thermographic camera - rubber-armoured body, lens barrel with focus ring and
                    germanium lens, a pistol grip and trigger, a rear screen showing a thermal image, a wrist strap
  phone4433.b3d     a cheap flip phone, open, ringing: "RESTRICTED NUMBER" on the screen, a worn keypad
  card2758.b3d      Room G14's custom identification card on a clip and a short lanyard
  jar3069.b3d       a specimen jar from SCP-3069's Access Point I: glass, cloudy preserving fluid, a sealed lid with a
                    label, and inside it a pale deep-sea thing with a glowing lure and trailing tentacles
Props (GFX\map\props, room units):
  scp2648.b3d       SCP-2648: a rolling amalgam of earth, flesh and everything it has picked up - logs, bushes,
                    pineapples, plastic turf mesh, mushrooms, and the red fluid it weeps
  scp3069a.b3d      a replica of SCP-3069-A: a steel pole on a bolted base, field coils, a phosphorescent green sphere
  scp4434c.b3d      an SCP-4434-C skull: a deer's skull with a predator's teeth and too many antler tines
   python make_hd30.py"""
import math
import os
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from make_hd29 import Model, grid, tube, lathe, card, nrm, cross, sub, add, render, ITEMS, PROPS, PREV

FB = r'C:\Windows\Fonts\arialbd.ttf'
FR = r'C:\Windows\Fonts\arial.ttf'
FM = r'C:\Windows\Fonts\courbd.ttf'


def F(n, f=FB):
    return ImageFont.truetype(f, n)


# ============================================================================ more shapes
def xform(s, start, fp):
    """apply fp (a function of a point) to the vertices added since `start`; normals follow (by differencing)"""
    for k in range(start, len(s.V)):
        v = s.V[k]
        p = fp((v[0], v[1], v[2]))
        q = fp((v[0] + v[3] * 0.01, v[1] + v[4] * 0.01, v[2] + v[5] * 0.01))
        n = nrm(sub(q, p))
        s.V[k] = (p[0], p[1], p[2], n[0], n[1], n[2]) + tuple(v[6:])


def rot(ax, deg, c=(0, 0, 0)):
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)

    def f(p):
        x, y, z = p[0] - c[0], p[1] - c[1], p[2] - c[2]
        if ax == 'x':
            y, z = y * ca - z * sa, y * sa + z * ca
        elif ax == 'y':
            x, z = x * ca + z * sa, -x * sa + z * ca
        else:
            x, y = x * ca - y * sa, x * sa + y * ca
        return (x + c[0], y + c[1], z + c[2])
    return f


def blob(s, c, r, e=1.0, rings=14, segs=20, uv=(0, 0, 1, 1), disp=None, col=None):
    """a superellipsoid (e < 1 boxy, 1 = ellipsoid) centred at c, radii r; disp(dir) -> radial scale"""
    u0, v0, u1, v1 = uv
    sg = lambda x: math.copysign(abs(x) ** e, x)

    def P(i, j):
        th = -math.pi / 2 + math.pi * i / rings
        ph = 2 * math.pi * j / segs
        d = (math.cos(th) * math.cos(ph), math.sin(th), math.cos(th) * math.sin(ph))
        k = disp(d) if disp else 1.0
        return (c[0] + sg(d[0]) * r[0] * k, c[1] + sg(d[1]) * r[1] * k, c[2] + sg(d[2]) * r[2] * k)
    grid(s, P, rings, segs, lambda i, j: (u0 + (u1 - u0) * j / segs, v0 + (v1 - v0) * (1 - i / rings)), col=col)


def quad(s, p0, p1, p2, p3, uv=(0, 0, 1, 1), col=(1, 1, 1)):
    """one-sided quad p0 p1 p2 p3 (counter-clockwise seen from the front: bottom-left, bottom-right, top-right,
    top-left); texture uv rect"""
    n = nrm(cross(sub(p3, p0), sub(p1, p0)))       # Blitz is left-handed: bl br tr tl as the viewer sees them
    u0, v0, u1, v1 = uv
    base = len(s.V)
    for p, (u, v) in zip((p0, p1, p2, p3), ((u0, v1), (u1, v1), (u1, v0), (u0, v0))):
        s.V.append((p[0], p[1], p[2], n[0], n[1], n[2], col[0], col[1], col[2], u, v))
    s.T.append((base, base + 2, base + 1))
    s.T.append((base, base + 3, base + 2))


def noise_tex(size, base, amp, blur=0.8, seed=0):
    a = np.random.default_rng(seed).normal(0, amp, (size, size, 1)).astype(np.float32) + np.array(base, np.float32)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(blur))


def save_item(im, name):
    im.save(os.path.join(ITEMS, name))


def save_prop(im, name):
    im.save(os.path.join(PROPS, name))


# ============================================================================ the thermal camera (SCP-4427)
def thermal():
    p = noise_tex(256, (200, 158, 34), 7, 0.6, 1)
    d = ImageDraw.Draw(p)
    d.text((20, 200), 'SITE-42  THERMOGRAPHIC', font=F(16), fill=(40, 34, 20))
    save_item(p, 't4427_body.png')
    r = Image.new('RGB', (256, 256), (26, 26, 28))
    d = ImageDraw.Draw(r)
    for y in range(0, 256, 8):
        d.rectangle([0, y, 256, y + 3], fill=(38, 38, 40))
    save_item(r.filter(ImageFilter.GaussianBlur(0.6)), 't4427_rubber.png')
    sc = np.zeros((240, 320, 3), np.float32)
    yy, xx = np.mgrid[0:240, 0:320].astype(np.float32)
    heat = 0.25 + 0.15 * np.sin(xx / 40) * np.cos(yy / 33)
    heat += 0.85 * np.exp(-(((xx - 170) ** 2 + (yy - 110) ** 2) / (2 * 38.0 ** 2)))     # the sphere
    heat = np.clip(heat, 0, 1)
    pal = np.array([(20, 0, 40), (90, 0, 120), (200, 30, 60), (250, 140, 20), (255, 245, 180)], np.float32)
    idx = heat * (len(pal) - 1)
    lo = np.floor(idx).astype(int).clip(0, len(pal) - 2)
    f = (idx - lo)[..., None]
    sc = pal[lo] * (1 - f) + pal[lo + 1] * f
    im = Image.fromarray(sc.astype(np.uint8))
    d = ImageDraw.Draw(im)
    d.text((10, 8), '37.8 C', font=F(20), fill=(255, 255, 255))
    d.line([(160, 110), (180, 110)], fill=(255, 255, 255), width=2)
    d.line([(170, 100), (170, 120)], fill=(255, 255, 255), width=2)
    d.rectangle([0, 0, 319, 239], outline=(10, 10, 10), width=6)
    save_item(im, 't4427_screen.png')
    g = Image.new('RGB', (128, 128), (10, 12, 18))
    d = ImageDraw.Draw(g)
    d.ellipse([20, 20, 108, 108], fill=(30, 40, 60))
    d.ellipse([34, 28, 60, 50], fill=(140, 160, 200))
    save_item(g, 't4427_lens.png')
    M = Model()
    body = M.surf('body', 't4427_body.png', shine=0.25)
    rub = M.surf('rubber', 't4427_rubber.png', shine=0.1)
    scr = M.surf('screen', 't4427_screen.png', fx=1)
    lens = M.surf('lens', 't4427_lens.png', shine=1.0)
    blob(body, (0, 12, 0), (4.6, 5.4, 8.0), e=0.35, rings=14, segs=24)               # the body
    blob(rub, (0, 12, -0.5), (4.8, 5.6, 6.2), e=0.3, rings=10, segs=24)             # rubber armour round its middle
    k = len(rub.V)                                                                  # the lens barrel, along +z
    lathe(rub, [(0.0, 0), (3.4, 0), (3.6, 0.6), (3.6, 2.4), (3.9, 2.6), (3.9, 4.2), (3.5, 4.4), (3.3, 6.2), (2.9, 6.4)], 28,
          lambda i: i / 4.0)
    xform(rub, k, lambda q: rot('x', 90)((q[0], q[1], q[2]))[0:1] + (rot('x', 90)(q)[1] + 13, rot('x', 90)(q)[2] + 7.4))
    k = len(lens.V)
    lathe(lens, [(2.9, 0), (2.4, 0.3), (1.2, 0.5), (0.0, 0.55)], 28, lambda i: i / 3.0)
    xform(lens, k, lambda q: (rot('x', 90)(q)[0], rot('x', 90)(q)[1] + 13, rot('x', 90)(q)[2] + 13.8))
    quad(scr, (-3.4, 9.2, -8.15), (3.4, 9.2, -8.15), (3.4, 15.2, -8.15), (-3.4, 15.2, -8.15))   # the rear screen
    blob(rub, (0, 4.5, 1.0), (2.2, 5.0, 2.8), e=0.6, rings=10, segs=16)              # the grip
    k = len(rub.V)
    blob(rub, (0, 0, 0), (0.6, 1.4, 0.9), e=0.7, rings=6, segs=10)                   # the trigger
    xform(rub, k, lambda q: (q[0], q[1] + 7.2, q[2] + 3.6))
    for x in (-1.4, 0, 1.4):                                                         # buttons on top
        blob(body, (x, 17.5, -4.5), (0.5, 0.35, 0.5), e=0.6, rings=5, segs=8)
    st = M.surf('strap', 't4427_rubber.png', fx=16)
    card(st, (2.4, 1.0, -1.5), (3.2, -3.0, -0.5), 1.0, 1.0, (0, 0, 1))
    return M


# ============================================================================ the flip phone (SCP-4433)
def phone():
    b = noise_tex(256, (150, 154, 160), 6, 0.5, 2)
    save_item(b, 'p4433_body.png')
    k = Image.new('RGB', (256, 384), (60, 62, 66))
    d = ImageDraw.Draw(k)
    keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '0', '#']
    d.rounded_rectangle([20, 14, 236, 70], 18, fill=(90, 92, 96))
    d.ellipse([98, 20, 158, 64], fill=(120, 122, 126))
    for i, t in enumerate(keys):
        x, y = 30 + (i % 3) * 70, 90 + (i // 3) * 70
        d.rounded_rectangle([x, y, x + 58, y + 54], 14, fill=(200, 202, 206))
        d.text((x + 29, y + 27), t, font=F(28), fill=(30, 30, 34), anchor='mm')
    d.rounded_rectangle([30, 90, 88, 144], 14, fill=(80, 190, 90))               # the green key, worn
    save_item(k, 'p4433_keys.png')
    s = Image.new('RGB', (256, 320), (150, 200, 150))
    d = ImageDraw.Draw(s)
    d.rectangle([0, 0, 255, 319], outline=(20, 20, 20), width=14)
    d.text((128, 70), 'INCOMING CALL', font=F(24), fill=(20, 40, 20), anchor='mm')
    d.text((128, 140), 'RESTRICTED', font=F(30), fill=(20, 40, 20), anchor='mm')
    d.text((128, 180), 'NUMBER', font=F(30), fill=(20, 40, 20), anchor='mm')
    d.text((128, 260), '( MOM )', font=F(22), fill=(60, 80, 60), anchor='mm')
    save_item(s, 'p4433_screen.png')
    M = Model()
    body = M.surf('body', 'p4433_body.png', shine=0.6)
    keys_ = M.surf('keys', 'p4433_keys.png', shine=0.3)
    scr = M.surf('screen', 'p4433_screen.png', fx=1)
    blob(body, (0, 0.8, -4.8), (2.6, 0.8, 4.8), e=0.35, rings=10, segs=20)            # the lower half, keypad up
    quad(keys_, (-2.2, 1.7, -9.0), (2.2, 1.7, -9.0), (2.2, 1.7, -1.0), (-2.2, 1.7, -1.0))
    k = len(body.V)
    blob(body, (0, 0.7, 4.6), (2.6, 0.7, 4.6), e=0.35, rings=10, segs=20)             # the upper half, opened 160 deg
    k2 = len(scr.V)
    quad(scr, (-1.9, 1.5, 1.0), (1.9, 1.5, 1.0), (1.9, 1.5, 8.2), (-1.9, 1.5, 8.2))
    tilt = rot('x', -20, (0, 0.8, 0))
    xform(body, k, tilt)
    xform(scr, k2, tilt)
    k = len(body.V)
    lathe(body, [(0.75, -2.4), (0.75, 2.4)], 16, lambda i: i)                       # the hinge, along x
    xform(body, k, lambda q: (rot('z', 90)(q)[0], rot('z', 90)(q)[1] + 0.9, rot('z', 90)(q)[2]))
    blob(body, (1.9, 2.6, 8.8), (0.35, 0.9, 0.35), e=0.8, rings=6, segs=10)          # the antenna stub
    return M


# ============================================================================ Room G14's custom ID card (SCP-2758)
def idcard():
    c = Image.new('RGB', (512, 320), (236, 238, 232))
    d = ImageDraw.Draw(c)
    d.rectangle([0, 0, 512, 64], fill=(40, 70, 130))
    d.text((20, 32), 'SITE-42  |  MULTI-U DEPT.', font=F(28), fill=(255, 255, 255), anchor='lm')
    d.rectangle([24, 90, 164, 270], fill=(180, 186, 196))
    d.ellipse([60, 110, 128, 180], fill=(110, 116, 128))
    d.rounded_rectangle([44, 178, 144, 270], 30, fill=(110, 116, 128))
    d.text((190, 100), 'ROOM G14', font=F(40), fill=(20, 20, 30))
    d.text((190, 150), 'CUSTOM IDENTIFICATION', font=F(20), fill=(40, 40, 50))
    d.text((190, 180), 'SAFE-CLASS WING A4', font=F(20), fill=(40, 40, 50))
    d.text((190, 210), 'LOCKER #2758', font=F(20), fill=(140, 30, 30))
    for x in range(190, 480, 6):
        d.rectangle([x, 250, x + (2 if x % 18 else 4), 296], fill=(10, 10, 10))
    save_item(c, 'c2758_front.png')
    bk = Image.new('RGB', (512, 320), (220, 222, 216))
    d = ImageDraw.Draw(bk)
    d.rectangle([0, 40, 512, 100], fill=(20, 20, 20))                               # the magnetic stripe
    d.text((256, 200), 'PROPERTY OF THE FOUNDATION', font=F(22), fill=(60, 60, 60), anchor='mm')
    d.text((256, 240), 'IF FOUND RETURN TO SITE-42 SECURITY', font=F(18, FR), fill=(60, 60, 60), anchor='mm')
    save_item(bk, 'c2758_back.png')
    save_item(noise_tex(64, (40, 60, 120), 10, 0.5, 3), 'c2758_lanyard.png')
    M = Model()
    edge = M.surf('edge', 'c2758_lanyard.png', shine=0.5, tint=(1.6, 1.6, 1.4))
    fr = M.surf('front', 'c2758_front.png', shine=0.5)
    bk_ = M.surf('back', 'c2758_back.png', shine=0.5)
    ly = M.surf('lanyard', 'c2758_lanyard.png', fx=16)
    blob(edge, (0, 0, 0), (4.3, 0.07, 2.7), e=0.2, rings=6, segs=16)
    quad(fr, (-4.25, 0.1, -2.65), (4.25, 0.1, -2.65), (4.25, 0.1, 2.65), (-4.25, 0.1, 2.65))
    quad(bk_, (4.25, -0.1, -2.65), (-4.25, -0.1, -2.65), (-4.25, -0.1, 2.65), (4.25, -0.1, 2.65))
    k = len(edge.V)
    lathe(edge, [(0.6, -0.12), (0.75, 0), (0.6, 0.12)], 14, lambda i: i / 2)        # the clip ring
    xform(edge, k, lambda q: (q[0], q[1], q[2] + 3.2))
    card(ly, (0, 0, 3.8), (0, 0, 9.0), 1.2, 1.2, (1, 0, 0), nseg=2)
    return M


# ============================================================================ the specimen jar (SCP-3069)
def jar():
    save_item(noise_tex(128, (220, 230, 235), 4, 0.5, 4), 'j3069_glass.png')
    save_item(noise_tex(128, (120, 150, 120), 10, 1.5, 5), 'j3069_fluid.png')
    save_item(noise_tex(256, (150, 152, 150), 9, 0.5, 6), 'j3069_lid.png')
    sk = noise_tex(256, (210, 200, 205), 14, 1.2, 7)
    d = ImageDraw.Draw(sk)
    rnd = random.Random(3069)
    for _ in range(140):
        x, y = rnd.randrange(256), rnd.randrange(256)
        d.ellipse([x - 3, y - 2, x + 3, y + 2], fill=(150, 120, 150))
    save_item(sk, 'j3069_skin.png')
    save_item(Image.new('RGB', (32, 32), (120, 255, 200)), 'j3069_glow.png')
    lb = Image.new('RGB', (384, 192), (236, 230, 210))
    d = ImageDraw.Draw(lb)
    d.rectangle([4, 4, 379, 187], outline=(60, 60, 60), width=3)
    d.text((192, 34), 'SCP-3069 SPECIMEN 17', font=F(28), fill=(20, 20, 20), anchor='mm')
    d.text((192, 80), 'ACCESS POINT I  -  3500 m', font=F(20, FR), fill=(30, 30, 30), anchor='mm')
    d.text((192, 116), 'MTF GAMMA-6 "DEEP FEEDERS"', font=F(18, FR), fill=(30, 30, 30), anchor='mm')
    d.text((192, 156), 'DO NOT OPEN - SITE-42', font=F(22), fill=(160, 20, 20), anchor='mm')
    save_item(lb, 'j3069_label.png')
    M = Model()
    lid = M.surf('lid', 'j3069_lid.png', shine=0.8)
    skin = M.surf('skin', 'j3069_skin.png', shine=0.6)
    glow = M.surf('glow', 'j3069_glow.png', fx=1)
    lab = M.surf('label', 'j3069_label.png')
    fluid = M.surf('fluid', 'j3069_fluid.png', fx=1, alpha=0.38, tint=(0.75, 1.0, 0.85))
    glass = M.surf('glass', 'j3069_glass.png', shine=1.0, alpha=0.28)
    prof = [(0.0, 0.0), (5.6, 0.0), (6.0, 0.4), (6.0, 15.2), (5.4, 16.0), (4.6, 16.4)]
    lathe(glass, prof, 32, lambda i: i / 5.0)
    lathe(fluid, [(0.0, 0.4), (5.7, 0.4), (5.7, 14.0), (0.0, 14.0)], 28, lambda i: i / 3.0)
    lathe(lid, [(4.4, 16.2), (5.0, 16.3), (5.0, 17.6), (4.6, 18.0), (0.0, 18.1)], 32, lambda i: i / 4.0)
    a0, a1 = math.radians(-35), math.radians(35)
    for k in range(8):                                                       # the label, wrapped round the front
        t0 = a0 + (a1 - a0) * k / 8
        t1 = a0 + (a1 - a0) * (k + 1) / 8
        p = lambda t, y: (6.04 * math.sin(t), y, -6.04 * math.cos(t))
        quad(lab, p(t0, 3.0), p(t1, 3.0), p(t1, 8.0), p(t0, 8.0), uv=(k / 8, 0, (k + 1) / 8, 1))
    # the creature: a curled body, a ridge of fins, a stalk with a glowing lure, trailing tentacles
    path = [(2.5 * math.cos(t), 7.5 + 2.4 * math.sin(t * 0.7), 2.5 * math.sin(t)) for t in [i * 0.16 for i in range(26)]]
    tube(skin, path, lambda i: 0.4 + 1.5 * math.sin(math.pi * min(1.0, i / 22.0)) ** 0.8, 12, vrep=0.2)
    head = path[-1]
    blob(skin, head, (1.3, 1.1, 1.2), rings=10, segs=14)
    stalk = [add(head, (0, 0.5 * k, 0.15 * k * k)) for k in range(6)]
    tube(skin, stalk, lambda i: 0.18, 6, vrep=0.5)
    blob(glow, stalk[-1], (0.45, 0.45, 0.45), rings=8, segs=10)
    rnd = random.Random(30)
    for k in range(7):
        base = path[rnd.randint(2, 8)]
        tp = [add(base, (0.4 * j * math.cos(k + j * 0.4), -0.9 * j, 0.4 * j * math.sin(k + j * 0.3))) for j in range(7)]
        tube(skin, tp, lambda i: 0.22 * (1 - i / 7.0) + 0.04, 6, vrep=0.5)
    fins = M.surf('fins', 'j3069_skin.png', fx=16, alpha=0.7, tint=(1.0, 0.8, 0.9))
    for i in range(4, 20, 3):
        p0 = path[i]
        card(fins, p0, add(p0, (0, 1.4, 0)), 1.3, 0.3, nrm(sub(path[i + 1], path[i - 1])))
    return M


# ============================================================================ SCP-2648
def amalgam_tex():
    rnd = random.Random(2648)
    S = 1024
    a = np.zeros((S, S, 3), np.float32)
    a[:] = (74, 56, 40)
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    for _ in range(160):                       # patches: mud, grass, bark, flesh, wet red
        cx, cy, r = rnd.uniform(0, S), rnd.uniform(0, S), rnd.uniform(30, 120)
        kind = rnd.random()
        col = ((60, 90, 40) if kind < 0.3 else (90, 66, 44) if kind < 0.55 else (150, 90, 90) if kind < 0.75
               else (120, 24, 26) if kind < 0.85 else (50, 40, 32))
        dist = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
        m = np.clip(1 - dist / r, 0, 1) ** 0.6
        a = a * (1 - m[..., None]) + np.array(col, np.float32) * m[..., None]
    a += np.random.default_rng(2).normal(0, 12, (S, S, 1))
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    for _ in range(2500):                      # twigs, needles, grass blades
        x, y = rnd.randrange(S), rnd.randrange(S)
        L = rnd.randint(6, 26)
        an = rnd.uniform(0, math.pi)
        c = rnd.choice(((90, 70, 40), (70, 110, 50), (40, 30, 20), (160, 130, 90)))
        d.line([(x, y), (x + L * math.cos(an), y + L * math.sin(an))], fill=c, width=2)
    for _ in range(60):                        # glistening red streaks
        x, y = rnd.randrange(S), rnd.randrange(S)
        d.line([(x, y), (x + rnd.randint(-6, 6), y + rnd.randint(20, 70))], fill=(170, 20, 24), width=rnd.randint(3, 6))
    return im.filter(ImageFilter.GaussianBlur(0.8))


def pineapple_tex():
    im = Image.new('RGB', (256, 256), (170, 120, 40))
    d = ImageDraw.Draw(im)
    for y in range(-32, 288, 32):
        for x in range(-32, 288, 32):
            o = 16 if (y // 32) % 2 else 0
            d.polygon([(x + o, y), (x + o + 16, y + 16), (x + o, y + 32), (x + o - 16, y + 16)], fill=(196, 140, 52), outline=(90, 60, 20))
            d.ellipse([x + o - 3, y + 13, x + o + 3, y + 19], fill=(80, 50, 20))
    return im


def leaves_tex():
    rnd = random.Random(26480)
    im = Image.new('RGB', (256, 256), (0, 0, 0))
    d = ImageDraw.Draw(im)
    d.line([(128, 256), (128, 0)], fill=(70, 50, 30), width=4)
    for _ in range(160):
        y = rnd.randint(10, 250)
        e = rnd.choice((-1, 1))
        x1 = 128 + e * rnd.randint(30, 110)
        y1 = y - rnd.randint(10, 50)
        g = rnd.randint(70, 140)
        d.polygon([(128, y), (x1, y1), (x1 - e * 10, y1 + 14)], fill=(30, g, 30))
    return im


def turf_tex():
    im = Image.new('RGB', (256, 256), (0, 0, 0))
    d = ImageDraw.Draw(im)
    for x in range(0, 256, 16):                 # the plastic mesh
        d.line([(x, 0), (x, 256)], fill=(40, 70, 40), width=2)
        d.line([(0, x), (256, x)], fill=(40, 70, 40), width=2)
    rnd = random.Random(26481)
    for _ in range(900):
        x, y = rnd.randrange(256), rnd.randrange(256)
        d.line([(x, y), (x + rnd.randint(-4, 4), y - rnd.randint(8, 20))], fill=(60, rnd.randint(150, 200), 60), width=2)
    return im


def scp2648():
    save_prop(amalgam_tex(), 's2648_mass.png')
    save_prop(pineapple_tex(), 's2648_pine.png')
    save_prop(leaves_tex(), 's2648_leaves.png')
    save_prop(turf_tex(), 's2648_turf.png')
    save_prop(noise_tex(256, (92, 64, 44), 14, 0.8, 9), 's2648_wood.png')
    save_prop(noise_tex(128, (200, 190, 170), 10, 0.8, 10), 's2648_cap.png')
    save_prop(noise_tex(64, (150, 16, 20), 12, 0.8, 11), 's2648_fluid.png')
    rnd = random.Random(2648)
    R0 = 180.0
    M = Model()
    mass = M.surf('mass', 's2648_mass.png', fx=1 + 2, shine=0.3)
    wood = M.surf('wood', 's2648_wood.png', fx=1 + 2)
    pine = M.surf('pine', 's2648_pine.png', fx=1 + 2)
    leaf = M.surf('leaves', 's2648_leaves.png', fx=1 + 2 + 16, masked=True)
    turf = M.surf('turf', 's2648_turf.png', fx=1 + 2 + 16, masked=True)
    cap = M.surf('cap', 's2648_cap.png', fx=1 + 2)
    fl = M.surf('fluid', 's2648_fluid.png', fx=1 + 2, shine=1.0)
    bumps = [(nrm((rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-1, 1))), rnd.uniform(0.04, 0.16), rnd.uniform(0.2, 0.5)) for _ in range(46)]

    def disp(d):
        k = 1.0 + 0.04 * math.sin(d[0] * 9) * math.cos(d[2] * 7)
        for b, h, w in bumps:
            dot = d[0] * b[0] + d[1] * b[1] + d[2] * b[2]
            if dot > 1 - w:
                k += h * ((dot - (1 - w)) / w) ** 2
        return k

    def ao(p, n):
        up = max(0.0, n[1]) * 0.25 + 0.6
        low = min(1.0, (p[1] + 40) / (2 * R0)) * 0.3 + 0.7
        k = up * low
        return (k, k * 0.97, k * 0.95)
    blob(mass, (0, R0, 0), (R0, R0 * 0.92, R0), rings=44, segs=64, disp=disp, col=ao)

    def surface(d, sink=0.15):
        d = nrm(d)
        k = disp(d)
        return (d[0] * R0 * k * (1 - sink), R0 + d[1] * R0 * 0.92 * k * (1 - sink), d[2] * R0 * k * (1 - sink)), d
    for _ in range(7):                                                        # logs half sunk in it
        p, n = surface((rnd.uniform(-1, 1), rnd.uniform(-0.6, 1), rnd.uniform(-1, 1)), 0.05)
        t = nrm(cross(n, (rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-1, 1))))
        L = rnd.uniform(70, 130)
        tube(wood, [add(p, t, -L / 2), add(p, t, L / 2)], lambda i: 12, 9, vrep=1 / 80.0, col=ao)
    for _ in range(5):                                                        # pineapples
        p, n = surface((rnd.uniform(-1, 1), rnd.uniform(-0.3, 1), rnd.uniform(-1, 1)), 0.0)
        c = add(p, n, 8)
        blob(pine, c, (16, 22, 16), rings=10, segs=14, col=ao)
        for j in range(7):
            an = 2 * math.pi * j / 7
            dirv = nrm((math.cos(an) * 0.5, 1.0, math.sin(an) * 0.5))
            card(leaf, add(c, (0, 18, 0)), add(c, add((0, 18, 0), dirv, 30)), 9, 2, nrm(cross(dirv, (math.sin(an), 0, -math.cos(an)))), col=ao)
    for _ in range(9):                                                        # bushes sticking out
        p, n = surface((rnd.uniform(-1, 1), rnd.uniform(-0.2, 1), rnd.uniform(-1, 1)), 0.1)
        for j in range(5):
            dirv = nrm(add(n, (rnd.uniform(-0.6, 0.6), rnd.uniform(-0.3, 0.6), rnd.uniform(-0.6, 0.6))))
            side = nrm(cross(dirv, (0, 1, 0) if abs(dirv[1]) < 0.9 else (1, 0, 0)))
            card(leaf, p, add(p, dirv, rnd.uniform(50, 90)), rnd.uniform(40, 70), 20, side, nseg=2, col=ao)
    for _ in range(6):                                                        # plastic turf mesh, plastered on
        p, n = surface((rnd.uniform(-1, 1), rnd.uniform(-0.5, 1), rnd.uniform(-1, 1)), -0.02)
        t = nrm(cross(n, (0.3, 1, 0.2)))
        card(turf, add(p, t, -40), add(p, t, 40), 70, 60, nrm(cross(t, n)), col=ao)
    for _ in range(10):                                                       # mushrooms
        p, n = surface((rnd.uniform(-1, 1), rnd.uniform(-0.1, 1), rnd.uniform(-1, 1)), 0.0)
        tube(cap, [p, add(p, n, 14)], lambda i: 2.5, 6, col=ao)
        top = add(p, n, 14)
        blob(cap, top, (9, 4, 9), rings=6, segs=10, col=ao)
    for _ in range(12):                                                       # the red fluid it weeps
        p, n = surface((rnd.uniform(-1, 1), rnd.uniform(-0.8, 0.4), rnd.uniform(-1, 1)), -0.01)
        drip = [add(p, (0, -k * 9, 0)) for k in range(5)]
        drip = [add(q, n, 2 - k * 0.3) for k, q in enumerate(drip)]
        tube(fl, drip, lambda i: 3.0 * (1 - i / 6.0) + 0.8, 6, col=lambda p, n: (1, 1, 1))
    blob(fl, (rnd.uniform(-60, 60), 1, rnd.uniform(-60, 60)), (110, 2, 80), rings=4, segs=18)   # a puddle
    return M


# ============================================================================ SCP-3069-A replica
def scp3069a():
    save_prop(noise_tex(256, (130, 134, 138), 8, 0.6, 12), 's3069a_steel.png')
    save_prop(Image.new('RGB', (32, 32), (90, 255, 140)), 's3069a_glow.png')
    save_prop(noise_tex(128, (150, 90, 40), 10, 0.6, 13), 's3069a_coil.png')
    M = Model()
    steel = M.surf('steel', 's3069a_steel.png', shine=0.7)
    coil = M.surf('coil', 's3069a_coil.png', shine=0.6)
    glow = M.surf('glow', 's3069a_glow.png', fx=1)
    halo = M.surf('halo', 's3069a_glow.png', fx=1, alpha=0.25)
    lathe(steel, [(0, 0), (60, 0), (62, 6), (60, 12), (40, 14), (22, 30), (8, 34)], 32, lambda i: i / 3.0)
    for a in range(0, 360, 45):                                               # bolts round the base
        c = (50 * math.cos(math.radians(a)), 13, 50 * math.sin(math.radians(a)))
        blob(steel, c, (3, 2, 3), e=0.5, rings=4, segs=6)
    tube(steel, [(0, 30, 0), (0, 300, 0)], lambda i: 5.5, 16, vrep=1 / 60.0)
    for y in (60, 140, 220):
        lathe(steel, [(5.5, y - 4), (9, y - 2), (9, y + 2), (5.5, y + 4)], 16, lambda i: i)
    for y in (40, 52, 64):                                                    # field coils
        lathe(coil, [(14, y - 5), (20, y - 4), (21, y), (20, y + 4), (14, y + 5)], 24, lambda i: i / 2.0)
    lathe(steel, [(5.5, 296), (12, 300), (14, 306), (8, 310)], 16, lambda i: i)
    blob(glow, (0, 322, 0), (16, 16, 16), rings=14, segs=20)
    blob(halo, (0, 322, 0), (26, 26, 26), rings=12, segs=18)
    return M


# ============================================================================ SCP-4434-C skull
def skull():
    rnd = random.Random(4434)
    bone = noise_tex(256, (214, 204, 180), 10, 0.8, 14)
    d = ImageDraw.Draw(bone)
    for _ in range(60):
        x, y = rnd.randrange(256), rnd.randrange(256)
        d.line([(x, y), (x + rnd.randint(-20, 20), y + rnd.randint(-20, 20))], fill=(160, 150, 126), width=1)
    save_prop(bone, 's4434_bone.png')
    save_prop(noise_tex(64, (24, 18, 16), 6, 0.6, 15), 's4434_dark.png')
    save_prop(noise_tex(128, (120, 96, 70), 10, 0.6, 16), 's4434_antler.png')
    M = Model()
    b = M.surf('bone', 's4434_bone.png', shine=0.2)
    dk = M.surf('dark', 's4434_dark.png')
    an = M.surf('antler', 's4434_antler.png', shine=0.15)

    blob(b, (0, 13, -5), (7.5, 7.8, 9.5), rings=18, segs=24)                  # the cranium
    blob(b, (0, 11, 8), (4.6, 4.2, 12.5), rings=16, segs=20,                  # the long snout, tapering
         disp=lambda d: 1 - 0.35 * max(0.0, d[2]) ** 2)
    blob(b, (0, 7, 6), (4.4, 2.0, 14), rings=10, segs=18)                     # the lower jaw
    for e in (-1, 1):
        tube(b, [(e * 6.8, 11, -6), (e * 7.4, 10.5, -1), (e * 5.6, 9.5, 5)], lambda i: 1.3, 8)   # cheekbones
        tube(b, [(e * 2.0, 18.5, -9), (e * 5.5, 17.2, -3), (e * 4.8, 15.5, 1)], lambda i: 1.1, 8)  # brow ridges
        blob(dk, (e * 5.8, 14.2, -1.5), (2.1, 2.3, 2.6), rings=8, segs=10)    # eye sockets
        blob(dk, (e * 1.3, 12.6, 19.2), (0.8, 1.1, 1.2), rings=6, segs=8)     # nostrils
    blob(dk, (0, 9.2, 14), (2.6, 0.8, 9), rings=6, segs=10)                    # the gap between the jaws
    for row, y in ((1, 9.6), (-1, 9.0)):                                      # teeth: a predator's
        for k in range(9):
            z = 4 + k * 1.75
            for e in (-1, 1):
                x = e * (3.2 - k * 0.18)
                L = 2.4 if k in (0, 1) else 1.3
                tube(b, [(x, y, z), (x, y - row * L, z + 0.3)], lambda i: (0.55, 0.05)[i], 5)
    def antler(base, dirv, L, depth):
        pts = [add(base, dirv, L * t) for t in (0, 0.33, 0.66, 1)]
        pts = [add(p, (0, 3 * math.sin(t * 2), 0)) for t, p in enumerate(pts)]
        tube(an, pts, lambda i: max(0.4, 1.6 * (1 - i / 4.0) * (0.75 ** (3 - depth))), 7, vrep=0.1)
        if depth > 0:
            for t in (0.4, 0.75):
                p = add(base, dirv, L * t)
                nd = nrm(add(dirv, (rnd.uniform(-0.8, 0.8), rnd.uniform(0.3, 0.9), rnd.uniform(-0.6, 0.6))))
                antler(p, nd, L * 0.55, depth - 1)
    for e in (-1, 1):
        antler((e * 3.5, 19.5, -8), nrm((e * 0.7, 1.0, -0.5)), 26, 3)
    return M


if __name__ == '__main__':
    out = {}
    for name, fn, folder in (('thermal4427', thermal, ITEMS), ('phone4433', phone, ITEMS), ('card2758', idcard, ITEMS),
                             ('jar3069', jar, ITEMS), ('scp2648', scp2648, PROPS), ('scp3069a', scp3069a, PROPS),
                             ('scp4434c', skull, PROPS)):
        m = fn()
        m.write(os.path.join(folder, name + '.b3d'))
        out[name] = (m, folder)
        print('%-12s %6d triangles' % (name, m.tris()))
    spec = Model()                                   # the tank's specimen: the jar's creature at full size
    jm = out['jar3069'][0]
    for nm in ('skin', 'glow', 'fins'):
        s0 = jm.S[nm]
        s1 = spec.surf(nm, s0.tex, fx=s0.fx, shine=s0.shine, alpha=s0.alpha, tint=s0.tint, masked=s0.masked)
        s1.V = [(v[0] * 28, (v[1] - 7.5) * 28, v[2] * 28) + tuple(v[3:]) for v in s0.V]
        s1.T = list(s0.T)
    spec.write(os.path.join(PROPS, 'scp3069spec.b3d'))
    for f in ('j3069_skin.png', 'j3069_glow.png'):
        Image.open(os.path.join(ITEMS, f)).save(os.path.join(PROPS, f))
    views = {'thermal4427': ((-18, 20, -22), (0, 11, 2)), 'phone4433': ((10, 14, -16), (0, 2, 0)),
             'card2758': ((0, 13, -5), (0, 0, 0.5)), 'jar3069': ((14, 14, -20), (0, 8, 0)),
             'scp2648': ((380, 300, -620), (0, 170, 0)), 'scp3069a': ((160, 260, -420), (0, 170, 0)),
             'scp4434c': ((-38, 26, 22), (0, 15, 2))}
    tiles = []
    for name, (m, folder) in out.items():
        eye, look = views[name]
        tiles.append(render(m, folder, eye, look, size=(400, 400), fov=45, bg=(30, 30, 34)))
    sheet = Image.new('RGB', (1600, 800), (0, 0, 0))
    for i, t in enumerate(tiles):
        sheet.paste(t, ((i % 4) * 400, (i // 4) * 400))
    sheet.save(os.path.join(PREV, 'hd30_models.png'))
    for name in ('thermal4427', 'phone4433', 'card2758', 'jar3069'):
        m, folder = out[name]
        eye, look = views[name]
        render(m, folder, eye, look, size=(256, 256), fov=45, bg=(0, 0, 0)).resize((64, 64), Image.LANCZOS).save(
            os.path.join(ITEMS, 'INV%s.png' % name))
    print('previews and icons written')
