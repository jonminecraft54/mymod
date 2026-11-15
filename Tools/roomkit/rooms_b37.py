"""The thirty-seventh batch: SCP-028, the heavy water reactor, the deep archive, and two rooms remade from the
user's reference images 132-138. Code in IndevU37.bb; textures from make_assets37.py; notes from make_docs37.py.
Baked light only (small fixtures, red pendants, blue pool light); lightmaps capped at 512 (gen_b37.LM_MAX), coarse
luxels; the moving parts (archive shelves, pool water) are cheap runtime cubes and quads.

  room1scp028      LCZ  "Knowledge": the white shutter corridor (ref. 134/137), the guard post outside SCP-028
                        and a supply room (ref. 132: white shelves, benches, the red poster, the SCP banner, a camera);
                        through the east door the abandoned storage yard in still fog - and the sealed concrete room
                        built round the place where SCP-028 is
  room2b39reactor  HCZ  the reactor control room, decontamination; the east door opens on a gantry over the heavy
                        water pool, a bridge to the crane console, and a service lift down to the pool-floor walkway
                        where the sealed tray holds SCP-006-B
  room2b39archive  EZ   the reading room and the document store; the east door opens on the deep archive: twelve
                        ceiling-high motorised shelves that move (IndevU37.bb)
  room2b39hall     LCZ  ref. 133/136: a tall white hall with a railed balcony, offices with windows on the balcony,
                        red pendants, stairs and a staff lift between the floors; a supply room and a cell off the hub
  room2b39cells    LCZ  ref. 134/137: the shutter corridor; ref. 135/138: cells with a toilet, two sinks and a cot;
                        through the east door D-block, a second shutter corridor with three open cells
Everything is checked as before (no overlapping solids, doorways and aisles clear)."""
from rooms_b36 import *
from v02kit import lift
import random

YARD = Mat('indev_b37yard.png', 512)
LEAVES = Mat('indev_b37leaves.png', alpha=True, cast=False)
POSTER = Mat('indev_b37poster.png', cast=False)
REACT = Mat('indev_b37reactor.png', 256)
FILES = Mat('indev_b37files.png', 256)
PLASTER = Mat('indev_b37plaster.png', 256)
LIFTP = Mat('indev_b37lift.png', cast=False)
POOLB = Mat('indev_b37water.png', 128, emit=160)
WHITE = Mat('white.jpg', 128)
STYLES['plaster37'] = (PLASTER, TILE96, DARK)
STYLES['react37'] = (REACT, GRATE, DARK)


# ------------------------------------------------------------------------------------------------ reusable pieces
def cell_dress(R, xb, z0, z1, s, tag):
    """ref. 138: a cell's back wall at x = xb (s = +1 when the back wall is east): a toilet in the near corner, two
    sinks along the back wall, a steel cot along the far side wall."""
    xi = lambda d: xb - s * d                                                     # d units in from the back wall
    lo = lambda a, b: (min(xi(a), xi(b)), max(xi(a), xi(b)))
    # toilet: tank against the back wall, the bowl in front of it
    xa, xc = lo(0, 26)
    sbox(R, xa, 40, z0 + 20, xc, 112, z0 + 90, WHITE, 'toilet tank %s' % tag)
    xa, xc = lo(26, 86)
    sbox(R, xa, 0, z0 + 30, xc, 44, z0 + 80, WHITE, 'toilet bowl %s' % tag)
    R.box(xa, 44, z0 + 28, xc, 48, z0 + 82, Mat('dirtymetal.jpg', 64), lux=10)
    # two sinks on poles
    short = z1 - z0 < 400
    for k, zc in enumerate((z0 + 150,) if short else (z0 + 150, z0 + 260)):
        xa, xc = lo(0, 56)
        sbox(R, xa, 78, zc - 40, xc, 96, zc + 40, WHITE, 'sink %d %s' % (k, tag))
        R.tube((xi(30), 0, zc), (xi(30), 78, zc), 3, DARK, sides=6, caps=True)
        R.tube((xi(4), 96, zc), (xi(14), 108, zc), 1.5, METAL, sides=6, caps=True)
    xa, xc = lo(0, 2)
    R.box(xa, 120, z0 + 100, xc, 132, z0 + (200 if short else 310), DARK, lux=10)   # the dark trim strip (ref. 138)
    # the cot: steel frame, a stained mattress
    xa, xc = lo(30, 210 if short else 236)
    sbox(R, xa, 0, z1 - 104, xc, 62, z1 - 10, Mat('dirtymetal.jpg', 64), 'cot %s' % tag, skip='B')
    R.box(xa + 6, 62, z1 - 98, xc - 6, 72, z1 - 16, Mat('indev_b37plaster.png', 64), lux=10)


def cell_light(R, x, z, ceil):
    R.light(x, ceil - 40, z, rng=560, color=(240, 240, 235), power=58)
    R.box(x - 20, ceil - 4, z - 6, x + 20, ceil, z + 6, METAL, bottom=LIGHTPANEL, lux=10)


def passage(R, key, x1=256, mat=None):
    hall(R, 192, -96, x1, 96, 0, 320, mat or CONC36.but(vs=320, v0=320), FLOOR36, DARK,
         holes={'W': [(-96, 96, 0, 320)], 'E': [(-96, 96, 0, 320)]})
    R.spawns.append(dict(kind='door', pos=(224, 0, 0), angle=90, key=key))


def shutter_hub(R, west, east):
    for z in west:
        shutter(R, -192, z, 'E', w=150, h=240)
    for z in east:
        shutter(R, 192, z, 'W', w=150, h=240)


def supply_room(R, c, tag):
    """ref. 132: white shelves along the walls, benches in the middle, the red poster, the SCP banner, a camera"""
    for (z0, z1) in ((c - 290, c - 120), (c + 120, c + 290)):
        shelf_unit(R, -770, z0, -700, z1, 'shelf %s %d' % (tag, z0))
    shelf_unit(R, -640, c + 230, -470, c + 296, 'shelf back %s' % tag)
    bench30(R, -560, c - 60, -420, c - 20, 'bench a %s' % tag)
    bench30(R, -560, c + 40, -420, c + 80, 'bench b %s' % tag)
    decal30(R, POSTER, -340, c + 300, 'S', 110, 110, 190, 'poster %s' % tag)
    decal30(R, LOGO35, -776, c, 'E', 150, 150, 230, 'banner %s' % tag)
    named(R, 'CAM' + tag, -290, 300, c - 280)
    red_pendant(R, -516, c, 352, drop=60, power=36, rng=480)


# the big west room (one door at W 0): x -996..-256, z -980..980, 420 high
XW, XE, ZB, HW = -996.0, -256.0, 980.0, 420.0


def supply_hall(R, tag, north=True):
    """ref. 132, full size: white shelf rows along the walls and down the room, benches, the red poster, the SCP
    banner, a camera; the middle by the door stays clear"""
    rows = [(-940, -620), (-560, -240)] + ([(240, 560), (620, 940)] if north else [])
    for (z0, z1) in rows:
        shelf_unit(R, XW + 6, z0, XW + 76, z1, 'wall shelf %s %d' % (tag, z0))
        shelf_unit(R, -760, z0, -690, z1, 'row shelf %s %d' % (tag, z0))
    bench30(R, -560, -300, -420, -260, 'bench a %s' % tag)
    bench30(R, -560, -200, -420, -160, 'bench b %s' % tag)
    decal30(R, POSTER, -420, -ZB, 'N', 130, 130, 200, 'poster %s' % tag)
    decal30(R, LOGO35, XW, 0, 'E', 180, 180, 250, 'banner %s' % tag)
    named(R, 'CAM' + tag, -290, 340, -940)
    for z in (-700, -250, 250, 700):
        red_pendant(R, -600, z, HW, drop=70, power=46, rng=620)
    if north:
        return


# ------------------------------------------------------------------------------------------------ SCP-028
def room1scp028():
    R, rooms = wing33('room1scp028', 'ref96', {('W', 0): {'style': 'ref96', 'span': 980, 'depth': 740, 'h': 420}},
                      extra=[('E', 0)], amb=12)
    R.luxel = 16.0
    B = R.book
    hub_dress(R, 'ref96', [], pipes=False)
    shutter_hub(R, (-350, 350), (-350, 350))
    for z in (-600, 0, 600):
        red_pendant(R, 0, z, 384, drop=60, power=40, rng=560)
    # the west hall: the supply store (ref. 132) and, in the north end, the guard post outside SCP-028
    supply_hall(R, 'S', north=False)
    office_desk(R, -620, 500, -500, 620, 'E', 'post desk', chair=(-465, 560))
    office_desk(R, -620, 760, -500, 880, 'E', 'post desk 2', chair=(-465, 820))
    lockers(R, 'x', XW, 1, 300, 900)
    solid(R, (XW, 0, 300, XW + 30, 300, 900), 'post lockers')
    cabinets(R, -880, ZB - 50, -700, ZB, 'post cabinets')
    item(R, 'docb37_028', -580, 76, 540)
    item(R, 'radio', -580, 76, 800, chance=50)
    item(R, 'gasmask', -490, 44, -280, chance=50)
    item(R, 'bat', -490, 44, -180, chance=60)
    # ---------------- the east door: the abandoned storage yard
    passage(R, 3)
    H = 620.0
    R.walls([(256, -1000), (256, 1000), (1000, 1000), (1000, -1000)], 0, H, CONC36.but(us=512, vs=H, v0=H),
            holes={0: [(904, 1096, 0, 320)]})
    B.areas.append((256, 1000, -1000, 1000, H, 0))
    for (x0, z0, x1, z1) in ((256, -1000, 384, 1000), (384, -1000, 936, -276), (384, 276, 936, 1000), (936, -1000, 1000, 1000)):
        R.rect_floor(x0, z0, x1, z1, 0, YARD)
    # the sealed concrete room round SCP-028: walls 16 thick, a doorway in the west wall, a flat roof
    R.walls([(400, -260), (400, 260), (920, 260), (920, -260)], 0, 400, CONC36.but(vs=400, v0=400),
            holes={0: [(160, 360, 0, 260)]})
    R.walls([(384, -276), (936, -276), (936, 276), (384, 276)], 0, 401, CONC36.but(vs=401, v0=401),
            holes={3: [(176, 376, 0, 260)]})
    R.rect_floor(400, -260, 920, 260, 0, YARD)
    R.rect_ceil(400, -260, 920, 260, 400, CONC36)
    for zz in (-100, 100):
        R.wall((384, zz), (400, zz), 0, 260, CONC36)
        R.wall((400, zz), (384, zz), 0, 260, CONC36)
    R.box(384, 260, -100, 400, 401, 100, CONC36, lux=12)
    R.box(384, 401, -276, 936, 416, 276, CONC36, lux=12)
    for (box, n) in (((384, 0, -276, 400, 416, -100), 'west wall S'), ((384, 0, 100, 400, 416, 276), 'west wall N'),
                     ((400, 0, -276, 936, 416, -260), 'south wall'), ((400, 0, 260, 936, 416, 276), 'north wall'),
                     ((920, 0, -260, 936, 416, 260), 'east wall')):
        solid(R, box, n)
    warn(R, 1, 384, 180, 'W', 200, 'authorised only', s=70)
    decal30(R, LOGO35, 384, -180, 'W', 70, 70, 200, 'yard sign')
    named(R, 'CENTRE', 660, 0, 0)
    named(R, 'SEAL', 392, 140, 0)
    R.light(660, 330, 0, rng=560, color=(250, 245, 235), power=60)                 # one bare bulb
    R.box(656, 360, -4, 664, 400, 4, METAL, lux=10)
    # the yard: dead leaves, crates, drums, a dead tree, all in still fog
    rnd = random.Random(28)
    spots = []
    while len(spots) < 40:
        x, z = rnd.uniform(350, 910), rnd.uniform(-910, 910)
        if 274 < x < 1006 and -366 < z < 366:
            continue
        spots.append((x, z))
        s = rnd.uniform(40, 90)
        R.rect_floor(x - s, z - s, x + s, z + s, 0.6 + 0.05 * (len(spots) % 5), LEAVES)
    for k, (x0, z0) in enumerate(((820, -900), (880, -720), (300, 700), (760, 820))):
        sbox(R, x0, 0, z0, x0 + 90, 90, z0 + 90, CRATE35, 'crate %d' % k)
    sbox(R, 820, 90, -880, 890, 150, -830, CRATE35, 'crate top')
    for k, (x, z) in enumerate(((560, -760), (620, -820), (520, 820), (940, 420))):
        R.prism(octo(x, z, 28, 10), 0, 92, Mat('dirtymetal.jpg', 64), caps='T')
        solid(R, (x - 28, 0, z - 28, x + 28, 92, z + 28), 'drum %d' % k)
    R.tube((450, 0, -560), (452, 420, -556), 12, BARK867, sides=8, caps=True)
    for (dx, dy, dz) in ((90, 360, 40), (-60, 330, -80), (40, 400, -90)):
        R.tube((451, 280, -558), (451 + dx, dy + 60, -558 + dz), 4, BARK867, sides=6, caps=True)
    solid(R, (436, 0, -572, 466, 420, -542), 'dead tree')
    R.light(640, 560, 0, rng=2000, color=(170, 172, 176), power=130)                # overcast daylight
    for (x, z) in ((420, -700), (850, -600), (420, 700), (850, 650)):
        R.light(x, 420, z, rng=900, color=(160, 162, 166), power=60)
    B.clear = [((270, 0, -100, 360, 200, 100), 'yard approach'), ((440, 0, -90, 880, 200, 90), 'the room itself')]
    check33(R)
    return (R, 'K28', 'SCP-028 (Light Containment): the white shutter corridor, the guard post, a supply room - and through the east door, an abandoned storage yard in still fog and the sealed room round SCP-028.',
            1, 0.4, ((0, 165, -650), (300, 160, 0)))


# ------------------------------------------------------------------------------------------------ reactor
def room2b39reactor():
    YB = -768.0
    R, rooms = wing33('room2b39reactor', 'react37', {('W', 0): {'style': 'conc36', 'span': 980, 'depth': 740, 'h': 420}},
                      extra=[('E', 0)], amb=5)
    R.luxel = 16.0
    B = R.book
    hub_dress(R, 'react37', [], pipes=False)
    pipes_along(R, -180, -990, -520, (330, 352), (PIPE, PIPE), 'pipes W south', r=7)
    pipes_along(R, -180, 520, 990, (330, 352), (PIPE, PIPE), 'pipes W north', r=7)
    for z in (-560, 0, 560):
        ceiling_fixture(R, 0, z, 384, power=44, rng=560)
    red_emergency(R, 192, 300, -600, 'W', 'red hub E')
    red_emergency(R, -192, 300, 0, 'E', 'red hub W')
    warn(R, 1, 192, 600, 'W', 200, 'warn authorised')
    # W -400: the reactor control room
    for z in (-800, -600, -400):
        console30(R, XW + 46, z, 'E', 'reactor console %d' % z)
    decal30(R, FEEDS36, XW, -600, 'E', 420, 220, 260, 'control feeds')
    for z in (-760, -460):
        office_desk(R, -700, z, -580, z + 100, 'W', 'shift desk %d' % z, chair=(-545, z + 50))
    item(R, 'docb37_reactor', -650, 76, -720)
    for z in (-800, -350):
        red_pendant(R, -600, z, HW, drop=70, power=40, rng=600)
    # the north half: decontamination - shower heads over drains, lockers, the suit rack
    for z in (300, 500, 700):
        R.tube((-760, HW, z), (-760, 300, z), 3, METAL, sides=6, caps=True)
        R.prism(octo(-760, z, 14, 4), 292, 300, METAL, caps='TB')
    R.rect_floor(-840, 220, -680, 780, 0.6, GRATE)
    lockers(R, 'x', XW, 1, 300, 900)
    solid(R, (XW, 0, 300, XW + 30, 300, 900), 'decon lockers')
    bench30(R, -560, 600, -420, 650, 'decon bench')
    item(R, 'hazmatsuit', -600, 60, 400, chance=70)
    warn(R, 2, -500, ZB, 'S', 220, 'warn decon')
    for z in (350, 750):
        cell_light(R, -600, z, HW)
    # ---------------- the reactor hall: gantry at y 0, the pool, the pool-floor walkway at YB
    passage(R, 3, mat=REACT.but(vs=320, v0=320))
    hall(R, 256, -1000, 1000, 1000, YB, 400 - YB, REACT.but(vs=1168, v0=1168), Mat('concretefloor.jpg', 256), DARK,
         holes={'W': [(-96, 96, 0, 320)]})
    B.areas.append((256, 1000, -1000, 1000, 400, YB))
    sbox(R, 256, -16, -1000, 520, 0, 400, GRATE, 'gantry', skip='')
    sbox(R, 256, -16, 400, 380, 0, 1000, GRATE, 'gantry lift strip', skip='')
    rail_z(R, 516, -996, -64, 0, 'gantry rail S')
    rail_z(R, 516, 64, 380, 0, 'gantry rail N')
    rail_x(R, 396, 384, 512, 0, 'gantry rail lift')
    # the bridge over the pool to the crane console
    sbox(R, 520, -16, -60, 880, 0, 60, GRATE, 'bridge', skip='')
    sbox(R, 880, -16, -160, 1000, 0, 160, GRATE, 'crane platform', skip='')
    rail_x(R, -56, 524, 876, 0, 'bridge rail S')
    rail_x(R, 56, 524, 876, 0, 'bridge rail N')
    rail_z(R, 884, -148, -64, 0, 'platform rail S')
    rail_z(R, 884, 64, 148, 0, 'platform rail N')
    rail_x(R, -156, 888, 996, 0, 'platform rail SS')
    rail_x(R, 156, 888, 996, 0, 'platform rail NN')
    console30(R, 960, 0, 'W', 'crane console')
    named(R, 'CRANE', 940, 90, 0)
    # the pool: glass to the walkway, the core, fuel rods, the north wall that hides the lift shaft
    glass_wall(R, (560, -1000), (560, 400), YB, -440)
    R.wall((1000, 400), (380, 400), YB, 400, REACT.but(vs=1168, v0=1168))
    R.rect_floor(560, -1000, 1000, 400, YB + 0.5, POOLB)
    R.prism(octo(780, -300, 90, 12), YB, -560, POOLB, caps='T')
    for k in range(10):
        a = k * 0.628
        x, z = 780 + 150 * __import__('math').cos(a), -300 + 150 * __import__('math').sin(a)
        R.tube((x, YB, z), (x, -600, z), 5, METAL, sides=6, caps=True)
    named(R, 'WATER', 780, -470, -300)
    named(R, 'POOL', 540, -200, -300)
    # the service lift: gantry stop at y 0, pool-floor stop at YB (both behind the wall x = 380, z 420..980)
    R.wall((380, 1000), (380, 400), 0, 400, REACT.but(vs=400, v0=400), holes=[(204, 396, 0, 320)])
    R.wall((380, 1000), (380, 400), YB, 0, REACT.but(vs=768, v0=0), holes=[(204, 396, YB, YB + 320)])
    solid(R, (380, YB, 400, 1000, 400, 1000), 'lift shaft')
    lift(R, 380, 1, 700, 0, 700, YB, REACT.but(vs=384, v0=384))
    decal30(R, LIFTP, 380, 500, 'W', 90, 90, 150, 'lift sign top')
    decal30(R, LIFTP, 380, 500, 'W', 90, 90, YB + 150, 'lift sign bottom')
    # the pool-floor walkway: the sealed tray with SCP-006-B
    table33(R, 280, -320, 400, -200, YB, 'sample tray')
    item(R, 'scp006b', 330, YB + 78, -260)
    named(R, 'TRAY', 340, YB + 90, -260)
    decal30(R, LOGO35, 256, -600, 'E', 90, 90, YB + 220, 'walkway sign')
    # light: the Cherenkov blue from the pool, dim fixtures, red emergency lamps
    for (x, z) in ((700, -800), (900, -500), (700, -100), (900, 200), (650, 250)):
        R.light(x, -520, z, rng=1100, color=(60, 150, 255), power=70)
    R.light(400, -560, -400, rng=700, color=(70, 150, 255), power=40)
    for z in (-700, -200, 300):
        ceiling_fixture(R, 400, z, 400, power=40, rng=700)
    for (x, y, z, f) in ((1000, 200, -900, 'W'), (256, 200, -900, 'E'), (256, YB + 260, 300, 'E')):
        red_emergency(R, x, y, z, f, 'red hall %d %d' % (y, z), power=30, rng=460)
    warn(R, 2, 256, -400, 'E', 200, 'warn radiation')
    B.clear = [((270, 0, -990, 500, 200, -70), 'gantry walk'), ((270, 0, 70, 370, 200, 990), 'gantry to the lift'),
               ((270, YB, -180, 370, YB + 200, 990), 'walkway')]
    check33(R)
    return (R, 'RCT', 'Heavy Water Reactor Core (Heavy Containment): the control room and decontamination; the gantry over the glowing pool, the crane bridge, and a slow service lift to the pool-floor walkway where SCP-006-B is kept.',
            2, 0.5, ((300, 160, -800), (900, -300, 300)))


# ------------------------------------------------------------------------------------------------ deep archive
def room2b39archive():
    R, rooms = wing33('room2b39archive', 'ez', {('W', -400): {'style': 'ez'}, ('W', 400): {'style': 'ez'}},
                      extra=[('E', 0)], amb=6)
    R.luxel = 16.0
    B = R.book
    hub_dress(R, 'ez', [], pipes=False)
    # W -400: the reading room
    office_desk(R, -700, -660, -580, -540, 'E', 'reading desk', chair=(-545, -600))
    office_desk(R, -700, -300, -580, -180, 'E', 'reading desk 2', chair=(-545, -240))
    cabinets(R, -500, -690, -300, -640, 'reading cabinets')
    item(R, 'docb37_archive', -640, 76, -560)
    pendant(R, -516, -400, 352, drop=60, power=40, rng=500)
    # W 400: the document store, after ref. 132
    supply_room(R, 400, 'A')
    item(R, 'key3', -490, 44, 460, chance=50)
    # ---------------- the deep archive (shelves are made at runtime by IndevU37.bb)
    passage(R, 2, mat=WALL96.but(vs=320, v0=320))
    H = 640.0
    hall(R, 256, -1000, 1000, 1000, 0, H, WALL96.but(vs=H, v0=H), Mat('concretefloor.jpg', 256), CEIL96,
         holes={'W': [(-96, 96, 0, 320)]})
    B.areas.append((256, 1000, -1000, 1000, H, 0))
    for x in (420, 820):                                                         # the floor tracks
        R.box(x - 6, 0, -990, x + 6, 2, 990, METAL, lux=10)
    named(R, 'SHELVES', 620, 0, 0)
    for z in (-800, -400, 0, 400, 800):
        ceiling_fixture(R, 620, z, H, power=40, rng=820)
    for (x, z) in ((300, -700), (300, 700), (960, 0)):
        R.light(x, 300, z, rng=600, color=(255, 240, 210), power=22)
    decal30(R, POSTER, 1000, -600, 'W', 120, 120, 200, 'archive poster')
    red_emergency(R, 256, 400, 700, 'E', 'red archive')
    check33(R)
    return (R, 'ARC', 'Deep Storage Archives (Entrance Zone): the reading room, the document store and the deep archive - twelve ceiling-high motorised shelves that shift on their own.',
            3, 0.5, ((0, 165, -650), (300, 200, -900)))


# ------------------------------------------------------------------------------------------------ balcony hall
def room2b39hall():
    YL = -416.0
    R, rooms = wing33('room2b39hall', 'ref96', {('W', 0): {'style': 'ref96', 'span': 980, 'depth': 740, 'h': 420, 'key': 2}},
                      extra=[('E', 0)], amb=7)
    R.luxel = 16.0
    B = R.book
    hub_dress(R, 'ref96', [], pipes=False)
    shutter_hub(R, (-350, 350), (-350, 350))
    for z in (-600, 0, 600):
        red_pendant(R, 0, z, 384, drop=60, power=40, rng=560)
    # the west hall: the supply store (ref. 132) and a holding cell in the north end (ref. 138)
    supply_hall(R, 'H', north=False)
    item(R, 'firstaid', -490, 44, -280, chance=70)
    cell_dress(R, XW, 300, 900, -1, 'W')
    R.wall((-640, 280), (XW, 280), 0, HW, PLASTER.but(vs=HW, v0=HW))
    R.wall((XW, 280), (-640, 280), 0, HW, PLASTER.but(vs=HW, v0=HW))
    R.wall((-640, ZB), (-640, 680), 0, HW, PLASTER.but(vs=HW, v0=HW))
    R.wall((-640, 680), (-640, ZB), 0, HW, PLASTER.but(vs=HW, v0=HW))
    R.wall((-640, 520), (-640, 280), 0, HW, PLASTER.but(vs=HW, v0=HW))
    R.wall((-640, 280), (-640, 520), 0, HW, PLASTER.but(vs=HW, v0=HW))
    solid(R, (XW, 0, 276, -640, HW, 284), 'cell wall S')
    solid(R, (-644, 0, 284, -636, HW, 520), 'cell front a')
    solid(R, (-644, 0, 680, -636, HW, ZB), 'cell front b')
    cell_light(R, -820, 600, HW)
    item(R, 'docb37_cells', XW + 26, 96, 450)
    # ---------------- the hall (ref. 133 / 136)
    passage(R, 0, mat=WALL96.but(vs=320, v0=320))
    H = 400.0
    hall(R, 256, -1000, 1000, 1000, YL, H - YL, WALL96.but(vs=H - YL, v0=H), TILE96, DARK,
         holes={'W': [(-96, 96, 0, 320)]})
    B.areas.append((256, 1000, -1000, 1000, H, YL))
    # the balcony: a strip in front of the lift, the west run, the north run in front of the offices
    sbox(R, 256, -16, -1000, 380, 0, -400, WHITE, 'balcony lift strip', skip='')
    sbox(R, 256, -16, -400, 440, 0, 700, WHITE, 'balcony west', skip='')
    sbox(R, 256, -16, 700, 1000, 0, 1000, WHITE, 'balcony north', skip='')
    rail_z(R, 436, -396, 696, 0, 'balcony rail W')
    rail_x(R, 704, 444, 876, 0, 'balcony rail N')
    # the stairs down from the north run
    n = 13
    for i in range(n):
        za, zb = 700 - 32 * (i + 1), 700 - 32 * i
        top = YL * (i + 1) / n
        sbox(R, 880, max(top - 22, YL), za, 980, top, zb, CHECKER, 'step %d' % i)
    R.tube((876, 100, 700), (876, YL + 100, 700 - 32 * n), 3.5, METAL, sides=6, caps=True)
    solid(R, (872, YL, 700 - 32 * n, 878, 104, 700), 'stair rail')
    # the offices on the balcony: a front wall with two doors and two windows
    holesA = [(600, 700, 0, 260), (400, 550, 90, 240), (250, 350, 0, 260), (40, 200, 90, 240)]
    R.wall((1000, 794), (256, 794), 0, H, WALL96.but(vs=H, v0=H), holes=holesA)
    R.wall((256, 806), (1000, 806), 0, H, WALL96.but(vs=H, v0=H),
           holes=[(744 - b, 744 - a, y0, y1) for (a, b, y0, y1) in holesA])
    R.rect_ceil(256, 806, 1000, 1000, 300, DARK)
    for (a, b) in ((450, 600), (800, 960)):
        glass_wall(R, (a, 800), (b, 800), 90, 240)
        R.box(a, 86, 792, b, 90, 808, METAL, lux=10)
        R.box(a, 240, 792, b, 244, 808, METAL, lux=10)
    for (box, nm) in (((256, 0, 794, 300, H, 806), 'front a'), ((400, 0, 794, 650, H, 806), 'front b'),
                      ((750, 0, 794, 1000, H, 806), 'front c')):
        solid(R, box, nm)
    R.wall((620, 806), (620, 1000), 0, 300, WALL96.but(vs=300, v0=300))
    R.wall((620, 1000), (620, 806), 0, 300, WALL96.but(vs=300, v0=300))
    solid(R, (618, 0, 806, 622, 300, 1000), 'office partition')
    office_desk(R, 440, 880, 580, 980, 'S', 'office desk A', chair=(510, 835))
    office_desk(R, 760, 880, 900, 980, 'S', 'office desk B', chair=(830, 835))
    cabinets(R, 270, 940, 400, 990, 'office cabinets A')
    item(R, 'docb37_hall', 480, 76, 940)
    item(R, 'key2', 820, 76, 950, chance=50)
    ceil_light(R, 440, 900, 300, size=36, power=34, rng=480)
    ceil_light(R, 810, 900, 300, size=36, power=34, rng=480)
    # the staff lift between the floors, at the south end
    R.wall((380, -400), (380, -1000), 0, H, WALL96.but(vs=H, v0=H), holes=[(204, 396, 0, 320)])
    R.wall((380, -400), (380, -1000), YL, 0, WALL96.but(vs=-YL, v0=0), holes=[(204, 396, YL, YL + 320)])
    R.wall((380, -400), (1000, -400), YL, H, WALL96.but(vs=H - YL, v0=H))
    solid(R, (380, YL, -1000, 1000, H, -400), 'lift block')
    lift(R, 380, 1, -700, 0, -700, YL, WALL96.but(vs=384, v0=384))
    # the lower floor: vents, a bench, the red pendants (ref. 136)
    for z in (-200, 200):
        decal30(R, DARK, 1000, z, 'W', 60, 50, YL + 220, 'vent %d' % z)
    bench30_y(R, 940, -300, 990, -100, YL, 'hall bench')
    for (x, z) in ((700, -200), (700, 250)):
        red_pendant(R, x, z, H, drop=80, power=80, rng=900)
    for (x, z) in ((330, -300), (330, 300)):
        R.light(x, YL + 260, z, rng=640, color=(255, 240, 220), power=48)       # under the balcony
    named(R, 'DCLASS', 930, YL, -50)
    named(R, 'GUARD', 700, YL, -360)
    B.clear = [((268, 0, -390, 420, 200, 690), 'balcony walk'), ((268, 0, 712, 860, 200, 780), 'balcony north walk'),
               ((268, YL, -390, 420, YL + 200, 690), 'under the balcony')]
    check33(R)
    return (R, 'HAL', 'Balcony Hall (Light Containment): a tall white hall with a railed balcony, offices on the balcony, red pendants, stairs and a staff lift between the floors; a supply room and a cell off the shutter corridor.',
            1, 0.6, ((300, 160, -300), (700, -200, 600)))


def bench30_y(R, x0, z0, x1, z1, y, name):
    sbox(R, x0, y, z0, x1, y + 44, z1, WOOD, name, skip='B')


# ------------------------------------------------------------------------------------------------ cells
def room2b39cells():
    R, rooms = wing33('room2b39cells', 'ref96', {('W', 0): {'style': 'plaster37', 'span': 980, 'depth': 740, 'h': 420}},
                      extra=[('E', 0)], amb=6)
    R.luxel = 16.0
    B = R.book
    hub_dress(R, 'ref96', [], pipes=False)
    shutter_hub(R, (-350, 350), (-350, 350))
    for z in (-600, 0, 600):
        red_pendant(R, 0, z, 384, drop=60, power=40, rng=560)
    # the west ward: four cells (ref. 138) behind a front wall with open doorways, an aisle by the hub door
    XF = -620.0
    for k, (z0, z1) in enumerate(((-ZB, -490), (-490, 0), (0, 490), (490, ZB))):
        zc = (z0 + z1) / 2
        cell_dress(R, XW, z0 + 10, z1 - 10, -1, 'C%d' % k)
        cell_light(R, -800, zc, HW)
        for (a, b) in ((z0 + 6, zc - 70), (zc + 70, z1 - 6)):
            R.wall((XF, b), (XF, a), 0, HW, PLASTER.but(vs=HW, v0=HW))
            R.wall((XF, a), (XF, b), 0, HW, PLASTER.but(vs=HW, v0=HW))
            solid(R, (XF - 4, 0, a, XF + 4, HW, b), 'ward front %d %d' % (k, a))
        R.box(XF - 4, 260, zc - 70, XF + 4, HW, zc + 70, PLASTER, lux=12)
    for z in (-490, 0, 490):
        R.wall((XW, z), (XF, z), 0, HW, PLASTER.but(vs=HW, v0=HW))
        R.wall((XF, z), (XW, z), 0, HW, PLASTER.but(vs=HW, v0=HW))
        solid(R, (XW, 0, z - 4, XF - 4, HW, z + 4), 'ward partition %d' % z)
    for z in (-700, -250, 250, 700):
        red_pendant(R, -440, z, HW, drop=70, power=44, rng=620)
    item(R, 'docb37_cells', XW + 26, 96, -820)
    # ---------------- D-block: a cross corridor to a second shutter corridor with cells off it
    passage(R, 2, mat=WALL96.but(vs=320, v0=320))                         # the door sits in a short doorway
    hall(R, 256, -160, 540, 160, 0, 320, WALL96.but(vs=320, v0=320), TILE96, CEIL96,
         holes={'W': [(-96, 96, 0, 320)], 'E': [(-160, 160, 0, 320)]})        # then a wider cross corridor
    B.areas.append((256, 540, -160, 160, 320, 0))
    hall(R, 540, -1000, 720, 1000, 0, 320, WALL96.but(vs=320, v0=320), TILE96, CEIL96,
         holes={'W': [(-160, 160, 0, 320), (390, 510, 0, 240)], 'E': [(-610, -490, 0, 240), (490, 610, 0, 240)]})
    B.areas.append((192, 256, -96, 96, 320, 0))
    B.areas.append((540, 720, -1000, 1000, 320, 0))
    for (x0, x1, z0, z1, side, tag, back, s) in ((256, 540, 300, 600, 'E', 'D1', 256, -1), (720, 1000, -700, -400, 'W', 'D2', 1000, 1),
                                                (720, 1000, 400, 700, 'W', 'D6', 1000, 1)):
        zc = (z0 + z1) / 2
        hall(R, x0, z0, x1, z1, 0, 280, PLASTER.but(vs=280, v0=280), TILE96, DARK, holes={side: [(zc - 60, zc + 60, 0, 240)]})
        B.areas.append((x0, x1, z0, z1, 280, 0))
        cell_dress(R, back, z0, z1, s, tag)
        cell_light(R, (x0 + x1) / 2, zc, 280)
    for z in (-800, -250, 760):
        shutter(R, 540, z, 'E', w=140, h=240)
    for z in (-880, -200, 150, 860):
        shutter(R, 720, z, 'W', w=140, h=240)
    named(R, 'KNOCK', 712, 120, 150)
    named(R, 'VENT6', 990, 200, 550)
    named(R, 'DCELL', 420, 0, 340)
    for z in (-700, -250, 250, 700):
        red_pendant(R, 630, z, 320, drop=50, power=34, rng=480)
    item(R, 'key2', 930, 70, 640, chance=40)
    B.clear = [((550, 0, -990, 710, 200, 990), 'D-block corridor'), ((260, 0, -90, 530, 200, 90), 'cross corridor')]
    check33(R)
    return (R, 'CEL', 'Cell Block (Light Containment): the shutter corridor, two cells with a toilet, sinks and a cot, and D-block through the east door - a second shutter corridor with three open cells. Cell 6 is out of use.',
            1, 0.6, ((0, 165, -650), (630, 160, -800)))


ALL = [room1scp028, room2b39reactor, room2b39archive, room2b39hall, room2b39cells]
