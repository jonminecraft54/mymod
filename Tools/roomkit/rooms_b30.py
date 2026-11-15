"""The thirtieth batch: Site-42, the Foundation's site for sapient anomalies (after the public reveal, a small town of
a site with a public-relations wing). Code in IndevU30.bb; textures from make_assets30.py, models from make_hd30.py,
notes from make_docs30.py. SCP texts summarised from scp-wiki.wikidot.com (CC BY-SA 3.0); rooms and art our own.
The style follows the user's reference images 60-75 (EZ offices with peach-striped walls and pendant lamps, white
LCZ walls under black ceilings, pilastered corridors, roll-up shutters, the humanoid cell with bed, toilet and sink).

Layout: every room is a corridor (the hub, x -192..192, z -704..704, arms to the doors at z +-1024) with side rooms
behind doors at z = c (c = -400, 0 or +400); a side room runs x 256..776 (east) / -776..-256 (west), z c-300..c+300.

NO OVERLAPS: every piece of furniture, every model and every wall picture goes through solid() / model30() /
decal30(), which record it; check() then fails the build if
  * two solids intersect (things standing ON something - a monitor on a desk - touch, they do not intersect),
  * a solid leaves its room (the hub or a side room) or pokes into a wall,
  * a solid stands in a doorway or in the 110-unit strip in front of it on either side,
  * two pictures on the same wall overlap, or a picture covers a doorway or one of the game's door buttons
    (they sit 154 units either side of a door, 120-230 high, on both faces of the wall)."""
import math
from rooms_b29 import *

PL30 = Mat('indev_plates30.png', cast=False)
PLAQUE = Mat('indev_s42plaque.png', cast=False)
PR1 = Mat('indev_s42poster1.png', cast=False)
PR2 = Mat('indev_s42poster2.png', cast=False)
BOARD30 = Mat('indev_s42board.png', cast=False)
ATLANTIC = Mat('indev_s42atlantic.png', cast=False)
THERM = Mat('indev_s42thermal.png', cast=False)
HUME = Mat('indev_s42hume.png', cast=False)
NET = Mat('indev_s42netting.png', 256)
FEEDS = Mat('indev_s42feeds.png', cast=False)
AD4434 = Mat('indev_s42ad4434.png', cast=False)
CONT = Mat('indev_s42container.png', 256)
LAMBDA = Mat('indev_s42lambda.png', cast=False)
COUNT = Mat('indev_s42count.png', cast=False)
CONE = Mat('indev_s42cone.png', 64)
SHADE = Mat('scpcb_lampshade.jpg', 128)
CABTEX = Mat('scpcb_cabinet.jpg', 64, 176)
EXT = Mat('fire_extinguisher.jpg', cast=False)
KEYPAD = Mat('KeyPad.jpg', cast=False)
YEL = Mat('yellowmetal.jpg', 256)
SHUTTER = Mat('indev_shutter19.png', cast=False)
STYLES['cell30'] = (Mat('whitewall.jpg', 364), TILE, DARK)            # reference 66: white walls, tiles, black ceiling
PLATES30 = ['sherman', 'media', 'ethics', 'multiu', 'g14', 'lockers', 'room35', 'thermal', 'ocean', 'gamma6',
            'outposts', 'evidence', 'scp2648', 'storage']


# ================================================================================================ the bookkeeping
class Book:
    def __init__(self):
        self.solids, self.decals, self.areas, self.doors = [], [], [], []


def solid(R, box, name):
    """record a solid (x0, y0, z0, x1, y1, z1) - furniture, machinery, anything you can walk into"""
    x0, y0, z0, x1, y1, z1 = box
    R.book.solids.append(((min(x0, x1), min(y0, y1), min(z0, z1), max(x0, x1), max(y0, y1), max(z0, z1)), name))


def sbox(R, x0, y0, z0, x1, y1, z1, mat, name, **kw):
    kw.setdefault('lux', 10)
    R.box(x0, y0, z0, x1, y1, z1, mat, **kw)
    solid(R, (x0, y0, z0, x1, y1, z1), name)


def model30(R, file, x, y, z, yaw, size, name=None):
    """a prop model, size = (sx, sy, sz) as it stands at yaw 0"""
    R.model(file, x, y, z, rot=(0, yaw, 0), scale=(1, 1, 1))
    sx, sy, sz = size
    if int(yaw) % 180 == 90:
        sx, sz = sz, sx
    solid(R, (x - sx / 2, y, z - sz / 2, x + sx / 2, y + sy, z + sz / 2), name or file)


def decal30(R, mat, cx, cz, facing, w, h, yc, name, uv=(0, 0, 1, 1)):
    wall_decal(R, mat, cx, cz, facing, w, h, yc, uv=uv)
    along = 'z' if facing in 'EW' else 'x'
    plane = cx if along == 'z' else cz
    c = cz if along == 'z' else cx
    R.book.decals.append((along, plane, c - w / 2, c + w / 2, yc - h / 2, yc + h / 2, name))


def nplate(R, key, cx, cz, facing, yc=352, w=150):
    """a name plate (indev_plates30.png, 2 x 7 cells of 512 x 128) - over the door, clear of its buttons"""
    i = PLATES30.index(key)
    u0, v0 = (i % 2) * 0.5, (i // 2) * 128 / 896.0
    decal30(R, PL30, cx, cz, facing, w, w * 0.25, yc, 'plate ' + key, uv=(u0, v0, u0 + 0.5, v0 + 128 / 896.0))


def check(R):
    B = R.book
    bad = []
    inter = lambda a, b, e=0.5: all(a[i] < b[i + 3] - e and b[i] < a[i + 3] - e for i in range(3))
    for i in range(len(B.solids)):
        for j in range(i + 1, len(B.solids)):
            if inter(B.solids[i][0], B.solids[j][0]):
                bad.append('solids overlap: %s / %s' % (B.solids[i][1], B.solids[j][1]))
    for box, name in B.solids:
        ok = any(a[0] - 0.5 <= box[0] and box[3] <= a[1] + 0.5 and a[2] - 0.5 <= box[2] and box[5] <= a[3] + 0.5
                 and box[4] <= a[4] + 0.5 for a in B.areas)
        if not ok:
            bad.append('outside its room / into a wall: %s %s' % (name, tuple(int(v) for v in box)))
        for (side, c) in B.doors:
            s = 1 if side == 'E' else -1
            xa, xb = sorted((s * (192 - 110), s * (256 + 110)))
            if inter(box, (xa, 0, c - 110, xb, 320, c + 110)):
                bad.append('in a doorway: %s (door %s %d)' % (name, side, c))
    # a clear walk the length of the corridor: some strip of the hub at least 100 wide must be free of solids
    # everywhere between the two ends (at standing height, below 200)
    for z in range(-1000, 1001, 20):
        blocked = sorted((b[0][0], b[0][3]) for b in B.solids
                         if b[0][2] - 1 < z < b[0][5] + 1 and b[0][1] < 200 and b[0][3] > -192 and b[0][0] < 192)
        x, best = -192.0, 0.0
        for (a0, a1) in blocked:
            best = max(best, a0 - x)
            x = max(x, a1)
        best = max(best, 192 - x)
        if best < 100:
            bad.append('the corridor is blocked at z %d (widest gap %d)' % (z, best))
            break
    for i in range(len(B.decals)):
        a = B.decals[i]
        for j in range(i + 1, len(B.decals)):
            b = B.decals[j]
            if a[0] == b[0] and abs(a[1] - b[1]) < 3 and a[2] < b[3] and b[2] < a[3] and a[4] < b[5] and b[4] < a[5]:
                bad.append('pictures overlap: %s / %s' % (a[6], b[6]))
        for (side, c) in B.doors:
            s = 1 if side == 'E' else -1
            if a[0] == 'z' and min(abs(a[1] - s * 192), abs(a[1] - s * 256)) < 3:
                if a[2] < c + 96 and c - 96 < a[3] and a[4] < 320:
                    bad.append('picture over a doorway: %s' % a[6])
                for bz in (c - 154, c + 154):
                    if a[2] < bz + 22 and bz - 22 < a[3] and a[4] < 230 and 120 < a[5]:
                        bad.append('picture over a door button: %s' % a[6])
    if bad:
        raise SystemExit('%s:\n  ' % R.name + '\n  '.join(bad))
    print('  %s: %d solids, %d pictures - no overlaps' % (R.name, len(B.solids), len(B.decals)))


# ================================================================================================ building blocks
def wing(name, style, doors, amb=10):
    """the corridor and its side rooms: doors = {(side, c): dict(key=0, spawn=True, style=..., h=352, depth=520)}"""
    R = R_(name, amb=amb)
    R.book = Book()
    ops = {'hubE': [], 'hubW': []}
    for (side, c) in doors:
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
    return R, rooms


def pendant(R, x, z, ceil, drop=70, color=(255, 236, 210), power=60, rng=560):
    """a hanging lamp (reference images 61, 65, 71): cord, a cone shade, the bulb's light (above head height)"""
    y = ceil - drop
    R.tube((x, y + 26, z), (x, ceil, z), 1.5, DARK, sides=4, caps=False)
    R.prism(octo(x, z, 12, 10), y + 18, y + 26, SHADE, caps='T')
    R.prism(octo(x, z, 26, 12), y + 6, y + 18, SHADE, caps='')
    R.prism(octo(x, z, 34, 12), y, y + 6, SHADE, caps='')
    R.light(x, y - 8, z, rng=rng, color=color, power=power)


def cone(R, x, z):
    R.prism(octo(x, z, 20, 4), 0, 4, DARK, caps='T')
    R.prism(octo(x, z, 12, 8), 4, 44, CONE, caps='')
    R.prism(octo(x, z, 4, 8), 44, 56, CONE, caps='T')


def office_desk(R, x0, z0, x1, z1, facing, name, chair=None, lamp=True):
    """a desk, a monitor, keyboard, mug and lamp on it; the sitter faces `facing`; chair = (x, z)"""
    top = desk(R, x0, z0, x1, z1, 0)
    solid(R, (x0, 0, z0, x1, top, z1), name)
    cx, cz = (x0 + x1) / 2, (z0 + z1) / 2
    yaw = {'E': 270, 'W': 90, 'N': 180, 'S': 0}[facing]
    back = {'E': (1, 0), 'W': (-1, 0), 'N': (0, 1), 'S': (0, -1)}[facing]
    mx, mz = cx + back[0] * 18, cz + back[1] * 18
    model30(R, 'monitor.x', mx, top, mz, yaw, (40, 40, 26), name + ' monitor')
    model30(R, 'keyboard.x', cx - back[0] * 22, top, cz - back[1] * 22, yaw, (40, 4, 14), name + ' keyboard')
    model30(R, 'mug.x', x0 + 14, top, z0 + 14, 0, (8, 10, 8), name + ' mug')
    if lamp:
        model30(R, 'lamp1.x', x1 - 16, top, z1 - 16, 0, (16, 40, 16), name + ' lamp')
    if chair:
        model30(R, 'officeseat_a.x', chair[0], 0, chair[1], yaw, (50, 100, 50), name + ' chair')
    return top


def cabinets(R, x0, z0, x1, z1, name):
    """a run of steel filing cabinets (scpcb_cabinet texture), 140 high"""
    sbox(R, x0, 0, z0, x1, 140, z1, CABTEX, name, skip='B')


def shelf_unit(R, x0, z0, x1, z1, name, h=230):
    shelving(R, x0, z0, x1, z1, h=h)
    solid(R, (x0, 0, z0, x1, h, z1), name)


def bench30(R, x0, z0, x1, z1, name):
    bench(R, x0, z0, x1, z1)
    solid(R, (x0, 0, z0, x1, 78, z1), name)


def table30(R, x0, z0, x1, z1, name, h=78.0):
    table(R, x0, z0, x1, z1, h=h)
    solid(R, (x0, 0, z0, x1, h, z1), name)
    return h


def console30(R, x, z, facing, name):
    console(R, x, z, facing)
    w, d = (192, 80) if facing in 'NS' else (80, 192)
    solid(R, (x - w / 2, 0, z - d / 2, x + w / 2, 208, z + d / 2), name)


def hub_dress(R, style, plates, ceil=384, pipes=True):
    """detail for every corridor: pipes and a cable tray along the ceiling, low vents, an extinguisher cabinet, the
    plates over the doors"""
    if pipes:
        pipes_z(R, [(150, ceil - 26, 8), (128, ceil - 22, 5)], -990, 990)
        R.box(-170, ceil - 30, -990, -110, ceil - 26, 990, GRATE, lux=10)                  # the cable tray
    for z in (-650, 650):
        decal30(R, VENT, -192 if z < 0 else 192, z, 'E' if z < 0 else 'W', 70, 40, 40, 'vent %d' % z)
    sbox(R, -192, 90, 596, -178, 190, 646, Mat('red.jpg', 64), 'extinguisher cabinet')
    decal30(R, EXT, -177, 621, 'E', 44, 86, 140, 'extinguisher')
    for (side, c, key) in plates:
        s = 1 if side == 'E' else -1
        nplate(R, key, 192 * s, c, 'W' if s > 0 else 'E')


# ================================================================================================ administration
def room2b30admin():
    R, rooms = wing('room2b30admin', 'ez', {('E', -400): {}, ('E', 400): {}, ('W', -400): {}, ('W', 400): {}}, amb=11)
    hub_dress(R, 'ez', [('E', -400, 'sherman'), ('E', 400, 'media'), ('W', -400, 'ethics'), ('W', 400, 'multiu')])
    for z in (-560, -180, 180, 560):
        pendant(R, 0, z, 384, power=55, rng=600)
    for z in (-370, 370):
        ceil_vent(R, 0, z, 384, size=80, drop=30)
    decal30(R, PR1, 192, 0, 'W', 100, 134, 190, 'poster PR1')
    decal30(R, PR2, -192, 0, 'E', 100, 134, 190, 'poster PR2')
    decal30(R, PLAQUE, 0, 704, 'S', 140, 140, 250, 'plaque hub')
    sbox(R, -192, 0, -190, -150, 120, -150, WHITEP, 'water cooler')                        # a water cooler
    R.tube((-171, 120, -170), (-171, 170, -170), 16, Mat('glass.png', 64, alpha=True, cast=False), sides=10, caps=True)
    # Site Director Dr. T. Sherman: the desk facing the door, two visitor chairs, a bookcase, cabinets, the plaque
    top = office_desk(R, 580, -520, 700, -300, 'W', 'director desk', chair=(740, -410))
    model30(R, 'officeseat_a.x', 500, 0, -470, 270, (50, 100, 50), 'visitor chair 1')
    model30(R, 'officeseat_a.x', 500, 0, -350, 270, (50, 100, 50), 'visitor chair 2')
    named(R, 'SHERMAN', 640, top + 20, -410)
    item(R, 'docpr42', 610, top, -470)
    item(R, 'docsite42', 640, top, -330)
    item(R, 'keygatev', 600, top, -385)                                                # the Gate V access card (batch 32)
    cabinets(R, 320, -140, 480, -100, 'director cabinets')
    shelf_unit(R, 716, -690, 776, -580, 'director bookcase 1')
    shelf_unit(R, 716, -230, 776, -120, 'director bookcase 2')
    decal30(R, PLAQUE, 776, -410, 'W', 110, 110, 270, 'plaque director')
    decal30(R, WMON, 500, -700, 'N', 100, 100, 210, 'director monitor wall')
    decal30(R, PR1, 600, -100, 'S', 90, 120, 210, 'director poster')
    pendant(R, 640, -410, 352, drop=60, color=(255, 230, 200), power=70, rng=520)
    ceil_light(R, 400, -560, 352, size=36, power=40, rng=500)
    # Media Relations & Support: four desks in two facing pairs, the inquiries board, posters
    for (x0, z0, f, cx) in ((440, 220, 'E', 405), (440, 440, 'E', 405), (600, 220, 'W', 748), (600, 440, 'W', 748)):
        office_desk(R, x0, z0, x0 + 115, z0 + 90, f, 'media desk %d %d' % (x0, z0), chair=(cx, z0 + 45), lamp=False)
    decal30(R, BOARD30, 776, 400, 'W', 300, 150, 230, 'inquiries board')
    named(R, 'BOARD', 770, 230, 400)
    decal30(R, PR2, 500, 700, 'S', 100, 134, 210, 'media poster 2')
    decal30(R, PR1, 660, 100, 'N', 100, 134, 210, 'media poster 1')
    item(R, 'doc4427', 470, 76, 250)
    for z in (300, 520):
        ceil_light(R, 516, z, 352, size=44, power=55, rng=600)
    # the Ethics Subcommittee: a meeting table with chairs, a painting, the plaque
    meeting(R, -540, -400, along='x', length=240, width=130)
    solid(R, (-700, 0, -505, -380, 104, -295), 'ethics table and chairs')
    decal30(R, PAINT, -776, -400, 'E', 96, 96, 200, 'ethics painting')
    decal30(R, PLAQUE, -516, -700, 'N', 110, 110, 230, 'ethics plaque')
    named(R, 'ETHICS', -540, 100, -400)
    item(R, 'doc4433', -580, 78, -380)
    pendant(R, -540, -400, 352, drop=60, power=65, rng=560)
    # the Multi-U Dept.: a research desk, cabinets, a whiteboard of G14 notes
    office_desk(R, -700, 300, -580, 520, 'E', 'multiu desk', chair=(-545, 410))
    decal30(R, WB, -516, 700, 'S', 240, 120, 190, 'multiu whiteboard')
    cabinets(R, -480, 110, -300, 150, 'multiu cabinets')
    named(R, 'MULTIU', -640, 110, 410)
    item(R, 'doc2758', -650, 76, 340)
    ceil_light(R, -516, 400, 352, size=44, power=60, rng=620)
    check(R)
    return (R, 'ADM', 'Site-42 Administration (Entrance Zone): Site Director Dr. T. Sherman\'s office, Media Relations & Support, the Ethics Subcommittee for Sentient & Sapient Anomalies and the Multi-U Dept.',
            3, 0.4, ((0, 165, -650), (0, 150, 300)))


# ================================================================================================ Wing A4: SCP-2758
def room2b30a4():
    R, rooms = wing('room2b30a4', 'pillar', {('E', -400): {'spawn': False, 'style': 'cell30'}, ('E', 400): {},
                                             ('W', -400): {}}, amb=10)
    hub_dress(R, 'pillar', [('E', -400, 'g14'), ('E', 400, 'lockers')])
    for x in (-192, 192):                                                     # pilasters, clear of the doorways
        pilasters(R, 'x', x, 1 if x < 0 else -1, -680, 680, 680, 384)
        for z in (-680, 0, 680):
            solid(R, (min(x, x + (18 if x < 0 else -18)), 0, z - 22, max(x, x + (18 if x < 0 else -18)), 384, z + 22), 'pilaster %d %d' % (x, z))
    for z in (-500, 0, 500):
        ceil_light(R, 0, z, 384, size=40, power=55, rng=700)
    decal30(R, Mat('ElecBox.jpg', cast=False), -192, 400, 'E', 160, 200, 200, 'machine panel')     # ref. 63
    bench30(R, -190, -260, -130, -60, 'hub bench')
    ndoor(R, 'G14', 224, 0, -400, 90, locked=True)
    decal30(R, KEYPAD, 192, -620, 'W', 40, 60, 160, 'G14 card reader')
    named(R, 'READER', 188, 160, -620)
    # Room G14: a standard humanoid containment chamber (ref. 66) - bed, toilet, sink, a table and chair with the mic
    model30(R, 'dclass_bed.x', 715, 0, -580, 0, (100, 50, 200), 'G14 bed')
    model30(R, 'dclass_toilet.x', 735, 0, -170, 270, (60, 60, 40), 'G14 toilet')
    model30(R, 'dclass_sink.x', 610, 60, -125, 180, (50, 30, 40), 'G14 sink')
    table30(R, 400, -480, 540, -360, 'G14 table')
    model30(R, 'scpcb_chair.x', 575, 0, -420, 270, (40, 104, 40), 'G14 chair')
    R.tube((440, 78, -420), (440, 128, -420), 2, METAL, sides=6, caps=True)            # the microphone stand
    R.box(432, 128, -428, 448, 140, -412, DARK, lux=10)
    named(R, 'MIC', 440, 130, -420)
    named(R, 'FIGURE', 540, 20, -230)
    ceil_light(R, 516, -400, 352, size=50, power=60, rng=640)
    # the Safe-class lockers: locker #2758 holds G14's identification card
    lockers(R, 'x', 776, -1, 140, 660)
    solid(R, (746, 0, 140, 776, 300, 660), 'lockers east')
    lockers(R, 'z', 700, -1, 300, 690)
    solid(R, (300, 0, 670, 690, 300, 700), 'lockers north')
    named(R, 'LOCKER', 740, 140, 300)
    sbox(R, 420, 0, 400, 640, 44, 440, WOOD, 'locker bench', skip='B')
    ceil_light(R, 516, 400, 352, size=44, power=55, rng=620)
    # the recording booth: consoles, a desk, the interview archive
    console30(R, -730, -600, 'E', 'booth console 1')
    console30(R, -730, -200, 'E', 'booth console 2')
    office_desk(R, -520, -660, -400, -560, 'W', 'booth desk', chair=(-360, -610))
    cabinets(R, -480, -140, -300, -100, 'booth cabinets')
    item(R, 'doc2758', -470, 76, -590)
    ceil_light(R, -516, -400, 352, size=44, power=50, rng=600)
    check(R)
    return (R, 'A4', 'Safe-Class Containment Wing A4 (Light Containment): Room G14 behind its custom-ID door, the Safe-class lockers and the recording booth.',
            1, 0.5, ((0, 165, -650), (0, 150, 300)))


# ================================================================================================ Wing B4: SCP-4427
def room2b30b4():
    R, rooms = wing('room2b30b4', 'hcz', {('E', -400): {'key': 4, 'style': 'cell30'}, ('E', 400): {}, ('W', -400): {}}, amb=9)
    hub_dress(R, 'hcz', [('E', -400, 'room35'), ('E', 400, 'thermal')])
    for z in (-560, 560):
        ceil_light(R, 0, z, 384, size=40, power=55, rng=700)
    red_lamp(R, 0, 120, 384, power=50, rng=500)
    # SCP-4427: 1.5 m up over the middle of the corridor, a cordon of stanchions and tape round it, open to the north
    named(R, 'SPHERE', 0, 240, 0)
    # a tight cordon (the sphere is only 60 cm across): 120 x 120, so both sides of the corridor stay 110+ wide
    posts = [(-60, -60), (60, -60), (60, 60), (-60, 60)]
    for (x, z) in posts:
        R.tube((x, 0, z), (x, 100, z), 4, YEL, sides=8, caps=True)
        R.prism(octo(x, z, 12, 8), 0, 6, DARK, caps='T')
        solid(R, (x - 12, 0, z - 12, x + 12, 100, z + 12), 'stanchion %d %d' % (x, z))
    for (a, b) in ((posts[0], posts[1]), (posts[1], posts[2]), (posts[3], posts[0])):          # tape on three sides
        x0, x1 = sorted((a[0], b[0]))
        z0, z1 = sorted((a[1], b[1]))
        R.box(x0 - 1, 88, z0 - 1, x1 + 1, 96, z1 + 1, CONE, lux=10)
    # the walkways either side of it must stay clear for the player (the checker treats them like doorways)
    R.book.lanes = [(-192, -72), (72, 192)]
    for z in (-220, 220):
        ceil_light(R, 0, z, 384, size=40, power=55, rng=650)
    decal30(R, COUNT, -192, 0, 'E', 110, 110, 200, 'contact counter')
    named(R, 'COUNT', -186, 200, 0)
    # Room 35: SCP-4427-B. Scranton netting on the walls, a bed, a desk with books - Class II privileges
    for (cx, cz, f, w, nm) in ((776, -400, 'W', 560, 'netting E'), (516, -700, 'N', 500, 'netting S'), (516, -100, 'S', 500, 'netting N')):
        decal30(R, NET, cx, cz, f, w, 260, 180, nm)
    model30(R, 'dclass_bed.x', 715, 0, -580, 0, (100, 50, 200), 'R35 bed')
    desk(R, 620, -260, 760, -140, 0)
    solid(R, (620, 0, -260, 760, 76, -140), 'R35 desk')
    book(R, 680, 76, -200)
    book(R, 700, 82, -210)
    model30(R, 'scpcb_chair.x', 590, 0, -200, 270, (40, 104, 40), 'R35 chair')
    named(R, 'B35', 520, 20, -420)
    decal30(R, HUME, 192, -150, 'W', 80, 80, 200, 'hume display')
    named(R, 'HUME', 188, 200, -150)
    decal30(R, KEYPAD, 192, -640, 'W', 40, 60, 160, 'R35 intercom')
    named(R, 'INTERCOM', 188, 160, -640)
    ceil_light(R, 516, -400, 352, size=50, power=60, rng=640)
    # the thermal watch station: the screens on the far wall, consoles against the side walls, the camera's table
    decal30(R, THERM, 776, 400, 'W', 420, 210, 220, 'thermal screens')
    named(R, 'THERM', 770, 220, 400)
    console30(R, 560, 140, 'N', 'thermal console S')
    console30(R, 560, 660, 'S', 'thermal console N')
    table30(R, 400, 330, 540, 470, 'thermal table')
    item(R, 'thermal4427', 470, 78, 400)
    item(R, 'doc4427', 430, 78, 350)
    model30(R, 'scpcb_chair.x', 590, 0, 400, 270, (40, 104, 40), 'thermal chair')
    ceil_light(R, 516, 400, 352, size=44, power=50, rng=600, color=(255, 210, 180))
    # the wing security office
    office_desk(R, -700, -560, -580, -360, 'E', 'security desk', chair=(-545, -460))
    lockers(R, 'z', -700, +1, -540, -290)
    solid(R, (-540, 0, -700, -290, 300, -670), 'security lockers')
    decal30(R, WMON, -776, -200, 'E', 100, 100, 210, 'security monitor')
    item(R, 'key3', -640, 76, -400, chance=60)
    ceil_light(R, -516, -400, 352, size=44, power=55, rng=600)
    check(R)
    return (R, 'B4', 'Euclid-Level Containment Wing B4 (Heavy Containment): SCP-4427 cordoned off in the corridor (visible only on thermal), Room 35 (SCP-4427-B), the thermal watch station and the wing security office.',
            2, 0.45, ((0, 165, -650), (0, 200, 0)))


# ================================================================================================ SCP-3069
def room2b30ocean():
    R, rooms = wing('room2b30ocean', 'hcz', {('E', 0): {'depth': 600, 'h': 448, 'span': 700}, ('W', 0): {'span': 700}}, amb=8)
    hub_dress(R, 'hcz', [('E', 0, 'ocean'), ('W', 0, 'gamma6')])
    for z in (-560, -200, 200, 560):
        ceil_light(R, 0, z, 384, size=36, power=45, rng=600, color=(200, 230, 255))
    decal30(R, ATLANTIC, 192, -470, 'W', 240, 120, 210, 'hub sonar map')
    R.box(-40, 0, -700, 40, 2, 700, GRATE, lux=10)                                       # a drain grating down the middle
    # east: the specimen tank (x 600..856), the viewing platform with a rail, the Atlantic map, consoles
    for z in (-500, 500):
        sbox(R, 600, 0, min(z, z + (12 if z < 0 else -12)), 856, 448, max(z, z + (12 if z < 0 else -12)), PANELS, 'tank side %d' % z)
    sbox(R, 600, 0, -488, 612, 40, 488, PANELS, 'tank sill', top=CHECKER)
    R.decal((612, -488), (612, 488), 40, 420, GLASS, (0, 0, 4, 1), off=0.5)              # the tank's front glass
    R.collide_wall((612, -488), (612, 488), 0, 448)
    R.rect_floor(612, -488, 856, 488, 4, Mat('concretemoss.jpg', 256))
    R.rect_ceil(612, -488, 856, 488, 420, TANKW)                                         # the water surface from below
    for z in (-300, 0, 300):
        R.light(740, 380, z, rng=520, color=(80, 200, 220), power=60)
    named(R, 'SPEC', 740, 220, 0)
    sbox(R, 390, 0, -420, 580, 48, 420, CHECKER, 'viewing platform', skip='B')
    sbox(R, 368, 0, -150, 390, 24, 150, CHECKER, 'platform step', skip='B')
    for z in range(-410, 420, 82):
        R.tube((572, 48, z), (572, 150, z), 3, METAL, sides=6, caps=True)
    R.tube((572, 150, -410), (572, 150, 410), 3, METAL, sides=6, caps=True)
    decal30(R, ATLANTIC, 430, 700, 'S', 400, 200, 330, 'tank map')
    named(R, 'MAP', 430, 330, 690)
    console30(R, 420, 650, 'S', 'ocean console N')
    console30(R, 420, -650, 'N', 'ocean console S')
    named(R, 'CONSOLE', 420, 120, -620)
    ceil_light(R, 420, 0, 448, size=60, power=50, rng=700, color=(210, 230, 255))
    # west: MTF Gamma-6's equipment room - the SCP-3069-A replica, dive gear, oxygen, a workbench with the jar
    named(R, 'REPLICA', -516, 0, 150)
    sbox(R, -600, 0, 70, -432, 20, 230, CHECKER, 'replica plinth', skip='B')
    for z in (-250, -170, -90):
        R.tube((-756, 0, z), (-756, 170, z), 14, Mat('oxygen-cylinder.jpg', 128), sides=10, caps=True)
        solid(R, (-770, 0, z - 14, -742, 170, z + 14), 'oxygen %d' % z)
    for z in (-650, -560, -470):
        sbox(R, -776, 40, z - 30, -740, 220, z + 30, YEL, 'dive suit %d' % z)
        R.box(-762, 220, z - 14, -742, 250, z + 14, DARK, lux=10)
    table30(R, -560, -560, -380, -440, 'gamma bench')
    item(R, 'jar3069', -470, 78, -500)
    item(R, 'doc3069', -420, 78, -470)
    decal30(R, Mat('caution_tesla.jpg', cast=False), -776, 450, 'E', 140, 70, 230, 'gamma sign')
    ceil_light(R, -516, 0, 352, size=50, power=60, rng=680, color=(220, 236, 255))
    check(R)
    return (R, 'OCN', 'SCP-3069 deep monitoring (Heavy Containment): a specimen tank, the Atlantic map and a viewing platform; MTF Gamma-6\'s equipment room with the SCP-3069-A replica.',
            2, 0.55, ((0, 165, -650), (0, 150, 300)))


# ================================================================================================ Outposts 4433-A / 4434
def room2b30outpost():
    R, rooms = wing('room2b30outpost', 'lcz', {('E', 0): {'span': 700}, ('W', 0): {'span': 700}}, amb=10)
    hub_dress(R, 'lcz', [('E', 0, 'outposts'), ('W', 0, 'evidence')])
    for z in (-500, 0, 500):
        pendant(R, 0, z, 384, power=55, rng=600)
    decal30(R, FEEDS, 192, -480, 'W', 220, 110, 200, 'hub feeds')
    decal30(R, PR2, -192, -480, 'E', 100, 134, 200, 'hub poster')
    sbox(R, 150, 0, 420, 192, 160, 560, DARK, 'radio rack', top=CTRL)                     # a radio equipment rack
    # east: the surveillance control room (ref. 64): a wall of feeds, the console run, the desk with the phone
    decal30(R, FEEDS, 776, -100, 'W', 420, 210, 240, 'control feeds')
    named(R, 'FEEDS', 770, 240, -100)
    decal30(R, THERM, 776, 290, 'W', 180, 90, 250, 'control thermal')
    sbox(R, 700, 0, -320, 776, 90, 160, DARK, 'console run', skip='B', top=CTRL)
    named(R, 'RADIO', 740, 110, 60)
    office_desk(R, 420, -280, 560, -160, 'E', 'outpost desk', chair=(385, -220))
    item(R, 'phone4433', 520, 76, -180)
    item(R, 'doc4433', 470, 76, -260)
    cabinets(R, 280, 200, 340, 340, 'outpost cabinets')
    ceil_light(R, 516, 0, 352, size=44, power=50, rng=640)
    pendant(R, 490, -220, 352, drop=60, power=55, rng=480)
    # west: the SCP-4434 evidence room: the skull in a glass case, Figure A, the locator tray
    named(R, 'SKULL', -560, 110, -100)
    sbox(R, -660, 0, -200, -460, 100, 0, PANELS, 'display plinth', skip='B')
    for (a, b) in (((-660, -200), (-460, -200)), ((-460, 0), (-660, 0)), ((-460, -200), (-460, 0)), ((-660, 0), (-660, -200))):
        R.decal(a, b, 100, 250, GLASS, (0, 0, 1, 1), off=0.5)
    R.box(-664, 250, -204, -456, 256, 4, METAL, lux=10)
    solid(R, (-664, 100, -204, -456, 256, 4), 'display case')
    decal30(R, AD4434, -776, 220, 'E', 150, 200, 200, 'figure A')
    named(R, 'AD', -770, 200, 220)
    table30(R, -560, 300, -380, 420, 'evidence table')
    item(R, 'doc4434', -470, 78, 340)
    item(R, 'doc4434ad', -430, 78, 380)
    cabinets(R, -480, -290, -300, -260, 'evidence cabinets')
    ceil_light(R, -516, -100, 352, size=44, power=60, rng=600)
    ceil_light(R, -516, 300, 352, size=36, power=45, rng=520)
    check(R)
    return (R, 'OUT', 'Outposts 4433-A and 4434 remote surveillance (Entrance Zone): a wall of camera feeds and a desk with a phone that rings; the SCP-4434 evidence room with an SCP-4434-C skull.',
            3, 0.6, ((0, 165, -650), (0, 150, 300)))


# ================================================================================================ SCP-2648
def room2b30store():
    R, rooms = wing('room2b30store', 'store27', {('E', 0): {'depth': 600, 'h': 448, 'span': 700}, ('W', 0): {'span': 700}}, amb=10)
    hub_dress(R, 'store27', [('E', 0, 'scp2648'), ('W', 0, 'storage')])
    for z in (-560, 0, 560):
        pendant(R, 0, z, 384, power=55, rng=640)
    for (x, f) in ((192, 'W'), (-192, 'E')):                                              # roll-up shutters (ref. 65)
        for z in (-420, 420):
            decal30(R, SHUTTER, x, z, f, 200, 260, 130, 'shutter %d %d' % (x, z))
    for x in (-150, 150):
        R.box(x - 3, 0, -700, x + 3, 1, 700, Mat('indev_o_stripes.png', 64), lux=10)      # yellow lane lines
    # east: the shipping container, doors open, a gate of bars across the front; the amalgam inside
    cx0, cx1, cz0, cz1, ch = 430, 840, -260, 260, 420
    sbox(R, cx0, 0, cz0 - 12, cx1, ch, cz0, CONT, 'container side S')
    sbox(R, cx0, 0, cz1, cx1, ch, cz1 + 12, CONT, 'container side N')
    sbox(R, cx1, 0, cz0 - 12, cx1 + 12, ch, cz1 + 12, CONT, 'container back')
    R.box(cx0, ch, cz0 - 12, cx1 + 12, ch + 12, cz1 + 12, CONT, lux=10)
    R.rect_floor(cx0, cz0, cx1, cz1, 2, Mat('indev_o_mud.png', 128))
    for z in range(cz0 + 20, cz1, 40):                                                  # the bars
        R.tube((cx0 - 4, 0, z), (cx0 - 4, ch, z), 3, METAL, sides=6, caps=True)
    R.collide_wall((cx0 - 4, cz0), (cx0 - 4, cz1), 0, ch)
    R.collide_wall((cx0 - 4, cz1), (cx0 - 4, cz0), 0, ch)
    sbox(R, cx0 - 20, 0, cz0 - 200, cx0 - 8, ch, cz0 - 12, CONT, 'container door S')
    sbox(R, cx0 - 20, 0, cz1 + 12, cx0 - 8, ch, cz1 + 200, CONT, 'container door N')
    named(R, 'AMAL', 640, 0, 0)
    named(R, 'GATE', cx0 - 10, 150, 0)
    decal30(R, LAMBDA, 640, -700, 'N', 300, 150, 240, 'lambda board')
    named(R, 'LAMBDA', 640, 240, -690)
    R.box(380, 0, -300, 384, 1, 300, Mat('indev_o_stripes.png', 64), lux=10)             # the keep-back line
    ceil_light(R, 640, 0, 448, size=60, power=60, rng=760, color=(255, 240, 220))
    ceil_light(R, 330, -500, 448, size=40, power=50, rng=600)
    item(R, 'doc2648', 320, 0, -620)
    # west: general storage (ref. 60): the banner between two shelving units, the poster, benches, a camera
    shelf_unit(R, -776, -330, -716, -170, 'storage shelves S')
    shelf_unit(R, -776, 170, -716, 330, 'storage shelves N')
    decal30(R, BANNER, -776, 0, 'E', 300, 105, 230, 'storage banner')
    decal30(R, POSTER24, -516, -700, 'N', 80, 110, 210, 'storage poster')
    bench30(R, -620, -300, -420, -250, 'storage bench S')
    bench30(R, -620, 250, -420, 300, 'storage bench N')
    sbox(R, -776, 300, 380, -760, 330, 396, DARK, 'camera bracket')
    item(R, 'firstaid', -700, 10, -240, chance=60)
    ceil_light(R, -516, -150, 352, size=40, power=55, rng=600)
    ceil_light(R, -516, 150, 352, size=40, power=55, rng=600)
    check(R)
    return (R, 'STR', 'SCP-2648 container and general storage (Light Containment): the amalgam in its shipping container behind bars, MTF Lambda-14\'s readings; a storage room in the old style.',
            1, 0.6, ((0, 165, -650), (0, 150, 300)))


ALL = [room2b30admin, room2b30a4, room2b30b4, room2b30ocean, room2b30outpost, room2b30store]
