"""Seven rooms for thirteen SCPs (the sixth batch, code in IndevS13.bb).

  room2scps4      LCZ    Containment 4-L, rebuilt from the reference corridor shot:
                         four cells - SCP-1079, SCP-1916, SCP-1200 (+ an SCP-1200-A), SCP-971
  room2storage13  Indev  Storage Unit 13: SCP-1080 (+ an SCP-1080-1 worker), SCP-1081, SCP-1082, SCP-1083
  room2beefbelly  EZ     an SCP-2789 instance grown into the canteen: staff, the owner, the free burger
  room2grocery    Indev  SCP-3182: the Aisle 3 fixtures from Denton, and the Deimos Event that came with them
  room2testhouse  EZ     Test House 1879, up a lift: three closet doors and SCP-1879
  room2nagasaki   HCZ    Chamber 1145, down a lift: SCP-1145 in its lit tank, two Class-D cells, the lamp breaker
  room2ltstorage  HCZ    Long-Term Storage 6D: SCP-1921, the cotton candy kiosk and its calliope

Same conventions as rooms_s16.py: named() / ndoor() / reserve() / lever() hand things to the code,
gen_b6.py turns them into r\\Objects[] / r\\RoomDoors[] slots and S13_* constants."""
from rooms_s16 import *

UP = 704.0
L4 = json.load(open(os.path.join(HERE, 'labels4.json')))
DPJ = json.load(open(os.path.join(HERE, 'doorplates.json')))
P4 = json.load(open(os.path.join(HERE, 'plates4.json')))
PR4 = json.load(open(os.path.join(HERE, 'props4.json')))
LAB4 = Mat('indev_labels4.png', cast=False)
DPL = Mat('indev_doorplates.png', cast=False)
PLT4 = Mat('indev_plates4.png', cast=False)
PROPS = Mat('indev_props4.png', cast=False)
QUARTZ = Mat('indev_quartz.png', 64)
VINYL = Mat('indev_vinyl.png', 128)
KIOSKM = Mat('indev_kiosk.png', 128)
FLOSS = Mat('indev_floss.png', 64)
CANOPY = Mat('indev_canopy.png', 64)
WATERM = Mat('indev_water.png', 256, alpha=True, cast=False)
GOODS = Mat('indev_goods.png', 512, 256, 256)
WALLP = Mat('indev_wallpaper.png', 192)
BBMENU = Mat('indev_bbmenu.png', emit=170, cast=False)
STYLES['lcz'] = (Mat('whitewall.jpg', 364), CONC, DARK)
STYLES['bb'] = (Mat('officewall.jpg', 364), Mat('indev_bbfloor.png', 128), EZCEIL)
STYLES['store'] = (Mat('Old_Whitewall.jpg', 384), TILE, EZCEIL)
STYLES['house'] = (WALLP, WOOD, Mat('white.jpg', 256))


def label4(R, num, cx, cz, facing, yc=214.0, size=76.0):
    wall_decal(R, LAB4, cx, cz, facing, size, size, yc, uv=L4[num])


def doorplate(R, num, cx, cz, facing, yc=258.0, size=68.0):
    wall_decal(R, DPL, cx, cz, facing, size, size, yc, uv=DPJ[num])


def plate4(R, key, cx, cz, facing, yc=352.0, w=200.0, h=40.0):
    wall_decal(R, PLT4, cx, cz, facing, w, h, yc, uv=P4[key])


def hang_sign(R, key, x, z, y, w=200.0, h=40.0, top=None):
    """A sign hung across an aisle on two chains, readable from both sides (its face spans x)."""
    R.box(x - w / 2, y - h / 2, z - 2, x + w / 2, y + h / 2, z + 2, DARK, lux=10)
    wall_decal(R, PLT4, x, z + 2, 'N', w, h, y, uv=P4[key])
    wall_decal(R, PLT4, x, z - 2, 'S', w, h, y, uv=P4[key])
    if top:
        for dx in (-w / 2 + 12, w / 2 - 12):
            chain(R, x + dx, z, top, top - (y + h / 2))


def lever(R, name, x, y, z, yaw, up=True):
    """A wall lever (IAxLever): base in the named slot, handle in the next one."""
    R.spawns.append(dict(kind='lever', name=name, pos=(x, y, z), yaw=yaw, up=up))


def chamfer_pilaster(R, plane, sign, c, h, mat, w=72.0, d=30.0, foot=62.0, ky=150.0, fy=42.0):
    """The pilasters of the reference corridor: a flat column whose foot flares out in a slope.
    The wall is x = plane, the pilaster stands out towards sign * x, centred on z = c."""
    def P(dep, z, y):
        return V(plane + sign * dep, y, z)
    z0, z1 = c - w / 2, c + w / 2
    out = (sign, 0, 0)
    poly_facing(R, [P(d, z0, ky), P(d, z1, ky), P(d, z1, h), P(d, z0, h)], out, mat, lux=12)
    poly_facing(R, [P(foot, z0, fy), P(foot, z1, fy), P(d, z1, ky), P(d, z0, ky)], (sign, 0.6, 0), mat, lux=12)
    poly_facing(R, [P(foot, z0, 0), P(foot, z1, 0), P(foot, z1, fy), P(foot, z0, fy)], out, DARK, lux=12)
    for (z, s) in ((z0, -1), (z1, 1)):
        poly_facing(R, [P(0, z, 0), P(foot, z, 0), P(foot, z, fy), P(d, z, ky), P(0, z, ky)], (0, 0, s), mat, lux=12)
        poly_facing(R, [P(0, z, ky), P(d, z, ky), P(d, z, h), P(0, z, h)], (0, 0, s), mat, lux=12)


def glass_box(R, x0, y0, z0, x1, y1, z1, frame=DARK):
    """A reinforced glass case: glass sides (no collision of their own), a steel top and base, hidden walls."""
    R.box(x0 - 6, y0, z0 - 6, x1 + 6, y0 + 10, z1 + 6, frame, skip='B', lux=10)
    R.box(x0, y0 + 10, z0, x1, y1, z1, GLASS, skip='TB', lm=False, coll=False)
    R.box(x0 - 6, y1, z0 - 6, x1 + 6, y1 + 10, z1 + 6, frame, lux=10)
    for (px, pz) in ((x0, z0), (x1, z0), (x1, z1), (x0, z1)):
        R.box(px - 4, y0 + 10, pz - 4, px + 4, y1, pz + 4, frame, skip='TB', lux=10)
    corners = [(x0, z0), (x1, z0), (x1, z1), (x0, z1)]
    for i in range(4):
        a, b = corners[i], corners[(i + 1) % 4]
        R.collide_wall(a, b, y0, y1)
        R.collide_wall(b, a, y0, y1)


# =====================================================================  LCZ
def room2scps4():
    """The corridor from the reference shot: white walls with a dark band, sloped pilaster feet, a dark
    ceiling with bulkheads, containment doors with black plates, and a window into a machine niche."""
    R = R_('room2scps4')
    w, ch = 224.0, 448.0
    win = (-150.0, 150.0, 100.0, 330.0)
    junction(R, 'NS', 'lcz', w=w, ch=ch, openings={'S_W': [door_op(-560)], 'N_W': [door_op(560)],
                                                   'S_E': [door_op(-560)], 'N_E': [door_op(560)], 'hubE': [win]})
    WM = wmat('lcz', ch)
    for c in (-800, -330, 330, 800):
        chamfer_pilaster(R, -w, +1, c, ch, WM)
        chamfer_pilaster(R, w, -1, c, ch, WM)
        R.box(-w, ch - 64, c - 36, w, ch, c + 36, WM.but(us=256), skip='T', lux=12)
    # the window into the machine niche
    annex(R, 'x', w, +1, -200, 200, 120, 384, 'std', window=win)
    wall_decal(R, CTRL, w + 64 + 120, 0, 'W', 280, 200, 215)
    for zz in (-60, 60):
        R.tube((w + 120, 300, zz), (w + 120, 384, zz), 14, DIRTY, sides=8, lux=16)
    plate4(R, 'cont4l', -w, 0, 'E', yc=300, w=220, h=44)
    lamps(R, ((0, -560), (0, 0), (0, 560)), ch, power=92, rng=900, size=32)
    # the four cells
    cells = [('1079', -1, -560), ('1916', -1, 560), ('1200', +1, -560), ('971', +1, 560)]
    for num, s, dz in cells:
        lo, hi = (dz - 300, dz + 300)
        annex(R, 'x', s * w, s, lo, hi, 448, 352, 'white', door=dz)
        doorplate(R, num, s * w, dz + (132 if dz < 0 else -132), 'E' if s < 0 else 'W')
        ceil_light(R, s * 512, dz, 352, size=48, power=86, rng=640, color=(250, 250, 255))
    # SCP-1079: the crate of bonbons
    crate(R, -640, 0, -760, yaw=10)
    top = table(R, -460, -830, -320, -730)
    tbox(R, -446, top, -808, -406, top + 8, -772, PROPS, PR4['bonbon'])
    tbox(R, -398, top, -806, -362, top + 8, -776, PROPS, PR4['bonbon'])
    named(R, 'BONBON', -410, top + 10, -790)
    label4(R, '1079', -736, -560, 'E')
    item(R, 'doc1079', -330, 0, -470)
    item(R, 'doc1079b', -350, top, -746)
    # SCP-1916: the sealed crate, and one box out on the table
    tbox(R, -720, 0, 640, -580, 110, 840, PROPS, PR4['crate'])
    wall_decal(R, PLT4, -580, 740, 'E', 130, 26, 70, uv=P4['noneat'])
    top = table(R, -460, 730, -320, 830)
    tbox(R, -420, top, 752, -380, top + 10, 792, PROPS, PR4['moonrocks'])
    named(R, 'MOONROCKS', -400, top + 12, 772)
    label4(R, '1916', -736, 560, 'E')
    item(R, 'doc1916', -330, 0, 470)
    item(R, 'doc1916b', -350, top, 740)
    # SCP-1200: gum on the table, an SCP-1200-A in a reinforced case
    top = table(R, 330, -830, 470, -730)
    for gx in (346, 386, 426):
        tbox(R, gx, top, -800, gx + 24, top + 6, -770, PROPS, PR4['gum'])
    named(R, 'GUM', 400, top + 8, -785)
    glass_box(R, 560, 0, -580, 720, 300, -400)
    named(R, 'IRON', 640, 0, -490)
    label4(R, '1200', 736, -700, 'W')
    item(R, 'doc1200', 330, 0, -470)
    item(R, 'doc1200b', 440, top, -748)
    # SCP-971: the menu on the desk, the phone on the wall, cabinet #26
    top = desk(R, 640, 600, 730, 840, 0)
    flat(R, 660, 680, 710, 750, top + 0.7, PROPS, PR4['menu'], bottom='W')
    named(R, 'MENU', 685, top + 4, 715)
    R.box(726, 150, 780, 736, 222, 822, DARK, lux=8)
    R.box(722, 196, 788, 726, 216, 814, DIRTY, lux=8)
    named(R, 'PHONE', 724, 186, 800)
    cabinet(R, 700, 380, 0, 'W')
    label4(R, '971', 520, 860, 'S')
    item(R, 'doc971', 330, 0, 470)
    item(R, 'doc971b', 690, top, 640)
    return (R, 'C4L', 'Containment 4-L (Indev). A corridor of four cells: SCP-1079, SCP-1916, SCP-1200 and SCP-971.',
            1, 0.5, ((0, 165, -940), (0, 190, 0)))


# =====================================================================  Indev zone
def room2storage13():
    R = R_('room2storage13')
    hub = (-640, -576, 640, 576)
    junction(R, 'NS', 'std', hub=hub, hh=512, openings={'hubE': [door_op(360)]})
    annex(R, 'x', 640, +1, 200, 560, 224, 320, 'std', door=360, spawn_door=False)
    ndoor(R, 'CLOSET', 672, 0, 360, 90, locked=True)
    t = shelf_unit(R, 710, 500, 900, 552, 0, height=220, levels=3)
    item(R, 'firstaid', 760, t[1], 526)
    item(R, '18vbat', 840, t[1], 526)
    item(R, 'key4', 800, t[2], 526, 45)
    item(R, 'nvgoggles', 740, t[2], 526, 30)
    ceil_light(R, 816, 380, 320, size=36, power=56, rng=520)
    named(R, 'CRATE', 590, 0, 360)
    named(R, 'CRATE2', 590, 0, 110)
    reserve(R, 'CRATEM')
    # SCP-1080: the black chamber, and the worker it made
    R.box(-600, 0, -420, -300, 228, 36, DARK, skip='B', lux=10)
    R.box(-300, 96, -220, -292, 144, -170, CHECKER, lux=8)
    named(R, 'TANK', -290, 120, -195)
    named(R, 'WORKER', -200, 0, 140)
    label4(R, '1080', -640, 200, 'E', yc=236)
    # the broken tug
    HZ = STYLES['haz'][0].but(us=256, vs=128)
    R.box(360, 20, -420, 480, 120, -260, HZ, skip='B', top=DARK, lux=10)
    R.box(470, 20, -400, 490, 262, -280, DIRTY, skip='B', lux=10)
    R.box(490, 8, -394, 600, 18, -370, DIRTY, lux=10)
    R.box(490, 8, -310, 600, 18, -286, DIRTY, lux=10)
    for (wx, wz) in ((380, -424), (380, -256), (460, -424), (460, -256)):
        R.tube((wx, 22, wz - 8), (wx, 22, wz + 8), 20, DARK, sides=8, caps=True, coll=False, lux=16)
    named(R, 'TUG', 420, 80, -340)
    # SCP-1081 on its bench, lead-lined lockers behind
    lockers(R, 'z', 576, -1, -620, -300)
    top = table(R, -260, 470, -60, 560)
    R.box(-170, top, 500, -146, top + 30, 520, DARK, lux=8)
    ball(R, (-158, top + 40, 510), 9, DARK, seg=6, rings=2, lux=20)
    flat(R, -120, 490, -80, 530, top + 0.7, PROPS, PR4['dials'], bottom='S')
    named(R, 'SPEAKER', -158, top + 22, 510)
    label4(R, '1081', -160, 576, 'S', yc=262)
    # SCP-1082: the triple-locked safe
    R.box(330, 0, 470, 520, 230, 572, PANELS2.but(us=256, vs=230, v0=230), skip='B', top=DARK, lux=10)
    wall_decal(R, PROPS, 425, 470, 'S', 160, 160, 120, uv=PR4['safedoor'])
    named(R, 'SAFE', 425, 120, 466)
    top2 = table(R, 220, 480, 300, 560)
    label4(R, '1082', 590, 576, 'S', yc=262)
    # SCP-1083 in an open locker
    open_cabinet(R, -80, 0, -572, 80, 200, -480, DIRTY, 'N')
    R.box(-74, 94, -566, 74, 100, -486, DIRTY, lux=10)
    ball(R, (0, 120, -528), 19, QUARTZ, seg=8, rings=3, lux=12)
    R.box(-12, 100, -514, 12, 108, -500, QUARTZ, lux=10)
    for ex in (-8, 8):
        R.quad(V(ex + 5, 116, -507.5), V(ex - 5, 116, -507.5), V(ex - 5, 126, -507.5), V(ex + 5, 126, -507.5), DARK,
               uvrect=(0, 0, 0.1, 0.1), coll=False, cast=False, lux=8)
    named(R, 'SKULL', 0, 120, -526)
    label4(R, '1083', -200, -576, 'N', yc=232)
    t = shelf_unit(R, -634, -560, -574, -440, 0, height=230, levels=4)
    crate(R, -520, 0, 420, yaw=8)
    bigfan(R, 0, 470, 0, radius=160)
    plate4(R, 'storage13', 0, -576, 'N', yc=448, w=240, h=48)
    for (x, z) in ((-330, -300), (330, -300), (-330, 300), (330, 300)):
        ceil_light(R, x, z, 512, size=64, power=96, rng=900, color=(240, 244, 255))
    lamps(R, ((0, -800), (0, 800)), 384, power=72, size=36)
    item(R, 'doc1080', -250, 0, -100)
    item(R, 'doc1080b', -170, 0, 220)
    item(R, 'doc1081', -230, top, 530)
    item(R, 'doc1081b', -110, 0, 430)
    item(R, 'doc1082', 425, 0, 400)
    item(R, 'doc1082b', 260, top2, 520)
    item(R, 'doc1083', 110, 0, -430)
    item(R, 'doc1083b', 45, 100, -505)
    item(R, 'bat', -604, t[1], -500, 70)
    item(R, 'eyedrops', -604, t[2], -480, 40)
    return (R, 'U13', 'Storage Unit 13 (Indev). SCP-1080 and its worker, SCP-1081, SCP-1082 in its safe, SCP-1083.',
            4, 0.3, ((300, 165, -520), (-420, 110, 120)))


def room2grocery():
    R = R_('room2grocery')
    junction(R, 'NS', 'old', openings={'S_W': [door_op(-560)]})
    x0, z0, x1, z1 = annex(R, 'x', -192, -1, -760, 700, 720, 352, 'store', door=-560, spawn_door=False)
    ndoor(R, 'STORE', -224, 0, -560, 90)
    plate4(R, 'grocery', -192, -560, 'E', yc=352, w=220, h=40)
    gm = GOODS.but(us=256, vs=200, v0=200)
    for i, z in enumerate((-420, -120, 180, 480)):
        R.box(-900, 0, z - 40, -440, 200, z + 40, gm, skip='B', top=DARK, lux=12)
    for key, z in (('aisle1', -590), ('aisle2', -270), ('aisle3', 30), ('aisle4', 330)):
        hang_sign(R, key, -670, z, 290, w=170, h=34, top=352)
    named(R, 'AISLE3', -670, 0, 30)
    for i, (x, z) in enumerate(((-880, 30), (-470, 60), (-670, 610))):
        named(R, 'FIG%d' % i, x, 0, z)
    R.box(-400, 0, -360, -300, 96, -240, DIRTY, skip='B', top=DARK, lux=10)
    R.box(-380, 96, -340, -330, 140, -300, DARK, lux=8)
    wall_decal(R, PROPS, -616, z1, 'S', 520, 65, 288, uv=PR4['denton'])
    ceil_fan(R, -616, -300, 352)
    for (x, z, p) in ((-670, -590, 90), (-670, -270, 70), (-670, 30, 46), (-670, 330, 70), (-670, 610, 60), (-350, -200, 80)):
        ceil_light(R, x, z, 352, size=56, power=p, rng=700, color=(236, 246, 236))
    label4(R, '3182', x1, -300, 'W', yc=220)
    lamps(R, NS3, 384, power=80)
    item(R, 'doc3182', -320, 0, -650)
    item(R, 'doc3182b', -315, 96, -270)
    item(R, 'indevration', -470, 0, -300, 40)
    return (R, 'GRO', 'Denton Aisle 3 (Indev). The shelving of SCP-3182 and the Deimos Event that came with it.',
            4, 0.75, ((-300, 165, -700), (-700, 120, 60)))


# =====================================================================  EZ
def room2beefbelly():
    R = R_('room2beefbelly')
    junction(R, 'NS', 'bb', hub=(-640, -512, 640, 512), hh=384)
    # the counter, the kitchen behind it, the board above
    R.box(360, 0, -330, 440, 104, 330, VINYL, skip='B', top=METAL, lux=10)
    R.box(560, 0, -330, 636, 96, -170, METAL, skip='B', top=DARK, lux=10)
    R.box(560, 0, -110, 636, 90, 40, METAL, skip='B', top=DARK, lux=10)
    vending(R, 596, 220, 'W')
    wall_decal(R, BBMENU, 640, 0, 'W', 600, 150, 296)
    wall_decal(R, BBMENU, 0, -512, 'N', 250, 150, 280, uv=(0.01, 0.04, 0.38, 0.96))
    wall_decal(R, BBMENU, 0, 512, 'S', 250, 150, 280, uv=(0.01, 0.04, 0.38, 0.96))
    for i, z in enumerate((-200, 0, 200)):
        named(R, 'STAFF%d' % i, 500, 0, z)
    R.box(394, 104, 34, 410, 112, 50, DARK, lux=8)
    named(R, 'BELL', 402, 110, 42)
    flat(R, 376, -140, 424, -80, 104.7, PROPS, PR4['freecard'], bottom='W')
    ball(R, (400, 114, -40), 10, KIOSKM, seg=6, rings=2, lux=20)
    named(R, 'BURGER', 400, 112, -60)
    # the booths
    for z in (-300, 0, 300):
        table(R, -600, z - 50, -460, z + 50, top=WOODT)
        for s in (-1, 1):
            zs, zb = z + s * 90, z + s * 112
            R.box(-600, 0, min(zs, zs + s * 40), -460, 44, max(zs, zs + s * 40), VINYL, skip='B', lux=10)
            R.box(-600, 44, min(zb, zb + s * 14), -460, 112, max(zb, zb + s * 14), VINYL, lux=10)
    named(R, 'CEO', -420, 0, 300)
    # what it took from the building: pipes and wiring, some of it lagged in skin
    R.tube((640, 340, -420), (400, 340, -420), 7, FLESH, sides=6, coll=False, lux=24)
    R.tube((400, 340, -420), (400, 340, -330), 7, FLESH, sides=6, coll=False, lux=24)
    R.tube((640, 356, 420), (-640, 356, 420), 9, RUST.but(us=57, vs=256), sides=6, coll=False, lux=24)
    ceil_fan(R, -300, -200, 384)
    ceil_fan(R, -300, 250, 384)
    for (x, z) in ((-300, -380), (-300, 380), (200, -250), (200, 250)):
        ceil_light(R, x, z, 384, size=64, power=104, rng=820, color=(255, 240, 214))
    lamps(R, ((0, -800), (0, 800)), 384, power=84)
    label4(R, '2789', -640, -150, 'E', yc=240)
    item(R, 'doc2789', -200, 0, -380)
    return (R, 'BB', "Beefbelly Bill's (Indev). An instance of SCP-2789 grown into the staff canteen.",
            3, 0.4, ((-450, 165, -440), (400, 120, 100)))


def room2testhouse():
    R = R_('room2testhouse')
    AW = wmat('ez', 384)
    junction(R, 'NS', 'ez', openings={'S_E': [door_op(-500)]})
    lift(R, 192, +1, -500, 0, -500, UP, AW)
    plate4(R, 'testhouse', 192, -500, 'W', yc=352)
    sign_at(R, 'elevator', 192, -760, 'W', 150, 50, 250)
    label4(R, '1879', 192, -250, 'W')
    # the house, upstairs over the corridor
    HM = wmat('house', 352).but(v0=UP + 352)
    out = [(-760, -760), (-760, 560), (192, 560), (192, -760)]
    R.walls(out, UP, UP + 352, HM, holes={0: [(364.0, 556.0, UP, UP + 320)],
                                           1: [(164.0, 356.0, UP, UP + 320), (674.0, 866.0, UP, UP + 320)],
                                           2: [span(out[2], (192, -404), (192, -596)) + (UP, UP + 320)]})
    R.rect_floor(-760, -760, 192, 560, UP, WOOD)
    R.rect_ceil(-760, -760, 192, 560, UP + 352, Mat('white.jpg', 256))
    annex(R, 'z', 560, +1, -700, -300, 200, 320, 'house', door=-500, y=UP, spawn_door=False)
    annex(R, 'z', 560, +1, -190, 190, 200, 320, 'house', door=10, y=UP, spawn_door=False)
    annex(R, 'x', -760, -1, -520, -80, 180, 320, 'house', door=-300, y=UP, spawn_door=False)
    for i, (dx, dz, ang) in enumerate(((-500, 592, 0), (10, 592, 0), (-792, -300, 90))):
        ndoor(R, 'DOOR%d' % i, dx, UP, dz, ang)
    for i, (x, z) in enumerate(((-500, 470), (10, 470), (-660, -300))):
        named(R, 'SPOT%d' % i, x, UP, z)
    for i, (x, z) in enumerate(((-500, 690), (10, 690), (-900, -300))):
        named(R, 'IN%d' % i, x, UP, z)
    # a front room nobody lives in
    R.box(-620, UP, -600, -300, UP + 46, -520, VINYL, skip='B', lux=10)
    R.box(-620, UP, -640, -300, UP + 104, -600, VINYL, lux=10)
    tt = table(R, -540, -460, -380, -380, y=UP, h=46, top=WOODT)
    flat(R, -660, -500, -260, -260, UP + 0.8, VINYL.but(us=64), bottom='S', lux=16, cast=False)
    R.box(-160, UP, -756, 40, UP + 60, -690, WOODT, skip='B', lux=10)
    R.box(-130, UP + 60, -742, 10, UP + 160, -712, DARK, lux=10)
    wall_decal(R, PROPS, -760, 200, 'E', 90, 70, UP + 210, uv=PR4['photo'])
    wall_decal(R, PROPS, 192, 250, 'W', 90, 70, UP + 210, uv=PR4['photo'])
    pendant(R, -300, -200, UP + 352, power=120, rng=900, color=(255, 236, 200))
    ceil_light(R, -100, 300, UP + 352, size=48, power=70, rng=700, color=(255, 236, 200))
    lamps(R, NS3, 384, power=92, color=(255, 250, 240), size=64)
    item(R, 'doc1879', 100, 0, -320)
    item(R, 'doc1879b', -470, tt, -420)
    return (R, 'TH', 'Test House 1879 (Indev). A lift up to a furnished mock-up house with three closet doors. Somebody knocks.',
            3, 0.75, ((100, UP + 165, -650), (-400, UP + 120, 400)))


# =====================================================================  HCZ
def room2nagasaki():
    R = R_('room2nagasaki')
    AW = wmat('hcz', 384)
    junction(R, 'NS', 'hcz', openings={'hubW': [door_op(0)]})
    lift(R, -192, -1, 0, 0, 0, DEEP, AW)
    plate4(R, 'chamber1145', -192, 0, 'E', yc=352)
    sign_at(R, 'elevator', -192, -250, 'E', 150, 50, 250)
    bw = wmat('hcz', 512).but(v0=DEEP + 512)
    out = [(-192, -960), (-192, 960), (980, 960), (980, -960)]
    R.walls(out, DEEP, DEEP + 512, bw, holes={0: [span(out[0], (-192, -96), (-192, 96)) + (DEEP, DEEP + 320)]})
    R.rect_floor(-192, -960, 980, 960, DEEP, HCZFLOOR)
    R.rect_ceil(-192, -960, 980, 960, DEEP + 512, DIRTY)
    # the borosilicate tank on its dais
    cx = 500.0
    R.box(cx - 200, DEEP, -200, cx + 200, DEEP + 24, 200, DARK, skip='B', lux=12)
    glass_box(R, cx - 152, DEEP + 24, -152, cx + 152, DEEP + 330, 152)
    R.box(cx - 146, DEEP + 36, -146, cx + 146, DEEP + 300, 146, WATERM, skip='B', lm=False, coll=False)
    R.light(cx, DEEP + 170, 0, rng=720, color=(80, 160, 255), power=90)
    named(R, 'TEDDY', cx, DEEP + 120, 0)
    reserve(R, 'TEDDYM')
    # eight xenon lamps round it
    for k in range(8):
        a = math.radians(22.5 + 45 * k)
        lx, lz = cx + 400 * math.cos(a), 400 * math.sin(a)
        R.box(lx - 6, DEEP, lz - 6, lx + 6, DEEP + 250, lz + 6, DIRTY, skip='B', lux=10)
        R.box(lx - 18, DEEP + 250, lz - 18, lx + 18, DEEP + 290, lz + 18, LIGHTPANEL.but(emit=240), lux=8, cast=False)
        R.light(lx - 60 * math.cos(a), DEEP + 260, lz - 60 * math.sin(a), rng=760, color=(240, 244, 255), power=46, radius=12)
    # two Class-D cells, glass-fronted, against the north and south walls
    for i, s in enumerate((1, -1)):
        zf, zb = s * 700, s * 960
        lo, hi = sorted((zf, zb))
        R.box(380, DEEP, lo, 392, DEEP + 300, hi, PANELS2, lux=12)
        R.box(608, DEEP, lo, 620, DEEP + 300, hi, PANELS2, lux=12)
        R.box(380, DEEP + 300, lo, 620, DEEP + 312, hi, DARK, lux=12)
        R.quad(V(392, DEEP, zf), V(608, DEEP, zf), V(608, DEEP + 300, zf), V(392, DEEP, zf) + V(0, 300, 0), GLASS,
               uvrect=(0, 0, 0.85, 1.2), lm=False, coll=False)
        R.collide_wall((392, zf), (608, zf), DEEP, DEEP + 300)
        R.collide_wall((608, zf), (392, zf), DEEP, DEEP + 300)
        R.box(400, DEEP, min(s * 860, s * 950), 600, DEEP + 40, max(s * 860, s * 950), WHITE, skip='B', lux=10)
        ceil_light(R, 500, s * 830, DEEP + 300, size=36, power=48, rng=420)
        named(R, 'DCLASS%d' % i, 500, DEEP, s * 790)
    # the lamp breaker on the far wall
    wall_decal(R, CTRL, 980, 0, 'W', 150, 150, DEEP + 170)
    lever(R, 'LEVER', 976, DEEP + 170, 0, 270, up=True)
    plate4(R, 'xenon', 980, 0, 'W', yc=DEEP + 270, w=180, h=36)
    label4(R, '1145', 980, -260, 'W', yc=DEEP + 230)
    lamps(R, NS3, 384, power=74, color=(232, 238, 255), size=36)
    item(R, 'doc1145', -100, DEEP, -150)
    item(R, 'doc1145b', 900, DEEP, -120)
    return (R, 'N45', 'Chamber 1145 (Indev). A lift down to SCP-1145 in its lit water tank, two Class-D cells and the lamp breaker.',
            2, 0.45, ((-120, DEEP + 165, -500), (500, DEEP + 150, 0)))


def room2ltstorage():
    R = R_('room2ltstorage')
    junction(R, 'NS', 'std', openings={'hubE': [door_op(0)]})
    x0, z0, x1, z1 = annex(R, 'x', 192, +1, -560, 560, 700, 384, 'std', door=0, key=2)
    plate4(R, 'ltstorage', 192, 0, 'W', yc=352, w=220, h=40)
    # SCP-1921: the kiosk, its canopy and sign
    R.box(500, 20, -150, 740, 120, 150, KIOSKM, skip='B', top=WOODT, lux=10)
    for (wx, wz) in ((530, -156), (710, -156), (530, 156), (710, 156)):
        R.tube((wx, 28, wz - 6 if wz < 0 else wz), (wx, 28, wz if wz < 0 else wz + 6), 26, DARK, sides=8, caps=True, coll=False, lux=16)
    for (px, pz) in ((494, -174), (746, -174), (494, 174), (746, 174)):
        R.box(px - 4, 120, pz - 4, px + 4, 300, pz + 4, KIOSKM, skip='TB', lux=10)
    R.box(480, 300, -186, 760, 312, 186, CANOPY, top=CANOPY, lux=10)
    R.box(494, 314, -140, 500, 378, 140, WOODT, lux=10)
    wall_decal(R, PROPS, 494, 0, 'W', 272, 62, 346, uv=PR4['kiosksign'])
    R.tube((560, 120, 0), (560, 146, 0), 40, METAL, sides=10, lux=14)
    ball(R, (560, 156, 0), 30, FLOSS, seg=8, rings=3, lux=16, coll=False)
    named(R, 'SPINNER', 560, 150, 0)
    R.box(580, 0, 190, 660, 110, 250, DIRTY, skip='B', lux=10)
    wall_decal(R, PROPS, 580, 220, 'W', 56, 28, 72, uv=PR4['clownmilk'])
    named(R, 'MILK', 576, 72, 220)
    # the calliope behind it
    R.box(760, 20, -120, 860, 200, 120, KIOSKM, skip='B', top=DARK, lux=10)
    for k in range(8):
        pz = -98 + k * 28
        R.tube((810, 200, pz), (810, 270 + (k % 4) * 18, pz), 7, BRONZE, sides=6, caps=True, lux=20)
    named(R, 'CALLIOPE', 756, 150, 0)
    # the rolls, and the rest of the fairground salvage
    t = shelf_unit(R, 262, 300, 326, 540, 0, height=200, levels=3)
    for zz in (330, 380, 430, 480):
        R.tube((294, t[1] + 8, zz - 14), (294, t[1] + 8, zz + 14), 8, PROPS.but(us=50, vs=256), sides=6, caps=True, coll=False, lux=24)
    crate(R, 860, 0, -440, yaw=-12)
    crate(R, 380, 0, -470, yaw=20, kind=2)
    ceil_fan(R, 400, -350, 384)
    for (x, z) in ((420, 0), (720, -380), (720, 380)):
        ceil_light(R, x, z, 384, size=64, power=96, rng=860, color=(255, 236, 214))
    label4(R, '1921', x1, -300, 'W', yc=226)
    lamps(R, NS3, 384, power=80)
    item(R, 'doc1921', 330, 0, -100)
    item(R, 'doc1921b', 294, t[1], 520)
    return (R, 'LT6', 'Long-Term Storage 6D (Indev). SCP-1921, the black cotton candy kiosk, and its calliope.',
            2, 0.7, ((300, 165, -450), (640, 150, 60)))


ALL = [room2scps4, room2storage13, room2grocery, room2beefbelly, room2testhouse, room2nagasaki, room2ltstorage]
