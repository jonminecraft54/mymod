"""Five rooms for eight SCPs (the eighth batch, code in IndevS08.bb).

  room2yule        LCZ    Containment 4-Y (Seasonal), the reference corridor a third time: four cells -
                          SCP-2983 (cereal, prize terminal), SCP-1933 (a drunk Santa), SCP-1225 (the ornament on
                          the tree, a rotting supply locker), and MTF Kappa-31's staging room (SCP-6895)
  room2pinata      Indev  Humanoid Cell 956: the observation room, the cell, the cold store, the incinerator
  room2demoncore   HCZ    Bunker 095-FR, down a lift: the Demon Core on the Los Alamos bench, the shielded room
  room2argos       Indev  St. Nick's Workshop, and a lift down to the Fort Sheridan bunker (SCP-3355)
  room2chrono      HCZ    The Department of Chronology hangar, and a lift up to the launch deck (SCP-4255)

Same conventions as rooms_b7.py; gen_b8.py turns names into S08_* constants."""
from rooms_b7 import *

L6 = json.load(open(os.path.join(HERE, 'labels6.json')))
DP6 = json.load(open(os.path.join(HERE, 'doorplates6.json')))
P6 = json.load(open(os.path.join(HERE, 'plates6.json')))
PR6 = json.load(open(os.path.join(HERE, 'props6.json')))
N6 = json.load(open(os.path.join(HERE, 'neon6.json')))
LAB6 = Mat('indev_labels6.png', cast=False)
DPL6 = Mat('indev_doorplates6.png', cast=False)
PLT6 = Mat('indev_plates6.png', cast=False)
PROPS6 = Mat('indev_props6.png', cast=False)
NEON6 = Mat('indev_neon6.png', emit=215, cast=False)
LEAD = Mat('indev_lead.png', 128)
BEIGE = Mat('indev_beige.png', 128)
BERYL = Mat('indev_beryl.png', 64)
PU = Mat('indev_pu.png', 32)
LEAF = Mat('indev_leaf.png', 64)
CANDY = Mat('indev_candy.png', 64)
FROST = Mat('indev_frost.png', alpha=True, cast=False)
XLIGHTS = Mat('indev_xlights.png', alpha=True, cast=False)
STYLES['cold'] = (PANELS2.but(us=256), METAL, WHITE)
STYLES['hangar'] = (Mat('heavy_containment_wall_1789291243567.jpg', 512, 600, 600), Mat('scpcb_checkerplate.jpg', 128), DARK)


def label6(R, num, cx, cz, facing, yc=214.0, size=76.0):
    wall_decal(R, LAB6, cx, cz, facing, size, size, yc, uv=L6[num])


def doorplate6(R, num, cx, cz, facing, yc=258.0, size=68.0):
    wall_decal(R, DPL6, cx, cz, facing, size, size, yc, uv=DP6[num])


def plate6(R, k, cx, cz, facing, yc=352.0, w=230.0, h=None):
    wall_decal(R, PLT6, cx, cz, facing, w, h or w * 0.15, yc, uv=P6[k])


def prop6(R, k, cx, cz, facing, w, h, yc):
    wall_decal(R, PROPS6, cx, cz, facing, w, h, yc, uv=PR6[k])


def neon6(R, k, cx, cz, facing, w, h, yc):
    wall_decal(R, NEON6, cx, cz, facing, w, h, yc, uv=N6[k])


def fir(R, x, z, y=0.0, h=200.0, r=70.0):
    """a small potted fir: a terracotta pot and four stacked cones of needles"""
    R.prism(octo(x, z, 26), y, y + 40, TERRA, caps='T', top=SOILM, lux=12)
    R.tube((x, y + 40, z), (x, y + 70, z), 5, WOOD, sides=6, lux=16)
    for k in range(4):
        y0 = y + 60 + k * (h - 60) / 4.0
        rr = r * (1.0 - k * 0.22)
        ring = octo(x, z, rr)
        apex = V(x, y0 + (h - 60) / 4.0 + 26, z)
        for i in range(8):
            a, b = ring[i], ring[(i + 1) % 8]
            mid = ((a[0] + b[0]) / 2 - x, 0.5, (a[1] + b[1]) / 2 - z)
            poly_facing(R, [V(a[0], y0, a[1]), V(b[0], y0, b[1]), apex], mid, LEAF, lux=14)
        poly_facing(R, [V(p[0], y0, p[1]) for p in ring], (0, -1, 0), LEAF, lux=14)


def cabinet_box(R, x0, y0, z0, x1, y1, z1, front, face, mat=BEIGE):
    """a mainframe cabinet with a printed front on the side facing `face`"""
    R.box(x0, y0, z0, x1, y1, z1, mat, skip='B', lux=10)
    cx, cz = (x0 + x1) / 2, (z0 + z1) / 2
    pos = {'N': (cx, z1), 'S': (cx, z0), 'E': (x1, cz), 'W': (x0, cz)}[face]
    w = (x1 - x0) if face in 'NS' else (z1 - z0)
    prop6(R, front, pos[0], pos[1], face, w - 6, (y1 - y0) - 20, (y0 + y1) / 2)


# =====================================================================  LCZ
def room2yule():
    """The reference corridor a third time: white walls, the dark band, sloped pilaster feet, the dark ceiling with its
    bulkheads, four containment doors with black plates, the window onto machinery."""
    R = R_('room2yule')
    w, ch = 224.0, 448.0
    win = (-150.0, 150.0, 100.0, 330.0)
    junction(R, 'NS', 'lcz', w=w, ch=ch, openings={'S_W': [door_op(-560)], 'N_W': [door_op(560)],
                                                   'S_E': [door_op(-560)], 'N_E': [door_op(560)], 'hubE': [win]})
    WM = wmat('lcz', ch)
    for c in (-800, -330, 330, 800):
        chamfer_pilaster(R, -w, +1, c, ch, WM)
        chamfer_pilaster(R, w, -1, c, ch, WM)
        R.box(-w, ch - 64, c - 36, w, ch, c + 36, WM.but(us=256), skip='T', lux=12)
    annex(R, 'x', w, +1, -200, 200, 120, 384, 'std', window=win)
    wall_decal(R, CTRL, w + 64 + 120, 0, 'W', 280, 200, 215)
    for zz in (-60, 60):
        R.tube((w + 120, 300, zz), (w + 120, 384, zz), 14, DIRTY, sides=8, lux=16)
    plate6(R, 'yule', -w, 0, 'E', yc=300, w=250)
    lamps(R, ((0, -560), (0, 0), (0, 560)), ch, power=92, rng=900, size=32)
    for num, s, dz in (('2983', -1, -560), ('1933', -1, 560), ('1225', +1, -560), ('6895', +1, 560)):
        annex(R, 'x', s * w, s, dz - 300, dz + 300, 448, 352, 'white', door=dz)
        doorplate6(R, num, s * w, dz + (132 if dz < 0 else -132), 'E' if s < 0 else 'W')
        ceil_light(R, s * 512, dz, 352, size=48, power=86, rng=640, color=(250, 250, 255))
    # ---- SCP-2983: low-risk item storage, the cereal, the bowl, the vendor terminal
    t = shelf_unit(R, -730, -850, -670, -560, 0, height=230, levels=4)
    for k, y in enumerate(t[1:]):
        for j in range(5):
            z = -830 + j * 52
            tbox(R, -720, y, z, -684, y + 56, z + 20, PROPS6, PR6['cereal'], top=(0, 0, 0.25, 0.05))
    top = table(R, -520, -820, -360, -720)
    R.prism(octo(-430, -780, 16), top, top + 10, WHITE, caps='T', top=Mat('indev_beige.png', 32), lux=12)
    R.box(-400, top, -760, -376, top + 40, -740, WHITE, lux=10)
    tbox(R, -500, top, -800, -470, top + 50, -790, PROPS6, PR6['cereal'], top=(0, 0, 0.25, 0.05))
    named(R, 'BOWL', -430, top + 10, -780)
    named(R, 'BOX', -485, top + 30, -795)
    dtop = desk(R, -720, -500, -640, -320, 0)
    workstation(R, -690, dtop, -410, 90)
    neon6(R, 'vendor', -736, -410, 'E', 120, 60, 200)
    named(R, 'TERM', -680, dtop + 30, -410)
    named(R, 'WATERS', -560, 0, -330)
    prop6(R, 'wondersign', -512, -860, 'N', 160, 80, 260)
    plate6(R, 'lowrisk', -224, -560, 'E', yc=380, w=230)
    label6(R, '2983', -736, -700, 'E')
    # ---- SCP-1933: a low-security cell with basic furnishings
    R.box(-730, 0, 650, -560, 44, 850, DIRTY, skip='B', top=WHITE, lux=10)
    top = table(R, -480, 700, -380, 800)
    for k, (bx, bz) in enumerate(((-470, 710), (-450, 790), (-400, 720))):
        R.tube((bx, top, bz), (bx, top + 34, bz), 5, GREENP if k else Mat('indev_kiosk.png', 64), sides=6, caps=True, lux=18)
    tbox(R, -440, top, 760, -416, top + 30, 784, PROPS6, PR6['wrap0'])
    named(R, 'BOTTLE', -428, top + 15, 772)
    R.box(-700, 0, 300, -620, 44, 380, VINYL, skip='B', lux=10)
    R.box(-700, 44, 300, -620, 110, 316, VINYL, lux=10)
    named(R, 'SANTA', -560, 0, 520)
    ceil_fan(R, -512, 470, 352, radius=110)
    label6(R, '1933', -736, 420, 'E')
    # ---- SCP-1225: the open-air enclosure, the tree, the ornament's box, the supply locker
    R.add([V(620, 351, -720), V(380, 351, -720), V(380, 351, -400), V(620, 351, -400)],
          [(N6['sky'][2], N6['sky'][3]), (N6['sky'][0], N6['sky'][3]), (N6['sky'][0], N6['sky'][1]), (N6['sky'][2], N6['sky'][1])], NEON6)
    R.light(500, 330, -560, rng=700, color=(170, 190, 255), power=46, ent=False)
    fir(R, 420, -560)
    named(R, 'ORN', 455, 178, -545)
    top = plinth(R, 660, -780, h=90, s=40)
    R.box(630, top, -800, 690, top + 26, -760, METAL, lux=10)
    named(R, 'SBOX', 660, top + 20, -780)
    cabinet(R, 700, -380, 0, 'W')
    named(R, 'LOCKER', 668, 100, -380)
    plate6(R, 'openair', 224, -560, 'W', yc=380, w=230)
    plate6(R, 'nocont', 736, -560, 'W', yc=260, w=220)
    label6(R, '1225', 736, -760, 'W')
    # ---- MTF Kappa-31 staging: suits in lockers, unicycles, charity boxes, the map
    for k, z in enumerate((420.0, 520.0, 620.0, 720.0)):
        R.box(690, 0, z - 44, 736, 230, z + 44, PANELS2.but(us=88, vs=230, v0=230), skip='BE', lux=10)
        prop6(R, 'suit', 690, z, 'W', 80, 120, 140)
    for k, (x, z) in enumerate(((330.0, 330.0), (400.0, 330.0), (470.0, 330.0))):
        named(R, 'UNI%d' % k, x, 0, z)
    for k, x in enumerate((340.0, 420.0)):
        tbox(R, x, 0, 780, x + 60, 50, 840, PROPS6, PR6['stacy'])
    prop6(R, 'kmap', 520, 860, 'S', 220, 220, 200)
    bench(R, 560, 500, 90)
    named(R, 'KAPPA', 450, 0, 600)
    ceil_fan(R, 512, 660, 352, radius=110)
    reserve(R, 'ORNM')
    reserve(R, 'UNIM', 3)
    reserve(R, 'UNIV')
    plate6(R, 'unigift', 224, 560, 'W', yc=380, w=230)
    label6(R, '6895', 736, 300, 'W')
    item(R, 'doc2983', -330, 0, -470)
    item(R, 'doc2983b', -690, dtop, -350)
    item(R, 'doc1933', -330, 0, 470)
    item(R, 'doc1225', 330, 0, -470)
    item(R, 'doc1225b', 660, top, -800)
    item(R, 'doc6895', 330, 0, 470)
    item(R, 'doc6895b', 380, 50, 810)
    return (R, 'YUL', 'Containment 4-Y (Indev), the seasonal wing: SCP-2983, SCP-1933, SCP-1225 and MTF Kappa-31\'s staging room.',
            1, 0.15, ((0, 165, -940), (0, 190, 0)))


# =====================================================================  Indev zone
def room2pinata():
    R = R_('room2pinata')
    junction(R, 'NS', 'std', openings={'hubE': [door_op(0)]})
    x0, z0, x1, z1 = annex2(R, 'x', 192, +1, -480, 480, 320, 352, 'white', door=0,
                            extra={2: [(634.0, 826.0, 0.0, 320.0), (180.0, 480.0, 100.0, 260.0)], 1: [(68.0, 260.0, 0.0, 320.0)]})
    plate6(R, 'cell956', 192, 0, 'W', yc=352, w=220)
    label6(R, '956', 192, 250, 'W')
    # the cell itself, through the window and the door
    win = (0.0, 300.0, 100.0, 260.0)
    cx0, cz0, cx1, cz1 = annex(R, 'x', 576, +1, -420, 420, 380, 352, 'white', door=-250, window=win)
    glaze(R, 'x', 576, +1, win)
    named(R, 'PINATA', 830, 0, 0)
    for k, (x, z) in enumerate(((700, -360), (700, 360), (960, 360), (960, -360))):
        named(R, 'PC%d' % k, x, 0, z)
    R.box(cx1 - 30, 300, cz1 - 30, cx1, 340, cz1, DARK, lux=10)
    ceil_light(R, 830, 0, 352, size=72, power=110, rng=860)
    plate6(R, 'under12', x1, 150, 'W', yc=300, w=230)
    # the cold store, SCP-956-1 at -4 C
    ax0, az0, ax1, az1 = annex(R, 'z', 480, +1, 300, 560, 300, 300, 'cold', door=420)
    t = shelf_unit(R, 310, 780, 550, 840, 0, height=220, levels=4)
    for y in t[1:]:
        for k in range(6):
            x = 330 + k * 38
            R.prism(octo(x, 810, 13), y, y + 34, GLASS, caps='', lm=False, coll=False)
            R.prism(octo(x, 810, 11), y, y + 22, CANDY, caps='T', lux=16)
    for (bx, bz, br) in ((360.0, 640.0, 30.0), (480.0, 680.0, 24.0)):
        ball(R, (bx, 0, bz), br, CANDY, seg=7, rings=3, top_only=True, lux=18)
    named(R, 'CANDY', 420, 30, 660)
    prop6(R, 'jar', 430, az1, 'S', 120, 60, 260)
    for (x, z, f) in ((ax0, 700.0, 'E'), (ax1, 700.0, 'W')):
        wall_decal(R, FROST, x, z, f, 260, 280, 150)
    plate6(R, 'cold', 420, 480, 'S', yc=352, w=230)
    ceil_light(R, 430, 700, 300, size=40, power=60, rng=500, color=(200, 230, 255))
    # the incinerator, and the extra instance waiting for it
    R.box(300, 0, -476, 520, 220, -404, RUST.but(us=220, vs=220), skip='B', top=DARK, lux=10)
    R.box(360, 30, -404, 460, 130, -400, DARK, lux=8)
    named(R, 'FURNACE', 410, 80, -396)
    R.box(370, 0, -370, 450, 26, -300, METAL, skip='B', lux=10)
    named(R, 'EXTRA', 410, 26, -336)
    reserve(R, 'PINM')
    reserve(R, 'EXTRAM')
    plate6(R, 'incin', 410, -480, 'N', yc=280, w=200)
    wall_decal(R, CTRL, 540, -470, 'N', 50, 50, 140)
    named(R, 'BURN', 540, 140, -466)
    # the observation side: a desk, a monitor, the researcher
    dtop = desk(R, 260, 100, 340, 300, 0)
    wallmonitor(R, x0, 200, 'E', yc=230)
    named(R, 'DOCN', 380, 0, 220)
    ceil_fan(R, 420, -160, 352, radius=120)
    ceil_light(R, 420, 0, 352, size=56, power=88, rng=760)
    lamps(R, NS3, 384, power=80)
    item(R, 'doc956', 300, dtop, 160)
    item(R, 'doc956b', 300, dtop, 250)
    item(R, 'firstaid', 520, 0, 420, 50)
    return (R, 'PIN', 'Humanoid Cell 956 (Indev). SCP-956 walks the edge of its cell and stares at one wall. The cold store holds SCP-956-1.',
            4, 0.08, ((300, 165, -300), (830, 100, 0)))


def room2argos():
    R = R_('room2argos')
    AW = wmat('std', 384)
    junction(R, 'NS', 'std', openings={'hubE': [door_op(0)], 'hubW': [door_op(0)]})
    lift(R, -192, -1, 0, 0, 0, D, AW)
    x0, z0, x1, z1 = annex(R, 'x', 192, +1, -500, 500, 640, 352, 'ez', door=0)
    plate6(R, 'stnick', 192, 0, 'W', yc=352, w=230)
    plate6(R, 'sheridan', -192, 0, 'E', yc=352, w=250)
    sign_at(R, 'elevator', -192, -250, 'E', 150, 50, 250)
    label6(R, '3355', -192, 250, 'E')
    # St. Nick's Workshop: the charity front upstairs
    dtop = desk(R, 600, -200, 800, -120, 0)
    R.box(700, dtop, -170, 740, dtop + 16, -140, DARK, lux=10)
    chair(R, 700, -60, 'S')
    prop6(R, 'nickposter', x1, -300, 'W', 160, 160, 200)
    prop6(R, 'nickposter', x0, 300, 'E', 160, 160, 200)
    for k in range(9):
        x, z = 300 + (k % 3) * 70, 300 + (k // 3) * 62
        tbox(R, x, 0, z, x + 56, 40 + (k % 2) * 20, z + 48, PROPS6, PR6['wrap%d' % (k % 2)] if k % 3 else PR6['parcel'])
    fir(R, 820, 380, h=230, r=80)
    wall_decal(R, XLIGHTS, x1, 0, 'W', 400, 40, 300)
    named(R, 'VOL', 560, 0, 200)
    ceil_light(R, 600, 0, 352, size=64, power=100, rng=820, color=(255, 236, 214))
    # the bunker under Fort Sheridan
    LX = 920.0
    out = [(-192, -900), (-192, 900), (LX, 900), (LX, -900)]
    BW = Mat('concrete_wall_texture_1789291161197.jpg', 512, 400, D + 400)
    R.walls(out, D, D + 400, BW, holes={0: [span(out[0], (-192, -96), (-192, 96)) + (D, D + 320)],
                                        2: [span(out[2], (LX, -520), (LX, -680)) + (D + 220, D + 380),
                                            span(out[2], (LX, 680), (LX, 520)) + (D + 220, D + 380)]})
    R.rect_floor(-192, -900, LX, 900, D, HCZFLOOR)
    R.rect_ceil(-192, -900, LX, 900, D + 400, DIRTY)
    for zc in (-600.0, 600.0):
        wall_fan(R, 'x', LX, +1, zc, D + 300)
    for (zc, face) in ((480.0, 'S'), (-480.0, 'N')):
        for k in range(7):
            xa = -20 + k * 110
            z0_, z1_ = (zc, zc + 70) if face == 'S' else (zc - 70, zc)
            cabinet_box(R, xa, D, z0_, xa + 100, D + 250, z1_, 'argos', face)
    R.tube((LX - 30, D, 860), (LX - 30, D + 400, 860), 16, RUST.but(us=100), sides=8, lux=16)
    R.tube((LX - 70, D, 860), (LX - 70, D + 400, 860), 12, RUST.but(us=75), sides=8, lux=16)
    plate6(R, 'tograd', LX, 760, 'W', yc=D + 200, w=230)
    # Nick's terminal and printer
    ttop = desk(R, 500, -70, 640, 70, D)
    R.box(520, ttop, -40, 600, ttop + 70, 40, BEIGE, lux=10)
    neon6(R, 'crt', 520, 0, 'W', 70, 52, ttop + 38)
    named(R, 'TERM', 516, ttop + 38, 0)
    R.box(660, D, 100, 740, D + 90, 160, BEIGE, skip='B', top=DARK, lux=10)
    named(R, 'PRINTER', 700, D + 95, 130)
    plate6(R, 'argos', 570, -900, 'N', yc=D + 300, w=220)
    # the chute the packages come down
    R.box(260, D + 230, -240, 340, D + 400, -160, METAL, lux=10)
    ctop = table(R, 240, -260, 360, -140, y=D)
    named(R, 'CHUTE', 300, ctop, -200)
    reserve(R, 'PARCELM')
    bigfan(R, 300, D + 390, 300, radius=110)
    for (x, z) in ((0, 0), (300, -600), (300, 600), (700, -300), (700, 300)):
        ceil_light(R, x, z, D + 400, size=56, power=74, rng=760, color=(226, 240, 230))
    red_lamp(R, -100, -700, D + 400, power=50, rng=500)
    lamps(R, NS3, 384, power=80)
    item(R, 'doc3355', 700, dtop, -160)
    item(R, 'bat', 650, ttop, 50, 60)
    return (R, 'ARG', "St. Nick's Workshop (Indev): a charity front, and a lift down to the Argos bunker where SCP-3355 runs its deliveries.",
            4, 0.92, ((-60, D + 165, -350), (560, D + 120, 0)))


# =====================================================================  HCZ
def room2demoncore():
    R = R_('room2demoncore', amb=9)
    AW = wmat('hcz', 384)
    junction(R, 'NS', 'hcz', openings={'hubW': [door_op(0)]})
    lift(R, -192, -1, 0, 0, 0, D, AW)
    plate6(R, 'bunker', -192, 0, 'E', yc=352, w=230)
    plate6(R, 'classd', -192, 0, 'E', yc=300, w=210)
    sign_at(R, 'elevator', -192, -250, 'E', 150, 50, 250)
    prop6(R, 'trefoil', -192, 260, 'E', 90, 90, 200)
    label6(R, '095-FR', -192, -520, 'E')
    lamps(R, NS3, 384, power=72, color=(232, 238, 255), size=36)
    # the bunker
    HX, HZ, HH = 980.0, 900.0, 480.0
    out = [(-192, -HZ), (-192, HZ), (HX, HZ), (HX, -HZ)]
    BW = wmat('dark', HH).but(v0=D + HH)
    R.walls(out, D, D + HH, BW, holes={0: [span(out[0], (-192, -96), (-192, 96)) + (D, D + 320)]})
    R.rect_floor(-192, -HZ, HX, HZ, D, HCZFLOOR)
    R.rect_ceil(-192, -HZ, HX, HZ, D + HH, DIRTY)
    # the shielded control room, lead-lined, with a lead-glass window and a heavy door
    CZ, CX = -480.0, 560.0
    lw = [(-120.0, 200.0, D + 110, D + 260), (284.0, 476.0, D, D + 320)]
    # the lead walls are 64 thick, like the facility's own, so the heavy door and its buttons fit in them
    LT = 32.0
    both_faces(R, (-192, CZ), (CX, CZ), D, D + 320, LEAD, ('N', 'S'), holes=lw, mat2=PANELS2, t=LT)
    both_faces(R, (CX, -HZ), (CX, CZ), D, D + 320, LEAD, ('E', 'W'), mat2=PANELS2, t=LT)
    R.box(CX - LT, D, CZ - LT, CX + LT, D + 320, CZ + LT, LEAD, skip='TB', lux=10)
    reveals(R, 'x', CZ - LT, CZ + LT, -120, 200, D + 110, D + 260, LEAD)
    reveals(R, 'x', CZ - LT, CZ + LT, 284, 476, D, D + 320, LEAD)
    glass_quad(R, (-120, CZ), (200, CZ), D + 110, D + 260)
    R.box(-192, D + 320, -HZ, CX + LT, D + 340, CZ + LT, LEAD, lux=10)
    R.rect_ceil(-192, -HZ, CX - LT, CZ - LT, D + 319, PANELS2)
    ndoor(R, 'CTRL', 380, D, CZ, 0)
    plate6(R, 'shield', 380, CZ + LT, 'N', yc=D + 360, w=220)
    plate6(R, 'flux', 100, CZ + LT, 'N', yc=D + 300, w=230)
    ctop = desk(R, -120, CZ - 112, 200, CZ - 42, D)
    for x in (-60.0, 80.0):
        workstation(R, x, ctop, CZ - 80, 0)                  # screens towards the chairs (they were backwards)
        chair(R, x, CZ - 160, 'N', y=D)
    prop6(R, 'fluxdial', -170, CZ - LT, 'S', 80, 40, D + 200)
    named(R, 'CTRLIN', 180, D, -700)
    ceil_light(R, 180, -690, D + 320, size=48, power=72, rng=640, color=(240, 244, 255))
    # the lead safe, standing open
    R.box(700, D, -300, 900, D + 30, -100, DARK, skip='B', lux=10)
    R.box(720, D + 30, -280, 880, D + 230, -120, LEAD, skip='B', lux=10)
    R.box(712, D + 40, -122, 718, D + 220, -40, LEAD, lux=10)
    named(R, 'SAFE', 800, D + 120, -110)
    # the Los Alamos bench: the core, the lower cup, the upper shell propped on a screwdriver
    btop = table(R, 400, 200, 540, 300, y=D, top=METAL)
    R.prism(octo(470, 250, 26), btop, btop + 10, BERYL, caps='T', lux=10)
    ball(R, (470, btop + 22, 250), 12, PU, seg=8, rings=3, lux=10)
    ball(R, (470, btop + 30, 250), 26, BERYL, seg=10, rings=3, top_only=True, lux=10, coll=False)
    R.tube((500, btop + 4, 268), (488, btop + 32, 262), 1.6, DARK, sides=5, coll=False, lux=20)
    R.tube((500, btop + 4, 268), (514, btop - 6, 276), 3, Mat('indev_kiosk.png', 32), sides=5, coll=False, lux=20)
    named(R, 'CORE', 470, btop + 22, 250)
    named(R, 'SCREW', 500, btop + 10, 268)
    named(R, 'HANDLER', 380, D, 360)
    prop6(R, 'plaque', -192, 400, 'E', 160, 120, D + 200)
    for (x, z, f) in ((HX, 0.0, 'W'), (HX, 500.0, 'W'), (300.0, HZ, 'S')):
        prop6(R, 'trefoil', x, z, f, 110, 110, D + 260)
    plate6(R, 'radiation', 470, HZ, 'S', yc=D + 380, w=230)
    bigfan(R, 300, D + 470, 500, radius=120)
    bigfan(R, 760, D + 470, 400, radius=120)
    for (x, z) in ((100.0, 300.0), (470.0, 250.0), (800.0, -200.0), (700.0, 650.0)):
        ceil_light(R, x, z, D + HH, size=56, power=70, rng=820, color=(226, 236, 255))
    red_lamp(R, 470, 600, D + HH, power=56, rng=600)
    red_lamp(R, 0, -300, D + HH, power=56, rng=600)
    item(R, 'doc095fr', 40, ctop, CZ - 60)
    item(R, 'doc095frb', 160, D, -820)
    return (R, 'DEM', 'Bunker 095-FR (Indev). A lift down to SCP-095-FR, the Demon Core, on a copy of the Los Alamos bench, and a shielded control room.',
            2, 0.88, ((100, D + 165, -400), (470, D + 80, 250)))


def room2chrono():
    R = R_('room2chrono')
    AW = wmat('hcz', 384)
    junction(R, 'NS', 'hcz', openings={'hubE': [door_op(0)], 'S_W': [door_op(-500)]})
    lift(R, -192, -1, -500, 0, -500, UP, AW)
    x0, z0, x1, z1 = annex(R, 'x', 192, +1, -880, 880, 760, 600, 'hangar', door=0)
    plate6(R, 'chrono', 192, 0, 'W', yc=352, w=240)
    plate6(R, 'launch', -192, -500, 'E', yc=352, w=200)
    sign_at(R, 'elevator', -192, -760, 'E', 150, 50, 250)
    label6(R, '4255', 192, 250, 'W')
    # the hangar floor: workbenches with reindeer parts, the gift line, the BTKAI unit
    for z in (-500.0, -200.0):
        top = table(R, 400, z - 50, 620, z + 50)
        R.box(430, top, z - 30, 520, top + 40, z + 30, Mat('indev_kiosk.png', 64), lux=10)
        R.tube((560, top, z), (590, top + 70, z - 20), 3, LEAF.but(us=20), sides=5, coll=False, lux=20)
    R.box(900, 0, -700, 1000, 90, 700, METAL, skip='B', top=DARK, lux=10)
    for k in range(10):
        z = -640 + k * 136
        tbox(R, 920, 90, z, 976, 130, z + 50, PROPS6, PR6['wrap%d' % (k % 2)])
    plate6(R, 'giftline', x1, 0, 'W', yc=300, w=220)
    R.box(520, 0, -876, 760, 260, -800, Mat('indev_beige.png', 64), skip='B', lux=10)
    prop6(R, 'btkaifront', 640, -800, 'N', 230, 180, 140)
    neon6(R, 'btkai', 640, -800, 'N', 120, 60, 236)
    named(R, 'BTKAI', 640, 160, -796)
    plate6(R, 'btkai', 640, -880, 'N', yc=330, w=200)
    prop6(R, 'hourglass', x0, 400, 'E', 220, 220, 330)
    bigfan(R, 640, 590, 300, radius=150)
    for (x, z) in ((420, -400), (420, 400), (800, 0)):
        ceil_light(R, x, z, 600, size=96, power=120, rng=1100, color=(236, 242, 255))
    # the launch deck, up the lift: the sleigh on its rails, the eight reindeer, the hatch to the sky
    DX0, DX1, DZ = -192.0, 1016.0, 880.0
    out = [(DX0, -DZ), (DX0, DZ), (DX1, DZ), (DX1, -DZ)]
    DW = wmat('hangar', 520).but(v0=UP + 520)
    R.walls(out, UP, UP + 520, DW, holes={0: [span(out[0], (DX0, -596), (DX0, -404)) + (UP, UP + 320)]})
    R.rect_floor(DX0, -DZ, DX1, DZ, UP, Mat('scpcb_checkerplate.jpg', 128))
    R.rect_ceil(DX0, -DZ, DX1, DZ, UP + 520, DARK)
    sk = N6['sky']
    R.add([V(860, UP + 519, -600), V(160, UP + 519, -600), V(160, UP + 519, 800), V(860, UP + 519, 800)],
          [(sk[2], sk[3]), (sk[0], sk[3]), (sk[0], sk[1]), (sk[2], sk[1])], NEON6)
    R.light(510, UP + 480, 100, rng=1200, color=(150, 170, 255), power=60, ent=False)
    for x in (440.0, 580.0):
        R.box(x - 6, UP, -700, x + 6, UP + 8, 860, METAL, skip='B', lux=10)
    named(R, 'SLEIGH', 510, UP + 8, -300)
    for i in range(8):
        named(R, 'RD%d' % i, 450 + 120 * (i % 2), UP, -60 + 170 * (i // 2))
    named(R, 'ECHO', 300, UP, -300)
    named(R, 'CLANE', 300, UP, -520)
    ctop = desk(R, 80, -840, 300, -760, UP)
    for x in (130.0, 250.0):
        workstation(R, x, ctop, -800, 0)
    prop6(R, 'flightlog', 190, -DZ, 'N', 200, 100, UP + 200)
    for z in (-200.0, 300.0):
        R.box(DX1 - 60, UP, z - 60, DX1, UP + 220, z + 60, DARK, skip='B', lux=10)
        wall_decal(R, Mat('indev_crystal.png', emit=230, cast=False), DX1 - 60, z, 'W', 80, 160, UP + 120)
    plate6(R, 'launch', DX0, 200, 'E', yc=UP + 350, w=200)
    for (x, z) in ((100, -300), (100, 400), (800, -600)):
        ceil_light(R, x, z, UP + 520, size=72, power=90, rng=1000, color=(226, 236, 255))
    reserve(R, 'SLEIGHM')
    reserve(R, 'RDM', 8)
    lamps(R, NS3, 384, power=76, color=(232, 238, 255), size=36)
    item(R, 'doc4255', 300, 0, -700)
    item(R, 'doc4255b', 200, ctop, -790)
    return (R, 'CHR', 'Department of Chronology hangar (Indev): the SCP-4255-1 replica, its eight reindeer, and a lift up to the launch deck.',
            2, 0.08, ((300, 165, -650), (700, 160, 100)))


ALL = [room2yule, room2pinata, room2argos, room2demoncore, room2chrono]
