"""The forty-second batch: four rooms from the user's site write-ups (Site-56's Facility B, Site-45's Blocks C, D
and E), and the first three- and four-way rooms of these batches (code in IndevU42.bb).

  room2b44panopticon  HCZ  2-way  Facility B, the mass humanoid containment wing: a ring of twelve barred cells in
                               two tiers round a central observation tower with a glass cab; the floor emblem
  room3b44toybox      HCZ  3-way  C-Block "The Toy Box": three containment chambers, each with its own small lab
                               behind glass - SCP-127 (the living gun), SCP-439 (the terrarium), and the empty test
                               room for SCP-1577 - the block armory and the research offices
  room4b44vault       EZ   4-way  D-Block "The Vault": four vaults off a crossroads - SCP-4139's fridge, SCP-154 on
                               velvet, the backup servers, the sensitive archives
  room2b44cellar      HCZ  2-way  E-Block "The Cellar": the end of the long tunnel - ribbed, wired with demolition
                               charges - the blast control room, the airlock, and SCP-466 behind thick glass
Original textures throughout (ref96 white, LCZ/HCZ/EZ walls, tiles, metal, glass, lockers, desks, consoles, the
original doors); new ones only for the vault door, charges, server racks, the fridge and the floor emblem."""
from rooms_b41 import *

VAULTD = Mat('indev_b42vault.png', cast=False)
CHARGE = Mat('indev_b42charge.png', cast=False)
RACK = Mat('indev_b42rack.png', cast=False, emit=60)
FRIDGE = Mat('indev_b42fridge.png', cast=False)
EMBLEM = Mat('indev_b42floor.png', 600)
COS, SIN = math.cos, math.sin


def P(r, a):
    return (r * COS(a), r * SIN(a))


def both(R, a, b, y0, y1, mat, holes=None):
    R.wall(a, b, y0, y1, mat, holes=holes or [])
    R.wall(b, a, y0, y1, mat, holes=[(math.dist(a, b) - h[1], math.dist(a, b) - h[0], h[2], h[3]) for h in (holes or [])])


# ------------------------------------------------------------------------------------------------ the panopticon
def room2b44panopticon():
    H = 620.0
    R, B = big_hall('room2b44panopticon', 'ref96', H, 12)
    RI, RO, T1, T2 = 560.0, 800.0, 300.0, 560.0
    step = math.pi * 2 / 16
    cells = []
    for k in range(16):
        a0, a1 = k * step, (k + 1) * step
        mid = (a0 + a1) / 2
        if abs(math.sin(mid)) > 0.92:                                       # leave the N and S axes free
            continue
        cells.append((k, a0, a1))
    for n, (k, a0, a1) in enumerate(cells):
        quad = [P(RI, a0), P(RO, a0), P(RO, a1), P(RI, a1)]
        R.wall(P(RO, a0), P(RO, a1), 0, T2 + 40, PLASTER.but(vs=T2 + 40, v0=T2 + 40))            # back wall (inward)
        both(R, P(RI, a0), P(RO, a0), 0, T2 + 40, PLASTER.but(vs=T2 + 40, v0=T2 + 40))           # partition
        R.ceil(quad, T1, DARK)
        R.floor(quad, T1 + 16, TILE96)
        R.ceil(quad, T2 + 40, DARK)
        # the bars, both tiers (two cells on the ground ring stand open)
        open_cell = n in (1, 7)
        for (y0, y1) in ((0, T1 - 10), (T1 + 16, T2)):
            if open_cell and y0 == 0:
                continue
            for i in range(9):
                t = (i + 0.5) / 9
                a = a0 + (a1 - a0) * t
                x, z = P(RI, a)
                R.tube((x, y0, z), (x, y1, z), 2.2, DARK, sides=5, caps=False)
            for y in (y0 + 6, (y0 + y1) / 2, y1 - 6):
                R.tube(P(RI, a0)[:1] + (y,) + P(RI, a0)[1:], P(RI, a1)[:1] + (y,) + P(RI, a1)[1:], 2.2, DARK, sides=5, caps=False)
        # a cot and a toilet in each ground cell
        cx, cz = P((RI + RO) / 2, (a0 + a1) / 2)
        R.box(cx - 30, 0, cz - 30, cx + 30, 40, cz + 30, Mat('dirtymetal.jpg', 64), lux=10)
        if open_cell:
            blood(R, cx, cz, 120)
            named(R, 'OPEN%d' % (1 if n == 1 else 2), cx, 0, cz)
        R.light(cx * 0.95, 240, cz * 0.95, rng=260, color=(240, 240, 230), power=16)
    # the upper-tier catwalk ring (seen from the floor: a ledge and a rail)
    ring_in = [P(RI - 90, a) for a in [i * step for i in range(16)]]
    for (k, a0, a1) in cells:
        quad = [P(RI - 90, a0), P(RI, a0), P(RI, a1), P(RI - 90, a1)]
        R.floor(quad, T1 + 16, Mat('dirtymetal.jpg', 128))
        R.ceil(quad, T1, DARK)
        R.tube(P(RI - 88, a0)[:1] + (T1 + 110,) + P(RI - 88, a0)[1:], P(RI - 88, a1)[:1] + (T1 + 110,) + P(RI - 88, a1)[1:], 3, METAL, sides=6, caps=True)
        R.tube(P(RI - 88, a0)[:1] + (T1 + 16,) + P(RI - 88, a0)[1:], P(RI - 88, a0)[:1] + (T1 + 110,) + P(RI - 88, a0)[1:], 3, METAL, sides=6, caps=True)
    # the observation tower: an octagon, a door N and S, a glass cab on top
    TR = 170.0
    oct_pts = [P(TR, math.radians(22.5 + 45 * i)) for i in range(8)]
    for i in range(8):
        a, b = oct_pts[i], oct_pts[(i + 1) % 8]
        midang = math.degrees(math.atan2((a[1] + b[1]) / 2, (a[0] + b[0]) / 2)) % 360
        L = math.dist(a, b)
        holes = [(0, L, 0, 260)] if abs(midang - 90) < 5 or abs(midang - 270) < 5 else []
        both(R, b, a, 0, 300, Mat('dirtymetal.jpg', 128), holes)
        glass_wall(R, b, a, 300, 460)
    R.ceil(oct_pts, 300, DARK)
    R.floor(oct_pts, 300.5, Mat('dirtymetal.jpg', 64))
    R.ceil(oct_pts, 470, DARK)
    R.prism([(x * 1.08, z * 1.08) for (x, z) in oct_pts], 470, 490, Mat('dirtymetal.jpg', 64), caps='TB')
    sbox(R, -150, 0, -50, -100, 90, 50, Mat('dirtymetal.jpg', 64), 'tower console W')
    sbox(R, 100, 0, -50, 150, 90, 50, Mat('dirtymetal.jpg', 64), 'tower console E')
    named(R, 'TOWER', 0, 380, 0)
    R.light(0, 400, 0, rng=900, color=(250, 250, 240), power=60)
    for i in range(8):
        a = math.radians(22.5 + 45 * i)
        R.light(400 * COS(a), 560, 400 * SIN(a), rng=600, color=(240, 244, 255), power=36)
    R.rect_floor(-360, -360, 360, 360, 0.5, EMBLEM)
    item(R, 'docb42_blocks', 120, 90, 0)
    named(R, 'DCELL', *P((RI + RO) / 2 * 0.98, (cells[1][1] + cells[1][2]) / 2)[:1], 0, P((RI + RO) / 2 * 0.98, (cells[1][1] + cells[1][2]) / 2)[1]) if False else None
    for z in (-760, 760):
        red_emergency(R, -192, 300, z, 'E', 'red arm %d' % z)
    check33(R)
    return (R, 'PAN', 'Facility B - the Panopticon (Heavy Containment): a ring of barred cells in two tiers round a central observation tower with a glass cab.',
            2, 0.55, ((0, 165, -800), (0, 300, 0)))


# ------------------------------------------------------------------------------------------------ the Toy Box (3-way)
def room3b44toybox():
    H = 560.0
    R = R_('room3b44toybox', amb=20)
    R.book = Book()
    B = R.book
    R.luxel = 18.0
    WM, FM, CM = STYLES['hcz']
    junction(R, 'SEW', 'hcz', hub=(X0, Z0, X1, Z1), hh=H)
    B.areas.append((X0, X1, Z0, Z1, H))
    B.areas.append((-1024, 1024, -192, 192, 384))
    B.areas.append((-192, 192, -1024, 0, 384))
    W = WM.but(vs=H, v0=H)
    units = [(-1000, -340, 'W'), (-330, 330, 'M'), (340, 1000, 'E')]
    for (xa, xb, tag) in units:
        xc = (xa + xb) / 2
        # the lab front (z 200) and the chamber wall (z 480) - the chamber wall has a door and a long window
        both(R, (xb, 200), (xa, 200), 0, H, W, [(xb - xc - 96, xb - xc + 96, 0, 320)])
        L = xb - xa
        both(R, (xb, 480), (xa, 480), 0, H, W, [(xb - xc - 96 + 180, xb - xc + 96 + 180, 0, 320), (xb - xc - 250, xb - xc + 60, 100, 260)])
        glass_wall(R, (xc - 60, 480), (xc + 250, 480), 100, 260)
        R.spawns.append(dict(kind='door', pos=(xc - 180, 0, 480), angle=0, key=3))
        both(R, (xa if xa > -1000 else -1000, 200), (xa if xa > -1000 else -1000, 860), 0, H, W) if xa > -1000 else None
        for z in (200, 480):
            solid(R, (xa, 0, z - 2, xc - 100, H, z + 2), '%s wall %d a' % (tag, z)) if z == 200 else None
        R.light(xc, 420, 340, rng=620, color=(250, 248, 240), power=60)
        R.light(xc, 480, 670, rng=720, color=(240, 244, 255), power=70)
    # W: SCP-127 - the armory lab: racks, the feeding station; the gun in its case in the chamber
    lockers(R, 'x', -1000, 1, 220, 460)
    solid(R, (-1000, 0, 220, -970, 300, 460), 'toybox racks')
    table30(R, -800, 300, -600, 380, 'feeding station')
    sbox(R, -760, 0, 620, -600, 100, 720, Mat('dirtymetal.jpg', 64), '127 plinth')
    for (a, b) in (((-760, 620), (-600, 620)), ((-600, 620), (-600, 720)), ((-600, 720), (-760, 720)), ((-760, 720), (-760, 620))):
        glass_wall(R, a, b, 100, 180)
    R.box(-720, 100, 660, -640, 116, 680, DARK, lux=10)
    R.box(-700, 116, 664, -660, 124, 676, Mat('red.jpg', 32), lux=10)                  # it is alive in there
    named(R, 'GUN', -680, 120, 670)
    item(R, 'docb42_127', -700, 78, 340)
    # M: SCP-439 - microscopes and monitors; the terrarium and the empty cot in the chamber
    table30(R, -300, 240, -120, 320, 'micro bench')
    console30(R, 230, 300, 'W', 'lab console 439')
    sbox(R, -60, 0, 650, 120, 80, 740, WHITE, 'terrarium table')
    for (a, b) in (((-50, 660), (110, 660)), ((110, 660), (110, 730)), ((110, 730), (-50, 730)), ((-50, 730), (-50, 660))):
        glass_wall(R, a, b, 80, 140)
    R.rect_floor(-46, 664, 106, 726, 80.5, Mat('concretefloor.jpg', 32))
    named(R, 'TERRA', 30, 100, 695)
    sbox(R, 180, 0, 600, 300, 40, 820, Mat('white.jpg', 64), 'test cot')
    item(R, 'docb42_439', -200, 78, 280)
    # E: SCP-1577 - the control desk; the empty test room, scorched
    office_desk(R, 700, 240, 840, 340, 'N', 'control desk', chair=(770, 380))
    item(R, 'flare1577', 760, 76, 280)
    item(R, 'docb42_1577', 800, 76, 290)
    blood(R, 700, 700, 200) if False else R.rect_floor(560, 600, 880, 820, 0.6, Mat('indev_b36grime.png', 128, alpha=True))
    named(R, 'TESTROOM', 700, 200, 700)
    # S: the block armory (south-west) and the research offices (south-east)
    for s in (-1, 1):
        both(R, (s * 192, -860), (s * 192, -200), 0, 400, WM.but(vs=400, v0=400), [(260, 452, 0, 320)])
        both(R, (s * 1000, -200), (s * 192, -200), 0, 400, WM.but(vs=400, v0=400), [])
    lockers(R, 'z', -860, 1, -900, -400)
    solid(R, (-900, 0, -860, -400, 300, -830), 'armory lockers')
    table30(R, -700, -560, -500, -460, 'armory table')
    item(R, 'vest', -600, 78, -510, chance=60)
    decal30(R, Mat('indev_b36warn.png', cast=False), -192, -400, 'W', 80, 80, 200, 'armory sign', uv=(0.5, 0, 1, 0.5))
    for x in (450, 750):
        office_desk(R, x - 60, -760, x + 60, -660, 'N', 'office desk %d' % x, chair=(x, -620))
    decal30(R, WB, 600, -200, 'S', 260, 120, 200, 'office whiteboard')
    for (x, z) in ((-600, 0), (0, 0), (600, 0), (-600, -500), (600, -500)):
        ceiling_fixture(R, x, z, H, power=66, rng=820)
    B.clear = [((-110, 0, -1000, 110, 200, 190), 'S corridor'), ((-1000, 0, -110, 1000, 200, 110), 'E-W corridor')]
    # the standard corridor walk is for N-S rooms; this one has no north arm, so walk only the clear boxes
    check_b42(R)
    return (R, 'TOY', 'C-Block, the Toy Box (Heavy Containment, T-junction): three containment chambers each with its own small lab - SCP-127, SCP-439, SCP-1577\'s test room - the block armory and the research offices.',
            2, 0.5, ((0, 165, -700), (0, 150, 600)), 3)


def check_b42(R):
    """check33 without its N-S corridor walk (for the 3- and 4-way rooms): overlaps, room bounds, clear boxes"""
    B = R.book
    bad = []
    inter = lambda a, b, e=0.5: all(a[i] < b[i + 3] - e and b[i] < a[i + 3] - e for i in range(3))
    for i in range(len(B.solids)):
        for j in range(i + 1, len(B.solids)):
            if inter(B.solids[i][0], B.solids[j][0]):
                bad.append('solids overlap: %s / %s' % (B.solids[i][1], B.solids[j][1]))
    for clear, cn in getattr(B, 'clear', []):
        for box, name in B.solids:
            if inter(box, clear):
                bad.append('%s blocks the %s' % (name, cn))
    if bad:
        print(R.name + ':\n  ' + '\n  '.join(bad))
        raise SystemExit(1)
    print('  %s: %d solids - no overlaps, passages clear' % (R.name, len(B.solids)))


# ------------------------------------------------------------------------------------------------ the Vault (4-way)
def room4b44vault():
    H = 420.0
    R = R_('room4b44vault', amb=9)
    R.book = Book()
    B = R.book
    R.luxel = 18.0
    WM, FM, CM = STYLES['ez']
    junction(R, 'NSEW', 'ez', hub=(X0, Z0, X1, Z1), hh=H)
    B.areas.append((X0, X1, Z0, Z1, H))
    W = WM.but(vs=H, v0=H)
    VW = Mat('metalpanels2.jpg', 256).but(vs=H, v0=H)
    for sx in (-1, 1):
        for sz in (-1, 1):
            # the vault's two walls on the crossroads, double-skinned, a door in the N-S side
            xw, zw = 192 * sx, 192 * sz
            zc = 530 * sz
            zlo, zhi = sorted((zw, 860 * sz))
            hole = (abs(zc - zw) - 96, abs(zc - zw) + 96, 0, 320)
            both(R, (xw, zw), (xw, 860 * sz), 0, H, VW, [hole])
            both(R, (xw + 16 * sx, zw), (xw + 16 * sx, 860 * sz), 0, H, VW, [hole])
            both(R, (xw, zw), (1000 * sx, zw), 0, H, VW)
            solid(R, (min(xw, xw + 16 * sx), 0, zlo, max(xw, xw + 16 * sx), H, min(zc - 96, zc + 96) if zc > 0 else zc - 96), 'vault wall a %d %d' % (sx, sz)) if False else None
            R.box(min(xw, xw + 16 * sx), 320, zc - 96, max(xw, xw + 16 * sx), H, zc + 96, VW, lux=12)
            R.spawns.append(dict(kind='door', pos=(xw + 8 * sx, 0, zc), angle=90, key=3 if sz > 0 else 2))
            decal30(R, VAULTD, xw, zc - 220 * sz if False else zc, 'W' if sx > 0 else 'E', 0.01, 0.01, 1, 'nothing %d %d' % (sx, sz)) if False else None
            decal30(R, VAULTD, xw, zc + (-230 if sz > 0 else 230), 'W' if sx > 0 else 'E', 220, 220, 180, 'vault wheel %d %d' % (sx, sz))
            R.light(600 * sx, 360, 530 * sz, rng=700, color=(240, 244, 255), power=34)
    # NE: SCP-4139, the fridge
    sbox(R, 840, 0, 700, 960, 220, 820, WHITE, 'SCP-4139')
    decal30(R, FRIDGE, 840, 760, 'W', 110, 210, 110, 'fridge door')
    named(R, 'FRIDGE', 830, 120, 760)
    item(R, 'docb42_4139', 600, 0, 760)
    R.light(880, 300, 760, rng=400, color=(170, 210, 255), power=26)
    # NW: SCP-154 on velvet under a glass dome
    sbox(R, -660, 0, 500, -540, 100, 620, Mat('red.jpg', 64), 'velvet plinth')
    for (a, b) in (((-650, 510), (-550, 510)), ((-550, 510), (-550, 610)), ((-550, 610), (-650, 610)), ((-650, 610), (-650, 510))):
        glass_wall(R, a, b, 100, 170)
    item(R, 'bracelets154', -600, 100, 560)
    item(R, 'docb42_154', -400, 0, 700)
    R.light(-600, 300, 560, rng=360, color=(255, 230, 180), power=30)
    # SW: the backup servers
    for k, z in enumerate((-820, -620, -420)):
        sbox(R, -960, 0, z - 40, -500, 230, z + 40, DARK, 'server row %d' % k)
        decal30(R, RACK, -730, z + 40, 'N', 460, 230, 115, 'rack face %d' % k)
    named(R, 'SERVERS', -730, 120, -500)
    R.light(-730, 300, -620, rng=600, color=(140, 180, 255), power=30)
    # SE: the sensitive archives
    for z in (-820, -660, -500):
        shelf_unit(R, 600, z, 960, z + 70, 'archive shelf %d' % z)
    table30(R, 300, -400, 460, -300, 'reading desk')
    item(R, 'docb42_blocks', 380, 78, -350)
    # the crossroads: one bored security desk in the corner
    table30(R, 240, 240, 330, 330, 'security desk') if False else None
    for (x, z) in ((0, 0), (0, 600), (0, -600), (600, 0), (-600, 0)):
        ceiling_fixture(R, x, z, H, power=40, rng=600)
    B.clear = [((-110, 0, -1000, 110, 200, 1000), 'N-S'), ((-1000, 0, -110, 1000, 200, 110), 'E-W')]
    check_b42(R)
    return (R, 'VLT', 'D-Block, the Vault (Entrance Zone, crossroads): four vaults - SCP-4139\'s fridge, SCP-154 on velvet, the backup servers, the sensitive archives.',
            2, 0.5, ((0, 165, 0), (192, 150, 530)), 4)


# ------------------------------------------------------------------------------------------------ the Cellar
def room2b44cellar():
    R, rooms = wing33('room2b44cellar', 'conc36', {('W', -400): {'style': 'conc36'}, ('W', 400): {'style': 'cell30'}},
                      extra=[('E', 0)], amb=5)
    R.luxel = 16.0
    B = R.book
    hub_dress(R, 'conc36', [], pipes=False)
    # the tunnel: steel ribs every 160, demolition charges between them, red lamps
    for z in range(-960, 961, 160):
        if abs(z) < 120 or abs(abs(z) - 400) < 120 or abs(z) == 640:
            R.box(-192, 360, z - 10, 192, 384, z + 10, METAL, lux=10)
            continue
        for x0, x1 in ((-192, -176), (176, 192)):
            sbox(R, x0, 0, z - 10, x1, 384, z + 10, METAL, 'rib %d %d' % (x0, z))
        R.box(-176, 366, z - 10, 176, 384, z + 10, METAL, lux=10)
    for z in (-880, -560, 560, 880):
        for (x, f) in ((-176, 'E'), (176, 'W')):
            decal30(R, CHARGE, x, z - 80, f, 70, 70, 200, 'charge %d %d' % (x, z))
    for z in (-720, 720):
        red_emergency(R, -176, 300, z, 'E', 'red tunnel W %d' % z, power=34)
        red_emergency(R, 176, 300, z + 80, 'W', 'red tunnel E %d' % z, power=34)
    for z in (-600, 0, 600):
        ceiling_fixture(R, 0, z, 384, power=24, rng=420)
    # W -400: blast control - consoles, the detonator under a locked cover
    for z in (-596, -400):
        console30(R, -730, z, 'E', 'blast console %d' % z)
    sbox(R, -560, 0, -230, -460, 110, -160, Mat('dirtymetal.jpg', 64), 'detonator stand')
    R.box(-540, 110, -215, -480, 124, -175, Mat('red.jpg', 32), lux=10)
    named(R, 'DETONATOR', -510, 120, -195)
    red_pendant(R, -516, -400, 352, drop=60, power=30, rng=460)
    # W 400: the airlock - showers, benches
    for z in (250, 550):
        R.tube((-560, 352, z), (-560, 300, z), 3, METAL, sides=6, caps=True)
    bench30(R, -700, 300, -600, 500, 'airlock bench')
    cell_light(R, -516, 400, 352)
    # E: SCP-466 behind thick glass
    passage(R, 4, mat=CONC36.but(vs=320, v0=320))
    hall(R, 256, -1000, 1000, 1000, 0, 400, CONC36.but(vs=400, v0=400), FLOOR36, DARK, holes={'W': [(-96, 96, 0, 320)]})
    B.areas.append((256, 1000, -1000, 1000, 400, 0))
    both(R, (520, -1000), (520, 1000), 0, 400, CONC36.but(vs=400, v0=400), [(600, 1400, 60, 300)])
    glass_wall(R, (520, -400), (520, 400), 60, 300)
    R.box(512, 56, -400, 528, 60, 400, METAL, lux=10)
    solid(R, (516, 0, -1000, 524, 400, 1000), 'observation glass wall')
    for z in (-300, 0, 300):
        console30(R, 330, z, 'E', 'observation console %d' % z) if z != 0 else None
    R.rect_floor(560, -500, 960, 500, 0.6, BLOOD)
    R.rect_floor(700, -200, 900, 200, 0.7, Mat('concretefloor.jpg', 64))
    named(R, 'S466', 760, 0, 0)
    named(R, 'GLASS', 520, 160, 0)
    item(R, 'docb42_466', 300, 0, 500)
    R.light(760, 340, 0, rng=600, color=(255, 70, 60), power=40)
    R.light(380, 340, 0, rng=500, color=(240, 240, 235), power=26)
    check33(R)
    return (R, 'CEL', 'E-Block, the Cellar (Heavy Containment): the end of the long tunnel, ribbed and wired with demolition charges; the blast control room, the airlock, and SCP-466 behind thick glass.',
            2, 0.55, ((0, 165, -800), (0, 150, 800)))


ALL = [room2b44panopticon, room3b44toybox, room4b44vault, room2b44cellar]
