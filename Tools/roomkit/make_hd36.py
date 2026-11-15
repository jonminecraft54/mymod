r"""High-detail models for batch 36 (original work after scp-wiki.wikidot.com/scp-1921, -1200, -1916, -3147, -1479,
CC BY-SA 3.0, and the user's reference images 122 and 131).
Props (room units):
  scp1921.b3d   the cotton-candy kiosk: carved and painted wooden panels, scorched, the arched sign "COTTON CANDY -
                FREE WITH ADMISSION", the spinner bowl with a pump to the reservoir, a cone of black floss
  truck36.b3d   a Foundation transport truck (ref. 122): six wheels, a cab, a canvas-covered cargo bed
  cabin1479.b3d the cabin in the taiga (ref. 131): log walls, a steep shingled roof, a porch, boarded windows, a chimney,
                the lantern by the door
Items (cm): gum1200 (a "Tastes Like" pack), jar1916 (six jawbreakers in a jar), pop3147 (a Tongue Twister lollipop),
cotton1921 (a cone of black cotton candy).
   python make_hd36.py"""
import math
import os
import random
from PIL import Image, ImageDraw, ImageFilter
from make_hd29 import Model, tube, lathe, add, render, ITEMS, PROPS, PREV
from make_hd30 import blob, quad, xform, rot, noise_tex, F, FR
from make_hd31 import boxq
from make_hd33 import ring, tex, solid_tex
from make_hd34 import T

RND = random.Random(36)


def kiosk():
    w = noise_tex(256, (150, 60, 50), 10, 0.8, 1)
    d = ImageDraw.Draw(w)
    for k in range(0, 256, 32):
        d.rectangle([k + 4, 30, k + 28, 226], outline=(220, 180, 90), width=3)          # carved panels
        d.ellipse([k + 8, 110, k + 24, 146], outline=(240, 220, 160), width=2)
    for _ in range(30):                                                         # scorch
        x, y = RND.randrange(256), RND.randrange(256)
        d.ellipse([x - 14, y - 8, x + 14, y + 8], fill=(40, 26, 20))
    tex(w.filter(ImageFilter.GaussianBlur(0.6)), PROPS, 's1921_panel.png')
    sg = Image.new('RGB', (512, 128), (240, 220, 180))
    d = ImageDraw.Draw(sg)
    d.text((256, 46), 'COTTON CANDY', font=F(54), fill=(190, 40, 90), anchor='mm')
    d.text((256, 100), '- FREE WITH ADMISSION -', font=F(26), fill=(60, 40, 120), anchor='mm')
    tex(sg, PROPS, 's1921_sign.png')
    T(PROPS, 's1921_floss.png', (24, 18, 22), 10, 2, 2.0)
    M = Model()
    p = M.surf('panel', 's1921_panel.png', shine=0.4)
    s = M.surf('sign', 's1921_sign.png', fx=1)
    fl = M.surf('floss', 's1921_floss.png', shine=0.1)
    me = M.surf('steel', 's3938_chrome.png', shine=1.0)
    boxq(p, -60, 12, -40, 60, 110, 40, 1 / 60.0)                                   # the cart body
    boxq(p, -64, 110, -44, 64, 116, 44, 1 / 60.0)                                  # the counter top
    for x in (-60, 60):                                                          # the canopy posts and arch
        tube(p, [(x, 116, -40), (x, 230, -40)], lambda i: 3, 8)
        tube(p, [(x, 116, 40), (x, 230, 40)], lambda i: 3, 8)
    boxq(p, -66, 230, -46, 66, 238, 46, 1 / 60.0)
    arch = [(-62 + 124 * k / 12, 238 + 30 * math.sin(math.pi * k / 12), -44) for k in range(13)]
    tube(p, arch, lambda i: 2.5, 6)
    quad(s, (-56, 240, -45), (56, 240, -45), (56, 262, -45), (-56, 262, -45))
    for (x, z) in ((-50, -30), (50, -30), (-50, 30), (50, 30)):                     # wheels
        ring(M.surf('wheel', 's3938_tyre.png', shine=0.2), (x, 12, z + (6 if z > 0 else -6)), 11, 2.5, 'z', 18, 6)
    lathe(me, [(0, 116), (22, 116), (26, 134), (24, 136), (6, 124), (0, 124)], 24, lambda i: i / 5.0, cx=10, cz=0)   # the spinner bowl
    blob(fl, (10, 134, 0), (18, 10, 18), rings=8, segs=12)                         # black floss in the bowl
    tube(me, [(10, 112, 0), (10, 60, 20), (40, 30, 30)], lambda i: 1.4, 6)          # the pump line to the reservoir
    boxq(me, 28, 14, 20, 52, 40, 36, 0.05)                                         # the reservoir
    for k in range(3):                                                          # cones of black floss on the counter
        x = -44 + k * 16
        tube(M.surf('cone', 's4890_pages.png'), [(x, 116, -20), (x, 132, -20)], lambda i: (0.5, 0.5)[i], 6)
        blob(fl, (x, 140, -20), (7, 9, 7), rings=6, segs=10)
    return M


def truck():
    T(PROPS, 's36_truck.png', (70, 76, 64), 8, 3)
    T(PROPS, 's36_canvas.png', (86, 90, 70), 12, 4, 1.4)
    solid_tex(PROPS, 's36_glass.png', (30, 36, 40), 4, 5)
    M = Model()
    b = M.surf('body', 's36_truck.png', shine=0.4)
    cv = M.surf('canvas', 's36_canvas.png', shine=0.05)
    g = M.surf('glass', 's36_glass.png', shine=1.0)
    ty = M.surf('tyre', 's3938_tyre.png', shine=0.1)
    L, W = 420.0, 110.0                                                          # half length along z, half width
    boxq(b, -W, 50, -L, W, 70, L, 1 / 100.0)                                       # the chassis
    boxq(b, -W, 70, L - 170, W, 210, L, 1 / 100.0)                                 # the cab
    quad(g, (W - 10, 140, L + 0.5), (-W + 10, 140, L + 0.5), (-W + 10, 200, L + 0.5), (W - 10, 200, L + 0.5))
    for x in (-W - 0.5, W + 0.5):
        f = 1 if x > 0 else -1
        quad(g, (x, 140, L - 60 if f > 0 else L - 150), (x, 140, L - 150 if f > 0 else L - 60), (x, 196, L - 150 if f > 0 else L - 60), (x, 196, L - 60 if f > 0 else L - 150))
    boxq(b, -W + 10, 70, L, W - 10, 110, L + 20, 1 / 100.0)                         # the grille and bumper
    for x in (-W + 24, W - 24):
        blob(M.surf('lamp', 's3938_chrome.png', fx=1), (x, 120, L + 21), (8, 8, 2), rings=6, segs=10)
    boxq(b, -W, 70, -L, W, 100, L - 180, 1 / 100.0)                                # the bed
    pts = []
    for k in range(9):                                                          # the canvas tilt: a rounded cover
        a = math.pi * k / 8
        pts.append((-math.cos(a) * W, 100 + 90 + math.sin(a) * 60))
    for k in range(8):
        (x0, y0), (x1, y1) = pts[k], pts[k + 1]
        if k == 0:
            x0, y0 = -W, 100
        if k == 7:
            x1, y1 = W, 100
        quad(cv, (x0, y0, -L), (x1, y1, -L), (x1, y1, L - 185), (x0, y0, L - 185))
    quad(cv, (-W, 100, -L), (W, 100, -L), (W, 190, -L), (-W, 190, -L))
    for z in (-L + 70, -L + 190, L - 120):                                          # six wheels
        for x in (-W, W):
            k = len(ty.V)
            lathe(ty, [(0, -12), (38, -12), (42, -8), (42, 8), (38, 12), (0, 12)], 20, lambda i: i / 5.0)
            xform(ty, k, lambda p, x=x, z=z: (x + p[1], 42 + p[2], z + p[0]))
    boxq(b, -6, 210, L - 120, 6, 216, L - 20, 0.05)                                 # a beacon bar
    return M


def cabin():
    lg = Image.new('RGB', (256, 256), (60, 46, 34))
    d = ImageDraw.Draw(lg)
    for y in range(0, 256, 22):                                                 # log courses
        d.rectangle([0, y, 256, y + 18], fill=(74 + RND.randint(-8, 8), 56, 40))
        d.line([(0, y + 19), (256, y + 19)], fill=(28, 22, 16), width=3)
    tex(lg.filter(ImageFilter.GaussianBlur(0.8)), PROPS, 's1479_logs.png')
    sh = Image.new('RGB', (256, 256), (40, 40, 42))
    d = ImageDraw.Draw(sh)
    for y in range(0, 256, 16):
        for x in range(-((y // 16) % 2) * 12, 256, 24):
            d.rectangle([x + 1, y + 1, x + 22, y + 15], fill=(52 + RND.randint(-8, 8), 50, 50))
    tex(sh, PROPS, 's1479_shingle.png')
    bw = Image.new('RGB', (128, 128), (20, 18, 16))
    d = ImageDraw.Draw(bw)
    for k in range(3):
        d.polygon([(0, 20 + k * 40), (128, 6 + k * 40), (128, 30 + k * 40), (0, 44 + k * 40)], fill=(90, 74, 56))
    tex(bw, PROPS, 's1479_boards.png')
    solid_tex(PROPS, 's1479_door.png', (120, 84, 44), 10, 6)
    solid_tex(PROPS, 's1479_glow.png', (255, 180, 90), 8, 7)
    M = Model()
    lgs = M.surf('logs', 's1479_logs.png', shine=0.1)
    shg = M.surf('roof', 's1479_shingle.png', shine=0.1)
    bds = M.surf('boards', 's1479_boards.png', shine=0.1)
    dr = M.surf('door', 's1479_door.png', shine=0.2)
    gl = M.surf('glow', 's1479_glow.png', fx=1)
    W, D, H = 200.0, 160.0, 260.0                                                # half width (x), half depth (z), wall height
    boxq(lgs, -W, 0, -D, W, H, D, 1 / 120.0)
    boxq(lgs, -W - 10, 0, -D - 10, W + 10, 20, D + 10, 1 / 120.0)                    # the foundation sill
    # a steep gable roof along x, overhanging
    ridge = H + 170
    for f in (-1, 1):
        a = (-W - 20, H - 10, f * (D + 30))
        b = (W + 20, H - 10, f * (D + 30))
        c = (W + 20, ridge, 0)
        e = (-W - 20, ridge, 0)
        if f < 0:
            quad(shg, a, b, c, e)
        else:
            quad(shg, b, a, e, c)
    for x in (-W, W):                                                            # the gable ends
        f = 1 if x > 0 else -1
        k = len(lgs.V)
        lgs.V += [(x, H, -D, f, 0, 0, 1, 1, 1, 0, 1), (x, H, D, f, 0, 0, 1, 1, 1, 1, 1), (x, ridge - 20, 0, f, 0, 0, 1, 1, 1, 0.5, 0)]
        lgs.T.append((k, k + 2, k + 1) if f > 0 else (k, k + 1, k + 2))
    # the porch on -z: deck, posts, a porch roof
    boxq(dr, -W, 20, -D - 90, W, 30, -D, 1 / 80.0)
    for x in (-W + 10, -60, 60, W - 10):
        tube(dr, [(x, 30, -D - 84), (x, 190, -D - 84)], lambda i: 5, 8)
    quad(shg, (W + 10, 196, -D - 100), (-W - 10, 196, -D - 100), (-W - 10, 230, -D), (W + 10, 230, -D))
    quad(shg, (-W - 10, 196, -D - 100), (W + 10, 196, -D - 100), (W + 10, 230, -D), (-W - 10, 230, -D))
    quad(dr, (-34, 30, -D - 0.6), (34, 30, -D - 0.6), (34, 190, -D - 0.6), (-34, 190, -D - 0.6))     # the door
    for x in (-130, 130):                                                        # boarded windows, a glow behind
        quad(bds, (x - 40, 100, -D - 0.8), (x + 40, 100, -D - 0.8), (x + 40, 170, -D - 0.8), (x - 40, 170, -D - 0.8))
    quad(bds, (-60, H + 30, -D - 26), (60, H + 30, -D - 26), (60, H + 100, -D - 26), (-60, H + 100, -D - 26))    # attic window
    blob(gl, (-30, H + 60, -D - 27), (10, 8, 1), rings=4, segs=8)                    # eyes in the attic window
    blob(gl, (30, H + 60, -D - 27), (10, 8, 1), rings=4, segs=8)
    boxq(M.surf('stone', 's4612_stone.png'), W - 80, H, 40, W - 30, ridge + 40, 90, 1 / 60.0)    # the chimney
    tube(dr, [(56, 190, -D - 40), (56, 172, -D - 40)], lambda i: 0.6, 4)                  # the lantern on its hook
    boxq(M.surf('lantern', 's3938_tyre.png'), 50, 150, -D - 46, 62, 172, -D - 34, 0.1)
    blob(gl, (56, 160, -D - 40), (4, 7, 4), rings=6, segs=8)
    return M


def gum():
    im = Image.new('RGB', (256, 128), (250, 230, 60))
    d = ImageDraw.Draw(im)
    d.text((128, 40), 'Tastes Like', font=F(30, FR), fill=(60, 40, 20), anchor='mm')
    d.text((128, 86), 'CHEWING GUM', font=F(34), fill=(200, 40, 40), anchor='mm')
    d.text((128, 116), 'by The Factory', font=F(14, FR), fill=(60, 40, 20), anchor='mm')
    tex(im, ITEMS, 's1200_wrap.png')
    M = Model()
    s = M.surf('wrap', 's1200_wrap.png', shine=0.5)
    boxq(s, -3.5, 0, -1, 3.5, 1.6, 1, 0.1)
    quad(s, (-3.5, 1.61, 1), (3.5, 1.61, 1), (3.5, 1.61, -1), (-3.5, 1.61, -1))
    quad(s, (-3.5, 0, -1.01), (3.5, 0, -1.01), (3.5, 1.6, -1.01), (-3.5, 1.6, -1.01))
    for k in range(3):
        boxq(M.surf('stick', 's4890_pages.png'), 3.5, 0.2 + k * 0.45, -0.8, 5.2 - k * 0.4, 0.55 + k * 0.45, 0.8, 0.1)
    return M


def jawjar():
    M = Model()
    lathe(M.surf('glass', 's2394_glass.png', fx=16, alpha=0.25, shine=1.0), [(0, 0), (4.5, 0), (4.8, 1), (4.8, 10), (3.8, 11), (0, 11)], 24, lambda i: i / 5.0)
    lathe(M.surf('lid', 's1007_key.png', shine=0.8), [(3.9, 11), (4.1, 11.2), (4.1, 12.4), (0, 12.4)], 20, lambda i: i / 3.0)
    cols = [(220, 30, 30), (220, 200, 170), (230, 230, 226), (230, 140, 60), (20, 20, 20), (24, 24, 24)]
    for k, c in enumerate(cols):
        solid_tex(ITEMS, 's1916_%d.png' % (k + 1), c, 8, 10 + k)
        a = k * 1.05
        blob(M.surf('j%d' % k, 's1916_%d.png' % (k + 1), shine=1.0), (math.cos(a) * 2.2, 1.6 + (k // 3) * 3, math.sin(a) * 2.2), (1.5, 1.5, 1.5), rings=8, segs=12)
    return M


def lolly():
    im = Image.new('RGB', (128, 128), (230, 60, 150))
    d = ImageDraw.Draw(im)
    for k in range(0, 128, 16):
        d.arc([k // 2, k // 2, 128 - k // 2, 128 - k // 2], 0, 300, fill=(255, 220, 240), width=4)
    tex(im, ITEMS, 's3147_candy.png')
    M = Model()
    blob(M.surf('candy', 's3147_candy.png', shine=1.0), (0, 10, 0), (1.6, 1.6, 1.6), rings=10, segs=14)
    tube(M.surf('stick', 's4890_pages.png'), [(0, 0, 0), (0, 8.6, 0)], lambda i: 0.25, 6)
    return M


def cotton():
    M = Model()
    lathe(M.surf('cone', 's4890_pages.png'), [(0, 0), (0.6, 0), (1.6, 10), (0, 10)], 12, lambda i: i / 2.0)
    blob(M.surf('floss', 's1921_floss.png', shine=0.05), (0, 15, 0), (6, 7, 6), rings=10, segs=14)
    return M


if __name__ == '__main__':
    for f in ('s3938_chrome.png', 's3938_tyre.png', 's4890_pages.png', 's4612_stone.png', 's2394_glass.png', 's1007_key.png', 's1921_floss.png'):
        for folder in (PROPS, ITEMS):
            if not os.path.exists(os.path.join(folder, f)):
                src = [os.path.join(x, f) for x in (PROPS, ITEMS) if os.path.exists(os.path.join(x, f))]
                if src:
                    Image.open(src[0]).save(os.path.join(folder, f))
    out = {}
    for name, fn, folder in (('scp1921', kiosk, PROPS), ('truck36', truck, PROPS), ('cabin1479', cabin, PROPS)):
        m = fn()
        m.write(os.path.join(folder, name + '.b3d'))
        out[name] = (m, folder)
    Image.open(os.path.join(PROPS, 's1921_floss.png')).save(os.path.join(ITEMS, 's1921_floss.png'))
    for name, fn in (('gum1200', gum), ('jar1916', jawjar), ('pop3147', lolly), ('cotton1921', cotton)):
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
        eye = (c[0] + r * 0.8, c[1] + r * 0.5, c[2] - r * 1.2)
        tiles.append(render(m, folder, eye, c, size=(320, 320), fov=45, bg=(30, 30, 34)))
        if folder == ITEMS:
            render(m, folder, eye, c, size=(256, 256), fov=45, bg=(0, 0, 0)).resize((64, 64), Image.LANCZOS).save(
                os.path.join(ITEMS, 'INV%s.png' % name))
    sheet = Image.new('RGB', (320 * 4, 640))
    for i, t in enumerate(tiles):
        sheet.paste(t, ((i % 4) * 320, (i // 4) * 320))
    sheet.save(os.path.join(PREV, 'hd36_models.png'))
    print('%d models, %d triangles' % (len(out), sum(m.tris() for m, _ in out.values())))
