"""The thirty-third batch: four new rooms for twenty-three SCPs. Code in IndevU33.bb; textures from make_assets33.py,
models from make_hd33.py, notes from make_docs33.py. SCP texts summarised from scp-wiki.wikidot.com (CC BY-SA 3.0);
rooms and art our own. Style after the user's reference images 90-99:
  ref. 94/96  the white storage corridor: white plaster under a riveted steel trim, black skirting, grey roll-up
              shutters in black frames, a drop ceiling with a grille, dark red pendant lamps, white floor tiles
  ref. 99     the dark corridor: white walls with a black band, buttresses chamfered at the foot, beams overhead,
              a machinery recess, name plates by the doors, single bare bulbs
  ref. 90/95  the bulkhead tunnel: steel frames with chamfered corners, a grating floor, the light at the end
  ref. 91-93  offices: a bullpen of desks, a director's desk with a lamp and a bookcase, peach-striped EZ walls,
              name plates, pendant lamps

  room2b33toys     LCZ  Hall 8 (Little Misters: SCP-1007 in his coffin, SCP-3537 in a glass cell) and the Wondertainment
                        store (SCP-3938 the bicycle, SCP-4876 on a screen, SCP-4890 on a table) - shutter corridor
  room2b33archive  EZ   Site-73's secure archive (SCP-232 in its safe, SCP-865 in the firearms safe, SCP-696 on its
                        table), the decommissioned room (SCP-252-EX, SCP-762-EX in Gibson's locker, SCP-667-2's
                        remains), the research bullpen and Dr. Tolentino's office - peach-striped EZ corridor
  room2b33bio      HCZ  Bio-Site 84 annex: vivarium 3 (SCP-1563), the veterinary lab (SCP-2394 asleep in its tank),
                        SCP-3419's observation room, the Site-84 archive (SCP-7042, SCP-7284's transfer) - ref. 99
  room2b33deep     HCZ  the Site-91 liaison wing (bullpen, Director Varga's office: SCP-5512, SCP-5079's terminal,
                        SCP-5267) and, 768 below by a stairwell, VAULT 4612: SCP-4612-A on its altar in a vault of
                        charred glyph stone, the SCP-4712 vault door, the SCP-3743-A-1 Way, SCP-L043's turntable,
                        an SCP-5079-1 bed - bulkhead corridor

Every solid and picture is recorded and checked (no overlaps, nothing in a doorway, a clear walk down the corridor)."""
from rooms_b30 import *
from rooms_b29 import BARK867, SOIL

PL33 = Mat('indev_plates33.png', cast=False)
PLATES33 = ['hall8', 'toys', 'site73', 'explained', 'viv1563', 'frog', 'colony', 'arch84', 'bullpen', 'varga', 'vault',
            'office73', 'tolentino']
WALL96 = Mat('indev_b33wall96.png', 384)
WALL99 = Mat('indev_b33wall99.png', 384)
TILE96 = Mat('indev_b33tile.png', 384)
CEIL96 = Mat('indev_b33ceil.png', 128)
STONE = Mat('indev_b33stone.png', 320)
RSHADE = Mat('indev_b33shade.png', 128)
PIXEL = Mat('indev_b33pixel.png', cast=False)
DREAM = Mat('indev_b33dream.png', cast=False)
AKIVA = Mat('indev_b33akiva.png', cast=False)
METATRON = Mat('indev_b33metatron.png', cast=False)
COLONY = Mat('indev_b33colony.png', cast=False)
TRANSFER = Mat('indev_b33transfer.png', cast=False)
SKETCHES = Mat('indev_b33sketches.png', cast=False)
RUINS = Mat('indev_b33ruins.png', cast=False)
ASSEMBLY = Mat('indev_b33assembly.png', cast=False)
MISTERS = Mat('indev_b33misters.png', cast=False)
EXPL = Mat('indev_b33ex.png', cast=False)
HISTORY = Mat('indev_b33history.png', cast=False)
VIV = Mat('indev_b33viv.png', cast=False)
ELEC = Mat('ElecBox.jpg', cast=False)
STEEL = Mat('dirtymetal.jpg', 256)
BULKW = Mat('metalpanels2.jpg', 256)
CONCW = Mat('concretewall.jpg', 384)
STYLES['ref96'] = (WALL96, TILE96, CEIL96)
STYLES['ref99'] = (WALL99, Mat('concretefloor.jpg', 256), DARK)
STYLES['bulk33'] = (BULKW, GRATE, DARK)
STYLES['stone33'] = (STONE, Mat('concretefloor.jpg', 256), DARK)
Y0 = -768.0                                                                     # the vault level


def nplate33(R, key, cx, cz, facing, yc=352, w=150):
    i = PLATES33.index(key)
    u0, v0 = (i % 2) * 0.5, (i // 2) * 128 / 896.0
    decal30(R, PL33, cx, cz, facing, w, w * 0.25, yc, 'plate ' + key, uv=(u0, v0, u0 + 0.5, v0 + 128 / 896.0))


def plates33(R, rows):
    for (side, c, key) in rows:
        s = 1 if side == 'E' else -1
        nplate33(R, key, 192 * s, c, 'W' if s > 0 else 'E')


def wing33(name, style, doors, extra=(), amb=10):
    """wing() of batch 30, with extra hub openings ('E'/'W', c) that lead somewhere else than a side room"""
    R = R_(name, amb=amb)
    R.book = Book()
    ops = {'hubE': [], 'hubW': []}
    for (side, c) in list(doors) + list(extra):
        ops['hub' + side].append(door_op(c))
    junction(R, 'NS', style, hub=(-192, -704, 192, 704), openings=ops)
    R.book.areas.append((-192, 192, -1024, 1024, 384))
    rooms = {}
    for (side, c), o in doors.items():
        s = 1 if side == 'E' else -1
        depth, h = o.get('depth', 520), o.get('h', 352)
        span = o.get('span', 300)
        rooms[(side, c)] = annex(R, 'x', 192 * s, s, c - span, c + span, depth, h, o.get('style', style), door=c,
                                 key=o.get('key', 0), spawn_door=o.get('spawn', True))
        x0, z0, x1, z1 = rooms[(side, c)]
        R.book.areas.append((x0, x1, z0, z1, h))
        R.book.doors.append((side, c))
    for (side, c) in extra:
        R.book.doors.append((side, c))
    return R, rooms


def check33(R):
    """check() of batch 30, but the corridor walk only counts solids at standing height in the corridor's own
    storey (the vault under it does not block it)"""
    B = R.book
    bad = []
    inter = lambda a, b, e=0.5: all(a[i] < b[i + 3] - e and b[i] < a[i + 3] - e for i in range(3))
    for i in range(len(B.solids)):
        for j in range(i + 1, len(B.solids)):
            if inter(B.solids[i][0], B.solids[j][0]):
                bad.append('solids overlap: %s / %s' % (B.solids[i][1], B.solids[j][1]))
    for box, name in B.solids:
        ok = any(a[0] - 0.5 <= box[0] and box[3] <= a[1] + 0.5 and a[2] - 0.5 <= box[2] and box[5] <= a[3] + 0.5
                 and box[4] <= a[4] + 0.5 and box[1] >= a[5] - 0.5 for a in [x if len(x) > 5 else x + (0,) for x in B.areas])
        if not ok:
            bad.append('outside its room / into a wall: %s %s' % (name, tuple(int(v) for v in box)))
        for (side, c) in B.doors:
            s = 1 if side == 'E' else -1
            xa, xb = sorted((s * (192 - 110), s * (256 + 110)))
            if inter(box, (xa, 0, c - 110, xb, 320, c + 110)):
                bad.append('in a doorway: %s (door %s %d)' % (name, side, c))
    for z in range(-1000, 1001, 20):
        blocked = sorted((b[0][0], b[0][3]) for b in B.solids
                         if b[0][2] - 1 < z < b[0][5] + 1 and b[0][1] < 200 and b[0][4] > 0.5 and b[0][3] > -192 and b[0][0] < 192)
        x, best = -192.0, 0.0
        for (a0, a1) in blocked:
            best = max(best, a0 - x)
            x = max(x, a1)
        best = max(best, 192 - x)
        if best < 100:
            bad.append('the corridor is blocked at z %d (widest gap %d)' % (z, best))
            break
    for clear, cn in getattr(B, 'clear', []):
        for box, name in B.solids:
            if inter(box, clear):
                bad.append('%s blocks the %s' % (name, cn))
    for i in range(len(B.decals)):
        a = B.decals[i]
        for j in range(i + 1, len(B.decals)):
            b = B.decals[j]
            if a[0] == b[0] and abs(a[1] - b[1]) < 3 and a[2] < b[3] and b[2] < a[3] and a[4] < b[5] and b[4] < a[5]:
                bad.append('pictures overlap: %s / %s' % (a[6], b[6]))
        for (side, c) in B.doors:
            s = 1 if side == 'E' else -1
            if a[0] == 'z' and min(abs(a[1] - s * 192), abs(a[1] - s * 256)) < 3:
                if a[2] < c + 96 and c - 96 < a[3] and a[4] < 320 and a[5] > 0:
                    bad.append('picture over a doorway: %s' % a[6])
                for bz in (c - 154, c + 154):
                    if a[2] < bz + 22 and bz - 22 < a[3] and a[4] < 230 and 120 < a[5]:
                        bad.append('picture over a door button: %s' % a[6])
    if bad:
        raise SystemExit('%s:\n  ' % R.name + '\n  '.join(bad))
    print('  %s: %d solids, %d pictures - no overlaps, passages clear' % (R.name, len(B.solids), len(B.decals)))


def red_pendant(R, x, z, ceil, drop=80, power=55, rng=600):
    """ref. 96: a dark red enamel shade on a short rod"""
    y = ceil - drop
    R.tube((x, y + 22, z), (x, ceil, z), 1.5, DARK, sides=4, caps=False)
    R.prism(octo(x, z, 8, 10), y + 18, y + 24, RSHADE, caps='T')
    R.prism(octo(x, z, 24, 14), y + 6, y + 18, RSHADE, caps='')
    R.prism(octo(x, z, 34, 14), y, y + 6, RSHADE, caps='')
    R.light(x, y - 8, z, rng=rng, color=(255, 226, 190), power=power)


def shutter(R, x, z, facing, w=200, h=260, name='shutter'):
    """ref. 96: a grey roll-up shutter in a heavy black frame (the frame stands 6 out from the wall)"""
    decal30(R, SHUTTER, x, z, facing, w, h, h / 2, '%s %d %d' % (name, x, z))
    s = 1 if facing == 'E' else -1
    xa, xb = sorted((x, x + s * 7))
    for zz in (z - w / 2 - 10, z + w / 2):
        R.box(xa, 0, zz, xb, h + 10, zz + 10, DARK, lux=10)
    R.box(xa, h, z - w / 2, xb, h + 10, z + w / 2, DARK, lux=10)
    solid(R, (xa, 0, z - w / 2 - 10, xb, h + 10, z + w / 2 + 10), '%s frame %d %d' % (name, x, z))


def table33(R, x0, z0, x1, z1, y, name, h=78.0):
    table(R, x0, z0, x1, z1, y=y, h=h)
    solid(R, (x0, y, z0, x1, y + h, z1), name)
    return y + h


def prop33(R, key, x, y, z, size, name):
    """a pivot for a runtime HD prop (IndevU33.bb loads the b3d at it) and the space it takes"""
    named(R, key, x, y, z)
    sx, sy, sz = size
    solid(R, (x - sx / 2, y, z - sz / 2, x + sx / 2, y + sy, z + sz / 2), name)


def glass_wall(R, a, b, y0, y1):
    R.decal(a, b, y0, y1, GLASS, (0, 0, 2, 1), off=0.5)
    R.decal(b, a, y0, y1, GLASS, (0, 0, 2, 1), off=0.5)
    R.collide_wall(a, b, y0, y1)
    R.collide_wall(b, a, y0, y1)


# ================================================================================================ Hall 8 / Wondertainment
def room2b33toys():
    R, rooms = wing33('room2b33toys', 'ref96', {('E', -400): {'style': 'cell30'}, ('E', 400): {'style': 'store27'}}, amb=11)
    hub_dress(R, 'ref96', [], pipes=False)
    plates33(R, [('E', -400, 'hall8'), ('E', 400, 'toys')])
    for z in (-560, -180, 180, 560):                                          # ref. 96: dark red pendants on the axis
        red_pendant(R, 0, z, 384)
    for z in (-370, 370):
        ceil_vent(R, 0, z, 384, size=110, drop=8)
    for z in (-400, 0, 400):                                                   # ref. 96: the roll-up shutters
        shutter(R, -192, z, 'E')
    shutter(R, 192, 0, 'W')
    # Hall 8, Little Misters: SCP-1007 in his coffin, SCP-3537 behind glass
    prop33(R, 'COFFIN', 560, 0, -600, (204, 72, 100), 'SCP-1007 coffin')
    R.book.solids[-1] = ((458, 0, -636, 662, 72, -536), 'SCP-1007 coffin')
    glass_wall(R, (600, -330), (600, -100), 0, 352)
    glass_wall(R, (776, -330), (600, -330), 0, 352)
    R.box(596, 0, -334, 604, 352, -326, STEEL, lux=10)
    R.box(596, 340, -330, 604, 352, -100, STEEL, lux=10)
    R.box(600, 340, -334, 776, 352, -326, STEEL, lux=10)
    solid(R, (596, 0, -334, 776, 352, -100), 'SCP-3537 cell')
    named(R, 'SHAPEY', 690, 0, -215)
    sbox(R, 556, 0, -310, 586, 130, -280, STEEL, 'intercom post', top=CTRL)
    named(R, 'INTERCOM', 571, 130, -295)
    table33(R, 330, -230, 470, -140, 0, 'Hall 8 table')
    item(R, 'key1007', 360, 78, -190)
    item(R, 'doc1007', 420, 78, -205)
    item(R, 'doc3537', 445, 78, -165)
    decal30(R, MISTERS, 340, -700, 'N', 110, 146, 190, 'Little Misters checklist')
    named(R, 'MISTERS', 340, 190, -690)
    decal30(R, KEYPAD, 776, -480, 'W', 40, 60, 160, 'Hall 8 panel')
    ceil_light(R, 420, -560, 352, size=50, power=55, rng=600)
    ceil_light(R, 690, -215, 352, size=40, power=45, rng=420)
    # the Wondertainment store: the bicycle and its rack, the Pixel Buddies screen, the pop-up book
    prop33(R, 'BIKE', 560, 0, 520, (204, 175, 70), 'SCP-3938')
    sbox(R, 460, 0, 580, 660, 50, 592, YEL, 'bike rack')
    office_desk(R, 640, 180, 760, 300, 'E', 'pixel desk', chair=(605, 240))
    decal30(R, PIXEL, 776, 240, 'W', 200, 125, 230, 'pixel buddies screen')
    named(R, 'PIXEL', 770, 230, 240)
    item(R, 'drive4876', 690, 76, 282)
    table33(R, 300, 120, 430, 210, 0, 'book table')
    item(R, 'book4890', 360, 78, 165)
    item(R, 'doc4890', 400, 78, 190)
    item(R, 'doc3938', 330, 78, 195)
    item(R, 'doc4876', 405, 78, 140)
    decal30(R, HISTORY, 420, 700, 'S', 240, 120, 220, 'history page')
    ceil_light(R, 516, 300, 352, size=50, power=60, rng=640)
    ceil_light(R, 560, 560, 352, size=40, power=45, rng=500)
    check33(R)
    return (R, 'TOY', 'Hall 8 and the Wondertainment store (Light Containment): SCP-1007 in his coffin with his key, SCP-3537 behind glass, the Take-You-Anywhere Machine (SCP-3938), the Pixel Buddies (SCP-4876) and the Guide to History (SCP-4890) - ref. 96 shutter corridor.',
            1, 0.45, ((0, 165, -650), (0, 150, 300)))


# ================================================================================================ Site-73 archive
def room2b33archive():
    R, rooms = wing33('room2b33archive', 'ez', {('E', -400): {'style': 'cell30', 'key': 3}, ('E', 400): {'style': 'store27'},
                                               ('W', -400): {}, ('W', 400): {}}, amb=11)
    hub_dress(R, 'ez', [])
    plates33(R, [('E', -400, 'site73'), ('E', 400, 'explained'), ('W', -400, 'office73'), ('W', 400, 'tolentino')])
    for z in (-560, -180, 180, 560):                                          # ref. 93: pendant lamps
        pendant(R, 0, z, 384, power=55, rng=600)
    decal30(R, PR1, 192, 0, 'W', 100, 134, 190, 'hub poster E')
    decal30(R, PR2, -192, 0, 'E', 100, 134, 190, 'hub poster W')
    # Site-73's secure archive room: the safes, SCP-696 on its table, the archive shelves
    sbox(R, 700, 0, -660, 776, 150, -580, STEEL, 'firearms safe 865')
    named(R, 'SAFE865', 695, 100, -620)
    sbox(R, 700, 0, -480, 776, 120, -400, STEEL, 'safe 232')
    named(R, 'SAFE232', 695, 90, -440)
    decal30(R, KEYPAD, 776, -540, 'W', 34, 50, 170, 'safe keypad')
    top = table33(R, 420, -690, 560, -580, 0, 'typewriter table')
    prop33(R, 'TYPE', 490, top, -640, (40, 46, 34), 'SCP-696')
    shelf_unit(R, 400, -160, 640, -100, 'archive shelves')
    cabinets(R, 270, -690, 400, -650, 'archive cabinets')
    item(R, 'doc232', 440, 78, -600)
    item(R, 'doc865', 540, 78, -600)
    item(R, 'doc696', 545, 78, -670)
    ceil_light(R, 516, -400, 352, size=50, power=55, rng=620)
    # decommissioned: the SCP-252-EX casing, "EXPLAINED", Jr. Researcher Gibson's locker, SCP-667-2's remains
    prop33(R, 'BOMB', 520, 0, 560, (240, 60, 64), 'SCP-252-EX')
    decal30(R, EXPL, 520, 700, 'S', 200, 100, 200, 'explained plaque')
    lockers(R, 'x', 776, -1, 140, 404)
    solid(R, (746, 0, 140, 776, 300, 404), 'Gibson lockers')
    named(R, 'LOCKER', 740, 140, 272)
    sbox(R, 400, 0, 150, 470, 100, 220, PANELS, 'remains pedestal', skip='B', top=CHECKER)
    item(R, 'case667', 435, 100, 185)
    table33(R, 560, 150, 700, 240, 0, 'decommissioned table')
    item(R, 'doc252', 600, 78, 190)
    item(R, 'doc667', 650, 78, 210)
    ceil_light(R, 516, 400, 352, size=50, power=55, rng=620)
    # the Site-73 research bullpen (ref. 91)
    for (x0, z0) in ((-715, -680), (-715, -230), (-520, -680), (-520, -230)):
        office_desk(R, x0, z0, x0 + 115, z0 + 90, 'W', 'bullpen desk %d %d' % (x0, z0), chair=(x0 + 150, z0 + 45), lamp=False)
    decal30(R, WB, -776, -400, 'E', 260, 130, 200, 'bullpen whiteboard')
    cabinets(R, -600, -140, -430, -100, 'bullpen cabinets')
    decal30(R, PR1, -516, -700, 'N', 90, 120, 210, 'bullpen poster')
    item(R, 'key3', -460, 76, -660, chance=50)
    for z in (-560, -240):
        ceil_light(R, -516, z, 352, size=44, power=50, rng=560)
    # Dr. Tolentino's office (ref. 92): the desk with its lamp, bookcases, a painting; Gibson's envelope
    office_desk(R, -700, 300, -580, 500, 'E', 'Tolentino desk', chair=(-740, 400))
    shelf_unit(R, -720, 640, -540, 700, 'Tolentino bookcase N')
    shelf_unit(R, -776, 120, -716, 260, 'Tolentino bookcase W')
    model30(R, 'officeseat_a.x', -500, 0, 360, 90, (50, 100, 50), 'visitor chair')
    decal30(R, PAINT, -776, 420, 'E', 96, 96, 200, 'Tolentino painting')
    item(R, 'doc762', -640, 76, 340)
    pendant(R, -640, 400, 352, drop=60, color=(255, 226, 190), power=65, rng=520)
    check33(R)
    return (R, 'ARC', 'Site-73 secure archive (Entrance Zone): SCP-232 and SCP-865 in their safes, SCP-696 on its table; the decommissioned room with SCP-252-EX, SCP-762-EX and SCP-667-2\'s remains; the research bullpen; Dr. Tolentino\'s office - ref. 93 corridor.',
            3, 0.5, ((0, 165, -650), (0, 150, 300)))


# ================================================================================================ Bio-Site 84 annex
def buttress(R, x, z, name):
    """ref. 99: a buttress chamfered at the foot, and the beam across the ceiling to its partner"""
    s = 1 if x < 0 else -1
    xa, xb = sorted((x, x + s * 54))
    R.box(xa, 0, z - 30, xb, 110, z + 30, WALL99.but(us=128, vs=110, v0=0), lux=10)
    xa2, xb2 = sorted((x, x + s * 34))
    R.box(xa2, 110, z - 30, xb2, 344, z + 30, WALL99.but(us=128, vs=384, v0=0), lux=10)
    solid(R, (xa, 0, z - 30, xb, 110, z + 30), name + ' foot')
    solid(R, (xa2, 110, z - 30, xb2, 344, z + 30), name + ' shaft')


def room2b33bio():
    R, rooms = wing33('room2b33bio', 'ref99', {('E', -400): {'style': 'lcz', 'key': 3}, ('E', 400): {'style': 'cell30'},
                                             ('W', -400): {}, ('W', 400): {'style': 'store27'}}, amb=8)
    hub_dress(R, 'ref99', [], pipes=False)
    plates33(R, [('E', -400, 'viv1563'), ('E', 400, 'frog'), ('W', -400, 'colony'), ('W', 400, 'arch84')])
    for z in (-920, -760, -180, 180, 760, 920):
        for x in (-192, 192):
            buttress(R, x, z, 'buttress %d %d' % (x, z))
        R.box(-192, 344, z - 26, 192, 384, z + 26, WALL99.but(us=128, vs=40, v0=0), lux=10)
        solid(R, (-192, 344, z - 26, 192, 384, z + 26), 'beam %d' % z)
    for z in (-560, 0, 560):                                                   # ref. 99: single bare bulbs
        R.box(-10, 370, z - 10, 10, 384, z + 10, METAL, lux=10)
        R.light(0, 360, z, rng=640, color=(255, 246, 230), power=55)
    decal30(R, ELEC, 192, 0, 'W', 170, 200, 170, 'machinery recess')       # ref. 99: the machinery panel
    named(R, 'MACHINE', 188, 170, 0)
    decal30(R, VIV, 192, -700, 'W', 150, 75, 260, 'vivarium sign')
    # vivarium 3: forest floor, three trunks, the stake with SCP-1563
    R.rect_floor(256, -700, 776, -100, 1, SOIL)
    for (x, z) in ((450, -620), (720, -600), (700, -180)):
        R.tube((x, 0, z), (x, 352, z), 18, BARK867, sides=10, caps=False)
        solid(R, (x - 18, 0, z - 18, x + 18, 352, z + 18), 'tree %d %d' % (x, z))
    prop33(R, 'MARKER', 560, 0, -360, (48, 160, 32), 'SCP-1563 stake')
    for z in (-560, -240):
        R.light(560, 300, z, rng=500, color=(200, 255, 200), power=40)
    item(R, 'doc1563', 400, 1, -200)
    # the veterinary lab: SCP-2394 in its tank, the drip, the dream feed
    top = table33(R, 560, 350, 720, 450, 0, 'tank table')
    prop33(R, 'TANK', 640, top, 400, (96, 52, 64), 'SCP-2394 tank')
    named(R, 'FROG', 648, top + 18, 404)
    for k, (x, z) in enumerate(((440, 600), (700, 640), (330, 160))):
        named(R, 'HOP%d' % k, x, 0, z)
    R.tube((520, 0, 330), (520, 180, 330), 2, METAL, sides=6, caps=True)        # the drip stand
    R.box(510, 160, 324, 530, 190, 336, Mat('glass.png', 64, alpha=True, cast=False), lux=10)
    solid(R, (508, 0, 318, 532, 190, 342), 'drip stand')
    named(R, 'DRIP', 520, 150, 330)
    decal30(R, DREAM, 776, 560, 'W', 240, 150, 230, 'dream feed')
    named(R, 'DREAM', 770, 230, 560)
    console30(R, 470, 650, 'S', 'vet console')
    item(R, 'doc2394', 600, 78, 440)
    ceil_light(R, 516, 400, 352, size=50, power=60, rng=640)
    # SCP-3419's observation room: the long window onto the vivarium, the intercom, consoles
    decal30(R, COLONY, -776, -400, 'E', 440, 220, 190, 'colony window')
    named(R, 'WINDOW', -770, 190, -400)
    decal30(R, KEYPAD, -776, -150, 'E', 40, 60, 160, 'colony intercom')
    named(R, 'ALPHA', -770, 160, -150)
    console30(R, -560, -660, 'N', 'observation console')
    bench30(R, -600, -240, -460, -190, 'observation bench')
    item(R, 'doc3419', -520, 0, -560)
    ceil_light(R, -516, -400, 352, size=44, power=40, rng=560, color=(255, 230, 200))
    # the Site-84 archive: shelves, the sketch wall, SCP-7284's transfer notice, Goldie's bed, the sketchbook
    shelf_unit(R, -776, 120, -716, 300, 'archive84 shelves W')
    shelf_unit(R, -560, 640, -380, 700, 'archive84 shelves N')
    decal30(R, SKETCHES, -776, 480, 'E', 300, 150, 210, 'sketch wall')
    decal30(R, TRANSFER, -516, 100, 'N', 120, 160, 200, 'transfer notice')
    named(R, 'TRANSFER', -516, 200, 110)
    sbox(R, -720, 0, 560, -620, 14, 650, Mat('indev_b33shade.png', 64), 'dog bed', skip='B')
    R.prism(octo(-600, 520, 10, 10), 0, 6, METAL, caps='T')
    solid(R, (-610, 0, 510, -590, 6, 530), 'dog bowl')
    named(R, 'GOLDIE', -670, 20, 600)
    table33(R, -560, 300, -400, 420, 0, 'archive84 table')
    item(R, 'book7042', -500, 78, 340)
    item(R, 'doc7042', -440, 78, 380)
    item(R, 'doc7284', -470, 78, 400)
    ceil_light(R, -516, 400, 352, size=44, power=55, rng=600)
    check33(R)
    return (R, 'BIO', 'Bio-Site 84 annex (Heavy Containment): vivarium 3 (SCP-1563), SCP-2394 asleep in its tank, SCP-3419\'s observation room, the Site-84 archive (SCP-7042, SCP-7284) - ref. 99 buttressed corridor.',
            2, 0.5, ((0, 165, -650), (0, 150, 300)))


# ================================================================================================ Site-91 and VAULT 4612
def bulkhead(R, z, name, h=384):
    """ref. 95: a steel frame across the corridor with chamfered upper corners"""
    for x in (-192, 162):
        sbox(R, x, 0, z - 14, x + 30, h - 52, z + 14, STEEL, '%s post %d' % (name, x))
    sbox(R, -192, h - 52, z - 14, 192, h, z + 14, STEEL, name + ' head')
    for (x0, x1) in ((-162, -136), (136, 162)):
        R.box(x0, h - 80, z - 12, x1, h - 52, z + 12, STEEL, lux=10)
        solid(R, (x0, h - 80, z - 12, x1, h - 52, z + 12), '%s corner %d' % (name, x0))


def flight33(R, x_start, direction, z0, z1, y_top, name, rail_z, n=14, run=32.0, drop=256.0, floor=-1e9):
    for i in range(n):
        xa = x_start + direction * run * i
        xb = xa + direction * run
        top = y_top - drop * (i + 1) / n
        sbox(R, min(xa, xb), max(top - 22, floor), z0, max(xa, xb), top, z1, CHECKER, '%s step %d' % (name, i))
    xe = x_start + direction * run * n
    R.tube((x_start, y_top - drop / n + 100, rail_z), (xe, y_top - drop + 100, rail_z), 3.5, YEL, sides=6, caps=True)
    for k in range(0, n + 1, 4):
        x = x_start + direction * run * k
        y = y_top - drop * k / n
        R.tube((x, y, rail_z), (x, y + 100, rail_z), 3, YEL, sides=6, caps=True)


def room2b33deep():
    R, rooms = wing33('room2b33deep', 'bulk33', {('W', -400): {'style': 'ez'}, ('W', 400): {'style': 'ez'}},
                      extra=[('E', -400)], amb=8)
    B = R.book
    hub_dress(R, 'bulk33', [], pipes=False)
    plates33(R, [('W', -400, 'bullpen'), ('W', 400, 'varga'), ('E', -400, 'vault')])
    for z in (-920, -760, -180, 0, 180, 760, 920):                            # ref. 95: the bulkheads
        bulkhead(R, z, 'bulkhead %d' % z)
    for z in (-560, -280, 280, 560):
        R.box(-20, 374, z - 30, 20, 384, z + 30, METAL, bottom=LIGHTPANEL, lux=10)
        R.light(0, 350, z, rng=520, color=(255, 214, 160), power=40)
    R.light(0, 300, 990, rng=700, color=(255, 255, 250), power=90)            # the light at the end (ref. 95)
    # the jamb and the door to the stairwell
    hall(R, 192, -496, 256, -304, 0, 320, BULKW, GRATE, DARK, holes={'W': [(-496, -304, 0, 320)], 'E': [(-496, -304, 0, 320)]})
    R.spawns.append(dict(kind='door', pos=(224, 0, -400), angle=90, key=3))
    # ---------------- the stairwell: x 256..960, z -700..-100, from the vault (y -768) to 352
    hall(R, 256, -700, 960, -100, Y0, 352 - Y0, CONCW, Mat('concretefloor.jpg', 256), DARK,
         holes={'W': [(-496, -304, 0, 320)], 'N': [(864, 956, Y0, Y0 + 300)]})
    B.areas.append((256, 960, -700, -100, 352, Y0))
    sbox(R, 256, -16, -700, 420, 0, -100, CHECKER, 'top landing', skip='')
    flight33(R, 420, 1, -700, -560, 0, 'flight 1', -556)
    sbox(R, 868, -272, -700, 960, -256, -100, CHECKER, 'landing 1', skip='')
    flight33(R, 868, -1, -240, -100, -256, 'flight 2', -244)
    sbox(R, 256, -528, -700, 420, -512, -100, CHECKER, 'landing 2', skip='')
    flight33(R, 420, 1, -700, -560, -512, 'flight 3', -556, n=13, drop=256 * 13 / 14.0, floor=Y0)
    sbox(R, 420, Y0, -545, 868, 352, -255, CONCW, 'stair core')
    for (x, y) in ((424, 0), (864, -256), (424, -512)):                       # rails across the stair eye
        R.tube((x, y + 100, -255), (x, y + 100, -100 if x < 600 else -240), 3.5, YEL, sides=6, caps=True)
    R.tube((424, 100, -240), (424, 100, -100), 3.5, YEL, sides=6, caps=True)
    solid(R, (420, 0, -255, 428, 104, -100), 'top rail')
    for k, y in enumerate((0, -256, -512)):                                   # a caged lamp over every landing
        x = 940 if k % 2 else 276
        R.box(x - 12 if x > 600 else x - 20, y + 236, -412, x + 20 if x < 600 else x + 12, y + 260, -388, METAL, bottom=LIGHTPANEL, lux=10)
        R.light(x + (-30 if x > 600 else 30), y + 230, -400, rng=720, color=(255, 230, 196), power=75)
        R.light(640, y + 200, -630, rng=520, color=(255, 230, 196), power=35)
    R.light(900, Y0 + 230, -400, rng=640, color=(200, 220, 255), power=60)
    B.clear = [((268, 0, -690, 410, 200, -110), 'top landing walk'), ((880, Y0, -690, 950, Y0 + 260, -110), 'stair foot')]
    # ---------------- VAULT 4612: x -760..960, z -100..900, 480 high, charred glyph stone
    hall(R, -760, -100, 960, 900, Y0, 480, STONE, Mat('concretefloor.jpg', 256), DARK, holes={'S': [(864, 956, Y0, Y0 + 300)]})
    B.areas.append((-760, 960, -100, 900, Y0 + 480, Y0))
    for (x0, x1) in ((856, 864), (956, 964)):
        R.box(x0, Y0, -108, x1, Y0 + 300, -92, STEEL, lux=10)
    R.box(856, Y0 + 300, -108, 964, Y0 + 312, -92, STEEL, lux=10)
    R.rect_floor(-380, 180, 580, 720, Y0 + 1, STONE.but(us=192))              # the altar's paving
    for (x0, z0, x1, z1) in ((-388, 172, 588, 180), (-388, 720, 588, 728), (-388, 180, -380, 720), (580, 180, 588, 720)):
        R.box(x0, Y0, z0, x1, Y0 + 3, z1, STEEL, lux=10)
    prop33(R, 'CADAVER', 100, Y0, 450, (820, 210, 390), 'SCP-4612-A')
    named(R, 'CRYSTAL', 120, Y0 + 30, 290)
    decal30(R, AKIVA, 300, 900, 'S', 240, 150, Y0 + 230, 'Akiva meter')
    named(R, 'AKIVA', 300, Y0 + 230, 890)
    prop33(R, 'VAULTDOOR', -450, Y0, 870, (500, 340, 60), 'SCP-4712 door')
    R.book.solids[-1] = ((-640, Y0, 830, -140, Y0 + 340, 900), 'SCP-4712 door')
    prop33(R, 'WAY', -600, Y0, 300, (230, 300, 44), 'SCP-3743-A-1')
    named(R, 'ICON', -547, Y0 + 210, 304)
    top = table33(R, 600, 700, 760, 820, Y0, 'turntable table')
    prop33(R, 'TURNTABLE', 680, top, 760, (50, 16, 38), 'SCP-L043')
    prop33(R, 'BED5079', 420, Y0, 60, (204, 120, 92), 'SCP-5079-1 bed')
    for (x, z) in ((-560, 100), (-560, 700), (-180, 100)):
        sbox(R, x - 34, Y0, z - 34, x + 34, Y0 + 480, z + 34, STONE.but(us=136), 'vault pillar %d %d' % (x, z))
    item(R, 'doc4612', 900, Y0, 40)
    item(R, 'docl043', 640, top, 800)
    item(R, 'doc3743', -420, Y0, 360)
    item(R, 'doc5079', 540, Y0, 120)
    R.light(100, Y0 + 320, 450, rng=1100, color=(140, 180, 255), power=110)    # the body's cold blue glow
    R.light(100, Y0 + 60, 450, rng=600, color=(70, 130, 255), power=60)
    for (x, z) in ((-450, 600), (680, 500), (-300, 120), (700, 120), (-450, 250), (300, 780)):
        ceil_light(R, x, z, Y0 + 480, size=44, power=70, rng=820, color=(225, 232, 255))
    R.light(910, Y0 + 220, 200, rng=600, color=(255, 230, 200), power=55)      # by the stair door
    B.clear.append(((800, Y0, -95, 960, Y0 + 260, 690), 'vault walk from the stairs'))
    # ---------------- the Site-91 liaison bullpen (ref. 91): SCP-5512, SCP-5079's terminal
    for (x0, z0) in ((-715, -680), (-715, -230), (-520, -680), (-520, -230)):
        office_desk(R, x0, z0, x0 + 115, z0 + 90, 'W', 'liaison desk %d %d' % (x0, z0), chair=(x0 + 150, z0 + 45), lamp=False)
    decal30(R, METATRON, -776, -400, 'E', 240, 150, 220, 'METATRON terminal')
    named(R, 'TERM', -770, 220, -400)
    decal30(R, ASSEMBLY, -516, -100, 'S', 110, 146, 200, 'Assembly pamphlet')
    named(R, 'PAMPHLET', -516, 200, -110)
    item(R, 'doc5512', -480, 76, -200)
    for z in (-560, -240):
        ceil_light(R, -516, z, 352, size=44, power=50, rng=560)
    # Director Varga's office (ref. 92): the desk and lamp, bookcases, the SCP-5267 diorama and photographs
    office_desk(R, -700, 300, -580, 500, 'E', 'Varga desk', chair=(-740, 400))
    shelf_unit(R, -720, 640, -540, 700, 'Varga bookcase N')
    shelf_unit(R, -776, 120, -716, 260, 'Varga bookcase W')
    top = table33(R, -470, 140, -310, 240, 0, 'diorama table')
    prop33(R, 'DIORAMA', -390, top, 190, (160, 40, 110), 'SCP-5267 diorama')
    decal30(R, RUINS, -516, 700, 'S', 260, 130, 210, 'SCP-5267 photographs')
    item(R, 'doc5267', -640, 76, 340)
    item(R, 'doc4712', -620, 76, 460)
    pendant(R, -640, 400, 352, drop=60, color=(255, 226, 190), power=65, rng=520)
    check33(R)
    return (R, 'DEEP', 'Site-91 liaison wing and VAULT 4612 (Heavy Containment): the liaison bullpen and Director Varga\'s office (SCP-5512, SCP-5079, SCP-5267), and 768 below by the stairs the vault of charred glyph stone: SCP-4612-A on its altar, the SCP-4712 vault door, the SCP-3743-A-1 Way, SCP-L043\'s turntable - ref. 95 bulkhead corridor.',
            2, 0.5, ((0, 165, -650), (0, 150, 300)))


ALL = [room2b33toys, room2b33archive, room2b33bio, room2b33deep]
