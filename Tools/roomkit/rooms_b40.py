"""The fortieth batch: the Residential Sector - twelve connected house rooms in three wings, an abandoned home
rebuilt inside the facility (code in IndevU40.bb). Each wing is a concrete facility corridor (the original
concrete, floor, ceiling lights and doors) with four house rooms off it - two each side, joined to each other by an
inner doorway - so all twelve connect. House surfaces: wallpaper, carpet, wood floors and doors, lamps; one or two
unique features per room, as the user asked, to keep it light.

  room2b42house1  the living floor: Living Room (the television still on), Dining Room (a table set for six),
                  Kitchen (the radio-cassette with SCP-1220's tape), Residential Hallway (doors, doors, doors)
  room2b42house2  the bedrooms: the Sealed Bedroom (SCP-1197, a Foundation warning on the door), Bathroom (the
                  flickering tube), Children's Playroom (toys - and SCP-1192 in a birdcage), Attic Storage (dust
                  sheets over everything)
  room2b42house3  below stairs: Basement Storage (SCP-1355's boxes), the Garage (an old car - and SCP-1196's
                  chairs), the Model House (a perfect miniature of this house), the Foundation Safehouse
Everything is checked as before (no overlapping solids, doorways and corridor clear)."""
from rooms_b39 import *

PAPER1 = Mat('indev_b40paper1.png', 512)
PAPER2 = Mat('indev_b40paper2.png', 512)
WDOOR = Mat('indev_b40door.png', cast=False)
TVM = Mat('indev_b40tv.png', cast=False, emit=160)
DRAW = Mat('indev_b40drawing.png', cast=False)
LABELM = Mat('indev_b40labels.png', 96)
SHEET = Mat('indev_b40sheet.png', 96)
WOODF = Mat('wood.jpg', 160)
CONCF = Mat('concretefloor.jpg', 256)
FAB = Mat('indev_b39carpet.png', 64)            # upholstery
H = 320.0                                        # house ceiling height
ROOMS = {('W', 'S'): (-1000, -256, -860, -20), ('W', 'N'): (-1000, -256, 20, 860),
         ('E', 'S'): (256, 1000, -860, -20), ('E', 'N'): (256, 1000, 20, 860)}


def res_wing(name, amb, keys=None, specs=None):
    """the corridor and four house rooms; specs[(side, half)] = (wall, floor, ceil); keys[(side, half)] = door key"""
    R = R_(name, amb=amb + 6)
    R.book = Book()
    B = R.book
    R.luxel = 16.0
    junction(R, 'NS', 'conc36', hub=(-192, -860, 192, 860),
             openings={'hubW': [door_op(-430), door_op(430)], 'hubE': [door_op(-430), door_op(430)]})
    B.areas.append((-192, 192, -1024, 1024, 384))
    for (side, half), (x0, x1, z0, z1) in ROOMS.items():
        s = -1 if side == 'W' else 1
        c = -430 if half == 'S' else 430
        wall, floor, ceil = specs[(side, half)]
        hall(R, min(192 * s, 256 * s), c - 96, max(192 * s, 256 * s), c + 96, 0, 320, CONC36.but(vs=320, v0=320), FLOOR36, DARK,
             holes={'W': [(c - 96, c + 96, 0, 320)], 'E': [(c - 96, c + 96, 0, 320)]})
        B.areas.append((min(192 * s, 256 * s), max(192 * s, 256 * s), c - 96, c + 96, 320, 0))
        R.spawns.append(dict(kind='door', pos=(224 * s, 0, c), angle=90, key=(keys or {}).get((side, half), 0)))
        xa, xb = (-680, -560) if s < 0 else (560, 680)
        inner = 'N' if half == 'S' else 'S'
        hall(R, x0, z0, x1, z1, 0, H, wall.but(vs=H, v0=H), floor, ceil,
             holes={('E' if s < 0 else 'W'): [(c - 96, c + 96, 0, 320)], inner: [(xa, xb, 0, 260)]})
        B.areas.append((x0, x1, z0, z1, H, 0))
    for s in (-1, 1):                                                         # the inner doorways S <-> N
        xa, xb = (-680, -560) if s < 0 else (560, 680)
        hall(R, xa, -20, xb, 20, 0, 260, Mat('wood.jpg', 64), WOODF, DARK,
             holes={'S': [(xa, xb, 0, 260)], 'N': [(xa, xb, 0, 260)]})
        B.areas.append((xa, xb, -20, 20, 260, 0))
    # the corridor: original concrete, fixtures, a sector sign
    for z in (-600, 0, 600):
        ceiling_fixture(R, 0, z, 384, power=46, rng=600)
    warn(R, 1, 192, 0, 'W', 220, 'sector sign')
    decal30(R, LOGO35, -192, 0, 'E', 90, 90, 230, 'sector emblem')
    return R, B


def lamp(R, x, z, power=40, color=(255, 214, 160)):
    pendant(R, x, z, H, drop=60, color=color, power=power * 1.6, rng=720)


def sofa(R, x0, z0, x1, z1, name, back='W'):
    sbox(R, x0, 0, z0, x1, 42, z1, FAB, name)
    if back in ('W', 'E'):
        xb = (x0, x0 + 16) if back == 'W' else (x1 - 16, x1)
        R.box(xb[0], 42, z0, xb[1], 90, z1, FAB, lux=10)
    else:
        zb = (z0, z0 + 16) if back == 'S' else (z1 - 16, z1)
        R.box(x0, 42, zb[0], x1, 90, zb[1], FAB, lux=10)


def chair_w(R, x, z, name):
    sbox(R, x - 20, 0, z - 20, x + 20, 44, z + 20, WOODF, name)
    R.box(x - 20, 44, z + 16, x + 20, 96, z + 20, WOODF, lux=10)


# ------------------------------------------------------------------------------------------------ the living floor
def room2b42house1():
    specs = {('W', 'S'): (PAPER1, CARPET, WOODT), ('W', 'N'): (PAPER2, WOODF, WHITE),
             ('E', 'S'): (PAPER2, CHECKER, WHITE), ('E', 'N'): (PAPER1, WOODF, WHITE)}
    R, B = res_wing('room2b42house1', 9, specs=specs)
    # Living Room (W, S): the television still on, a sofa, an armchair, the stove
    sofa(R, -960, -700, -880, -460, 'sofa', back='W')
    sofa(R, -640, -820, -560, -740, 'armchair', back='S')
    table30(R, -760, -640, -680, -520, 'coffee table', h=40.0)
    sbox(R, -560, 0, -260, -380, 60, -200, WOODF, 'tv stand')
    R.box(-540, 60, -232, -400, 160, -212, DARK, lux=10)
    decal30(R, TVM, -470, -233, 'S', 128, 90, 110, 'tv screen')
    named(R, 'TV', -470, 110, -240)
    sbox(R, -960, 0, -260, -880, 110, -180, Mat('white.jpg', 64), 'stove')
    R.light(-470, 110, -320, rng=420, color=(150, 170, 220), power=30)
    lamp(R, -700, -500)
    # Dining Room (W, N): a table set for six
    table30(R, -760, 300, -560, 600, 'dining table')
    for (x, z) in ((-700, 350), (-620, 350), (-700, 450), (-620, 450), (-700, 550), (-620, 550)):
        R.prism(octo(x, z, 16, 8), 78, 80, WHITE, caps='T')                         # plates
    for z in (350, 450, 550):
        chair_w(R, -800, z, 'dining chair W %d' % z)
        chair_w(R, -520, z, 'dining chair E %d' % z)
    sbox(R, -980, 0, 300, -940, 180, 600, WOODF, 'sideboard')
    lamp(R, -660, 450, power=46)
    named(R, 'TABLE6', -660, 90, 450)
    # Kitchen (E, S): counters, the fridge, the radio-cassette with SCP-1220's tape
    sbox(R, 940, 0, -840, 1000, 90, -300, WOODF, 'counter')
    decal30(R, CHECKER, 1000, -570, 'W', 520, 80, 140, 'splashback')
    sbox(R, 900, 0, -280, 1000, 200, -200, METAL, 'fridge')
    table30(R, 520, -600, 680, -480, 'kitchen table')
    R.box(580, 78, -560, 620, 98, -540, DARK, lux=10)
    named(R, 'TAPE', 600, 90, -550)
    item(R, 'docb40_1220', 540, 78, -520)
    for (x, z) in ((480, -540), (720, -540)):
        chair_w(R, x, z, 'kitchen chair %d' % x)
    lamp(R, 600, -540)
    ceiling_fixture(R, 900, -600, H, power=30, rng=420)
    # Residential Hallway (E, N): a rug, coats, and doors - lots of doors
    R.rect_floor(400, 300, 900, 560, 0.6, FAB)
    for k, z in enumerate((150, 350, 550, 750)):
        decal30(R, WDOOR, 1000, z, 'W', 100, 220, 110, 'hall door E %d' % k)
    for k, x in enumerate((450, 800)):
        decal30(R, WDOOR, x, 860, 'S', 100, 220, 110, 'hall door N %d' % k)
    named(R, 'DOORS', 990, 110, 350)
    sbox(R, 300, 0, 780, 340, 180, 840, WOODF, 'coat stand')
    decal30(R, DRAW, 256, 600, 'E', 70, 70, 160, 'hall picture')
    item(R, 'docb40_house', 600, 0, 500)
    for z in (250, 650):
        lamp(R, 650, z, power=34)
    check33(R)
    return (R, 'HS1', 'Residential Sector - the living floor (Light Containment): a living room with the television still on, a dining room set for six, the kitchen with SCP-1220\'s cassette, and a hallway of doors.',
            1, 0.7, ((-300, 165, -430), (-470, 110, -240)))


# ------------------------------------------------------------------------------------------------ the bedrooms
def room2b42house2():
    specs = {('W', 'S'): (PAPER2, CARPET, WHITE), ('W', 'N'): (Mat('indev_b33tile.png', 128), TILE96, WHITE),
             ('E', 'S'): (PAPER1, CARPET, WHITE), ('E', 'N'): (Mat('wood.jpg', 256), WOODF, WOODT)}
    R, B = res_wing('room2b42house2', 9, specs=specs, keys={('W', 'S'): 3})
    decal30(R, Mat('indev_b36warn.png', cast=False), -192, -620, 'E', 80, 80, 200, 'bedroom warning',
            uv=(0.5, 0, 1, 0.5))
    # the Sealed Bedroom (W, S) - SCP-1197: bed, TV, mini-fridge, telephone, and SCP-1197-1 in the west wall
    sbox(R, -900, 0, -820, -700, 50, -620, Mat('white.jpg', 64), 'bed')
    R.box(-900, 50, -820, -880, 110, -620, WOODF, lux=10)
    sbox(R, -680, 0, -840, -620, 60, -780, WOODF, 'nightstand')
    R.box(-670, 60, -830, -640, 72, -810, DARK, lux=10)                              # the telephone
    named(R, 'PHONE', -655, 70, -820)
    sbox(R, -400, 0, -300, -320, 70, -240, METAL, 'mini fridge')
    sbox(R, -560, 0, -260, -440, 60, -200, WOODF, 'tv cabinet')
    R.box(-540, 60, -232, -460, 120, -212, DARK, lux=10)
    decal30(R, WDOOR, -1000, -300, 'E', 100, 220, 110, 'SCP-1197-1')
    named(R, 'D1197', -990, 110, -300)
    named(R, 'DUP', -900, 0, -300)
    item(R, 'docb40_1197', -650, 72, -790)
    lamp(R, -700, -500, power=40)
    # the Bathroom (W, N): tub, toilet, sink - and the fluorescent tube that will not settle
    sbox(R, -1000, 0, 700, -840, 60, 860, WHITE, 'bathtub')
    cell_dress(R, -1000, 300, 640, -1, 'bath')
    R.box(-620, H - 6, 430, -560, H, 470, METAL, bottom=LIGHTPANEL, lux=10)
    R.light(-590, H - 30, 450, rng=520, color=(230, 240, 255), power=40)
    named(R, 'TUBE', -590, H - 20, 450)
    # the Children's Playroom (E, S): blocks, a rocking horse, a toy box, drawings - and SCP-1192 in a cage
    rnd = random.Random(1192)
    for k in range(14):
        x, z = rnd.uniform(560, 900), rnd.uniform(-800, -500)
        c = rnd.choice((Mat('red.jpg', 32), YEL, Mat('indev_b33shade.png', 32), WHITE))
        R.box(x, 0, z, x + 16, 16, z + 16, c, lux=10)
    sbox(R, 900, 0, -300, 1000, 70, -200, WOODF, 'toy box')
    sbox(R, 700, 0, -320, 760, 90, -240, WOODF, 'rocking horse')
    for k, z in enumerate((-700, -500)):
        decal30(R, DRAW, 1000, z, 'W', 120, 120, 150, 'drawing %d' % k)
    sbox(R, 360, 0, -820, 440, 100, -740, WOODF, 'cage stand')
    for i in range(10):
        a = i * 0.628
        R.tube((400 + 30 * math.cos(a), 100, -780 + 30 * math.sin(a)), (400 + 30 * math.cos(a), 190, -780 + 30 * math.sin(a)), 1.2, YEL, sides=4, caps=False)
    R.prism(octo(400, -780, 30, 10), 190, 196, YEL, caps='T')
    R.prism(octo(400, -780, 9, 6), 110, 130, Mat('concretefloor.jpg', 32), caps='T')   # the grey bird
    R.box(396, 130, -784, 404, 140, -776, Mat('red.jpg', 32), lux=10)                  # its red crest
    named(R, 'BIRD', 400, 130, -780)
    item(R, 'docb40_1192', 420, 100, -740)
    lamp(R, 600, -500, power=44, color=(255, 230, 200))
    # Attic Storage (E, N): low beams, dust sheets over the furniture, trunks
    for x in (400, 600, 800):
        R.box(x - 10, H - 30, 20, x + 10, H, 860, WOODF, lux=10)
    for k, (x, z, w, h) in enumerate(((400, 300, 160, 100), (700, 400, 120, 150), (500, 650, 200, 80), (850, 700, 100, 190))):
        sbox(R, x - w / 2, 0, z - 50, x + w / 2, h, z + 50, SHEET, 'sheet %d' % k)
    sbox(R, 900, 0, 150, 980, 60, 260, WOODF, 'trunk')
    named(R, 'SHEETS', 700, 100, 400)
    R.light(600, 200, 450, rng=520, color=(255, 220, 170), power=26)
    check33(R)
    return (R, 'HS2', 'Residential Sector - the bedrooms (Light Containment): the sealed bedroom (SCP-1197), a bathroom with a flickering tube, the children\'s playroom with SCP-1192, and an attic store of dust-sheeted furniture.',
            1, 0.7, ((-300, 165, -430), (-990, 110, -300)))


# ------------------------------------------------------------------------------------------------ below stairs
def room2b42house3():
    specs = {('W', 'S'): (CONC36, CONCF, DARK), ('W', 'N'): (CONC36, CONCF, DARK),
             ('E', 'S'): (PAPER1, WOODF, WHITE), ('E', 'N'): (PAPER2, CARPET, WHITE)}
    R, B = res_wing('room2b42house3', 7, specs=specs, keys={('E', 'N'): 2})
    # Basement Storage (W, S): shelves, labelled boxes (SCP-1355-1 are made at runtime among them)
    for z in (-820, -600):
        shelf_unit(R, -990, z, -920, z + 160, 'basement shelf %d' % z)
    for k, (x, z) in enumerate(((-760, -780), (-700, -700), (-560, -820), (-820, -320), (-500, -300))):
        sbox(R, x, 0, z, x + 70, 60, z + 60, LABELM, 'box %d' % k)
    named(R, 'BOXES', -640, 0, -520)
    item(R, 'docb40_1355', -460, 0, -640)
    ceiling_fixture(R, -640, -500, H, power=30, rng=500)
    # the Garage (W, N): pillars, three working tubes, an old car (SCP-1196's chairs are made at runtime)
    for (x, z) in ((-760, 300), (-760, 620)):
        sbox(R, x - 25, 0, z - 25, x + 25, H, z + 25, CONC36.but(vs=H, v0=H), 'garage pillar %d' % z)
    sbox(R, -980, 0, 200, -880, 80, 760, Mat('dirtymetal.jpg', 128), 'tool bench')
    sbox(R, -600, 14, 380, -420, 70, 760, Mat('red.jpg', 128), 'car body')
    R.box(-590, 70, 470, -430, 120, 660, DARK, lux=10)
    for (x, z) in ((-610, 420), (-410, 420), (-610, 720), (-410, 720)):
        R.tube((x, 20, z), (x + (8 if x < -500 else -8), 20, z), 20, DARK, sides=8, caps=True)
    named(R, 'CHAIRS', -500, 0, 250)
    for z in (250, 500, 750):
        R.box(-680, H - 6, z - 40, -660, H, z + 40, METAL, bottom=LIGHTPANEL, lux=10)
        R.light(-670, H - 30, z, rng=460, color=(235, 245, 255), power=30)
    item(R, 'docb40_1196', -930, 80, 300)
    # the Model House (E, S): a perfect miniature of this house on a table, under glass
    table30(R, 520, -560, 760, -380, 'model table')
    for (x0, z0, x1, z1) in ((540, -540, 740, -536), (540, -404, 740, -400), (540, -540, 544, -400), (736, -540, 740, -400), (636, -540, 640, -400)):
        R.box(x0, 78, z0, x1, 108, z1, PAPER1, lux=10)
    R.prism(octo(640, -470, 6, 4), 108, 112, WOODF, caps='T')
    for (a, b) in (((516, -564), (764, -564)), ((764, -564), (764, -376)), ((764, -376), (516, -376)), ((516, -376), (516, -564))):
        glass_wall(R, a, b, 78, 150)
    named(R, 'MODEL', 640, 100, -470)
    lamp(R, 640, -470, power=40)
    # the Foundation Safehouse (E, N): a sofa and a monitor wall, a weapons locker, a radio
    sofa(R, 400, 600, 640, 680, 'safehouse sofa', back='N')
    table30(R, 460, 460, 580, 540, 'safehouse table', h=40.0)
    sbox(R, 980, 90, 300, 996, 330 if False else 300, 700, DARK, 'monitor backboard')
    decal30(R, FEEDS36, 980, 500, 'W', 380, 190, 200, 'safehouse monitors')
    console30(R, 900, 500, 'W', 'safehouse console')
    lockers(R, 'z', 860, -1, 300, 520)
    solid(R, (300, 0, 830, 520, 300, 860), 'gun lockers')
    item(R, 'radio', 520, 40, 500, chance=60)
    item(R, 'bat', 560, 40, 480, chance=60)
    lamp(R, 520, 520, power=40)
    named(R, 'SAFE', 900, 150, 500)
    check33(R)
    return (R, 'HS3', 'Residential Sector - below stairs (Light Containment): basement storage (SCP-1355\'s boxes), the garage with an old car and SCP-1196\'s chairs, the model house, and a Foundation safehouse.',
            1, 0.7, ((-300, 165, 430), (-500, 100, 500)))


ALL = [room2b42house1, room2b42house2, room2b42house3]
