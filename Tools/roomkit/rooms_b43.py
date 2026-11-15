"""The forty-third batch: three rooms remade closely from the user's reference screenshots (code in IndevU43.bb).
Original textures and furniture throughout; one or two features per room, detail where the eye goes.

  room2b45lobby       LCZ  ref. 219 + 217: an elevator lobby round a heavy octagonal pillar with a dark band, three
                           lift doors (one working, two out of service). The working lift goes DOWN to the hoist
                           control office: a console wall of monitors, the HOIST and DOOR switch panel, the desk,
                           a row of filing cabinets, a locker to hide in
  room2b45checkpoint  HCZ  ref. 212: a dark poured-concrete checkpoint - the guard sits behind a counter window in
                           the corridor wall; the booth (locked), the weapons-check room, and through the east door
                           the screening hall: the scanner arch, the inspection table, a holding cell
  room2b45offices     EZ   ref. 214 + the striped EZ corridor: offices behind windows - desk, filing cabinet,
                           pendant lamp, the door with the emblem - and through the east door an open office floor
                           with two glass-fronted offices and a telephone that will not stop ringing
"""
from rooms_b42 import *
from v02kit import lift

D = -704.0


# ------------------------------------------------------------------------------------------------ the lift lobby
def room2b45lobby():
    R = R_('room2b45lobby', amb=18)
    R.book = Book()
    B = R.book
    R.luxel = 16.0
    H = 384.0
    WM, FM, CM = STYLES['lcz']
    AW = WM.but(vs=384, v0=384)
    junction(R, 'NS', 'lcz', hub=(-400, -640, 400, 640), hh=H, openings={'hubW': [door_op(0)]})
    B.areas.append((-400, 400, -1024, 1024, H))
    # the pillar (ref. 219): a wide octagon with a dark band at door-head height
    R.prism(octo(0, 0, 120, 8), 0, 240, WM.but(vs=240, v0=240), caps='')
    R.prism(octo(0, 0, 124, 8), 240, 252, DARK, caps='TB')
    R.prism(octo(0, 0, 120, 8), 252, H, WM.but(vs=H - 252, v0=H), caps='')
    R.prism(octo(0, 0, 130, 8), 0, 14, DARK, caps='T')
    # (the pillar leaves the walkway either side: x 130..400)
    # the working lift, west wall
    lift(R, -400, -1, 0, 0, 0, D, AW)
    decal30(R, Mat('indev_b36warn.png', cast=False), -400, 160, 'E', 70, 70, 200, 'lift sign', uv=(0, 0.5, 0.5, 1))
    # two lifts out of service, east wall (frames, closed doors, dead call panels)
    for z in (-300, 300):
        R.box(392, 0, z - 110, 400, 330, z - 96, DARK, lux=10)
        R.box(392, 0, z + 96, 400, 330, z + 110, DARK, lux=10)
        R.box(392, 320, z - 110, 400, 330, z + 110, DARK, lux=10)
        R.box(394, 0, z - 96, 400, 320, z + 96, Mat('dirtymetal.jpg', 128), lux=10)
        R.box(390, 140, z + 130, 400, 180, z + 150, DARK, lux=10)
        solid(R, (390, 0, z - 110, 400, 330, z + 150), 'dead lift %d' % z)
    named(R, 'DEADLIFT', 395, 160, 300)
    for (x, z) in ((-250, -450), (250, 450), (-250, 450), (250, -450)):
        ceiling_fixture(R, x, z, H, power=69, rng=620)
    R.light(0, 300, 0, rng=400, color=(255, 240, 220), power=36)
    # ---- the hoist control office, below (ref. 217)
    X0b, X1b, ZH, HH = -400.0, 700.0, 560.0, 340.0
    out = [(X0b, -ZH), (X0b, ZH), (X1b, ZH), (X1b, -ZH)]
    R.walls(out, D, D + HH, Mat('white.jpg', 256).but(vs=HH, v0=D + HH), holes={0: [span(out[0], (X0b, -96), (X0b, 96)) + (D, D + 320)]})
    R.rect_floor(X0b, -ZH, X1b, ZH, D, TILE96)
    R.rect_ceil(X0b, -ZH, X1b, ZH, D + HH, DARK)
    B.areas.append((X0b, X1b, -ZH, ZH, D + HH, D))
    # the console wall: monitors, the HOIST and DOOR switch panel, the console
    sbox(R, 660, D, -320, 700, D + 300, 260, Mat('dirtymetal.jpg', 128), 'console wall')
    decal30(R, FEEDS36, 660, -150, 'W', 300, 120, D + 230, 'office monitors')
    decal30(R, Mat('indev_b36warn.png', cast=False), 660, 120, 'W', 60, 60, D + 210, 'hoist label', uv=(0.5, 0.5, 1, 1))
    R.box(652, D + 120, 60, 660, D + 200, 120, Mat('white.jpg', 32), lux=10)          # the HOIST switch plate
    R.box(652, D + 120, 160, 660, D + 200, 220, Mat('white.jpg', 32), lux=10)         # the DOOR switch plate
    named(R, 'HOIST', 650, D + 160, 90)
    named(R, 'DOORSW', 650, D + 160, 190)
    sbox(R, 540, D, 40, 620, D + 90, 240, Mat('dirtymetal.jpg', 64), 'switch console', top=CONSP)
    sbox(R, 300, D, -260, 420, D + 76, -140, WHITE, 'office desk', skip='B')            # the desk, on the lower floor
    R.box(330, D + 76, -230, 350, D + 120, -170, DARK, lux=10)                          # its monitor
    R.box(380, D + 76, -230, 400, D + 100, -200, Mat('red.jpg', 32), lux=10)            # the red binder
    model30(R, 'officeseat_a.x', 455, D, -200, 270, (50, 100, 50), 'office chair')
    decal30(R, Mat('indev_b36warn.png', cast=False), 660, -330, 'W', 60, 40, D + 170, 'lockdown sign', uv=(0, 0, 0.5, 0.5))
    for k, x in enumerate((-300, -200, -100, 0)):
        sbox(R, x, D, ZH - 60, x + 96, D + 150, ZH, Mat('dirtymetal.jpg', 64), 'filing cabinet %d' % k)
    lockers(R, 'z', -ZH, 1, 200, 320, )
    solid(R, (200, D, -ZH, 320, D + 300, -ZH + 30), 'hiding locker')
    named(R, 'LOCKER', 260, D + 120, -ZH + 40)
    item(R, 'docb43_hoist', 340, D + 76, -220)
    item(R, 'key3', 360, D + 76, -170, chance=40)
    pendant(R, 360, -200, D + HH, drop=70, color=(255, 236, 210), power=60, rng=520)
    ceiling_fixture(R, 100, 200, D + HH, power=60, rng=620)
    red_emergency(R, 700, D + 260, -450, 'W', 'red office', power=42)
    for (box, n) in (((-400, D, -ZH, 700, D + 1, ZH), 'office floor marker'),):
        pass
    B.clear = [((-110, 0, -1000, 110, 200, -140), 'S walk'), ((140, 0, -600, 380, 200, 600), 'E walk')]
    check_b42(R)
    return (R, 'LBY', 'Lift Lobby (Light Containment): a lobby round a heavy octagonal pillar with three lift doors - one working, down to the hoist control office.',
            1, 0.45, ((300, 165, -560), (0, 150, 0)))


# ------------------------------------------------------------------------------------------------ the checkpoint
def room2b45checkpoint():
    R, rooms = wing33('room2b45checkpoint', 'conc36', {('W', -400): {'style': 'conc36', 'key': 4}, ('W', 400): {'style': 'conc36'}},
                      extra=[('E', 0)], amb=12)
    R.luxel = 14.0
    B = R.book
    hub_dress(R, 'conc36', [], pipes=False)
    # the guard booth (ref. 212): a poured-concrete box against the west wall of the corridor, a counter window
    # facing the walkway, its own low ceiling; the guard sits behind the glass
    BX0, BX1, BZ0, BZ1, BH = -192.0, -70.0, -780.0, -540.0, 300.0
    bpts = [(BX0, BZ0), (BX0, BZ1), (BX1, BZ1), (BX1, BZ0)]
    R.walls([(BX1, BZ0), (BX1, BZ1), (BX0, BZ1), (BX0, BZ0)][::-1], 0, BH, CONC36.but(vs=BH, v0=BH))     # inside faces
    out = [(BX0, BZ1), (BX1, BZ1), (BX1, BZ0), (BX0, BZ0)]
    R.wall(out[0], out[1], 0, BH, CONC36.but(vs=BH, v0=BH))
    R.wall(out[1], out[2], 0, BH, CONC36.but(vs=BH, v0=BH), holes=[(30, 210, 110, 250)])
    R.wall(out[2], out[3], 0, BH, CONC36.but(vs=BH, v0=BH))
    R.box(BX0, BH, BZ0, BX1, BH + 14, BZ1, CONC36, lux=12)
    R.rect_ceil(BX0, BZ0, BX1, BZ1, BH, DARK)
    glass_wall(R, (BX1, BZ1 - 30), (BX1, BZ0 + 30), 110, 250)
    R.box(BX1 - 40, 104, BZ0 + 30, BX1 + 20, 110, BZ1 - 30, METAL, lux=10)                # the counter shelf
    solid(R, (BX0, 0, BZ0, BX1, BH + 14, BZ1), 'guard booth')
    named(R, 'WINDOW', BX1 + 10, 160, (BZ0 + BZ1) / 2)
    named(R, 'GUARD', -150, 0, (BZ0 + BZ1) / 2)
    R.light(-130, 260, (BZ0 + BZ1) / 2, rng=260, color=(255, 214, 160), power=39)
    # W -400 (locked): the guards' quarters - bunk, logbook, the monitor
    sbox(R, -776, 0, -680, -600, 50, -580, Mat('dirtymetal.jpg', 64), 'guard bunk')
    sbox(R, -400, 0, -700, -330, 90, -600, CONC36, 'quarters desk')
    model30(R, 'monitor.x', -380, 90, -650, 90, (40, 40, 26), 'quarters monitor')
    item(R, 'docb43_checkpoint', -360, 90, -620)
    R.light(-500, 300, -400, rng=420, color=(255, 214, 160), power=39)
    # W 400: weapons check - lockers, a table, an empty rifle rack
    lockers(R, 'x', -776, 1, 160, 640)
    solid(R, (-776, 0, 160, -746, 300, 640), 'check lockers')
    table30(R, -560, 300, -420, 500, 'check table')
    item(R, 'vest', -490, 78, 360, chance=50)
    red_pendant(R, -516, 400, 352, drop=60, power=45, rng=460)
    # corridor: grime, red lamps, the stencil
    grime_hub(R, 120)
    for z in (-250, 700):
        red_emergency(R, 192, 300, z, 'W', 'red cp %d' % z, power=45)
    decal30(R, SCPST, 192, -500, 'W', 200, 100, 220, 'stencil')
    for z in (-560, 0, 560):
        ceiling_fixture(R, 0, z, 384, power=45, rng=460)
    # E: the screening hall - the scanner arch, the inspection table, a holding cell
    east(R, B, 3, CONC36, FLOOR36, DARK, 380)
    for x in (480, 640):
        sbox(R, x - 20, 0, -120, x + 20, 260, -100, METAL, 'scanner post %d' % x)
        sbox(R, x - 20, 0, 100, x + 20, 260, 120, METAL, 'scanner post b %d' % x)
    R.box(460, 260, -120, 660, 280, 120, METAL, lux=10)
    R.light(560, 250, 0, rng=300, color=(120, 220, 255), power=30)
    named(R, 'SCANNER', 560, 140, 0)
    table30(R, 760, -400, 960, -260, 'inspection table')
    item(R, 'docb43_contraband', 860, 78, -330)
    both(R, (700, 500), (1000, 500), 0, 380, CONC36.but(vs=380, v0=380), [(60, 240, 0, 260)])
    for i in range(10):
        x = 760 + i * 18
        R.tube((x, 0, 500), (x, 260, 500), 2.2, DARK, sides=5, caps=False)
    solid(R, (700, 0, 496, 1000, 380, 504), 'holding cell front')
    sbox(R, 860, 0, 820, 1000, 40, 1000, Mat('dirtymetal.jpg', 64), 'holding cot')
    for z in (-600, 0, 600):
        ceiling_fixture(R, 620, z, 380, power=54, rng=600)
    check33(R)
    return (R, 'CHK', 'Security Checkpoint (Heavy Containment): a dark concrete corridor where a guard watches from behind a counter window, the weapons-check room, and the screening hall with its scanner arch and holding cell.',
            2, 0.45, ((0, 165, -300), (-224, 160, -650)))


# ------------------------------------------------------------------------------------------------ the offices
def office_window_room(R, c, tag):
    """ref. 214: an office off the corridor - desk with a monitor, a filing cabinet, a pendant, two windows"""
    office_desk(R, -700, c - 120, -560, c + 20, 'E', 'office desk %s' % tag, chair=(-520, c - 50))
    sbox(R, -770, 0, c + 120, -700, 170, c + 200, WHITE, 'filing cabinet %s' % tag)
    decal30(R, Mat('indev_gatev_window.png', cast=False), -776, c - 50, 'E', 140, 90, 200, 'office window %s' % tag)
    pendant(R, -600, c - 50, 352, drop=70, color=(255, 236, 210), power=63, rng=520)
    item(R, 'docb43_memo', -650, 76, c - 80, chance=70)


def room2b45offices():
    R, rooms = wing33('room2b45offices', 'ez', {('W', -400): {'style': 'ez'}, ('W', 400): {'style': 'ez'}}, extra=[('E', 0)], amb=15)
    R.luxel = 16.0
    B = R.book
    WM, FM, CM = STYLES['ez']
    hub_dress(R, 'ez', [], pipes=False)
    office_window_room(R, -400, 'A')
    office_window_room(R, 400, 'B')
    decal30(R, Mat('indev_b33plates.png', cast=False) if False else LOGO35, -192, -620, 'E', 60, 60, 260, 'nameplate A')
    for z in (-600, 0, 600):
        red_pendant(R, 0, z, 384, drop=60, power=60, rng=560)
    # E: the open office floor with two glass-fronted offices
    east(R, B, 2, WM, FM, CM, 400)
    for k, z0 in enumerate((-1000, 500)):
        z1 = z0 + 500
        zf = z1 if z0 < 0 else z0
        holes = [(80, 180, 0, 300), (260, 560, 100, 260)]
        both(R, (1000, zf), (560, zf), 0, 400, WM.but(vs=400, v0=400), holes)
        both(R, (560, z0), (560, z1), 0, 400, WM.but(vs=400, v0=400), [])
        glass_wall(R, (740, zf), (440 + 300, zf), 100, 260) if False else glass_wall(R, (1000 - 560, zf), (1000 - 260, zf), 100, 260)
        solid(R, (560, 0, zf - 3, 820, 400, zf + 3) if z0 < 0 else (560, 0, zf - 3, 820, 400, zf + 3), 'glass front %d' % k)
        zc = (z0 + z1) / 2
        office_desk(R, 760, zc - 60, 900, zc + 60, 'W', 'glass office desk %d' % k, chair=(720, zc))
        sbox(R, 940, 0, zc + 120 if z0 < 0 else zc - 200, 1000, 170, zc + 200 if z0 < 0 else zc - 120, WHITE, 'cabinet %d' % k)
    for (x, z) in ((330, -300), (330, 300)):
        for dz in (-60, 60):
            office_desk(R, x, z + dz - 50, x + 120, z + dz + 50, 'E', 'open desk %d %d' % (z, dz), chair=(x + 155, z + dz))
    R.box(388, 76, -332, 404, 84, -318, DARK, lux=10)                               # the telephone
    named(R, 'PHONE', 396, 84, -325)
    item(R, 'docb43_memo', 380, 76, 280)
    for z in (-700, -250, 250, 700):
        ceiling_fixture(R, 450, z, 400, power=60, rng=560)
    check33(R)
    return (R, 'OFC', 'Office Wing (Entrance Zone): offices behind windows off the striped corridor, and an open office floor with two glass-fronted offices - and a telephone that will not stop ringing.',
            3, 0.45, ((-300, 165, -400), (-700, 120, -450)))


ALL = [room2b45lobby, room2b45checkpoint, room2b45offices]
