"""Ten rooms for ten SCPs (the seventh batch, code in IndevS10.bb).

  room2subway052  HCZ    59th St. platform, down a lift (after the reference photo of the R4 car):
                         SCP-052 pulls in at its hour, opens its doors, and leaves - with you or without you
  room2hall99     LCZ    Hallway 99 (a second remake of the reference corridor): kennels both sides,
                         SCP-953's cell at the end, standing open
  room2gameshow   Indev  Sound Stage 024 and the observation lab above it (lift up): SCP-024
  room2diner      EZ     Freddy's Diner, SCP-4258: the windows look out on other places
  room2sheet      HCZ    Humanoid Chamber 6096 (a hotel room in all but name) and Holding 6096-B
  room2block15    HCZ    Cell Block 15, vaulted, 1840s: Cell 667 is SCP-2701
  room2mailbox    Indev  Property 1269: a street, a lawn, a house, and SCP-1269 at the curb
  room2psych      LCZ    Psychiatric Observation and Containment Locker 482
  room2realchar   Indev  Real Characters Industries: the studio, and a lift down to LG-1 (SCP-3325)
  room2wait1440   HCZ    Interview Room 142 and its observation room: SCP-1440

Same conventions as rooms_b6.py: named() / ndoor() / reserve() / lever() hand things to the code,
gen_b7.py turns them into r\\Objects[] / r\\RoomDoors[] slots and S10_* constants."""
from rooms_b6 import *

L5 = json.load(open(os.path.join(HERE, 'labels5.json')))
DP5 = json.load(open(os.path.join(HERE, 'doorplates5.json')))
P5 = json.load(open(os.path.join(HERE, 'plates5.json')))
PR5 = json.load(open(os.path.join(HERE, 'props5.json')))
N5 = json.load(open(os.path.join(HERE, 'neon5.json')))
LAB5 = Mat('indev_labels5.png', cast=False)
DPL5 = Mat('indev_doorplates5.png', cast=False)
PLT5 = Mat('indev_plates5.png', cast=False)
PROPS5 = Mat('indev_props5.png', cast=False)
NEON5 = Mat('indev_neon5.png', emit=215, cast=False)
D = DEEP
TILEW = Mat('indev_subtile.png', 512, 520, D + 520)
BALLAST = Mat('indev_ballast.png', 256)
EDGE = Mat('indev_edge.png', 40, cast=False)
GREENP = Mat('indev_greenpaint.png', 128)
STAGEF = Mat('indev_stagefloor.png', 256)
CURT = Mat('indev_curtain.png', 256, 960, 960)
GSTILE = Mat('indev_gstile.png', cast=False)
BLEACH = Mat('indev_bleach.png', 128)
DFLOOR = Mat('indev_dinerfloor.png', 128)
DWALL = Mat('indev_dinerwall.png', 256, 352, 352)
CHROME = Mat('indev_chrome.png', 64)
CARPET = Mat('indev_carpet.png', 256)
HWALL = Mat('indev_hotelwall.png', 192)
PLASTER = Mat('indev_plaster.png', 512, 520, 520)
LAWN = Mat('indev_lawn.png', 128)
SIDING = Mat('indev_siding.png', 128)
ASPHALT = Mat('indev_asphalt.png', 256)
PADDED = Mat('indev_padded.png', 128)
LINO = Mat('indev_lino.png', 128)
FLUID = Mat('indev_fluid.png', 128, alpha=True, cast=False)
BACKDROP = Mat('indev_backdrop.png', cast=False)
OLDWOOD = Mat('indev_oldwood.png', 128)
STRAW = Mat('indev_straw.png', 128, cast=False)
SHOWERC = Mat('indev_curtain2.png', 128)
FUTON = Mat('indev_futon.png', 96)
VIEW0 = Mat('indev_view0.png', emit=170, cast=False)
CLAWS = Mat('indev_claws.png', alpha=True, cast=False)
LABW = Mat('lab_tile_wall_1789291261627.jpg', 512, 420, D + 420)
STYLES['block'] = (PLASTER, CONC, DARK)
STYLES['cell'] = (PLASTER.but(vs=300, v0=300), CONC, DARK)
STYLES['stage'] = (CURT, STAGEF, DARK)
STYLES['diner'] = (DWALL, DFLOOR, WHITE)
STYLES['hotel'] = (HWALL, CARPET, WHITE)
STYLES['ward'] = (Mat('medibay.jpg', 384), LINO, WHITE)
STYLES['studio'] = (Mat('officewall.jpg', 364), STAGEF, DARK)
STYLES['yard'] = (Mat('concrete_wall_texture_1789291161197.jpg', 512), ASPHALT, DARK)
STYLES['int'] = (Mat('standard_concrete_1789291464696.jpg', 512), CONC, WHITE)


def ndoor(R, name, x, y, z, angle, key=0, locked=False, old=False, start_open=False):
    """rooms_s16.ndoor plus: old = the Indev zone's old door panel, start_open = open when the map is built"""
    R.spawns.append(dict(kind='ndoor', name=name, pos=(x, y, z), angle=angle, key=key, locked=locked, old=old, open=start_open))
STYLES['cell953'] = (WHITE, WOOD, WHITE)


# --------------------------------------------------------------------- small helpers
def label5(R, num, cx, cz, facing, yc=214.0, size=76.0):
    wall_decal(R, LAB5, cx, cz, facing, size, size, yc, uv=L5[num])


def doorplate5(R, num, cx, cz, facing, yc=258.0, size=68.0):
    wall_decal(R, DPL5, cx, cz, facing, size, size, yc, uv=DP5[num])


def plate5(R, key, cx, cz, facing, yc=352.0, w=220.0, h=None):
    wall_decal(R, PLT5, cx, cz, facing, w, h or w * 0.15, yc, uv=P5[key])


def prop5(R, key, cx, cz, facing, w, h, yc):
    wall_decal(R, PROPS5, cx, cz, facing, w, h, yc, uv=PR5[key])


def neon5(R, key, cx, cz, facing, w, h, yc):
    wall_decal(R, NEON5, cx, cz, facing, w, h, yc, uv=N5[key])


def hang5(R, key, x, z, y, w=220.0, h=34.0, top=None):
    """a sign hung across the room on chains, readable from both sides (its face spans x)"""
    R.box(x - w / 2, y - h / 2, z - 2, x + w / 2, y + h / 2, z + 2, DARK, lux=10)
    wall_decal(R, PLT5, x, z + 2, 'N', w, h, y, uv=P5[key])
    wall_decal(R, PLT5, x, z - 2, 'S', w, h, y, uv=P5[key])
    if top:
        for dx in (-w / 2 + 12, w / 2 - 12):
            chain(R, x + dx, z, top, top - (y + h / 2))


def wall_facing(R, p, q, y0, y1, mat, facing, holes=(), **kw):
    """an axis-aligned wall between p and q (xz) whose visible side faces `facing` ('N' 'S' 'E' 'W');
    holes = [(c0, c1, hy0, hy1)] with c in absolute world units along the wall"""
    if facing in 'NS':
        lo, hi = sorted((p[0], q[0]))
        z = p[1]
        a, b = ((hi, z), (lo, z)) if facing == 'N' else ((lo, z), (hi, z))
        ref = a[0]
    else:
        lo, hi = sorted((p[1], q[1]))
        x = p[0]
        a, b = ((x, lo), (x, hi)) if facing == 'E' else ((x, hi), (x, lo))
        ref = a[1]
    hs = [tuple(sorted((abs(c0 - ref), abs(c1 - ref)))) + (hy0, hy1) for (c0, c1, hy0, hy1) in holes]
    R.wall(a, b, y0, y1, mat, holes=hs, **kw)


def both_faces(R, p, q, y0, y1, mat, facings, holes=(), mat2=None, t=0.0, **kw):
    """a partition seen from both sides; t = half thickness (offsets each face off the centre line)"""
    f1, f2 = facings
    off = {'N': (0, t), 'S': (0, -t), 'E': (t, 0), 'W': (-t, 0)}
    for f, m in ((f1, mat), (f2, mat2 or mat)):
        o = off[f]
        wall_facing(R, (p[0] + o[0], p[1] + o[1]), (q[0] + o[0], q[1] + o[1]), y0, y1, m, f, holes, **kw)


def reveals(R, axis, a, b, c0, c1, y0, y1, mat):
    """the four faces lining a rectangular hole through a wall that runs along `axis` (the wall's
    thickness spans a..b across it); c0..c1 along the wall, y0..y1 up"""
    if axis == 'z':                       # wall runs along z, thickness along x
        poly_facing(R, [V(a, y0, c0), V(b, y0, c0), V(b, y0, c1), V(a, y0, c1)], (0, 1, 0), mat, lux=10)
        poly_facing(R, [V(a, y1, c0), V(b, y1, c0), V(b, y1, c1), V(a, y1, c1)], (0, -1, 0), mat, lux=10)
        poly_facing(R, [V(a, y0, c0), V(b, y0, c0), V(b, y1, c0), V(a, y1, c0)], (0, 0, 1), mat, lux=10)
        poly_facing(R, [V(a, y0, c1), V(b, y0, c1), V(b, y1, c1), V(a, y1, c1)], (0, 0, -1), mat, lux=10)
    else:                                 # wall runs along x, thickness along z
        poly_facing(R, [V(c0, y0, a), V(c0, y0, b), V(c1, y0, b), V(c1, y0, a)], (0, 1, 0), mat, lux=10)
        poly_facing(R, [V(c0, y1, a), V(c0, y1, b), V(c1, y1, b), V(c1, y1, a)], (0, -1, 0), mat, lux=10)
        poly_facing(R, [V(c0, y0, a), V(c0, y0, b), V(c0, y1, b), V(c0, y1, a)], (1, 0, 0), mat, lux=10)
        poly_facing(R, [V(c1, y0, a), V(c1, y0, b), V(c1, y1, b), V(c1, y1, a)], (-1, 0, 0), mat, lux=10)


def collide_facing(R, pts, hint):
    """an invisible collision quad (stairs ramps); wound the way roomkit winds a visible one facing `hint`"""
    P = [np.asarray(p, dtype=float) for p in pts]
    n = np.zeros(3)
    for i in range(1, len(P) - 1):
        n += np.cross(P[i + 1] - P[0], P[i] - P[0])
    if np.dot(n, np.asarray(hint, dtype=float)) < 0:
        P = P[::-1]
    R.hidden.append(P)


def glass_quad(R, a, b, y0, y1):
    """a pane of glass between two xz points, drawn both ways, collides both ways"""
    L = float(np.linalg.norm(np.asarray(b, dtype=float) - np.asarray(a, dtype=float)))
    for (p, q) in ((a, b), (b, a)):
        R.quad(V(p[0], y0, p[1]), V(q[0], y0, q[1]), V(q[0], y1, q[1]), V(p[0], y1, p[1]), GLASS, uvrect=(0, 0, L / 256.0, (y1 - y0) / 512.0), lm=False, coll=False)
    R.collide_wall(a, b, y0, y1)
    R.collide_wall(b, a, y0, y1)


def recess(R, x0, x1, y0, y1, zf, depth, sign, mat):
    """a dark stub behind a hole in a wall at z = zf, going `depth` further in the `sign` direction (faces inward)"""
    zb = zf + sign * depth
    za, zc = sorted((zf, zb))
    poly_facing(R, [V(x0, y0, zb), V(x1, y0, zb), V(x1, y1, zb), V(x0, y1, zb)], (0, 0, -sign), mat, lux=16)
    poly_facing(R, [V(x0, y0, za), V(x0, y0, zc), V(x0, y1, zc), V(x0, y1, za)], (1, 0, 0), mat, lux=16)
    poly_facing(R, [V(x1, y0, za), V(x1, y0, zc), V(x1, y1, zc), V(x1, y1, za)], (-1, 0, 0), mat, lux=16)
    poly_facing(R, [V(x0, y1, za), V(x1, y1, za), V(x1, y1, zc), V(x0, y1, zc)], (0, -1, 0), mat, lux=16)
    poly_facing(R, [V(x0, y0, za), V(x1, y0, za), V(x1, y0, zc), V(x0, y0, zc)], (0, 1, 0), mat, lux=16)


def stool(R, x, z, y=0.0):
    R.tube((x, y, z), (x, y + 70, z), 5, CHROME, sides=6, lux=16)
    R.prism(octo(x, z, 20), y + 70, y + 82, VINYL.but(us=64), lux=12)
    R.prism(octo(x, z, 16), y, y + 4, CHROME, caps='T', lux=12)


def tube_tank(R, x, z, y, r=58.0, h=280.0, broken=False):
    """an RCI growth tube: plinth, glass, fluid, cap, feed pipes"""
    R.prism(octo(x, z, r + 14), y, y + 30, DARK, caps='T', lux=12)
    if broken:
        R.prism(octo(x, z, r), y + 30, y + 92, GLASS, caps='', lm=False, coll=False)
        R.floor(octo(x + 30, z - 40, r + 50), y + 1.0, FLUID, coll=False)
    else:
        R.prism(octo(x, z, r), y + 30, y + 30 + h, GLASS, caps='', lm=False, coll=False)
        R.prism(octo(x, z, r - 6), y + 31, y + 20 + h, FLUID, caps='T', lm=False, coll=False)
        R.prism(octo(x, z, r + 10), y + 30 + h, y + 60 + h, DARK, caps='TB', lux=12)
        for dx in (-24, 24):
            R.tube((x + dx, y + 60 + h, z), (x + dx, y + 420, z), 6, RUST.but(us=38, vs=256), sides=6, lux=18)
    ring = octo(x, z, r)
    for i in range(8):
        a, b = ring[i], ring[(i + 1) % 8]
        R.collide_wall(a, b, y, y + 30 + h)
        R.collide_wall(b, a, y, y + 30 + h)


def open_bay(R, plane, sign, a0, a1, depth, h, wallm, floorm, ceilm):
    """an alcove behind a hole (a0..a1 along z, 0..h) in the wall x = plane, open to the corridor"""
    far = plane + sign * depth
    lo, hi = sorted((plane, far))
    wall_facing(R, (far, a0), (far, a1), 0, h, wallm, 'E' if sign < 0 else 'W')
    wall_facing(R, (lo, a0), (hi, a0), 0, h, wallm, 'N')
    wall_facing(R, (lo, a1), (hi, a1), 0, h, wallm, 'S')
    R.rect_floor(lo, a0, hi, a1, 0, floorm)
    R.rect_ceil(lo, a0, hi, a1, h, ceilm)
    return lo, hi


# =====================================================================  HCZ
def room2subway052():
    """SCP-052's platform, from the reference photo: a 59 ST station under the corridor, tiled walls with a
    mosaic band, steel columns, a yellow edge, the pit, and the R4 car (code-made) when it comes."""
    R = R_('room2subway052', amb=10)
    AW = wmat('hcz', 384)
    junction(R, 'NS', 'hcz', openings={'hubW': [door_op(0)]})
    lift(R, -192, -1, 0, 0, 0, D, AW)
    plate5(R, 'platform', -192, 0, 'E', yc=352, w=240)
    sign_at(R, 'elevator', -192, -250, 'E', 150, 50, 250)
    label5(R, '052', -192, 250, 'E')
    plate5(R, 'closed', -192, 630, 'E', yc=190, w=250)
    lamps(R, NS3, 384, power=78, color=(232, 238, 255), size=36)
    # ---- the hall at platform level
    PE, PX, ZE = 440.0, 920.0, 900.0          # platform edge, far wall, end walls
    PIT = D - 140.0
    CONCD = Mat('concrete_wall_texture_1789291161197.jpg', 256)
    wall_facing(R, (-192, -ZE), (-192, ZE), D, D + 520, TILEW, 'E', holes=[(-96.0, 96.0, D, D + 320)])
    for zs, f in ((ZE, 'S'), (-ZE, 'N')):
        wall_facing(R, (-192, zs), (PE, zs), D, D + 520, TILEW, f)
        wall_facing(R, (PE, zs), (PX, zs), D, D + 520, TILEW, f, holes=[(470.0, 890.0, D, D + 300)])
        wall_facing(R, (PE, zs), (PX, zs), PIT, D, CONCD, f, holes=[(470.0, 890.0, PIT, D)])
        recess(R, 470, 890, PIT, D + 300, zs, 110, 1 if zs > 0 else -1, DARK)
    wall_facing(R, (PX, -ZE), (PX, ZE), D, D + 520, TILEW, 'W')
    wall_facing(R, (PX, -ZE), (PX, ZE), PIT, D, CONCD, 'W')
    R.rect_floor(-192, -ZE, PE, ZE, D, CONC)
    R.rect_floor(400, -ZE, PE, ZE, D + 0.6, EDGE, coll=False, lux=10)
    wall_facing(R, (PE, -ZE), (PE, ZE), PIT, D, CONCD, 'E')
    R.rect_floor(PE, -ZE, PX, ZE, PIT, BALLAST)
    R.rect_ceil(-192, -ZE, PX, ZE, D + 520, DIRTY)
    # the track: sleepers, rails, the covered third rail
    for k in range(-13, 14):
        z = k * 64.0
        R.box(560, PIT, z - 7, 780, PIT + 12, z + 7, OLDWOOD, skip='B', lux=10)
    for x in (573.0, 767.0):
        R.box(x - 4, PIT + 12, -ZE, x + 4, PIT + 30, ZE, METAL, skip='BNS', lux=10)
    R.box(866, PIT, -ZE, 876, PIT + 26, ZE, DIRTY, skip='BNS', lux=10)
    R.box(856, PIT + 26, -ZE, 892, PIT + 32, ZE, OLDWOOD, skip='NS', lux=10)
    # steps out of the pit at the north end (no car ever stops over them)
    for i in range(5):
        x1 = PE + (5 - i) * 36
        R.box(PE, PIT, 830, x1, PIT + (i + 1) * 28, ZE, CONCD, skip='BN', top=CONC, lux=10)
    collide_facing(R, [V(PE + 216, PIT, 830), V(PE + 216, PIT, ZE), V(PE + 30, D, ZE), V(PE + 30, D, 830)], (1, 1, 0))
    # columns, ceiling girders, the name tablets, signs, the clock, benches
    for z in (-720.0, -280.0, 280.0, 720.0):
        R.box(366, D, z - 15, 396, D + 520, z + 15, GREENP, skip='TB', lux=12)
        R.box(360, D, z - 21, 402, D + 30, z + 21, GREENP, skip='B', lux=10)
    for z in (-720.0, -280.0, 280.0, 720.0):
        ibeam(R, 'z', z, -192, PX, D + 500, size=26)
    for z in (-560.0, 560.0):
        prop5(R, '59st', -192, z, 'E', 300, 112, D + 330)
    for z in (-600.0, 0.0, 600.0):
        prop5(R, '59st', PX, z, 'W', 380, 142, D + 290)
    prop5(R, 'stripmap', -192, -300, 'E', 330, 41, D + 210)
    hang5(R, 'uptown', 180, -120, D + 420, w=230, h=34, top=D + 500)
    R.box(158, D + 410, 196, 202, D + 454, 204, DARK, lux=10)
    prop5(R, 'clock', 180, 204, 'N', 40, 40, D + 432)
    prop5(R, 'clock', 180, 196, 'S', 40, 40, D + 432)
    chain(R, 180, 200, D + 500, 46)
    for z in (-420.0, 140.0):
        R.model('scpcb_bench.x', 40, D, z, rot=(0, 90, 0), scale=(1, 1, 1), size=(44, 50, 144))
    # MTF Gamma-6 post at the south end
    top = desk(R, -186, -820, -106, -640, D)
    chair(R, -60, -730, 'W', y=D)
    plate5(R, 'gamma6', -192, -730, 'E', yc=D + 300, w=220)
    named(R, 'GUARD', -40, D, -560)
    # the vent over the track
    R.rect_ceil(600, -480, 760, -320, D + 519.4, VENT.but(us=160), coll=False)
    bigfan(R, 680, D + 505, -400, radius=78)
    # the light: yellow, as in the photo
    for z in (-760.0, -450.0, -140.0, 170.0, 480.0, 780.0):
        ceil_light(R, 130, z, D + 520, size=24, power=74, rng=720, color=(255, 212, 150))
    for z in (-560.0, 0.0, 560.0):
        ceil_light(R, 680, z, D + 520, size=20, power=44, rng=620, color=(255, 200, 140))
    named(R, 'TRAIN', 680, D, 0)           # the car's floor centre (the car is 400 wide, 1640 long)
    named(R, 'PASS', 420, D, 0)            # where a passenger steps off
    named(R, 'PSTAND', 170, D, 60)         # where he waits
    named(R, 'EXIT', 250, D, -100)         # where a rider is set down again
    reserve(R, 'TRAINM')
    reserve(R, 'LEAF', 6)
    reserve(R, 'TFAN', 2)
    item(R, 'doc052', -150, top, -700)
    item(R, 'firstaid', -150, top, -770, 60)
    item(R, 'bat', 60, D, -380, 50)
    return (R, 'SUB', '59th St. platform (Indev). A lift down to a copy of the station SCP-052 stops at. It still stops.',
            2, 0.5, ((-80, D + 165, -820), (620, D + 160, 200)))


def room2sheet():
    R = R_('room2sheet')
    win = (-380.0, -200.0, 100.0, 260.0)
    junction(R, 'NS', 'hcz', openings={'hubW': [door_op(0)], 'S_E': [door_op(-560), win]})
    annex(R, 'x', -192, -1, -560, 560, 640, 352, 'hotel', door=0, spawn_door=False)
    ndoor(R, 'CHAMBER', -224, 0, 0, 90)
    annex(R, 'x', 192, +1, -740, -170, 320, 320, 'white', door=-560, window=win, spawn_door=False)
    glaze(R, 'x', 192, +1, win)
    ndoor(R, 'HOLD', 224, 0, -560, 90, locked=True)
    plate5(R, 'ch6096', -192, 0, 'E', yc=352, w=240)
    plate5(R, 'holdb', 192, -560, 'W', yc=352, w=200)
    label5(R, '6096', -192, 260, 'E')
    # the "chamber": a hotel room
    R.box(-892, 0, 300, -680, 40, 540, DIRTY, skip='B', top=WHITE, lux=10)
    R.box(-892, 40, 310, -690, 58, 530, WHITE, lux=10)
    R.box(-896, 0, 296, -884, 150, 544, WOOD, skip='B', lux=10)
    for z in (360.0, 480.0):
        tbox(R, -880, 58, z - 40, -830, 74, z + 40, WHITE)
    R.box(-600, 0, 520, -440, 60, 556, WOOD, skip='B', lux=10)
    R.box(-580, 60, 530, -460, 160, 550, DARK, lux=10)
    neon5(R, 'static', -520, 529, 'S', 104, 78, 110)
    named(R, 'SIT', -520, 0, 330)
    R.box(-420, 0, 330, -330, 44, 430, VINYL, skip='B', lux=10)
    R.box(-420, 44, 420, -330, 110, 440, VINYL, lux=10)
    R.box(-896, 0, -380, -840, 90, -260, WOOD, skip='B', top=WHITE, lux=10)
    prop5(R, 'sinkcab', -840, -320, 'E', 110, 60, 46)
    R.box(-896, 90, -360, -876, 220, -280, DIRTY, lux=10)
    named(R, 'SINK', -836, 60, -320)
    R.box(-896, 0, -200, -850, 90, -140, WHITE, skip='B', lux=10)
    prop5(R, 'hotelart', -650, 560, 'S', 160, 80, 200)
    flat(R, -760, -160, -400, 220, 0.8, CARPET.but(us=96), bottom='S', lux=14, cast=False)
    prop5(R, 'sheetnotice', -256, 230, 'W', 120, 60, 250)
    # the fan over the middle of the room, its hoist lever by the door
    ceil_fan(R, -430, -60, 352, radius=150)
    named(R, 'FANSPOT', -430, 0, -60)
    wall_decal(R, CTRL, -330, -560, 'N', 110, 110, 170)
    lever(R, 'HOIST', -330, 170, -556, 180, up=True)
    plate5(R, 'hoist', -330, -560, 'N', yc=250, w=150)
    named(R, 'ZETA', -700, 0, -300)
    named(R, 'P1', -150, 0, 0)
    named(R, 'P2', 0, 0, -560)
    named(R, 'P3', 300, 0, -560)
    reserve(R, 'SHEETM')
    reserve(R, 'PIN')
    # Holding 6096-B
    R.box(480, 0, -730, 570, 40, -560, DIRTY, skip='B', top=WHITE, lux=10)
    R.box(260, 0, -300, 320, 50, -240, WHITE, skip='B', lux=10)
    named(R, 'DCLASS', 430, 0, -380)
    for (x, z) in ((-420, 0), (-640, -380), (-640, 380)):
        ceil_light(R, x, z, 352, size=56, power=88, rng=800, color=(255, 236, 206))
    ceil_light(R, 420, -450, 320, size=48, power=72, rng=600)
    lamps(R, NS3, 384, power=74, color=(232, 238, 255), size=36)
    item(R, 'doc6096', -300, 0, 300)
    item(R, 'eyedrops', -700, 0, 500, 50)
    return (R, 'SH6', 'Humanoid Chamber 6096 (Indev). A hotel room in all but name, a figure under a sheet facing the TV, and Holding 6096-B.',
            2, 0.3, ((-280, 165, -420), (-520, 100, 300)))


def room2block15():
    R = R_('room2block15', amb=9)
    W_ = 256.0
    junction(R, 'NS', 'block', w=W_, ch=530, openings={'hubE': [door_op(160)], 'S_W': [door_op(-500)],
                                                      'N_W': [(480.0, 640.0, 320.0, 480.0)], 'S_E': [(-640.0, -480.0, 320.0, 480.0)]})
    # the barrel vault, with three skylights in its crown
    n = 10
    sky = ((-700.0, -500.0), (-100.0, 100.0), (500.0, 700.0))
    for k in range(n):
        a0, a1 = math.pi * k / n, math.pi * (k + 1) / n
        p0 = (W_ * math.cos(a0), 300 + 220 * math.sin(a0))
        p1 = (W_ * math.cos(a1), 300 + 220 * math.sin(a1))
        am = (a0 + a1) / 2
        hint = (-math.cos(am), -math.sin(am), 0)
        cuts = [(-992.0, 992.0, PLASTER)]
        if k in (4, 5):
            cuts = []
            prev = -992.0
            for (s0, s1) in sky:
                cuts.append((prev, s0, PLASTER))
                cuts.append((s0, s1, LIGHTPANEL.but(emit=205)))
                prev = s1
            cuts.append((prev, 992.0, PLASTER))
        for (z0, z1, m) in cuts:
            poly_facing(R, [V(p0[0], p0[1], z0), V(p1[0], p1[1], z0), V(p1[0], p1[1], z1), V(p0[0], p0[1], z1)], hint, m,
                        lux=16, cast=(m is PLASTER))
    for (s0, s1) in sky:
        R.light(0, 470, (s0 + s1) / 2, rng=980, color=(206, 218, 240), power=78, radius=40)
    wall_fan(R, 'x', -W_, -1, 560, 400)
    wall_fan(R, 'x', W_, +1, -560, 400)
    # the cell doors nobody opens
    for z in (-860.0, -180.0, 120.0, 400.0, 800.0):
        prop5(R, 'celldoor', -W_, z, 'E', 120, 230, 115)
    for z in (-860.0, -300.0, 480.0, 800.0):
        prop5(R, 'celldoor', W_, z, 'W', 120, 230, 115)
    # Cell 667
    annex(R, 'x', W_, +1, -20, 340, 260, 300, 'cell', door=160, spawn_door=False)
    ndoor(R, 'C667', W_ + 32, 0, 160, 90, old=True)
    R.box(470, 0, 200, 576, 38, 330, OLDWOOD, skip='B', top=STRAW, lux=10)
    R.prism(octo(360, 290, 20), 0, 36, DIRTY, caps='T', top=DARK, lux=12)
    ceil_light(R, 450, 160, 300, size=24, power=26, rng=380, color=(220, 220, 210))
    named(R, 'CELLIN', 470, 0, 160)
    prop5(R, 'intake', W_, 290, 'W', 70, 90, 150)
    named(R, 'CLIP', W_ - 4, 150, 290)
    plate5(R, 'c667', W_, 160, 'W', yc=352, w=170)
    label5(R, '2701', W_, 0, 'W', yc=230)
    # the open cell, and the man in it
    annex(R, 'x', -W_, -1, -660, -340, 260, 300, 'cell', door=-500, spawn_door=False)
    ndoor(R, 'OPEN', -W_ - 32, 0, -500, 90, old=True, start_open=True)
    R.box(-576, 0, -650, -470, 38, -520, OLDWOOD, skip='B', top=STRAW, lux=10)
    named(R, 'PRIS', -440, 0, -600)
    ceil_light(R, -450, -500, 300, size=24, power=26, rng=380, color=(220, 220, 210))
    # the guard post
    top = desk(R, -250, -820, -170, -640, 0)
    chair(R, -130, -730, 'W')
    for z in (-600.0, -560.0):
        chain(R, -250, z, 300, 130)
    named(R, 'GUARD', -60, 0, -760)
    plate5(R, 'block15', -W_, -920, 'E', yc=300, w=200)
    for z in (-700.0, -300.0, 100.0, 520.0, 880.0):
        wall_light(R, -W_, z, 270, 'E', power=34, rng=520, color=(255, 214, 160))
    for z in (-520.0, -80.0, 620.0, 900.0):
        wall_light(R, W_, z, 270, 'W', power=34, rng=520, color=(255, 214, 160))
    item(R, 'doc2701', -210, top, -760)
    item(R, 'doc2701b', -520, 38, -590)
    return (R, 'B15', 'Cell Block 15 (Indev). An 1840s vaulted cell block. Cell 667 is SCP-2701; the INTAKE form hangs beside it.',
            2, 0.75, ((-120, 165, -880), (200, 200, 300)))


def room2wait1440():
    R = R_('room2wait1440')
    junction(R, 'NS', 'hcz', openings={'S_W': [door_op(-250)], 'N_W': [door_op(370)]})
    annex2(R, 'x', -192, -1, -560, 60, 480, 352, 'int', door=-250, extra={1: [(86.0, 386.0, 100.0, 260.0)]})
    annex2(R, 'x', -192, -1, 140, 600, 480, 352, 'int', door=370, extra={3: [(94.0, 394.0, 100.0, 260.0)]})
    reveals(R, 'x', 60, 140, -650, -350, 100, 260, DARK)
    glass_quad(R, (-650, 100), (-350, 100), 100, 260)
    plate5(R, 'int142', -192, -250, 'E', yc=352, w=220)
    plate5(R, 'observe', -192, 370, 'E', yc=352, w=200)
    label5(R, '1440', -192, -500, 'E')
    # Interview Room 142: a steel table, two chairs, the old man's things
    top = table(R, -560, -320, -400, -180, top=METAL)
    chair(R, -610, -250, 'E')
    chair(R, -350, -250, 'W')
    flat(R, -520, -280, -460, -230, top + 0.7, PROPS5, PR5['cards'], bottom='W')
    R.prism(octo(-430, -205, 6, 8), top, top + 14, GLASS, caps='', lm=False, coll=False)
    ball(R, (-690, 26, -350), 26, OLDWOOD, seg=7, rings=3, lux=18)
    named(R, 'OLD', -640, 0, -250)
    named(R, 'TABLE', -480, top, -250)
    named(R, 'CARDS', -490, top + 2, -255)
    named(R, 'CUP', -430, top + 8, -205)
    R.tube((-736, 320, -470), (-256, 320, -470), 10, RUST.but(us=63), sides=8, lux=16)
    named(R, 'PIPE', -500, 320, -470)
    named(R, 'CRACKAT', -734, 180, -250)
    reserve(R, 'CRACK')
    ceil_fan(R, -500, -60, 352, radius=120)
    ceil_light(R, -480, -300, 352, size=56, power=96, rng=760, color=(240, 244, 255))
    # the observation room behind the mirror
    dtop = desk(R, -660, 150, -340, 230, 0)
    for x in (-600.0, -400.0):
        workstation(R, x, dtop, 190, 180)
        chair(R, x, 300, 'S')
    ceil_light(R, -500, 400, 352, size=48, power=60, rng=640, color=(220, 230, 255))
    lamps(R, NS3, 384, power=74, color=(232, 238, 255), size=36)
    item(R, 'doc1440', -520, dtop, 170)
    item(R, 'firstaid', -300, 0, 560, 50)
    return (R, 'OLD', 'Interview Room 142 (Indev). SCP-1440 has stopped here. Things are starting to break.',
            2, 0.15, ((-300, 165, 0), (-620, 120, -250)))


# =====================================================================  LCZ
def room2hall99():
    """Hallway 99: the reference corridor again - white walls, a dark band, pilasters with sloped feet, a dark
    ceiling with bulkheads, black door plates, a window onto machinery - lined with open dog kennels."""
    R = R_('room2hall99')
    w, ch = 224.0, 448.0
    hub = (-w, -640, w, 320)
    win = (380.0, 580.0, 100.0, 300.0)
    niche = (-900.0, -740.0, 120.0, 330.0)
    junction(R, 'NS', 'lcz', w=w, ch=ch, hub=hub, hh=ch,
             openings={'hubW': [(-620.0, 240.0, 0.0, 300.0)], 'hubE': [(-620.0, 240.0, 0.0, 300.0)],
                       'N_E': [door_op(740), win], 'N_W': [(520.0, 680.0, 250.0, 410.0)], 'S_W': [niche]})
    WM = wmat('lcz', ch)
    for c in (-940.0, -690.0, 930.0):
        chamfer_pilaster(R, -w, +1, c, ch, WM)
        chamfer_pilaster(R, w, -1, c, ch, WM)
    chamfer_pilaster(R, -w, +1, 360, ch, WM)
    chamfer_pilaster(R, w, -1, 330, ch, WM)
    for c in (-940.0, -690.0, 320.0, 930.0):
        R.box(-w, ch - 64, c - 36, w, ch, c + 36, WM.but(us=256), skip='T', lux=12)
    # the kennels: three a side, wire fronts, straw
    for s in (-1, 1):
        lo, hi = open_bay(R, s * w, s, -620, 240, 230, 300, WHITE.but(us=256), CONC, DARK)
        for z in (-330.0, -45.0):
            R.box(lo, 0, z - 6, hi, 300, z + 6, WHITE, skip='TB', lux=10)
        mesh_panel(R, (s * (w + 6), -620), (s * (w + 6), 240), 0, 300)
        for (a, b) in ((-610.0, -342.0), (-318.0, -57.0), (-33.0, 230.0)):
            flat(R, lo + 10, a + 10, hi - 10, b - 10, 0.8, STRAW, bottom='S', lux=12)
            bx = s * (w + 190)
            R.prism(octo(bx, (a + b) / 2 + 80, 14), 0, 10, METAL, caps='T', top=DARK, lux=14)
        for i, zc in enumerate((-476.0, -188.0, 98.0)):
            named(R, 'DOG%d' % (i if s < 0 else i + 3), s * (w + 120), 0, zc)
    prop5(R, 'kennelcard', -w - 6, -476, 'E', 90, 45, 330)
    prop5(R, 'kennelcard', w + 6, 98, 'W', 90, 45, 330)
    plate5(R, 'kennel', -w, -200, 'E', yc=380, w=220)
    plate5(R, 'kennel', w, -200, 'W', yc=380, w=220)
    for (z, key) in ((280.0, 'ALERT'), (-700.0, 'ALERT2')):
        wall_decal(R, CTRL, w, z, 'W', 56, 56, 150)
        plate5(R, 'alert', w, z, 'W', yc=200, w=120)
        named(R, key, w - 4, 150, z)
    # SCP-953's cell, its window, its door (found open)
    annex(R, 'x', w, +1, 340, 930, 448, 352, 'cell953', door=740, window=win, spawn_door=False)
    glaze(R, 'x', w, +1, win)
    ndoor(R, 'CELL', w + 32, 0, 740, 90, start_open=True)
    doorplate5(R, '953', w, 880, 'W')
    plate5(R, 'hall99', -w, 600, 'E', yc=340, w=200)
    R.box(560, 0, 760, 730, 18, 920, WOOD, skip='B', top=FUTON, lux=10)
    tbox(R, 680, 18, 860, 726, 30, 912, WHITE)
    R.box(310, 0, 860, 380, 8, 920, METAL, skip='B', lux=10)
    ball(R, (345, 14, 890), 16, FLESH, seg=6, rings=2, top_only=True, lux=20)
    R.tube((420, 0, 900), (420, 40, 900), 6, GREENP, sides=6, caps=True, lux=18)
    book(R, 600, 0, 600, 30)
    book(R, 640, 0, 640, -50)
    wall_decal(R, CLAWS, w + 64, 860, 'E', 90, 120, 160)
    label5(R, '953', 736, 500, 'W', yc=220)
    named(R, 'DEN', 600, 0, 560)
    ceil_light(R, 520, 640, 352, size=48, power=70, rng=640, color=(255, 236, 214))
    # the window onto machinery (as in the reference shot), and a fan in the north wall
    annex(R, 'x', -w, -1, -920, -720, 120, 384, 'std', window=niche)
    wall_decal(R, CTRL, -w - 64 - 120, -820, 'E', 180, 200, 215)
    for zz in (-870.0, -770.0):
        R.tube((-w - 120, 300, zz), (-w - 120, 384, zz), 14, DIRTY, sides=8, lux=16)
    wall_fan(R, 'x', -w, -1, 600, 330)
    # the cart's run, the spots she likes
    named(R, 'CARTA', 160, 0, -900)
    named(R, 'CARTB', 160, 0, 680)
    named(R, 'SPOTN', -90, 0, 880)
    named(R, 'SPOTS', -60, 0, -880)
    reserve(R, 'DOGM', 6)
    reserve(R, 'FOXM')
    reserve(R, 'CARTM')
    lamps(R, ((0, -820), (0, -340), (0, 120), (0, 560), (0, 870)), ch, power=90, rng=900, size=32)
    for s in (-1, 1):
        for zc in (-476.0, -188.0, 98.0):
            ceil_light(R, s * (w + 120), zc, 300, size=28, power=40, rng=420, color=(255, 240, 220))
    item(R, 'doc953', 620, 0, 700)
    item(R, 'doc953b', 180, 0, 300)
    item(R, 'firstaid', -w - 70, 0, -820, 60)
    return (R, 'H99', 'Hallway 99 (Indev). The kennel corridor to SCP-953\'s cell. The cell is open. Keep the dogs loud.',
            1, 0.35, ((0, 165, -940), (0, 190, 200)))


def room2psych():
    R = R_('room2psych')
    junction(R, 'NS', 'old', openings={'hubE': [door_op(0)]})
    x0, z0, x1, z1 = annex(R, 'x', 192, +1, -640, 640, 700, 352, 'ward', door=0, key=1)
    plate5(R, 'psych', 192, 0, 'W', yc=352, w=240)
    label5(R, '482', 192, 250, 'W')
    # two padded cells along the south, glass fronts
    zf = -300.0
    wins = [(300.0, 540.0, 60.0, 260.0), (640.0, 880.0, 60.0, 260.0)]
    both_faces(R, (x0, zf), (x1, zf), 0, 352, Mat('medibay.jpg', 384), ('N', 'S'), holes=wins, mat2=PADDED, t=6)
    for (c0, c1, y0, y1) in wins:
        reveals(R, 'x', zf - 6, zf + 6, c0, c1, y0, y1, WHITE)
        glass_quad(R, (c0, zf), (c1, zf), y0, y1)
    both_faces(R, (590, z0), (590, zf), 0, 352, PADDED, ('E', 'W'), t=6)
    R.box(584, 0, zf - 6, 596, 352, zf + 6, WHITE, skip='TBEW', lux=10)
    for (a, b) in ((x0, 584.0), (596.0, x1)):
        wall_facing(R, (a, z0 + 1), (b, z0 + 1), 0, 352, PADDED, 'N')
        R.rect_floor(a, z0, b, zf - 6, 0.6, PADDED, coll=False, lux=12)
    wall_facing(R, (x0 + 1, z0), (x0 + 1, zf), 0, 352, PADDED, 'E')
    wall_facing(R, (x1 - 1, z0), (x1 - 1, zf), 0, 352, PADDED, 'W')
    named(R, 'PAT', 420, 0, -480)
    ceil_light(R, 420, -470, 352, size=40, power=52, rng=520)
    ceil_light(R, 770, -470, 352, size=40, power=40, rng=520)
    # Containment Locker 482: a wire cage in the corner, the jacket on its hook
    cage(R, 760, 380, 940, 630, h=260, open_side='S', gap=(800.0, 900.0))
    named(R, 'JACKET', 860, 0, 540)
    reserve(R, 'JACKETM')
    prop5(R, 'tag482', 860, z1, 'S', 72, 36, 140)
    plate5(R, 'locker482', 850, z1, 'S', yc=300, w=230)
    # the attendant's desk
    top = desk(R, 500, 120, 700, 210, 0)
    workstation(R, 600, top, 150, 180)
    chair(R, 600, 260, 'S')
    named(R, 'ATT', 650, 0, 300)
    ceil_fan(R, 560, 60, 352)
    for (x, z) in ((420, 200), (760, 200), (850, 500)):
        ceil_light(R, x, z, 352, size=64, power=104, rng=860, color=(240, 248, 255))
    lamps(R, NS3, 384, power=86)
    item(R, 'doc482', 540, top, 165)
    item(R, 'doc482b', 660, top, 140)
    item(R, 'eyedrops', 320, 0, 560, 60)
    return (R, 'PSY', 'Psychiatric Observation (Indev). Two padded cells and Containment Locker 482: SCP-482, the black straitjacket.',
            1, 0.85, ((300, 165, 560), (860, 150, 520)))


# =====================================================================  EZ
def room2diner():
    R = R_('room2diner')
    wz = (-420.0, -140.0, 140.0, 420.0)
    junction(R, 'NS', 'ez', openings={'hubE': [door_op(0)]})
    x0, z0, x1, z1 = annex2(R, 'x', 192, +1, -620, 620, 720, 352, 'diner', door=0,
                            extra={2: [tuple(sorted((620 - (c - 100), 620 - (c + 100)))) + (120.0, 270.0) for c in wz]})
    # the windows: a short chrome-lined recess each, with the default view at the back (the code paints over it)
    for c in wz:
        reveals(R, 'z', x1, x1 + 24, c - 100, c + 100, 120, 270, CHROME)
        wall_facing(R, (x1 + 24, c - 100), (x1 + 24, c + 100), 120, 270, VIEW0, 'W')
    for i, c in enumerate(wz):
        named(R, 'WIN%d' % i, x1 + 23, 195, c)
        top = table(R, x1 - 100, c - 40, x1 - 4, c + 40, top=CHROME)
        for s in (-1, 1):
            zs = c + s * 58
            R.box(x1 - 100, 0, min(zs, zs + s * 40), x1 - 2, 44, max(zs, zs + s * 40), VINYL, skip='B', lux=10)
            zb = c + s * 98
            R.box(x1 - 100, 44, min(zb, zb + s * 12), x1 - 2, 120, max(zb, zb + s * 12), VINYL, lux=10)
    # the counter and the stools
    R.box(420, 0, 300, 900, 96, 356, VINYL, skip='B', top=CHROME, lux=10)
    R.box(414, 96, 294, 906, 104, 362, CHROME, lux=10)
    for x in (470.0, 560.0, 650.0, 740.0, 830.0):
        stool(R, x, 250)
    R.box(420, 0, 570, 900, 92, 620, METAL, skip='B', top=CHROME, lux=10)
    R.box(470, 92, 586, 530, 170, 616, DARK, lux=10)
    glass_box(R, 640, 92, 580, 760, 160, 614)
    for x in (670.0, 730.0):
        R.prism(octo(x, 597, 14), 102, 112, Mat('indev_candy.png', 96), caps='T', lux=14)
    neon5(R, 'freddys', 660, z1, 'S', 340, 106, 300)
    prop5(R, 'menuboard', 660, z1, 'S', 260, 130, 200)
    named(R, 'FRED', 660, 0, 470)
    # the jukebox and the DINER sign
    R.box(560, 0, z0, 640, 160, z0 + 56, DARK.but(us=512), skip='B', lux=10)
    prop5(R, 'jukebox', 600, z0 + 56, 'N', 78, 98, 100)
    named(R, 'JUKE', 600, 100, z0 + 60)
    neon5(R, 'dinersign', 600, z0, 'N', 300, 110, 280)
    # the decontamination shower by the door
    R.box(x0, 0, 434, 380, 260, 446, TILE, skip='B', lux=10)
    wall_facing(R, (x0 + 1, 446), (x0 + 1, z1), 0, 260, TILE, 'E')
    R.rect_floor(x0, 446, 380, z1, 0.6, TILE, coll=False)
    R.tube((300, 240, 600), (300, 250, 540), 4, CHROME, sides=6, lux=16)
    named(R, 'SHOWER', 320, 150, 530)
    plate5(R, 'decon', 318, 434, 'S', yc=290, w=150)
    for (x, z) in ((560.0, -380.0), (780.0, 60.0)):
        ceil_fan(R, x, z, 352)
    for x in (560.0, 800.0):
        pendant(R, x, 330, 352, power=90, rng=640, color=(255, 230, 190))
    for (x, z) in ((420, -300), (700, -330), (820, 440), (360, 180)):
        ceil_light(R, x, z, 352, size=56, power=92, rng=760, color=(255, 238, 214))
    for i, (x, z) in enumerate(((610.0, 205.0), (800.0, -260.0), (690.0, -480.0))):
        named(R, 'PAT%d' % i, x, 0, z)
    plate5(R, 'diner', 192, 0, 'W', yc=352, w=200)
    label5(R, '4258', 192, -250, 'W')
    lamps(R, NS3, 384, power=96, color=(255, 250, 240), size=64)
    item(R, 'doc4258', 120, 0, -330)
    item(R, 'doc4258b', x1 - 52, 78, 140)
    return (R, 'DIN', "Freddy's Diner (Indev). SCP-4258: a 1950s diner whose windows look out on wherever the last customer came from.",
            3, 0.55, ((300, 165, -520), (760, 120, 240)))


# =====================================================================  Indev zone
def room2gameshow():
    R = R_('room2gameshow')
    AW = wmat('std', 384)
    junction(R, 'NS', 'std', openings={'hubE': [door_op(0)], 'S_W': [door_op(-500)]})
    lift(R, -192, -1, -500, 0, -500, UP, AW)
    x0, z0, x1, z1 = annex2(R, 'x', 192, +1, -880, 880, 760, 960, 'stage', door=0, extra={0: [(180.0, 680.0, 730.0, 950.0)]})
    R.spawns.pop()                                    # the stage door is the code's
    ndoor(R, 'STAGE', 224, 0, 0, 90)
    plate5(R, 'stage', 192, 0, 'W', yc=352, w=220)
    label5(R, '024', 192, 250, 'W')
    plate5(R, 'onair', 192, -250, 'W', yc=300, w=150)
    plate5(R, 'obs', -192, -500, 'E', yc=352, w=230)
    sign_at(R, 'elevator', -192, -760, 'E', 150, 50, 250)
    # the mailbox where the tapes turn up
    R.box(-192, 110, 260, -160, 176, 340, DARK, lux=10)
    plate5(R, 'mail', -160, 300, 'E', yc=158, w=70)
    named(R, 'MAILBOX', -156, 140, 300)
    named(R, 'OUTSIDE', -40, 0, 200)
    # STAY / LEAVE
    R.box(440, 0, -90, 500, 112, 90, DARK, skip='B', lux=10)
    prop5(R, 'stay', 440, -45, 'W', 60, 60, 78)
    prop5(R, 'leave', 440, 45, 'W', 60, 60, 78)
    named(R, 'BSTAY', 436, 78, -45)
    named(R, 'BLEAVE', 436, 78, 45)
    # round one: the light-up floor (3 x 4 tiles of 128)
    for i in range(3):
        for j in range(4):
            tx, tz = 560 + i * 128, -720 + j * 128
            flat(R, tx + 2, tz + 2, tx + 126, tz + 126, 0.7, GSTILE, bottom='S', lux=10)
    named(R, 'GRID', 560, 1, -720)
    named(R, 'GRID2', 944, 1, -208)
    reserve(R, 'TILE', 12)
    # round two: padded pillars to weave through
    for (x, z) in ((560, -40), (840, -40), (700, 140), (560, 320), (840, 320)):
        R.box(x - 32, 0, z - 32, x + 32, 200, z + 32, Mat('indev_canopy.png', 64), skip='B', top=DARK, lux=10)
    # round three: the podium and its two buttons, the empty bleachers, the sign
    R.box(560, 0, 540, 940, 22, 760, DARK, skip='B', top=STAGEF, lux=10)
    R.box(700, 22, 690, 800, 140, 730, DARK, lux=10)
    neon5(R, 'take', 725, 690, 'S', 44, 44, 110)
    neon5(R, 'risk', 775, 690, 'S', 44, 44, 110)
    named(R, 'BTAKE', 725, 110, 686)
    named(R, 'BRISK', 775, 110, 686)
    named(R, 'PRIZE', 750, 22, 620)
    for k in range(3):
        R.box(300, 0, 780 + 33 * k, 1000, 40 * (k + 1), z1, BLEACH, skip='B', lux=10)
    neon5(R, 'takeprize', 650, z1, 'S', 720, 112, 560)
    neon5(R, 'applause', x0, -400, 'E', 180, 112, 420)
    neon5(R, 'score', x1, 0, 'W', 260, 162, 380)
    # the rig: trusses with coloured lamps, two studio cameras, the stage fan
    for (c, col) in ((-400.0, (255, 70, 200)), (0.0, (80, 220, 255)), (400.0, (255, 220, 90))):
        ibeam(R, 'z', c, x0, x1, 900, size=34)
        for x in (420.0, 700.0, 940.0):
            R.light(x, 860, c, rng=1100, color=col, power=70, radius=20)
    for z in (-560.0, 520.0):
        R.box(330, 120, z - 30, 390, 170, z + 30, DARK, lux=10)
        for (dx, dz) in ((-26, -26), (26, -26), (0, 30)):
            R.tube((360, 120, z), (360 + dx, 0, z + dz), 3, METAL, sides=5, coll=False, lux=20)
    bigfan(R, 640, 940, -500, radius=110)
    ceil_light(R, 600, -460, 960, size=96, power=120, rng=1300)
    ceil_light(R, 740, 120, 960, size=96, power=110, rng=1300)
    ceil_light(R, 740, 640, 960, size=96, power=120, rng=1300)
    named(R, 'STAGEIN', 330, 0, 0)
    reserve(R, 'SHADE', 2)
    # the remote observation lab, up the lift: a booth looking down on the stage
    out = [(-192, -760), (-192, -120), (250, -120), (250, -760)]
    BW = wmat('ez', 340).but(v0=UP + 340)
    R.walls(out, UP, UP + 340, BW, holes={0: [(164.0, 356.0, UP, UP + 320)], 2: [(80.0, 580.0, 730.0, 950.0)]})
    R.rect_floor(-192, -760, 250, -120, UP, TILE)
    R.rect_ceil(-192, -760, 250, -120, UP + 340, EZCEIL)
    reveals(R, 'z', 250, 256, -700, -200, 730, 950, DARK)
    glass_quad(R, (253, -700), (253, -200), 730, 950)
    btop = desk(R, 170, -700, 244, -200, UP, h=22)
    for z in (-600.0, -300.0):
        workstation(R, 195, btop, z, 270)
        chair(R, 90, z, 'E', y=UP)
    t = shelf_unit(R, -100, -756, 120, -712, UP, height=220, levels=4)
    for k, x in enumerate((-80, -40, 0, 40, 80)):
        tbox(R, x, t[1], -748, x + 30, t[1] + 18, -722, TAPEM)
    neon5(R, 'applause', 30, -120, 'S', 150, 92, UP + 240)
    ceil_light(R, 30, -440, UP + 340, size=56, power=70, rng=700, color=(230, 240, 255))
    lamps(R, NS3, 384, power=84)
    item(R, 'doc024', 190, btop, -450)
    item(R, 'bat', 0, t[2], -734, 70)
    return (R, 'GS', 'Sound Stage 024 (Indev). SCP-024, the game show, and the observation lab above it. Losers never leave.',
            4, 0.55, ((300, 165, -200), (750, 200, 500)))


def room2mailbox():
    R = R_('room2mailbox', amb=8)
    junction(R, 'NS', 'std', openings={'hubE': [door_op(0)]})
    x0, z0, x1, z1 = annex(R, 'x', 192, +1, -900, 900, 744, 384, 'yard', door=0)
    plate5(R, 'prop1269', 192, 0, 'W', yc=352, w=220)
    label5(R, '1269', 192, 250, 'W')
    HF, HE, HZ, HC = 470.0, 990.0, 700.0, 330.0         # house front, back, half length, ceiling
    # the street, the curb, the lawn
    R.box(330, 0, z0, 345, 8, z1, CONC, skip='BNS', lux=10)
    R.rect_floor(345, z0, HF, z1, 0.5, LAWN, coll=False, lux=12)
    R.rect_floor(HF, -900, x1, -HZ, 0.5, LAWN, coll=False, lux=12)
    R.rect_floor(HF, HZ, x1, 900, 0.5, LAWN, coll=False, lux=12)
    # the house: siding outside, wallpaper in
    HW = wmat('house', HC)
    front = [(-70.0, 70.0, 0.0, 260.0), (-280.0, -120.0, 110.0, 240.0), (400.0, 560.0, 110.0, 240.0)]
    wall_facing(R, (HF, -HZ), (HF, HZ), 0, 384, SIDING, 'W', holes=front)
    wall_facing(R, (HF + 12, -HZ + 12), (HF + 12, HZ - 12), 0, HC, HW, 'E', holes=front)
    for (c0, c1, y0, y1) in front:
        reveals(R, 'z', HF, HF + 12, c0, c1, y0, y1, WOOD)
        if y0 > 0:
            glass_quad(R, (HF + 6, c0), (HF + 6, c1), y0, y1)
    for (zs, fo, fi) in ((HZ, 'N', 'S'), (-HZ, 'S', 'N')):
        wall_facing(R, (HF, zs), (x1, zs), 0, 384, SIDING, fo)
        wall_facing(R, (HF + 12, zs - (12 if zs > 0 else -12)), (HE, zs - (12 if zs > 0 else -12)), 0, HC, HW, fi)
    wall_facing(R, (HE, -HZ), (HE, HZ), 0, HC, HW, 'W')
    R.rect_floor(HF + 12, -HZ + 12, HE, HZ - 12, 0.8, WOOD, coll=False, lux=12)
    R.rect_ceil(HF + 12, -HZ + 12, HE, HZ - 12, HC, WHITE)
    # partitions: bathroom (south), kitchen (north), the bedroom behind a locked door (east)
    both_faces(R, (HF + 12, -310), (HE, -310), 0, HC, HW, ('N', 'S'), holes=[(600.0, 730.0, 0.0, 260.0)], mat2=TILE, t=6)
    reveals(R, 'x', -316, -304, 600, 730, 0, 260, WOOD)
    both_faces(R, (HF + 12, 310), (HE, 310), 0, HC, HW, ('S', 'N'), holes=[(560.0, 690.0, 0.0, 260.0)], t=6)
    reveals(R, 'x', 304, 316, 560, 690, 0, 260, WOOD)
    both_faces(R, (770, -304), (770, 304), 0, HC, HW, ('W', 'E'), holes=[(-96.0, 96.0, 0.0, 320.0)], t=6)
    ndoor(R, 'BED', 770, 0, 0, 90, locked=True)
    named(R, 'KNOCK', 760, 150, 0)
    R.box(800, 0, 120, 980, 46, 296, WOOD, skip='B', top=FUTON, lux=10)
    # living room
    R.box(690, 0, -220, 760, 44, 140, VINYL, skip='B', lux=10)
    R.box(740, 44, -220, 760, 110, 140, VINYL, lux=10)
    R.box(HF + 14, 0, 140, HF + 60, 70, 260, WOOD, skip='B', lux=10)
    R.box(HF + 20, 70, 160, HF + 50, 140, 240, DARK, lux=10)
    flat(R, 540, -200, 680, 160, 1.0, CARPET.but(us=96), bottom='W', lux=14)
    pendant(R, 620, -40, HC, power=70, rng=640, color=(255, 226, 180))
    # bathroom: the shower and its curtain
    R.box(860, 0, -HZ + 12, HE, 10, -540, WHITE, skip='B', lux=10)
    for (p, q, f) in (((870, -HZ + 12), (870, -540), 'W'), ((871, -HZ + 12), (871, -540), 'E')):
        wall_facing(R, p, q, 30, 270, SHOWERC, f, coll=(f == 'W'))
    R.tube((870, 272, -HZ + 12), (870, 272, -540), 2.5, CHROME, sides=6, lux=20)
    R.box(HF + 14, 0, -500, HF + 70, 50, -440, WHITE, skip='B', lux=10)
    R.box(HF + 14, 0, -360, HF + 60, 80, -320, WHITE, skip='B', lux=10)
    ceil_light(R, 700, -500, HC, size=40, power=56, rng=560, color=(240, 244, 255))
    # kitchen
    R.box(HF + 14, 0, HZ - 60, 900, 90, HZ - 12, WOOD, skip='B', top=METAL, lux=10)
    R.box(920, 0, 600, HE, 200, HZ - 12, WHITE, skip='B', lux=10)
    tt = table(R, 600, 440, 700, 520, top=WOODT)
    chair(R, 650, 400, 'N')
    chair(R, 650, 560, 'S')
    ceil_light(R, 700, 500, HC, size=44, power=64, rng=600, color=(255, 236, 206))
    ceil_light(R, 620, -40, HC, size=36, power=40, rng=520, color=(255, 226, 180))
    ceil_light(R, 880, 0, HC, size=28, power=26, rng=420, color=(200, 210, 240))
    named(R, 'RES', 560, 0, 600)
    # the yard: a street lamp, the dumpster, the bags, the mailboxes that were replaced
    R.tube((300, 0, -600), (300, 340, -600), 6, DIRTY, sides=8, lux=16)
    R.box(296, 334, -604, 350, 346, -590, DARK, lux=10)
    R.box(300, 326, -606, 344, 333, -594, LIGHTPANEL.but(emit=230), lux=8, cast=False)
    R.light(322, 300, -600, rng=900, color=(255, 196, 120), power=90, radius=10)
    R.light(700, 370, 800, rng=900, color=(110, 130, 200), power=40, ent=False)
    R.light(700, 370, -800, rng=900, color=(110, 130, 200), power=40, ent=False)
    R.box(290, 0, 740, 440, 130, 880, GREENP, skip='B', top=DARK, lux=10)
    for (bx, bz, br) in ((500, 800, 26), (560, 846, 22), (520, 862, 18)):
        ball(R, (bx, br * 0.8, bz), br, DARK, seg=7, rings=3, lux=18)
    for k, (mx, mz) in enumerate(((620, 760), (690, 800), (640, 850))):
        R.box(mx, 0, mz - 34, mx + 22, 24, mz + 34, DARK, skip='B', lux=10)
        flat(R, mx + 1, mz - 32, mx + 21, mz + 32, 24.6, PROPS5, PR5['painted'], bottom='W')
    # where SCP-1269 can be: at the curb, at the window, behind the curtain, in a doorway, in the corners
    for i, (mx, mz) in enumerate(((395.0, -470.0), (430.0, -200.0), (935.0, -615.0), (708.0, 340.0), (745.0, 268.0),
                                  (895.0, 560.0), (430.0, 480.0))):
        named(R, 'MS%d' % i, mx, 0, mz)
    reserve(R, 'MBOX')
    reserve(R, 'MFLAG')
    lamps(R, NS3, 384, power=80)
    item(R, 'doc1269', 290, 0, -360)
    item(R, 'firstaid', 860, 90, HZ - 36, 50)
    return (R, 'MB', 'Property 1269 (Indev). A street, a lawn and a house rebuilt inside the zone. SCP-1269 stands at the curb. It moves.',
            4, 0.2, ((290, 165, -820), (520, 140, -250)))


def room2realchar():
    R = R_('room2realchar')
    AW = wmat('std', 384)
    junction(R, 'NS', 'std', openings={'hubE': [door_op(0)], 'hubW': [door_op(0)]})
    lift(R, -192, -1, 0, 0, 0, D, AW)
    x0, z0, x1, z1 = annex(R, 'x', 192, +1, -560, 560, 640, 384, 'studio', door=0)
    plate5(R, 'rci', 192, 0, 'W', yc=352, w=250)
    plate5(R, 'labs', -192, 0, 'E', yc=352, w=220)
    sign_at(R, 'elevator', -192, -250, 'E', 150, 50, 250)
    label5(R, '3325', -192, 250, 'E')
    # the studio: the painted set, a stage, a puppet booth, cameras, ON AIR
    wall_decal(R, BACKDROP, x1, 0, 'W', 900, 380, 192)
    R.box(620, 0, -420, x1 - 2, 30, 420, Mat('indev_canopy.png', 64), skip='B', top=STAGEF, lux=10)
    R.box(700, 30, -330, 800, 200, -170, Mat('indev_curtain.png', 64, 170, 200), skip='B', top=DARK, lux=10)
    named(R, 'BOOTH', 750, 0, -340)
    for z in (-220.0, 220.0):
        R.box(400, 120, z - 30, 460, 170, z + 30, DARK, lux=10)
        for (dx, dz) in ((-26, -26), (26, -26), (0, 30)):
            R.tube((430, 120, z), (430 + dx, 0, z + dz), 3, METAL, sides=5, coll=False, lux=20)
    prop5(R, 'poster3325', 560, z1, 'S', 150, 150, 200)
    plate5(R, 'onair', 560, z0, 'N', yc=300, w=150)
    top = table(R, 300, 380, 420, 480)
    chair(R, 360, 330, 'N')
    for (x, z) in ((420.0, -300.0), (420.0, 300.0), (700.0, 0.0)):
        ceil_light(R, x, z, 384, size=72, power=118, rng=900, color=(255, 246, 226))
    # LG-1, down the lift
    LX = 920.0
    out = [(-192, -900), (-192, 900), (LX, 900), (LX, -900)]
    R.walls(out, D, D + 420, LABW, holes={0: [span(out[0], (-192, -96), (-192, 96)) + (D, D + 320)],
                                         2: [span(out[2], (LX, 480), (LX, 320)) + (D + 220, D + 380)]})
    R.rect_floor(-192, -900, LX, 900, D, TILE)
    R.rect_ceil(-192, -900, LX, 900, D + 420, DIRTY)
    wall_fan(R, 'x', LX, +1, 400, D + 300)
    # growth tubes (one broken), feed lines
    for i, (x, z) in enumerate(((150.0, 520.0), (350.0, 520.0), (550.0, 520.0), (250.0, 760.0), (450.0, 760.0))):
        tube_tank(R, x, z, D)
        named(R, 'TUBE%d' % i, x, D + 130, z)
    tube_tank(R, 650, 760, D, broken=True)
    reserve(R, 'SPEC', 5)
    wall_decal(R, PROPS5, 150, 452, 'S', 70, 35, D + 150, uv=PR5['specimen'])
    red_lamp(R, 650, 640, D + 420, power=80, rng=700)
    # the bullet-resistant chamber
    CH = (40.0, -900.0, 460.0, -560.0)
    for xw in (CH[0], CH[2]):
        both_faces(R, (xw, CH[1]), (xw, CH[3]), D, D + 360, LABW.but(vs=360, v0=D + 360), ('E', 'W'), t=6)
    R.rect_ceil(CH[0], CH[1], CH[2], CH[3], D + 360, DARK)
    for (a, b) in ((CH[0], 154.0), (346.0, CH[2])):
        glass_quad(R, (a, CH[3]), (b, CH[3]), D, D + 360)
    glass_quad(R, (154, CH[3]), (346, CH[3]), D + 320, D + 360)
    R.box(CH[0], D + 360, CH[1], CH[2], D + 372, CH[3] + 6, DARK, lux=10)
    ndoor(R, 'CHAMBER', 250, D, -560, 0)
    plate5(R, 'cham', 250, -560, 'N', yc=D + 390, w=230)
    R.box(500, D, -600, 530, D + 170, -570, DARK, skip='B', lux=10)
    wall_decal(R, CTRL, 500, -585, 'W', 30, 40, D + 140)
    named(R, 'PANEL', 496, D + 140, -585)
    named(R, 'CHSPOT', 250, D, -760)
    # the pens: carcasses, straw, an open gate
    for xs in (666.0, 812.0):
        mesh_panel(R, (xs, -900), (xs, -560), D, D + 220)
    for (a, b) in ((520.0, 560.0), (650.0, 900.0)):
        mesh_panel(R, (a, -560), (b, -560), D, D + 220)
    mesh_panel(R, (520, -900), (520, -560), D, D + 220)
    plate5(R, 'pens', 710, -560, 'N', yc=D + 260, w=200)
    for (a, b) in ((520.0, 666.0), (666.0, 812.0), (812.0, LX)):
        R.rect_floor(a + 4, -896, b - 4, -564, D + 0.6, STRAW, coll=False, lux=12)
    for (bx, bz, br) in ((600.0, -740.0, 40.0), (740.0, -800.0, 34.0), (870.0, -720.0, 44.0)):
        ball(R, (bx, D + br * 0.5, bz), br, FLESH, seg=7, rings=3, lux=18)
    named(R, 'MEAT', 600, D + 30, -720)
    # steel containers along the east wall
    for z in (-420.0, -320.0, -220.0, -120.0, 120.0, 220.0):
        R.tube((LX - 40, D, z), (LX - 40, D + 110, z), 32, METAL.but(us=100, vs=110), sides=10, caps=True, lux=16)
    named(R, 'CRE', 640, D, 620)
    reserve(R, 'CREM')
    reserve(R, 'CREJ')
    reserve(R, 'CREC')
    reserve(R, 'MEATM')
    for (x, z) in ((150, 0), (450, 0), (750, 0), (300, -400), (700, 400)):
        ceil_light(R, x, z, D + 420, size=64, power=84, rng=820, color=(226, 240, 236))
    lamps(R, NS3, 384, power=80)
    item(R, 'doc3325', -100, D, -300)
    item(R, 'doc3325b', 330, top, 430)
    item(R, 'doc3325c', 750, 30, -360)
    return (R, 'RCI', 'Real Characters Industries (Indev). A children\'s TV set, and a lift down to LG-1, where SCP-3325-1 are grown. One is loose.',
            4, 0.4, ((-60, D + 165, -350), (450, D + 130, 520)))


ALL = [room2subway052, room2hall99, room2gameshow, room2diner, room2sheet, room2block15, room2mailbox, room2psych,
       room2realchar, room2wait1440]
