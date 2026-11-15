"""The thirty-sixth batch: two more underground rooms, five candy SCPs and SCP-1479's taiga. Code in IndevU36.bb;
textures from make_assets36.py (1024 concrete and industrial floor, 512 panels, grime and warning decals), models from
make_hd36.py. After the user's reference images 115-131 and their brief: dim baked light, small ceiling fixtures,
red emergency lamps, dark corners, reusable materials, efficient geometry, no clean sci-fi.

  room2b36confect  HCZ  Confectionery Anomalies: the service corridor (ref. 121: the red stencilled SCP, pipe bundles,
                        dropped concrete beams); the observation room (ref. 124: a desk of binders at a long window
                        onto two sealed cells - SCP-1921's kiosk in a cage, SCP-3409-A's chocolate fungus); the
                        surveillance room (ref. 126: a monitor wall, consoles, red shades); and through the east door,
                        down from a mezzanine, vehicle bay 3 (ref. 122): a transport truck on the lane markings, the
                        bay door, high windows, the delivery table with SCP-1200, SCP-1916 and SCP-3147
  room2b36taiga    LCZ  the coal plant's basement (pipes, panels, a high-voltage room); the investigators' office and
                        the cold-weather store; and the east door - the empty utility room that is SCP-1479: a night
                        taiga in fog, black pines, grave crosses, a lone cabin with a lantern (ref. 131), and eyes
Everything is checked as before (no overlaps, doorways and aisles clear)."""
from rooms_b33 import *
from rooms_b32 import rail_x, rail_z

YL = -256.0
CONC36 = Mat('indev_b36conc.png', 512)
FLOOR36 = Mat('indev_b36floor.png', 512)
PANEL36 = Mat('indev_b36panel.png', 256)
SCPST = Mat('indev_b36scp.png', alpha=True, cast=False)
GRIME = Mat('indev_b36grime.png', alpha=True, cast=False)
WARN = Mat('indev_b36warn.png', cast=False)
FEEDS36 = Mat('indev_b36feeds.png', cast=False)
ROAD = Mat('indev_b36road.png', 256)
CROSS = Mat('indev_b36cross.png', cast=False)
BAYDOOR = Mat('indev_b36bay.png', cast=False)
FOREST = Mat('indev_b36forest.png', cast=False, emit=120)
SKY36 = Mat('indev_b36sky.png', 512, cast=False)
GROUND = Mat('indev_b36ground.png', 256)
NEEDLE = Mat('indev_b36needle.png', 96)
CHOC = Mat('indev_b36choc.png', 96)
CRATE35 = Mat('indev_b35crate.png', 96)
CONSP = Mat('indev_b34console.png', cast=False)
LOGO35 = Mat('indev_b35logo.png', cast=False)
GWIN = Mat('indev_gatev_window.png', cast=False)
PIPE = Mat('Pipes.jpg', 128)
STYLES['conc36'] = (CONC36, FLOOR36, CONC36)


# ------------------------------------------------------------------------------------------------ reusable pieces
def red_emergency(R, x, y, z, facing, name, power=22, rng=320):
    """a small caged red emergency lamp on a wall (the same piece everywhere); a dim red baked light"""
    nx, nz = {'E': (1, 0), 'W': (-1, 0), 'N': (0, 1), 'S': (0, -1)}[facing]
    cx, cz = x + nx * 6, z + nz * 6
    R.box(cx - 7, y - 9, cz - 7, cx + 7, y + 9, cz + 7, Mat('red.jpg', 32), lux=10)
    for dy in (-11, 11):                                                         # the wire cage, top and bottom
        R.box(cx - 8, y + dy - 1, cz - 8, cx + 8, y + dy + 1, cz + 8, METAL, lux=10)
    R.light(x + nx * 24, y, z + nz * 24, rng=rng, color=(255, 40, 30), power=power)


def ceiling_fixture(R, x, z, ceil, power=30, rng=420):
    """a small square ceiling fixture: a dim light, nothing more"""
    R.box(x - 14, ceil - 6, z - 14, x + 14, ceil, z + 14, METAL, bottom=LIGHTPANEL, lux=10)
    R.light(x, ceil - 24, z, rng=rng, color=(255, 240, 220), power=power)


def pipes_along(R, x, z0, z1, ys, mats, name, r=6):
    """a horizontal bundle of pipes along a wall (x), each with its own material, recorded as one solid"""
    for y, m in zip(ys, mats):
        R.tube((x, y, z0), (x, y, z1), r, m, sides=8, caps=True)
    solid(R, (x - r, min(ys) - r, min(z0, z1), x + r, max(ys) + r, max(z0, z1)), name)


def grime_base(R, a, b, h=110):
    """dirt and damp up from the foot of a wall (a..b seen from the room). The decal quads are part of the room's
    collision, so a wall with doorways is dressed in pieces (grime_hub) - never across a door."""
    R.decal(a, b, 0, h, GRIME, (0, 0, 2, 1), off=0.6)
    R.decal(b, a, 0, h, GRIME, (0, 0, 2, 1), off=0.6)


def grime_hub(R, h):
    """grime along both corridor walls, in pieces between the doorways (W doors at z -400 / 400, E door at 0)"""
    for (z0, z1) in ((-990, -500), (-300, 300), (500, 990)):
        grime_base(R, (-192, z0), (-192, z1), h)
    for (z0, z1) in ((-990, -100), (100, 990)):
        grime_base(R, (192, z1), (192, z0), h)


def warn(R, k, cx, cz, facing, yc, name, s=60):
    u0, v0 = (k % 2) * 0.5, (k // 2) * 0.5
    decal30(R, WARN, cx, cz, facing, s, s, yc, name, uv=(u0, v0, u0 + 0.5, v0 + 0.5))


# ------------------------------------------------------------------------------------------------ confectionery
def room2b36confect():
    R, rooms = wing33('room2b36confect', 'conc36', {('W', -400): {'style': 'cell30'}, ('W', 400): {'style': 'conc36'}},
                      extra=[('E', 0)], amb=5)
    R.luxel = 14.0                                                               # coarse, cheap lightmaps
    B = R.book
    hub_dress(R, 'conc36', [], pipes=False)
    # ref. 121: the service corridor - dropped beams, pipe bundles, the red stencil, grime, red emergency lamps
    for z in (-760, 760):
        sbox(R, -192, 300, z - 40, 192, 384, z + 40, CONC36.but(us=256), 'dropped beam %d' % z)
    pipes_along(R, 180, -716, -140, (330, 350, 368), (Mat('indev_b33shade.png', 64), PANEL36, PIPE), 'pipes E south')
    pipes_along(R, 180, 140, 716, (330, 350, 368), (Mat('indev_b33shade.png', 64), PANEL36, PIPE), 'pipes E north')
    for z in (850, 880, 910):                                                    # vertical risers by the north end
        R.tube((178, 0, z), (178, 300, z), 6, (PIPE, PANEL36, Mat('indev_b33shade.png', 64))[(z // 30) % 3], sides=8, caps=True)
    solid(R, (172, 0, 844, 186, 300, 916), 'risers')
    decal30(R, SCPST, -192, 700, 'E', 200, 100, 220, 'SCP stencil W')
    decal30(R, SCPST, 192, -700, 'W', 200, 100, 220, 'SCP stencil E')
    grime_hub(R, 110)
    for z in (-560, 0, 560):
        ceiling_fixture(R, 0, z, 384, power=46, rng=560)
    for z in (-900, 260):
        red_emergency(R, -192, 300, z, 'E', 'red hub W %d' % z)
    red_emergency(R, 192, 300, -260, 'W', 'red hub E')
    warn(R, 3, 192, 600, 'W', 200, 'warn sugar dust')
    # ---------------- the observation room (ref. 124): x -776..-256, z -700..-100
    for (x, f) in ((-566, -1), (-554, 1)):                                       # the window wall, both faces
        a, b = ((x, -700), (x, -100)) if f < 0 else ((x, -100), (x, -700))
        R.wall(a, b, 0, 352, CONC36.but(vs=352, v0=352), holes=[(40, 560, 90, 300)])
    R.box(-566, 86, -660, -554, 90, -140, METAL, lux=10)                          # sill, head, jambs
    R.box(-566, 300, -660, -554, 304, -140, METAL, lux=10)
    glass_wall(R, (-560, -660), (-560, -140), 90, 300)
    solid(R, (-566, 0, -700, -554, 352, -100), 'observation window wall')
    sbox(R, -776, 0, -410, -566, 352, -390, CONC36.but(us=128), 'cell partition')
    # cell 1: SCP-1921's kiosk inside a cage of bars (ref. 124), a lamp
    named(R, 'KIOSK', -680, 0, -555)
    for (x, z) in ((-760, -640), (-600, -640), (-600, -470), (-760, -470)):
        R.tube((x, 0, z), (x, 250, z), 2.5, DARK, sides=6, caps=True)
    for y in range(20, 251, 28):
        for (a, b) in (((-760, -640), (-600, -640)), ((-600, -640), (-600, -470)), ((-600, -470), (-760, -470))):
            R.tube((a[0], y, a[1]), (b[0], y, b[1]), 1.6, DARK, sides=6, caps=False)
    pendant(R, -680, -555, 352, drop=50, color=(255, 230, 190), power=45, rng=360)
    # cell 2: SCP-3409-A, the chocolate fungus over floor and walls, the glow of SCP-3409-B in the corner
    R.rect_floor(-776, -390, -566, -100, 1, CHOC)
    rnd = __import__('random').Random(3409)
    for k in range(26):
        x0, z0 = rnd.uniform(-760, -600), rnd.uniform(-380, -110)
        x1, z1 = x0 + rnd.uniform(-60, 60), z0 + rnd.uniform(-60, 60)
        y1 = rnd.choice((2, 2, 60, 140))
        R.tube((x0, 2, z0), (min(-580, max(-770, x1)), y1, min(-110, max(-380, z1))), rnd.uniform(2, 5), CHOC, sides=6, caps=True)
    R.prism(octo(-740, -140, 24, 10), 0, 120, Mat('indev_b33shade.png', 64), caps='T')
    R.light(-730, 150, -150, rng=380, color=(200, 90, 40), power=40)
    named(R, 'FUNGUS', -560, 160, -245)
    # the observer's side: the desk along the window, binders, a monitor, chairs, the sample hatch
    sbox(R, -548, 0, -660, -478, 76, -140, Mat('white.jpg', 128), 'observation desk', skip='B')
    for (z, m) in ((-600, DARK), (-570, DARK), (-450, Mat('red.jpg', 32)), (-260, DARK)):
        R.box(-540, 76, z - 10, -500, 104, z + 10, m, lux=10)
    model30(R, 'monitor.x', -520, 76, -190, 90, (40, 40, 26), 'observation monitor')
    model30(R, 'officeseat_a.x', -430, 0, -560, 270, (50, 100, 50), 'observation chair 1')
    model30(R, 'officeseat_a.x', -430, 0, -230, 270, (50, 100, 50), 'observation chair 2')
    R.box(-548, 76, -400, -520, 86, -370, METAL, lux=10)                          # the sample hatch
    named(R, 'HATCH', -530, 90, -385)
    item(R, 'docb36_1921', -510, 76, -620)
    item(R, 'docb36_3409', -510, 76, -330)
    pendant(R, -420, -400, 352, drop=60, color=(255, 220, 190), power=40, rng=500)
    # ---------------- the surveillance room (ref. 126): x -776..-256, z 100..700
    sbox(R, -776, 90, 170, -760, 330, 590, DARK, 'monitor wall backboard')
    decal30(R, FEEDS36, -760, 380, 'E', 400, 300, 210, 'monitor wall')
    named(R, 'FEEDS', -756, 210, 380)
    sbox(R, -620, 0, 300, -500, 90, 460, Mat('dirtymetal.jpg', 128), 'centre console', top=CONSP)
    sbox(R, -460, 0, 640, -300, 100, 700, Mat('dirtymetal.jpg', 128), 'rear console', top=CONSP)
    decal30(R, CONSP, -380, 700, 'S', 200, 100, 190, 'rear console panel')
    decal30(R, LOGO35, -560, 700, 'S', 80, 80, 260, 'SCP sign')
    model30(R, 'officeseat_a.x', -440, 0, 380, 90, (50, 100, 50), 'surveillance chair 1')
    model30(R, 'officeseat_a.x', -380, 0, 600, 180, (50, 100, 50), 'surveillance chair 2')
    for z in (300, 520):
        red_pendant(R, -560, z, 352, drop=70, power=30, rng=420)
    warn(R, 0, -680, 100, 'N', 220, 'warn high voltage')
    item(R, 'docb36_1200', -560, 90, 330)
    # ---------------- the east door, the mezzanine and the stairs down into vehicle bay 3 (ref. 122)
    hall(R, 192, -96, 256, 96, 0, 320, CONC36.but(vs=320, v0=320), FLOOR36, DARK, holes={'W': [(-96, 96, 0, 320)], 'E': [(-96, 96, 0, 320)]})
    R.spawns.append(dict(kind='door', pos=(224, 0, 0), angle=90, key=3))
    hall(R, 256, -1000, 960, 1000, YL, 352 - YL, CONC36.but(vs=608, v0=608), TILE96, DARK, holes={'W': [(-96, 96, 0, 320)]})
    B.areas.append((256, 960, -1000, 1000, 352, YL))
    sbox(R, 256, -16, -200, 440, 0, 200, CHECKER, 'mezzanine', skip='')
    rail_z(R, 436, -196, 196, 0, 'mezzanine rail E')
    rail_x(R, -196, 260, 426, 0, 'mezzanine rail S')
    rail_x(R, 204, 412, 432, 0, 'mezzanine rail N')
    for i in range(14):
        za, zb = 200 + 32 * i, 232 + 32 * i
        top = -256.0 * (i + 1) / 14
        sbox(R, 256, max(top - 22, YL), za, 400, top, zb, CHECKER, 'step %d' % i)
    R.tube((404, 82, 200), (404, YL + 100, 648), 3.5, YEL, sides=6, caps=True)
    solid(R, (400, YL, 200, 408, 104, 648), 'stair rail')
    # the bay floor: an asphalt lane with its markings and a hatched crossing, white tiles either side
    R.rect_floor(520, -1000, 780, 1000, YL + 0.5, ROAD)
    R.rect_floor(520, -520, 780, -440, YL + 0.8, CROSS)
    decal30(R, BAYDOOR, 650, 1000, 'S', 300, 300, YL + 150, 'bay door')
    named(R, 'BAYDOOR', 650, YL + 150, 990)
    for z in (-600, -200, 200, 600):                                             # the high windows of the control gallery
        decal30(R, GWIN, 960, z, 'W', 160, 90, 230, 'bay window %d' % z)
    named(R, 'TRUCK', 650, YL, 120)
    solid(R, (536, YL, -340, 764, YL + 220, 560), 'truck')
    # the delivery table with the candy, pallets of crates, a bench
    table33(R, 820, -900, 940, -780, YL, 'delivery table')
    item(R, 'gum1200', 850, YL + 78, -860)
    item(R, 'jar1916', 890, YL + 78, -830)
    item(R, 'pop3147', 920, YL + 78, -870)
    item(R, 'docb36_1916', 850, YL + 78, -800)
    item(R, 'docb36_3147', 900, YL + 78, -800)
    for zc in (-560, -380):
        sbox(R, 840, YL, zc - 60, 950, YL + 12, zc + 60, Mat('wood.jpg', 128), 'pallet %d' % zc)
        sbox(R, 846, YL + 12, zc - 56, 900, YL + 70, zc - 2, CRATE35, 'crate a %d' % zc)
        sbox(R, 846, YL + 12, zc + 2, 900, YL + 70, zc + 56, CRATE35, 'crate b %d' % zc)
        sbox(R, 904, YL + 12, zc - 40, 946, YL + 52, zc + 40, CRATE35, 'crate c %d' % zc)
    bench30_y(R, 280, 790, 330, 960, 'bay bench')
    for (a, b) in (((256, -1000), (960, -1000)), ((960, 1000), (256, 1000)), ((960, -1000), (960, 1000))):
        R.decal(a, b, YL, YL + 110, GRIME, (0, 0, 4, 1), off=0.6)
        R.decal(b, a, YL, YL + 110, GRIME, (0, 0, 4, 1), off=0.6)
    for z in (-700, 0, 700):
        ceiling_fixture(R, 650, z, 352, power=62, rng=760)
    for z in (-350, 350):
        R.light(470, YL + 220, z, rng=520, color=(255, 236, 210), power=34)
        R.light(860, YL + 220, z, rng=520, color=(255, 236, 210), power=34)
    for (x, z, f) in ((960, -900, 'W'), (960, 900, 'W'), (256, -800, 'E')):
        red_emergency(R, x, YL + 260, z, f, 'red bay %d' % z, power=30, rng=420)
    warn(R, 1, 960, -330, 'W', YL + 160, 'warn bay')
    R.light(330, 200, 0, rng=500, color=(255, 230, 200), power=30)
    B.clear = [((268, 0, -190, 424, 200, 190), 'mezzanine walk'), ((270, YL + 30, 660, 390, YL + 200, 760), 'stair foot'),
               ((420, YL, -990, 530, YL + 200, 990), 'west lane'), ((770, YL, -330, 830, YL + 200, 990), 'east lane')]
    check33(R)
    return (R, 'CON', 'Confectionery Anomalies (Heavy Containment): the red-stencilled service corridor, the observation room onto SCP-1921 and SCP-3409-A, the surveillance room, and vehicle bay 3 below with the candy deliveries (SCP-1200, SCP-1916, SCP-3147).',
            2, 0.35, ((0, 165, -650), (0, 150, 300)))


def bench30_y(R, x0, z0, x1, z1, name):
    sbox(R, x0, YL, z0, x1, YL + 44, z1, WOOD, name, skip='B')


# ------------------------------------------------------------------------------------------------ SCP-1479
def pine(R, x, z, h, name):
    R.tube((x, 0, z), (x, h * 0.35, z), 9, BARK867, sides=8, caps=False)
    for k in range(5):
        y0 = h * (0.25 + k * 0.15)
        r = 90 * (1 - k * 0.17)
        R.prism(octo(x, z, r, 9), y0, y0 + h * 0.12, NEEDLE, caps='B')
        R.prism(octo(x, z, r * 0.45, 9), y0 + h * 0.12, y0 + h * 0.2, NEEDLE, caps='T')
    solid(R, (x - 10, 0, z - 10, x + 10, h, z + 10), name)


def room2b36taiga():
    R, rooms = wing33('room2b36taiga', 'conc36', {('W', -400): {'style': 'conc36'}, ('W', 400): {'style': 'cell30'}},
                      extra=[('E', 0)], amb=5)
    R.luxel = 16.0
    B = R.book
    hub_dress(R, 'conc36', [], pipes=False)
    # the coal plant's basement: rusty pipe runs high on both walls, risers, electrical panels, grime, red lamps
    for x in (-180, 180):
        for (z0, z1) in ((-990, -560), (-240, -140), (140, 240), (560, 990)) if x < 0 else ((-990, -140), (140, 990)):
            pipes_along(R, x, z0, z1, (334, 356), (PIPE, PIPE), 'pipes %d %d' % (x, z0), r=7)
    decal30(R, Mat('ElecBox.jpg', cast=False), 192, -600, 'W', 150, 190, 170, 'panel S')
    decal30(R, Mat('ElecBox.jpg', cast=False), 192, 600, 'W', 150, 190, 170, 'panel N')
    warn(R, 0, 192, -760, 'W', 280, 'warn hv')
    grime_hub(R, 140)
    for z in (-560, 0, 560):
        ceiling_fixture(R, 0, z, 384, power=44, rng=560)
    red_emergency(R, -192, 300, 0, 'E', 'red basement W')
    red_emergency(R, 192, 300, 300, 'W', 'red basement E')
    # W -400: the investigators' office: a desk, a map board, ropes, lanterns, the camera that sees the walls
    office_desk(R, -700, -660, -580, -540, 'E', 'investigation desk', chair=(-545, -600))
    decal30(R, WB, -776, -330, 'E', 260, 130, 200, 'map board')
    table30(R, -560, -260, -400, -170, 'gear table')
    named(R, 'CAMERA', -480, 90, -215)
    item(R, 'docb36_1479', -640, 76, -560)
    for k in range(3):
        R.prism(octo(-740, -300 + k * 36, 16, 10), 0, 14, Mat('indev_867bark.png', 32), caps='T')    # coiled ropes
    solid(R, (-760, 0, -316, -720, 14, -212), 'ropes')
    pendant(R, -516, -400, 352, drop=60, color=(255, 220, 180), power=40, rng=520)
    # W 400: the cold-weather store: lockers, parkas, a bench
    lockers(R, 'x', -776, 1, 140, 660)
    solid(R, (-776, 0, 140, -746, 300, 660), 'store lockers')
    for z in (200, 300, 400, 500):
        sbox(R, -700, 120, z - 30, -660, 260, z + 30, YEL, 'parka %d' % z)
    bench30(R, -560, 300, -400, 350, 'store bench')
    item(R, 'key2', -480, 78, 325, chance=60)
    ceil_light(R, -516, 400, 352, size=36, power=36, rng=520)
    # ---------------- the east door: the empty utility room that holds 144 km2 of taiga
    hall(R, 192, -96, 256, 96, 0, 320, CONC36.but(vs=320, v0=320), FLOOR36, DARK, holes={'W': [(-96, 96, 0, 320)], 'E': [(-96, 96, 0, 320)]})
    R.spawns.append(dict(kind='door', pos=(224, 0, 0), angle=90, key=2))
    H = 900.0
    R.walls([(256, -1000), (256, 1000), (1000, 1000), (1000, -1000)], 0, H, FOREST.but(us=1024, vs=H, v0=H),
            holes={0: [(904, 1096, 0, 320)]})
    R.rect_floor(256, -1000, 1000, 1000, 0, GROUND)
    R.rect_ceil(256, -1000, 1000, 1000, H, SKY36)
    B.areas.append((256, 1000, -1000, 1000, H, 0))
    rnd = __import__('random').Random(1479)
    trees = []
    while len(trees) < 26:
        x, z = rnd.uniform(350, 905), rnd.uniform(-905, 905)
        if abs(z) < 140 and x < 520:
            continue                                                             # the clearing in front of the door
        if 440 < x < 920 and 200 < z < 700:
            continue                                                             # the cabin's ground
        if any((x - a) ** 2 + (z - b) ** 2 < 120 ** 2 for a, b in trees):
            continue
        trees.append((x, z))
    for k, (x, z) in enumerate(trees):
        pine(R, x, z, rnd.uniform(560, 860), 'pine %d' % k)
    for k, (x, z) in enumerate(trees[:6]):
        named(R, 'EYE%d' % k, x - 14, rnd.uniform(170, 260), z)
    named(R, 'CABIN', 700, 0, 450)
    solid(R, (450, 0, 225, 880, 470, 675), 'cabin')
    named(R, 'CABINDOOR', 470, 120, 450)
    R.light(470, 170, 470, rng=420, color=(255, 170, 80), power=45)                # the lantern
    for k, z in enumerate((760, 820, 880)):                                       # grave crosses
        sbox(R, 520 + k * 30, 0, z - 4, 528 + k * 30, 90, z + 4, WOOD, 'cross post %d' % k)
        R.box(506 + k * 30, 60, z - 3, 542 + k * 30, 68, z + 3, WOOD, lux=10)
    R.light(600, 700, 0, rng=2200, color=(110, 120, 140), power=70)              # the overcast night
    for (x, z) in ((450, -600), (800, -400), (450, 600), (800, 800), (650, 0)):
        R.light(x, 500, z, rng=900, color=(90, 100, 120), power=30)
    R.light(300, 200, 0, rng=380, color=(255, 220, 180), power=20)                # spill from the open door
    B.clear = [((270, 0, -120, 500, 200, 120), 'the clearing by the door')]
    check33(R)
    return (R, 'TGA', 'The coal plant basement and SCP-1479 (Light Containment): pipes, panels, the investigators\' office and the cold-weather store - and the empty utility room that holds a night taiga, a lone cabin with a lantern, and eyes.',
            1, 0.75, ((0, 165, -650), (0, 150, 300)))


ALL = [room2b36confect, room2b36taiga]
