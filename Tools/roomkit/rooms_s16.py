"""Ten containment rooms for sixteen SCPs (the "s16" batch).

  room2siv       LCZ    Small Items Vault            SCP-1045, SCP-1510, SCP-1125
  room2bio       LCZ    Biological Holding           SCP-1513, SCP-1515, SCP-1517, SCP-1519
  room2origin    HCZ    Procedure 1512-Alpha hall    SCP-1512
  room2purge     HCZ    foam-lined fan hall          SCP-1518
  room2review    EZ     Surveillance Review          SCP-1110, SCP-1250
  room2lecture   EZ     Lecture Room 2               SCP-1313
  room2site41    Indev  a section of Site 41         SCP-1312
  room2cell49    Indev  Humanoid Cell 49             SCP-1516
  room2vault117  Indev  Vault 117 (lift down)        SCP-1511
  room2bunker    Indev  Secure Bunker (lift down)    SCP-1514

Each function returns (Room, key, description, zone, set-room position, view).  Everything the game
code needs a handle on is recorded by name (named / ndoor / reserve) and gen_s16.py turns the names
into r\\Objects[] / r\\RoomDoors[] slots and Blitz constants, so IndevS16.bb never holds a coordinate."""
import random
from v02kit import *

DEEP = -704.0
NS3 = ((0, -600), (0, 0), (0, 600))
LABELS = json.load(open(os.path.join(HERE, 'labels3.json')))
PLATES = json.load(open(os.path.join(HERE, 'plates3.json')))
LAB3 = Mat('indev_labels3.png', cast=False)
PLT3 = Mat('indev_plates3.png', cast=False)
BRONZE = Mat('indev_bronze.png', 128)
STONEM = Mat('indev_stone.png', 256)
WAXP = Mat('indev_waxpaper.png', 128, cast=False)
FLESH = Mat('indev_flesh.png', 96)
FOAMW = Mat('indev_foam.png', 256)
ROOT = Mat('indev_root.png', 96)
SOILM = Mat('indev_soil.png', 128)
TERRA = Mat('indev_terracotta.png', 128)
CANDYM = Mat('indev_candy.png', 96)
DICEM = Mat('indev_dice.png', cast=False)
CRYSTAL = Mat('indev_crystal.png', 96, emit=215, cast=False)
WATER = Mat('indev_crystal.png', 220)
BOARDM = Mat('indev_board1313.png', cast=False)
CARDSM = Mat('indev_cards.png', cast=False)
WORDSM = Mat('indev_words.jpg', 256)
TAPEM = Mat('indev_tape.png', cast=False)
WHITE = Mat('white.jpg', 256)
STYLES['foam'] = (FOAMW, CONC, DIRTY)


def R_(name, amb=11):
    return Room(name, luxel=12, ambient=amb, fill=0.14)


def lamps(R, pts, ch, **kw):
    for (x, z) in pts:
        lamp(R, x, z, ch, **kw)


def red_lamp(R, x, z, ceil_y, power=120, rng=780):
    R.box(x - 14, ceil_y - 20, z - 14, x + 14, ceil_y, z + 14, REDLAMP, skip='T')
    R.light(x, ceil_y - 50, z, rng=rng, color=(255, 56, 44), power=power)


# --------------------------------------------------------------------- what the game code is told
def named(R, name, x, y, z):
    """A pivot the code finds as r\\Objects[S16_<KEY>_<name>]."""
    R.spawns.append(dict(kind='named', name=name, pos=(x, y, z)))


def reserve(R, name, n=1):
    """n free r\\Objects[] slots for things IndevS16.bb creates itself; the constant is the first."""
    R.spawns.append(dict(kind='reserve', name=name, n=n))


def ndoor(R, name, x, y, z, angle, key=0, locked=False):
    """A door the code keeps as r\\RoomDoors[S16_<KEY>_D_<name>]."""
    R.spawns.append(dict(kind='ndoor', name=name, pos=(x, y, z), angle=angle, key=key, locked=locked))


def annex2(R, axis, plane, sign, a0, a1, depth, h, style, door=None, key=0, jamb=64.0, extra=None):
    """annex() that can also cut holes in its other walls.  extra = {segment: [(s0, s1, y0, y1)]};
    segments: 0 west (from z0), 1 north (from x0), 2 east (from z1), 3 south (from x1)."""
    wallm, floorm, ceilm = STYLES[style]
    near = plane + sign * jamb
    far = near + sign * depth
    lo, hi = sorted((near, far))
    if axis == 'x':
        x0, x1, z0, z1 = lo, hi, a0, a1
    else:
        x0, x1, z0, z1 = a0, a1, lo, hi
    WM = wmat(style, h)

    def P(c, d):
        return (d, c) if axis == 'x' else (c, d)
    seg = {('x', 1): 0, ('x', -1): 2, ('z', 1): 3, ('z', -1): 1}[(axis, sign)]
    out = [(x0, z0), (x0, z1), (x1, z1), (x1, z0)]
    holes = {k: list(v) for k, v in (extra or {}).items()}
    c0, c1 = door - 96.0, door + 96.0
    holes.setdefault(seg, []).append(span(out[seg], P(c0, near), P(c1, near)) + (0.0, 320.0))
    R.walls(out, 0, h, WM, holes=holes)
    R.rect_floor(x0, z0, x1, z1, 0, floorm)
    R.rect_ceil(x0, z0, x1, z1, h, ceilm)
    pa, pb = sorted((plane, near))
    q = [P(c0, pa), P(c1, pa), P(c1, pb), P(c0, pb)]
    poly_facing(R, [V(p[0], 0, p[1]) for p in q], (0, 1, 0), floorm)
    poly_facing(R, [V(p[0], 320, p[1]) for p in q], (0, -1, 0), WM)
    for (c, s) in ((c0, 1), (c1, -1)):
        e0, e1 = P(c, pa), P(c, pb)
        hint = (0, 0, s) if axis == 'x' else (s, 0, 0)
        poly_facing(R, [V(e0[0], 0, e0[1]), V(e1[0], 0, e1[1]), V(e1[0], 320, e1[1]), V(e0[0], 320, e0[1])], hint, WM)
    dp = P(door, plane + sign * jamb / 2)
    ang = 90 if axis == 'x' else 0
    R.door_marker(dp[0], 0, dp[1], ang)
    R.spawns.append(dict(kind='door', pos=(dp[0], 0, dp[1]), angle=ang, key=key))
    return (x0, z0, x1, z1)


# --------------------------------------------------------------------- small geometry
def label(R, num, cx, cz, facing, yc=210.0, size=76.0):
    wall_decal(R, LAB3, cx, cz, facing, size, size, yc, uv=LABELS[num])


def plate(R, key, cx, cz, facing, yc=352.0, w=200.0, h=40.0):
    wall_decal(R, PLT3, cx, cz, facing, w, h, yc, uv=PLATES[key])


def signboard(R, num, x, z, facing, y=0.0):
    """A label on a post, for places where the walls are busy."""
    R.box(x - 3, y, z - 3, x + 3, y + 112, z + 3, DIRTY, skip='TB', lux=12)
    if facing in 'NS':
        R.box(x - 42, y + 112, z - 3, x + 42, y + 196, z + 3, DIRTY, lux=12)
        label(R, num, x, z + (3 if facing == 'N' else -3), facing, yc=y + 154)
    else:
        R.box(x - 3, y + 112, z - 42, x + 3, y + 196, z + 42, DIRTY, lux=12)
        label(R, num, x + (3 if facing == 'E' else -3), z, facing, yc=y + 154)


def plinth(R, x, z, y=0.0, h=90.0, s=34.0):
    R.box(x - s, y, z - s, x + s, y + h, z + s, STYLES['std'][0].but(us=4 * s, vs=h, v0=y + h), skip='B', top=DARK, lux=10)
    R.box(x - s - 5, y, z - s - 5, x + s + 5, y + 12, z + s + 5, DARK, skip='B', lux=10)
    return y + h


def flat(R, x0, z0, x1, z1, y, mat, rect=(0, 0, 1, 1), bottom='S', **kw):
    """A picture lying flat; `bottom` is the side its lower edge is on (where the reader stands)."""
    c = {'S': ((x0, z0), (x1, z0), (x1, z1), (x0, z1)), 'N': ((x1, z1), (x0, z1), (x0, z0), (x1, z0)),
         'W': ((x0, z1), (x0, z0), (x1, z0), (x1, z1)), 'E': ((x1, z0), (x1, z1), (x0, z1), (x0, z0))}[bottom]
    kw.setdefault('cast', False)
    kw.setdefault('lux', 8)
    R.quad(*[V(p[0], y, p[1]) for p in c], mat, uvrect=rect, **kw)


def tbox(R, x0, y0, z0, x1, y1, z1, mat, rect=(0, 0, 1, 1), top=None, lux=8):
    """A small box showing the same picture on every side."""
    for (a, b) in (((x0, z0), (x1, z0)), ((x1, z0), (x1, z1)), ((x1, z1), (x0, z1)), ((x0, z1), (x0, z0))):
        R.quad(V(a[0], y0, a[1]), V(b[0], y0, b[1]), V(b[0], y1, b[1]), V(a[0], y1, a[1]), mat, uvrect=rect, lux=lux)
    flat(R, x0, z0, x1, z1, y1, mat, top or rect, lux=lux, cast=True)


def ball(R, c, r, mat, seg=6, rings=3, top_only=False, lux=24, **kw):
    cx, cy, cz = c

    def P(a, b):
        return V(cx + r * math.cos(a) * math.cos(b), cy + r * math.sin(a), cz + r * math.cos(a) * math.sin(b))
    for j in range(0 if top_only else -rings, rings):
        a0, a1 = (math.pi / 2) * j / rings, (math.pi / 2) * (j + 1) / rings
        for i in range(seg):
            b0, b1 = 2 * math.pi * i / seg, 2 * math.pi * (i + 1) / seg
            pts = [P(a0, b0), P(a0, b1), P(a1, b1), P(a1, b0)]
            if j == rings - 1:
                pts = pts[:3]
            elif j == -rings:
                pts = pts[1:]
            am, bm = (a0 + a1) / 2, (b0 + b1) / 2
            poly_facing(R, pts, (math.cos(am) * math.cos(bm), math.sin(am), math.cos(am) * math.sin(bm)), mat, lux=lux, **kw)


def octo(cx, cz, r, n=8):
    return [(cx + r * math.cos(2 * math.pi * i / n + math.pi / n), cz + r * math.sin(2 * math.pi * i / n + math.pi / n)) for i in range(n)]


def open_cabinet(R, x0, y0, z0, x1, y1, z1, mat, open_side='N', t=6.0, lux=12):
    R.box(x0, y0, z0, x1, y0 + t, z1, mat, skip='B', lux=lux)
    R.box(x0, y1 - t, z0, x1, y1, z1, mat, lux=lux)
    if open_side != 'W':
        R.box(x0, y0 + t, z0, x0 + t, y1 - t, z1, mat, skip='TB', lux=lux)
    if open_side != 'E':
        R.box(x1 - t, y0 + t, z0, x1, y1 - t, z1, mat, skip='TB', lux=lux)
    if open_side != 'S':
        R.box(x0 + t, y0 + t, z0, x1 - t, y1 - t, z0 + t, mat, skip='TBEW', lux=lux)
    if open_side != 'N':
        R.box(x0 + t, y0 + t, z1 - t, x1 - t, y1 - t, z1, mat, skip='TBEW', lux=lux)


def lantern(R, x, y, z):
    """SCP-1045: a square wooden lantern, 15 x 15 x 32 cm, waxed-paper sides."""
    R.box(x - 19, y, z - 19, x + 19, y + 6, z + 19, WOOD, skip='B', lux=8)
    R.box(x - 19, y + 76, z - 19, x + 19, y + 82, z + 19, WOOD, lux=8)
    for (dx, dz) in ((-19, -19), (16, -19), (-19, 16), (16, 16)):
        R.box(x + dx, y + 6, z + dz, x + dx + 3, y + 76, z + dz + 3, WOOD, skip='TB', lux=8)
    R.box(x - 17, y + 6, z - 17, x + 17, y + 76, z + 17, WAXP, skip='TB', lux=8, cast=False)
    R.tube((x, y + 82, z), (x, y + 92, z), 3, DIRTY, sides=5, lux=16)


def helmet(R, x, y, z):
    """SCP-1510: a bronze infantry helmet on a stand, facing -x."""
    R.tube((x, y, z), (x, y + 34, z), 4, DIRTY, sides=6, lux=16)
    ball(R, (x, y + 34, z), 30, BRONZE, seg=8, rings=3, top_only=True, lux=10)
    R.box(x - 8, y + 8, z - 31, x + 12, y + 34, z - 28, BRONZE, lux=10)
    R.box(x - 8, y + 8, z + 28, x + 12, y + 34, z + 31, BRONZE, lux=10)
    R.box(x + 26, y + 26, z - 22, x + 40, y + 30, z + 22, BRONZE, lux=10)
    R.tube((x, y + 63, z), (x, y + 74, z), 4, BRONZE, sides=6, caps=True, lux=16)


def crystal(R, x, y, z):
    ring = octo(x, z, 20, 6)
    R.prism(ring, y, y + 62, CRYSTAL, caps='', lux=12)
    apex = V(x + 5, y + 112, z - 3)
    for i in range(6):
        a, b = ring[i], ring[(i + 1) % 6]
        mid = ((a[0] + b[0]) / 2 - x, 0.4, (a[1] + b[1]) / 2 - z)
        poly_facing(R, [V(a[0], y + 62, a[1]), V(b[0], y + 62, b[1]), apex], mid, CRYSTAL, lux=12)


def fountain(R, x, z):
    """SCP-1518: a dead limestone fountain 1.8 m tall, in its foam shell."""
    R.prism(octo(x, z, 150), 0, 22, FOAMW, caps='T', lux=14)
    R.prism(octo(x, z, 112), 22, 60, STONEM, caps='T', lux=14)
    R.tube((x, 60, z), (x, 250, z), 34, STONEM.but(us=214, vs=256), sides=8, lux=16)
    R.prism(octo(x, z, 128), 250, 292, STONEM, caps='TB', lux=14)
    R.floor(octo(x, z, 110), 293, WATER, cast=False, coll=False)
    R.tube((x, 292, z), (x, 400, z), 18, STONEM.but(us=113, vs=256), sides=8, lux=16)
    R.prism(octo(x, z, 58), 400, 424, STONEM, caps='TB', lux=14)
    R.floor(octo(x, z, 46), 425, WATER, cast=False, coll=False)
    ball(R, (x, 446, z), 20, STONEM, seg=6, rings=2, lux=20)


def tendril(R, pts, r):
    m = ROOT.but(us=2 * math.pi * r, vs=96)
    # round the corners off: a Catmull-Rom curve through the points, three pieces to a span
    P = [pts[0]] + list(pts) + [pts[-1]]
    smooth = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for k in range(3):
            t = k / 3.0
            smooth.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t
                                 + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    smooth.append(pts[-1])
    pts = smooth
    for a, b in zip(pts[:-1], pts[1:]):
        R.tube(a, b, r, m, sides=5, coll=False, lux=30)


# =====================================================================  LCZ
def room2siv():
    R = R_('room2siv')
    junction(R, 'NS', 'old', openings={'hubE': [door_op(0)]})
    x0, z0, x1, z1 = annex(R, 'x', 192, +1, -448, 448, 576, 352, 'std', door=0, key=2)
    plate(R, 'siv', 192, 0, 'W')
    for num, z in (('1045', -280), ('1510', 0), ('1125', 280)):
        label(R, num, x1, z, 'W', yc=224)
    top = plinth(R, 770, -280)
    lantern(R, 770, top, -280)
    named(R, 'LANTERN', 770, top + 41, -280)
    reserve(R, 'GLOW')
    top = plinth(R, 770, 0)
    helmet(R, 770, top, 0)
    named(R, 'HELMET', 770, top + 40, 0)
    top = table(R, 730, 240, 810, 320)
    tbox(R, 762, top, 272, 780, top + 18, 290, DICEM, (0.01, 0.02, 0.32, 0.63), top=(0.67, 0.02, 0.985, 0.63))
    flat(R, 736, 250, 758, 306, top + 0.7, DICEM, (0.0, 0.68, 1.0, 1.0), bottom='W')
    named(R, 'DICE', 771, top + 12, 281)
    crate(R, 690, 0, 392, yaw=18)
    t = shelf_unit(R, 262, 220, 326, 440, 0, height=230, levels=4)
    ceil_fan(R, 500, -230, 352)
    ceil_light(R, 544, 0, 352, size=72, power=120, rng=900)
    R.light(700, 250, -280, rng=420, color=(255, 236, 200), power=40, ent=False)
    R.light(700, 250, 280, rng=420, color=(255, 236, 200), power=40, ent=False)
    lamps(R, NS3, 384, power=86)
    item(R, 'doc1045', 690, 0, -280)
    item(R, 'doc1510', 690, 0, 0)
    item(R, 'doc1125', 690, 0, 230)
    item(R, 'doc1045b', 294, t[1], 260)
    item(R, 'doc1510b', 294, t[1], 330)
    item(R, 'doc1125b', 294, t[1], 400)
    item(R, 'bat', 294, t[2], 300, 60)
    item(R, 'eyedrops', 294, t[2], 380, 40)
    return (R, 'SIV', 'Small Items Vault (Indev). SCP-1045 the candle lantern, SCP-1510 the helmet, SCP-1125 the answer dice.',
            1, 0.3, ((330, 165, -330), (780, 110, 60)))


def room2bio():
    R = R_('room2bio')
    junction(R, 'NS', 'lab', openings={'hubE': [door_op(0)]})
    x0, z0, x1, z1 = annex(R, 'x', 192, +1, -640, 640, 640, 352, 'lab', door=0, key=1)
    plate(R, 'bio', 192, 0, 'W')
    # SCP-1515: wire enclosure, soil floor
    cage(R, 520, 350, 890, 634)
    R.box(522, 0, 352, 888, 6, 632, SOILM, skip='B', lux=14)
    named(R, 'RODENTS', 705, 6, 492)
    reserve(R, 'ROD', 5)
    signboard(R, '1515', 462, 330, 'S')
    # SCP-1513: three pots in a soil tray; the middle one is the pet (a model, with its own pot)
    R.box(286, 0, 230, 366, 10, 560, DIRTY, skip='B', top=SOILM, lux=12)
    R.prism(octo(326, 280, 24), 10, 40, TERRA, caps='T', top=SOILM, lux=12)
    R.tube((326, 40, 280), (331, 96, 287), 2.5, ROOT, sides=5, coll=False, lux=30)
    R.prism(octo(326, 510, 24), 10, 34, TERRA, caps='T', top=DARK, lux=12)
    R.floor(octo(392, 516, 38), 1.2, SOILM, cast=False, coll=False)
    named(R, 'PET', 326, 10, 395)
    reserve(R, 'PETM')
    for i, (x, z) in enumerate(((440, 606), (866, -300), (292, -606), (866, 252))):
        named(R, 'FERAL%d' % i, x, 0, z)
    reserve(R, 'FERALM')
    label(R, '1513', 256, 395, 'E', yc=214)
    # SCP-1519: saline tank and the cradle on a bench
    top = desk(R, 806, -160, 890, 160, 0)
    R.box(820, top, -120, 880, top + 4, -20, DARK, skip='B', lux=10)
    R.box(822, top + 4, -118, 878, top + 56, -22, GLASS, skip='B', lm=False, coll=False)
    R.box(820, top + 56, -120, 880, top + 60, -20, DARK, lux=10)
    R.tube((850, top + 24, -100), (850, top + 24, -40), 11, FLESH, sides=8, caps=True, coll=False, lux=20)
    R.box(832, top, 50, 872, top + 12, 96, DARK, skip='B', lux=10)
    R.box(846, top + 12, 58, 858, top + 20, 64, DIRTY, skip='B', lux=10)
    R.box(846, top + 12, 82, 858, top + 20, 88, DIRTY, skip='B', lux=10)
    named(R, 'CRADLE', 852, top + 20, 73)
    label(R, '1519', x1, -70, 'W', yc=200)
    # SCP-1517: an upright freezer left ajar (the door itself is made by the game code, on its hinge)
    open_cabinet(R, 700, 0, -634, 860, 230, -548, WHITE, 'N')
    for y in (70, 130, 190):
        R.box(706, y - 5, -628, 854, y, -552, WHITE, top=CANDYM, lux=12)
    for (bx, by, bz) in ((730, 76, -590), (790, 76, -575), (826, 136, -596), (748, 136, -580), (800, 196, -590)):
        ball(R, (bx, by, bz), 6, CANDYM, seg=5, rings=2, lux=30, coll=False)
    named(R, 'HINGE', 700, 115, -548)
    named(R, 'CANDY', 780, 140, -584)
    reserve(R, 'SLAB')
    signboard(R, '1517', 640, -566, 'N')
    ceil_fan(R, 480, -250, 352)
    ceil_light(R, 576, 0, 352, size=80, power=124, rng=900, color=(245, 250, 255))
    ceil_light(R, 600, 430, 352, size=56, power=84, rng=760, color=(245, 250, 255))
    ceil_light(R, 560, -430, 352, size=56, power=84, rng=760, color=(245, 250, 255))
    lamps(R, NS3, 384, power=96, color=(245, 250, 255), size=64)
    item(R, 'doc1513', 410, 0, 395)
    item(R, 'doc1513b', 410, 0, 300)
    item(R, 'doc1515', 440, 0, 250)
    item(R, 'doc1515b', 480, 0, 280)
    item(R, 'doc1517', 640, 0, -470)
    item(R, 'doc1517b', 730, 0, -480)
    item(R, 'doc1519', 850, top, 130)
    item(R, 'doc1519b', 850, top, 10)
    return (R, 'BIO', 'Biological Holding (Indev). SCP-1513 potted pets, SCP-1515 in a wire enclosure, SCP-1517 in a freezer, SCP-1519 in saline.',
            1, 0.7, ((300, 165, -120), (760, 90, 330)))


# =====================================================================  HCZ
def room2origin():
    R = R_('room2origin', amb=9)
    junction(R, 'NS', 'dark', hub=(-352, -480, 352, 480), hh=448, openings={'hubE': [(-80.0, 80.0, 250.0, 410.0)]})
    wall_fan(R, 'x', 352, +1, 0, 330)
    rng = random.Random(1512)
    R.floor([(-70, -210), (64, -226), (92, 190), (-76, 214)], 1.0, DARK, cast=False, coll=False)
    for i in range(14):
        s = 1 if i % 2 else -1
        rz = rng.uniform(-200, 200)
        rx = rng.uniform(-50, 50)
        j = lambda a: rng.uniform(-a, a)
        r = rng.uniform(8, 13)
        pts = [V(rx, 3, rz), V(s * (140 + j(30)), 5 + r, rz + j(90)), V(s * (346 - r), 8 + r, rz + j(160)),
               V(s * (346 - r), 150 + j(40), rz + j(200)), V(s * (346 - r), 300 + j(40), rz + j(240)),
               V(s * (340 - r), 440 - r, rz + j(240)), V(s * (150 + j(40)), 442 - r, rz + j(260)), V(j(60), 442 - r, rz + j(280))]
        for p in pts:
            p[2] = max(-470.0, min(470.0, p[2]))
        tendril(R, pts[:rng.randint(5, 8)], r)
    top = desk(R, -348, -470, -264, -330, 0)
    flat(R, -330, -430, -282, -370, top + 0.7, WHITE, bottom='E')
    named(R, 'SHEET_S', -306, top + 6, -400)
    top = desk(R, 264, 330, 348, 470, 0)
    flat(R, 282, 370, 330, 430, top + 0.7, WHITE, bottom='W')
    named(R, 'SHEET_N', 306, top + 6, 400)
    named(R, 'SLIME', 0, 3, 0)
    reserve(R, 'SLIMEM')
    named(R, 'BODY', 300, 0, -410)
    label(R, '1512', 280, -480, 'N')
    label(R, '1512', -280, 480, 'S')
    plate(R, 'origin', 0, -480, 'N', yc=416, w=250, h=46)
    plate(R, 'origin', 0, 480, 'S', yc=416, w=250, h=46)
    red_lamp(R, 0, 0, 448, power=110, rng=900)
    lamp(R, 0, -400, 448, power=62, rng=700, size=36)
    lamp(R, 0, 400, 448, power=62, rng=700, size=36)
    lamps(R, ((0, -760), (0, 760)), 384, power=66, color=(230, 238, 255), size=36)
    item(R, 'doc1512', -306, top, -350)
    item(R, 'doc1512b', 306, top, 445)
    return (R, 'ORI', 'Procedure 1512-Alpha hall (Indev). A tendril of SCP-1512 has come up through the floor; a worksheet at each end.',
            2, 0.25, ((120, 165, -900), (-60, 150, 0)))


def room2purge():
    R = R_('room2purge')
    junction(R, 'NS', 'foam', hub=(-448, -512, 448, 512), hh=512,
             openings={'hubW': [(-400.0, -200.0, 200.0, 400.0), (200.0, 400.0, 200.0, 400.0)]})
    wall_fan(R, 'x', -448, -1, -300, 300, size=200, depth=110, radius=92)
    wall_fan(R, 'x', -448, -1, 300, 300, size=200, depth=110, radius=92)
    fountain(R, -250, 0)
    R.box(184, 138, -654, 192, 166, -626, REDLAMP, skip='E', lux=8)
    named(R, 'PURGE_S', 180, 152, -640)
    plate(R, 'purge', 192, -640, 'W', yc=198, w=130, h=28)
    R.box(-192, 138, 626, -184, 166, 654, REDLAMP, skip='W', lux=8)
    named(R, 'PURGE_N', -180, 152, 640)
    plate(R, 'purge', -192, 640, 'E', yc=198, w=130, h=28)
    named(R, 'BUBC', 60, 170, 0)
    reserve(R, 'BUB', 7)
    label(R, '1518', 330, -512, 'N')
    label(R, '1518', -330, 512, 'S')
    ceil_light(R, 0, -280, 512, size=72, power=124, rng=1000)
    ceil_light(R, 0, 280, 512, size=72, power=124, rng=1000)
    lamps(R, ((0, -780), (0, 780)), 384, power=78, size=36)
    item(R, 'doc1518', 100, 0, -640)
    item(R, 'doc1518b', -100, 0, 640)
    return (R, 'PUR', 'Foam-lined fan hall (Indev). SCP-1518, the bubble fountain; loose bubbles until the fans are purged.',
            2, 0.6, ((150, 165, -900), (-120, 190, 0)))


# =====================================================================  EZ
def room2review():
    R = R_('room2review')
    junction(R, 'NS', 'ez', openings={'hubW': [door_op(0)]})
    x0, z0, x1, z1 = annex(R, 'x', -192, -1, -420, 420, 544, 336, 'ez', door=0, key=2)
    plate(R, 'review', -192, 0, 'E')
    console(R, -620, z1 - 40, 'S')
    console(R, -420, z1 - 40, 'S')
    chair(R, -520, 290, 'N')
    wallmonitor(R, -520, z1, 'S', yc=272)
    named(R, 'PLAY', -520, 130, 334)
    label(R, '1110', -296, z1, 'S', yc=262)
    R.box(-720, 0, -416, -380, 96, -344, DIRTY, skip='B', top=WOOD, lux=12)
    R.box(-560, 268, -418, -540, 288, -380, DARK, lux=12)
    named(R, 'COUNTER', -550, 96, -380)
    top = desk(R, -796, -160, -712, 160, 0)
    R.box(-786, top, -40, -736, top + 18, 40, DARK, skip='B', lux=10)
    flat(R, -776, -24, -746, 24, top + 18.6, TAPEM, bottom='E')
    tbox(R, -780, top, 70, -740, top + 8, 96, TAPEM)
    tbox(R, -776, top + 8, 72, -736, top + 16, 98, TAPEM)
    named(R, 'DECK', -761, top + 22, 0)
    label(R, '1250', x0, 0, 'E', yc=224)
    cabinet(R, -764, -262, 0, 'E')
    named(R, 'STAFF', -470, 0, 70)
    ceil_light(R, -528, 0, 336, size=80, power=116, rng=820)
    lamps(R, NS3, 384, power=96, color=(255, 250, 240), size=64)
    item(R, 'firstaid', -680, 96, -380)
    item(R, '18vbat', -610, 96, -380)
    item(R, 'eyedrops', -490, 96, -380)
    item(R, 'key3', -420, 96, -380, 50)
    item(R, 'doc1110', -520, 0, 230)
    item(R, 'doc1110b', -330, 0, -250)
    item(R, 'doc1250', -756, top, -110)
    item(R, 'doc1250b', -756, top, 126)
    return (R, 'REV', 'Surveillance Review (Indev). SCP-1110 on the review monitor, SCP-1250 tapes and a deck.',
            3, 0.3, ((-290, 165, 240), (-640, 100, -260)))


def room2lecture():
    R = R_('room2lecture')
    junction(R, 'NS', 'ez', openings={'S_W': [door_op(-400)]})
    x0, z0, x1, z1 = annex(R, 'x', -192, -1, -600, 544, 640, 352, 'ez', door=-400)
    plate(R, 'lecture', -192, -400, 'E')
    wall_decal(R, BOARDM, -576, z1, 'S', 420, 210, 195)
    named(R, 'BOARD', -576, 195, z1 - 4)
    R.box(-400, 0, 400, -340, 112, 444, WOOD, skip='B', lux=10)
    for z in (180, 40, -100):
        for x in (-780, -670, -560, -450):
            chair(R, x, z, 'N')
    named(R, 'BEAR', -600, 0, 430)
    reserve(R, 'BEARM')
    label(R, '1313', x1, -120, 'W', yc=214)
    whiteboard(R, x0, -200, 'E')
    ceil_vent(R, -700, -360, 352)
    ceil_light(R, -576, 250, 352, size=80, power=112, rng=860)
    ceil_light(R, -576, -280, 352, size=64, power=96, rng=820)
    lamps(R, NS3, 384, power=96, color=(255, 250, 240), size=64)
    item(R, 'doc1313', -330, 0, -400)
    item(R, 'doc1313b', -370, 112, 422)
    return (R, 'LEC', 'Lecture Room 2 (Indev). Most of SCP-1313 is still on the board.',
            3, 0.7, ((-300, 165, -480), (-620, 150, 420)))


# =====================================================================  Indev zone
def room2site41():
    R = R_('room2site41')
    junction(R, 'NS', 'board', openings={'hubE': [door_op(0)]})
    x0, z0, x1, z1 = annex2(R, 'x', 192, +1, -576, 576, 704, 384, 'std', door=0, extra={1: [(438.0, 630.0, 0.0, 320.0)]})
    annex(R, 'z', 576, +1, 620, 960, 280, 320, 'std', door=790, spawn_door=False)
    ndoor(R, 'CELL', 790, 0, 608, 0)
    named(R, 'CELLSPOT', 790, 0, 790)
    named(R, 'POST', 790, 0, 480)
    plate(R, 'site41', 192, 0, 'W')
    mesh_panel(R, (480, -576), (480, -70), 0, 384)
    mesh_panel(R, (480, 70), (480, 576), 0, 384)
    for z in (-570, -320, -70, 70, 320, 570):
        R.box(475, 0, z - 5, 485, 384, z + 5, DIRTY, skip='TB', lux=12)
    wall_decal(R, PLT3, 478, -195, 'W', 190, 38, 215, uv=PLATES['site41'])
    label(R, '1312', 478, 200, 'W', yc=215)
    ibeam(R, 'z', -300, 480, 960, 344)
    ibeam(R, 'z', 300, 480, 960, 344)
    top = desk(R, 880, -110, 952, 110, 0)
    crate(R, 880, 0, -470, yaw=15)
    crate(R, 620, 0, -520, yaw=-10, kind=2)
    bench(R, 290, 330, 90)
    named(R, 'GUARD', 368, 0, -330)
    named(R, 'WHITE', 836, 0, 0)
    named(R, 'ORANGE', 640, 0, -400)
    named(R, 'BLACK', 690, 0, 330)
    ceil_light(R, 368, 0, 384, size=64, power=96, rng=820)
    ceil_light(R, 720, -260, 384, size=64, power=100, rng=900, color=(235, 242, 255))
    ceil_light(R, 720, 260, 384, size=64, power=100, rng=900, color=(235, 242, 255))
    ceil_light(R, 790, 780, 320, size=40, power=60, rng=520)
    lamps(R, NS3, 384, power=80)
    item(R, 'doc1312', 400, 0, 120)
    item(R, 'doc1312b', 916, top, -60)
    item(R, 'key3', 916, top, 30, 60)
    item(R, 'firstaid', 916, top, 86)
    return (R, 'S41', 'A section of Site 41 (Indev). SCP-1312: a fence, a guard, and three figures of one flat colour each.',
            4, 0.15, ((300, 165, -420), (800, 120, 250)))


def room2cell49():
    R = R_('room2cell49')
    win = (-200.0, 200.0, 96.0, 256.0)
    junction(R, 'NS', 'std', openings={'hubE': [door_op(0)], 'hubW': [(-80.0, 80.0, 220.0, 380.0)]})
    wall_fan(R, 'x', -192, -1, 0, 300)
    x0, z0, x1, z1 = annex2(R, 'x', 192, +1, -384, 384, 320, 336, 'std', door=0, extra={2: [(184.0, 584.0, 96.0, 256.0)]})
    cx0, cz0, cx1, cz1 = annex(R, 'x', 576, +1, -320, 320, 352, 320, 'white', window=win)
    glaze(R, 'x', 576, +1, win)
    plate(R, 'cell49', 192, 0, 'W')
    label(R, '1516', 576, 292, 'W', yc=200)
    R.box(540, 72, -44, 576, 92, 44, DIRTY, skip='E', lux=10)
    named(R, 'TRAY', 556, 94, 0)
    top = desk(R, 296, -380, 536, -312, 0)
    for i, x in enumerate((350, 416, 482)):
        flat(R, x - 20, -366, x + 20, -326, top + 0.7, CARDSM, (i / 3.0, 0, (i + 1) / 3.0, 1), bottom='N')
        named(R, 'CARD%d' % i, x, top + 6, -346)
    chair(R, 416, -270, 'S')
    R.box(652, 0, -306, 760, 46, -120, WORDSM, skip='B', lux=12)
    R.box(900, 0, 180, 980, 74, 300, WORDSM, skip='B', lux=12)
    R.box(836, 0, 220, 878, 44, 262, WORDSM, skip='B', lux=12)
    wall_decal(R, WORDSM, cx1, -40, 'W', 320, 190, 170, uv=(0, 0, 0.7, 0.42))
    named(R, 'MAN', 800, 0, 0)
    ceil_light(R, 416, 0, 336, size=64, power=92, rng=760)
    ceil_light(R, 816, 0, 320, size=80, power=132, rng=860, color=(255, 255, 255))
    lamps(R, NS3, 384, power=84)
    item(R, 'doc1516', 312, top, -346)
    item(R, 'doc1516b', 300, 0, 250)
    return (R, 'C49', 'Humanoid Cell 49 (Indev). SCP-1516, the Written Man, behind glass; three word cards on the desk.',
            4, 0.45, ((300, 165, -250), (800, 120, 120)))


def room2vault117():
    R = R_('room2vault117')
    AW = wmat('dark', 384)
    junction(R, 'NS', 'dark', openings={'hubW': [door_op(0)]})
    lift(R, -192, -1, 0, 0, 0, DEEP, AW)
    bw = wmat('dark', 384).but(v0=DEEP + 384)
    out = [(-192, -448), (-192, 448), (576, 448), (576, -448)]
    R.walls(out, DEEP, DEEP + 384, bw, holes={0: [span(out[0], (-192, -96), (-192, 96)) + (DEEP, DEEP + 320)]})
    R.rect_floor(-192, -448, 576, 448, DEEP, HCZFLOOR)
    R.rect_ceil(-192, -448, 576, 448, DEEP + 384, DIRTY)
    top = plinth(R, 330, 0, y=DEEP, h=80, s=40)
    crystal(R, 330, top, 0)
    named(R, 'CRYSTAL', 330, top + 50, 0)
    R.light(330, top + 90, 0, rng=660, color=(150, 205, 255), power=95)
    R.box(430, DEEP, 180, 500, DEEP + 124, 240, STONEM, skip='B', lux=12)
    ball(R, (250, DEEP + 22, -220), 22, STONEM, seg=6, rings=2, lux=20)
    R.tube((120, DEEP + 10, 260), (212, DEEP + 14, 312), 10, STONEM.but(us=63, vs=128), sides=6, caps=True, coll=False, lux=24)
    tt = table(R, 60, -400, 220, -320, y=DEEP)
    flat(R, 80, -390, 130, -330, tt + 0.7, GLASS, (0, 0, 0.2, 0.25), bottom='N', lm=False, coll=False)
    flat(R, 146, -386, 196, -334, tt + 0.7, GLASS, (0, 0, 0.2, 0.25), bottom='N', lm=False, coll=False)
    label(R, '1511', 576, 0, 'W', yc=DEEP + 216)
    plate(R, 'vault', -192, 0, 'E')
    sign_at(R, 'elevator', -192, -250, 'E', 150, 50, 250)
    ceil_light(R, 120, 0, DEEP + 384, size=44, power=64, rng=700, color=(210, 225, 255))
    lamps(R, NS3, 384, power=74, color=(230, 238, 255), size=40)
    item(R, 'doc1511', 140, DEEP, 120)
    item(R, 'doc1511b', 30, tt, -360)
    return (R, 'V117', 'Vault 117 (Indev). A lift down to a piece of SCP-1511 that still speaks.',
            4, 0.65, ((-60, DEEP + 165, -330), (330, DEEP + 110, 20)))


def room2bunker():
    R = R_('room2bunker')
    AW = wmat('hcz', 384)
    junction(R, 'NS', 'hcz', openings={'hubE': [door_op(0)]})
    lift(R, 192, +1, 0, 0, 0, DEEP, AW)
    bw = wmat('hcz', 384).but(v0=DEEP + 384)
    out = [(-640, -448), (-640, 448), (192, 448), (192, -448)]
    R.walls(out, DEEP, DEEP + 384, bw, holes={1: [(244.0, 436.0, DEEP, DEEP + 320)],
                                              2: [span(out[2], (192, 96), (192, -96)) + (DEEP, DEEP + 320)]})
    R.rect_floor(-640, -448, 192, 448, DEEP, HCZFLOOR)
    R.rect_ceil(-640, -448, 192, 448, DEEP + 384, DIRTY)
    annex(R, 'z', 448, +1, -480, -120, 220, 320, 'hcz', door=-300, y=DEEP, spawn_door=False)
    ndoor(R, 'LOCKER', -300, DEEP, 480, 0, locked=True)
    t = shelf_unit(R, -474, 690, -130, 728, DEEP, height=220, levels=3)
    ceil_light(R, -300, 620, DEEP + 320, size=36, power=56, rng=520)
    # SCP-1514-1A: a steel unit 1.5 x 0.9 x 0.6 m with its dials on the front
    R.box(-636, DEEP, -192, -480, DEEP + 232, 192, PANELS2.but(us=256, vs=232, v0=DEEP + 232), skip='B', top=DARK, lux=12)
    wall_decal(R, CTRL, -480, -40, 'E', 220, 130, DEEP + 135)
    wall_decal(R, REDLAMP, -480, 130, 'E', 56, 56, DEEP + 140)
    R.tube((-560, DEEP + 232, 0), (-560, DEEP + 384, 0), 16, RUST.but(us=100, vs=256), sides=8, lux=16)
    named(R, 'PANEL', -474, DEEP + 135, -40)
    red_lamp(R, -220, 0, DEEP + 384)
    bigfan(R, -220, DEEP + 372, -270, radius=120)
    named(R, 'BODY', -330, DEEP, -230)
    label(R, '1514', -640, 292, 'E', yc=DEEP + 216)
    plate(R, 'bunker', 192, 0, 'W')
    sign_at(R, 'elevator', 192, -250, 'W', 150, 50, 250)
    ceil_light(R, -60, 250, DEEP + 384, size=44, power=58, rng=700, color=(255, 230, 210))
    lamps(R, NS3, 384, power=72, color=(232, 238, 255), size=36)
    item(R, 'doc1514', 40, DEEP, -220)
    item(R, 'doc1514b', -250, DEEP, -300)
    item(R, 'firstaid', -420, t[1], 708)
    item(R, '18vbat', -340, t[1], 708)
    item(R, 'key4', -260, t[1], 708, 40)
    item(R, 'nvgoggles', -200, t[2], 708, 30)
    item(R, 'bat', -400, t[2], 708, 70)
    return (R, 'BUN', 'Secure Bunker (Indev). A lift down to SCP-1514-1A, its alarm, and a locker that opens when the inspection is logged.',
            4, 0.85, ((100, DEEP + 165, 330), (-480, DEEP + 110, -60)))


ALL = [room2siv, room2bio, room2origin, room2purge, room2review, room2lecture, room2site41, room2cell49, room2vault117, room2bunker]
