"""The thirty-fourth batch: four deep storage complexes for the hundred SCPs of data34.py. Code in IndevU34.bb; textures
from make_assets34.py, models from make_hd34.py. After the user's reference images 100-106:
  ref. 101/106  a mezzanine with a railing over a sunken storage floor, short stairs down, white walls under a riveted
                trim, a black ceiling, white tiles, a STORAGE AREA sign over the door
  ref. 100      the server room: machine cabinets under steel beams and dark red pendant lamps
  ref. 102/105  the control console with its scope; the HEAVY CONTAINMENT ZONE LOCKDOWN switch panel
  ref. 103/104  the dark surveillance office with its monitors; the Surveillance Room door with CAUTION and a keypad

Every room: a corridor (the hub) with two side rooms on the west (X1 at z -400, X2 at z +400) and on the east a door
to the STORAGE AREA: a mezzanine (y 0) and stairs down to the sunken floor (y -256), x 256..960, z -1000..1000, with
  11 alcoves along the east wall (cells with observation windows, tanks, record walls, display plinths, big objects),
  4 alcoves along the west wall below the mezzanine, and a centre row of glass display plinths and big objects.
Every unit gets a placard. Everything is checked: no solids overlap, nothing in a doorway or on the stairs."""
import math
from rooms_b33 import *
from rooms_b32 import rail_x, rail_z
from data34 import U, ROOMS

YL = -256.0
PLAC = Mat('indev_b34plac.png', cast=False)
SCR = Mat('indev_b34scr.png', cast=False)
WIN = Mat('indev_b34win.png', cast=False)
DOOR1619 = Mat('indev_b34door1619.png', cast=False)
SIGNS = Mat('indev_b34signs.png', cast=False)
LOCKP = Mat('indev_b34lock.png', cast=False)
CONSP = Mat('indev_b34console.png', cast=False)
SULF = Mat('indev_b34sulfur.png', cast=False)
WATER = Mat('indev_820water.png', 128, alpha=True, cast=False)
SAND = Mat('indev_o_mud.png', 128)
SCREENS = [u for u in U if u['unit'] == 'screen' and u['num'] != '1619']
MODEL_SIZE = {   # footprint x, height, footprint z (as it stands at yaw 0) of the runtime props
    'scp629': (60, 182, 48), 'scp5147': (150, 186, 90), 'scp1508': (112, 172, 100), 'scp1731': (84, 182, 80),
    'scp1970': (86, 112, 64), 'scp1445': (120, 88, 120), 'scp4566': (130, 98, 72), 'scp711': (44, 84, 76),
    'scp324': (76, 152, 76), 'scp1473': (58, 40, 50)}
OPT = {}          # batch 35 and later set this before calling storage_room(): materials, barred cells, hooks
CASE_MODELS = {'scp5199', 'scp2792', 'scp3016', 'scp2597', 'scp2414', 'scp1404'}


# ------------------------------------------------------------------------------------------------ small pieces
def unitpiv(R, u, p, m=None, yaw=0):
    """the interaction point p of unit u, and where its runtime model stands (m) with which yaw"""
    R.units.append((U.index(u), p, m, yaw))


def placard(R, u, cx, cz, facing, yc):
    i = U.index(u)
    u0, v0 = (i % 8) / 8.0, (i // 8) / 16.0
    decal30(R, PLAC, cx, cz, facing, 96, 48, yc, 'placard ' + u['num'], uv=(u0, v0, u0 + 1 / 8.0, v0 + 1 / 16.0))


def glass_box(R, x0, y0, z0, x1, y1, z1):
    for (a, b) in (((x0, z0), (x1, z0)), ((x1, z0), (x1, z1)), ((x1, z1), (x0, z1)), ((x0, z1), (x0, z0))):
        R.decal(b, a, y0, y1, GLASS, (0, 0, 1, 1), off=0.3)
        R.decal(a, b, y0, y1, GLASS, (0, 0, 1, 1), off=0.3)
    R.box(x0 - 2, y1, z0 - 2, x1 + 2, y1 + 3, z1 + 2, METAL, lux=10)


def content(R, num, x, y, z):
    """small things inside the glass of a display plinth (baked into the room)"""
    c = {'6482': 'jar', '1066': 'frame', '3634': 'tool', '4509': 'book', '1597': 'cloth', '1273': 'lamp', '2488': 'bottles',
         '4110-1': 'costume', '1667': 'shoes', '1626': 'cloth', '1534': 'boxes', '551': 'puzzle', '385': 'harness',
         '674': 'gun', '2137': 'disc', '5567': 'tape', '4828': 'book', '445-EX': 'paper', '726-EX': 'rod', '6976': 'heart',
         '1705': 'bones', '1036': 'figures'}.get(num, '')
    W = Mat('white.jpg', 64)
    if c == 'jar':
        R.prism(octo(x, z, 12, 10), y, y + 30, GLASS, caps='T')
        R.prism(octo(x, z, 11, 10), y, y + 14, Mat('concretefloor.jpg', 64), caps='T')
    elif c == 'frame':
        R.box(x - 26, y, z - 2, x + 26, y + 36, z + 2, WOOD, lux=10)
        R.box(x - 22, y + 4, z - 3, x + 22, y + 32, z - 2, W, lux=10)
    elif c in ('book', 'tape', 'disc'):
        h = {'book': 5, 'tape': 3, 'disc': 1.2}[c]
        R.box(x - 12, y, z - 16, x + 12, y + h, z + 16, DARK if c != 'disc' else METAL, lux=10)
    elif c == 'tool':
        R.tube((x - 12, y + 3, z), (x + 12, y + 3, z), 2, METAL, sides=6, caps=True)
        R.tube((x - 12, y + 3, z), (x - 12, y + 3, z + 10), 2.5, METAL, sides=6, caps=True)
    elif c == 'cloth':
        R.box(x - 26, y, z - 22, x + 26, y + 8, z + 22, Mat('indev_b33shade.png' if num == '1597' else 'concretefloor.jpg', 64), lux=10)
    elif c == 'lamp':
        R.prism(octo(x, z, 10, 8), y, y + 4, W, caps='T')
        R.prism(octo(x, z, 7, 8), y + 4, y + 22, W, caps='T')
        for e in (-1, 1):
            R.box(x + e * 4 - 1.5, y + 22, z - 1, x + e * 4 + 1.5, y + 36, z + 1, W, lux=10)
    elif c == 'bottles':
        for k in range(5):
            R.prism(octo(x - 24 + k * 12, z, 5, 8), y, y + 26, GLASS, caps='T')
    elif c == 'costume':
        R.box(x - 16, y, z - 6, x + 16, y + 44, z + 6, Mat('indev_120pink.png', 64), lux=10)
        R.prism(octo(x, z, 8, 8), y + 44, y + 58, Mat('indev_120pink.png', 64), caps='T')
    elif c == 'shoes':
        for k in range(3):
            R.box(x - 26 + k * 18, y, z - 10, x - 14 + k * 18, y + 9, z + 14, DARK, lux=10)
    elif c == 'boxes':
        for k in range(3):
            R.box(x - 28 + k * 20, y, z - 10, x - 12 + k * 20, y + 18 + k * 4, z + 10, Mat('wood.jpg', 64), lux=10)
    elif c == 'puzzle':
        R.box(x - 30, y, z - 22, x + 30, y + 1.5, z + 22, Mat('indev_b33colony.png', 64), lux=10)
    elif c == 'harness':
        R.box(x - 22, y, z - 8, x + 22, y + 10, z + 8, Mat('indev_867bark.png', 64), lux=10)
        R.box(x - 8, y + 10, z - 6, x + 8, y + 22, z + 6, YEL, lux=10)
    elif c == 'gun':
        R.box(x - 14, y, z - 3, x + 14, y + 6, z + 3, Mat('concretefloor.jpg', 32), lux=10)
        R.box(x - 14, y, z - 3, x - 6, y + 14, z + 3, DARK, lux=10)
    elif c == 'paper':
        for k in range(4):
            R.box(x - 24 + k * 12, y, z - 10, x - 14 + k * 12, y + 1, z + 10, Mat(('indev_120pink.png', 'white.jpg', 'indev_b33shade.png', 'concretefloor.jpg')[k], 32), lux=10)
    elif c == 'rod':
        R.tube((x - 30, y + 2, z - 6), (x + 6, y + 2, z), 1.5, Mat('indev_b33shade.png', 32), sides=6, caps=True)
        R.tube((x + 6, y + 2, z), (x + 30, y + 2, z - 10), 1.5, Mat('indev_b33shade.png', 32), sides=6, caps=True)
    elif c == 'heart':
        R.prism(octo(x, z, 10, 10), y, y + 22, WOOD, caps='T')
    elif c == 'bones':
        for k in range(6):
            R.tube((x - 24 + k * 8, y + 2, z - 14), (x - 20 + k * 8, y + 2, z + 14), 2, Mat('white.jpg', 32), sides=6, caps=True)
    elif c == 'figures':
        for k in range(4):
            R.prism(octo(x - 24 + k * 16, z, 5, 6), y, y + 30, Mat('indev_867bark.png', 32), caps='T')


# ------------------------------------------------------------------------------------------------ the units
def alcove_unit(R, u, side, zc, B):
    """one alcove: E side x 830..960 (open face x = 830, facing west), W side x 256..386 (open face 386, facing east)"""
    s = -1 if side == 'E' else 1                      # the direction the alcove faces
    xo = 830.0 if side == 'E' else 386.0              # the open face
    xb = 960.0 if side == 'E' else 256.0              # the back wall
    facing = 'W' if side == 'E' else 'E'
    yaw = -90 if side == 'E' else 90
    xm = (xo + xb) / 2
    z0, z1 = zc - 80, zc + 80
    kind = u['unit']
    num = u['num']
    front = (xo + s * 30, YL + 150, zc)               # where you stand to use it
    if kind == 'cell' and OPT.get('cellbars'):         # ref. 108: a barred front - the occupant visible inside
        for zz in range(int(z0) + 8, int(z1), 14):
            R.tube((xo, YL, zz), (xo, YL + 300, zz), 2.2, METAL, sides=6, caps=False)
        for yy in (YL + 2, YL + 150, YL + 296):
            R.box(min(xo, xo - s * 6), yy - 2, z0, max(xo, xo - s * 6), yy + 4, z1, METAL, lux=10)
        R.collide_wall((xo, z0), (xo, z1), YL, YL + 300)
        R.collide_wall((xo, z1), (xo, z0), YL, YL + 300)
        lo, hi = sorted((xo, xb))
        solid(R, (lo, YL, z0, hi, YL + 300, z1), 'barred cell %s' % num)
        w = {'1976': 3, '1702': 4}.get(num, (U.index(u) * 7) % 3)
        decal30(R, WIN, xb, zc, facing, 110, 150, YL + 120, 'occupant %s' % num, uv=(w / 5.0, 0, (w + 1) / 5.0, 1))
        a, b = sorted((xb, xb + s * 60))
        R.box(a, YL, zc - 70, b, YL + 40, zc - 10, Mat('white.jpg', 64), lux=10)       # the bunk
        decal30(R, PLAC, xo, zc, facing, 96, 48, YL + 236, 'placard %s' % num, uv=plac_uv(u))
        unitpiv(R, u, (xo, YL + 160, zc))
        return
    if kind == 'cell':                                # a steel front, an observation window, an intercom
        xa, xc = sorted((xo, xo - s * 16))
        sbox(R, xa, YL, z0, xc, YL + 300, z1, Mat('dirtymetal.jpg', 128), 'cell front %s' % num)
        w = {'1976': 3, '1702': 4}.get(num, (U.index(u) * 7) % 3)
        decal30(R, WIN, xo, zc, facing, 100, 100, YL + 175, 'window %s' % num, uv=(w / 5.0, 0, (w + 1) / 5.0, 1))
        decal30(R, KEYPAD, xo, zc + 64 * (1 if side == 'E' else -1), facing, 20, 30, YL + 140, 'intercom %s' % num)
        placard(R, u, xo, zc, facing, YL + 82)
        unitpiv(R, u, (xo, YL + 160, zc))
        if num == '1913':
            R.rect_floor(min(xo, xo - s * 80), z0 + 30, max(xo, xo - s * 80), z1 - 30, YL + 1, SULF)
        if num == '3356':
            R.box(min(xo, xo - s * 2), YL + 110, zc - 50, max(xo, xo - s * 2), YL + 240, zc + 50, Mat('indev_o_rust.png', 64), lux=10)
        return
    if kind == 'tank':                                # a glass tank filling the alcove
        xa, xc = sorted((xo, xb))
        sbox(R, xa, YL, z0, xc, YL + 40, z1, PANELS, 'tank sill %s' % num, top=SAND)
        R.decal((xo, z1 if side == 'E' else z0), (xo, z0 if side == 'E' else z1), YL + 40, YL + 290, GLASS, (0, 0, 2, 1), off=-s * 0.5)
        R.collide_wall((xo, z0), (xo, z1), YL + 40, YL + 300)
        R.collide_wall((xo, z1), (xo, z0), YL + 40, YL + 300)
        R.rect_ceil(xa, z0, xc, z1, YL + 260, WATER)
        R.light(xm, YL + 230, zc, rng=260, color=(90, 200, 230), power=30)
        solid(R, (xa, YL + 40, z0, xc, YL + 300, z1), 'tank %s' % num)
        R.box(xa, YL + 290, z0, xc, YL + 300, z1, METAL, lux=10)
        placard(R, u, xo, zc, facing, YL + 20)
        unitpiv(R, u, (xo, YL + 140, zc), (xm, YL + 40, zc) if u['model'] else None, yaw)
        if not u['model']:                            # what lives in the tank
            for k in range(5):
                R.prism(octo(xm + ((k * 23) % 50 - 25), zc - 50 + k * 25, 6 + k % 3 * 2, 6), YL + 40, YL + 48 + (k % 3) * 8,
                        Mat({'2608': 'grating.jpg', '525': 'indev_867bark.png', '3023-B': 'wood.jpg', '7925': 'white.jpg',
                             '1902': 'concretefloor.jpg', '1908': 'white.jpg'}.get(num, 'white.jpg'), 32), caps='T')
        return
    if kind == 'screen':                              # a record wall: the screen or photograph on the back wall
        if num == '1619':
            decal30(R, DOOR1619, xb, zc, facing, 110, 220, YL + 115, 'door drawing 1619')
        else:
            i = SCREENS.index(u)
            u0, v0 = (i % 4) / 4.0, (i // 4) / 8.0
            decal30(R, SCR, xb, zc, facing, 150, 75, YL + 170, 'record %s' % num, uv=(u0, v0, u0 + 0.25, v0 + 0.125))
        lo, hi = sorted((xo, xo - s * 10))
        sbox(R, lo, YL, z0 + 20, hi, YL + 90, z1 - 20, YEL, 'record rail %s' % num)
        placard(R, u, xb, zc, facing, YL + (262 if num == '1619' else 60))
        unitpiv(R, u, (xb, YL + 160, zc))
        return
    if kind == 'floor':                               # a big object standing in the open alcove behind a yellow line
        sx, sy, sz = MODEL_SIZE[u['model']]
        lo, hi = sorted((xm - sz / 2, xm + sz / 2))     # (turned 90 degrees: z size across x)
        solid(R, (lo, YL, zc - sx / 2, hi, YL + sy, zc + sx / 2), u['model'])
        a, b = sorted((xo, xo - s * 6))
        R.box(a, YL, z0, b, YL + 1, z1, Mat('indev_o_stripes.png', 64), lux=10)
        placard(R, u, xb, zc, facing, YL + 230)
        unitpiv(R, u, (xm, YL + sy * 0.6, zc), (xm, YL, zc), yaw)
        return
    # 'case' / 'item': a waist-high plinth with a glass hood (or an open top with the item on it)
    center_case(R, u, xm, zc, yaw, facing_wall=(xb, facing))


def center_case(R, u, x, z, yaw, facing_wall=None, y=YL):
    num = u['num']
    sbox(R, x - 46, y, z - 46, x + 46, y + 100, z + 46, PANELS, 'plinth %s' % num, skip='B', top=CHECKER)
    if u['unit'] == 'item':
        item(R, u['item'], x, y + 100, z)
        unitpiv(R, u, (x, y + 110, z))
    else:
        glass_box(R, x - 40, y + 100, z - 40, x + 40, y + 180, z + 40)
        solid(R, (x - 42, y + 100, z - 42, x + 42, y + 183, z + 42), 'hood %s' % num)
        if u['model'] in CASE_MODELS:
            unitpiv(R, u, (x, y + 140, z), (x, y + 100, z), yaw)
        else:
            content(R, num, x, y + 100, z)
            unitpiv(R, u, (x, y + 140, z))
            if num == '1273':
                R.light(x, y + 130, z, rng=180, color=(255, 230, 160), power=15)
    if facing_wall:
        placard(R, u, facing_wall[0], z, facing_wall[1], y + 230)
    else:                                            # a placard on a little stand in front (west)
        R.box(x - 50, y, z - 2, x - 48, y + 60, z + 2, METAL, lux=10)
        R.decal((x - 51, z + 24), (x - 51, z - 24), y + 60, y + 84, PLAC, plac_uv(u), off=0.2)
        R.decal((x - 47, z - 24), (x - 47, z + 24), y + 60, y + 84, PLAC, plac_uv(u), off=0.2)


def plac_uv(u):
    i = U.index(u)
    u0, v0 = (i % 8) / 8.0, (i // 8) / 16.0
    return (u0, v0, u0 + 1 / 8.0, v0 + 1 / 16.0)


def center_floor(R, u, x, z, yaw=-90):
    """a big object standing on the storage floor in the centre row, with its placard on a stand"""
    m = u['model']
    if m in OPT.get('floor', {}):
        OPT['floor'][m](R, u, x, z)
    elif m == 'scp1969':                               # the disco ball over a round stage
        R.prism(octo(x, z, 70, 16), YL, YL + 10, CHECKER, caps='T')
        solid(R, (x - 70, YL, z - 70, x + 70, YL + 10, z + 70), 'stage 1969')
        unitpiv(R, u, (x, YL + 250, z), (x, YL + 230, z), 0)
        R.tube((x, YL + 300, z), (x, 352, z), 1.2, METAL, sides=4, caps=False)
    elif m == 'scp1564':                             # three of the six brass eggs in a steel cradle
        sbox(R, x - 50, YL, z - 150, x + 50, YL + 16, z + 150, Mat('dirtymetal.jpg', 128), 'egg cradle')
        unitpiv(R, u, (x, YL + 90, z), [(x, YL + 16, z + k * 96) for k in (-1, 0, 1)], 0)
        solid(R, (x - 40, YL + 16, z - 140, x + 40, YL + 160, z + 140), 'eggs 1564')
    elif m == 'scp1575':                             # the Venus fountain
        solid(R, (x - 90, YL, z - 90, x + 90, YL + 290, z + 90), 'Venus 1575')
        unitpiv(R, u, (x, YL + 70, z - 90), (x, YL, z), 0)
    elif m == 'scp3085':                             # the sphere: a white ring on the floor, the sphere floating
        R.prism(octo(x, z, 110, 20), YL, YL + 2, Mat('white.jpg', 64), caps='T')
        sbox(R, x - 60, YL, z - 60, x + 60, YL + 40, z + 60, Mat('white.jpg', 64), 'sphere plinth', skip='B')
        unitpiv(R, u, (x, YL + 150, z), (x, YL + 150, z), 0)
        solid(R, (x - 90, YL + 60, z - 90, x + 90, YL + 240, z + 90), 'sphere 3085')
        R.light(x, YL + 300, z, rng=420, color=(255, 255, 255), power=60)
    elif m == 'scp1807':                             # the okapi on a steel table
        sbox(R, x - 60, YL, z - 120, x + 60, YL + 80, z + 120, Mat('dirtymetal.jpg', 128), 'okapi table')
        solid(R, (x - 50, YL + 80, z - 110, x + 50, YL + 140, z + 110), 'okapi')
        unitpiv(R, u, (x, YL + 110, z), (x, YL + 80, z), -90)
    elif m == 'scp5147':                             # three mannequins on a low stage
        sbox(R, x - 75, YL, z - 75, x + 75, YL + 10, z + 75, WOOD, 'troupe stage')
        solid(R, (x - 60, YL + 10, z - 60, x + 60, YL + 196, z + 60), 'troupe')
        unitpiv(R, u, (x, YL + 120, z), (x, YL + 10, z), -90)
    else:
        sx, sy, sz = MODEL_SIZE[m]
        solid(R, (x - sz / 2, YL, z - sx / 2, x + sz / 2, YL + sy, z + sx / 2), m)
        unitpiv(R, u, (x, YL + sy * 0.6, z), (x, YL, z), yaw)
    R.box(x - 124, YL, z - 2, x - 120, YL + 60, z + 2, METAL, lux=10)            # the placard stand, west of it
    R.decal((x - 125, z + 24), (x - 125, z - 24), YL + 60, YL + 84, PLAC, plac_uv(u), off=0.2)
    R.decal((x - 119, z - 24), (x - 119, z + 24), YL + 60, YL + 84, PLAC, plac_uv(u), off=0.2)
    solid(R, (x - 126, YL, z - 3, x - 118, YL + 86, z + 3), 'stand %s' % u['num'])


# ------------------------------------------------------------------------------------------------ the room
def storage_room(key, style, x1style, x2style, amb=9):
    name = ROOMS[key]
    units = [u for u in U if u['room'] == key]
    R, rooms = wing33(name, style, {('W', -400): {'style': x1style}, ('W', 400): {'style': x2style}}, extra=[('E', 0)], amb=amb)
    R.units = []
    B = R.book
    hub_dress(R, style, [], pipes=False)
    k = 'ABCD'.index(key) if key in 'ABCD' else OPT.get('signk', 0)
    u0, v0 = (k % 2) * 0.5, (k // 2) * 0.25                                     # STORAGE AREA 06..09 over the door
    decal30(R, SIGNS, 192, 0, 'W', 150, 37, 350, 'storage sign', uv=(u0, v0, u0 + 0.5, v0 + 0.25))
    for z in (-560, -180, 180, 560):
        red_pendant(R, 0, z, 384)
    # the door, the jamb
    hall(R, 192, -96, 256, 96, 0, 320, wmat(style, 320), STYLES[style][1], DARK, holes={'W': [(-96, 96, 0, 320)], 'E': [(-96, 96, 0, 320)]})
    R.spawns.append(dict(kind='door', pos=(224, 0, 0), angle=90, key={'A': 3, 'B': 2, 'C': 3, 'D': 4}.get(key, OPT.get('doorkey', 3))))
    # ---------------- the storage hall (ref. 101 / 106)
    hall(R, 256, -1000, 960, 1000, YL, 352 - YL, OPT.get('wall', WALL96.but(vs=352 - YL, v0=352 - YL)), OPT.get('floormat', TILE96),
         OPT.get('ceil', DARK), holes={'W': [(-96, 96, 0, 320)]})
    B.areas.append((256, 960, -1000, 1000, 352, YL))
    sbox(R, 256, -16, -200, 440, 0, 200, CHECKER, 'mezzanine', skip='')
    rail_z(R, 436, -196, 196, 0, 'mezzanine rail E')
    rail_x(R, -196, 260, 426, 0, 'mezzanine rail S')
    rail_x(R, 204, 412, 432, 0, 'mezzanine rail N')
    for i in range(14):                                                         # the stairs down (ref. 106)
        za, zb = 200 + 32 * i, 232 + 32 * i
        top = -256.0 * (i + 1) / 14
        sbox(R, 256, max(top - 22, YL), za, 400, top, zb, CHECKER, 'step %d' % i)
    R.tube((404, 82, 200), (404, YL + 100, 648), 3.5, YEL, sides=6, caps=True)
    for i in range(0, 15, 4):
        y = -256.0 * i / 14
        R.tube((404, y, 200 + 32 * i), (404, y + 100, 200 + 32 * i), 3, YEL, sides=6, caps=True)
    solid(R, (400, YL, 200, 408, 104, 648), 'stair rail')
    B.clear = [((268, 0, -190, 424, 200, 190), 'mezzanine walk'), ((270, YL + 30, 660, 390, YL + 200, 760), 'stair foot'),
               ((712, YL, -990, 820, YL + 200, 990), 'east aisle'), ((400, YL, -990, 490, YL + 200, -460), 'west aisle S')]
    for z in ((-800, -400, 400, 800) if OPT.get('beams', True) else ()):         # steel beams (ref. 100 / 101)
        R.box(256, 300, z - 14, 960, 330, z + 14, Mat('dirtymetal.jpg', 128), lux=10)
        solid(R, (256, 300, z - 14, 960, 330, z + 14), 'beam %d' % z)
    for z in (-600, -200, 200, 600):
        red_pendant(R, 620, z, 352, drop=70, power=42, rng=640)
        R.light(910, YL + 260, z, rng=500, color=(255, 236, 210), power=40)
    for z in (-900, 900):
        ceil_light(R, 620, z, 352, size=40, power=32, rng=560)
    decal30(R, SIGNS, 960, 0, 'W', 220, 55, 260, 'hall sign', uv=(u0, v0, u0 + 0.5, v0 + 0.25))
    R.light(330, 200, 0, rng=500, color=(255, 236, 210), power=45)
    # the atmosphere pass (batch 36): red emergency lamps, grime at the foot of the end walls, darker corners
    from rooms_b36 import red_emergency, GRIME
    for (x, z, f) in ((620, -1000, 'N'), (620, 1000, 'S'), (256, 860, 'E')):
        red_emergency(R, x, YL + 240, z, f, 'red hall %d' % z, power=24, rng=380)
    for (a, b) in (((960, -1000), (256, -1000)), ((256, -1000), (960, -1000)), ((256, 1000), (960, 1000)), ((960, 1000), (256, 1000))):
        R.decal(a, b, YL, YL + 120, GRIME, (0, 0, 3, 1), off=0.6)
    if OPT.get('decorate'):
        OPT['decorate'](R)
    # ---------------- the units
    E = [u for u in units if u['slot'] == 'E']
    for i, u in enumerate(E):
        alcove_unit(R, u, 'E', -900 + 180 * i, B)
    for i in range(len(E), 11):                                                 # empty alcoves: a shelf of boxes
        zc = -900 + 180 * i
        shelf_unit33(R, 880, zc - 60, 950, zc + 60, 'spare shelf %d' % i)
    for i, zc in enumerate((-900, -720, -540, -360)):
        Wl = [u for u in units if u['slot'] == 'W']
        if i < len(Wl):
            alcove_unit(R, Wl[i], 'W', zc, B)
    for i in range(11):                                                         # partitions between the east alcoves
        zp = -900 + 180 * i + 80
        if i < 10:
            sbox(R, 830, YL, zp, 960, 300, zp + 20, OPT.get('part', WALL96).but(us=128, vs=556, v0=556), 'partition E %d' % i)
    for zp in (-820, -640, -460):
        sbox(R, 256, YL, zp, 386, YL + 300, zp + 20, OPT.get('part', WALL96).but(us=128, vs=556, v0=556), 'partition W %d' % zp)
    sbox(R, 256, YL, -280, 386, -16, -260, OPT.get('part', WALL96).but(us=128, vs=240, v0=240), 'partition W end')
    C = [u for u in units if u['slot'] == 'C']
    cpos = CENTER.get(key)
    for i, u in enumerate(C):
        z = cpos[u['num']] if isinstance(cpos, dict) else cpos[i][0]
        if u['unit'] == 'floor':
            center_floor(R, u, 620, z)
        else:
            center_case(R, u, 620, z, -90)
    # ---------------- the side rooms
    SIDE[key](R, [u for u in units if u['slot'] == 'X1'], [u for u in units if u['slot'] == 'X2'])
    if OPT.get('docs'):
        OPT['docs'](R, key)
    else:
        from make_docs34 import AREA, PAGES
        for p in range(len(PAGES[key])):                                        # the registry, on the mezzanine
            item(R, 'docarea%sp%d' % (AREA[key][0], p + 1), 300 + (p % 2) * 70, 0, -160 + (p // 2) * 70)
    check33(R)
    R.units33 = R.units
    return R


def shelf_unit33(R, x0, z0, x1, z1, name):
    """a spare alcove: a tall steel storage cabinet"""
    sbox(R, x0, YL, z0, x1, YL + 220, z1, CABTEX, name, skip='B')


CENTER = {   # the centre row: (z, -) per unit, in order
    'A': [(-900, 0), (-700, 0), (-500, 0), (-300, 0), (-100, 0), (100, 0), (300, 0), (500, 0), (700, 0), (900, 0)],
    'B': [(-900, 0), (-700, 0), (-500, 0), (-300, 0), (-100, 0), (100, 0), (300, 0), (500, 0), (700, 0), (900, 0)],
    'C': {'1807': 400, '1564': -760, '1575': -380, '3085': 20, '1255': 640, '4193': 780, '5604': 920, '2983': 200},
    'D': []}


# ------------------------------------------------------------------------------------------------ side rooms
def side_A(R, X1, X2):
    # X1: the surveillance room (ref. 103 / 104): monitors, two desks, the records of 2884-2, 1374, 5002
    decal30(R, SIGNS, -192, -130, 'E', 150, 75, 260, 'surveillance sign', uv=(0, 0.5, 0.5, 1.0))
    office_desk(R, -700, -660, -580, -540, 'W', 'surveillance desk 1', chair=(-545, -600))
    office_desk(R, -700, -260, -580, -140, 'W', 'surveillance desk 2', chair=(-545, -200))
    for k, u in enumerate(X1):
        zc = (-560, -400, -240)[k]
        i = SCREENS.index(u)
        uu, vv = (i % 4) / 4.0, (i // 4) / 8.0
        decal30(R, SCR, -776, zc, 'E', 150, 75, 230, 'record %s' % u['num'], uv=(uu, vv, uu + 0.25, vv + 0.125))
        placard(R, u, -776, zc, 'E', 160)
        unitpiv(R, u, (-770, 220, zc))
    decal30(R, WMON, -516, -700, 'N', 100, 100, 220, 'surveillance monitor S')
    decal30(R, WMON, -516, -100, 'S', 100, 100, 220, 'surveillance monitor N')
    ceil_light(R, -516, -400, 352, size=36, power=30, rng=520, color=(200, 220, 255))
    # X2: the HCZ lockdown control (ref. 105, 102): the switch panel, the console, 579, the tablets
    decal30(R, LOCKP, -776, 400, 'E', 200, 200, 190, 'lockdown panel')
    named(R, 'LOCKDOWN', -770, 190, 400)
    sbox(R, -776, 0, 140, -680, 96, 330, Mat('dirtymetal.jpg', 128), 'control desk', top=CONSP)
    model30(R, 'officeseat_a.x', -640, 0, 235, 270, (50, 100, 50), 'control chair')
    for u in X2:
        if u['unit'] == 'screen':
            i = SCREENS.index(u)
            uu, vv = (i % 4) / 4.0, (i // 4) / 8.0
            decal30(R, SCR, -516, 700, 'S', 180, 90, 220, 'record 579', uv=(uu, vv, uu + 0.25, vv + 0.125))
            placard(R, u, -516, 700, 'S', 140)
            unitpiv(R, u, (-516, 200, 690))
        else:
            table30(R, -480, 140, -340, 230, 'tablet table')
            item(R, u['item'], -410, 78, 185)
            placard(R, u, -516, 100, 'N', 160)
            unitpiv(R, u, (-410, 90, 185))
    ceil_light(R, -516, 400, 352, size=44, power=50, rng=600)


def side_B(R, X1, X2):
    # X1: Storage Area 06's office (ref. 106): the printer on its table, the photocopier, a desk
    table30(R, -700, -660, -560, -560, 'printer table')
    for u in X1:
        if u['model'] == 'scp1473':
            unitpiv(R, u, (-630, 110, -610), (-630, 78, -610), 90)
            solid(R, (-655, 78, -640, -605, 118, -580), 'LaserJet')
            placard(R, u, -776, -610, 'E', 200)
        else:
            unitpiv(R, u, (-700, 80, -240), (-700, 0, -240), 90)
            solid(R, (-740, 0, -305, -660, 98, -175), 'photocopier')
            placard(R, u, -776, -240, 'E', 200)
    office_desk(R, -510, -560, -390, -460, 'S', 'storage office desk', chair=(-450, -415))
    cabinets(R, -560, -140, -380, -100, 'storage office cabinets')
    ceil_light(R, -516, -400, 352, size=44, power=50, rng=600)
    # X2: the anomalous stationery room: three items on a long table, shelving
    table30(R, -700, 300, -380, 400, 'stationery table')
    for k, u in enumerate(X2):
        x = -650 + k * 110
        item(R, u['item'], x, 78, 350)
        unitpiv(R, u, (x, 90, 350))
        placard(R, u, x, 700, 'S', 180)
    shelf_unit(R, -776, 120, -716, 260, 'stationery shelves')
    ceil_light(R, -516, 400, 352, size=44, power=50, rng=600)


def side_C(R, X1, X2):
    # X1: the server room (ref. 100): two rows of machine cabinets, beams, red pendants, 5275 / 2999
    decal30(R, SIGNS, -192, -130, 'E', 150, 75, 260, 'server sign', uv=(0.5, 0.5, 1.0, 1.0))
    for x in (-700, -560):
        for z in (-640, -520):
            sbox(R, x - 40, 0, z - 50, x + 40, 210, z + 50, Mat('dirtymetal.jpg', 128), 'cabinet %d %d' % (x, z), top=CTRL)
            decal30(R, CTRL, x + 40 if x > -650 else x + 40, z, 'E', 70, 120, 120, 'cabinet panel %d %d' % (x, z))
    for z in (-560, -240):
        R.box(-776, 300, z - 12, -256, 324, z + 12, Mat('dirtymetal.jpg', 128), lux=10)
        solid(R, (-776, 300, z - 12, -256, 324, z + 12), 'server beam %d' % z)
    red_pendant(R, -516, -400, 352, drop=70, power=55, rng=620)
    for k, u in enumerate(X1):
        x = (-640, -420)[k]
        i = SCREENS.index(u)
        uu, vv = (i % 4) / 4.0, (i // 4) / 8.0
        decal30(R, SCR, x, -100, 'S', 180, 90, 210, 'record %s' % u['num'], uv=(uu, vv, uu + 0.25, vv + 0.125))
        placard(R, u, x, -100, 'S', 130)
        unitpiv(R, u, (x, 200, -110))
    # X2: the lab: the camera on the bench, the photo board of 1897-1
    table30(R, -700, 300, -560, 500, 'lab bench')
    for u in X2:
        if u['unit'] == 'item':
            item(R, u['item'], -630, 78, 400)
            unitpiv(R, u, (-630, 90, 400))
            placard(R, u, -776, 400, 'E', 200)
        else:
            i = SCREENS.index(u)
            uu, vv = (i % 4) / 4.0, (i // 4) / 8.0
            decal30(R, SCR, -516, 700, 'S', 220, 110, 210, 'record %s' % u['num'], uv=(uu, vv, uu + 0.25, vv + 0.125))
            placard(R, u, -330, 700, 'S', 210)
            unitpiv(R, u, (-516, 200, 690))
    bench30(R, -480, 120, -300, 170, 'lab bench 2')
    ceil_light(R, -516, 400, 352, size=44, power=55, rng=600)


def side_D(R, X1, X2):
    # X1: the control room (ref. 102): the console, its chair, the scope
    sbox(R, -776, 0, -560, -660, 110, -240, Mat('dirtymetal.jpg', 128), 'control console', top=CONSP)
    decal30(R, CONSP, -776, -400, 'E', 240, 120, 210, 'console back panel')
    named(R, 'CONSOLE', -700, 130, -400)
    model30(R, 'officeseat_a.x', -610, 0, -400, 270, (50, 100, 50), 'console chair')
    decal30(R, LOCKP, -516, -700, 'N', 150, 150, 200, 'door control panel')
    ceil_light(R, -516, -400, 352, size=40, power=40, rng=560, color=(220, 230, 255))
    # X2: the records office (ref. 103): a dark office, monitors over the desk, filing cabinets
    office_desk(R, -700, 300, -580, 500, 'E', 'records desk', chair=(-740, 400))
    decal30(R, WMON, -516, 700, 'S', 110, 110, 230, 'records monitor 1')
    decal30(R, WMON, -380, 700, 'S', 90, 90, 230, 'records monitor 2')
    cabinets(R, -500, 120, -300, 160, 'records cabinets')
    item(R, 'key4', -640, 76, 340, chance=40)
    ceil_light(R, -516, 400, 352, size=36, power=30, rng=480)
    # the centre of the storage floor: record desks instead of plinths
    for z in (-700, -300, 300, 700):
        sbox(R, 560, YL, z - 60, 680, YL + 76, z + 60, WOOD, 'record table %d' % z, skip='B')
        cabinets_low(R, 560, z + 80, 680, z + 120, 'record cabinets %d' % z)


def cabinets_low(R, x0, z0, x1, z1, name):
    sbox(R, x0, YL, z0, x1, YL + 140, z1, CABTEX, name, skip='B')


SIDE = {'A': side_A, 'B': side_B, 'C': side_C, 'D': side_D}


def room2b34humanoid():
    R = storage_room('A', 'ref99', 'cell30', 'cell30', amb=8)
    return (R, 'HUM', 'Deep Storage Area 06 (Heavy Containment): humanoid SCPs in cells along a sunken storage floor; the surveillance room and the lockdown control.',
            2, 0.4, ((0, 165, -650), (0, 150, 300)))


def room2b34objects():
    R = storage_room('B', 'ref96', 'ez', 'store27', amb=10)
    return (R, 'OBJ', 'Deep Storage Area 07 (Light Containment): anomalous objects on display plinths and in alcoves on a sunken storage floor; the printing office and the stationery room.',
            1, 0.4, ((0, 165, -650), (0, 150, 300)))


def room2b34bio():
    R = storage_room('C', 'hcz', 'cell30', 'cell30', amb=8)
    return (R, 'BIO', 'Deep Storage Area 08 (Heavy Containment): biological SCPs in tanks and pens, the brass ovoids, the Venus fountain and the grey sphere; the server room and the lab.',
            2, 0.6, ((0, 165, -650), (0, 150, 300)))


def room2b34site45():
    R = storage_room('D', 'bulk33', 'ez', 'ez', amb=8)
    return (R, 'S45', 'Deep Storage Area 09 (Entrance Zone): the Site-45 records, SCP-1619\'s drawn door, and the cells of SCP-3811, -4477, -5151, -5424 and -5534; the control room and the records office.',
            3, 0.6, ((0, 165, -650), (0, 150, 300)))


ALL = [room2b34humanoid, room2b34objects, room2b34bio, room2b34site45]
