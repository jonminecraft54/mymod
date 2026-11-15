"""The forty-first batch: thirteen rooms from the community's room ideas (code in IndevU41.bb), in five wings,
built from the original SCP:CB pieces - the Entrance Zone's striped walls, the LCZ/HCZ walls and tiles, doors,
lockers, desks, office chairs, monitors, the vending machine, whiteboards - with one or two features each.

  room2b43staff     EZ   Break Room (vending machine, microwave, fridge, round tables, red chairs, the counter with
                         a memo - and SCP-860 left by the coffee), Conference Room (a projector that shows a face),
                         Staff Dormitories (bunks, computers with half-typed test logs, cold coffee)
  room2b43medical   LCZ  Infirmary (beds, surgical tray, cabinets), Chemistry Lab (benches, fume hood),
                         Research Lab (microscopes, specimen tanks, cages, the x-ray lightbox, a dissection table)
  room2b43security  HCZ  Armory (weapon lockers stripped bare, vests and masks left behind, dead guards),
                         Storage Room (tiny, dark: boxes, shelves of paper, a gas mask on the cabinet),
                         Locker Room (rows of lockers and benches; the toilets at the back are a dead end)
  room2b43rec       LCZ  Theater (rows of red seats; the screen flashes hard enough to blind), Gymnasium
                         (barricades, bodies - or nothing at all; it changes from game to game)
  room2b43dblock    LCZ  D-class cells, open and bloodied, and the block's own row of cells
Everything checked as before."""
from rooms_b40 import *
from v02kit import VEND, WMON

BLOOD = Mat('indev_b41blood.png', alpha=True, cast=False)
GYMF = Mat('indev_b41gym.png', 1024)
SCREEN = Mat('indev_b41screen.png', cast=False, emit=200)
XRAY = Mat('indev_b41xray.png', cast=False, emit=120)
REDC = Mat('red.jpg', 64)


def blood(R, x, z, s=120):
    R.rect_floor(x - s / 2, z - s / 2, x + s / 2, z + s / 2, 0.8, BLOOD)


def east(R, B, key, style_mat, floor, ceil, H, x1=1000):
    """the big room through the east door (x 256..x1, z -1000..1000)"""
    WM = style_mat
    passage(R, key, mat=WM.but(vs=320, v0=320))
    hall(R, 256, -1000, x1, 1000, 0, H, WM.but(vs=H, v0=H), floor, ceil, holes={'W': [(-96, 96, 0, 320)]})
    B.areas.append((256, x1, -1000, 1000, H, 0))


def red_chair(R, x, z, name):
    sbox(R, x - 18, 0, z - 18, x + 18, 42, z + 18, REDC, name)
    R.box(x - 18, 42, z + 14, x + 18, 90, z + 18, REDC, lux=10)


# ------------------------------------------------------------------------------------------------ staff
def room2b43staff():
    R, rooms = wing33('room2b43staff', 'ez', {('W', -400): {'style': 'ez'}, ('W', 400): {'style': 'ez'}}, extra=[('E', 0)], amb=10)
    R.luxel = 16.0
    B = R.book
    WM, FM, CM = STYLES['ez']
    hub_dress(R, 'ez', [], pipes=False)
    # Break Room (W -400): vending machine, counter with microwave and fridge, round tables, red chairs
    sbox(R, -776, 0, -690, -700, 200, -590, METAL, 'vending machine')
    decal30(R, VEND, -700, -640, 'E', 96, 190, 100, 'vending front')
    sbox(R, -776, 0, -560, -716, 90, -220, WOODF, 'counter')
    R.box(-770, 90, -520, -730, 120, -470, METAL, lux=10)                          # microwave
    sbox(R, -776, 0, -200, -716, 170, -130, WHITE, 'mini fridge')
    for (x, z) in ((-520, -560), (-520, -260)):
        R.prism(octo(x, z, 46, 10), 70, 76, WHITE, caps='TB')
        R.tube((x, 0, z), (x, 70, z), 4, METAL, sides=6, caps=True)
        solid(R, (x - 46, 0, z - 46, x + 46, 76, z + 46), 'round table %d' % z)
        for (dx, dz) in ((-74, 0), (74, 0), (0, -74)):
            red_chair(R, x + dx, z + dz, 'red chair %d %d %d' % (z, dx, dz))
    item(R, 'docb41_break', -746, 90, -400)
    item(R, 'scp860', -746, 90, -320, chance=70)
    item(R, 'cup', -746, 90, -280)
    item(R, 'key3', -746, 90, -250, chance=40)
    for (x, z) in ((-640, -500), (-400, -330)):
        R.box(x, 0.8, z, x + 20, 1.2, z + 14, Mat('red.jpg', 16), lux=10)            # wrappers, chip bags
    pendant(R, -516, -400, 352, drop=60, power=46, rng=520)
    # Conference Room (W 400): the long table, chairs, the projector screen with a face on it
    table30(R, -700, 260, -500, 540, 'conference table')
    for z in (290, 360, 430, 500):
        model30(R, 'officeseat_a.x', -740, 0, z, 90, (50, 100, 50), 'conf chair W %d' % z)
        model30(R, 'officeseat_a.x', -455, 0, z, 270, (50, 100, 50), 'conf chair E %d' % z)
    decal30(R, SCREEN, -530, 700, 'S', 260, 150, 200, 'projection')
    named(R, 'PROJ', -530, 200, 690)
    sbox(R, -776, 0, 140, -740, 140, 220, WHITE, 'water dispenser')
    item(R, 'docb41_minutes', -600, 78, 400)
    R.light(-530, 200, 640, rng=420, color=(220, 230, 255), power=34)
    pendant(R, -530, 400, 352, drop=60, power=36, rng=500)
    # Staff Dormitories (E): bunks in rows, desks with computers, cold coffee
    east(R, B, 2, WM, FM, CM, 400)
    for k, z in enumerate((-880, -600, -320, 320, 600, 880)):
        for x0 in (280, 880):
            sbox(R, x0, 0, z - 50, x0 + 100, 40, z + 50, WHITE, 'bunk %d %d' % (x0, k))
            R.box(x0, 160, z - 50, x0 + 100, 172, z + 50, WHITE, lux=10)
            for dz in (-48, 48):
                R.tube((x0 + 4, 0, z + dz), (x0 + 4, 172, z + dz), 2.5, METAL, sides=6, caps=True)
    for z in (-460, 460):
        office_desk(R, 560, z - 60, 680, z + 60, 'W', 'dorm desk %d' % z, chair=(520, z))
    item(R, 'docb41_testlog', 600, 76, -500)
    item(R, 'cup', 610, 76, 420)
    for z in (-700, 0, 700):
        ceiling_fixture(R, 620, z, 400, power=40, rng=640)
    named(R, 'DORM', 620, 0, 0)
    check33(R)
    return (R, 'STF', 'Staff Wing (Entrance Zone): the break room with its vending machine and red chairs, the conference room and its projector, and the staff dormitories.',
            3, 0.6, ((-300, 165, -400), (-700, 120, -500)))


# ------------------------------------------------------------------------------------------------ medical
def room2b43medical():
    R, rooms = wing33('room2b43medical', 'lcz', {('W', -400): {'style': 'cell30'}, ('W', 400): {'style': 'lcz'}}, extra=[('E', 0)], amb=10)
    R.luxel = 16.0
    B = R.book
    WM, FM, CM = STYLES['lcz']
    hub_dress(R, 'lcz', [], pipes=False)
    # Infirmary (W -400): beds, a surgical tray, cabinets, blood
    for k, z in enumerate((-660, -520, -280, -140)):
        sbox(R, -776, 0, z - 40, -600, 60, z + 40, WHITE, 'infirmary bed %d' % k)
    sbox(R, -480, 0, -420, -400, 80, -380, METAL, 'surgical tray')
    R.box(-470, 80, -415, -410, 84, -385, WHITE, lux=10)
    cabinets(R, -360, -690, -260, -650, 'medicine cabinets')
    item(R, 'firstaid', -440, 84, -400)
    item(R, 'eyedrops', -420, 84, -390, chance=70)
    item(R, 'syringe', -310, 0, -620, chance=60)
    blood(R, -500, -520)
    cell_light(R, -516, -400, 352)
    # Chemistry Lab (W 400): benches of glassware, the fume hood
    for z in (260, 540):
        sbox(R, -700, 0, z - 40, -440, 90, z + 40, WHITE, 'lab bench %d' % z)
        for k in range(5):
            R.prism(octo(-680 + k * 50, z, 8, 6), 90, 90 + 20 + k * 4, Mat('indev_b33shade.png', 32), caps='T')
    sbox(R, -776, 0, 640, -680, 240, 696, METAL, 'fume hood')
    R.box(-680, 100, 650, -676, 200, 690, Mat('indev_b33shade.png', 32), lux=10)
    named(R, 'HOOD', -690, 150, 670)
    warn(R, 2, -256, 640, 'W', 220, 'warn chem')
    pendant(R, -570, 400, 352, drop=60, power=40, rng=520)
    # Research Lab (E): microscopes, specimen tanks, cages, the x-ray lightbox, the dissection table
    east(R, B, 2, WM, FM, CM, 420)
    for k, z in enumerate((-800, -500)):
        table30(R, 300, z - 60, 520, z + 60, 'microscope bench %d' % k)
        for dx in (40, 140):
            R.tube((300 + dx, 78, z), (300 + dx, 110, z), 4, DARK, sides=6, caps=True)
            R.box(296 + dx, 78, z - 14, 304 + dx + 10, 84, z + 14, DARK, lux=10)
    for k, z in enumerate((-200, 100, 400)):
        R.prism(octo(900, z, 50, 12), 0, 220, Mat('indev_b33shade.png', 64), caps='TB')
        solid(R, (850, 0, z - 50, 950, 220, z + 50), 'specimen tank %d' % k)
        R.light(900, 120, z, rng=260, color=(120, 220, 160), power=20)
    for k, z in enumerate((650, 850)):
        sbox(R, 860, 0, z - 70, 1000, 140, z + 70, Mat('dirtymetal.jpg', 64), 'cage %d' % k)
    decal30(R, XRAY, 256, 600, 'E', 200, 200, 180, 'x-ray lightbox')
    named(R, 'XRAY', 262, 180, 600)
    sbox(R, 560, 0, 160, 720, 90, 260, METAL, 'dissection table')
    blood(R, 640, 210, 90)
    named(R, 'DISSECT', 640, 100, 210)
    item(R, 'bat', 400, 78, -500)
    item(R, 'key3', 420, 78, -820, chance=40)
    for z in (-600, 0, 600):
        ceiling_fixture(R, 620, z, 420, power=44, rng=640)
    check33(R)
    return (R, 'MED', 'Medical Wing (Light Containment): the infirmary, the chemistry lab and its fume hood, and the research lab - microscopes, specimen tanks, cages, the x-ray lightbox, the dissection table.',
            1, 0.6, ((-300, 165, -400), (-700, 80, -400)))


# ------------------------------------------------------------------------------------------------ security
def room2b43security():
    R, rooms = wing33('room2b43security', 'hcz', {('W', -400): {'style': 'hcz', 'key': 3}, ('W', 400): {'style': 'ref99', 'span': 160, 'depth': 300}},
                      extra=[('E', 0)], amb=8)
    R.luxel = 16.0
    B = R.book
    WM, FM, CM = STYLES['hcz']
    hub_dress(R, 'hcz', [], pipes=False)
    # Armory (W -400): weapon lockers stripped bare, a vest and a mask left behind, dead guards (runtime), blood
    lockers(R, 'x', -776, 1, -680, -120)
    solid(R, (-776, 0, -680, -746, 300, -120), 'weapon lockers')
    table30(R, -560, -560, -400, -440, 'armory table')
    item(R, 'vest', -480, 78, -500, chance=80)
    item(R, 'gasmask', -440, 78, -470, chance=70)
    item(R, 'bat', -520, 78, -470)
    blood(R, -600, -300, 160)
    blood(R, -400, -620)
    named(R, 'DEAD1', -620, 0, -300)
    red_pendant(R, -516, -400, 352, drop=60, power=34, rng=520)
    # Storage Room (W 400): tiny and dark - boxes, shelves of paper, a gas mask on the little cabinet
    shelf_unit(R, -550, 250, -490, 380, 'paper shelf')
    sbox(R, -470, 0, 480, -410, 60, 540, CRATE35, 'storage box')
    sbox(R, -540, 0, 480, -480, 70, 540, WOODF, 'little cabinet')
    item(R, 'gasmask', -510, 70, 510)
    R.light(-450, 280, 400, rng=360, color=(255, 230, 190), power=18)
    # Locker Room (E): rows of lockers and benches, the toilets at the back (a dead end)
    east(R, B, 0, WM, FM, CM, 380)
    for k, z in enumerate((-700, -300, 100)):
        sbox(R, 420, 0, z - 15, 900, 200, z + 15, Mat('dirtymetal.jpg', 128), 'locker row %d' % k)
        bench30(R, 460, z + 60, 860, z + 100, 'locker bench %d' % k)
    named(R, 'LOCKER', 700, 120, -285)
    item(R, 'radio', 600, 44, 180, chance=60)
    item(R, 'scp420j', 880, 44, -600, chance=50)
    for (x0, x1) in ((560, 600), (760, 800)):
        sbox(R, x0, 0, 500, x1, 260, 1000, WM.but(vs=260, v0=260), 'stall wall %d' % x0)
    for x in (480, 680, 880):
        R.prism(octo(x, 900, 22, 8), 0, 40, WHITE, caps='T')
    for z in (-600, 0, 600):
        ceiling_fixture(R, 620, z, 380, power=40, rng=600)
    check33(R)
    return (R, 'SEC', 'Security Wing (Heavy Containment): the armory, stripped and bloodied; a tiny dark storage room; and the guards\' locker room with its dead-end toilets.',
            2, 0.6, ((-300, 165, -400), (-700, 120, -400)))


# ------------------------------------------------------------------------------------------------ recreation
def room2b43rec():
    R, rooms = big_west('room2b43rec', 'lcz', amb=6)
    R.luxel = 16.0
    B = R.book
    WM, FM, CM = STYLES['lcz']
    hub_dress(R, 'lcz', [], pipes=False)
    # the Theater (west): a stepped floor of red seats facing the screen on the west wall
    decal30(R, SCREEN, XW, 0, 'E', 620, 340, 230, 'theater screen')
    named(R, 'SCREEN', XW + 10, 230, 0)
    for k, x in enumerate((-820, -720, -620, -520)):
        for z in range(-800, 801, 80):
            if abs(z) < 130:
                continue                                                       # the centre aisle
            red_chair(R, x, z, 'seat %d %d' % (k, z))
    R.light(XW + 100, 230, 0, rng=700, color=(220, 230, 255), power=30)
    for z in (-700, 700):
        R.light(-400, 380, z, rng=400, color=(255, 180, 120), power=16)
    # the Gymnasium (east)
    east(R, B, 0, WM, GYMF, CM, 520)
    for (x, z) in ((300, -900), (300, 900)):
        R.tube((x, 0, z), (x, 300, z), 5, METAL, sides=6, caps=True)
    for k, (x0, z0, x1, z1) in enumerate(((520, -200, 560, 200), (600, 260, 760, 300), (700, -320, 840, -280))):
        sbox(R, x0, 0, z0, x1, 110, z1, WOODF, 'barricade %d' % k)
    bench30(R, 900, -600, 980, -400, 'gym bench a')
    bench30(R, 900, 400, 980, 600, 'gym bench b')
    blood(R, 640, -500, 180)
    blood(R, 820, 600, 140)
    named(R, 'GYM', 700, 0, 0)
    item(R, 'docb41_gym', 600, 0, 600)
    item(R, 'firstaid', 940, 44, -500, chance=60)
    for z in (-600, 0, 600):
        ceiling_fixture(R, 620, z, 520, power=50, rng=800)
    B.clear = [((-380, 0, -110, -260, 200, 110), 'theater aisle')]
    check33(R)
    return (R, 'REC', 'Recreation Wing (Light Containment): the theater, rows of red seats before a screen that flashes hard enough to blind, and the gymnasium - barricades, bodies, or nothing at all.',
            1, 0.6, ((-300, 165, 0), (-900, 200, 0)))


# ------------------------------------------------------------------------------------------------ D-block
def room2b43dblock():
    R, rooms = wing33('room2b43dblock', 'lcz', {('W', -400): {'style': 'plaster37'}, ('W', 400): {'style': 'plaster37'}}, extra=[('E', 0)], amb=8)
    R.luxel = 16.0
    B = R.book
    WM, FM, CM = STYLES['lcz']
    hub_dress(R, 'lcz', [], pipes=False)
    cell_dress(R, -776, -680, -120, -1, 'D1')
    cell_dress(R, -776, 120, 680, -1, 'D2')
    blood(R, -500, -400, 160)
    blood(R, -600, 450, 120)
    cell_light(R, -516, -400, 352)
    cell_light(R, -516, 400, 352)
    item(R, 'docb41_dclass', -750, 96, -530)
    item(R, 'docb41_dclass', -750, 96, 270)
    item(R, 'scp420j', -330, 0, 640, chance=40)
    # the block: a row of open cells either side of a central walk (E)
    east(R, B, 0, PLASTER, TILE96, DARK, 340)
    for z0 in range(-1000, 1000, 250):
        for (xa, xb) in ((256, 470), (790, 1000)):
            if z0 > -1000 and not (xa == 256 and abs(z0) <= 110):
                sbox(R, xa, 0, z0 - 6, xb, 340, z0 + 6, PLASTER.but(vs=340, v0=340), 'cell wall %d %d' % (xa, z0))
            if xa == 256 and abs(z0 + 125) < 140:
                continue
            for dz in (40, 210):
                R.tube((xb if xa == 256 else xa, 0, z0 + dz), (xb if xa == 256 else xa, 240, z0 + dz), 2.5, DARK, sides=6, caps=True)
    for (x, z) in ((620, -600), (620, 300), (900, 700)):
        blood(R, x, z, 140)
    named(R, 'DEAD1', 620, 0, -400)
    named(R, 'DEAD2', 900, 0, 400)
    for z in (-700, -250, 250, 700):
        red_pendant(R, 630, z, 340, drop=50, power=40, rng=520)
    check33(R)
    return (R, 'DBK', 'D-Block (Light Containment): D-class cells, open and bloodied, and the block\'s row of cells - empty now.',
            1, 0.6, ((-300, 165, -400), (-700, 80, -400)))


ALL = [room2b43staff, room2b43medical, room2b43security, room2b43rec, room2b43dblock]
