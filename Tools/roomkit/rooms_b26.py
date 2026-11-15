"""The twenty-sixth batch: an unnamed outdoor expansion - an evergreen-forest surface reached by a lift from the
facility, and two indoor wings of new rooms. Code in IndevU26.bb. Textures from make_assets26.py (new or recoloured
SCP:CB textures); the "models" (trees, rocks, logs, booth, barrier, poles, car, shed, generator, terminals, vents,
cabinets, beds) are low-poly geometry baked into the rooms. No real place names anywhere.

  room2b26exit      EZ   Surface exit: a checkpoint lobby with a lift up. At the top (y = 1024) the surface:
                         a concrete exit hut, a security booth and barrier, fences and floodlights, a wet road with
                         an abandoned car and utility poles, a forest of evergreens with rocks and fallen logs,
                         a utility shed with a generator, and a tree line all round. Fog and rain while outside.
  room2b26labs      LCZ  Four rooms: forest research laboratory, abandoned medical ward, secure equipment storage,
                         damaged security control room.
  room2b26utility   HCZ  Three rooms: rainwater drainage chamber, underground utility station, forest observation
                         room (a big rain-streaked window onto the trees)."""
import math
import random
from rooms_b25 import *

MOSS = Mat('indev_o_moss.png', 384)
DAMP = Mat('indev_o_damp.png', 364)
RUST = Mat('indev_o_rust.png', 256)
MUD = Mat('indev_o_mud.png', 256)
GRASS = Mat('indev_o_grass.png', 256)
ASPH = Mat('indev_o_asphalt.png', 256)
ROAD = Mat('indev_o_road.png', 300)
BARK = Mat('indev_o_bark.png', 128)
NEEDLE = Mat('indev_o_needles.png', 128)
ROCK = Mat('indev_o_rock.png', 128)
FOREST = Mat('indev_o_forest.png', cast=False)
WINDOW = Mat('indev_o_window.png', cast=False)
STRIPES = Mat('indev_o_stripes.png', 64)
SIGN = Mat('indev_o_sign.png', cast=False)
SCREEN = Mat('indev_o_screen.png', cast=False)
BROKEN = Mat('indev_o_broken.png', cast=False)
PANEL = Mat('indev_o_panel.png', cast=False)
STYLES['moss26'] = (MOSS, CONC, DARK)
STYLES['damp26'] = (DAMP, TILE, EZCEIL)
Y = 1024.0                                                     # the surface level
RO = R_  # the room factory from the earlier batches


def tree(R, x, z, h, y=Y):
    """a low-poly evergreen: a trunk and four stacked tiers of needles"""
    R.tube((x, y, z), (x, y + h * 0.3, z), 10 + h * 0.012, BARK, sides=6, caps=False)
    r = h * 0.3
    for k in range(4):
        y0 = y + h * (0.22 + 0.19 * k)
        R.prism(octo(x, z, r * (1 - 0.22 * k), 6), y0, y0 + h * 0.2, NEEDLE, caps='TB')


def rock(R, x, z, s, y=Y):
    R.prism(octo(x, z, s, 5), y, y + s * 0.6, ROCK, caps='T')


def room2b26exit():
    R = Room('room2b26exit', luxel=22.0, ambient=44, fill=0.35)             # coarse: the surface is very large
    AW = Mat('indev_o_moss.png', 384).but(v0=0)
    junction(R, 'NS', 'moss26', hub=(-352, -512, 352, 512), hh=384, openings={'hubW': [door_op(0)]})
    lift(R, -352, -1, 0, 0, 0, Y, AW)
    sign_at(R, 'elevator', -352, -250, 'E', 150, 50, 250)
    wall_decal(R, SIGN, -352, 300, 'E', 220, 110, 250)
    R.box(200, 0, -440, 340, 110, -300, DARK, skip='B', top=PANELS, lux=10)      # the checkpoint desk, clear of the walk
    wall_decal(R, SCREEN, 352, -370, 'W', 90, 70, 170)
    named(R, 'TERMINAL', 330, 150, -370)
    ceil_light(R, 0, -300, 384, size=44, power=60, rng=700)
    ceil_light(R, 0, 300, 384, size=44, power=60, rng=700)
    item(R, 'doc26_exit', 270, 110, -400)

    # ---- the surface ----
    X0, X1, Z0, Z1 = -352.0, 3200.0, -2200.0, 2200.0
    # the exit hut round the top of the lift: walls, a roof, a doorway east
    hut = [(X0, -300), (X0, 300), (40, 300), (40, -300)]
    R.walls(hut, Y, Y + 400, MOSS, holes={0: [span(hut[0], (X0, -96), (X0, 96)) + (Y, Y + 320)],
                                         2: [span(hut[2], (40, 96), (40, -96)) + (Y, Y + 320)]})
    R.rect_floor(X0, -300, 40, 300, Y, CONC)
    R.rect_ceil(X0, -300, 40, 300, Y + 400, DARK)
    R.box(X0 - 10, Y + 400, -320, 60, Y + 420, 320, RUST, lux=10)                  # its roof, seen from outside
    # the ground: mud and grass, the road east-west through the middle, a gravel apron at the hut
    R.rect_floor(40, -300, 600, 300, Y, ASPH)
    R.rect_floor(600, -160, X1, 160, Y, ROAD)
    for z0, z1 in ((Z0, -300), (300, Z1)):
        R.rect_floor(X0 - 400, z0, X1, z1, Y, MUD)
    R.rect_floor(X0 - 400, -300, X0, 300, Y, GRASS)
    R.rect_floor(40, -300, 600, -160, Y, ASPH)
    R.rect_floor(600, -300, X1, -160, Y, GRASS)
    R.rect_floor(600, 160, X1, 300, Y, GRASS)
    R.rect_floor(40, 160, 600, 300, Y, ASPH)
    # the tree line all round: a tall wall of the forest picture, the edge of the map
    edge = [(X0 - 400, Z0), (X0 - 400, Z1), (X1, Z1), (X1, Z0)]
    R.walls(edge, Y, Y + 1100, FOREST.but(us=1100, vs=1100))
    # the checkpoint: a booth with a window, a barrier across the road, fences, floodlights, the sign
    R.box(700, Y, 200, 860, Y + 260, 340, DAMP, skip='B', lux=10)
    wall_decal(R, GLASS, 780, 200, 'N', 120, 70, Y + 170)
    R.box(690, Y + 260, 190, 870, Y + 276, 350, RUST, lux=10)
    named(R, 'BOOTH', 780, Y + 120, 180)
    R.box(880, Y + 90, -150, 900, Y + 104, 140, STRIPES, lux=10)                  # the barrier arm, raised a little
    R.tube((890, Y, 150), (890, Y + 104, 150), 10, RUST, sides=6, caps=True)
    for z in (-300, 300):
        R.box(900, Y, z - 4 if z > 0 else z - 2, 2400, Y + 220, z + 4 if z > 0 else z + 2, GRATE, lux=10)   # fences
    wall_decal(R, SIGN, 1100, -296, 'N', 220, 110, Y + 150)
    for x in (700, 1500, 2300):
        R.tube((x, Y, -340), (x, Y + 520, -340), 9, RUST, sides=6, caps=True)
        ceil_light(R, x, -300, Y + 500, size=30, power=110, rng=1100, color=(230, 236, 255))
    # utility poles along the road, an abandoned car
    for x in (1000, 1800, 2600):
        R.tube((x, Y, 200), (x, Y + 700, 200), 12, BARK, sides=6, caps=True)
        R.box(x - 70, Y + 640, 194, x + 70, Y + 652, 206, BARK, lux=10)
    R.box(1500, Y, -120, 1820, Y + 90, 30, RUST, skip='B', lux=10)                 # the car body
    R.box(1560, Y + 90, -110, 1740, Y + 160, 20, DARK, skip='B', lux=10)           # its cabin
    named(R, 'CAR', 1650, Y + 60, -140)
    # the utility shed with its generator
    shed = [(1800, 700), (1800, 1100), (2200, 1100), (2200, 700)]
    R.walls(shed, Y, Y + 300, MOSS, holes={0: [span(shed[0], (1800, 820), (1800, 980)) + (Y, Y + 260)]})
    R.rect_floor(1800, 700, 2200, 1100, Y + 2, CONC)
    R.rect_ceil(1800, 700, 2200, 1100, Y + 300, RUST)
    R.box(1790, Y + 300, 690, 2210, Y + 316, 1110, RUST, lux=10)
    R.box(1980, Y, 760, 2160, Y + 120, 900, METAL, skip='B', lux=10)              # the generator
    wall_decal(R, PANEL, 2200, 1000, 'W', 120, 120, Y + 150)
    named(R, 'GENERATOR', 1960, Y + 80, 830)
    ceil_light(R, 2000, 900, Y + 300, size=24, power=30, rng=500, color=(255, 210, 160))
    item(R, 'doc26_shed', 2100, Y + 120, 850)
    item(R, 'key3', 2050, Y + 2, 1050, chance=80)
    # the forest: trees, rocks and logs, kept off the road, the paths and the buildings
    rnd = random.Random(26)
    placed = 0
    while placed < 70:
        x, z = rnd.uniform(X0 - 300, X1 - 150), rnd.uniform(Z0 + 150, Z1 - 150)
        if abs(z) < 420 or (1700 < x < 2300 and 600 < z < 1200) or (x < 120 and abs(z) < 700):
            continue
        if 900 < x < 1300 and z > 0:                                              # a path north to a clearing
            continue
        tree(R, x, z, rnd.uniform(520, 900))
        placed += 1
    for _ in range(18):
        x, z = rnd.uniform(X0, X1), rnd.uniform(Z0 + 200, Z1 - 200)
        if abs(z) > 450:
            rock(R, x, z, rnd.uniform(30, 80))
    for x, z, a in ((600, -900, 0.4), (2500, 1500, 1.2), (1200, -1500, 2.0)):
        R.tube((x, Y + 24, z), (x + 300 * math.cos(a), Y + 24, z + 300 * math.sin(a)), 22, BARK, sides=6, caps=True)
    named(R, 'CLEARING', 1100, Y + 50, 1400)
    named(R, 'OUTSIDE', 600, Y + 100, 0)
    item(R, 'doc26_trail', 1100, Y, 1400)
    return (R, 'EXT', 'Surface exit (Entrance Zone): a checkpoint lobby and a lift up to the surface - a foggy evergreen forest, a road, a security booth and a utility shed.',
            3, 0.5, ((300, Y + 165, -100), (1500, Y + 200, -400)))


def wing26(name, style):
    R = RO(name, amb=8)
    junction(R, 'NS', style, hub=(-192, -704, 192, 704),
             openings={'hubE': [door_op(-400), door_op(400)], 'hubW': [door_op(-400), door_op(400)]})
    for s, c in CELLS:
        annex(R, 'x', 192 * s, s, c - 300, c + 300, 520, 352, style, door=c)
        ceil_light(R, 516 * s, c, 352, size=30, power=36, rng=520)
    for z in (-500, 0, 500):
        ceil_light(R, 0, z, 384, size=40, power=50, rng=700)
    return R


def room2b26labs():
    R = wing26('room2b26labs', 'damp26')
    # east south: forest research laboratory - benches, a terminal, sample cabinets, a fume vent
    R.box(560, 0, -680, 760, 90, -600, METAL, skip='B', top=METAL, lux=10)
    R.box(560, 0, -200, 760, 90, -120, METAL, skip='B', top=METAL, lux=10)
    wall_decal(R, SCREEN, 776, -400, 'W', 110, 80, 160)
    named(R, 'LABTERM', 760, 140, -400)
    R.box(700, 0, -560, 776, 220, -460, CABINET, skip='B', lux=10)
    R.box(600, 300, -440, 720, 352, -360, VENT, lux=10)
    item(R, 'doc26_lab', 640, 90, -640)
    # east north: abandoned medical ward - beds, an IV stand, debris
    for z in (180, 400, 620):
        R.box(620, 0, z - 50, 760, 50, z + 50, METAL, skip='B', lux=10)
        R.box(624, 50, z - 46, 756, 62, z + 46, WHITEP, skip='B', lux=10)
    R.tube((580, 0, 300), (580, 180, 300), 4, METAL, sides=6, caps=True)
    for k in range(6):
        R.box(400 + k * 40, 0, 500 + (k % 3) * 30, 430 + k * 40, 10 + k % 2 * 8, 520 + (k % 3) * 30, DAMP, lux=10)
    item(R, 'firstaid', 690, 62, 620)
    named(R, 'WARD', 600, 100, 400)
    # west south: secure equipment storage - cabinets, crates, a keycard reader
    for z in range(-680, -140, 110):
        R.box(-776, 0, z, -700, 220, z + 100, CABINET, skip='B', lux=10)
    R.box(-600, 0, -300, -480, 100, -180, Mat('wood.jpg', 512), skip='B', lux=10)
    R.box(-460, 0, -320, -360, 70, -220, Mat('wood.jpg', 512), skip='B', lux=10)
    wall_decal(R, STRIPES, -500, -700, 'S', 300, 20, 2)
    item(R, 'bat', -540, 100, -240)
    # west north: damaged security control room - consoles, cracked monitors, a red lamp, debris
    R.box(-776, 0, 150, -690, 110, 650, DARK, skip='B', top=PANELS, lux=10)
    for z in (250, 400, 550):
        wall_decal(R, BROKEN, -776, z, 'E', 110, 80, 200)
    named(R, 'SPARK', -700, 200, 400)
    red_lamp(R, -500, 400, 352)
    for k in range(5):
        R.box(-560 + k * 30, 0, 250 + k * 50, -530 + k * 30, 14, 280 + k * 50, RUST, lux=10)
    item(R, 'doc26_sec', -600, 0, 300)
    return (R, 'LAB', 'Research wing (Light Containment): a forest research laboratory, an abandoned medical ward, secure equipment storage and a damaged security control room.',
            1, 0.45, ((0, 165, -800), (500, 100, -400)))


def room2b26utility():
    R = wing26('room2b26utility', 'moss26')
    # east south: rainwater drainage chamber - a grated channel, pipes, the drip
    R.box(300, 0, -620, 760, 6, -560, GRATE, lux=10)
    R.box(300, 0, -240, 760, 6, -180, GRATE, lux=10)
    for z in (-600, -200):
        R.tube((300, 300, z), (760, 300, z), 18, RUST, sides=8, caps=True)
    R.tube((700, 0, -400), (700, 352, -400), 26, RUST, sides=8, caps=True)
    named(R, 'DRIP', 600, 50, -400)
    item(R, 'doc26_drain', 400, 0, -400)
    # east north: underground utility station - generators, electrical panels, a vent unit
    R.box(560, 0, 160, 740, 120, 300, METAL, skip='B', lux=10)
    R.box(560, 0, 480, 740, 120, 620, METAL, skip='B', lux=10)
    wall_decal(R, PANEL, 776, 400, 'W', 120, 120, 170)
    R.box(300, 260, 300, 420, 352, 500, VENT, lux=10)
    named(R, 'POWER', 760, 170, 400)
    # west south: forest observation room - a big rain-streaked window, two chairs, a desk
    wall_decal(R, WINDOW, -776, -400, 'E', 480, 240, 200)
    chair(R, -600, -480, 'W')
    chair(R, -600, -320, 'W')
    dtop = desk(R, -480, -460, -380, -340, 0)
    named(R, 'OBS', -760, 200, -400)
    item(R, 'doc26_obs', -430, dtop, -400)
    # west north: a store of rain gear and spare parts
    for z in range(160, 640, 120):
        R.box(-776, 0, z, -700, 200, z + 100, RUST, skip='B', lux=10)
    item(R, 'key2', -600, 0, 400, chance=70)
    return (R, 'UTL', 'Utility wing (Heavy Containment): a rainwater drainage chamber, an underground utility station and a forest observation room.',
            2, 0.45, ((0, 165, -800), (500, 100, -400)))


ALL = [room2b26exit, room2b26labs, room2b26utility]
