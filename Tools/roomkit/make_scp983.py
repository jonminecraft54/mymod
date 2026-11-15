r"""SCP-983, the birthday monkey, and its gumdrop candies - models and textures (original work, after the user's
reference image and scp-wiki.wikidot.com/scp-983, CC BY-SA 3.0).

  GFX\map\props\scp983.b3d + scp983.png   the monkey, sitting with its legs out: a carved wooden face with a grin of
                                          square teeth and red glass eyes, brown fur, a faded red ringmaster's vest
                                          with a brass button, yellow-green sleeves, striped trousers, dark wooden
                                          hands and feet; a tarnished brass bell raised in the left hand, a brass
                                          striking rod in the right. About 2300 triangles, one 1024 texture.
  GFX\items\candy983.b3d                  a gumdrop: a sugared dome on a flat base
  GFX\items\candy983_<kind>.png, INVcandy983_<kind>.png   lum (crystal clear, glowing), clear, red, green, yellow,
                                          purple, black
  SCP-330's sweets get the user's four wrapper textures (images 46-49): candy330_<flavour>.png and their icons.
   python make_scp983.py"""
import math
import os
import random
import struct
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = r'I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9'
PROPS = os.path.join(ROOT, 'GFX', 'map', 'props')
ITEMS = os.path.join(ROOT, 'GFX', 'items')
IMG = r'C:\Users\Computer\AppData\Local\Temp\claude\I--MythicalC-v1-2-7-v0-1-scpcb-dx9\26a70fcf-4472-4ddb-a1ca-a030fd032c01\images'
RND = random.Random(983)

# ---------------------------------------------------------------- the texture atlas: name -> (u0, v0, u1, v1) in 0..1
ATLAS = {'face': (0, 0, .5, .5), 'fur': (.5, 0, .75, .25), 'vest': (.75, 0, 1, .25), 'sleeve': (.5, .25, .75, .5),
         'pants': (.75, .25, 1, .5), 'hand': (0, .5, .25, .75), 'brass': (.25, .5, .5, .75), 'rod': (.5, .5, .75, .75),
         'eye': (.75, .5, .875, .625), 'teeth': (.875, .5, 1, .625), 'button': (.75, .625, .875, .75)}


def grime(im, amount=26, seed=1):
    rnd = random.Random(seed)
    px = im.load()
    w, h = im.size
    for _ in range(w * h // 6):
        x, y = rnd.randrange(w), rnd.randrange(h)
        r, g, b = px[x, y][:3]
        n = rnd.randint(-amount, amount // 2)
        px[x, y] = (max(0, min(255, r + n)), max(0, min(255, g + n)), max(0, min(255, b + n)))
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for _ in range(18):
        x, y, r = rnd.randrange(w), rnd.randrange(h), rnd.randint(w // 20, w // 6)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(40, 30, 20, 40))
    return Image.alpha_composite(im.convert('RGBA'), ov.filter(ImageFilter.GaussianBlur(w // 30))).convert('RGB')


def atlas():
    S = 1024
    tex = Image.new('RGB', (S, S), (60, 40, 30))

    def put(name, im):
        u0, v0, u1, v1 = ATLAS[name]
        tex.paste(im.resize((int((u1 - u0) * S), int((v1 - v0) * S))), (int(u0 * S), int(v0 * S)))

    # the face: pale carved wood, darker round the edge, a grin of square teeth, a little nose, the brow
    f = Image.new('RGB', (512, 512), (186, 160, 118))
    d = ImageDraw.Draw(f)
    for r in range(256, 0, -8):
        c = int(150 + 40 * (1 - r / 256))
        d.ellipse([256 - r, 256 - r, 256 + r, 256 + r], fill=(c + 20, c, c - 40))
    for y in range(0, 512, 7):                                          # wood grain
        d.line([(0, y + RND.randint(-2, 2)), (512, y + RND.randint(-2, 2))], fill=(150, 124, 86), width=1)
    d.rectangle([150, 300, 362, 380], fill=(60, 30, 25))                # the mouth
    for k in range(6):
        d.rectangle([156 + k * 34, 304, 184 + k * 34, 338], fill=(236, 226, 200), outline=(90, 80, 60))
        d.rectangle([156 + k * 34, 344, 184 + k * 34, 376], fill=(228, 216, 190), outline=(90, 80, 60))
    d.ellipse([236, 250, 276, 280], fill=(90, 60, 45))                  # the nose
    for x in (170, 342):                                                 # eye sockets
        d.ellipse([x - 40, 150, x + 40, 230], fill=(110, 80, 55))
    d.rectangle([0, 0, 512, 90], fill=(110, 70, 45))                    # the brown cap of fur above the brow
    put('face', grime(f, 30, 2))
    fur = Image.new('RGB', (256, 256), (112, 72, 46))
    d = ImageDraw.Draw(fur)
    for _ in range(900):
        x, y = RND.randrange(256), RND.randrange(256)
        d.line([(x, y), (x + RND.randint(-3, 3), y + 6)], fill=(RND.randint(70, 100), RND.randint(44, 62), RND.randint(28, 40)))
    put('fur', grime(fur, 20, 3))
    vest = Image.new('RGB', (256, 256), (128, 40, 42))
    d = ImageDraw.Draw(vest)
    d.rectangle([0, 0, 256, 20], fill=(150, 120, 60))
    put('vest', grime(vest, 34, 4))
    sl = Image.new('RGB', (256, 256), (170, 166, 84))
    put('sleeve', grime(sl, 30, 5))
    pa = Image.new('RGB', (256, 256), (214, 214, 200))
    d = ImageDraw.Draw(pa)
    for x in range(0, 256, 32):
        d.rectangle([x, 0, x + 12, 256], fill=(170, 160, 96))
        d.line([(x + 20, 0), (x + 20, 256)], fill=(140, 150, 150), width=2)
    put('pants', grime(pa, 40, 6))
    ha = Image.new('RGB', (256, 256), (82, 52, 36))
    put('hand', grime(ha, 20, 7))
    br = Image.new('RGB', (256, 256), (186, 120, 84))
    d = ImageDraw.Draw(br)
    for _ in range(60):                                                  # the tarnish
        x, y, r = RND.randrange(256), RND.randrange(256), RND.randint(4, 18)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(120, 96, 70))
    put('brass', br.filter(ImageFilter.GaussianBlur(2)))
    put('rod', Image.new('RGB', (64, 64), (96, 64, 44)))
    ey = Image.new('RGB', (128, 128), (220, 200, 180))
    d = ImageDraw.Draw(ey)
    d.ellipse([20, 20, 108, 108], fill=(150, 20, 20))
    d.ellipse([46, 46, 82, 82], fill=(30, 5, 5))
    d.ellipse([52, 40, 64, 52], fill=(255, 220, 220))
    put('eye', ey)
    put('teeth', Image.new('RGB', (64, 64), (232, 222, 196)))
    bu = Image.new('RGB', (64, 64), (200, 160, 70))
    ImageDraw.Draw(bu).ellipse([12, 12, 52, 52], outline=(120, 90, 30), width=5)
    put('button', bu)
    tex.save(os.path.join(PROPS, 'scp983.png'))


# ---------------------------------------------------------------- geometry
class Mesh:
    def __init__(self):
        self.V, self.T = [], []

    def ellipsoid(self, c, r, part, rings=12, segs=16, rot=None, uvfront=False):
        """an ellipsoid at c with radii r; UVs spread over the atlas region of `part` (uvfront: planar from the
        front, for the face)"""
        u0, v0, u1, v1 = ATLAS[part]
        base = len(self.V)
        for i in range(rings + 1):
            th = math.pi * i / rings
            for j in range(segs + 1):
                ph = 2 * math.pi * j / segs
                nx, ny, nz = math.sin(th) * math.cos(ph), math.cos(th), math.sin(th) * math.sin(ph)
                p = [nx * r[0], ny * r[1], nz * r[2]]
                n = [nx / r[0], ny / r[1], nz / r[2]]
                if rot:
                    p, n = rot(p), rot(n)
                l = math.sqrt(sum(k * k for k in n)) or 1
                if uvfront:
                    uu, vv = 0.5 + nx * 0.5, 0.5 - ny * 0.5
                else:
                    uu, vv = j / segs, i / rings
                self.V.append((c[0] + p[0], c[1] + p[1], c[2] + p[2], n[0] / l, n[1] / l, n[2] / l,
                               u0 + (u1 - u0) * uu, v0 + (v1 - v0) * vv))
        for i in range(rings):
            for j in range(segs):
                a = base + i * (segs + 1) + j
                b = a + segs + 1
                self.T.append((a, a + 1, b))
                self.T.append((a + 1, b + 1, b))

    def tube(self, p0, p1, r0, r1, part, segs=12, caps=True):
        u0, v0, u1, v1 = ATLAS[part]
        ax = [p1[k] - p0[k] for k in range(3)]
        L = math.sqrt(sum(k * k for k in ax)) or 1
        w = [k / L for k in ax]
        t = [0, 1, 0] if abs(w[1]) < 0.9 else [1, 0, 0]
        a = [w[1] * t[2] - w[2] * t[1], w[2] * t[0] - w[0] * t[2], w[0] * t[1] - w[1] * t[0]]
        la = math.sqrt(sum(k * k for k in a))
        a = [k / la for k in a]
        b = [w[1] * a[2] - w[2] * a[1], w[2] * a[0] - w[0] * a[2], w[0] * a[1] - w[1] * a[0]]
        base = len(self.V)
        for e, (p, r) in enumerate(((p0, r0), (p1, r1))):
            for j in range(segs + 1):
                ph = 2 * math.pi * j / segs
                n = [math.cos(ph) * a[k] + math.sin(ph) * b[k] for k in range(3)]
                self.V.append((p[0] + n[0] * r, p[1] + n[1] * r, p[2] + n[2] * r, n[0], n[1], n[2],
                               u0 + (u1 - u0) * j / segs, v0 + (v1 - v0) * e))
        for j in range(segs):                      # both windings: sleeves, legs and rods are seen from any side
            self.T.append((base + j, base + segs + 1 + j, base + j + 1))
            self.T.append((base + j + 1, base + segs + 1 + j, base + segs + 2 + j))
            self.T.append((base + j, base + j + 1, base + segs + 1 + j))
            self.T.append((base + j + 1, base + segs + 2 + j, base + segs + 1 + j))
        if caps:
            for e, (p, r, s) in enumerate(((p0, r0, -1), (p1, r1, 1))):
                c = len(self.V)
                self.V.append((p[0], p[1], p[2], w[0] * s, w[1] * s, w[2] * s, (u0 + u1) / 2, (v0 + v1) / 2))
                ring = base + e * (segs + 1)
                for j in range(segs):
                    self.T.append((c, ring + j + 1, ring + j) if s < 0 else (c, ring + j, ring + j + 1))

    def lathe(self, prof, c, part, segs=20, tilt=None):
        """a surface of revolution round the y axis: prof = [(radius, y)] bottom to top"""
        u0, v0, u1, v1 = ATLAS[part]
        base = len(self.V)
        for i, (r, y) in enumerate(prof):
            for j in range(segs + 1):
                ph = 2 * math.pi * j / segs
                p = [r * math.cos(ph), y, r * math.sin(ph)]
                n = [math.cos(ph), 0.3, math.sin(ph)]
                if tilt:
                    p, n = tilt(p), tilt(n)
                l = math.sqrt(sum(k * k for k in n))
                self.V.append((c[0] + p[0], c[1] + p[1], c[2] + p[2], n[0] / l, n[1] / l, n[2] / l,
                               u0 + (u1 - u0) * j / segs, v0 + (v1 - v0) * i / (len(prof) - 1)))
        for i in range(len(prof) - 1):
            for j in range(segs):
                a = base + i * (segs + 1) + j
                b = a + segs + 1
                self.T.append((a, b, a + 1))
                self.T.append((a + 1, b, b + 1))
                self.T.append((a, a + 1, b))          # both sides: the bell is open underneath
                self.T.append((a + 1, b + 1, b))


def rot_x(deg):
    a = math.radians(deg)
    return lambda p: [p[0], p[1] * math.cos(a) - p[2] * math.sin(a), p[1] * math.sin(a) + p[2] * math.cos(a)]


def monkey():
    """sitting, facing -z (towards the viewer), units ~cm: 38 tall"""
    m = Mesh()
    m.ellipsoid((0, 15, 0), (8, 10, 6.5), 'vest', 14, 18)                 # the body and vest
    m.ellipsoid((0, 15.5, -6.2), (1.0, 1.0, 0.5), 'button', 6, 8)       # the brass button
    m.ellipsoid((0, 7.5, 0.5), (8.5, 5.5, 7), 'pants', 12, 18)          # hips in striped trousers
    for s in (-1, 1):                                                    # legs out in front, feet up
        m.tube((s * 4.5, 5, -1), (s * 5.5, 3.5, -12), 3.6, 3.2, 'pants', 14)
        m.ellipsoid((s * 5.6, 4, -14.5), (3.2, 2.2, 3.4), 'hand', 8, 10)
        for k in (-1, 0, 1):                                             # toes
            m.tube((s * 5.6 + k * 1.3, 3, -16.5), (s * 5.6 + k * 1.3, 1.6, -18.5), 0.6, 0.4, 'hand', 6)
    m.ellipsoid((0, 30, -0.5), (7.2, 7.8, 6.8), 'fur', 14, 18)          # the head
    m.ellipsoid((0, 28.8, -4.2), (6.0, 6.6, 3.4), 'face', 14, 18, uvfront=True)    # the carved face
    for s in (-1, 1):
        m.ellipsoid((s * 2.4, 31.2, -7.2), (1.2, 1.2, 0.8), 'eye', 8, 10)          # red glass eyes
        m.ellipsoid((s * 7.4, 30.5, 0), (1.8, 2.4, 1.0), 'fur', 8, 10)             # ears
    m.tube((-3.2, 25.4, -7.0), (3.2, 25.4, -7.0), 1.0, 1.0, 'teeth', 10)          # the grin, standing out
    # arms: left (+x) raised, holding the bell up; right (-x) forward, holding the rod
    m.tube((7.5, 21, 0), (13, 25, -2), 2.6, 2.3, 'sleeve', 12)
    m.tube((13, 25, -2), (14, 31, -6), 2.3, 2.0, 'sleeve', 12)
    m.ellipsoid((14, 32, -6.5), (2.0, 1.8, 2.0), 'hand', 8, 10)
    m.tube((14, 33.5, -6.5), (14, 37.5, -6.5), 0.6, 0.6, 'brass', 8)              # the bell's handle
    m.lathe([(4.6, 23.0), (4.4, 24.0), (3.2, 26.5), (2.3, 29.5), (1.6, 31.0), (0.4, 31.4)], (14, 0, -6.5), 'brass', 20)
    m.tube((-7.5, 21, 0), (-10, 18.5, -6), 2.6, 2.3, 'sleeve', 12)
    m.tube((-10, 18.5, -6), (-6, 19.5, -11), 2.3, 2.0, 'sleeve', 12)
    m.ellipsoid((-5.6, 19.6, -12), (2.0, 1.8, 2.0), 'hand', 8, 10)
    m.tube((-5.6, 19.6, -12), (1.5, 21.5, -12.5), 0.55, 0.55, 'rod', 8)            # the striking rod
    m.ellipsoid((2.0, 21.6, -12.5), (1.2, 1.2, 1.2), 'brass', 6, 8)
    return m


def gumdrop():
    m = Mesh()
    ATLAS['drop'] = (0, 0, 1, 1)
    prof = [(0.0, 0.0), (1.55, 0.0), (1.6, 0.25), (1.55, 0.9), (1.35, 1.5), (1.0, 1.9), (0.5, 2.1), (0.0, 2.15)]
    base = len(m.V)
    segs = 24
    for i, (r, y) in enumerate(prof):
        for j in range(segs + 1):
            ph = 2 * math.pi * j / segs
            n = [math.cos(ph) * (1 if i else 0), 0.6 if i > 1 else -1, math.sin(ph) * (1 if i else 0)]
            l = math.sqrt(sum(k * k for k in n))
            m.V.append((r * math.cos(ph), y, r * math.sin(ph), n[0] / l, n[1] / l, n[2] / l, j / segs, i / (len(prof) - 1)))
    for i in range(len(prof) - 1):                  # rings go up: wound the other way from the ellipsoids
        for j in range(segs):
            a = base + i * (segs + 1) + j
            b = a + segs + 1
            m.T.append((a, b, a + 1))
            m.T.append((a + 1, b, b + 1))
    return m


def write_b3d(path, mesh, texname, shine=0.3, fx=0, alpha=1.0):
    chunk = lambda tag, body: tag + struct.pack('<i', len(body)) + body
    cstr = lambda s: s.encode('latin-1') + b'\0'
    texs = chunk(b'TEXS', cstr(texname) + struct.pack('<2i5f', 1, 2, 0, 0, 1, 1, 0))
    brus = chunk(b'BRUS', struct.pack('<i', 1) + cstr('main') + struct.pack('<5f2i', 1, 1, 1, alpha, shine, 1, fx) + struct.pack('<i', 0))
    vb = struct.pack('<3i', 1, 1, 2) + b''.join(struct.pack('<8f', *v) for v in mesh.V)
    tb = struct.pack('<i', 0) + b''.join(struct.pack('<3i', *t) for t in mesh.T)
    msh = chunk(b'MESH', struct.pack('<i', 0) + chunk(b'VRTS', vb) + chunk(b'TRIS', tb))
    node = chunk(b'NODE', cstr('m') + struct.pack('<10f', 0, 0, 0, 1, 1, 1, 1, 0, 0, 0) + msh)
    open(path, 'wb').write(chunk(b'BB3D', struct.pack('<i', 1) + texs + brus + node))


# ---------------------------------------------------------------- candies
KINDS = {'lum': (236, 248, 255), 'clear': (214, 228, 236), 'red': (220, 40, 52), 'green': (90, 200, 70),
         'yellow': (246, 214, 40), 'purple': (160, 70, 200), 'black': (16, 14, 18)}


def candy_tex(kind):
    col = KINDS[kind]
    im = Image.new('RGB', (128, 128), col)
    d = ImageDraw.Draw(im)
    rnd = random.Random(kind)
    for _ in range(420):                                               # sugar crystals
        x, y = rnd.randrange(128), rnd.randrange(128)
        v = 255 if kind != 'black' else 60
        d.point((x, y), fill=(v, v, v) if rnd.random() < 0.5 else tuple(min(255, c + 50) for c in col))
    if kind in ('lum', 'clear'):
        for y in range(128):                                           # a glassy band of light
            k = max(0, 1 - abs(y - 40) / 18)
            d.line([(0, y), (128, y)], fill=tuple(min(255, int(c + 40 * k)) for c in col))
    im.save(os.path.join(ITEMS, 'candy983_%s.png' % kind))
    ic = Image.new('RGB', (64, 64), (0, 0, 0))
    d = ImageDraw.Draw(ic)
    d.pieslice([10, 14, 54, 70], 180, 360, fill=col)
    d.rectangle([10, 41, 54, 44], fill=tuple(max(0, c - 40) for c in col))
    for _ in range(40):
        x, y = rnd.randint(14, 50), rnd.randint(18, 40)
        d.point((x, y), fill=(255, 255, 255) if kind != 'black' else (70, 70, 80))
    if kind == 'lum':
        ic = Image.blend(ic, ic.filter(ImageFilter.GaussianBlur(4)), 0.5)
    ic.save(os.path.join(ITEMS, 'INVcandy983_%s.png' % kind))


def candy330():
    """the user's wrapper textures for SCP-330's four flavours (originals kept as .bak_wrapper)"""
    for src, flav in (('46.png', 'grape'), ('47.png', 'lemon'), ('48.png', 'apple'), ('49.png', 'cherry')):
        p = os.path.join(IMG, src)
        if not os.path.exists(p):
            print('missing', p)
            continue
        dst = os.path.join(ITEMS, 'candy330_%s.png' % flav)
        if os.path.exists(dst) and not os.path.exists(dst + '.bak_wrapper'):
            os.replace(dst, dst + '.bak_wrapper')
        im = Image.open(p).convert('RGB')
        im.save(dst)
        icon = Image.new('RGB', (64, 64), (0, 0, 0))
        w = im.resize((40, 22)).rotate(-20, expand=True)
        icon.paste(w, ((64 - w.width) // 2, (64 - w.height) // 2))
        d = ImageDraw.Draw(icon)
        c = im.getpixel((10, 10))
        d.polygon([(6, 22), (14, 32), (6, 42)], fill=c)
        d.polygon([(58, 22), (50, 32), (58, 42)], fill=c)
        iv = os.path.join(ITEMS, 'INVcandy330_%s.png' % flav)
        if os.path.exists(iv) and not os.path.exists(iv + '.bak_wrapper'):
            os.replace(iv, iv + '.bak_wrapper')
        icon.save(iv)


if __name__ == '__main__':
    atlas()
    m = monkey()
    write_b3d(os.path.join(PROPS, 'scp983.b3d'), m, 'scp983.png', shine=0.25)
    g = gumdrop()
    write_b3d(os.path.join(ITEMS, 'candy983.b3d'), g, 'candy983_clear.png', shine=0.9)
    for k in KINDS:
        candy_tex(k)
    candy330()
    print('scp983: %d vertices, %d triangles; gumdrop %d triangles; %d candy kinds; SCP-330 wrappers'
          % (len(m.V), len(m.T), len(g.T), len(KINDS)))
