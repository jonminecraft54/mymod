"""The thirty-ninth batch: three very big rooms - each fills the whole map cell as one open space (2000 x 1720
inside), no side corridor - and five new SCPs (code in IndevU39.bb). Reference photos 150-161: dark concrete
(150), the observation window onto a test chamber with a guard on a balcony (152), the tunnel steps (153), the
tiered cell block with the emblem in the floor (154), the crate-lined storage tunnel (156), the red SCP stencil on
concrete (157), the pillared concrete hall with wall lamps (158), the vehicle bay (159 - reused as the warehouse
loading lane), and a home kitchen and living room (159-161 - remade as the research staff lounge: wood-plank
ceiling, brick fireplace, armchairs, a kitchenette with a checkered splashback). Original textures reused
throughout (concrete, crates, stencil, tiles, wood, metal, glass); new ones only where nothing fitted.

  room2b41research  EZ   Research Department: glass-walled labs (SCP-586, SCP-1176), open-plan desks, a
                         whiteboard bay and the staff lounge
  room2b41warehouse LCZ  Warehouse B: a pillared concrete hall, pallets of crates, the red stencil, two blocks of
                         barred containment cells (SCP-1562's slide in one), SCP-1370 in its glass case
  room2b41testcon   HCZ  Test Containment 4: a white observation hall with a balcony, the big window onto the test
                         chamber - and in it SCP-1013
Everything checked as before (no overlapping solids, the through-aisle and doorways clear)."""
from rooms_b38 import *
import math

BRICK = Mat('indev_b39brick.png', 192)
CARPET = Mat('indev_b39carpet.png', 192)
HONEY = Mat('indev_b39honey.png', 96, emit=40)
MUMMY = Mat('indev_b39mummy.png', 64)
GREEN = Mat('indev_b39green.png', 32)
SCALES = Mat('indev_b39scales.png', 48)
METER = Mat('indev_b39meter.png', cast=False)
X0, X1, Z0, Z1 = -1000.0, 1000.0, -860.0, 860.0


def big_hall(name, style, hh, amb):
    R = R_(name, amb=amb)
    R.book = Book()
    R.luxel = 18.0
    junction(R, 'NS', style, hub=(X0, Z0, X1, Z1), hh=hh)
    R.book.areas.append((X0, X1, Z0, Z1, hh))
    R.book.areas.append((-192, 192, -1024, 1024, 384))
    return R, R.book


def glass_room(R, xa, xb, za, zb, door_side, door_c, name):
    """a lab walled in glass on its open sides (x = xa / z = zb faces), metal posts, one doorway"""
    walls = []
    if door_side in ('xa', 'xb'):
        x = xa if door_side == 'xa' else xb
        walls += [((x, za), (x, door_c - 70)), ((x, door_c + 70), (x, zb - 4))]
    for (a, b) in walls:
        glass_wall(R, a, b, 0, 300)
        solid(R, (a[0] - 3, 0, min(a[1], b[1]), a[0] + 3, 300, max(a[1], b[1])), '%s glass %d' % (name, a[1]))
        R.box(a[0] - 4, 300, min(a[1], b[1]), a[0] + 4, 308, max(a[1], b[1]), METAL, lux=10)
    zc = zb if za < 0 else za
    x_lo, x_hi = (xa, xb) if xa < xb else (xb, xa)
    glass_wall(R, (x_lo, zc), (x_hi, zc), 0, 300)
    solid(R, (x_lo, 0, zc - 3, x_hi, 300, zc + 3), '%s glass front' % name)
    R.box(x_lo, 300, zc - 4, x_hi, 308, zc + 4, METAL, lux=10)


# ------------------------------------------------------------------------------------------------ research
def room2b41research():
    H = 448.0
    R, B = big_hall('room2b41research', 'ez', H, 8)
    # SCP-586's lab (south-west) and SCP-1176's lab (south-east), glass on two sides
    glass_room(R, -480, X0, Z0, -300, 'xa', -560, 'lab 586')
    glass_room(R, 480, X1, Z0, -300, 'xa', -560, 'lab 1176')
    sbox(R, -780, 0, -640, -700, 100, -560, WHITE, 'plinth 586')
    R.prism(octo(-740, -600, 16, 7), 100, 118, GREEN, caps='TB')
    named(R, 'S586', -740, 110, -600)
    for z in (-820, -700):
        office_desk(R, -980, z - 40, -880, z + 60, 'E', 'typing desk %d' % z, chair=(-850, z + 10), lamp=False)
        R.box(-960, 76, z - 10, -920, 90, z + 30, DARK, lux=10)                      # typewriters
    item(R, 'docb39_586', -940, 76, -690)
    sbox(R, 660, 0, -660, 860, 80, -560, Mat('concretefloor.jpg', 64), 'sarcophagus')
    R.rect_floor(668, -652, 852, -568, 80.5, HONEY)
    R.box(700, 70, -625, 820, 79, -595, MUMMY, lux=10)
    R.tube((860, 30, -610), (884, 30, -610), 4, METAL, sides=6, caps=True)        # the faucet
    named(R, 'FAUCET', 880, 40, -610)
    named(R, 'S1176', 760, 90, -610)
    table30(R, 900, -840, 990, -720, 'honey jars table')
    item(R, 'docb39_1176', 940, 78, -780)
    R.light(760, 250, -610, rng=520, color=(255, 210, 140), power=40)
    # the open-plan desks either side of the aisle
    for x0 in (-440, 220):
        for z in (-200, 40):
            office_desk(R, x0, z, x0 + 120, z + 100, 'S', 'desk %d %d' % (x0, z), chair=(x0 + 60, z - 30))
            office_desk(R, x0 + 140, z, x0 + 220, z + 100, 'S', 'desk b %d %d' % (x0, z), chair=(x0 + 180, z - 30), lamp=False)
    # the whiteboard bay (north-east)
    for x in (500, 760):
        decal30(R, WB, x, Z1, 'S', 220, 110, 200, 'whiteboard %d' % x)
    for z in (380, 640):
        console30(R, 960, z, 'W', 'analysis console %d' % z)
    table30(R, 520, 520, 760, 640, 'meeting table')
    for x in (560, 640, 720):
        model30(R, 'officeseat_a.x', x, 0, 680, 180, (50, 100, 50), 'meeting chair %d' % x)
    # the staff lounge (north-west): carpet, a wood-plank ceiling, brick fireplace, armchairs, kitchenette
    R.rect_floor(X0, 300, -450, Z1, 0.6, CARPET)
    R.box(X0, 320, 300, -450, 328, Z1, WOODT, lux=12)
    R.wall((-700, 300), (X0, 300), 0, 320, PLASTER.but(vs=320, v0=320))
    R.wall((X0, 300), (-700, 300), 0, 320, PLASTER.but(vs=320, v0=320))
    solid(R, (X0, 0, 296, -700, 320, 304), 'lounge wall')
    sbox(R, X0, 0, 480, -930, 180, 700, BRICK, 'fireplace')
    R.box(-930, 20, 540, -928, 110, 640, DARK, lux=10)
    R.box(-935, 180, 470, -910, 188, 710, WOODT, lux=10)                            # the mantel
    R.light(-900, 60, 590, rng=300, color=(255, 140, 60), power=30)
    for (x, z) in ((-760, 520), (-760, 660)):
        sbox(R, x - 40, 0, z - 40, x + 40, 50, z + 40, DARK, 'armchair %d' % z)
        R.box(x + 30, 50, z - 40, x + 40, 110, z + 40, DARK, lux=10)
    table30(R, -660, 560, -600, 620, 'side table', h=55.0)
    sbox(R, X0, 0, 800, -700, 90, Z1, WOODT, 'kitchen counter')
    decal30(R, CHECKER, -850, Z1, 'S', 300, 80, 140, 'splashback')
    sbox(R, -680, 0, 790, -600, 200, Z1, METAL, 'fridge')
    for x in (-800, -600):
        pendant(R, x, 600, 320, drop=60, color=(255, 230, 190), power=36, rng=420)
    item(R, 'firstaid', -820, 90, 830, chance=60)
    # light
    for x in (-600, 0, 600):
        for z in (-500, 0, 500):
            if not (x == -600 and z == 500):
                ceiling_fixture(R, x, z, H, power=58, rng=780)
    decal30(R, LOGO35, X1, 0, 'W', 200, 200, 280, 'department emblem')
    B.clear = [((-110, 0, -850, 110, 200, 850), 'the aisle')]
    check33(R)
    return (R, 'RES', 'Research Department (Entrance Zone): one big open floor - the glass labs of SCP-586 and SCP-1176, open-plan desks, a whiteboard bay and the staff lounge with its fireplace and kitchenette.',
            3, 0.65, ((0, 165, -700), (-600, 120, -500)))


# ------------------------------------------------------------------------------------------------ warehouse
def room2b41warehouse():
    H = 600.0
    R, B = big_hall('room2b41warehouse', 'conc36', H, 14)
    # ref. 158: the square concrete pillars
    for x in (-650, -300, 300, 650):
        for z in (-560, -160, 240):
            sbox(R, x - 40, 0, z - 40, x + 40, H, z + 40, CONC36.but(vs=H, v0=H), 'pillar %d %d' % (x, z))
    # ref. 156: pallets and crate stacks between the pillars
    rnd = random.Random(392)
    for x in (-850, -480, 480, 850):
        for z in (-760, -360, 40):
            sbox(R, x - 70, 0, z - 60, x + 70, 12, z + 60, Mat('wood.jpg', 128), 'pallet %d %d' % (x, z))
            hgt = 12
            for lvl in range(rnd.randint(1, 3)):
                sbox(R, x - 64 + lvl * 4, hgt, z - 54, x + 64 - lvl * 4, hgt + 56, z + 54, CRATE35, 'crates %d %d %d' % (x, z, lvl))
                hgt += 56
    # ref. 157: the red stencil
    decal30(R, SCPST, X0, -400, 'E', 260, 130, 260, 'stencil W')
    decal30(R, SCPST, X1, -400, 'W', 260, 130, 260, 'stencil E')
    # the containment blocks: barred cells along the north wall, west and east of the aisle
    for (xa, xb, tag) in ((X0, -400, 'W'), (400, X1, 'E')):
        w = (xb - xa) / 3
        for k in range(4):
            x = xa + k * w
            if 0 < k < 3:
                sbox(R, x - 8, 0, 500, x + 8, 360, Z1, CONC36.but(vs=360, v0=360), 'cell wall %s %d' % (tag, k))
        R.box(xa, 360, 500, xb, 376, Z1, CONC36, lux=12)
        for k in range(3):
            c0, c1 = xa + k * w + 10, xa + (k + 1) * w - 10
            n = int((c1 - c0) / 24)
            for i in range(n + 1):
                x = c0 + (c1 - c0) * i / n
                if tag == 'E' and k == 1 and abs(x - (c0 + c1) / 2) < 50:
                    continue                                                 # the slide cell's gate stands open
                R.tube((x, 0, 500), (x, 360, 500), 2.5, DARK, sides=6, caps=False)
            for y in (120, 240):
                R.tube((c0, y, 500), (c1, y, 500), 2.5, DARK, sides=6, caps=False)
            if tag == 'E' and k == 1:
                gap = (c0 + c1) / 2
                solid(R, (c0, 0, 497, gap - 50, 360, 503), 'bars E1a')
                solid(R, (gap + 50, 0, 497, c1, 360, 503), 'bars E1b')
            else:
                solid(R, (c0, 0, 497, c1, 360, 503), 'bars %s %d' % (tag, k))
            R.light((c0 + c1) / 2, 320, 700, rng=360, color=(255, 236, 210), power=24)
        for k in range(3):
            c = xa + (k + 0.5) * w
            if not (tag == 'E' and k == 1):
                sbox(R, c - 60, 0, 640, c + 60, 70, 760, CRATE35, 'sealed crate %s %d' % (tag, k))
    # SCP-1562: the slide, in the middle east cell
    sx = 400 + (X1 - 400) / 2
    for dx in (-36, 36):
        R.tube((sx + dx, 0, 820), (sx + dx, 250, 820), 4, METAL, sides=6, caps=True)  # ladder posts
    for y in range(30, 250, 40):
        R.tube((sx - 36, y, 820), (sx + 36, y, 820), 2.5, METAL, sides=6, caps=False)
    for i in range(7):
        x = sx - 30 + i * 10
        R.tube((x, 220, 800), (x, 30, 580), 4, Mat('dirtymetal.jpg', 64), sides=6, caps=True)
    for dx in (-36, 36):
        R.tube((sx + dx, 240, 800), (sx + dx, 50, 580), 3, METAL, sides=6, caps=True)
    solid(R, (sx - 40, 0, 560, sx + 40, 250, 830), 'SCP-1562')
    named(R, 'SLIDE', sx, 120, 560)
    item(R, 'docb39_1562', sx + 120, 0, 560)
    # SCP-1370 in its glass case, beside the aisle
    sbox(R, 200, 0, -80, 320, 60, 40, WHITE, '1370 case base')
    for (a, b) in (((200, -80), (320, -80)), ((320, -80), (320, 40)), ((320, 40), (200, 40)), ((200, 40), (200, -80))):
        glass_wall(R, a, b, 60, 220)
    R.box(200, 220, -80, 320, 224, 40, METAL, lux=10)
    R.box(244, 60, -30, 276, 130, -10, METAL, lux=10)
    R.box(248, 130, -32, 272, 156, -8, METER, lux=10)
    for dx in (-22, 22):
        R.tube((260 + dx * 0.6, 120, -20), (260 + dx, 80, -20), 3, METAL, sides=6, caps=True)
    named(R, 'R1370', 260, 140, -20)
    decal30(R, PLAQUE, 320, -20, 'E', 70, 35, 40, 'plaque 1370', uv=(0, 0, 0.5, 0.25))
    item(R, 'docb39_1370', 140, 0, -60)
    # ref. 158: wall lamps, high fixtures
    for z in (-700, -300, 100, 400):
        for (x, f) in ((X0, 'E'), (X1, 'W')):
            R.box(x - 6 if f == 'W' else x, 240, z - 18, x + 6 if f == 'E' else x, 270, z + 18, LIGHTPANEL, lux=10)
            R.light(x + (40 if f == 'E' else -40), 255, z, rng=520, color=(255, 220, 160), power=52)
    for z in (-600, -100, 300):
        ceiling_fixture(R, 0, z, H, power=72, rng=900)
    B.clear = [((-110, 0, -850, 110, 200, 850), 'the aisle'), ((sx - 50, 0, 504, sx + 50, 200, 556), 'the slide cell gate')]
    check33(R)
    return (R, 'WHB', 'Warehouse B (Light Containment): a pillared concrete hall of crated pallets, the red stencil, barred containment cells along the north wall - SCP-1562\'s slide in one - and SCP-1370 in its glass case.',
            1, 0.65, ((0, 165, -700), (500, 120, 600)))


# ------------------------------------------------------------------------------------------------ test containment
def room2b41testcon():
    H = 640.0
    R, B = big_hall('room2b41testcon', 'plaster37', H, 12)
    # ceiling beams (ref. 152)
    for z in (-600, -200, 200, 600):
        R.box(X0, H - 50, z - 20, X1, H, z + 20, Mat('dirtymetal.jpg', 128), lux=12)
    # the test chamber: x 420..1000, z -700..700, a heavy window in its west wall and a sealed door
    XC = 420.0
    holes = [(300, 1100, 80, 380), (1300, 1400 - 10, 0, 300)]
    R.wall((XC, 700), (XC, -700), 0, H, PLASTER.but(vs=H, v0=H), holes=[(300, 1100, 80, 380), (1150, 1290, 0, 300)])
    R.wall((XC + 24, -700), (XC + 24, 700), 0, H, PLASTER.but(vs=H, v0=H), holes=[(300, 1100, 80, 380), (110, 250, 0, 300)])
    R.wall((XC, -700), (X1, -700), 0, H, PLASTER.but(vs=H, v0=H))
    R.wall((X1, -700), (XC, -700), 0, H, PLASTER.but(vs=H, v0=H))
    R.wall((X1, 700), (XC, 700), 0, H, PLASTER.but(vs=H, v0=H))
    R.wall((XC, 700), (X1, 700), 0, H, PLASTER.but(vs=H, v0=H))
    R.collide_wall((XC + 12, -400), (XC + 12, 400), 80, 380)                    # clear: you see straight in
    R.collide_wall((XC + 12, 400), (XC + 12, -400), 80, 380)
    R.box(XC - 30, 380, -440, XC + 54, 420, 440, Mat('red.jpg', 64), lux=10)       # the red band over the frame
    for z in (-420, 420):
        R.box(XC - 30, 0, z - 20, XC + 54, 420, z + 20, Mat('dirtymetal.jpg', 64), lux=10)
    R.box(XC - 30, 60, -420, XC + 54, 80, 420, Mat('dirtymetal.jpg', 64), lux=10)
    for (box, nm) in (((XC, 0, -700, XC + 24, H, -590), 'chamber wall a'), ((XC, 0, -450, XC + 24, H, 700), 'chamber wall b'),
                      ((XC, 0, 700, X1, H, 704), 'chamber wall N'), ((XC, 0, -704, X1, H, -700), 'chamber wall S')):
        solid(R, box, nm)
    R.spawns.append(dict(kind='door', pos=(XC + 12, 0, -520), angle=90, key=4))
    B.areas.append((XC + 24, X1, -700, 700, H, 0))
    # in the chamber: SCP-1013 on a bed of grit, calcified remains, the tail curled round
    R.rect_floor(700, 100, 960, 500, 0.6, Mat('concretefloor.jpg', 64))
    sbox(R, 790, 0, 290, 850, 18, 330, SCALES, 'SCP-1013 body')
    R.prism(octo(860, 310, 8, 6), 18, 40, SCALES, caps='T')
    R.box(866, 34, 298, 880, 44, 322, Mat('red.jpg', 32), lux=10)                  # wattle and comb
    R.box(852, 30, 290, 856, 52, 330, SCALES, lux=10)                              # the frill
    pts = [(790, 6, 310), (750, 5, 340), (720, 5, 300), (740, 5, 250), (780, 5, 240)]
    for a, b in zip(pts, pts[1:]):
        R.tube(a, b, 3, SCALES, sides=6, caps=True)
    named(R, 'LIZARD', 862, 40, 310)
    for (x, z) in ((720, 420), (900, 160)):
        R.prism(octo(x, z, 22, 8), 0, 30, Mat('white.jpg', 32), caps='T')         # calcified remains
    named(R, 'DCLASS', 600, 0, -150)
    R.light(720, 520, 0, rng=900, color=(255, 246, 236), power=60)
    # the observation side: a balcony along the west wall with stairs, the guard, consoles at the window
    sbox(R, X0, 280, -700, -760, 300, 700, Mat('dirtymetal.jpg', 128), 'balcony', skip='')
    rail_z(R, -764, -696, 380, 300, 'balcony rail')
    for i in range(10):
        za, zb = 400 + 30 * i, 430 + 30 * i
        top = 300 - 30 * (i + 1)
        sbox(R, -760, max(top - 22, 0), za, -660, top, zb, CHECKER, 'step %d' % i)
    R.tube((-656, 400, 400), (-656, 100, 700), 3.5, METAL, sides=6, caps=True)
    solid(R, (-660, 0, 400, -652, 404, 700), 'stair rail')
    for (x, z) in ((X0, -300), (X0, 100)):
        decal30(R, Mat('vent.jpg', cast=False) if False else DARK, x, z, 'E', 80, 60, 120, 'vent %d' % z)
    named(R, 'GUARD', -880, 300, -300)
    for z in (-300, -100, 100, 300):
        console30(R, 340, z, 'E', 'window console %d' % z)
    named(R, 'WINDOW', XC, 230, 0)
    item(R, 'docb39_1013', 300, 0, -560)
    for x in (-600, -100):
        for z in (-500, 0, 500):
            ceiling_fixture(R, x, z, H - 50, power=66, rng=880)
    red_emergency(R, XC, 500, -560, 'W', 'red chamber')
    B.clear = [((-110, 0, -850, 110, 200, 850), 'the aisle'), ((-990, 300, -690, -780, 500, 690), 'balcony walk')]
    check33(R)
    return (R, 'TST', 'Test Containment 4 (Heavy Containment): a tall white observation hall with a guard balcony and a big window onto the test chamber - and SCP-1013 inside it. Do not meet its eyes.',
            2, 0.6, ((-300, 165, 0), (420, 200, 0)))


ALL = [room2b41research, room2b41warehouse, room2b41testcon]
