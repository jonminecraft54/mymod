"""The thirty-second batch: Gate V, the underground emergency exit. Code in IndevU32.bb; textures from
make_assets32.py, models from make_hd32.py, notes from make_docs32.py. Style after the user's reference images 80-87
(Gate A's skylit atrium with balconies and railings, Gate B's white hall with the gallery and the heavy gate door under
its black sign, the dark bulkhead corridor, the covered stair to the sky, the snowy mountains outside).

room2b32gatev (Entrance Zone), all inside one map cell, two levels:
  level 0      the corridor; the Gate V antechamber - white walls, a black ceiling, an observation gallery with
               dark windows, a checkpoint desk, and on the south wall the heavy GATE V door in a massive frame
               with a red band, its card reader and the break-glass emergency release
  the stair    behind the door, a stairwell 1024 deep: four flights of 14 steps, landings, yellow handrails, a
               central core, the stair eye, level markers and lamps
  level -1024  the bulkhead tunnel (steel frames every 220, a grating floor, pipes, the alarm breaker box), and
               the exit atrium: a skylight, a gallery with a railing and windows, the exit console, and in the
               west wall the open exit portal with its swung-back vault hatch - beyond it, snow and mountains

Every solid and picture is recorded and checked (no overlaps, nothing in a passage)."""
from rooms_b30 import *

Y0 = -1024.0
GSIGN = Mat('indev_gatev_sign.png', cast=False)
GEXIT = Mat('indev_gatev_exit.png', cast=False)
GWARN = Mat('indev_gatev_warn.png', cast=False)
GLEVELS = Mat('indev_gatev_levels.png', cast=False)
MOUNT = Mat('indev_gatev_mountains.png', cast=False, emit=200)
SKY = Mat('indev_gatev_sky.png', cast=False, emit=230)
BREAKER = Mat('indev_gatev_breaker.png', cast=False)
GLASSBOX = Mat('indev_gatev_glass.png', cast=False)
GCONS = Mat('indev_gatev_console.png', cast=False)
BAND = Mat('indev_gatev_band.png', 128)
GWIN = Mat('indev_gatev_window.png', cast=False)
SNOW = Mat('white.jpg', 256, emit=150)
WALLA = Mat('whitewall.jpg', 364, 352, 352)
STEEL = Mat('dirtymetal.jpg', 256)
STEP = Mat('scpcb_checkerplate.jpg', 128)


def frame_box(R, x0, y0, z0, x1, y1, z1, mat, name):
    sbox(R, x0, y0, z0, x1, y1, z1, mat, name)


def rail_x(R, z, x0, x1, y, name, step=110):
    """a yellow handrail along x at z (posts every `step`), from y"""
    x = x0
    while x <= x1 + 0.5:
        R.tube((x, y, z), (x, y + 100, z), 3, YEL, sides=6, caps=True)
        x += step
    R.tube((x0, y + 100, z), (x1, y + 100, z), 3.5, YEL, sides=6, caps=True)
    R.tube((x0, y + 55, z), (x1, y + 55, z), 2.5, YEL, sides=6, caps=True)
    solid(R, (x0 - 4, y, z - 4, x1 + 4, y + 104, z + 4), name)


def rail_z(R, x, z0, z1, y, name, step=110):
    z = z0
    while z <= z1 + 0.5:
        R.tube((x, y, z), (x, y + 100, z), 3, YEL, sides=6, caps=True)
        z += step
    R.tube((x, y + 100, z0), (x, y + 100, z1), 3.5, YEL, sides=6, caps=True)
    R.tube((x, y + 55, z0), (x, y + 55, z1), 2.5, YEL, sides=6, caps=True)
    solid(R, (x - 4, y, z0 - 4, x + 4, y + 104, z1 + 4), name)


def flight(R, x_start, direction, z0, z1, y_top, name, n=14, run=32.0, drop=256.0):
    """n steps along x from x_start (direction -1 or +1), going down from y_top by `drop`; a sloped rail on the
    open (z1) side"""
    for i in range(n):
        xa = x_start + direction * run * i
        xb = xa + direction * run
        top = y_top - drop * (i + 1) / n
        sbox(R, min(xa, xb), top - 22, z0, max(xa, xb), top, z1, STEP, '%s step %d' % (name, i))
    xe = x_start + direction * run * n
    R.tube((x_start, y_top - drop / n + 100, z1 - 4), (xe, y_top - drop + 100, z1 - 4), 3.5, YEL, sides=6, caps=True)
    for k in range(0, n + 1, 4):
        x = x_start + direction * run * k
        y = y_top - drop * k / n
        R.tube((x, y, z1 - 4), (x, y + 100, z1 - 4), 3, YEL, sides=6, caps=True)


def room2b32gatev():
    R = Room('room2b32gatev', luxel=9.0, ambient=10, fill=0.15)
    R.book = Book()
    junction(R, 'NS', 'ez', hub=(-192, -704, 192, 704), openings={'hubE': [door_op(0)]})
    for z in (-560, -180, 180, 560):
        pendant(R, 0, z, 384, power=55, rng=600)
    decal30(R, GEXIT, 192, -300, 'W', 180, 68, 300, 'hub exit sign S')
    decal30(R, GEXIT, 192, 300, 'W', 180, 68, 300, 'hub exit sign N')
    decal30(R, GSIGN, 192, 0, 'W', 180, 45, 352, 'hub gate sign')
    decal30(R, PR2, -192, 0, 'E', 100, 134, 190, 'hub poster')
    # the jamb and the door into the antechamber
    hall(R, 192, -96, 256, 96, 0, 320, WALLA, TILE, DARK, holes={'W': [(-96, 96, 0, 320)], 'E': [(-96, 96, 0, 320)]})
    R.spawns.append(dict(kind='door', pos=(224, 0, 0), angle=90, key=0))

    # ================= level 0: the Gate V antechamber (x 256..960, z -540..540, 560 high)
    hall(R, 256, -540, 960, 540, 0, 560, WALLA, TILE, DARK,
         holes={'W': [(-96, 96, 0, 320)], 'S': [(684, 876, 0, 320)]})
    for (x, z) in ((450, -300), (760, -300), (450, 180), (760, 180)):
        pendant(R, x, z, 560, drop=110, power=70, rng=700)
    for z in range(-500, 501, 250):                                                   # wall lamps under the band
        R.light(950, 300, z, rng=400, color=(255, 240, 220), power=25)
    # the heavy gate's frame (ref. 87): two pillars, a beam with the red band, the sign, hazard floor
    frame_box(R, 600, 0, -540, 684, 400, -512, STEEL, 'gate pillar W')
    frame_box(R, 876, 0, -540, 960, 400, -512, STEEL, 'gate pillar E')
    frame_box(R, 684, 320, -540, 876, 400, -512, STEEL, 'gate beam')
    decal30(R, BAND, 780, -512, 'N', 360, 30, 385, 'gate band')
    decal30(R, GSIGN, 780, -540, 'N', 380, 95, 470, 'GATE V sign')
    R.box(684, 0, -512, 876, 1, -420, Mat('indev_o_stripes.png', 64), lux=10)       # hazard floor in front
    for (x, z0, z1) in ((676, -556, -540), (876, -556, -540)):                        # jamb faces in the wall gap
        R.box(x, 0, z0, x + 8, 320, z1, STEEL, lux=10)
    R.box(676, 320, -556, 884, 330, -540, STEEL, lux=10)
    decal30(R, KEYPAD, 520, -540, 'N', 40, 60, 160, 'gate card reader')
    named(R, 'READER', 520, 160, -530)
    decal30(R, GLASSBOX, 430, -540, 'N', 70, 70, 150, 'break glass')
    named(R, 'GLASS', 430, 150, -530)
    decal30(R, GWARN, 330, -540, 'N', 130, 65, 250, 'gate warning')
    # the observation gallery along the north wall (ref. 86): deck, railing, columns, dark windows, a door
    sbox(R, 256, 300, 400, 960, 316, 540, CHECKER, 'gallery deck')
    rail_x(R, 404, 256, 960, 316, 'gallery rail')
    for x in (400, 650, 900):
        sbox(R, x - 12, 0, 404, x + 12, 300, 428, STEEL, 'gallery column %d' % x)
    for x in (480, 620, 760):
        decal30(R, GWIN, x, 540, 'S', 120, 90, 420, 'gallery window %d' % x)
    decal30(R, Mat('Door01.jpg', cast=False), 320, 540, 'S', 90, 200, 416, 'gallery door')
    # the checkpoint desk, an exit sign
    office_desk(R, 300, -420, 440, -300, 'N', 'checkpoint desk', chair=(370, -265))
    item(R, 'docgatev', 400, 76, -400)
    decal30(R, GEXIT, 960, -250, 'W', 200, 75, 300, 'antechamber exit sign')
    decal30(R, POSTER24, 960, 120, 'W', 80, 110, 170, 'antechamber poster')

    # ================= the stairwell (x 256..960, z -1000..-556, from Y0 up to 560)
    hall(R, 256, -1000, 960, -556, Y0, 0 - Y0 + 560, Mat('concretewall.jpg', 384), CONC, DARK,
         holes={'N': [(684, 876, 0, 320), (764, 956, Y0, Y0 + 300)]})
    sbox(R, 640, -16, -700, 960, 0, -556, CHECKER, 'top landing A', skip='')
    sbox(R, 840, -16, -1000, 960, 0, -700, CHECKER, 'top landing B', skip='')
    flight(R, 840, -1, -1000, -860, 0, 'flight 1')
    sbox(R, 256, -272, -1000, 392, -256, -700, CHECKER, 'landing 1')
    flight(R, 392, 1, -840, -700, -256, 'flight 2')
    sbox(R, 840, -528, -1000, 960, -512, -700, CHECKER, 'landing 2')
    flight(R, 840, -1, -1000, -860, -512, 'flight 3')
    sbox(R, 256, -784, -1000, 392, -768, -700, CHECKER, 'landing 3')
    flight(R, 392, 1, -840, -700, -768, 'flight 4', n=13, drop=256 * 13 / 14.0)
    sbox(R, 392, Y0, -860, 840, -16, -840, Mat('concretewall.jpg', 384), 'stair core')
    rail_x(R, -700, 640, 840, 0, 'top landing rail S')
    rail_z(R, 644, -692, -560, 0, 'top landing rail W')
    for (y, xs) in ((-256, (256, 392)), (-768, (256, 392)), (-512, (840, 960))):
        rail_x(R, -704, xs[0], xs[1], y, 'landing rail %d' % y)
    for k, y in enumerate((0, -256, -512, -768)):
        u0 = k * 0.25
        R.decal((960, -760), (960, -880), y + 150, y + 270, GLEVELS, (u0, 0, u0 + 0.25, 1), off=1.0)
        R.light(940, y + 230, -800, rng=520, color=(255, 236, 200), power=45)
        R.light(276, y + 230, -800, rng=420, color=(255, 236, 200), power=30)
    R.light(600, Y0 + 260, -640, rng=520, color=(255, 236, 200), power=40)
    R.decal((960, -590), (960, -690), Y0 + 220, Y0 + 290, GEXIT, (0, 0, 1, 1), off=1.0)

    # ================= level -1024: the bulkhead tunnel (x 760..960, z -556..760)
    TW = Mat('metalpanels2.jpg', 256)
    hall(R, 760, -556, 960, 760, Y0, 300, TW, GRATE, DARK,
         holes={'S': [(764, 956, Y0, Y0 + 300)], 'W': [(568, 752, Y0, Y0 + 300)]})
    for z in range(-440, 700, 220):                                                   # the bulkheads (ref. 85)
        frame_box(R, 760, Y0, z - 12, 790, Y0 + 300, z + 12, STEEL, 'bulkhead W %d' % z)
        frame_box(R, 930, Y0, z - 12, 960, Y0 + 300, z + 12, STEEL, 'bulkhead E %d' % z)
        frame_box(R, 790, Y0 + 262, z - 12, 930, Y0 + 300, z + 12, STEEL, 'bulkhead top %d' % z)
        for (x0, x1) in ((790, 812), (908, 930)):                                     # chamfered corners
            R.box(x0, Y0 + 240, z - 10, x1, Y0 + 262, z + 10, STEEL, lux=10)
    for z in range(-330, 700, 220):
        R.box(840, Y0 + 290, z - 30, 880, Y0 + 300, z + 30, METAL, bottom=LIGHTPANEL, lux=10)
        R.light(860, Y0 + 260, z, rng=360, color=(255, 214, 160), power=30)
    for y in (Y0 + 40, Y0 + 60):
        R.tube((945, y, -556), (945, y, 760), 6, Mat('Pipes.jpg', 128), sides=8, caps=False)
    decal30(R, BREAKER, 760, 100, 'E', 90, 135, Y0 + 150, 'alarm breaker')
    named(R, 'BREAKER', 770, Y0 + 150, 100)
    R.decal((960, 520), (960, 380), Y0 + 210, Y0 + 260, GEXIT, (0, 0, 1, 1), off=1.0)
    item(R, 'docgatev2', 900, Y0, -300)

    # ================= level -1024: the exit atrium (x -960..744, z 200..1000, 640 high)
    hall(R, -960, 200, 744, 1000, Y0, 640, WALLA, TILE, Mat('concrete.jpg', 256),
         holes={'E': [(568, 752, Y0, Y0 + 300)], 'W': [(520, 760, Y0, Y0 + 360)]})
    for (x0, z0, z1) in ((744, 560, 568), (744, 752, 760)):                           # the gap to the tunnel
        R.box(x0, Y0, z0, x0 + 16, Y0 + 300, z1, STEEL, lux=10)
    R.box(744, Y0 + 300, 560, 760, Y0 + 310, 760, STEEL, lux=10)
    # the skylight (ref. 81): a lit octagon of sky, radial beams, a ring
    cx, cz, rr = -180, 560, 260
    oct_ = octo(cx, cz, rr, 12)
    R.add([V(p[0], Y0 + 638, p[1]) for p in oct_], [((p[0] - cx) / (2 * rr) + 0.5, (p[1] - cz) / (2 * rr) + 0.5) for p in oct_], SKY)
    for i in range(12):
        a, b = oct_[i], oct_[(i + 1) % 12]
        R.tube((a[0], Y0 + 632, a[1]), (b[0], Y0 + 632, b[1]), 8, STEEL, sides=6, caps=True)
        R.tube((cx, Y0 + 632, cz), (a[0], Y0 + 632, a[1]), 5, STEEL, sides=6, caps=True)
    R.light(cx, Y0 + 560, cz, rng=1400, color=(240, 246, 255), power=140)
    # the gallery along the north wall, its railing, the windows above
    sbox(R, -960, Y0 + 300, 860, 744, Y0 + 316, 1000, CHECKER, 'atrium gallery deck')
    rail_x(R, 864, -960, 744, Y0 + 316, 'atrium gallery rail')
    for x in (-700, -300, 100, 500):
        sbox(R, x - 12, Y0, 864, x + 12, Y0 + 300, 888, STEEL, 'atrium column %d' % x)
        decal30(R, GWIN, x, 1000, 'S', 120, 90, Y0 + 430, 'atrium window %d' % x)
    for x in (-500, 300):
        decal30(R, VENT, x, 200, 'N', 90, 50, Y0 + 80, 'atrium vent %d' % x)
    # the exit portal (refs. 80, 83): the frame, GATE V over it, the hatch swung back, the light outside
    frame_box(R, -960, Y0, 488, -930, Y0 + 400, 520, STEEL, 'portal post S')
    frame_box(R, -960, Y0, 760, -930, Y0 + 400, 792, STEEL, 'portal post N')
    frame_box(R, -960, Y0 + 360, 520, -930, Y0 + 400, 760, STEEL, 'portal lintel')
    decal30(R, GSIGN, -960, 640, 'E', 420, 105, Y0 + 470, 'atrium GATE V sign')
    decal30(R, GEXIT, -960, 330, 'E', 180, 68, Y0 + 320, 'atrium exit sign')
    named(R, 'HATCH', -1193, Y0 + 202, 459)
    solid(R, (-952, Y0, 30, -782, Y0 + 404, 483), 'vault hatch')
    named(R, 'PORTAL', -940, Y0 + 20, 640)
    for k, z in enumerate((580, 640, 700)):
        named(R, 'MTF%d' % k, -930, Y0, z)
    console30(R, -920, 880, 'E', 'exit console')
    decal30(R, GCONS, -960, 880, 'E', 150, 100, Y0 + 260, 'exit console screen')
    named(R, 'CONSOLE', -900, Y0 + 120, 880)
    # outside: the snow, the mountains, the sky
    R.rect_floor(-1020, 300, -960, 980, Y0, SNOW)
    R.decal((-1020, 100), (-1020, 1000), Y0 - 160, Y0 + 520, MOUNT, (0, 0, 1, 1), off=0)        # 900 x 680: the picture's 4:3
    R.decal((-1020, 100), (-1020, 1000), Y0 + 520, Y0 + 900, SKY, (0, 0, 1, 0.4), off=0)
    R.decal((-960, 980), (-1020, 980), Y0, Y0 + 900, SKY, (0, 0, 1, 1), off=0)
    R.decal((-1020, 300), (-960, 300), Y0, Y0 + 900, SKY, (0, 0, 1, 1), off=0)
    R.rect_ceil(-1020, 300, -960, 980, Y0 + 900, SKY)
    R.light(-990, Y0 + 300, 640, rng=900, color=(255, 255, 255), power=120)
    for (x, z) in ((-600, 400), (-600, 800), (300, 400), (300, 760)):
        ceil_light(R, x, z, Y0 + 640, size=60, power=45, rng=700)
    check32(R)
    return (R, 'GV', 'Gate V (Entrance Zone): the underground emergency exit - the antechamber and its heavy gate, a 1024-deep stairwell, the bulkhead tunnel and the exit atrium with the open hatch to the mountains.',
            3, 0.75, ((300, 165, 300), (780, 200, -540)))


def check32(R):
    """overlaps between solids, and the passages that must stay clear (each as a box)"""
    B = R.book
    bad = []
    inter = lambda a, b, e=0.5: all(a[i] < b[i + 3] - e and b[i] < a[i + 3] - e for i in range(3))
    for i in range(len(B.solids)):
        for j in range(i + 1, len(B.solids)):
            if inter(B.solids[i][0], B.solids[j][0]):
                bad.append('solids overlap: %s / %s' % (B.solids[i][1], B.solids[j][1]))
    clear = [((82, 0, -110, 366, 320, 110), 'antechamber door'), ((684, 0, -660, 876, 320, -430), 'gate door'),
             ((764, Y0, -695, 956, Y0 + 280, -420), 'stair bottom to tunnel'),
             ((780, Y0, -400, 920, Y0 + 250, 750), 'tunnel walk'), ((-930, Y0, 540, 744, Y0 + 280, 740), 'atrium walk')]
    for box, name in B.solids:
        if 'bulkhead' in name:
            continue
        for c, cn in clear:
            if inter(box, c):
                bad.append('%s blocks the %s' % (name, cn))
    for i in range(len(B.decals)):
        a = B.decals[i]
        for j in range(i + 1, len(B.decals)):
            b = B.decals[j]
            if a[0] == b[0] and abs(a[1] - b[1]) < 3 and a[2] < b[3] and b[2] < a[3] and a[4] < b[5] and b[4] < a[5]:
                bad.append('pictures overlap: %s / %s' % (a[6], b[6]))
    if bad:
        raise SystemExit('%s:\n  ' % R.name + '\n  '.join(bad))
    print('  %s: %d solids, %d pictures - no overlaps, passages clear' % (R.name, len(B.solids), len(B.decals)))


ALL = [room2b32gatev]
