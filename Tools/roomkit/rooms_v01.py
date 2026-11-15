"""The 24 "v0.1 style" rooms for the Indev zone.  Each function returns (Room, description, shape,
commonness, view) - view is the camera used for the preview sheet."""
from v01kit import *

LOW = -448.0


def R_(name):
    return Room(name, luxel=12, ambient=11, fill=0.14)


# =====================================================================  two-door rooms
def room2v_hall():
    R = R_('room2v_hall')
    junction(R, 'NS', 'old')
    for z in (-600, 0, 600):
        lamp(R, 0, z, 384, power=88)
    bench(R, -160, 330, 90)
    item(R, 'bat', -160, 54, 330, 30)
    return R, 'A plain early-pattern hallway: rust-banded concrete, three ceiling lamps, a bench.', '2', 100, ((0, 165, -940), (0, 150, 0))


def room2v_arch():
    R = R_('room2v_arch')
    w, ch = 256.0, 448.0
    junction(R, 'NS', 'old', w=w, ch=ch)
    for z in (-600, 0, 600):
        arch(R, 'z', z, w, ch)
    for z in (-300, 300):
        ibeam(R, 'z', z, -w, w, 396)
        lamp(R, 0, z, ch, power=84)
    return R, 'A tall hallway crossed by three concrete portal frames with a lamp in each leg, and steel beams between them.', '2', 80, ((0, 165, -940), (0, 190, 0))


def room2v_guard():
    R = R_('room2v_guard')
    win = (-160.0, 160.0, 112.0, 288.0)
    junction(R, 'NS', 'board', openings={'hubE': [win]})
    b = annex(R, 'x', 192, +1, -224, 224, 256, 320, 'board', window=win)
    lamp(R, 384, 0, 320, power=70, rng=520, color=(255, 225, 190))
    for z in (-620, 620):
        lamp(R, 0, z, 384, power=80)
    spot(R, 380, 0, 0)
    item(R, 'bat', 224, 112, -100, 50)
    item(R, 'radio', 224, 112, 100, 25)
    sign_at(R, 'admittance', 192, -300, 'W', 96, 70, 230, sheet='misc')
    return R, 'A guard post: a counter and an open hatch in the corridor wall, and whoever is still on duty behind it.', '2', 45, ((-120, 165, -420), (300, 150, 20))


def room2v_medbay():
    R = R_('room2v_medbay')
    junction(R, 'NS', 'ez', openings={'N_E': [door_op(420)]})
    x0, z0, x1, z1 = annex(R, 'x', 192, +1, 220, 860, 600, 352, 'med', door=420)
    for z in (-600, 0, 600):
        lamp(R, 0, z, 384, power=96, color=(255, 250, 240), size=64)
    bench(R, -160, -330, 90)
    bench(R, -160, -520, 90)
    R.decal((192, 660), (192, 580), 150, 250, Mat('labelmedicalbay.jpg', cast=False), (0, 0, 1, 1))
    # the bay: three beds, a desk, a chair, a body
    white = Mat('white.jpg', 256)
    for z in (300, 500, 700):
        R.box(640, 0, z - 46, 840, 46, z + 46, DIRTY, skip='B', lux=10)
        R.box(644, 46, z - 42, 836, 58, z + 42, white, skip='B', lux=10)
    top = desk(R, 270, 690, 350, 840, 0)
    R.model('officeseat_a.x', 420, 0, 760, rot=(0, 90, 0), scale=(3.5, 3.5, 3.5), size=(84, 160, 84))
    ceil_light(R, 520, 520, 352, size=80, power=118, rng=820, color=(240, 250, 240))
    ceil_fan(R, 480, 420, 352)
    spot(R, 470, 0, 600)
    item(R, 'firstaid', 310, top, 720, 100)
    item(R, 'syringe', 310, top, 800, 50)
    item(R, 'eyedrops', 740, 58, 300, 60)
    return R, 'An office-zone corridor with benches and the old medical bay: green-striped walls, three beds, a body.', '2', 40, ((300, 165, 300), (760, 60, 760))


def room2v_lockers():
    R = R_('room2v_lockers')
    w = 224.0
    junction(R, 'NS', 'dark', w=w)
    lockers(R, 'x', w, -1, 260, 700)
    lockers(R, 'x', -w, +1, -700, -260)
    cabinet(R, w - 32, 80, 0, 'W')
    cabinet(R, w - 32, 140, 0, 'W')
    for z in (-560, 480):
        lamp(R, 0, z, 384, power=74, color=(235, 240, 255))
    spot(R, 150, 0, -70)
    item(R, 'key2', 70, 0, -40, 70)
    item(R, 'eyedrops', -150, 0, 150, 30)
    return R, 'A steel-floored passage lined with lockers. A researcher is sitting against the cabinets and will not be getting up.', '2', 45, ((-100, 165, -420), (160, 60, 20))


def room2v_surv():
    R = R_('room2v_surv')
    junction(R, 'NS', 'old', openings={'S_W': [door_op(-500)]})
    x0, z0, x1, z1 = annex(R, 'x', -192, -1, -760, -240, 480, 352, 'std', door=-500)
    R.decal((x0, -720), (x0, -520), 30, 260, CTRL, (0.0, 0.0, 0.5, 1.0))
    R.decal((x0, -500), (x0, -300), 30, 260, CTRL, (0.5, 0.0, 1.0, 1.0))
    top = desk(R, -560, -300, -330, -250, 0)
    workstation(R, -480, top, -270, yaw=180)
    workstation(R, -390, top, -270, yaw=180)
    R.model('officeseat_a.x', -440, 0, -360, rot=(0, 0, 0), scale=(3.5, 3.5, 3.5), size=(84, 160, 84))
    lamp(R, -500, -500, 352, power=92)
    for z in (-600, 0, 600):
        lamp(R, 0, z, 384, power=86)
    sign_at(R, 'admittance', -192, -300, 'E', 96, 70, 230, sheet='misc')
    item(R, 'bat', -540, top, -275, 60)
    item(R, 'radio', -620, 0, -600, 30)
    item(R, 'nvgoggles', -700, 0, -330, 12)
    return R, 'A hallway with the old surveillance room off it: a console wall, two monitors, a swivel chair.', '2', 40, ((-290, 165, -700), (-700, 120, -400))


def room2v_pillars():
    R = R_('room2v_pillars')
    junction(R, 'NS', 'std', hub=(-560, -640, 560, 640), hh=480)
    for x in (-300, 300):
        for z in (-400, 0, 400):
            pillar(R, x, z, 480)
    for (x, z) in ((0, -320), (0, 320), (-440, 0), (440, 0)):
        lamp(R, x, z, 480, power=92, rng=900)
    crate(R, 470, 0, 540, yaw=15)
    item(R, 'bat', -480, 0, -560, 25)
    return R, 'A wide hall with two rows of square concrete pillars.', '2', 60, ((0, 165, -900), (120, 170, 0))


def room2v_pipes():
    R = R_('room2v_pipes')
    w, ch = 176.0, 352.0
    junction(R, 'NS', 'dark', w=w, ch=ch, openings={'hubW': [(-80.0, 80.0, 150.0, 310.0)]})
    for (x, y, r) in ((-116, 306, 22), (118, 312, 16), (70, 328, 9)):
        R.tube((x, y, -990), (x, y, 990), r, RUST.but(us=2 * math.pi * r, vs=256), sides=8, lux=16)
    wall_fan(R, 'x', -w, -1, 0, 230)
    lamp(R, 0, -560, ch, power=70, color=(235, 240, 255), size=36)
    R.box(-14, ch - 20, 546, 14, ch, 574, REDLAMP, skip='T')
    R.light(0, ch - 50, 560, rng=760, color=(255, 56, 44), power=120)
    return R, 'A narrow dark service passage with pipes under the roof, a duct fan in the wall and a red lamp.', '2', 55, ((0, 165, -900), (-30, 170, 0))


def room2v_cells():
    R = R_('room2v_cells')
    junction(R, 'NS', 'std', openings={'hubW': [door_op(0)]})
    x0, z0, x1, z1 = annex(R, 'x', -192, -1, -200, 200, 360, 320, 'white', door=0)
    dd = Mat('dclass_door.jpg', 256, cast=False)
    for z in (-760, -470, 470, 760):
        R.decal((-192, z - 76), (-192, z + 76), 0, 304, dd, (0, 0, 1, 1))
        R.decal((192, z + 76), (192, z - 76), 0, 304, dd, (0, 0, 1, 1))
    R.model('dclass_bed.x', x0 + 70, 0, 60, size=(100, 80, 228))
    R.model('dclass_toilet.x', x1 - 60, 0, -150, rot=(0, 180, 0), size=(56, 90, 70))
    lamp(R, (x0 + x1) / 2, 0, 320, power=84, size=36)
    for z in (-600, 0, 600):
        lamp(R, 0, z, 384, power=80)
    item(R, 'indevration', x0 + 70, 84, 0, 60)
    item(R, 'bat', x0 + 200, 0, 140, 25)
    return R, 'A row of Class-D cells. One door still opens.', '2', 45, ((0, 165, -900), (-60, 150, 0))


def room2v_lift():
    R = R_('room2v_lift')
    AW = wmat('old', 384)
    junction(R, 'NS', 'old', openings={'N_E': [door_op(400)]})
    d1, p1 = elevator(R, 192, 400, 0, +1, AW)
    # the basement store under the hallway
    bw = wmat('std', 384).but(v0=LOW + 384)
    out = [(-448, -640), (-448, 160), (192, 160), (192, -640)]
    R.walls(out, LOW, LOW + 384, bw, holes={2: [span(out[2], (192, -304), (192, -496)) + (LOW, LOW + 320)]})
    R.rect_floor(-448, -640, 192, 160, LOW, CONC)
    R.rect_ceil(-448, -640, 192, 160, LOW + 384, DIRTY)
    d2, p2 = elevator(R, 192, -400, LOW, +1, AW)
    R.spawns.append(dict(kind='lift', a=d1, ap=p1, b=d2, bp=p2))
    t = shelf_unit(R, -440, -600, -376, -200, LOW, height=250, levels=4)
    t2 = shelf_unit(R, -300, 96, 60, 152, LOW, height=250, levels=4)
    crate(R, -300, LOW, -520, yaw=12)
    ceil_light(R, -128, -240, LOW + 384, size=64, power=96, rng=820, color=(255, 236, 206))
    for z in (-600, 0, 600):
        lamp(R, 0, z, 384, power=86)
    sign_at(R, 'elevator', 192, 180, 'W', 150, 50, 250)
    item(R, 'firstaid', -408, t[1], -500, 80)
    item(R, 'bat', -408, t[1], -320, 100)
    item(R, '18vbat', -408, t[2], -400, 40)
    item(R, 'gasmask', -200, t2[1], 124, 30)
    item(R, 'indevration', -60, t2[2], 124, 50)
    return R, 'A hallway with a lift down to a basement store.', '2', 35, ((0, 165, -300), (150, 150, 500))


def room2v_vent():
    R = R_('room2v_vent')
    junction(R, 'NS', 'std', hub=(-512, -512, 512, 512), hh=448)
    vent_block(R, -176, -176, 176, 176, 448)
    ceil_fan(R, -350, 0, 448)
    lamp(R, 350, 0, 448, power=70, rng=700, size=36)
    for (x, z) in ((-380, -380), (380, -380), (-380, 380), (380, 380)):
        lamp(R, x, z, 448, power=70, rng=700, size=36)
    return R, 'A hall built round a concrete plant block with vent grilles and lamps on every face, and two ceiling fans.', '2', 50, ((-380, 165, -480), (120, 170, 100))


# =====================================================================  corner rooms (doors on -z and +x)
def room2cv_plain():
    R = R_('room2cv_plain')
    junction(R, 'SE', 'old')
    lamp(R, 0, 0, 384, power=96)
    lamp(R, 0, -640, 384, power=80)
    lamp(R, 640, 0, 384, power=80)
    return R, 'A plain early-pattern corner.', '2C', 100, ((0, 165, -900), (60, 150, 0))


def room2cv_lamps():
    R = R_('room2cv_lamps')
    junction(R, 'SE', 'ez', hub=(-256, -256, 256, 256))
    pendant(R, 0, -640, 384, power=128)
    pendant(R, 0, 0, 384, power=128)
    pendant(R, 640, 0, 384, power=128)
    bench(R, -200, 0, 90)
    return R, 'An office-zone corner under red pendant lamps.', '2C', 80, ((0, 165, -900), (80, 160, 0))


def room2cv_post():
    R = R_('room2cv_post')
    win = (-200.0, 200.0, 0.0, 300.0)
    junction(R, 'SE', 'std', hub=(-320, -320, 320, 320), hh=448, openings={'hubN': [win]})
    x0, z0, x1, z1 = annex(R, 'z', 320, +1, -260, 260, 280, 320, 'std', window=win)
    pillar(R, -200, -200, 448, s=44)
    t = shelf_unit(R, x0 + 8, z1 - 60, x1 - 8, z1 - 6, 0, height=250, levels=4)
    crate(R, x0 + 90, 0, z0 + 110, yaw=10)
    lamp(R, 0, 0, 448, power=100, rng=900)
    lamp(R, 0, (z0 + z1) / 2, 320, power=72, rng=520, size=36)
    lamp(R, 0, -660, 384, power=78)
    lamp(R, 660, 0, 384, power=78)
    item(R, 'bat', -120, t[1], z1 - 34, 70)
    item(R, 'firstaid', 120, t[2], z1 - 34, 35)
    item(R, 'eyedrops', 40, t[1], z1 - 34, 40)
    return R, 'A corner with a pillar and an open store alcove.', '2C', 60, ((-60, 165, -700), (60, 140, 400))


def room2cv_office():
    R = R_('room2cv_office')
    junction(R, 'SE', 'ez', openings={'hubN': [door_op(0)]})
    x0, z0, x1, z1 = annex(R, 'z', 192, +1, -360, 360, 480, 352, 'ez', door=0)
    top = desk(R, -320, z1 - 110, -120, z1 - 30, 0)
    workstation(R, -220, top, z1 - 60, yaw=0)
    R.model('officeseat_a.x', -220, 0, z1 - 170, rot=(0, 180, 0), scale=(3.5, 3.5, 3.5), size=(84, 160, 84))
    cabinet_row(R, (x1 - 32, z0 + 40), (x1 - 32, z0 + 240), 0, 'W')
    ceil_light(R, 0, (z0 + z1) / 2, 352, size=80, power=110, rng=760)
    lamp(R, 0, 0, 384, power=96, color=(255, 250, 240), size=64)
    lamp(R, 0, -640, 384, power=84, color=(255, 250, 240), size=64)
    lamp(R, 640, 0, 384, power=84, color=(255, 250, 240), size=64)
    item(R, 'bat', -150, top, z1 - 70, 60)
    item(R, 'eyedrops', x1 - 32, 180, z0 + 100, 40)
    item(R, 'key1', -290, top, z1 - 70, 25)
    return R, 'An office-zone corner with a small office off it.', '2C', 55, ((120, 165, 330), (-260, 100, 700))


# =====================================================================  T junctions (doors on -z, +x, -x)
def room3v_plain():
    R = R_('room3v_plain')
    junction(R, 'SEW', 'old')
    lamp(R, 0, 0, 384, power=98)
    for (x, z) in ((0, -640), (640, 0), (-640, 0)):
        lamp(R, x, z, 384, power=78)
    return R, 'A plain early-pattern T junction.', '3', 100, ((0, 165, -900), (0, 150, 100))


def room3v_arch():
    R = R_('room3v_arch')
    w, ch = 224.0, 416.0
    junction(R, 'SEW', 'old', w=w, ch=ch)
    arch(R, 'z', -560, w, ch)
    arch(R, 'x', 560, w, ch)
    arch(R, 'x', -560, w, ch)
    lamp(R, 0, 0, ch, power=104, rng=900)
    return R, 'A T junction with a concrete portal frame across each arm.', '3', 70, ((0, 165, -900), (0, 170, 100))


def room3v_hub():
    R = R_('room3v_hub')
    junction(R, 'SEW', 'std', hub=(-512, -512, 512, 512), hh=480)
    pillar(R, 0, 0, 480, s=72)
    for f, x, z in (('S', 0, -72), ('N', 0, 72), ('E', 72, 0), ('W', -72, 0)):
        wall_light(R, x, z, 300, f, power=58, rng=520)
    ibeam(R, 'z', -300, -512, 512, 430)
    ibeam(R, 'z', 300, -512, 512, 430)
    ceil_fan(R, 330, 330, 480)
    lamp(R, -330, 330, 480, power=76, rng=760, size=36)
    crate(R, -420, 0, 430, yaw=-12)
    return R, 'A T junction opened out into a hall round a central pier, with beams and a ceiling fan.', '3', 55, ((0, 165, -900), (60, 190, 0))


def room3v_booth():
    R = R_('room3v_booth')
    win = (-60.0, 300.0, 112.0, 288.0)
    junction(R, 'SEW', 'board', hub=(-448, -192, 448, 192), openings={'hubN': [win, door_op(-320)]})
    x0, z0, x1, z1 = annex(R, 'z', 192, +1, -448, 448, 400, 320, 'board', door=-320, window=win)
    top = desk(R, -40, z0 + 8, 280, z0 + 80, 0)
    workstation(R, 120, top, z0 + 44, yaw=180)
    cabinet_row(R, (x1 - 32, z1 - 220), (x1 - 32, z1 - 20), 0, 'W')
    lamp(R, 0, (z0 + z1) / 2, 320, power=82, rng=620, color=(255, 225, 190))
    lamp(R, 0, 0, 384, power=92)
    for (x, z) in ((0, -640), (700, 0), (-700, 0)):
        lamp(R, x, z, 384, power=76)
    item(R, 'bat', 40, top, z0 + 44, 60)
    item(R, 'key2', 230, top, z0 + 44, 20)
    item(R, 'firstaid', x1 - 32, 180, z1 - 120, 35)
    return R, 'A T junction overlooked by a checkpoint booth with a hatch and a door.', '3', 50, ((0, 165, -700), (60, 150, 300))


# =====================================================================  crossroads
def room4v_plain():
    R = R_('room4v_plain')
    junction(R, 'NSEW', 'old', hub=(-256, -256, 256, 256), hh=448)
    lamp(R, 0, 0, 448, power=110, rng=900)
    for (x, z) in ((0, -640), (0, 640), (640, 0), (-640, 0)):
        lamp(R, x, z, 384, power=74)
    return R, 'A plain early-pattern crossroads.', '4', 100, ((0, 165, -900), (0, 170, 0))


def room4v_block():
    R = R_('room4v_block')
    junction(R, 'NSEW', 'std', hub=(-576, -576, 576, 576), hh=480)
    vent_block(R, -144, -144, 144, 144, 480)
    for sx in (-1, 1):
        for sz in (-1, 1):
            pillar(R, sx * 430, sz * 430, 480, s=36)
    ceil_fan(R, -360, 0, 480)
    lamp(R, 360, 0, 480, power=70, rng=700, size=36)
    lamp(R, 0, 360, 480, power=70, rng=700, size=36)
    lamp(R, 0, -360, 480, power=70, rng=700, size=36)
    return R, 'A crossroads round a vent block, with a pillar in each corner and a ceiling fan.', '4', 60, ((-300, 165, -860), (100, 190, 0))


def room4v_beams():
    R = R_('room4v_beams')
    junction(R, 'NSEW', 'board', hub=(-384, -384, 384, 384), hh=576)
    ibeam(R, 'z', -150, -384, 384, 500)
    ibeam(R, 'z', 150, -384, 384, 500)
    ibeam(R, 'x', -150, -384, 384, 450)
    ibeam(R, 'x', 150, -384, 384, 450)
    pendant(R, 0, 0, 576, power=140, rng=1100)
    for f, x, z in (('S', -280, 384), ('N', 280, -384), ('W', 384, 280), ('E', -384, -280)):
        wall_light(R, x, z, 280, f, power=50, rng=440)
    return R, 'A tall crossing under two layers of steel beams.', '4', 60, ((0, 165, -900), (0, 260, 0))


# =====================================================================  dead ends (door on -z)
def room1v_173():
    R = R_('room1v_173')
    win = (-240.0, 240.0, 0.0, 352.0)
    junction(R, 'S', 'old', hub=(-640, -448, 640, 640), hh=640, openings={'hubN': [win]})
    x0, z0, x1, z1 = annex(R, 'z', 640, +1, -320, 320, 280, 400, 'lab', window=win)
    cd = Mat('containment_doors.jpg', 512)
    R.box(-300, 0, 600, -240, 420, 640, cd, skip='BN')
    R.box(240, 0, 600, 300, 420, 640, cd, skip='BN')
    R.box(-240, 352, 600, 240, 420, 640, Mat('red.jpg', 128), skip='N')
    ceil_light(R, 0, (z0 + z1) / 2, 400, size=96, power=150, rng=900)
    # the gallery on the west wall, on two posts
    R.box(-640, 304, -220, -420, 320, 220, DIRTY, skip='W')
    R.box(-432, 320, -220, -420, 404, 220, PANELS, skip='B', lux=10)
    R.box(-640, 320, -220, -432, 404, -208, PANELS, skip='BW', lux=10)
    R.box(-640, 320, 208, -432, 404, 220, PANELS, skip='BW', lux=10)
    for z in (-212, 212):
        R.box(-436, 0, z - 8, -420, 304, z + 8, DIRTY, skip='TB', lux=10)
    spot(R, -530, 320, 0)
    for z in (-420, 420):
        R.decal((-640, z - 40), (-640, z + 40), 40, 120, VENT, (0, 0, 1, 1), off=2)
    lamp(R, -200, -100, 640, power=120, rng=1300, size=64)
    lamp(R, 300, 250, 640, power=120, rng=1300, size=64)
    lamp(R, 0, -720, 384, power=74)
    R.waypoint(0, 66, -300)
    item(R, 'bat', 250, 0, z0 + 60, 40)
    return R, 'The old SCP-173 test yard: a tall hall, a gallery for the guard, and the open containment door.', '1', 25, ((300, 165, -380), (-200, 220, 500))


def room1v_store():
    R = R_('room1v_store')
    junction(R, 'S', 'board', hub=(-448, -320, 448, 512), hh=352)
    t1 = shelf_unit(R, -440, -200, -376, 440, 0, height=250, levels=4)
    t2 = shelf_unit(R, -300, 456, 300, 504, 0, height=250, levels=4)
    file_row(R, (-190, 430, -408), (0, 0, 0), t1[3], 'z', seed=91, fill=0.4)
    crate(R, 330, 0, 300, yaw=10)
    crate(R, 340, 0, 120, yaw=-25, kind=2)
    ceil_fan(R, 0, 100, 352)
    lamp(R, 0, -100, 352, power=92, rng=900)
    lamp(R, 0, -720, 384, power=74)
    R.waypoint(0, 66, -200)
    item(R, 'bat', -408, t1[1], -100, 80)
    item(R, 'indevration', -408, t1[2], 200, 60)
    item(R, 'firstaid', -100, t2[1], 480, 50)
    item(R, 'gasmask', 150, t2[2], 480, 20)
    item(R, '18vbat', 220, t2[1], 480, 35)
    return R, 'A dead-end storeroom: shelving, crates, a ceiling fan.', '1', 100, ((0, 165, -640), (-120, 120, 300))


ALL = [room2v_hall, room2v_arch, room2v_guard, room2v_medbay, room2v_lockers, room2v_surv, room2v_pillars,
       room2v_pipes, room2v_cells, room2v_lift, room2v_vent,
       room2cv_plain, room2cv_lamps, room2cv_post, room2cv_office,
       room3v_plain, room3v_arch, room3v_hub, room3v_booth,
       room4v_plain, room4v_block, room4v_beams,
       room1v_173, room1v_store]
