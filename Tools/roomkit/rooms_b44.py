"""The forty-fourth batch: the early SCP-1074 room (an old prototype wing, after the user's screenshots) and five
distinctive sites - the Cryogenic Research Facility, the Experimental Testing Theatre, the Gravity Testing Chamber,
the Geological Anomaly Research Site and the O5 Classified Records Vault (code in IndevU44.bb).

Every corridor follows the user's HD standards: pipes and a cable tray along the ceiling, hazard stripes at the
thresholds, room-number and warning signs, fluorescent fixtures plus red emergency or local blue light.

  room2b46old1074    LCZ  the old brick wing: SCP-1074 tipped over against the wall, a dead researcher in a pool
                          of blood, papers on the floor (ref. 222/223); a store of dust-sheeted junk
  room2b46cryo       HCZ  Cryo-1: six frosted suspension pods under feed pipes, the monitoring room, LN2 storage
  room2b46theatre    EZ   Testing Theatre 2: a round test floor under a surgical lamp, ringed by a tiered gallery;
                          the projection/PA booth, the prep room
  room2b46gravity    HCZ  the Gravity Lab: a tall padded chamber, field rings in floor and ceiling, crates hanging
                          in the air; the control room, the equipment store
  room2b46geology    LCZ  Geo Site 7: a rock cavern round a glowing crystal formation, a drill rig, core racks,
                          the seismograph; the core lab and the tool store
  room2b46o5vault    EZ   the O5 Records Vault: black marble, panelled walls, the record cabinets, the long reading
                          table and its green lamp; the antechamber and the shredder room
"""
from rooms_b43 import *

BRICK44 = Mat('indev_b44brick.png', 384)
COBBLE = Mat('indev_b44cobble.png', 256)
PAINT = Mat('indev_b44painting.png', cast=False)
FROST = Mat('indev_b44frost.png', 96, emit=90)
PAD = Mat('indev_b44pad.png', 256)
CRYST = Mat('indev_b44crystal.png', 64, emit=150)
MARBLE = Mat('indev_b44marble.png', 384)
HAZ = Mat('indev_b44hazard.png', 128)
SIGNS = Mat('indev_b44signs.png', cast=False)
STONE = Mat('indev_b33stone.png', 320)
STYLES['brick44'] = (BRICK44, COBBLE, DARK)
STYLES['pad44'] = (PAD, Mat('concretefloor.jpg', 256), DARK)
STYLES['rock44'] = (STONE, Mat('concretefloor.jpg', 256), DARK)
STYLES['marble44'] = (WOODT, MARBLE, DARK)


def sign(R, k, x, z, facing, yc, name, w=130, h=65):
    u0, v0 = (k % 2) * 0.5, (k // 2) * 0.25
    decal30(R, SIGNS, x, z, facing, w, h, yc, name, uv=(u0, v0, u0 + 0.5, v0 + 0.25))


def hd_hub(R, style, sign_w=None, sign_e=None, red=True):
    """the HD corridor dressing: wall pipes (in pieces between the doors), a ceiling cable tray, hazard stripes
    at each threshold, room signs, fluorescent fixtures and red emergency lamps"""
    hub_dress(R, style, [], pipes=False)
    for (z0, z1) in ((-990, -520), (-280, -110), (110, 280), (520, 990)):
        pipes_along(R, -182, z0, z1, (336, 356), (PIPE, Mat('indev_b33shade.png', 64)), 'pipes W %d' % z0, r=6)
    for (z0, z1) in ((-990, -110), (110, 990)):
        pipes_along(R, 182, z0, z1, (336, 356), (PIPE, PIPE), 'pipes E %d' % z0, r=6)
    R.box(-40, 368, -1000, 40, 374, 1000, METAL, lux=10)                         # cable tray
    for z in range(-960, 961, 240):
        R.box(-40, 374, z - 4, 40, 384, z + 4, METAL, lux=10)
    for (x0, x1, z0, z1) in ((-192, -150, -496, -304), (-192, -150, 304, 496), (150, 192, -96, 96)):
        R.rect_floor(x0, z0, x1, z1, 0.6, HAZ)
    if sign_w is not None:
        sign(R, sign_w, -192, -760, 'E', 250, 'sign W')
    if sign_e is not None:
        sign(R, sign_e, 192, 360, 'W', 250, 'sign E')
    for z in (-640, 0, 640):
        ceiling_fixture(R, 0, z, 384, power=50, rng=600)
    if red:
        red_emergency(R, -192, 300, 0, 'E', 'red hub W', power=26)


# ------------------------------------------------------------------------------------------------ old SCP-1074
def room2b46old1074():
    R, rooms = wing33('room2b46old1074', 'brick44', {('W', -400): {'style': 'brick44'}, ('W', 400): {'style': 'brick44'}}, amb=11)
    R.luxel = 16.0
    B = R.book
    hub_dress(R, 'brick44', [], pipes=False)
    for z in (-600, 600):
        R.light(0, 330, z, rng=620, color=(255, 214, 160), power=40)
        R.box(-6, 354, z - 6, 6, 384, z + 6, DARK, lux=10)                             # bare bulbs on flex
    sign(R, 5, -192, -760, 'E', 250, 'room 104')
    # W -400 (ref. 222/223): the painting tipped against the north-west corner, its easel down, the body, blood
    R.box(-776, 0, -690, -760, 200, -540, WOODT, lux=10)                              # the frame's back board
    decal30(R, PAINT, -760, -615, 'E', 130, 170, 105, 'SCP-1074')
    for (a, b) in (((-740, 0, -560), (-620, 10, -470)), ((-740, 0, -680), (-620, 10, -600)), ((-700, 0, -620), (-610, 40, -420))):
        R.tube(a, b, 3, WOODT, sides=6, caps=True)                                    # the fallen easel
    solid(R, (-776, 0, -690, -740, 200, -540), 'painting')
    named(R, 'PAINTING', -760, 100, -615)
    named(R, 'BODY', -560, 0, -450)
    R.rect_floor(-660, -560, -440, -340, 0.8, BLOOD)
    for (x, z) in ((-600, -620), (-640, -380), (-480, -500)):
        R.box(x, 0.8, z, x + 26, 1.4, z + 34, WHITE, lux=10)                            # scattered papers
    item(R, 'docb44_1074', -460, 0, -620)
    R.light(-520, 300, -400, rng=520, color=(170, 180, 220), power=34)
    R.light(-680, 160, -615, rng=260, color=(255, 230, 200), power=18)
    # W 400: the old store - dust sheets, crates
    for k, (x, z, w, h) in enumerate(((-700, 300, 110, 120), (-600, 520, 140, 90), (-420, 620, 90, 160))):
        sbox(R, x - w / 2, 0, z - 50, x + w / 2, h, z + 50, SHEET, 'sheeted %d' % k)
    sbox(R, -760, 0, 600, -680, 80, 680, CRATE35, 'old crate')
    R.light(-520, 300, 400, rng=420, color=(255, 214, 160), power=18)
    check33(R)
    return (R, 'O74', 'The Old Wing (Light Containment): a damp brick corridor from the facility\'s first days - where SCP-1074 was first kept, and where a researcher looked at it too long.',
            1, 0.35, ((-300, 165, -400), (-680, 60, -560)))


# ------------------------------------------------------------------------------------------------ cryo
def room2b46cryo():
    R, rooms = wing33('room2b46cryo', 'react37', {('W', -400): {'style': 'react37'}, ('W', 400): {'style': 'react37', 'key': 3}}, extra=[('E', 0)], amb=8)
    R.luxel = 16.0
    B = R.book
    hd_hub(R, 'react37', sign_w=7, sign_e=0)
    # W -400: monitoring - consoles, the pod feeds
    for z in (-596, -400, -204):
        console30(R, -730, z, 'E', 'cryo console %d' % z)
    decal30(R, FEEDS36, -776, -400, 'E', 300, 160, 240, 'pod feeds')
    item(R, 'docb44_cryo', -500, 0, -620)
    R.light(-500, 300, -400, rng=500, color=(180, 210, 255), power=40)
    # W 400: LN2 storage - tanks, the cold-burn sign
    for k, z in enumerate((220, 400, 580)):
        R.prism(octo(-700, z, 50, 12), 0, 240, Mat('dirtymetal.jpg', 96), caps='TB')
        solid(R, (-750, 0, z - 50, -650, 240, z + 50), 'LN2 tank %d' % k)
    sign(R, 7, -776, 640, 'E', 300, 'cold burn')
    R.light(-500, 300, 400, rng=480, color=(200, 220, 255), power=34)
    # E: the cryo hall - six pods with feed pipes, floor grates, blue light
    east(R, B, 3, REACT, GRATE, DARK, 420)
    for k, (x, z) in enumerate(((460, -640), (460, -320), (460, 320), (800, -640), (800, -320), (800, 320))):
        R.prism(octo(x, z, 64, 12), 0, 20, METAL, caps='T')
        R.prism(octo(x, z, 56, 12), 20, 240, FROST, caps='')
        R.prism(octo(x, z, 64, 12), 240, 270, METAL, caps='TB')
        R.tube((x, 270, z), (x, 420, z), 8, PIPE, sides=8, caps=False)
        solid(R, (x - 64, 0, z - 64, x + 64, 270, z + 64), 'pod %d' % (k + 1))
        R.light(x, 150, z, rng=320, color=(110, 180, 255), power=26)
        if k == 3:
            named(R, 'POD4', x, 150, z)
    for z in (-480, 480):
        R.tube((300, 390, z), (960, 390, z), 9, PIPE, sides=8, caps=True)
    R.rect_floor(560, 560, 760, 900, 0.6, HAZ)
    sign(R, 0, 1000, 0, 'W', 260, 'CRYO-1 sign', w=200, h=100)
    for z in (-700, 0, 700):
        ceiling_fixture(R, 630, z, 420, power=36, rng=600)
    B.clear = [((540, 0, -990, 720, 200, 990), 'pod aisle')]
    check33(R)
    return (R, 'CRY', 'Cryogenic Research Facility (Heavy Containment): six frosted suspension pods under their feed pipes, the monitoring room and the LN2 store.',
            2, 0.5, ((300, 165, -900), (630, 150, 200)))


# ------------------------------------------------------------------------------------------------ the theatre
def room2b46theatre():
    R, rooms = wing33('room2b46theatre', 'ez', {('W', -400): {'style': 'ez'}, ('W', 400): {'style': 'ez'}}, extra=[('E', 0)], amb=10)
    R.luxel = 16.0
    B = R.book
    WM, FM, CM = STYLES['ez']
    hd_hub(R, 'ez', sign_w=6, sign_e=1, red=False)
    # W -400: projection and PA booth
    console30(R, -730, -500, 'E', 'projection console')
    sbox(R, -600, 0, -300, -520, 90, -220, METAL, 'PA desk')
    R.tube((-560, 90, -260), (-560, 130, -250), 2, DARK, sides=6, caps=True)
    R.box(-566, 130, -256, -554, 140, -244, Mat('red.jpg', 16), lux=10)
    named(R, 'MIC', -560, 120, -260)
    pendant(R, -516, -400, 352, drop=60, power=40, rng=500)
    # W 400: prep room - lockers, a bench, gowns
    lockers(R, 'x', -776, 1, 160, 640)
    solid(R, (-776, 0, 160, -746, 300, 640), 'prep lockers')
    bench30(R, -560, 340, -420, 380, 'prep bench')
    item(R, 'docb44_theatre', -490, 44, 360)
    ceiling_fixture(R, -516, 400, 352, power=40, rng=500)
    # E: the theatre - the round test floor, the lamp, three tiers of gallery round it
    east(R, B, 2, WM, Mat('white.jpg', 256), DARK, 520)
    R.rect_floor(470, -210, 790, 210, 0.6, Mat('indev_b42floor.png', 420))
    sbox(R, 570, 0, -40, 690, 80, 40, METAL, 'test table')
    R.prism(octo(630, 0, 70, 12), 440, 470, METAL, caps='TB')
    R.tube((630, 470, 0), (630, 520, 0), 4, DARK, sides=6, caps=False)
    R.light(630, 420, 0, rng=520, color=(255, 252, 240), power=90)
    named(R, 'STAGE', 630, 100, 0)
    for t in range(3):
        y = 40 * (t + 1)
        for (x0, z0, x1, z1) in ((880 + t * 40, -900, 1000, 900), (300, 700 + t * 50, 880 + t * 40, 1000), (300, -1000, 880 + t * 40, -700 - t * 50)):
            sbox(R, x0, y - 40, z0, x1, y, z1, WOODT, 'tier %d %d %d' % (t, x0, z0))
    rail_z(R, 876, -660, 660, 0, 'gallery rail E', step=110)
    rail_x(R, 696, 320, 860, 0, 'gallery rail N', step=110)
    rail_x(R, -696, 320, 860, 0, 'gallery rail S', step=110)
    for (x, z) in ((420, -600), (420, 600), (900, 0)):
        R.light(x, 440, z, rng=500, color=(255, 236, 210), power=22)
    B.clear = [((300, 0, -690, 540, 200, 690), 'the floor west of the stage')]
    check33(R)
    return (R, 'THT', 'Experimental Testing Theatre (Entrance Zone): a round test floor under a surgical lamp, ringed by a tiered gallery; the projection and PA booth and the prep room.',
            3, 0.5, ((300, 165, -600), (630, 60, 0)))


# ------------------------------------------------------------------------------------------------ gravity
def room2b46gravity():
    R, rooms = wing33('room2b46gravity', 'hcz', {('W', -400): {'style': 'hcz'}, ('W', 400): {'style': 'hcz'}}, extra=[('E', 0)], amb=12)
    R.luxel = 18.0
    B = R.book
    hd_hub(R, 'hcz', sign_w=6, sign_e=2)
    # W -400: the field control room
    for z in (-596, -400, -204):
        console30(R, -730, z, 'E', 'field console %d' % z)
    named(R, 'FIELD', -700, 120, -400)
    decal30(R, FEEDS36, -776, -400, 'E', 300, 160, 250, 'chamber feeds')
    R.light(-500, 300, -400, rng=500, color=(230, 240, 255), power=40)
    # W 400: equipment - straps, helmets, crates
    lockers(R, 'x', -776, 1, 160, 640)
    solid(R, (-776, 0, 160, -746, 300, 640), 'harness lockers')
    sbox(R, -480, 0, 520, -400, 80, 600, CRATE35, 'equipment crate')
    item(R, 'docb44_gravity', -440, 80, 560)
    ceiling_fixture(R, -516, 400, 352, power=40, rng=500)
    # E: the chamber - tall, padded, field rings in floor and ceiling (crates float at runtime)
    H = 800.0
    east(R, B, 3, PAD, Mat('concretefloor.jpg', 256), DARK, H)
    for (y0, y1) in ((0, 14), (H - 30, H)):
        for rr in (220, 300):
            R.prism(octo(630, 0, rr, 16), y0, y1, METAL, caps='T' if y0 == 0 else 'B')
    R.rect_floor(410, -220, 850, 220, 14.5 if False else 15, HAZ) if False else None
    named(R, 'CRATES', 630, 0, 0)
    for (x, z) in ((350, -800), (350, 800), (900, -800), (900, 800)):
        R.light(x, 600, z, rng=900, color=(240, 244, 255), power=50)
    R.light(630, 200, 0, rng=500, color=(140, 200, 255), power=40)
    sign(R, 2, 256, 300, 'E', 300, 'GRAVITY LAB sign', w=200, h=100)
    B.clear = [((300, 0, -990, 960, 200, 990), 'chamber floor')]
    check33(R)
    return (R, 'GRV', 'Gravity Testing Chamber (Heavy Containment): a tall padded chamber with field rings in floor and ceiling and crates hanging in the air; the field control room and the equipment store.',
            2, 0.5, ((300, 165, -800), (630, 300, 0)))


# ------------------------------------------------------------------------------------------------ geology
def room2b46geology():
    R, rooms = wing33('room2b46geology', 'rock44', {('W', -400): {'style': 'lcz'}, ('W', 400): {'style': 'rock44'}}, extra=[('E', 0)], amb=9)
    R.luxel = 18.0
    B = R.book
    hd_hub(R, 'rock44', sign_w=6, sign_e=3)
    # W -400: the core lab - racks of core samples, a bench
    for z in (-660, -560):
        sbox(R, -776, 0, z - 30, -560, 160, z + 30, Mat('dirtymetal.jpg', 64), 'core rack %d' % z)
        for k in range(6):
            R.tube((-760 + k * 34, 160, z), (-760 + k * 34, 200, z), 9, STONE, sides=8, caps=True)
    table30(R, -560, -300, -400, -200, 'core bench')
    item(R, 'docb44_geo', -480, 78, -250)
    ceiling_fixture(R, -516, -400, 352, power=40, rng=500)
    # W 400: tool store - picks, helmets on hooks, a generator
    sbox(R, -776, 0, 200, -700, 120, 360, Mat('dirtymetal.jpg', 64), 'generator')
    lockers(R, 'x', -776, 1, 420, 640)
    solid(R, (-776, 0, 420, -746, 300, 640), 'tool lockers')
    R.light(-500, 300, 400, rng=480, color=(255, 210, 120), power=34)
    # E: the cavern - rock columns, the crystal, the drill rig, the seismograph, work lights
    east(R, B, 2, STONE, Mat('concretefloor.jpg', 256), STONE, 560)
    rnd = random.Random(447)
    for k, (x, z, r) in enumerate(((360, -760, 60), (900, -700, 80), (380, 760, 70), (920, 640, 60), (760, -300, 50), (420, 300, 45))):
        R.prism(octo(x, z, r, 7), 0, 560, STONE, caps='')
        solid(R, (x - r, 0, z - r, x + r, 560, z + r), 'rock column %d' % k)
    for k in range(7):
        a = k * 0.9
        x, z = 660 + 50 * math.cos(a), 120 + 50 * math.sin(a)
        R.prism(octo(x, z, 14 + 6 * (k % 3), 6), 0, 80 + 40 * (k % 4), CRYST, caps='T')
    solid(R, (590, 0, 50, 730, 200, 190), 'crystal formation')
    named(R, 'CRYSTAL', 660, 100, 120)
    R.light(660, 140, 120, rng=520, color=(90, 230, 210), power=50)
    for dx in (-30, 30):
        R.tube((880 + dx, 0, -100), (880, 300, -100), 5, YEL, sides=6, caps=True)        # the drill rig
    R.box(860, 300, -120, 900, 320, -80, YEL, lux=10)
    solid(R, (840, 0, -140, 920, 320, -60), 'drill rig')
    console30(R, 330, -300, 'E', 'seismograph')
    named(R, 'SEISMO', 340, 100, -300)
    for (x, z) in ((420, -500), (850, 300), (500, 650)):
        R.light(x, 400, z, rng=520, color=(255, 210, 120), power=36)
    B.clear = [((300, 0, -100, 560, 200, 100), 'entrance')]
    check33(R)
    return (R, 'GEO', 'Geological Anomaly Research Site (Light Containment): a rock cavern round a glowing crystal formation, the drill rig and seismograph; the core lab and the tool store.',
            1, 0.5, ((300, 165, -60), (660, 100, 120)))


# ------------------------------------------------------------------------------------------------ the O5 vault
def room2b46o5vault():
    R, rooms = wing33('room2b46o5vault', 'ez', {('W', -400): {'style': 'marble44'}, ('W', 400): {'style': 'ez', 'key': 4}}, extra=[('E', 0)], amb=8)
    R.luxel = 16.0
    B = R.book
    hd_hub(R, 'ez', sign_w=6, sign_e=4, red=False)
    # W -400: the antechamber - a security desk, the visitors' log
    sbox(R, -560, 0, -560, -420, 100, -440, WOODT, 'security desk')
    model30(R, 'officeseat_a.x', -600, 0, -500, 90, (50, 100, 50), 'antechamber chair')
    pendant(R, -516, -400, 352, drop=60, color=(255, 230, 180), power=40, rng=500)
    # W 400: the shredder room - the shredder, bin bags of strips
    sbox(R, -700, 0, 300, -620, 100, 380, METAL, 'shredder')
    for k, (x, z) in enumerate(((-560, 560), (-500, 600), (-620, 600))):
        R.prism(octo(x, z, 30, 7), 0, 60, DARK, caps='T')
    ceiling_fixture(R, -516, 400, 352, power=36, rng=500)
    # E: the vault - marble floor, panelled walls, record cabinets, the long reading table, the green lamp
    passage(R, 5, mat=Mat('metalpanels2.jpg', 256).but(vs=320, v0=320))
    hall(R, 256, -1000, 1000, 1000, 0, 420, WOODT.but(vs=420, v0=420), MARBLE, DARK, holes={'W': [(-96, 96, 0, 320)]})
    B.areas.append((256, 1000, -1000, 1000, 420, 0))
    decal30(R, VAULTD, 256, 300, 'E', 200, 200, 180, 'vault wheel inner')
    for z in (-900, -700, -500, 500, 700, 900):
        sbox(R, 760, 0, z - 60, 1000, 240, z + 60, WOODT, 'record cabinets %d' % z)
        for k in range(4):
            R.box(756, 30 + k * 55, z - 50, 760, 70 + k * 55, z + 50, Mat('dirtymetal.jpg', 32), lux=10)
    table30(R, 520, -260, 660, 260, 'reading table')
    for z in range(-220, 221, 88):
        model30(R, 'officeseat_a.x', 480, 0, z, 90, (50, 100, 50), 'reader W %d' % z)
        model30(R, 'officeseat_a.x', 700, 0, z, 270, (50, 100, 50), 'reader E %d' % z)
    R.box(580, 78, -20, 600, 120, 20, Mat('indev_b33shade.png', 32), lux=10)        # the green lamp
    R.light(590, 160, 0, rng=360, color=(180, 255, 180), power=30)
    console30(R, 950, 0, 'W', 'records terminal')
    named(R, 'TERMINAL', 930, 100, 0)
    for z in (-600, 0, 600):
        pendant(R, 600, z, 420, drop=90, color=(255, 230, 180), power=40, rng=600)
    sign(R, 4, 1000, 300, 'W', 280, 'O5 RECORDS sign', w=200, h=100)
    check33(R)
    return (R, 'O5V', 'O5 Classified Records Vault (Entrance Zone): black marble and panelled walls, the record cabinets, the long reading table and its green lamp; the antechamber and the shredder room.',
            3, 0.5, ((300, 165, -800), (490, 100, 0)))


ALL = [room2b46old1074, room2b46cryo, room2b46theatre, room2b46gravity, room2b46geology, room2b46o5vault]
