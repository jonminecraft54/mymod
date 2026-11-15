r"""High-detail models for batch 29 (original work after scp-wiki.wikidot.com/scp-820-jp and /scp-867, CC BY-SA 3.0):

  GFX\items\scp820jp.b3d   SCP-820-JP: a knapped flint blade (every flake scar a real facet, a sharp lens-shaped
                           edge), a turquoise-mosaic grip between hammered gold bands with a step-fret pommel, and a
                           feathered serpent that coils up out of the pommel, round the grip and the blade, its
                           head resting near the tip - scaled body, gold eyes, forked tongue, a crest of feathers.
                           About 13 000 triangles, five 1024 textures (scp820_*.png).
  GFX\map\props\scp867.b3d SCP-867: a blood-red spruce about 3.6 m tall - a tapering, slightly crooked trunk with
                           root flare, sixteen whorls of drooping branches, every branch carrying crossed needle
                           fronds (masked, two-sided), a dense inner crown, light and ambient occlusion baked into
                           the vertex colours. About 10 000 triangles, textures scp867_*.png.
  GFX\items\INVscp820jp.png  rendered from the model.
  Tools\roomkit\previews\hd29_*.png   preview renders (software rasteriser below).
   python make_hd29.py"""
import math
import os
import random
import struct
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = r'I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9'
ITEMS = os.path.join(ROOT, 'GFX', 'items')
PROPS = os.path.join(ROOT, 'GFX', 'map', 'props')
PREV = os.path.join(ROOT, 'Tools', 'roomkit', 'previews')


# ============================================================================ mesh with surfaces
class Surf:
    def __init__(self, tex, fx=0, shine=0.0, masked=False, alpha=1.0, tint=(1, 1, 1)):
        self.tex, self.fx, self.shine, self.masked, self.alpha, self.tint = tex, fx, shine, masked, alpha, tint
        self.V = []   # x y z nx ny nz r g b u v
        self.T = []


class Model:
    def __init__(self):
        self.S = {}

    def surf(self, name, tex, **kw):
        if name not in self.S:
            self.S[name] = Surf(tex, **kw)
        return self.S[name]

    def tris(self):
        return sum(len(s.T) for s in self.S.values())

    def write(self, path):
        chunk = lambda tag, body: tag + struct.pack('<i', len(body)) + body
        cstr = lambda s: s.encode('latin-1') + b'\0'
        names = list(self.S)
        texs = b''
        for n in names:
            s = self.S[n]
            texs += cstr(s.tex) + struct.pack('<2i5f', 1 + (4 if s.masked else 0) + 8, 2, 0, 0, 1, 1, 0)
        brus = struct.pack('<i', 1)
        for i, n in enumerate(names):
            s = self.S[n]
            brus += cstr(n) + struct.pack('<5f2i', s.tint[0], s.tint[1], s.tint[2], s.alpha, s.shine, 1, s.fx) + struct.pack('<i', i)
        V, tb = [], b''
        for i, n in enumerate(names):
            s = self.S[n]
            base = len(V)
            V += s.V
            tb += chunk(b'TRIS', struct.pack('<i', i) + b''.join(struct.pack('<3i', a + base, b + base, c + base) for a, b, c in s.T))
        vb = struct.pack('<3i', 3, 1, 2) + b''.join(
            struct.pack('<12f', v[0], v[1], v[2], v[3], v[4], v[5], v[6], v[7], v[8], 1.0, v[9], v[10]) for v in V)
        msh = chunk(b'MESH', struct.pack('<i', -1) + chunk(b'VRTS', vb) + tb)
        node = chunk(b'NODE', cstr('m') + struct.pack('<10f', 0, 0, 0, 1, 1, 1, 1, 0, 0, 0) + msh)
        open(path, 'wb').write(chunk(b'BB3D', struct.pack('<i', 1) + chunk(b'TEXS', texs) + chunk(b'BRUS', brus) + node))


def nrm(v):
    l = math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2]) or 1.0
    return (v[0] / l, v[1] / l, v[2] / l)


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def add(a, b, k=1.0):
    return (a[0] + b[0] * k, a[1] + b[1] * k, a[2] + b[2] * k)


def grid(s, P, nu, nv, uv, col=None, flat=False, wrap_v=False):
    """a surface from P(i, j) -> point on an (nu+1) x (nv+1) grid; outward = (dP/du x dP/dv). smooth normals
    unless flat (faceted: every triangle its own vertices)"""
    pts = [[P(i, j) for j in range(nv + 1)] for i in range(nu + 1)]
    if flat:
        for i in range(nu):
            for j in range(nv):
                q = [(i, j), (i + 1, j), (i + 1, j + 1), (i, j + 1)]
                for tri in ((q[0], q[1], q[2]), (q[0], q[2], q[3])):
                    a, b, c = [pts[x][y] for x, y in tri]
                    n = nrm(cross(sub(b, a), sub(c, a)))
                    base = len(s.V)
                    for (x, y), p in zip(tri, (a, b, c)):
                        cc = col(p, n) if col else (1, 1, 1)
                        u, v = uv(x, y)
                        s.V.append((p[0], p[1], p[2], n[0], n[1], n[2], cc[0], cc[1], cc[2], u, v))
                    s.T.append((base, base + 1, base + 2))
        return
    base = len(s.V)
    for i in range(nu + 1):
        for j in range(nv + 1):
            p = pts[i][j]
            du = sub(pts[min(i + 1, nu)][j], pts[max(i - 1, 0)][j])
            jp, jm = (j + 1, j - 1)
            if wrap_v:
                jp, jm = (j + 1) % nv if j + 1 <= nv else 1, (j - 1) % nv
            else:
                jp, jm = min(j + 1, nv), max(j - 1, 0)
            dv = sub(pts[i][jp], pts[i][jm])
            n = nrm(cross(du, dv))
            cc = col(p, n) if col else (1, 1, 1)
            u, v = uv(i, j)
            s.V.append((p[0], p[1], p[2], n[0], n[1], n[2], cc[0], cc[1], cc[2], u, v))
    for i in range(nu):
        for j in range(nv):
            a = base + i * (nv + 1) + j
            b = a + nv + 1
            s.T.append((a, b, b + 1))
            s.T.append((a, b + 1, a + 1))


def frames(path):
    """parallel-transport frames along a polyline: [(p, t, n, b)]"""
    out = []
    t0 = nrm(sub(path[1], path[0]))
    ref = (0, 0, 1) if abs(t0[2]) < 0.9 else (1, 0, 0)
    n = nrm(cross(t0, ref))
    for i, p in enumerate(path):
        a = path[max(i - 1, 0)]
        c = path[min(i + 1, len(path) - 1)]
        t = nrm(sub(c, a))
        n = nrm(sub(n, tuple(t[k] * sum(n[m] * t[m] for m in range(3)) for k in range(3))))
        b = cross(t, n)
        out.append((p, t, n, b))
    return out


def tube(s, path, radius, sides, vrep=1.0, col=None, flat_scale=None):
    """a tube along a path; radius(i) -> r (or (rx, ry) for an elliptic section); UV u round, v along"""
    F = frames(path)
    L = [0.0]
    for i in range(1, len(path)):
        L.append(L[-1] + math.sqrt(sum((path[i][k] - path[i - 1][k]) ** 2 for k in range(3))))

    def P(i, j):
        p, t, n, b = F[i]
        r = radius(i)
        rx, ry = (r, r) if not isinstance(r, tuple) else r
        a = 2 * math.pi * j / sides
        return add(add(p, n, rx * math.cos(a)), b, -ry * math.sin(a))
    grid(s, lambda i, j: P(i, j), len(path) - 1, sides, lambda i, j: (j / sides, L[i] * vrep), col=col)


def lathe(s, prof, segs, uvv, y0=0.0, col=None, cx=0.0, cz=0.0):
    """revolve [(r, y)] round the y axis (bottom to top)"""
    def P(i, j):
        r, y = prof[i]
        a = 2 * math.pi * j / segs
        return (cx + r * math.cos(a), y0 + y, cz + r * math.sin(a))
    grid(s, P, len(prof) - 1, segs, lambda i, j: (j / segs, uvv(i)), col=col)


def card(s, p0, p1, w0, w1, side, nseg=1, col=None, uvx=(0, 1)):
    """a flat two-sided strip (needle frond) from p0 to p1, widths w0..w1, spread along `side`"""
    base = len(s.V)
    up = nrm(cross(nrm(sub(p1, p0)), side))
    for k in range(nseg + 1):
        f = k / nseg
        c = add(p0, sub(p1, p0), f)
        w = w0 + (w1 - w0) * f
        for e in (-1, 1):
            q = add(c, side, e * w / 2)
            cc = col(q, up) if col else (1, 1, 1)
            s.V.append((q[0], q[1], q[2], up[0], up[1], up[2], cc[0], cc[1], cc[2], uvx[0] + (uvx[1] - uvx[0]) * (e + 1) / 2, 1 - f))
    for k in range(nseg):
        a = base + k * 2
        s.T.append((a, a + 2, a + 3))
        s.T.append((a, a + 3, a + 1))


# ============================================================================ textures
def tex_save(im, path):
    im.save(path)


def flint_tex():
    rnd = random.Random(8201)
    S = 1024
    a = np.zeros((S, S, 3), np.float32)
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    base = np.array([58, 52, 50], np.float32)
    a[:] = base
    # conchoidal ripples round many flake centres, with pale scar rims
    for _ in range(70):
        cx, cy, r = rnd.uniform(0, S), rnd.uniform(0, S), rnd.uniform(60, 220)
        d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
        m = d < r
        ripple = 0.5 + 0.5 * np.sin(d / rnd.uniform(5, 11))
        shade = rnd.uniform(-14, 22)
        a[m] += (shade + ripple[m, None] * 8 - (d[m, None] / r) * 10)
        rim = (np.abs(d - r) < 1.6)
        a[rim] += 12
    noise = np.random.default_rng(820).normal(0, 6, (S, S, 1)).astype(np.float32)
    a += noise
    # speckles of chalky inclusions
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    for _ in range(900):
        x, y = rnd.randrange(S), rnd.randrange(S)
        c = rnd.randint(90, 140)
        d.point((x, y), fill=(c, c - 8, c - 12))
    return im.filter(ImageFilter.GaussianBlur(0.7))


def mosaic_tex():
    """turquoise mosaic: irregular tesserae (voronoi), dark grout, some red shell and jet"""
    rnd = random.Random(8202)
    S = 512
    pts = np.array([(rnd.uniform(0, S), rnd.uniform(0, S)) for _ in range(900)], np.float32)
    cols = []
    for _ in range(len(pts)):
        k = rnd.random()
        if k < 0.68:
            c = (40 + rnd.randint(-15, 25), 160 + rnd.randint(-30, 30), 150 + rnd.randint(-30, 30))
        elif k < 0.84:
            c = (20, 110 + rnd.randint(-20, 20), 130 + rnd.randint(-20, 20))
        elif k < 0.93:
            c = (190 + rnd.randint(-20, 20), 60, 45)
        else:
            c = (22, 22, 26)
        cols.append(c)
    cols = np.array(cols, np.float32)
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    best = np.full((S, S), 1e9, np.float32)
    second = np.full((S, S), 1e9, np.float32)
    idx = np.zeros((S, S), np.int32)
    for i, (px, py) in enumerate(pts):
        # tile: wrap distances so the texture repeats
        dx = np.abs(xx - px)
        dy = np.abs(yy - py)
        dx = np.minimum(dx, S - dx)
        dy = np.minimum(dy, S - dy)
        d = dx * dx + dy * dy
        m = d < best
        second = np.where(m, best, np.minimum(second, d))
        idx = np.where(m, i, idx)
        best = np.where(m, d, best)
    a = cols[idx]
    edge = np.sqrt(second) - np.sqrt(best)
    grout = np.clip(edge / 2.5, 0, 1)[..., None]
    a = a * (0.55 + 0.45 * grout) + np.array([30, 26, 20], np.float32) * (1 - grout)
    a += np.random.default_rng(1).normal(0, 5, (S, S, 1))
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def gold_tex():
    rnd = random.Random(8203)
    S = 512
    im = Image.new('RGB', (S, S), (196, 150, 58))
    d = ImageDraw.Draw(im)
    for _ in range(1400):                       # hammer marks
        x, y, r = rnd.randrange(S), rnd.randrange(S), rnd.randint(4, 12)
        c = rnd.randint(-30, 40)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(196 + c, 150 + c, 58 + c // 2))
    im = im.filter(ImageFilter.GaussianBlur(1.5))
    d = ImageDraw.Draw(im)
    step = 64                                    # an engraved step-fret (xicalcoliuhqui) band
    for x0 in range(0, S, step):
        pts = [(x0, 300), (x0, 200), (x0 + 40, 200), (x0 + 40, 240), (x0 + 20, 240), (x0 + 20, 260),
               (x0 + 52, 260), (x0 + 52, 180), (x0 + 64, 180)]
        d.line(pts, fill=(110, 76, 24), width=6)
    d.line([(0, 170), (S, 170)], fill=(110, 76, 24), width=5)
    d.line([(0, 312), (S, 312)], fill=(110, 76, 24), width=5)
    return im


def scales_tex():
    """the serpent's skin: u = round the body (0 / 1 = belly, 0.5 = back), v = along it (tiles)"""
    rnd = random.Random(8204)
    W, H = 512, 512
    im = Image.new('RGB', (W, H), (40, 120, 80))
    d = ImageDraw.Draw(im)
    rows, cols = 32, 24
    for r in range(rows + 1):
        for c in range(cols + 1):
            x = (c + (0.5 if r % 2 else 0)) * W / cols
            y = r * H / rows
            back = 1 - abs((x / W) - 0.5) * 2               # 1 on the back, 0 on the belly
            g = (int(30 + 30 * (1 - back) ** 4), int(115 + 55 * back), int(72 + 40 * back))
            if back < 0.08:
                g = (214, 196, 120)                           # the pale belly plates
            j = rnd.randint(-12, 12)
            g = tuple(max(0, min(255, v + j)) for v in g)
            d.ellipse([x - W / cols * 0.62, y - H / rows * 0.2, x + W / cols * 0.62, y + H / rows * 1.05],
                      fill=g, outline=(20, 60, 40))
    # dark diamonds down the back and a turquoise feather-serpent band
    for y in range(0, H, 64):
        d.polygon([(W / 2, y), (W / 2 + 40, y + 32), (W / 2, y + 64), (W / 2 - 40, y + 32)], outline=(10, 30, 22), fill=None)
        d.polygon([(W / 2, y + 14), (W / 2 + 18, y + 32), (W / 2, y + 50), (W / 2 - 18, y + 32)], fill=(20, 60, 50))
    for x in (W * 0.3, W * 0.7):
        d.line([(x, 0), (x, H)], fill=(60, 190, 180), width=3)
    return im.filter(ImageFilter.GaussianBlur(0.6))


def feather_tex():
    im = Image.new('RGB', (256, 256), (0, 0, 0))
    d = ImageDraw.Draw(im)
    for k, col in enumerate(((40, 170, 90), (60, 200, 190), (210, 60, 40))):
        x0 = 20 + k * 80
        d.polygon([(x0 + 30, 250), (x0, 140), (x0 + 30, 6), (x0 + 60, 140)], fill=col)
        d.line([(x0 + 30, 250), (x0 + 30, 10)], fill=(240, 230, 160), width=3)
        for y in range(30, 240, 10):
            d.line([(x0 + 30, y), (x0 + 6, y - 16)], fill=tuple(max(1, c - 30) for c in col), width=1)
            d.line([(x0 + 30, y), (x0 + 54, y - 16)], fill=tuple(max(1, c - 30) for c in col), width=1)
    return im


# ============================================================================ SCP-820-JP
def knife():
    M = Model()
    blade = M.surf('flint', 'scp820_flint.png', shine=0.55)
    grip = M.surf('mosaic', 'scp820_mosaic.png', shine=0.35)
    gold = M.surf('gold', 'scp820_gold.png', shine=0.8)
    skin = M.surf('scales', 'scp820_scales.png', shine=0.45)
    feath = M.surf('feather', 'scp820_feather.png', fx=16, masked=True)
    rnd = random.Random(820)
    # --- the handle: pommel (gold, stepped), grip (mosaic, waisted), band (gold)
    lathe(gold, [(0.0, -1.2), (1.3, -1.2), (1.9, -0.9), (2.1, -0.4), (1.7, -0.2), (1.9, 0.2), (2.2, 0.5), (1.5, 0.9),
                 (1.35, 1.2)], 32, lambda i: i / 8.0)
    prof = [(1.35 + 0.18 * math.sin(math.pi * k / 10) ** 2 - 0.12 * math.sin(math.pi * k / 5) ** 4, 1.2 + k * 0.78) for k in range(11)]
    lathe(grip, prof, 32, lambda i: i / 3.0)
    lathe(gold, [(1.45, 9.0), (1.9, 9.1), (2.0, 9.6), (1.95, 10.1), (1.4, 10.3), (0.9, 10.4)], 32, lambda i: i / 5.0)
    # --- the blade: a leaf-shaped lens 20 long, knapped
    L, y0 = 20.0, 10.0
    W = lambda u: 3.5 * (u ** 0.55) * ((1 - u) ** 0.8) / (0.42 ** 0.55 * 0.58 ** 0.8) * (1 + 0.025 * math.sin(u * 70))
    Tk = lambda u: 0.85 * ((1 - u) ** 0.6) * min(1.0, u * 8 + 0.35)
    scars = []
    for side in (1, -1):
        for _ in range(55):
            scars.append((side, rnd.uniform(0.04, 0.97), rnd.choice((-1, 1)) * rnd.uniform(0.55, 1.05),
                          rnd.uniform(0.05, 0.14), rnd.uniform(0.25, 0.45), rnd.uniform(0.18, 0.4)))
    nu, nv = 56, 22

    def bp(i, j, side):
        u = 0.004 + 0.992 * i / nu
        v = -1 + 2 * j / nv
        w, t = W(u), Tk(u)
        z = t * (1 - v * v) ** 0.85
        for sd, su, sv, ru, rv, dep in scars:
            if sd != side:
                continue
            du, dv = (u - su) / ru, (v - sv) / rv
            q = du * du + dv * dv
            if q < 1:
                z -= dep * t * (1 - q) ** 1.5
        z = max(z, t * 0.06 * (1 - v * v))
        return (w * v, y0 + u * L, side * z)
    grid(blade, lambda i, j: bp(i, nv - j, 1), nu, nv, lambda i, j: (0.15 + 0.7 * (nv - j) / nv, i / nu * 1.6), flat=True)
    grid(blade, lambda i, j: bp(i, j, -1), nu, nv, lambda i, j: (0.15 + 0.7 * j / nv, i / nu * 1.6 + 0.3), flat=True)
    # --- the serpent: out of the pommel, two turns round the grip, a turn and a half up the blade
    path = []
    N = 230
    for k in range(N):
        f = k / (N - 1)
        if f < 0.42:
            g = f / 0.42
            a = g * 2 * math.pi * 2.2
            y = 0.3 + g * 9.2
            r = 1.75 + 0.15 * math.sin(math.pi * k / 10) ** 2 if y < 9 else 2.25
            path.append((r * math.cos(a), y, r * math.sin(a)))
        else:
            g = (f - 0.42) / 0.58
            a = 2 * math.pi * 2.2 + g * 2 * math.pi * 1.45
            u = 0.02 + g * 0.8
            w, t = W(u), Tk(u)
            ca, sa = math.cos(a), math.sin(a)
            path.append(((w + 0.42) * ca, y0 + u * L, (t * (1 - ca * ca) + 0.5) * sa))
    rad = lambda i: (0.18 + 0.42 * min(1.0, i / 25.0)) * (1.0 if i < N - 22 else 0.92)
    tube(skin, path, rad, 14, vrep=0.38)
    # the head: a wedge-shaped skull along the last direction, jaw, eyes, tongue, a crest of feathers
    p, t = path[-1], nrm(sub(path[-1], path[-6]))
    side = nrm(cross(t, (0, 0, 1) if abs(t[2]) < 0.9 else (1, 0, 0)))
    upv = nrm(cross(side, t))

    def head(i, j):
        th = math.pi * i / 16
        ph = -2 * math.pi * j / 20
        x, y, z = math.sin(th) * math.cos(ph), math.cos(th), math.sin(th) * math.sin(ph)
        along = y * 1.5 + 0.9                                # length
        taper = 1 - 0.45 * max(0.0, y)                      # narrower to the snout
        wide = 0.78 * taper * (1.12 if z < 0 else 1.0)
        tall = 0.55 * taper * (0.8 if z < 0 else 1.0)
        q = add(p, t, along)
        return add(add(q, side, x * wide), upv, z * tall)
    grid(skin, head, 16, 20, lambda i, j: (j / 20, i / 16 * 0.6))
    hp = add(p, t, 0.9)
    for e in (-1, 1):
        ep = add(add(add(hp, t, 0.85), side, e * 0.52), upv, 0.22)
        lathe(gold, [(0.0, -0.17), (0.16, -0.12), (0.2, 0.0), (0.16, 0.12), (0.0, 0.17)], 10, lambda i: 0.5, cx=ep[0], cz=ep[2], y0=ep[1])
    tip = add(hp, t, 2.45)
    for e in (-1, 1):                                          # the forked tongue
        a = add(tip, t, 0.9)
        b = add(add(a, t, 0.45), side, e * 0.25)
        card(feath, tip, a, 0.07, 0.06, side, uvx=(0.66, 0.70))
        card(feath, a, b, 0.06, 0.02, side, uvx=(0.66, 0.70))
    for k in range(7):                                         # the crest of feathers
        ang = (k - 3) * 0.33
        base = add(add(hp, t, -0.2), upv, 0.35)
        dirv = nrm(add(add(t, (0, 0, 0), 0), add(upv, side, math.sin(ang)), 1.4))
        dirv = nrm(add(tuple(-x for x in t), add(upv, side, math.sin(ang) * 1.3), 1.6))
        sv = nrm(cross(dirv, upv)) if abs(sum(dirv[i] * upv[i] for i in range(3))) < 0.99 else side
        u0 = (k % 3) / 3.0
        card(feath, base, add(base, dirv, 2.1 + 0.3 * math.cos(ang * 2)), 0.25, 0.75, sv, nseg=3, uvx=(u0, u0 + 0.33))
    return M


# ============================================================================ SCP-867
def needle_card_tex():
    """a branchlet frond on black (masked): a twig up the middle, red needles both ways, tips paler"""
    rnd = random.Random(8671)
    W, H = 512, 512
    im = Image.new('RGB', (W, H), (0, 0, 0))
    d = ImageDraw.Draw(im)
    # side twigs first, then a dense coat of needles on the main twig and on every side twig
    twigs = [((W / 2, H), (W / 2, 0), 230)]
    for k in range(9):
        y = H - 30 - k * 54
        for e in (-1, 1):
            reach = (W / 2 - 20) * (0.55 + 0.45 * (y / H))
            twigs.append(((W / 2, y), (W / 2 + e * reach, y - 120), 110))
    for (x0, y0), (x1, y1), nl in twigs:
        d.line([(x0, y0), (x1, y1)], fill=(84, 34, 24), width=4)
    for (x0, y0), (x1, y1), nl in twigs:
        L = math.hypot(x1 - x0, y1 - y0)
        tx, ty = (x1 - x0) / L, (y1 - y0) / L
        for s in range(0, int(L), 3):
            f = 1 - s / L
            px, py = x0 + tx * s, y0 + ty * s
            for e in (-1, 1):
                ln = (16 + nl * 0.42 * f) * rnd.uniform(0.7, 1.0)
                ang = math.radians(rnd.uniform(35, 62))
                # rotate the twig direction by +-ang
                ca, sa = math.cos(e * ang), math.sin(e * ang)
                dx, dy = tx * ca - ty * sa, tx * sa + ty * ca
                base = rnd.randint(120, 215)
                col = (base, rnd.randint(10, 32), rnd.randint(16, 34))
                d.line([(px, py), (px + dx * ln, py + dy * ln)], fill=col, width=3)
                d.point((px + dx * ln, py + dy * ln), fill=(min(255, base + 40), 110, 110))
    return im


def bark_tex():
    rnd = random.Random(8672)
    S = 512
    a = np.zeros((S, S, 3), np.float32)
    a[:] = (82, 34, 28)
    xs = np.arange(S, dtype=np.float32)
    for _ in range(46):                                      # vertical fissures, wandering
        x0 = rnd.uniform(0, S)
        amp = rnd.uniform(3, 12)
        ph = rnd.uniform(0, 6)
        for y in range(S):
            x = int(x0 + amp * math.sin(y / 40 + ph)) % S
            w = rnd.randint(2, 4)
            a[y, max(0, x - w):x + w] *= 0.45
    a += np.random.default_rng(3).normal(0, 9, (S, S, 1))
    for _ in range(300):                                     # flakes of scale bark
        x, y = rnd.randrange(S), rnd.randrange(S)
        a[y:y + rnd.randint(4, 14), x:x + rnd.randint(8, 22)] += rnd.uniform(6, 22)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))


def crown_tex():
    """the opaque inner crown: densely packed red needles, darker"""
    rnd = random.Random(8673)
    S = 512
    im = Image.new('RGB', (S, S), (60, 10, 14))
    d = ImageDraw.Draw(im)
    for _ in range(9000):
        x, y = rnd.randrange(S), rnd.randrange(S)
        ln = rnd.randint(8, 22)
        ang = rnd.uniform(0, math.pi)
        c = rnd.randint(80, 160)
        d.line([(x, y), (x + ln * math.cos(ang), y + ln * math.sin(ang))], fill=(c, rnd.randint(6, 22), rnd.randint(10, 26)), width=2)
    return im


def spruce(seed=867, H=370.0):
    rnd = random.Random(seed)
    M = Model()
    bark = M.surf('bark', 'scp867_bark.png', fx=1 + 2)
    crown = M.surf('crown', 'scp867_crown.png', fx=1 + 2)
    fr = M.surf('fronds', 'scp867_frond.png', fx=1 + 2 + 16, masked=True)
    top_light = (0.35, 1.0, 0.25)

    def shade(p, n, base=1.0, reach=1.0):
        h = max(0.0, min(1.0, p[1] / H))
        dl = max(0.0, n[0] * top_light[0] + n[1] * top_light[1] + n[2] * top_light[2]) / 1.12
        ao = 0.42 + 0.58 * min(1.0, reach) * (0.55 + 0.45 * h)
        k = base * ao * (0.62 + 0.38 * dl)
        return (min(1, k * 1.06), min(1, k), min(1, k))
    # trunk: crooked, tapering, root flare
    lean = [(rnd.uniform(-3, 3), rnd.uniform(-3, 3)) for _ in range(6)]
    trunk = []
    for k in range(31):
        f = k / 30
        o = lean[min(5, int(f * 5))]
        trunk.append((o[0] * f * 2, f * H, o[1] * f * 2))
    tube(bark, trunk, lambda i: max(1.5, 17 * (1 - i / 30) ** 1.1 + (10 * (1 - i / 4) if i < 4 else 0)), 12, vrep=1 / 160.0,
         col=lambda p, n: shade(p, n, 0.9, 0.5))
    for k in range(5):                                        # root buttresses
        a = 2 * math.pi * k / 5 + rnd.uniform(-0.3, 0.3)
        tube(bark, [(math.cos(a) * 6, 14, math.sin(a) * 6), (math.cos(a) * 22, 3, math.sin(a) * 22), (math.cos(a) * 34, -2, math.sin(a) * 34)],
             lambda i: (6, 4, 2)[i], 6, vrep=1 / 120.0, col=lambda p, n: shade(p, n, 0.7, 0.4))
    # the inner crown: stacked opaque cones
    tiers = 16
    for k in range(5):
        yb, yt = H * (0.14 + 0.16 * k), H * (0.34 + 0.16 * k)
        rb = 70 * (1 - k / 5.3) ** 1.05
        prof = [(rb * 0.6, 0), (rb, (yt - yb) * 0.25), (rb * 0.55, (yt - yb) * 0.7), (1.0, yt - yb)]
        lathe(crown, prof, 18, lambda i: i / 1.5, y0=yb, col=lambda p, n: shade(p, n, 0.75, 0.4))
    # branch whorls
    for k in range(tiers):
        f = k / (tiers - 1)
        y = H * (0.12 + 0.82 * f)
        Lb = 150 * (1 - f) ** 0.95 + 18
        nb = rnd.randint(6, 8) if f < 0.8 else 5
        a0 = rnd.uniform(0, 2 * math.pi)
        tr = trunk[min(30, int(y / H * 30))]
        for b in range(nb):
            a = a0 + 2 * math.pi * b / nb + rnd.uniform(-0.25, 0.25)
            dx, dz = math.cos(a), math.sin(a)
            L = Lb * rnd.uniform(0.85, 1.12)
            droop = rnd.uniform(0.18, 0.32)
            pts = []
            for s in range(7):
                g = s / 6
                yy = y - L * droop * math.sin(math.pi * g * 0.8) + L * 0.12 * g ** 3
                pts.append((tr[0] + dx * L * g, yy, tr[2] + dz * L * g))
            tube(bark, pts, lambda i: 1.8 * (1 - i / 7) + 0.4, 5, vrep=1 / 100.0, col=lambda p, n: shade(p, n, 0.6, 0.5))
            sidev = (-dz, 0, dx)
            for s in range(6):
                p0, p1 = pts[s], pts[s + 1]
                g = s / 6
                wd = L * (0.85 - 0.55 * g)
                c = lambda q, n, g=g: shade(q, (0, 1, 0), 1.0, 0.45 + 0.6 * g)
                card(fr, p0, add(p1, sub(p1, p0), 0.25), wd, wd * 0.8, sidev, col=c)                 # flat spray
                tilt = nrm(add(sidev, (0, -1.1, 0), 1))
                card(fr, p0, add(p1, sub(p1, p0), 0.25), wd * 0.6, wd * 0.45, tilt, col=c)           # hanging fringe
                tilt2 = nrm(add(tuple(-x for x in sidev), (0, -1.1, 0), 1))
                card(fr, p0, add(p1, sub(p1, p0), 0.25), wd * 0.6, wd * 0.45, tilt2, col=c)
    # the leader: a spire of fronds at the top
    top = trunk[-1]
    for k in range(5):
        a = 2 * math.pi * k / 5
        card(fr, add(top, (0, -40, 0)), add(top, (0, 22, 0)), 26, 4, (math.cos(a), 0, math.sin(a)),
             col=lambda q, n: shade(q, (0, 1, 0), 1.0, 1.0))
    return M


# ============================================================================ a small software renderer (previews, icons)
def render(M, texdir, eye, look, size=(640, 640), fov=40.0, bg=(18, 18, 22), light=True):
    W, H = size
    img = np.zeros((H, W, 3), np.float32)
    img[:] = bg
    zb = np.full((H, W), 1e9, np.float32)
    f = nrm(sub(look, eye))
    r = nrm(cross((0, 1, 0), f))                           # left-handed like Blitz: looking +z, +x is right
    u = cross(f, r)
    fl = 0.5 * H / math.tan(math.radians(fov) / 2)
    texc = {}
    for s in sorted(M.S.values(), key=lambda q: q.alpha < 1):
        if s.tex not in texc:
            texc[s.tex] = np.asarray(Image.open(os.path.join(texdir, s.tex)).convert('RGB'), np.float32)
        T = texc[s.tex]
        th, tw = T.shape[:2]
        V = np.array(s.V, np.float32)
        if len(V) == 0:
            continue
        P = V[:, :3] - np.array(eye, np.float32)
        cx = P @ np.array(r, np.float32)
        cy = P @ np.array(u, np.float32)
        cz = P @ np.array(f, np.float32)
        sx = W / 2 + cx / np.maximum(cz, 0.01) * fl
        sy = H / 2 - cy / np.maximum(cz, 0.01) * fl
        N = V[:, 3:6]
        ld = nrm((0.4, 0.8, -0.45))
        lam = np.clip(N @ np.array(ld, np.float32), 0, 1)
        lam2 = np.abs(N @ np.array(ld, np.float32))
        for a, b, c in s.T:
            if cz[a] < 0.1 or cz[b] < 0.1 or cz[c] < 0.1:
                continue
            x0, x1 = int(max(0, min(sx[a], sx[b], sx[c]))), int(min(W - 1, max(sx[a], sx[b], sx[c]) + 1))
            y0, y1 = int(max(0, min(sy[a], sy[b], sy[c]))), int(min(H - 1, max(sy[a], sy[b], sy[c]) + 1))
            if x1 < x0 or y1 < y0:
                continue
            ar = (sx[b] - sx[a]) * (sy[c] - sy[a]) - (sx[c] - sx[a]) * (sy[b] - sy[a])
            if abs(ar) < 1e-6:
                continue
            if not (s.fx & 16):
                e1 = V[b, :3] - V[a, :3]
                e2 = V[c, :3] - V[a, :3]
                if float(np.dot(np.cross(e1, e2), P[a])) > 0:
                    continue                                   # back face (Blitz: front = outward cross)
            gy, gx = np.mgrid[y0:y1 + 1, x0:x1 + 1].astype(np.float32) + 0.5
            w0 = ((sx[b] - gx) * (sy[c] - gy) - (sx[c] - gx) * (sy[b] - gy)) / ar
            w1 = ((sx[c] - gx) * (sy[a] - gy) - (sx[a] - gx) * (sy[c] - gy)) / ar
            w2 = 1 - w0 - w1
            m = (w0 >= 0) & (w1 >= 0) & (w2 >= 0)
            if not m.any():
                continue
            z = 1.0 / np.maximum(w0 / cz[a] + w1 / cz[b] + w2 / cz[c], 1e-6)   # perspective-correct depth
            m &= z < zb[y0:y1 + 1, x0:x1 + 1]
            if not m.any():
                continue
            iz = w0 / cz[a] + w1 / cz[b] + w2 / cz[c]
            tu = (w0 * V[a, 9] / cz[a] + w1 * V[b, 9] / cz[b] + w2 * V[c, 9] / cz[c]) / iz
            tv = (w0 * V[a, 10] / cz[a] + w1 * V[b, 10] / cz[b] + w2 * V[c, 10] / cz[c]) / iz
            tx = ((tu % 1.0) * (tw - 1)).astype(np.int32)
            ty = ((tv % 1.0) * (th - 1)).astype(np.int32)
            col = T[ty, tx]
            if s.masked:
                m &= col.sum(-1) > 12
                if not m.any():
                    continue
            vc = (w0[..., None] * V[a, 6:9] + w1[..., None] * V[b, 6:9] + w2[..., None] * V[c, 6:9])
            if s.fx & 1:
                sh = vc
            else:
                L = (w0 * (lam2[a] if s.fx & 16 else lam[a]) + w1 * (lam2[b] if s.fx & 16 else lam[b]) + w2 * (lam2[c] if s.fx & 16 else lam[c]))
                sh = (0.35 + 0.75 * L)[..., None] * vc
            out = col * sh * np.array(s.tint, np.float32)
            reg = img[y0:y1 + 1, x0:x1 + 1]
            if s.alpha < 1:
                reg[m] = reg[m] * (1 - s.alpha) + out[m] * s.alpha
                continue
            reg[m] = out[m]
            zr = zb[y0:y1 + 1, x0:x1 + 1]
            zr[m] = z[m]
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))


if __name__ == '__main__':
    os.makedirs(PREV, exist_ok=True)
    tex_save(flint_tex(), os.path.join(ITEMS, 'scp820_flint.png'))
    tex_save(mosaic_tex(), os.path.join(ITEMS, 'scp820_mosaic.png'))
    tex_save(gold_tex(), os.path.join(ITEMS, 'scp820_gold.png'))
    tex_save(scales_tex(), os.path.join(ITEMS, 'scp820_scales.png'))
    tex_save(feather_tex(), os.path.join(ITEMS, 'scp820_feather.png'))
    K = knife()
    K.write(os.path.join(ITEMS, 'scp820jp.b3d'))
    print('scp820jp: %d triangles' % K.tris())
    tex_save(needle_card_tex(), os.path.join(PROPS, 'scp867_frond.png'))
    tex_save(bark_tex(), os.path.join(PROPS, 'scp867_bark.png'))
    tex_save(crown_tex(), os.path.join(PROPS, 'scp867_crown.png'))
    T = spruce()
    T.write(os.path.join(PROPS, 'scp867.b3d'))
    print('scp867: %d triangles' % T.tris())
    # previews and the knife's inventory icon
    a = render(K, ITEMS, (14, 20, -30), (0, 15, 0), size=(512, 640), fov=42)
    b = render(K, ITEMS, (-4, 29, -8), (0, 25, 1), size=(512, 640), fov=40)
    sheet = Image.new('RGB', (1024, 640))
    sheet.paste(a, (0, 0))
    sheet.paste(b, (512, 0))
    sheet.save(os.path.join(PREV, 'hd29_scp820jp.png'))
    ic = render(K, ITEMS, (16, 15, -26), (0, 14.5, 0), size=(256, 256), fov=48, bg=(0, 0, 0))
    ic.resize((64, 64), Image.LANCZOS).save(os.path.join(ITEMS, 'INVscp820jp.png'))
    t1 = render(T, PROPS, (0, 190, -560), (0, 180, 0), size=(512, 640), fov=46, bg=(40, 40, 44))
    t2 = render(T, PROPS, (150, 60, -150), (0, 230, 0), size=(512, 640), fov=60, bg=(40, 40, 44))
    sheet = Image.new('RGB', (1024, 640))
    sheet.paste(t1, (0, 0))
    sheet.paste(t2, (512, 0))
    sheet.save(os.path.join(PREV, 'hd29_scp867.png'))
    print('previews written')
