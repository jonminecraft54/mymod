"""The thirty-eighth batch: three new rooms, each with its own layout and purpose (code in IndevU38.bb).
Original SCP:CB textures and furniture wherever they do the job (ref96 walls and tiles after the user's images
148/149, white.jpg, wood.jpg, dirtymetal.jpg, metalpanels2.jpg, the office chairs and lockers); new textures only
for what the game has nothing for (make_assets38.py).

  room2b40infhall  LCZ  Corridor L-40 (ref. 148/149): one wide, tall white hallway the length of the room, pillars
                        and shutters, double doors with two big windows at the far end. Walking north it goes on
                        and on - the hallway loops back on you three times before it lets you reach the doors
  room2b40display  EZ   the SCP-1148 chamber off the corridor: a wall splits it, the entrance half brightly lit, the
                        far half dark, the window between them; through the east door the display hall / temporary
                        containment: seven pending-classification objects in glass cases and SCP-1039 on its plinth
  room2b40party    LCZ  the D-block holiday social: long tables, a buffet, paper chains and a banner - and a
                        birthday cake nobody brought (music: SFX\\Music\\SCP-x1x.ogg); through the east door the
                        vault with SCP-1117-1, the table that never empties
Everything is checked as before (no overlapping solids, doorways and aisles clear)."""
from rooms_b37 import *
import math

MIRROR = Mat('indev_b38mirror.png', cast=False)
PLAQUE = Mat('indev_b38plaque.png', cast=False)
GARLAND = Mat('indev_b38garland.png', alpha=True, cast=False)
BANNER = Mat('indev_b38banner.png', cast=False)
FROST = Mat('indev_b38frost.png', 64)
FOOD = Mat('indev_b38food.png', 96)
DOLLM = Mat('indev_b38doll.png', 32)
CLAY = Mat('concretefloor.jpg', 32)
WOODT = Mat('wood.jpg', 128)


def big_west(name, style, amb, key=0):
    extra = ", 'key': %d" % key if key else ''
    return wing33(name, style, {('W', 0): dict(style=style, span=980, depth=740, h=420, key=key)},
                  extra=[('E', 0)], amb=amb)


# ------------------------------------------------------------------------------------------------ the long hallway
def room2b40infhall():
    R = R_('room2b40infhall', amb=8)
    R.book = Book()
    B = R.book
    R.luxel = 16.0
    H = 448.0
    junction(R, 'NS', 'ref96', hub=(-320, -704, 320, 704), hh=H)
    B.areas.append((-320, 320, -704, 704, H))
    B.areas.append((-192, 192, -1024, 1024, 384))
    # pillars every 150 and a shutter in every other bay: the pattern repeats every 300, so the loop is seamless
    for k in range(9):
        z = -675 + 150 * k
        for (x0, x1) in ((-320, -290), (290, 320)):
            sbox(R, x0, 0, z - 15, x1, H, z + 15, WALL96.but(vs=H, v0=H), 'pillar %d %d' % (x0, k))
    for z in (-600, -300, 0, 300):
        shutter(R, -320, z, 'E', w=100, h=240)
        shutter(R, 320, z, 'W', w=100, h=240)
        ceiling_fixture(R, 0, z, H, power=40, rng=560)
    # the far end: a wall with double doors and two big windows
    holes = [(224, 416, 0, 320), (450, 620, 80, 300), (20, 190, 80, 300)]
    R.wall((320, 600), (-320, 600), 0, H, WALL96.but(vs=H, v0=H), holes=holes)
    R.wall((-320, 616), (320, 616), 0, H, WALL96.but(vs=H, v0=H), holes=holes)
    for x in (-96, 96):
        R.wall((x, 600), (x, 616), 0, 320, DARK)
        R.wall((x, 616), (x, 600), 0, 320, DARK)
    R.box(-96, 320, 600, 96, H, 616, WALL96, lux=12)
    for (a, b) in ((-300, -130), (130, 300)):
        glass_wall(R, (a, 608), (b, 608), 80, 300)
        R.box(a, 76, 598, b, 80, 618, METAL, lux=10)
        R.box(a, 300, 598, b, 304, 618, METAL, lux=10)
    solid(R, (-320, 0, 600, -96, H, 616), 'end wall W')
    solid(R, (96, 0, 600, 320, H, 616), 'end wall E')
    R.spawns.append(dict(kind='door', pos=(0, 0, 608), angle=0, key=0))
    named(R, 'ENDDOOR', 0, 160, 600)
    R.light(0, 300, 660, rng=420, color=(255, 236, 210), power=30)
    item(R, 'docb38_hall', -200, 0, -650)
    check33(R)
    return (R, 'INF', 'Corridor L-40 (Light Containment): one long, tall white hallway with pillars and shutters, and double doors with two big windows at the far end - which take a lot longer to reach than they should.',
            1, 0.5, ((0, 165, -650), (0, 150, 600)))


# ------------------------------------------------------------------------------------------------ display hall
CASES = [(420, -700), (820, -700), (420, -350), (820, -350), (420, 350), (820, 350), (420, 700)]


def case_object(R, k, x, z):
    y = 90
    if k == 0:                                                                # music box
        R.box(x - 16, y, z - 12, x + 16, y + 18, z + 12, WOODT, lux=10)
    elif k == 1:                                                              # snow globe
        R.prism(octo(x, z, 12, 6), y, y + 6, WOODT, caps='T')
        R.prism(octo(x, z, 11, 8), y + 6, y + 28, Mat('indev_b33shade.png', 32), caps='T')
    elif k == 2:                                                              # typewriter
        R.box(x - 22, y, z - 16, x + 22, y + 14, z + 16, DARK, lux=10)
        R.box(x - 20, y + 14, z - 2, x + 20, y + 22, z + 6, METAL, lux=10)
    elif k == 3:                                                              # rubber duck
        R.prism(octo(x, z, 9, 6), y, y + 12, Mat('yellow.jpg', 32) if False else YEL, caps='T')
        R.prism(octo(x + 6, z, 5, 6), y + 12, y + 20, YEL, caps='T')
    elif k == 4:                                                              # ceramic mask
        R.box(x - 12, y, z - 3, x + 12, y + 30, z + 3, WHITE, lux=10)
    elif k == 5:                                                              # teapot
        R.prism(octo(x, z, 13, 8), y, y + 18, WHITE, caps='T')
        R.tube((x + 12, y + 8, z), (x + 22, y + 18, z), 2, WHITE, sides=6, caps=True)
    else:                                                                     # pocket watch
        R.prism(octo(x, z, 9, 10), y, y + 3, YEL, caps='T')


def room2b40display():
    R, rooms = big_west('room2b40display', 'ez', amb=4)
    R.luxel = 16.0
    B = R.book
    WM, FM, CM = STYLES['ez']
    hub_dress(R, 'ez', [], pipes=False)
    # ---------------- west: the SCP-1148 chamber - lit entrance half, the window, the dark half
    holes = [(680, 1280, 60, 320)]
    R.wall((-640, ZB), (-640, -ZB), 0, HW, PLASTER.but(vs=HW, v0=HW), holes=holes)
    R.wall((-656, -ZB), (-656, ZB), 0, HW, PLASTER.but(vs=HW, v0=HW), holes=holes)
    for (a, b) in (((-656, -300), (-640, -300)), ((-640, 300), (-656, 300))):
        R.wall(a, b, 60, 320, METAL)
    R.box(-656, 56, -300, -640, 60, 300, METAL, lux=10)
    R.box(-656, 320, -300, -640, 324, 300, METAL, lux=10)
    glass_wall(R, (-648, -300), (-648, 300), 60, 320)
    decal30(R, MIRROR, -640, 0, 'E', 600, 260, 190, 'SCP-1148')
    for (box, n) in (((-656, 0, -ZB, -640, HW, -300), 'divider S'), ((-656, 0, 300, -640, HW, ZB), 'divider N'),
                     ((-656, 0, -300, -640, 60, 300), 'sill'), ((-656, 320, -300, -640, HW, 300), 'head')):
        solid(R, box, n)
    named(R, 'WINDOW', -640, 190, 0)
    for z in (-600, 0, 600):                                                  # never less than 100 W: bright
        R.light(-450, 360, z, rng=800, color=(255, 250, 240), power=95)
        ceiling_fixture(R, -450, z, HW, power=40, rng=500)
    office_desk(R, -520, -900, -400, -780, 'W', 'observation desk', chair=(-560, -840))
    item(R, 'docb38_1148', -470, 76, -860)
    sbox(R, -500, 0, 820, -400, 50, 900, CRATE35, 'chemlight crate')
    warn(R, 1, -256, -600, 'W', 220, 'warn lights')
    named(R, 'CAMW', -290, 340, -940)
    # ---------------- east: the display hall / temporary containment
    passage(R, 2, mat=WM.but(vs=320, v0=320))
    H = 480.0
    hall(R, 256, -1000, 1000, 1000, 0, H, WM.but(vs=H, v0=H), FM, CM, holes={'W': [(-96, 96, 0, 320)]})
    B.areas.append((256, 1000, -1000, 1000, H, 0))
    for k, (x, z) in enumerate(CASES):
        sbox(R, x - 50, 0, z - 50, x + 50, 90, z + 50, WHITE, 'case %d' % k)
        for (a, b) in (((x - 46, z - 46), (x + 46, z - 46)), ((x + 46, z - 46), (x + 46, z + 46)),
                       ((x + 46, z + 46), (x - 46, z + 46)), ((x - 46, z + 46), (x - 46, z - 46))):
            glass_wall(R, a, b, 90, 200)
        R.box(x - 48, 200, z - 48, x + 48, 204, z + 48, METAL, lux=10)
        case_object(R, k, x, z)
        u0, v0 = ((k + 1) % 2) * 0.5, ((k + 1) // 2) * 0.25
        f, xf = ('E', x + 50) if x < 620 else ('W', x - 50)
        decal30(R, PLAQUE, xf, z, f, 80, 40, 50, 'plaque %d' % k, uv=(u0, v0, u0 + 0.5, v0 + 0.25))
        named(R, 'CASE%d' % k, x, 140, z)
        pendant(R, x, z, H, drop=120, color=(255, 240, 220), power=36, rng=420)
    # SCP-1039 on its open plinth in the middle of the hall
    sbox(R, 580, 0, -40, 660, 100, 40, WHITE, 'doll plinth')
    R.box(612, 100, -8, 628, 132, 8, DOLLM, lux=10)
    R.prism(octo(620, 0, 9, 8), 132, 150, CLAY, caps='TB')
    R.tube((612, 104, -4), (600, 100, -10), 2.5, DOLLM, sides=6, caps=True)
    R.tube((628, 104, 4), (640, 100, 10), 2.5, DOLLM, sides=6, caps=True)
    decal30(R, PLAQUE, 580, 0, 'W', 80, 40, 50, 'plaque 1039', uv=(0, 0, 0.5, 0.25))
    named(R, 'DOLL', 620, 120, 0)
    named(R, 'DROP', 620, 10, 90)
    red_pendant(R, 620, 0, H, drop=140, power=50, rng=500)
    # the temporary containment lockers and the reception desk
    lockers(R, 'x', 1000, -1, -900, -300)
    solid(R, (970, 0, -900, 1000, 300, -300), 'pending lockers')
    decal30(R, LOGO35, 1000, 0, 'W', 160, 160, 260, 'hall emblem')
    table30(R, 280, 150, 380, 230, 'reception desk')
    item(R, 'docb38_register', 310, 78, 190)
    item(R, 'docb38_1039', 350, 78, 180)
    for z in (-600, 0, 600):
        ceiling_fixture(R, 620, z, H, power=36, rng=700)
    B.clear = [((480, 0, -990, 560, 200, 990), 'west aisle'), ((680, 0, -990, 760, 200, 990), 'east aisle')]
    check33(R)
    return (R, 'DSP', 'Display Hall (Entrance Zone): the SCP-1148 chamber, split by a wall between a brightly lit half and a dark half, and the display hall and temporary containment - pending objects in glass cases and SCP-1039 on its plinth.',
            3, 0.6, ((-300, 165, 0), (-640, 160, 0)))


# ------------------------------------------------------------------------------------------------ the party
def room2b40party():
    R, rooms = big_west('room2b40party', 'lcz', amb=8)
    R.luxel = 16.0
    B = R.book
    hub_dress(R, 'lcz', [], pipes=False)
    # ---------------- west: the D-block holiday social
    for (x0, x1) in ((-900, -820), (-700, -620)):
        for (z0, z1) in ((-860, -260), (260, 860)):
            table30(R, x0, z0, x1, z1, 'long table %d %d' % (x0, z0))
            for z in range(z0 + 60, z1, 150):
                model30(R, 'officeseat_a.x', x1 + 40, 0, z, 90, (50, 100, 50), 'chair %d %d' % (x0, z))
    table30(R, -900, 900, -480, 960, 'buffet')
    R.box(-896, 78, 904, -484, 82, 956, FOOD, lux=10)
    table30(R, -520, -560, -400, -440, 'cake table')
    R.prism(octo(-460, -500, 34, 12), 78, 116, FROST, caps='T')
    R.prism(octo(-460, -500, 24, 12), 116, 140, FROST, caps='T')
    for k in range(5):
        a = k * 1.2566
        R.tube((-460 + 14 * math.cos(a), 140, -500 + 14 * math.sin(a)), (-460 + 14 * math.cos(a), 152, -500 + 14 * math.sin(a)), 1.5, YEL, sides=6, caps=True)
    named(R, 'CAKE', -460, 120, -500)
    decal30(R, BANNER, XW, 0, 'E', 560, 140, 300, 'banner')
    for z, f in ((-ZB, 'N'), (ZB, 'S')):
        for x in (-820, -480):
            decal30(R, GARLAND, x, z, f, 320, 70, 360, 'garland %d %d' % (x, z))
    for (x, z, c) in ((-760, -600, (255, 80, 70)), (-760, 600, (90, 255, 110)), (-480, 0, (255, 220, 120))):
        R.light(x, 340, z, rng=700, color=c, power=40)
    for z in (-600, 0, 600):
        ceiling_fixture(R, -600, z, HW, power=40, rng=640)
    item(R, 'docb38_1117', -500, 78, 930)
    # ---------------- east: the SCP-1117-1 vault
    passage(R, 4, mat=BULKW.but(vs=320, v0=320))
    H = 380.0
    hall(R, 256, -500, 920, 500, 0, H, BULKW.but(vs=H, v0=H), Mat('concretefloor.jpg', 256), DARK,
         holes={'W': [(-96, 96, 0, 320)]})
    B.areas.append((256, 920, -500, 500, H, 0))
    sbox(R, 544, 70, -94, 656, 80, 94, WOODT, 'table top')
    for (x, z) in ((550, -88), (650, -88), (550, 88), (650, 88)):
        R.tube((x, 0, z), (x, 70, z), 3, WOODT, sides=6, caps=True)
    solid(R, (544, 0, -94, 656, 70, 94), 'table legs')
    R.box(548, 80, -90, 652, 92, 90, FOOD, lux=10)
    for (x, z, r) in ((570, -50, 14), (630, 40, 16), (600, 70, 10), (580, 20, 12)):
        R.prism(octo(x, z, r, 8), 92, 104, WHITE, caps='T')
        R.prism(octo(x, z, r * 0.7, 8), 104, 112, FOOD, caps='T')
    named(R, 'TABLE', 600, 100, 0)
    pendant(R, 600, 0, H, drop=110, color=(255, 210, 150), power=50, rng=520)
    warn(R, 1, 920, 0, 'W', 200, 'vault warning')
    decal30(R, LOGO35, 256, -300, 'E', 90, 90, 220, 'vault emblem')
    check33(R)
    return (R, 'PTY', 'D-Block Social (Light Containment): the holiday party room - long tables, a buffet, paper chains and a banner, and a birthday cake nobody brought - and the vault with SCP-1117-1, the table that never empties.',
            1, 0.6, ((-300, 165, 0), (-700, 120, -400)))


ALL = [room2b40infhall, room2b40display, room2b40party]
