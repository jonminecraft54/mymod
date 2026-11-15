r"""High-detail models for batch 35 (original work after the scp-wiki.wikidot.com articles, CC BY-SA 3.0).
Props (room units): Grandmother Predictions (517), the jewelled projector (806), a floating marble head (569), the
mossy cedar giant (1579), the organ printer (1512-EX), the coin-eating reptile (1779).
Items (cm): hat2890, brush2816, briefs1388, watch1912.
   python make_hd35.py"""
import math
import os
import random
from PIL import Image, ImageDraw, ImageFilter
from make_hd29 import Model, tube, lathe, add, render, ITEMS, PROPS, PREV
from make_hd30 import blob, quad, xform, rot, noise_tex, F, FR
from make_hd31 import boxq
from make_hd33 import ring, tex, solid_tex
from make_hd34 import T, biped

RND = random.Random(35)


def fortune():
    T(PROPS, 's517_wood.png', (110, 50, 34), 12, 1)
    sg = Image.new('RGB', (256, 64), (40, 20, 60))
    d = ImageDraw.Draw(sg)
    d.text((128, 32), 'GRANDMOTHER PREDICTIONS', font=F(18), fill=(255, 220, 120), anchor='mm')
    tex(sg, PROPS, 's517_sign.png')
    T(PROPS, 's517_shawl.png', (60, 90, 170), 10, 2)
    T(PROPS, 's517_blouse.png', (236, 232, 222), 5, 3)
    T(PROPS, 's517_face.png', (220, 186, 160), 6, 4)
    solid_tex(PROPS, 's517_flame.png', (255, 210, 120), 6, 5)
    M = Model()
    w = M.surf('wood', 's517_wood.png', shine=0.6)
    gl = M.surf('glass', 's2394_glass.png', fx=16, alpha=0.22, shine=1.0)
    boxq(w, -45, 0, -35, 45, 100, 35, 1 / 60.0)                                   # the cabinet base
    boxq(w, -45, 190, -35, 45, 215, 35, 1 / 60.0)
    for (x, z) in ((-45, -35), (45, -35), (-45, 35), (45, 35)):
        boxq(w, x - 3, 100, z - 3, x + 3, 190, z + 3, 1 / 60.0)
    quad(gl, (-42, 100, -35), (42, 100, -35), (42, 190, -35), (-42, 190, -35))
    for f in (-1, 1):
        quad(gl, (f * 45, 100, -32 * f), (f * 45, 100, 32 * f), (f * 45, 190, 32 * f), (f * 45, 190, -32 * f))
    quad(M.surf('sign', 's517_sign.png', fx=1), (-44, 196, -35.5), (44, 196, -35.5), (44, 212, -35.5), (-44, 212, -35.5))
    # the puppet: an old woman in a white blouse and a blue shawl, behind the glass
    sh = M.surf('shawl', 's517_shawl.png', shine=0.1)
    bl = M.surf('blouse', 's517_blouse.png', shine=0.1)
    fc = M.surf('face', 's517_face.png', shine=0.3)
    blob(bl, (0, 130, 5), (18, 22, 13), rings=10, segs=14)
    blob(sh, (0, 142, 5), (22, 12, 15), e=0.8, rings=8, segs=14)
    blob(fc, (0, 164, 3), (9, 11, 9), rings=10, segs=12)
    blob(M.surf('hair', 's517_blouse.png'), (0, 170, 6), (9.5, 7, 9), rings=8, segs=12)
    for e in (-1, 1):
        tube(sh, [(e * 18, 140, 4), (e * 20, 120, -6), (e * 10, 112, -14)], lambda i: 4, 8)
        blob(fc, (e * 8, 111, -15), (3.5, 3, 3), rings=6, segs=8)
    blob(M.surf('ball', 's2394_glass.png', shine=1.0, alpha=0.6), (0, 113, -18), (6, 6, 6), rings=8, segs=12)
    tube(w, [(28, 100, -10), (28, 120, -10)], lambda i: 2, 8)                        # the electric candle
    blob(M.surf('flame', 's517_flame.png', fx=1), (28, 124, -10), (2, 4, 2), rings=6, segs=8)
    boxq(M.surf('slot', 's3938_tyre.png'), -10, 70, -35.5, 10, 74, -35, 0.1)
    tube(M.surf('cord', 's3938_tyre.png'), [(40, 4, 30), (60, 1, 36), (66, 1, 40)], lambda i: 1, 6)     # the cut cord
    return M


def projector():
    T(PROPS, 's806_body.png', (40, 40, 44), 6, 6)
    solid_tex(PROPS, 's806_brass.png', (190, 150, 60), 10, 7)
    gem = Image.new('RGB', (64, 64))
    d = ImageDraw.Draw(gem)
    for i in range(0, 64, 8):
        d.rectangle([0, i, 64, i + 8], fill=[(200, 40, 60), (60, 160, 220), (60, 200, 90), (240, 200, 60)][(i // 8) % 4])
    tex(gem, PROPS, 's806_gem.png')
    M = Model()
    b = M.surf('body', 's806_body.png', shine=0.7)
    br = M.surf('brass', 's806_brass.png', shine=1.0)
    for (x, z) in ((-30, -24), (30, -24), (-30, 24), (30, 24)):
        tube(br, [(x, 0, z), (x * 0.4, 90, z * 0.4)], lambda i: 2, 6)                # the tripod stand
    boxq(b, -30, 90, -18, 30, 130, 18, 0.05)
    for z in (-30, 30):                                                          # the two reels
        ring(b, (0, 152, z * 0.0 + (z / 2)), 22, 2.5, 'x', 24, 6) if False else ring(b, (-14 if z < 0 else 14, 152, 0), 22, 2.5, 'z', 24, 6)
    for x in (-14, 14):
        tube(br, [(x, 130, 0), (x, 152, 0)], lambda i: 1.4, 6)
    k = len(br.V)
    lathe(br, [(0, 0), (9, 0), (9, 24), (7, 26), (0, 26)], 20, lambda i: i / 4.0)       # the lens barrel
    xform(br, k, lambda p: (p[1] - 56, p[0] + 110, p[2]))
    k = len(M.surf('gem', 's806_gem.png', fx=1, shine=1.0).V)
    lathe(M.S['gem'], [(0, 0), (7.5, 0), (7.5, 2)], 20, lambda i: i)
    xform(M.S['gem'], k, lambda p: (p[1] - 58, p[0] + 110, p[2]))
    return M


def marblehead():
    T(PROPS, 's569_marble.png', (226, 224, 220), 6, 8, 1.6)
    M = Model()
    m = M.surf('m', 's569_marble.png', shine=0.6)
    blob(m, (0, 0, 0), (11, 14, 12.5), rings=14, segs=18)
    blob(m, (0, -2, -12), (3, 4.5, 3), rings=6, segs=8)                              # the nose
    for e in (-1, 1):
        blob(m, (e * 11.5, 0, 0), (2, 4, 3), rings=6, segs=8)                       # ears
        blob(M.surf('eye', 's3938_tyre.png', shine=0.4), (e * 4.5, 2, -11.4), (1.6, 1.0, 0.8), rings=4, segs=8)
    tube(m, [(-4, -9, -11), (0, -10, -12), (4, -9, -11)], lambda i: 0.8, 6)          # the mouth
    tube(m, [(0, -13, 0), (0, -19, 2)], lambda i: (6, 5)[i], 10)                       # the cut neck
    return M


def cedar():
    T(PROPS, 's1579_cedar.png', (120, 74, 48), 16, 9, 1.0)
    T(PROPS, 's1579_moss.png', (70, 140, 50), 18, 10, 1.4)
    M = Model()
    c = M.surf('cedar', 's1579_cedar.png', shine=0.1)
    mo = M.surf('moss', 's1579_moss.png', shine=0.0)
    biped(c, 340, 1.25)
    for k in range(40):                                                           # moss patches
        y = RND.uniform(30, 320)
        a = RND.uniform(0, 6.28)
        r = 30 if y < 170 else 50
        blob(mo, (math.cos(a) * r, y, math.sin(a) * r * 0.6), (RND.uniform(5, 10), RND.uniform(4, 8), RND.uniform(3, 6)), rings=4, segs=6)
    boxq(c, -50, 0, -40, 50, 8, 40, 0.02)
    return M


def printer():
    T(PROPS, 's1512_frame.png', (180, 184, 190), 6, 11)
    T(PROPS, 's1512_gel.png', (220, 150, 150), 10, 12)
    M = Model()
    f = M.surf('frame', 's1512_frame.png', shine=0.8)
    for (x, z) in ((-70, -40), (70, -40), (-70, 40), (70, 40)):
        boxq(f, x - 4, 0, z - 4, x + 4, 140, z + 4, 0.05)
    boxq(f, -74, 70, -44, 74, 76, 44, 0.05)                                        # the bed
    boxq(M.surf('gel', 's1512_gel.png', shine=1.0, alpha=0.8), -50, 76, -30, 50, 80, 30, 0.05)
    for z in (-40, 40):
        boxq(f, -74, 136, z - 4, 74, 142, z + 4, 0.05)                             # the gantry rails
    boxq(f, -8, 128, -44, 8, 140, 44, 0.05)                                       # the carriage
    tube(f, [(0, 128, 0), (0, 92, 0)], lambda i: (4, 1.2)[i], 8)                     # the head
    blob(M.surf('organ', 's1512_gel.png', shine=0.9), (10, 86, 4), (12, 7, 9), rings=8, segs=12)
    lathe(M.surf('jar', 's2394_glass.png', fx=16, alpha=0.3, shine=1.0), [(0, 0), (10, 0), (10, 30), (0, 30)], 16, lambda i: i / 3.0, cx=60, cz=-20)
    return M


def reptile():
    T(PROPS, 's1779_skin.png', (96, 120, 90), 10, 13, 1.0)
    T(PROPS, 's1779_mane.png', (200, 170, 110), 18, 14, 0.6)
    solid_tex(PROPS, 's1779_coin.png', (196, 198, 200), 8, 15)
    M = Model()
    s = M.surf('skin', 's1779_skin.png', shine=0.8)
    mn = M.surf('mane', 's1779_mane.png', shine=0.1, fx=16)
    path = [(-24, 6, 0), (-8, 8, 0), (8, 8, 2), (20, 7, 4), (30, 5, 2)]
    tube(s, path, lambda i: (4, 6, 6, 4.5, 3)[i], 12)
    tube(s, [(-24, 6, 0), (-40, 4, -6), (-52, 2, -14)], lambda i: (4, 2.4, 0.6)[i], 8)     # tail
    blob(s, (36, 6, 2), (7, 4, 4.5), rings=8, segs=12)
    for e in (-1, 1):
        for x in (-12, 14):
            tube(s, [(x, 6, e * 5), (x + 3, 3, e * 10), (x + 5, 0, e * 12)], lambda i: (2, 1.6, 1.2)[i], 6)
        blob(M.surf('eye', 's3938_tyre.png', shine=1.0), (39, 8, 2 + e * 3.5), (1.2, 1.2, 1.2), rings=4, segs=6)
    for k in range(14):                                                           # the feathery mane
        a = k * 0.45
        p = (10 + math.cos(a) * 2, 12, 2 + math.sin(a) * 6)
        quad(mn, p, add(p, (2, 0, 0)), add(p, (-2, 8, math.sin(a) * 3)), add(p, (-4, 8, math.sin(a) * 3)))
    for k in range(6):
        lathe(M.surf('coin', 's1779_coin.png', shine=1.0), [(0, 0), (1.2, 0), (1.2, 0.2), (0, 0.2)], 12, lambda i: i, cx=-20 + k * 7, cz=12)
    return M


def tophat():
    T(ITEMS, 's2890_silk.png', (20, 20, 22), 4, 16)
    solid_tex(ITEMS, 's2890_band.png', (60, 20, 24), 4, 17)
    M = Model()
    s = M.surf('silk', 's2890_silk.png', shine=0.9)
    lathe(s, [(0, 0.4), (14, 0.4), (16, 0), (16, 0.6), (9, 1.2), (9.5, 14), (9.6, 15), (0, 15)], 32, lambda i: i / 7.0)
    lathe(M.surf('band', 's2890_band.png', shine=0.4), [(9.25, 1.4), (9.3, 4)], 32, lambda i: i)
    return M


def brushes():
    T(ITEMS, 's2816_wood.png', (170, 120, 70), 10, 18)
    solid_tex(ITEMS, 's2816_hair.png', (40, 30, 24), 8, 19)
    M = Model()
    w = M.surf('wood', 's2816_wood.png', shine=0.5)
    h = M.surf('hair', 's2816_hair.png', shine=0.1)
    me = M.surf('ferrule', 's3938_chrome.png', shine=1.0)
    for k, sz in enumerate((0.4, 0.6, 0.9, 1.2)):
        z = -4 + k * 2.6
        tube(w, [(-12, sz, z), (6, sz, z)], lambda i: (sz * 0.7, sz)[i], 8)
        tube(me, [(6, sz, z), (9, sz, z)], lambda i: sz * 1.05, 8)
        tube(h, [(9, sz, z), (12, sz, z), (13.5, sz, z)], lambda i: (sz, sz * 0.8, 0.1)[i], 8)
    return M


def briefs():
    im = Image.new('RGB', (256, 128), (40, 90, 210))
    d = ImageDraw.Draw(im)
    for k in range(8):
        x, y = RND.randrange(256), RND.randrange(30, 128)
        d.regular_polygon((x, y, 12), 5, fill=(250, 220, 40))
    d.rectangle([0, 0, 256, 24], fill=(220, 30, 40))
    d.text((128, 12), 'SUPER POWERS', font=F(16), fill=(255, 255, 255), anchor='mm')
    tex(im.transpose(Image.FLIP_TOP_BOTTOM), ITEMS, 's1388_cloth.png')
    M = Model()
    c = M.surf('cloth', 's1388_cloth.png', shine=0.2)
    lathe(c, [(9, 0), (10, 4), (11, 9), (11.5, 12)], 28, lambda i: i / 3.0)
    xform(c, 0, lambda p: (p[0], p[1] * 0.9, p[2] * 0.55))
    return M


def watch():
    face = Image.new('RGB', (128, 128), (240, 234, 214))
    d = ImageDraw.Draw(face)
    for k in range(12):
        a = math.radians(k * 30)
        d.text((64 + math.sin(a) * 48, 64 - math.cos(a) * 48), ('XII', 'I', 'II', 'III', 'IIII', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI')[k], font=F(11, FR), fill=(30, 30, 30), anchor='mm')
    d.line([(64, 64), (64, 30)], fill=(20, 20, 20), width=3)
    d.line([(64, 64), (40, 74)], fill=(20, 20, 20), width=3)
    tex(face, ITEMS, 's1912_face.png')
    M = Model()
    g = M.surf('gold', 's1007_key.png', shine=1.0)
    lathe(g, [(0, 0), (2.4, 0), (2.6, 0.5), (2.6, 1.0), (2.4, 1.2)], 32, lambda i: i / 4.0)
    fc = M.surf('face', 's1912_face.png', shine=0.8)
    base = len(fc.V)
    fc.V.append((0, 1.21, 0, 0, 1, 0, 1, 1, 1, 0.5, 0.5))
    for j in range(33):
        a = 2 * math.pi * j / 32
        x, z = 2.35 * math.cos(a), 2.35 * math.sin(a)
        fc.V.append((x, 1.21, z, 0, 1, 0, 1, 1, 1, x / 4.7 + 0.5, 1 - (z / 4.7 + 0.5)))
    for j in range(32):
        fc.T.append((base, base + 2 + j, base + 1 + j))
    ring(g, (0, 0.6, 2.9), 0.7, 0.2, 'x', 12, 5)
    tube(g, [(0, 0.6, 3.6), (0.5, 0.6, 7), (-0.5, 0.6, 10)], lambda i: 0.15, 4)          # a bit of chain
    return M


PROP_MODELS = [('scp517', fortune), ('scp806', projector), ('scp569', marblehead), ('scp1579', cedar),
               ('scp1512', printer), ('scp1779', reptile)]
ITEM_MODELS = [('hat2890', tophat), ('brush2816', brushes), ('briefs1388', briefs), ('watch1912', watch)]

if __name__ == '__main__':
    for f in ('s2394_glass.png', 's3938_tyre.png', 's3938_chrome.png', 's1007_key.png'):
        for folder in (PROPS, ITEMS):
            if not os.path.exists(os.path.join(folder, f)):
                src = [os.path.join(x, f) for x in (PROPS, ITEMS) if os.path.exists(os.path.join(x, f))]
                Image.open(src[0]).save(os.path.join(folder, f))
    out = {}
    for name, fn in PROP_MODELS:
        m = fn()
        m.write(os.path.join(PROPS, name + '.b3d'))
        out[name] = (m, PROPS)
    for name, fn in ITEM_MODELS:
        m = fn()
        m.write(os.path.join(ITEMS, name + '.b3d'))
        out[name] = (m, ITEMS)
    tiles = []
    for name, (m, folder) in out.items():
        pts = [v[:3] for s in m.S.values() for v in s.V]
        lo = [min(p[i] for p in pts) for i in range(3)]
        hi = [max(p[i] for p in pts) for i in range(3)]
        c = [(lo[i] + hi[i]) / 2 for i in range(3)]
        r = max(hi[i] - lo[i] for i in range(3))
        eye = (c[0] + r * 0.9, c[1] + r * 0.6, c[2] - r * 1.3)
        tiles.append(render(m, folder, eye, c, size=(256, 256), fov=45, bg=(30, 30, 34)))
        if folder == ITEMS:
            render(m, folder, eye, c, size=(256, 256), fov=45, bg=(0, 0, 0)).resize((64, 64), Image.LANCZOS).save(
                os.path.join(ITEMS, 'INV%s.png' % name))
    sheet = Image.new('RGB', (256 * 5, 512))
    for i, t in enumerate(tiles):
        sheet.paste(t, ((i % 5) * 256, (i // 5) * 256))
    sheet.save(os.path.join(PREV, 'hd35_models.png'))
    print('%d models, %d triangles' % (len(out), sum(m.tris() for m, _ in out.values())))
