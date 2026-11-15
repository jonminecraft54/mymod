r"""High-detail models for batch 33 (original work after the scp-wiki.wikidot.com articles named below, CC BY-SA 3.0).
Props (GFX\map\props, room units):
  scp3938.b3d   Dr. Wondertainment's Take-You-Anywhere Machine: a bicycle with orange wheel covers (red centres), a
                cartoon face between the handlebars (red nose, big eyes, blue lips), a sofa-cushion seat with a
                backrest and lap belt, speakers under the seat, two antennae with W flags, the white back plate
  scp1007.b3d   a plain coffin, lid leaning on it, SCP-1007 inside (aged), the keyhole plate between the shoulders
  scp696.b3d    a portable mechanical typewriter with a red ribbon and a sheet of paper in red capitals
  scp252.b3d    a Mark 65 general-purpose bomb casing on a wooden cradle, "The Pink Scare" scrawled in pink
  scpl043.b3d   a manual turntable on its plinth, the record on the platter, the tonearm in the runout groove
  scp4612.b3d   the stone altar and SCP-4612-A: a ten-metre white limaciform body (translucent), six long arms with
                many-fingered hands and crystals in the palms, a fin along its length, the blue incision, palm prints
  scp2394.b3d   a terrarium on a stand, a green tree frog on a branch, the Firewire port on its skull, a cable, an IV
  scp1563.b3d   a wooden survey stake wound with pink "flagging tape" that is not tape
  scp3743.b3d   a Way of bent branches lashed into an arch, the painted icon of Eros hanging from it
  scp4712.b3d   a 12 cm hydraulic vault door: the round leaf with its bolt ring, the hinge, two rams, the frame
  scp5079.b3d   a hospital bed, the figure on it grown into it: pale fungal tendrils into the frame and the floor
  scp5267.b3d   a survey diorama of the hill and the ruined fort on the steppe
Items (GFX\items, cm units):
  key1007 (SCP-1007-1), drive4876, book4890, zapper232, gun865, coin762, case667 (SCP-667-2 remains), book7042
   python make_hd33.py"""
import math
import os
import random
from PIL import Image, ImageDraw, ImageFilter
from make_hd29 import Model, grid, tube, lathe, card, nrm, cross, sub, add, render, ITEMS, PROPS, PREV
from make_hd30 import blob, quad, xform, rot, noise_tex, F, FR, FM
from make_hd31 import boxq

RND = random.Random(33)


def tex(im, folder, name):
    im.save(os.path.join(folder, name))
    return name


def solid_tex(folder, name, rgb, amp=6, seed=0):
    return tex(noise_tex(64, rgb, amp, 0.8, seed), folder, name)


def ring(s, c, r, rt, axis='z', n=28, sides=8):
    """a torus: centre c, radius r, tube radius rt, in the plane normal to axis"""
    pts = []
    for k in range(n + 1):
        a = 2 * math.pi * k / n
        if axis == 'z':
            pts.append((c[0] + r * math.cos(a), c[1] + r * math.sin(a), c[2]))
        elif axis == 'x':
            pts.append((c[0], c[1] + r * math.sin(a), c[2] + r * math.cos(a)))
        else:
            pts.append((c[0] + r * math.cos(a), c[1], c[2] + r * math.sin(a)))
    tube(s, pts, lambda i: rt, sides)


def disc(s, c, r, axis='z', n=28, face=1):
    """a flat disc facing +axis (face=1) or -axis"""
    k = len(s.V)
    lathe(s, [(0, 0), (r, 0)] if face > 0 else [(r, 0), (0, 0)], n, lambda i: i)
    f = {'z': rot('x', 90 * face), 'x': rot('z', -90 * face), 'y': (lambda p: p) if face > 0 else rot('x', 180)}[axis]
    xform(s, k, lambda p: add(f(p), c))


# ============================================================================ SCP-3938: the bicycle
def bike():
    face = Image.new('RGB', (256, 256), (250, 236, 200))
    d = ImageDraw.Draw(face)
    for e in (-1, 1):
        d.ellipse([128 + e * 50 - 34, 50, 128 + e * 50 + 34, 130], fill=(255, 255, 255), outline=(0, 0, 0), width=4)
        d.ellipse([128 + e * 50 - 12, 76, 128 + e * 50 + 12, 116], fill=(10, 10, 10))
    d.ellipse([104, 120, 152, 168], fill=(230, 30, 30))
    d.chord([70, 150, 186, 230], 10, 170, fill=(40, 90, 220))
    tex(face, PROPS, 's3938_face.png')
    cover = Image.new('RGB', (256, 256), (250, 140, 30))
    d = ImageDraw.Draw(cover)
    d.ellipse([88, 88, 168, 168], fill=(220, 30, 30))
    tex(cover, PROPS, 's3938_cover.png')
    plate = Image.new('RGB', (512, 128), (246, 246, 246))
    d = ImageDraw.Draw(plate)
    d.text((256, 44), "Dr. Wondertainment's", font=F(30), fill=(200, 40, 140), anchor='mm')
    d.text((256, 92), 'TAKE-YOU-ANYWHERE MACHINE', font=F(34), fill=(40, 80, 200), anchor='mm')
    tex(plate, PROPS, 's3938_plate.png')
    flag = Image.new('RGB', (128, 128), (250, 230, 60))
    ImageDraw.Draw(flag).text((64, 64), 'W', font=F(90), fill=(200, 30, 160), anchor='mm')
    tex(flag, PROPS, 's3938_flag.png')
    solid_tex(PROPS, 's3938_frame.png', (40, 120, 200), 5, 1)
    solid_tex(PROPS, 's3938_tyre.png', (24, 24, 24), 4, 2)
    solid_tex(PROPS, 's3938_chrome.png', (190, 196, 200), 8, 3)
    tex(noise_tex(128, (200, 60, 70), 10, 1.4, 4), PROPS, 's3938_sofa.png')
    M = Model()
    fr = M.surf('frame', 's3938_frame.png', shine=0.8)
    ty = M.surf('tyre', 's3938_tyre.png', shine=0.1)
    ch = M.surf('chrome', 's3938_chrome.png', shine=1.0)
    cv = M.surf('cover', 's3938_cover.png', shine=0.5)
    fc = M.surf('face', 's3938_face.png', shine=0.4)
    so = M.surf('sofa', 's3938_sofa.png', shine=0.1)
    pl = M.surf('plate', 's3938_plate.png', shine=0.3)
    fl = M.surf('flag', 's3938_flag.png', fx=16)
    R0 = 36.0
    wheels = ((-62.0, R0, 0.0), (62.0, R0, 0.0))
    for c in wheels:
        ring(ty, c, R0, 3.2, 'z', 36, 8)
        ring(ch, c, R0 - 4, 1.2, 'z', 36, 6)
        for f in (1, -1):                                                        # the orange covers
            disc(cv, (c[0], c[1], c[2] + f * 1.5), R0 - 5, 'z', 32, f)
        tube(ch, [(c[0], c[1], -6), (c[0], c[1], 6)], lambda i: 2.4, 8)          # the hub
    rear, front = wheels
    bb = (-6.0, 30.0, 0.0)                                                       # bottom bracket
    st = (-24.0, 92.0, 0.0)                                                      # seat post top
    ht = (46.0, 96.0, 0.0)                                                       # head tube top
    hb = (52.0, 80.0, 0.0)
    for a, b in ((bb, st), (bb, hb), (st, ht), (rear, bb), (rear, st)):
        tube(fr, [a, b], lambda i: 2.6, 8)
    for z in (-4.5, 4.5):
        tube(fr, [(front[0], front[1], z), (hb[0] + 2, hb[1], z * 0.5), (ht[0], ht[1], 0)], lambda i: 2.0, 8)
    tube(ch, [(ht[0], ht[1], 0), (ht[0] - 4, ht[1] + 14, 0)], lambda i: 2.0, 8)
    tube(ch, [(ht[0] - 4, 110, -26), (ht[0] - 4, 110, 26)], lambda i: 1.6, 8)  # the bars
    for z in (-26, 26):
        tube(ty, [(ht[0] - 4, 110, z * 1.0), (ht[0] - 4, 110, z * 1.25)], lambda i: 2.2, 8)
    k = len(fc.V)                                                               # the face, between the bars
    quad(fc, (ht[0] + 2, 92, -17), (ht[0] + 2, 92, 17), (ht[0] + 2, 126, 17), (ht[0] + 2, 126, -17))
    blob(fc, (ht[0] + 0.5, 109, 0), (2.5, 17, 17), e=0.3, rings=6, segs=12, uv=(0, 0, 0.02, 0.02))
    blob(M.surf('nose', 's3938_cover.png', shine=0.8), (ht[0] + 4, 106, 0), (3.5, 3.5, 3.5), rings=8, segs=12,
         uv=(0.45, 0.45, 0.55, 0.55))
    # the sofa-cushion seat with a backrest and the lap belt, the speakers below
    blob(so, (st[0] - 2, st[1] + 6, 0), (16, 5, 14), e=0.4, rings=8, segs=16)
    blob(so, (st[0] - 16, st[1] + 20, 0), (4, 14, 14), e=0.4, rings=8, segs=16)
    tube(ty, [(st[0] - 8, st[1] + 12, -14), (st[0] + 6, st[1] + 13, 0), (st[0] - 8, st[1] + 12, 14)], lambda i: 0.8, 6)
    for z in (-11, 11):
        boxq(ty, st[0] - 10, st[1] - 10, z - 3, st[0] + 6, st[1] + 0, z + 3, 0.1)
        disc(ch, (st[0] - 2, st[1] - 5, z + (3.1 if z > 0 else -3.1)), 4, 'z', 16, 1 if z > 0 else -1)
    # two antennae over the back wheel with W flags; the back plate
    for z in (-6, 6):
        top = (rear[0] - 14, 170, z)
        tube(ch, [(rear[0] - 8, R0 + 6, z), top], lambda i: 0.8, 6)
        quad(fl, top, (top[0] - 18, top[1], z), (top[0] - 18, top[1] - 12, z), (top[0], top[1] - 12, z))
    boxq(ch, rear[0] - 26, 66, -1, rear[0] - 6, 70, 1, 0.1)
    for f in (-1, 1):
        quad(pl, (rear[0] - 40, 46, f * 9), (rear[0] - 6, 46, f * 9), (rear[0] - 6, 64, f * 9), (rear[0] - 40, 64, f * 9)) if f > 0 else \
            quad(pl, (rear[0] - 6, 46, f * 9), (rear[0] - 40, 46, f * 9), (rear[0] - 40, 64, f * 9), (rear[0] - 6, 64, f * 9))
    boxq(ch, rear[0] - 41, 44, -9, rear[0] - 5, 46, 9, 0.1)
    for z in (-12, 12):                                                         # the pedals
        tube(ch, [(bb[0], bb[1], 0), (bb[0] + (8 if z > 0 else -8), bb[1] - 10 * (1 if z > 0 else -1), z)], lambda i: 1.0, 6)
    return M


# ============================================================================ SCP-1007: the coffin
def coffin():
    tex(noise_tex(256, (92, 60, 38), 12, 1.0, 10), PROPS, 's1007_wood.png')
    tex(noise_tex(128, (200, 190, 200), 5, 1.2, 11), PROPS, 's1007_satin.png')
    tex(noise_tex(128, (190, 150, 128), 8, 1.4, 12), PROPS, 's1007_skin.png')
    tex(noise_tex(128, (210, 210, 206), 6, 1.4, 13), PROPS, 's1007_gown.png')
    solid_tex(PROPS, 's1007_brass.png', (190, 150, 60), 10, 14)
    M = Model()
    wd = M.surf('wood', 's1007_wood.png', shine=0.4)
    sa = M.surf('satin', 's1007_satin.png', shine=0.6)
    sk = M.surf('skin', 's1007_skin.png', shine=0.2)
    gw = M.surf('gown', 's1007_gown.png', shine=0.1)
    br = M.surf('brass', 's1007_brass.png', shine=0.9)
    L, W, H = 100.0, 34.0, 50.0                                                 # half-length (x), half-width, height
    boxq(wd, -L, 0, -W, L, 6, W, 1 / 60.0)
    for (x0, z0, x1, z1) in ((-L, -W, L, -W + 5), (-L, W - 5, L, W), (-L, -W, -L + 5, W), (L - 5, -W, L, W)):
        boxq(wd, x0, 6, z0, x1, H, z1, 1 / 60.0)
    quad(sa, (-L + 5, 6.2, W - 5), (L - 5, 6.2, W - 5), (L - 5, 6.2, -W + 5), (-L + 5, 6.2, -W + 5))
    for x in (-L * 0.6, 0, L * 0.6):                                            # brass handles
        for z in (-W - 2.5, W + 2.5):
            tube(br, [(x - 14, 26, z), (x - 12, 22, z), (x + 12, 22, z), (x + 14, 26, z)], lambda i: 1.0, 6)
    # the lid leaning against the far side
    k = len(wd.V)
    boxq(wd, -L, 0, -3, L, 4, W * 2 + 4, 1 / 60.0)
    xform(wd, k, lambda p: add(rot('x', -70)(p), (0, 0, W + 4)))
    # SCP-1007: an old man lying on the satin, the pillow, folded hands
    blob(sa, (-L + 24, 14, 0), (14, 6, 20), e=0.5, rings=6, segs=12)
    blob(sk, (-L + 26, 26, 0), (11, 9, 9), rings=10, segs=14)                  # head
    blob(gw, (-20, 22, 0), (52, 11, 20), e=0.7, rings=10, segs=16)              # torso and hips
    for z in (-8, 8):
        tube(gw, [(30, 18, z), (70, 15, z * 1.1), (L - 12, 15, z * 1.2)], lambda i: (8, 7, 5)[i], 10)
        blob(sk, (L - 10, 18, z * 1.2), (4, 4, 4), rings=6, segs=8)
    blob(sk, (-8, 33, 0), (8, 3.5, 10), rings=6, segs=10)                       # folded hands
    tube(gw, [(-50, 26, -18), (-24, 30, -16), (-10, 33, -6)], lambda i: 4.5, 8)
    tube(gw, [(-50, 26, 18), (-24, 30, 16), (-10, 33, 6)], lambda i: 4.5, 8)
    return M


# ============================================================================ SCP-696: the typewriter
def typewriter():
    tex(noise_tex(128, (34, 36, 34), 6, 0.8, 20), PROPS, 's696_body.png')
    solid_tex(PROPS, 's696_key.png', (226, 222, 210), 4, 21)
    solid_tex(PROPS, 's696_ribbon.png', (170, 20, 24), 6, 22)
    pap = Image.new('RGB', (256, 320), (246, 244, 236))
    d = ImageDraw.Draw(pap)
    for k, l in enumerate(['YOUR TIME IS NIGH.', 'IF YOU HAVE A GOD,', 'PRAY TO IT NOW.', 'STOP.', '',
                           'I MEANT THAT AS AN', 'OPENING LINE. IS IT', 'TOO MUCH? STOP.']):
        d.text((20, 30 + k * 30), l, font=F(18, FM), fill=(170, 20, 20))
    tex(pap.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.FLIP_TOP_BOTTOM), PROPS, 's696_paper.png')
    M = Model()
    b = M.surf('body', 's696_body.png', shine=0.7)
    ky = M.surf('keys', 's696_key.png', shine=0.5)
    rb = M.surf('ribbon', 's696_ribbon.png', shine=0.4)
    pp = M.surf('paper', 's696_paper.png', fx=16)
    boxq(b, -16, 0, -14, 16, 6, 12, 0.05)                                     # base
    k = len(b.V)
    boxq(b, -16, 0, 0, 16, 7, 12, 0.05)                                       # the sloped key bed
    xform(b, k, lambda p: add(rot('x', -14)(p), (0, 4, -12)))
    boxq(b, -17, 6, 6, 17, 13, 14, 0.05)                                       # the carriage housing
    tube(b, [(-20, 15, 10), (20, 15, 10)], lambda i: 3.0, 12)                  # the platen
    for x in (-21, 21):
        disc(b, (x, 15, 10), 3.4, 'x', 12, 1 if x > 0 else -1)
    tube(b, [(18, 16, 6), (24, 18, 2)], lambda i: 0.7, 6)                      # the return lever
    for r in range(4):                                                          # four rows of round keys
        for c in range(10 - (r % 2)):
            x = -12.5 + c * 2.8 + (r % 2) * 1.4
            z = -11.5 + r * 2.6
            y = 6.5 + r * 0.7
            lathe(ky, [(0, y + 1.1), (1.0, y + 1.1), (1.0, y)], 10, lambda i: i / 2.0, cx=x, cz=z)
            tube(b, [(x, y, z), (x, y - 1.8, z)], lambda i: 0.3, 4)
    for x in (-7, 7):                                                           # ribbon spools
        lathe(rb, [(0, 13.4), (2.6, 13.4), (2.6, 14.6), (0, 14.6)], 14, lambda i: i / 3.0, cx=x, cz=8)
    quad(pp, (-10, 14, 13), (10, 14, 13), (10, 40, 18), (-10, 40, 18))
    return M


# ============================================================================ SCP-252-EX: the bomb
def bomb():
    sk = noise_tex(512, (96, 104, 84), 8, 1.0, 30)
    d = ImageDraw.Draw(sk)
    for k in range(0, 512, 128):
        d.line([(k, 0), (k, 512)], fill=(70, 74, 60), width=4)
    d.text((300, 200), 'The Pink Scare', font=F(46, FR), fill=(255, 110, 190), anchor='mm')
    d.rectangle([60, 300, 140, 330], fill=(230, 190, 40))
    tex(sk, PROPS, 's252_skin.png')
    M = Model()
    s = M.surf('skin', 's252_skin.png', shine=0.5)
    wd = M.surf('wood', 's1007_wood.png', shine=0.2)
    prof = [(0, 0), (6, 2), (14, 12), (19, 30), (21, 50), (21, 120), (18, 160), (12, 185), (9, 200), (0, 200)]
    k = len(s.V)
    lathe(s, prof, 28, lambda i: i / 9.0)
    xform(s, k, lambda p: (p[1] - 100, p[0] + 34, p[2]))                       # lying along x
    for a in range(4):                                                          # the tail fins (box tail)
        k = len(s.V)
        boxq(s, 90, 0, -0.8, 130, 22, 0.8, 0.02)
        xform(s, k, lambda p, a=a: add(rot('x', 45 + a * 90)((p[0], p[1], p[2])), (0, 34, 0)))
    ring(s, (118, 34, 0), 20, 1.4, 'x', 24, 6)
    for x in (-50, 40):                                                         # the cradle
        boxq(wd, x - 6, 0, -26, x + 6, 16, 26, 1 / 40.0)
        boxq(wd, x - 6, 16, -26, x + 6, 22, -14, 1 / 40.0)
        boxq(wd, x - 6, 16, 14, x + 6, 22, 26, 1 / 40.0)
    return M


# ============================================================================ SCP-L043: the turntable
def turntable():
    lab = Image.new('RGB', (256, 256), (10, 10, 10))
    d = ImageDraw.Draw(lab)
    for r in range(126, 40, -3):
        d.ellipse([128 - r, 128 - r, 128 + r, 128 + r], outline=(26, 26, 26))
    d.ellipse([84, 84, 172, 172], fill=(200, 40, 50))
    d.text((128, 116), 'SIDE B', font=F(12), fill=(250, 230, 200), anchor='mm')
    d.text((128, 140), 'RUNOUT', font=F(10), fill=(250, 230, 200), anchor='mm')
    tex(lab, PROPS, 'sl043_record.png')
    tex(noise_tex(128, (110, 70, 40), 10, 1.0, 40), PROPS, 'sl043_wood.png')
    M = Model()
    wd = M.surf('wood', 'sl043_wood.png', shine=0.6)
    ch = M.surf('chrome', 's3938_chrome.png', shine=1.0)
    rc = M.surf('record', 'sl043_record.png', shine=0.9)
    dk = M.surf('dark', 's3938_tyre.png', shine=0.2)
    boxq(wd, -24, 0, -18, 24, 8, 18, 0.03)
    lathe(ch, [(0, 8), (16, 8), (16, 9.5), (0, 9.5)], 32, lambda i: i / 3.0, cx=-4, cz=0)
    k = len(rc.V)
    lathe(rc, [(15.5, 9.8), (0, 9.8)], 40, lambda i: i)
    for i in range(k, len(rc.V)):                                              # planar uv for the label
        v = rc.V[i]
        rc.V[i] = v[:9] + ((v[0]) / 31.0 + 0.5, (v[2]) / 31.0 + 0.5)
        rc.V[i] = (v[0] - 4,) + rc.V[i][1:]
    tube(ch, [(-4, 9, 0), (-4, 11.5, 0)], lambda i: 0.5, 6)
    tube(ch, [(18, 8, 12), (18, 13, 12)], lambda i: 1.4, 8)                    # the arm pivot
    tube(ch, [(18, 13, 12), (10, 12.5, 6), (0, 11, -6)], lambda i: 0.6, 6)    # the arm, in the runout
    boxq(dk, -1.5, 10, -8, 1.5, 11.5, -4, 0.1)
    for (x, z) in ((18, -12), (20, -6)):
        lathe(dk, [(0, 9.5), (1.6, 9.5), (1.6, 8)], 10, lambda i: i, cx=x, cz=z)
    return M


# ============================================================================ SCP-4612: the cadaver on its altar
def cadaver():
    fl = noise_tex(512, (232, 234, 238), 6, 1.6, 50)
    d = ImageDraw.Draw(fl)
    for _ in range(14):                                                         # the bloodied palm prints (blue)
        x, y = RND.randrange(30, 480), RND.randrange(30, 480)
        d.ellipse([x - 14, y - 18, x + 14, y + 14], fill=(70, 110, 200))
        for f in range(10):
            a = math.radians(-160 + f * 14)
            d.line([(x, y), (x + math.cos(a) * 34, y + math.sin(a) * 34)], fill=(70, 110, 200), width=4)
    tex(fl.filter(ImageFilter.GaussianBlur(1.2)), PROPS, 's4612_flesh.png')
    solid_tex(PROPS, 's4612_blood.png', (30, 90, 255), 12, 51)
    solid_tex(PROPS, 's4612_crystal.png', (150, 220, 255), 20, 52)
    st = noise_tex(256, (110, 104, 94), 14, 1.2, 53)
    d = ImageDraw.Draw(st)
    for x in range(10, 250, 14):
        d.polygon([(x, 120), (x + 9, 124), (x, 128)], fill=(64, 58, 50))
    tex(st, PROPS, 's4612_stone.png')
    M = Model()
    s = M.surf('flesh', 's4612_flesh.png', shine=0.7, alpha=0.88)
    bl = M.surf('blood', 's4612_blood.png', fx=1, shine=1.0)
    cr = M.surf('crystal', 's4612_crystal.png', fx=1, shine=1.0, alpha=0.9)
    sto = M.surf('stone', 's4612_stone.png', shine=0.1)
    boxq(sto, -380, 0, -70, 380, 70, 70, 1 / 100.0)                              # the altar
    boxq(sto, -400, 0, -90, 400, 14, 90, 1 / 100.0)
    for x in range(-330, 340, 110):
        boxq(sto, x - 30, 70, -72, x + 30, 76, 72, 1 / 100.0)
    # the body: a long tapering slug, flattened, lying along x on the altar
    n = 18
    path = [(-390 + 780 * i / n, 70 + 40 + 6 * math.sin(i * 0.7), 6 * math.sin(i * 0.4)) for i in range(n + 1)]
    rad = lambda i: (34 + 26 * math.sin(math.pi * min(1, (i + 2) / (n + 2))), 44 + 30 * math.sin(math.pi * min(1, (i + 2) / (n + 2))))
    tube(s, path, lambda i: (rad(i)[0], rad(i)[1]), 18, vrep=1 / 200.0)
    blob(s, path[-1], (30, 40, 44), rings=10, segs=16)                         # the head end
    blob(s, path[0], (16, 16, 20), rings=8, segs=12)
    # the fin along its back
    pts = [(p[0], p[1] + rad(i)[0] - 4, p[2]) for i, p in enumerate(path)]
    k = len(s.V)
    for i in range(n):
        a, b = pts[i], pts[i + 1]
        h = 26 * math.sin(math.pi * (i + 0.5) / n) + 4
        quad(s, a, b, (b[0], b[1] + h, b[2]), (a[0], a[1] + h, a[2]))
        quad(s, b, a, (a[0], a[1] + h, a[2]), (b[0], b[1] + h, b[2]))
    # the incision (glowing blue) along the near flank
    tube(bl, [(p[0], p[1] - 10, p[2] - rad(i)[1] + 1) for i, p in enumerate(path[2:-2], 2)], lambda i: 3.0, 6)
    # six arms (3 m): from the flanks, down over the altar's edges to the floor, many-fingered hands, crystals
    for k3, x in enumerate((-220, 0, 220)):
        for side in (-1, 1):
            j = int((x + 390) / 780 * n)
            sh = (x, 110, side * (rad(j)[1] - 8))
            el = (x + 20 * side, 74, side * 110)
            wr = (x + 10, 8, side * 150)
            tube(s, [sh, add(sh, (0, 0, side * 40)), el, wr], lambda i: (14, 12, 10, 8)[i], 12)
            hand = add(wr, (0, -2, side * 14))
            blob(s, hand, (14, 4, 12), rings=6, segs=12)
            for f in range(10):                                                 # ten digits
                a = math.radians(-80 + f * 17)
                tip = add(hand, (math.sin(a) * 26, -1, side * math.cos(a) * 26))
                tube(s, [hand, add(hand, (math.sin(a) * 13, 1, side * math.cos(a) * 13)), tip], lambda i: (2.4, 1.8, 0.8)[i], 5)
            blob(cr, add(hand, (0, 4, 0)), (5, 5, 5), e=0.5, rings=4, segs=6)
    return M


# ============================================================================ SCP-2394: the frog in its tank
def frog():
    tex(noise_tex(128, (70, 170, 70), 12, 1.0, 60), PROPS, 's2394_skin.png')
    solid_tex(PROPS, 's2394_glass.png', (200, 230, 230), 4, 61)
    tex(noise_tex(128, (90, 70, 50), 14, 1.0, 62), PROPS, 's2394_bark.png')
    solid_tex(PROPS, 's2394_port.png', (60, 60, 64), 5, 63)
    M = Model()
    sk = M.surf('skin', 's2394_skin.png', shine=0.9)
    gl = M.surf('glass', 's2394_glass.png', fx=16, alpha=0.25, shine=1.0)
    bk = M.surf('bark', 's2394_bark.png', shine=0.1)
    pt = M.surf('port', 's2394_port.png', shine=0.8)
    fr = M.surf('frame', 's3938_tyre.png', shine=0.4)
    W, D, H = 45.0, 28.0, 40.0
    boxq(fr, -W - 2, 0, -D - 2, W + 2, 4, D + 2, 0.05)
    for (x, z) in ((-W, -D), (W, -D), (W, D), (-W, D)):
        boxq(fr, x - 1.5, 4, z - 1.5, x + 1.5, 4 + H, z + 1.5, 0.05)
    boxq(fr, -W - 2, 4 + H, -D - 2, W + 2, 6 + H, D + 2, 0.05)
    for f in (rot('y', 0), rot('y', 180)):
        k = len(gl.V)
        quad(gl, (-W, 4, -D), (W, 4, -D), (W, 4 + H, -D), (-W, 4 + H, -D))
        xform(gl, k, f)
    for f in (rot('y', 90), rot('y', -90)):
        k = len(gl.V)
        quad(gl, (-D, 4, -W), (D, 4, -W), (D, 4 + H, -W), (-D, 4 + H, -W))
        xform(gl, k, f)
    blob(bk, (0, 5, 0), (W - 2, 1.5, D - 2), e=0.3, rings=4, segs=12)          # the bedding
    tube(bk, [(-36, 6, -10), (-10, 14, -4), (20, 18, 6), (36, 26, 12)], lambda i: (4, 3.5, 3, 2.5)[i], 10)
    tube(pt, [(8, 4 + H, 4), (0, 4 + H + 4, 0)], lambda i: 0.4, 6)              # the cable, hanging loose
    tube(M.surf('iv', 's2394_glass.png', shine=1.0), [(-6, 30, 10), (-14, 40, 14), (-30, 4 + H + 4, 20)], lambda i: 0.3, 6)
    return M


def frogonly():
    """SCP-2394 alone (it sits at (8, 18, 4) on the tank's branch)"""
    M = Model()
    sk = M.surf('skin', 's2394_skin.png', shine=0.9)
    pt = M.surf('port', 's2394_port.png', shine=0.8)
    c = (0, 4.5, 0)
    blob(sk, c, (6.5, 4.5, 5.5), rings=10, segs=14)
    blob(sk, add(c, (5.5, 2.5, 0)), (4.0, 3.2, 4.4), rings=8, segs=12)
    for z in (-2.6, 2.6):
        blob(M.surf('eye', 's3938_tyre.png', shine=1.0), add(c, (7.5, 5.0, z)), (1.3, 1.3, 1.3), rings=6, segs=8)
        tube(sk, [add(c, (-3, -1, z * 1.5)), add(c, (-7, -3, z * 2.6)), add(c, (-2, -4.5, z * 2.8))], lambda i: 1.4, 6)
        tube(sk, [add(c, (3, -2, z * 1.5)), add(c, (6, -4.5, z * 2.2))], lambda i: 1.0, 6)
    boxq(pt, c[0] + 4, c[1] + 4.5, c[2] - 1.2, c[0] + 7, c[1] + 6.4, c[2] + 1.2, 0.1)    # the Firewire port
    return M


# ============================================================================ SCP-1563: the "marker" on its stake
def marker():
    tex(noise_tex(128, (150, 120, 80), 12, 1.0, 70), PROPS, 's1563_stake.png')
    tp = noise_tex(64, (250, 100, 170), 8, 0.6, 71)
    d = ImageDraw.Draw(tp)
    for y in range(0, 64, 8):
        d.line([(0, y), (64, y)], fill=(255, 220, 236))                          # the tiny pale teeth
    tex(tp, PROPS, 's1563_tape.png')
    M = Model()
    st = M.surf('stake', 's1563_stake.png', shine=0.05)
    tp = M.surf('tape', 's1563_tape.png', shine=0.7, fx=16)
    boxq(st, -5, 0, -5, 5, 150, 5, 1 / 40.0)
    k = len(st.V)
    boxq(st, -5, 150, -5, 5, 158, 5, 1 / 40.0)
    # the coils round the stake, and one long tail hanging, a little lifted, as if waiting
    pts = [(7 * math.cos(t * 0.6), 104 + t * 1.2, 7 * math.sin(t * 0.6)) for t in range(0, 30)]
    tube(tp, pts, lambda i: (2.2, 0.5), 4)
    tail = [pts[-1], (10, 135, 4), (22, 128, 8), (28, 112, 10), (30, 96, 8), (31, 84, 6)]
    for i in range(len(tail) - 1):
        a, b = tail[i], tail[i + 1]
        quad(tp, (a[0], a[1], a[2] - 2.2), (b[0], b[1], b[2] - 2.2), (b[0], b[1], b[2] + 2.2), (a[0], a[1], a[2] + 2.2))
    return M


# ============================================================================ SCP-3743-A-1: the Way of branches
def way():
    tex(noise_tex(256, (82, 66, 48), 16, 1.0, 80), PROPS, 's3743_bark.png')
    ic = Image.new('RGB', (128, 192), (160, 120, 50))
    d = ImageDraw.Draw(ic)
    d.rectangle([8, 8, 120, 184], fill=(40, 34, 30))
    d.ellipse([44, 30, 84, 70], fill=(220, 180, 140))                            # Eros, winged, with a bow
    d.rectangle([52, 70, 76, 140], fill=(220, 180, 140))
    d.polygon([(52, 80), (14, 54), (24, 110)], fill=(240, 236, 220))
    d.polygon([(76, 80), (114, 54), (104, 110)], fill=(240, 236, 220))
    d.arc([20, 90, 108, 170], 200, 340, fill=(200, 160, 60), width=4)
    tex(ic, PROPS, 's3743_icon.png')
    M = Model()
    bk = M.surf('bark', 's3743_bark.png', shine=0.05)
    icn = M.surf('icon', 's3743_icon.png', shine=0.4, fx=16)
    for side in (-1, 1):                                                        # the two bent main branches
        for k in range(3):
            o = k * 7 - 7
            path = [(side * (100 + o), 0, o * 0.5), (side * (104 + o), 120, o), (side * (80 + o), 230, o * 0.7),
                    (side * (30 + o * 0.5), 280 + o, 0), (0, 286 + o, 0)]
            tube(bk, path, lambda i: (8 - k, 7 - k, 6 - k, 5 - k, 4 - k)[i] * 0.9, 8, vrep=1 / 80.0)
    for _ in range(30):                                                          # twigs and lashings
        t = RND.random()
        a = math.pi * t
        p = (-100 * math.cos(a) * (1.02), 286 * math.sin(a) ** 0.8, 0)
        q = add(p, (RND.uniform(-30, 30), RND.uniform(10, 40), RND.uniform(-20, 20)))
        tube(bk, [p, q], lambda i: (2.0, 0.6)[i], 5)
    for y in (60, 180):
        for side in (-1, 1):
            ring(bk, (side * 102, y, 0), 10, 1.2, 'y', 12, 5)
    tube(bk, [(40, 270, 0), (52, 236, 4)], lambda i: 0.4, 4)                   # the cord for the icon
    quad(icn, (40, 180, 4), (66, 180, 4), (66, 236, 4), (40, 236, 4))
    return M


# ============================================================================ SCP-4712: the vault door
def vaultdoor():
    st = noise_tex(256, (110, 116, 118), 10, 0.8, 90)
    tex(st, PROPS, 's4712_steel.png')
    M = Model()
    s = M.surf('steel', 's4712_steel.png', shine=0.8)
    gl = M.surf('glyph', 'indev_b33glyph.png', shine=0.5)
    yl = M.surf('yellow', 's1007_brass.png', shine=0.6)
    R0 = 150.0
    k = len(s.V)                                                                 # the frame: a square ring against the wall
    for (x0, y0, x1, y1) in ((-190, 0, -160, 340), (160, 0, 190, 340), (-190, 310, 190, 340), (-190, 0, 190, 20)):
        boxq(s, x0, y0, -12, x1, y1, 0, 1 / 80.0)
    c = (0.0, 165.0, -14.0)
    k = len(s.V)
    lathe(s, [(0, 0), (R0, 0), (R0, 12), (R0 - 10, 14), (0, 14)], 48, lambda i: i / 4.0)    # the leaf
    xform(s, k, lambda p: add(rot('x', -90)(p), c))
    k = len(gl.V)
    disc(gl, (c[0], c[1], c[2] - 14.2), R0 - 12, 'z', 48, -1)
    for i in range(len(gl.V) - (48 + 1) * 2, len(gl.V)):                       # planar uv
        v = gl.V[i]
        gl.V[i] = v[:9] + ((v[0] - c[0]) / (2 * R0) + 0.5, 1 - ((v[1] - c[1]) / (2 * R0) + 0.5))
    for b in range(16):                                                          # the bolt ring
        a = 2 * math.pi * b / 16
        p = (c[0] + math.cos(a) * (R0 - 18), c[1] + math.sin(a) * (R0 - 18), c[2] - 14)
        tube(s, [p, add(p, (0, 0, -6))], lambda i: 5, 8)
    tube(s, [(c[0], c[1], c[2] - 14), (c[0], c[1], c[2] - 40)], lambda i: 8, 12)   # the wheel spindle
    ring(s, (c[0], c[1], c[2] - 40), 46, 4, 'z', 32, 8)
    for a in range(0, 360, 60):
        x, y = math.cos(math.radians(a)) * 46, math.sin(math.radians(a)) * 46
        tube(s, [(c[0], c[1], c[2] - 40), (c[0] + x, c[1] + y, c[2] - 40)], lambda i: 2.5, 6)
    boxq(s, 150, 60, -60, 186, 270, -12, 1 / 80.0)                              # the hinge block
    for y in (90, 240):                                                          # the hydraulic rams
        tube(yl, [(186, y, -36), (240, y, -20), (300, y, -4)], lambda i: (9, 9, 6)[i], 10)
    return M


# ============================================================================ SCP-5079: the bed
def fungal():
    tex(noise_tex(128, (214, 196, 170), 14, 1.4, 100), PROPS, 's5079_fungus.png')
    tex(noise_tex(128, (200, 206, 214), 5, 1.0, 101), PROPS, 's5079_sheet.png')
    M = Model()
    fu = M.surf('fungus', 's5079_fungus.png', shine=0.3)
    sh = M.surf('sheet', 's5079_sheet.png', shine=0.2)
    ch = M.surf('chrome', 's3938_chrome.png', shine=1.0)
    for (x, z) in ((-95, -40), (95, -40), (95, 40), (-95, 40)):
        tube(ch, [(x, 0, z), (x, 60, z)], lambda i: 2.0, 8)
    boxq(ch, -100, 56, -44, 100, 62, 44, 0.05)
    boxq(sh, -96, 62, -40, 96, 72, 40, 1 / 60.0)
    tube(ch, [(-100, 62, -44), (-100, 110, -44), (-100, 110, 44), (-100, 62, 44)], lambda i: 2.2, 8)
    blob(fu, (-70, 84, 0), (11, 10, 9), rings=10, segs=14)                      # the head
    blob(fu, (-10, 80, 0), (46, 10, 20), e=0.8, rings=10, segs=16)
    for z in (-8, 8):
        tube(fu, [(30, 78, z), (88, 76, z * 1.2)], lambda i: 7, 10)
    rnd = random.Random(5079)
    for _ in range(46):                                                          # the tendrils, into everything
        a = (rnd.uniform(-80, 80), 80 + rnd.uniform(0, 8), rnd.uniform(-16, 16))
        side = rnd.choice((-1, 1))
        if rnd.random() < 0.5:
            b = (a[0] + rnd.uniform(-20, 20), 62, side * 44)
            c = (b[0] + rnd.uniform(-10, 10), rnd.uniform(0, 40), side * (46 + rnd.uniform(0, 30)))
        else:
            b = (a[0] + rnd.uniform(-30, 30), 90 + rnd.uniform(0, 20), a[2] + side * 20)
            c = (b[0] + rnd.uniform(-10, 10), 62, side * 40)
        tube(fu, [a, add(a, sub(b, a), 0.5), b, c], lambda i: (1.6, 1.2, 0.9, 0.5)[i], 5)
    return M


# ============================================================================ SCP-5267: the diorama
def diorama():
    tex(noise_tex(128, (120, 140, 70), 14, 1.0, 110), PROPS, 's5267_grass.png')
    M = Model()
    gr = M.surf('grass', 's5267_grass.png', shine=0.0)
    sto = M.surf('stone', 's4612_stone.png', shine=0.0)
    wd = M.surf('wood', 's1007_wood.png', shine=0.3)
    boxq(wd, -80, 0, -55, 80, 10, 55, 1 / 40.0)
    blob(gr, (10, 10, 0), (70, 26, 48), e=0.9, rings=10, segs=20)
    quad(gr, (-80, 10.1, 55), (80, 10.1, 55), (80, 10.1, -55), (-80, 10.1, -55))
    for (x0, z0, x1, z1) in ((-20, -24, 34, -20), (-20, 20, 34, 24), (-20, -24, -16, 24), (30, -24, 34, 4)):
        boxq(sto, x0, 30, z0, x1, 30 + RND.uniform(6, 14), z1, 1 / 20.0)
    for (x, z) in ((-60, -36), (-56, 34), (56, 36)):
        boxq(sto, x - 7, 10, z - 6, x + 7, 20, z + 6, 1 / 20.0)
    return M


# ============================================================================ items
def key1007():
    solid_tex(ITEMS, 's1007_key.png', (170, 140, 70), 10, 120)
    M = Model()
    b = M.surf('brass', 's1007_key.png', shine=1.0)
    ring(b, (0, 0, 0), 1.6, 0.35, 'z', 20, 6)
    for a in (45, 135, 225, 315):
        ring(b, (math.cos(math.radians(a)) * 1.6, math.sin(math.radians(a)) * 1.6, 0), 0.6, 0.2, 'z', 12, 5)
    tube(b, [(1.9, 0, 0), (6.5, 0, 0)], lambda i: 0.3, 8)
    boxq(b, 5.4, -1.2, -0.12, 6.5, 0, 0.12, 0.2)
    boxq(b, 4.6, -0.8, -0.12, 5.0, 0, 0.12, 0.2)
    return M


def drive4876():
    t = Image.new('RGB', (128, 64), (40, 40, 60))
    d = ImageDraw.Draw(t)
    cols = [(255, 80, 80), (80, 220, 80), (80, 140, 255), (250, 220, 60), (200, 80, 220)]
    for i in range(16):
        for j in range(8):
            if (i + j * 3) % 4 == 0:
                d.rectangle([i * 8, j * 8, i * 8 + 7, j * 8 + 7], fill=cols[(i + j) % 5])
    tex(t, ITEMS, 's4876_drive.png')
    M = Model()
    b = M.surf('body', 's4876_drive.png', shine=0.7)
    m = M.surf('metal', 's3938_chrome.png', shine=1.0)
    Image.open(os.path.join(PROPS, 's3938_chrome.png')).save(os.path.join(ITEMS, 's3938_chrome.png'))
    boxq(b, -2.6, 0, -1, 2.6, 0.8, 1, 0.2)
    boxq(m, 2.6, 0.15, -0.6, 4.0, 0.65, 0.6, 0.2)
    return M


def book4890():
    cv = Image.new('RGB', (256, 320), (100, 40, 150))
    d = ImageDraw.Draw(cv)
    d.text((128, 50), "DR. WONDERTAINMENT'S", font=F(18), fill=(255, 220, 120), anchor='mm')
    d.text((128, 90), 'GUIDE TO', font=F(30), fill=(255, 255, 255), anchor='mm')
    d.text((128, 128), 'HISTORY', font=F(36), fill=(255, 255, 255), anchor='mm')
    d.text((128, 230), 'W', font=F(120), fill=(255, 200, 60), anchor='mm')
    tex(cv, ITEMS, 's4890_cover.png')
    solid_tex(ITEMS, 's4890_pages.png', (240, 236, 220), 5, 130)
    M = Model()
    c = M.surf('cover', 's4890_cover.png', shine=0.6)
    p = M.surf('pages', 's4890_pages.png', shine=0.1)
    boxq(p, -10.5, 0.2, -13.5, 10.5, 2.6, 13.5, 0.1)
    quad(c, (-11, 2.8, -14), (11, 2.8, -14), (11, 2.8, 14), (-11, 2.8, 14))
    quad(c, (-11, 0, 14), (11, 0, 14), (11, 0, -14), (-11, 0, -14), (0, 0, 0.05, 0.05))
    boxq(c, -11.4, 0, -14, -10.5, 2.8, 14, 0.01)
    return M


def zapper232():
    tin = noise_tex(128, (200, 60, 50), 8, 0.8, 140)
    tex(tin, ITEMS, 's232_tin.png')
    solid_tex(ITEMS, 's232_silver.png', (200, 204, 210), 8, 141)
    solid_tex(ITEMS, 's232_bulb.png', (255, 60, 40), 6, 142)
    M = Model()
    t = M.surf('tin', 's232_tin.png', shine=0.9)
    sv = M.surf('silver', 's232_silver.png', shine=1.0)
    bu = M.surf('bulb', 's232_bulb.png', fx=1, shine=1.0)
    k = len(t.V)
    lathe(t, [(0, 0), (2.4, 0), (2.8, 4), (2.2, 9), (1.6, 14), (1.2, 18), (0, 18)], 24, lambda i: i / 6.0)
    xform(t, k, lambda p: (p[1] - 6, p[0] + 9, p[2]))
    for x in (0.0, 4.0, 8.0):
        ring(sv, (x, 9, 0), 2.6 - x * 0.12, 0.5, 'x', 20, 6)
    for a in (0, 120, 240):                                                      # the fins
        k = len(sv.V)
        boxq(sv, -6, 0, -0.15, 0, 4, 0.15, 0.1)
        xform(sv, k, lambda p, a=a: add(rot('x', a)((p[0], p[1] + 2, p[2])), (0, 9, 0)))
    blob(bu, (12.4, 9, 0), (0.9, 0.9, 0.9), rings=6, segs=10)
    tube(t, [(-2, 7, 0), (-3.5, 3, 0), (-4, 0, 0)], lambda i: (1.5, 1.4, 1.3)[i], 10)
    tube(sv, [(-0.5, 7, 0), (0.5, 4.8, 0), (-1.5, 4.0, 0)], lambda i: 0.3, 6)
    return M


def gun865():
    solid_tex(ITEMS, 's865_steel.png', (78, 80, 86), 6, 150)
    solid_tex(ITEMS, 's865_grip.png', (46, 44, 42), 10, 151)
    tg = Image.new('RGB', (128, 64), (250, 240, 160))
    d = ImageDraw.Draw(tg)
    d.text((64, 20), 'NON-FUNCTIONAL', font=F(14), fill=(160, 20, 20), anchor='mm')
    d.text((64, 44), 'DO NOT USE', font=F(14), fill=(30, 30, 30), anchor='mm')
    tex(tg, ITEMS, 's865_tag.png')
    M = Model()
    s = M.surf('steel', 's865_steel.png', shine=0.9)
    g = M.surf('grip', 's865_grip.png', shine=0.3)
    tg = M.surf('tag', 's865_tag.png', fx=16)
    boxq(s, -2, 10, -1.5, 19, 13.5, 1.5, 0.2)                                    # slide
    for x in range(0, 6):
        boxq(s, -1.6 + x * 0.7, 13.5, -1.4, -1.3 + x * 0.7, 13.6, 1.4, 0.2)
    boxq(s, 0, 8, -1.3, 17, 10, 1.3, 0.2)                                        # frame
    tube(s, [(19, 11.8, 0), (19.4, 11.8, 0)], lambda i: 0.6, 8)
    k = len(g.V)
    boxq(g, -2.4, -2, -1.6, 4.0, 8.2, 1.6, 0.2)                                  # grip, raked
    xform(g, k, lambda p: rot('z', 14, (1, 8, 0))(p))
    tube(s, [(5, 8, 0), (7, 5.2, 0), (11, 5.2, 0), (12, 8, 0)], lambda i: 0.35, 6)   # trigger guard
    tube(s, [(7.5, 8, 0), (7.8, 6.4, 0)], lambda i: 0.4, 6)
    tube(tg, [(6, 5.2, 0), (6.4, 2, 0.5)], lambda i: 0.08, 4)
    quad(tg, (4.4, -2, 0.6), (8.4, -2, 0.6), (8.4, 0.2, 0.6), (4.4, 0.2, 0.6))
    return M


def coin762():
    for name, side in (('s762_heads.png', 'heads'),):
        im = Image.new('RGB', (128, 128), (196, 198, 200))
        d = ImageDraw.Draw(im)
        d.ellipse([4, 4, 124, 124], outline=(150, 150, 152), width=4)
        d.ellipse([34, 24, 94, 96], fill=(170, 172, 176))                        # a profile, worn
        d.ellipse([70, 40, 96, 64], fill=(196, 198, 200))
        d.text((64, 108), '1968', font=F(16), fill=(120, 120, 124), anchor='mm')
        d.text((64, 16), 'LIBERTY', font=F(12), fill=(120, 120, 124), anchor='mm')
        tex(im, ITEMS, name)
    M = Model()
    h = M.surf('heads', 's762_heads.png', shine=1.0)
    r = M.surf('rim', 's3938_chrome.png', shine=1.0)
    lathe(r, [(1.21, 0), (1.21, 0.18)], 40, lambda i: i)
    for y, f in ((0.18, 1), (0.0, -1)):                                          # heads on both faces (fans)
        base = len(h.V)
        h.V.append((0, y, 0, 0, f, 0, 1, 1, 1, 0.5, 0.5))
        for j in range(41):
            a = 2 * math.pi * j / 40
            x, z = 1.21 * math.cos(a), 1.21 * math.sin(a)
            h.V.append((x, y, z, 0, f, 0, 1, 1, 1, x / 2.42 + 0.5, 1 - (z * f / 2.42 + 0.5)))
        for j in range(40):
            a, b = base + 1 + j, base + 2 + j
            h.T.append((base, b, a) if f > 0 else (base, a, b))
    return M


def case667():
    tex(noise_tex(128, (90, 60, 38), 10, 1.0, 160), ITEMS, 's667_wood.png')
    solid_tex(ITEMS, 's667_glass.png', (210, 230, 230), 4, 161)
    tex(noise_tex(64, (60, 44, 30), 10, 0.8, 162), ITEMS, 's667_chitin.png')
    solid_tex(ITEMS, 's667_wing.png', (220, 220, 200), 6, 163)
    solid_tex(ITEMS, 's667_glow.png', (200, 255, 120), 10, 164)
    lb = Image.new('RGB', (128, 32), (240, 236, 220))
    ImageDraw.Draw(lb).text((64, 16), 'SCP-667-2', font=F(16), fill=(30, 30, 30), anchor='mm')
    tex(lb, ITEMS, 's667_label.png')
    M = Model()
    w = M.surf('wood', 's667_wood.png', shine=0.4)
    g = M.surf('glass', 's667_glass.png', fx=16, alpha=0.25, shine=1.0)
    c = M.surf('chitin', 's667_chitin.png', shine=0.8)
    wg = M.surf('wing', 's667_wing.png', fx=16, alpha=0.6)
    gl = M.surf('glow', 's667_glow.png', fx=1)
    lb = M.surf('label', 's667_label.png')
    boxq(w, -7, 0, -5, 7, 1.2, 5, 0.2)
    quad(lb, (-4, 0.3, -5.01), (4, 0.3, -5.01), (4, 0.9, -5.01), (-4, 0.9, -5.01))
    for f in range(4):
        k = len(g.V)
        a, b = (7, 5) if f % 2 == 0 else (5, 7)
        quad(g, (-a, 1.2, -b), (a, 1.2, -b), (a, 7, -b), (-a, 7, -b))
        xform(g, k, rot('y', f * 90))
    quad(g, (-7, 7, 5), (7, 7, 5), (7, 7, -5), (-7, 7, -5))
    # the remains: a 7.5 cm firefly-like body shaped like a tiny person, wings spread, pinned
    y = 1.4
    blob(c, (0, y + 0.4, 0.6), (0.8, 0.45, 1.4), rings=8, segs=10)               # torso
    blob(c, (0, y + 0.4, 2.4), (0.55, 0.45, 0.6), rings=8, segs=10)              # head
    for x in (-0.5, 0.5):
        tube(c, [(x * 0.6, y + 0.3, -0.6), (x * 1.2, y + 0.3, -2.6), (x * 1.4, y + 0.3, -3.6)], lambda i: 0.28, 6)
        tube(c, [(x * 1.4, y + 0.4, 1.4), (x * 3.0, y + 0.4, 0.6), (x * 3.4, y + 0.4, -0.4)], lambda i: 0.2, 6)
        blob(gl, (x * 1.3, y + 0.35, -3.0), (0.3, 0.25, 0.5), rings=4, segs=6)
        quad(wg, (0, y + 0.8, 1.6), (x * 8, y + 0.8, 1.0) if x > 0 else (0, y + 0.8, -2.0),
             (x * 7, y + 0.8, -2.6) if x > 0 else (x * 7, y + 0.8, -2.6), (0, y + 0.8, -2.0) if x > 0 else (x * 8, y + 0.8, 1.0))
    tube(M.surf('pin', 's3938_chrome.png', shine=1.0), [(0, y - 0.2, 0.6), (0, y + 2.6, 0.6)], lambda i: 0.08, 4)
    return M


def book7042():
    lt = noise_tex(256, (92, 56, 34), 14, 1.0, 170)
    d = ImageDraw.Draw(lt)
    for _ in range(30):
        x, y = RND.randrange(256), RND.randrange(256)
        d.line([(x, y), (x + RND.randint(-40, 40), y + RND.randint(-6, 6))], fill=(60, 34, 20), width=2)
    tex(lt, ITEMS, 's7042_leather.png')
    tex(noise_tex(64, (230, 226, 210), 6, 0.8, 171), ITEMS, 's7042_pages.png')
    tex(noise_tex(64, (230, 226, 216), 20, 0.4, 172), ITEMS, 's7042_birch.png')
    M = Model()
    l = M.surf('leather', 's7042_leather.png', shine=0.3)
    p = M.surf('pages', 's7042_pages.png', shine=0.1)
    b = M.surf('birch', 's7042_birch.png', shine=0.2)
    boxq(p, -10, 0.3, -14, 10.2, 1.9, 14, 0.1)
    boxq(l, -10.4, 1.9, -14.4, 10.6, 2.3, 14.4, 0.05)
    boxq(l, -10.4, 0, -14.4, 10.6, 0.3, 14.4, 0.05)
    boxq(l, -11, 0, -14.4, -10.4, 2.3, 14.4, 0.05)
    tube(b, [(-6, 2.8, -10), (6, 2.8, 10)], lambda i: 0.4, 8)
    tube(M.surf('lead', 's3938_tyre.png'), [(6, 2.8, 10), (6.6, 2.8, 11)], lambda i: (0.4, 0.05)[i], 6)
    return M


if __name__ == '__main__':
    # the shared textures some models reuse from another folder
    PROP_MODELS = (('scp3938', bike), ('scp1007', coffin), ('scp696', typewriter), ('scp252', bomb),
                   ('scpl043', turntable), ('scp4612', cadaver), ('scp2394', frog), ('scp2394f', frogonly), ('scp1563', marker),
                   ('scp3743', way), ('scp4712', vaultdoor), ('scp5079', fungal), ('scp5267', diorama))
    ITEM_MODELS = (('key1007', key1007), ('drive4876', drive4876), ('book4890', book4890), ('zapper232', zapper232),
                   ('gun865', gun865), ('coin762', coin762), ('case667', case667), ('book7042', book7042))
    out = {}
    for name, fn in PROP_MODELS:
        m = fn()
        m.write(os.path.join(PROPS, name + '.b3d'))
        out[name] = (m, PROPS)
        print('%-10s %6d triangles' % (name, m.tris()))
    Image.open(os.path.join(PROPS, 's3938_tyre.png')).save(os.path.join(ITEMS, 's3938_tyre.png'))
    from make_assets5 import MAPDIR
    Image.open(os.path.join(MAPDIR, 'indev_b33glyph.png')).save(os.path.join(PROPS, 'indev_b33glyph.png'))
    for name, fn in ITEM_MODELS:
        m = fn()
        m.write(os.path.join(ITEMS, name + '.b3d'))
        out[name] = (m, ITEMS)
        print('%-10s %6d triangles' % (name, m.tris()))
    views = {'scp3938': ((170, 170, -220), (0, 70, 0)), 'scp1007': ((150, 180, -230), (0, 25, 0)),
             'scp696': ((40, 50, -60), (0, 12, 0)), 'scp252': ((200, 140, -260), (0, 34, 0)),
             'scpl043': ((40, 50, -55), (0, 8, 0)), 'scp4612': ((600, 520, -760), (0, 90, 0)),
             'scp2394': ((70, 70, -110), (0, 22, 0)), 'scp2394f': ((14, 14, -20), (0, 4, 0)), 'scp1563': ((90, 150, -160), (0, 100, 0)),
             'scp3743': ((260, 200, -420), (0, 150, 0)), 'scp4712': ((180, 260, -420), (0, 165, 0)),
             'scp5079': ((170, 190, -230), (0, 60, 0)), 'scp5267': ((120, 140, -170), (0, 20, 0)),
             'key1007': ((3, 7, -9), (3, 0, 0)), 'drive4876': ((4, 6, -7), (0.6, 0.4, 0)),
             'book4890': ((14, 30, -26), (0, 1, 0)), 'zapper232': ((6, 18, -26), (3, 7, 0)),
             'gun865': ((22, 18, -40), (8, 6, 0)), 'coin762': ((1.5, 3.5, -3.0), (0, 0, 0)),
             'case667': ((8, 14, -14), (0, 3, 0)), 'book7042': ((14, 28, -24), (0, 1, 0))}
    tiles = []
    for name, (m, folder) in out.items():
        eye, look = views[name]
        tiles.append(render(m, folder, eye, look, size=(320, 320), fov=45, bg=(30, 30, 34)))
    cols = 5
    sheet = Image.new('RGB', (320 * cols, 320 * ((len(tiles) + cols - 1) // cols)))
    for i, t in enumerate(tiles):
        sheet.paste(t, ((i % cols) * 320, (i // cols) * 320))
    sheet.save(os.path.join(PREV, 'hd33_models.png'))
    for name, _ in ITEM_MODELS:
        m, folder = out[name]
        eye, look = views[name]
        render(m, folder, eye, look, size=(256, 256), fov=45, bg=(0, 0, 0)).resize((64, 64), Image.LANCZOS).save(
            os.path.join(ITEMS, 'INV%s.png' % name))
    print('previews and icons written')
