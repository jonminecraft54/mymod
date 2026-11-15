"""The forty-sixth batch (code in IndevU46.bb): the alternate timeline - a breach years before the one on record.

  room2b49checkpoint  HCZ  Checkpoint 9, abandoned: the guard booth, coats still on the hooks, the radio left on;
                           the east door opens on the team's ready room - empty racks, a card table mid-game
  room2b49hidden      LCZ  Sector R, the research department removed from the maps: dust on everything, sheeted
                           equipment, the wall map with the sector struck out; Dr. Harrison never left
  room2b49perslift    LCZ  the personnel lift: a waiting hall with benches; the car goes DOWN to the lower complex -
                           a second, older facility - where Officer Miller still holds the platform
  room2b49sealed      HCZ  a wing sealed for decades: dust drifts, a calendar stopped years ago, chairs left where
                           people stood up, and the sealed blast door to the rest of it
"""
from rooms_b45 import *
from v02kit import lift

DUST = Mat('indev_b49dust.png', 256, alpha=True, cast=False)
MAP49 = Mat('indev_b49map.png', cast=False)
SIGN49 = Mat('indev_b49sign.png', cast=False)
D = -704.0


def dust(R, x0, z0, x1, z1, y=0.7):
    R.rect_floor(x0, z0, x1, z1, y, DUST)


# ------------------------------------------------------------------------------------------------ checkpoint 9
def room2b49checkpoint():
    R, rooms = wing33('room2b49checkpoint', 'conc36', {('W', -400): {'style': 'conc36'}, ('W', 400): {'style': 'conc36'}},
                      extra=[('E', 0)], amb=10)
    R.luxel = 16.0
    B = R.book
    hd_hub(R, 'conc36', sign_w=6)
    decal30(R, SIGN49, -192, 0, 'E', 120, 30, 290, 'cp sign', uv=(0, 0.5, 1, 0.75))
    # W -400: the booth - console, the radio, coats on hooks
    for z in (-596, -400):
        console30(R, -730, z, 'E', 'booth console %d' % z)
    sbox(R, -560, 0, -240, -440, 76, -160, METAL, 'radio desk')
    R.box(-540, 76, -220, -480, 110, -190, DARK, lux=10)                 # the radio set
    R.box(-500, 110, -212, -496, 170, -208, METAL, lux=10)                # its aerial
    named(R, 'RADIO', -510, 96, -205)
    for z in (-700, -660, -620):
        R.box(-776, 150, z, -768, 260, z + 30, Mat('indev_b33shade.png', 32), lux=10)
    item(R, 'docb46_radio', -470, 76, -180)
    item(R, 'radio', -530, 76, -170, chance=60)
    red_pendant(R, -516, -400, 352, drop=60, power=34, rng=480)
    # W 400: the locker room - doors hanging open
    lockers(R, 'z', 680, -1, -700, -400)
    solid(R, (-700, 0, 650, -400, 300, 680), 'lockers')
    item(R, 'vest', -600, 0, 560, chance=30)
    cell_light(R, -516, 400, 352)
    # E: the ready room
    passage(R, 0)
    hall(R, 256, -800, 900, 800, 0, 360, CONC36.but(vs=360, v0=360), FLOOR36, DARK, holes={'W': [(-96, 96, 0, 320)]})
    B.areas.append((256, 900, -800, 800, 360, 0))
    for k, z in enumerate((-600, -300, 300, 600)):
        sbox(R, 840, 0, z - 80, 900, 220, z + 80, METAL, 'empty rack %d' % k)
    table30(R, 480, -120, 640, 120, 'card table')
    R.box(520, 76.5, -60, 600, 77, 60, Mat('white.jpg', 16), lux=10)       # the cards
    model30(R, 'officeseat_a.x', 450, 0, 0, 90, (50, 100, 50), 'chair 1')
    model30(R, 'officeseat_a.x', 690, 0, -40, 270, (50, 100, 50), 'chair 2')
    named(R, 'CARDS', 560, 80, 0)
    dust(R, 300, -760, 860, 760)
    pendant(R, 560, 0, 360, drop=70, power=46, rng=520)
    red_emergency(R, 900, 280, 500, 'W', 'red ready', power=26)
    item(R, 'keysectorr', 600, 77, 80)
    B.clear = [((300, 0, -100, 420, 200, 100), 'entrance')]
    check33(R)
    return (R, 'CP9', 'Checkpoint 9 (Heavy Containment): an abandoned security checkpoint - the booth, the coats on their hooks, a radio still switched on; the empty ready room.',
            2, 0.5, ((300, 165, -600), (-510, 96, -205)))


# ------------------------------------------------------------------------------------------------ sector R
def room2b49hidden():
    R, rooms = wing33('room2b49hidden', 'lcz', {('W', -400): {'style': 'lcz', 'key': 8}, ('W', 400): {'style': 'cell30'}},
                      extra=[('E', 0)], amb=9)
    R.luxel = 16.0
    B = R.book
    hd_hub(R, 'lcz', sign_w=6)
    dust(R, -192, -1000, 192, 1000)
    # W -400: the records office, untouched
    office_desk(R, -700, -660, -580, -540, 'E', 'old desk', chair=(-545, -600))
    cabinets(R, -500, -690, -300, -650, 'old cabinets')
    item(R, 'docb46_sector', -640, 76, -560)
    dust(R, -776, -776, -256, -24)
    pendant(R, -516, -400, 352, drop=60, power=30, rng=460)
    # W 400: storage of sheeted things
    for k, (x, z) in enumerate(((-680, 240), (-520, 260), (-680, 520))):
        sbox(R, x - 60, 0, z - 60, x + 60, 150, z + 60, SHEET, 'sheeted rig %d' % k)
    dust(R, -776, 24, -256, 776)
    cell_light(R, -516, 400, 352)
    # E: the lab - the map wall, the terminal, Harrison
    passage(R, 0)
    hall(R, 256, -900, 1000, 900, 0, 400, Mat('white.jpg', 256).but(vs=400, v0=400), TILE96, WHITE, holes={'W': [(-96, 96, 0, 320)]})
    B.areas.append((256, 1000, -900, 900, 400, 0))
    decal30(R, MAP49, 1000, -300, 'W', 360, 360, 220, 'site map')
    named(R, 'MAP', 990, 200, -300)
    sbox(R, 820, 0, 200, 960, 90, 500, Mat('dirtymetal.jpg', 64), 'terminal bench', top=CONSP)
    decal30(R, FEEDS36, 960, 350, 'W', 260, 110, 170, 'old monitors')
    named(R, 'TERMINAL', 880, 110, 350)
    for k, x in enumerate((400, 560, 720)):
        sbox(R, x, 0, -820, x + 120, 90, -700, WHITE, 'lab bench %d' % k)
        sbox(R, x + 10, 90, -800, x + 110, 160, -720, SHEET, 'sheeted kit %d' % k)
    named(R, 'HARRISON', 640, 0, 120)
    item(R, 'docb46_timeline', 900, 90, 260)
    item(R, 'key4', 900, 90, 440, chance=40)
    dust(R, 256, -900, 1000, 900, 0.8)
    for z in (-600, 0, 600):
        ceiling_fixture(R, 620, z, 400, power=34, rng=560)
    B.clear = [((300, 0, -100, 420, 200, 100), 'entrance')]
    check33(R)
    return (R, 'SCR', 'Sector R (Light Containment): a research department struck off the site maps - dust on everything, sheeted equipment, the map with the sector blacked out, and the one researcher who never left.',
            1, 0.5, ((300, 165, -600), (990, 200, -300)))


# ------------------------------------------------------------------------------------------------ the personnel lift
def room2b49perslift():
    R = R_('room2b49perslift', amb=16)
    R.book = Book()
    B = R.book
    R.luxel = 16.0
    H = 384.0
    WM, FM, CM = STYLES['lcz']
    AW = WM.but(vs=384, v0=384)
    junction(R, 'NS', 'lcz', hub=(-400, -640, 400, 640), hh=H, openings={'hubW': [door_op(0)]})
    B.areas.append((-400, 400, -1024, 1024, H))
    lift(R, -400, -1, 0, 0, 0, D, AW)
    decal30(R, SIGN49, -400, 170, 'E', 160, 40, 300, 'lift sign', uv=(0, 0, 1, 0.25))
    named(R, 'NOTICE', -395, 160, -300)
    decal30(R, MAP49, -400, -300, 'E', 120, 120, 170, 'lift notice board')
    # benches along the east wall
    for k, z in enumerate((-450, -150, 150, 450)):
        sbox(R, 300, 0, z - 100, 380, 46, z + 100, Mat('dirtymetal.jpg', 64), 'bench %d' % k)
    for (x, z) in ((-200, -450), (200, 450), (-200, 450), (200, -450)):
        ceiling_fixture(R, x, z, H, power=60, rng=620)
    item(R, 'docb46_lift', 320, 46, -150)
    # ---- the lower complex: an older, wider concourse
    X0b, X1b, ZH, HH = -400.0, 1000.0, 700.0, 440.0
    out = [(X0b, -ZH), (X0b, ZH), (X1b, ZH), (X1b, -ZH)]
    R.walls(out, D, D + HH, CONC36.but(vs=HH, v0=D + HH), holes={0: [span(out[0], (X0b, -96), (X0b, 96)) + (D, D + 320)]})
    R.rect_floor(X0b, -ZH, X1b, ZH, D, FLOOR36)
    R.rect_ceil(X0b, -ZH, X1b, ZH, D + HH, DARK)
    B.areas.append((X0b, X1b, -ZH, ZH, D + HH, D))
    decal30(R, SIGN49, -400, 400, 'E', 200, 50, D + 340, 'lower sign', uv=(0, 0.25, 1, 0.5))
    # the sealed blast door, far wall
    sbox(R, 960, D, -260, 1000, D + 360, 260, Mat('dirtymetal.jpg', 128), 'blast door')
    for z in (-270, 260):
        R.box(950, D, z, 1000, D + 380, z + 10, Mat('indev_b33shade.png', 32), lux=10)
    named(R, 'BLAST', 950, D + 160, 0)
    # Miller's post: sandbag-style crates, a lamp on a stand
    for k, z in enumerate((-160, 0, 160)):
        sbox(R, 600, D, z - 70, 680, D + 90, z + 70, CRATE35, 'barricade %d' % k)
    named(R, 'MILLER', 760, D, 0)
    R.light(760, D + 200, 0, rng=500, color=(255, 230, 190), power=46)
    rubble(R, 200, -560, 8, 50, 70, 'old rubble', 49)
    dust(R, X0b, -ZH, X1b, ZH, D + 0.8)
    for z in (-500, 500):
        ceiling_fixture(R, 300, z, D + HH, power=30, rng=520)
    red_emergency(R, 1000, D + 300, 500, 'W', 'red lower', power=30)
    item(R, 'firstaid', 640, D + 90, 160, chance=55)
    B.clear = [((-110, 0, -1000, 110, 200, -140), 'S walk'), ((-110, 0, 140, 110, 200, 1000), 'N walk')]
    check_b42(R)
    return (R, 'PEL', 'Personnel Lift (Light Containment): a waiting hall with benches and a lift that goes down to the lower complex - an older facility below this one.',
            1, 0.45, ((300, 165, -560), (-400, 150, 0)))


# ------------------------------------------------------------------------------------------------ the sealed wing
def room2b49sealed():
    R, rooms = wing33('room2b49sealed', 'conc36', {('W', -400): {'style': 'conc36', 'key': 7}, ('W', 400): {'style': 'conc36'}},
                      extra=[('E', 0)], amb=6)
    R.luxel = 16.0
    B = R.book
    hd_hub(R, 'conc36', sign_w=6)
    dust(R, -192, -1000, 192, 1000)
    # W -400: an office left mid-morning
    office_desk(R, -700, -660, -580, -540, 'E', 'stopped desk', chair=(-545, -600))
    R.box(-776, 160, -420, -770, 260, -340, Mat('white.jpg', 32), lux=10)   # the calendar
    named(R, 'CALENDAR', -770, 210, -380)
    dust(R, -776, -776, -256, -24)
    pendant(R, -516, -400, 352, drop=60, power=24, rng=440)
    # W 400: the mess - chairs pushed back, trays
    table30(R, -700, 300, -500, 520, 'mess table')
    for (x, z, yaw) in ((-455, 330, 70), (-455, 470, 110), (-730, 410, 260)):
        model30(R, 'officeseat_a.x', x, 0, z, yaw, (50, 100, 50), 'mess chair %d' % z)
    dust(R, -776, 24, -256, 776)
    cell_light(R, -516, 400, 352)
    # E: the long corridor to the blast door
    passage(R, 0)
    hall(R, 256, -300, 1000, 300, 0, 340, CONC36.but(vs=340, v0=340), FLOOR36, DARK, holes={'W': [(-96, 96, 0, 320)]})
    B.areas.append((256, 1000, -300, 300, 340, 0))
    sbox(R, 960, 0, -220, 1000, 320, 220, Mat('dirtymetal.jpg', 128), 'sealed door')
    decal30(R, Mat('indev_b36warn.png', cast=False), 960, 0, 'W', 80, 80, 280, 'seal sign', uv=(0, 0, 0.5, 0.5))
    named(R, 'SEAL', 950, 150, 0)
    dust(R, 256, -300, 1000, 300, 0.8)
    rubble(R, 700, 200, 5, 30, 50, 'fallen tiles', 491)
    R.light(800, 300, 0, rng=500, color=(200, 210, 230), power=22)
    named(R, 'SPAWN106', 600, 0, -200)
    item(R, 'docb46_timeline', -640, 76, -560, chance=50)
    B.clear = [((300, 0, -100, 420, 200, 100), 'entrance')]
    check33(R)
    return (R, 'SLD', 'The Sealed Wing (Heavy Containment): rooms closed for decades - dust drifts, a calendar stopped years ago, chairs where people stood up and left, and the blast door to the rest.',
            2, 0.5, ((300, 165, -600), (950, 150, 0)))

# ------------------------------------------------------------------------------------------------ the old SCP-173 cell
OLDW = Mat('olderscp173_whitewall.jpg', 256)
OLDF = Mat('olderscp173_white.jpg', 256)
VENT = Mat('vent.jpg', 64)


def room2scp173oldercell():
    """ref. 229: the whole tile is one tall bare-concrete chamber under dark steel beams, with the map's two doors
    at its north and south ends; the control corner and the guard balcony on the west side; the big containment
    door in the east wall and behind it the old cell, white and bloodied, the statue inside."""
    R = R_('room2scp173oldercell', amb=16)
    R.book = Book()
    B = R.book
    R.luxel = 22.0
    H = 600.0
    X0, X1 = -900.0, 1000.0
    hall(R, X0, -1024, X1, 1024, 0, H, OLDW.but(vs=H, v0=H), Mat('concretefloor.jpg', 256), DARK,
         holes={'N': [(-96, 96, 0, 320)], 'S': [(-96, 96, 0, 320)]})
    B.areas.append((X0, X1, -1024, 1024, H, 0))
    for z in (-1024, 1024):                                                       # door surrounds
        R.box(-120, 320, z - 6 if z > 0 else z, 120, 360, z if z > 0 else z + 6, DARK, lux=10)
    # thick end walls round the two map doors, so their buttons sit on a wall instead of in the air
    for (z0, z1) in ((-1024, -990), (990, 1024)):
        for (x0, x1) in ((X0, -112), (112, X1)):
            R.box(x0, 0, z0, x1, H, z1, OLDW.but(vs=H, v0=H), lux=40)
    for x in (-500, 0, 500):                                                       # the steel beams
        R.box(x - 28, H - 70, -1024, x + 28, H, 1024, DARK, lux=10)
    for z in (-850, -300, 300):                                                    # wall vents
        R.box(X0, 140, z - 60, X0 + 6, 230, z + 60, VENT, lux=10)
    # ---- west, south: the control corner - consoles, the intercom, the card desk
    for z in (-760, -560):
        console30(R, X0 + 46, z, 'E', 'control console %d' % z)
    named(R, 'INTERCOM', X0 + 20, 120, -660)
    sbox(R, -640, 0, -460, -520, 76, -340, METAL, 'card desk')
    item(R, 'keyold', -580, 76, -420)
    item(R, 'docb46_173', -560, 76, -370)
    R.light(-700, 400, -600, rng=520, color=(255, 240, 220), power=40)
    # ---- west, north: the guard balcony (ref. 229), parapet and posts
    sbox(R, X0, 320, 420, -540, 350, 1024, Mat('concretefloor.jpg', 128), 'balcony')
    sbox(R, X0, 350, 420, -540, 440, 436, OLDW, 'balcony parapet')
    sbox(R, -556, 350, 436, -540, 440, 1024, OLDW, 'balcony side')
    for z in (480, 960):
        R.box(-570, 0, z - 14, -540, 320, z + 14, DARK, lux=10)
    named(R, 'GUARD', -720, 350, 720)
    for z in (560, 880):                                                           # benches under it
        sbox(R, X0, 0, z - 90, X0 + 70, 46, z + 90, Mat('dirtymetal.jpg', 64), 'bench %d' % z)
    # ---- east: the cell - front wall with the big door opening, side walls, white inside
    CX, CZ = 440.0, 700.0
    for (z0, z1) in ((-CZ - 24, -320), (320, CZ + 24)):
        sbox(R, CX, 0, z0, CX + 24, H, z1, OLDW, 'cell front %d' % z0)
    sbox(R, CX, 460, -320, CX + 24, H, 320, OLDW, 'cell lintel')
    for (z0, z1) in ((-CZ - 24, -CZ), (CZ, CZ + 24)):
        sbox(R, CX + 24, 0, z0, X1, H, z1, OLDW, 'cell side %d' % z0)
    R.box(CX + 24, 0.4, -CZ, X1, 0.6, CZ, OLDF, lux=10)                             # the white cell floor
    R.box(X1 - 8, 0, -CZ, X1, 460, CZ, OLDF, lux=10)
    R.rect_floor(700, -260, 900, 60, 0.8, BLOOD)
    R.rect_floor(560, 180, 700, 380, 0.8, BLOOD)
    R.box(X1 - 10, 220, 400, X1, 300, 480, Mat('dirtymetal.jpg', 32), lux=10)        # the cell's junction box
    named(R, 'DOOR', CX + 12, 0, 0)
    named(R, 'S173', 820, 0, 0)
    named(R, 'DCL1', 120, 0, -260)
    named(R, 'DCL2', 120, 0, 260)
    named(R, 'CELL1', 640, 0, -200)
    named(R, 'CELL2', 640, 0, 200)
    decal30(R, Mat('indev_b36warn.png', cast=False), CX, -420, 'W', 100, 130, 260, 'cell warning', uv=(0, 0, 0.5, 0.5))
    R.light(760, 420, 0, rng=640, color=(255, 250, 240), power=64)
    for z in (-700, 0, 700):
        ceiling_fixture(R, -200, z, H - 70, power=60, rng=760)
    red_emergency(R, CX, 520, 520, 'W', 'red cell', power=24)
    B.clear = [((-130, 0, -1024, 130, 200, 1024), 'walkway'), ((130, 0, -300, 420, 200, 300), 'to the cell')]
    check_b42(R)
    return (R, 'O73', 'The old SCP-173 cell (Light Containment): one tall concrete chamber under steel beams with a door at each end, a guard balcony, the control corner, and the big door to the old white cell.',
            1, 0.5, ((-300, 165, -900), (820, 150, 0)))


ALL = [room2b49checkpoint, room2b49hidden, room2b49perslift, room2b49sealed, room2scp173oldercell]




