"""55 more v0.1-style rooms for the Indev zone (the "w" series).
Each function returns (Room, description, shape, commonness, view, rare-item tag)."""
from v02kit import *

LOW = -448.0
DEEP = -704.0
VIEW = ((0, 165, -900), (0, 170, 0))
NS3 = ((0, -600), (0, 0), (0, 600))


def R_(name, amb=11):
    return Room(name, luxel=12, ambient=amb, fill=0.14)


def lamps(R, pts, ch, **kw):
    for (x, z) in pts:
        lamp(R, x, z, ch, **kw)


def red_lamp(R, x, z, ceil_y, power=120, rng=780):
    R.box(x - 14, ceil_y - 20, z - 14, x + 14, ceil_y, z + 14, REDLAMP, skip='T')
    R.light(x, ceil_y - 50, z, rng=rng, color=(255, 56, 44), power=power)


# =====================================================================  hallways
def room2w_narrow():
    R = R_('room2w_narrow')
    w, ch = 176.0, 336.0
    junction(R, 'NS', 'board', w=w, ch=ch)
    pilasters(R, 'x', -w, +1, -800, 800, 320, ch)
    pilasters(R, 'x', w, -1, -800, 800, 320, ch)
    lamps(R, ((0, -480), (0, 480)), ch, power=78)
    return R, 'A low, narrow board-marked passage with concrete ribs.', '2', 70, VIEW, ''


def room2w_wide():
    R = R_('room2w_wide')
    w, ch = 288.0, 416.0
    junction(R, 'NS', 'old', w=w, ch=ch)
    bench(R, -252, -300, 90)
    bench(R, -252, 300, 90)
    bench(R, 252, 0, 90)
    lamps(R, NS3, ch, power=98, rng=820)
    item(R, 'bat', 252, 54, 0, 20)
    return R, 'A broad early-pattern hallway with benches along the walls.', '2', 70, VIEW, ''


def room2w_tall():
    R = R_('room2w_tall')
    ch = 576.0
    junction(R, 'NS', 'std', ch=ch)
    for z in (-500, 0, 500):
        ibeam(R, 'z', z, -192, 192, 468)
    for z in (-250, 250):
        wall_light(R, -192, z, 380, 'E', power=62, rng=520)
        wall_light(R, 192, -z, 380, 'W', power=62, rng=520)
    lamp(R, 0, 0, ch, power=70, rng=900)
    return R, 'A tall, narrow concrete hallway crossed by steel beams.', '2', 60, ((0, 165, -900), (0, 260, 0)), ''


def room2w_ribs():
    R = R_('room2w_ribs')
    w, ch = 208.0, 368.0
    junction(R, 'NS', 'dark', w=w, ch=ch)
    pilasters(R, 'x', -w, +1, -896, 896, 256, ch, depth=26, width=56, style='dark')
    pilasters(R, 'x', w, -1, -896, 896, 256, ch, depth=26, width=56, style='dark')
    lamps(R, ((0, -640), (0, 0), (0, 640)), ch, power=66, color=(230, 238, 255), size=36)
    return R, 'A dark ribbed tunnel with a steel floor.', '2', 60, VIEW, ''


def room2w_oct():
    R = R_('room2w_oct')
    junction2(R, 'NS', 'std', hub=(-448, -448, 448, 448), cut=192, hh=480)
    lamp(R, 0, 0, 480, power=124, rng=1000, size=72)
    for f, x, z in (('E', -448, 0), ('W', 448, 0)):
        vents(R, x, z, f, n=2, gap=140)
        wall_light(R, x, z, 300, f, power=56, rng=480)
    return R, 'An eight-sided concrete hall on the line of the hallway.', '2', 55, VIEW, ''


def room2w_consoles():
    R = R_('room2w_consoles')
    junction(R, 'NS', 'old', openings={'S_W': [door_op(-480)]})
    x0, z0, x1, z1 = annex(R, 'x', -192, -1, -760, -200, 480, 352, 'old', door=-480)
    console(R, -610, z1 - 40, 'S')
    console(R, -410, z1 - 40, 'S')
    bench(R, -500, z0 + 40, 0)
    wall_light(R, x0, -480, 260, 'E', power=58, rng=460)
    wall_light(R, -500, z1, 300, 'S', power=58, rng=460)
    lamps(R, NS3, 384, power=86)
    roll(R, -500, 0, -480)
    item(R, 'bat', -500, 54, z0 + 40, 40)
    return R, 'A hallway with a small control room off it: two console units, a bench, wall lamps.', '2', 45, ((-290, 165, -640), (-560, 110, -260)), 'testing'


def room2w_meeting():
    R = R_('room2w_meeting')
    junction(R, 'NS', 'ez', openings={'N_E': [door_op(380)]})
    x0, z0, x1, z1 = annex(R, 'x', 192, +1, 200, 820, 560, 336, 'old', door=380)
    top = meeting(R, 540, 520, 'z')
    whiteboard(R, x1, 520, 'W')
    ceil_vent(R, 540, 520, 336)
    lamp(R, 420, 320, 336, power=80, rng=700)
    lamps(R, NS3, 384, power=96, color=(255, 250, 240), size=64)
    roll(R, 540, top, 600)
    return R, 'An office-zone hallway with the old meeting room: a long table, white chairs, a whiteboard.', '2', 45, ((300, 165, 260), (700, 90, 700)), 'office'


def room2w_whitedoor():
    R = R_('room2w_whitedoor')
    junction(R, 'NS', 'std', openings={'S_E': [door_op(-460)]})
    x0, z0, x1, z1 = annex(R, 'x', 192, +1, -800, -160, 620, 352, 'old', door=-460)
    glow_door(R, x1, -480, 'W')
    vents(R, 520, z1, 'S', n=2, gap=130, yc=110, size=90)
    cabinet_row(R, (600, z0 + 32), (830, z0 + 32), 0, 'N')
    top = table(R, 380, -620, 560, -500)
    book(R, 470, top, -560)
    lamps(R, NS3, 384, power=84)
    roll(R, 420, top, -560)
    return R, 'A hallway with a dim records room; at its far wall, a doorway of flat white light that is not a door.', '2', 40, ((300, 165, -740), (860, 150, -470)), 'office'


def room2w_canteen():
    R = R_('room2w_canteen')
    junction(R, 'NS', 'ez', openings={'N_W': [door_op(420)]})
    x0, z0, x1, z1 = annex(R, 'x', -192, -1, 180, 860, 580, 352, 'ez', door=420)
    vending(R, -720, z1, 'S')
    vending(R, -620, z1, 'S')
    for (cx, cz) in ((-640, 420), (-420, 640)):
        top = table(R, cx - 70, cz - 50, cx + 70, cz + 50, top=WOODT)
        chair(R, cx, cz - 90, 'N')
        chair(R, cx, cz + 90, 'S')
    ceil_light(R, -540, 520, 352, size=80, power=112, rng=820)
    lamps(R, NS3, 384, power=96, color=(255, 250, 240), size=64)
    item(R, 'indevration', -640, top, 420, 50)
    roll(R, -420, top, 640)
    return R, 'An office-zone hallway with a small canteen: two vending machines, two tables.', '2', 45, ((-300, 165, 300), (-700, 100, 800)), 'cafeteria'


def room2w_lab():
    R = R_('room2w_lab')
    win = (-420.0, -180.0, 96.0, 256.0)
    junction(R, 'NS', 'lab', openings={'S_E': [door_op(-620), win]})
    x0, z0, x1, z1 = annex(R, 'x', 192, +1, -800, -120, 560, 352, 'lab', door=-620, window=win)
    glaze(R, 'x', 192, +1, win)
    top = desk(R, x1 - 100, -700, x1 - 20, -380, 0)
    workstation(R, x1 - 60, top, -600, yaw=270)
    workstation(R, x1 - 60, top, -460, yaw=270)
    cabinet_row(R, (420, z1 - 32), (700, z1 - 32), 0, 'S')
    table(R, 420, -560, 600, -440)
    ceil_light(R, 520, -460, 352, size=96, power=140, rng=900)
    lamps(R, NS3, 384, power=98, color=(245, 250, 255), size=64)
    roll(R, 510, 78, -500)
    item(R, 'eyedrops', x1 - 60, top, -520, 50)
    return R, 'A white-tiled hallway with a glazed laboratory.', '2', 45, ((-120, 165, -500), (700, 110, -380)), 'testing'


def room2w_generator():
    R = R_('room2w_generator')
    w = 224.0
    win = (-200.0, 200.0, 0.0, 320.0)
    junction(R, 'NS', 'hcz', w=w, openings={'hubE': [win], 'hubW': [(-80.0, 80.0, 150.0, 310.0)]})
    x0, z0, x1, z1 = annex(R, 'x', w, +1, -320, 320, 420, 384, 'hcz', window=win)
    tank(R, x1 - 150, z0 + 20, x1 - 20, z0 + 200)
    tank(R, x1 - 150, z1 - 200, x1 - 20, z1 - 20)
    pipes_z(R, ((x1 - 85, 350, 18),), z0, z1)
    wall_fan(R, 'x', -w, -1, 0, 230)
    red_lamp(R, (x0 + x1) / 2, 0, 384)
    lamps(R, ((0, -600), (0, 600)), 384, power=72, color=(232, 238, 255), size=36)
    return R, 'A heavy steel passage with a plant bay: two tanks, a duct fan, a red lamp.', '2', 45, ((-120, 165, -420), (560, 150, 60)), ''


def room2w_bridge():
    R = R_('room2w_bridge')
    junction(R, 'NS', 'std', hub=(-320, -640, 320, 640), hh=576)
    bridge(R, 'x', 0, -320, 320, y=352)
    ibeam(R, 'z', -400, -320, 320, 500)
    ibeam(R, 'z', 400, -320, 320, 500)
    lamps(R, ((0, -330), (0, 330)), 576, power=104, rng=1000, size=64)
    for z in (-480, 480):
        wall_light(R, -320, z, 260, 'E', power=52, rng=440)
        wall_light(R, 320, z, 260, 'W', power=52, rng=440)
    return R, 'A tall hall with a railed walkway crossing overhead.', '2', 50, ((0, 165, -900), (0, 280, 0)), ''


def room2w_mezz():
    R = R_('room2w_mezz')
    junction(R, 'NS', 'board', hub=(-512, -512, 512, 512), hh=544)
    wm = wmat('board', 192)
    R.box(-512, 0, -16, -256, 192, 512, wm, skip='BWN', top=CONC)
    stairs(R, -512, -256, -400, 12, 16.0, 32.0, +1, 0, STYLES['std'][0].but(us=256, vs=256), top=CONC)
    railing(R, (-256, -16), (-256, 512), 192)
    R.collide_wall((-256, -400), (-256, -16), 0, 330)
    R.collide_wall((-256, -16), (-256, -400), 0, 330)
    t = shelf_unit(R, -504, 300, -444, 500, 192, height=230, levels=4)
    crate(R, -400, 192, 120, yaw=14)
    lamps(R, ((0, -250), (0, 250), (-380, 250)), 544, power=96, rng=1000, size=56)
    item(R, 'bat', -474, t[1], 360, 80)
    item(R, 'firstaid', -474, t[2], 440, 40)
    return R, 'A hall with a mezzanine up a flight of steps; a few stores are kept up there.', '2', 45, ((300, 165, -420), (-400, 200, 200)), ''


def room2w_lift2():
    R = R_('room2w_lift2')
    AW = wmat('std', 384)
    junction(R, 'NS', 'std', openings={'S_E': [door_op(-400)]})
    lift(R, 192, +1, -400, 0, 400, 448, AW)
    UW = wmat('std', 352).but(v0=800)
    out = [(-448, -160), (-448, 640), (192, 640), (192, -160)]
    R.walls(out, 448, 800, UW, holes={2: [span(out[2], (192, 496), (192, 304)) + (448, 768)]})
    R.rect_floor(-448, -160, 192, 640, 448, CONC)
    R.rect_ceil(-448, -160, 192, 640, 800, DIRTY)
    t = shelf_unit(R, -440, 0, -376, 400, 448, height=250, levels=4)
    crate(R, -200, 448, 540, yaw=12)
    ceil_light(R, -128, 240, 800, size=64, power=100, rng=860, color=(255, 236, 206))
    lamps(R, NS3, 384, power=86)
    sign_at(R, 'elevator', 192, -620, 'W', 150, 50, 250)
    item(R, 'bat', -408, t[1], 100, 100)
    item(R, 'eyedrops', -408, t[2], 220, 50)
    item(R, 'key2', -408, t[1], 320, 30)
    return R, 'A hallway with a lift up to a store on the floor above.', '2', 35, ((0, 165, 200), (150, 150, -500)), 'storage'


def room2w_dogleg():
    R = R_('room2w_dogleg')
    junction(R, 'NS', 'old', hub=(-448, -448, 448, 448))
    wm = wmat('old', 384)
    R.box(-448, 0, -232, 64, 384, -168, wm, skip='TBW', lux=12)
    R.box(-64, 0, 168, 448, 384, 232, wm, skip='TBE', lux=12)
    lamps(R, ((260, -330), (0, 0), (-260, 330)), 384, power=92)
    return R, 'A hall split by two baffle walls, so the way through doubles back on itself.', '2', 55, ((250, 165, -420), (-100, 150, 100)), ''


def room2w_checkpoint():
    R = R_('room2w_checkpoint')
    win = (-160.0, 160.0, 112.0, 288.0)
    junction(R, 'NS', 'haz', openings={'hubE': [win]})
    annex(R, 'x', 192, +1, -224, 224, 256, 320, 'haz', window=win)
    glaze(R, 'x', 192, +1, win)
    arch(R, 'z', -330, 192, 384)
    arch(R, 'z', 330, 192, 384)
    lamp(R, 384, 0, 320, power=72, rng=520, color=(255, 225, 190))
    lamps(R, ((0, -640), (0, 0), (0, 640)), 384, power=82)
    role(R, 'guard', 380, 0, 0, 90)
    sign_at(R, 'admittance', -192, 0, 'E', 96, 70, 230, sheet='misc')
    return R, 'A hazard-striped checkpoint between two portal frames, with a glazed guard booth.', '2', 40, ((-120, 165, -520), (300, 150, 40)), ''


def room2w_cages():
    R = R_('room2w_cages')
    junction(R, 'NS', 'dark', hub=(-512, -640, 512, 640))
    cage(R, -504, -600, -240, -240)
    cage(R, -504, -180, -240, 180, open_side='E', gap=(-60, 60))
    cage(R, -504, 240, -240, 600)
    cage(R, 240, -600, 504, -240)
    cage(R, 240, 240, 504, 600)
    crate(R, -400, 0, -420, yaw=10)
    crate(R, -380, 0, 430, yaw=-20, kind=2)
    crate(R, 380, 0, -400, yaw=30)
    lamps(R, ((0, -360), (0, 360)), 384, power=84, color=(232, 238, 255))
    item(R, 'bat', -400, 0, 60, 60)
    item(R, 'gasmask', -420, 0, -80, 25)
    roll(R, -380, 0, 0)
    return R, 'A store hall of wire cages. One has been left open.', '2', 45, ((200, 165, -560), (-400, 110, 100)), 'storage'


def room2w_infirm():
    R = R_('room2w_infirm')
    junction(R, 'NS', 'med', openings={'N_E': [door_op(400)]})
    x0, z0, x1, z1 = annex(R, 'x', 192, +1, 220, 760, 520, 352, 'med', door=400)
    beds(R, x1 - 200, x1 - 10, (300, 500, 700))
    cabinet(R, x0 + 32, 700, 0, 'E')
    ceil_light(R, 500, 500, 352, size=80, power=114, rng=820, color=(240, 250, 240))
    lamps(R, NS3, 384, power=92, color=(245, 250, 245), size=56)
    role(R, 'liej', 420, 0, 560, 200)
    item(R, 'firstaid', x1 - 100, 58, 300, 80)
    item(R, 'syringe', x0 + 32, 180, 700, 50)
    roll(R, 400, 0, 320)
    return R, 'A green-striped corridor and a three-bed ward.', '2', 40, ((300, 165, 280), (700, 60, 700)), 'medical'


def room2w_archive():
    R = R_('room2w_archive')
    junction(R, 'NS', 'old', openings={'S_W': [door_op(-460)]})
    x0, z0, x1, z1 = annex(R, 'x', -192, -1, -800, -160, 560, 352, 'old', door=-460)
    cabinet_row(R, (x0 + 32, z0 + 20), (x0 + 32, z1 - 20), 0, 'E')
    t = shelf_unit(R, -700, z0 + 8, -320, z0 + 56, 0, height=250, levels=4)
    for lvl, sd in ((0, 61), (1, 62), (3, 63)):
        file_row(R, (-690, -330, z0 + 32), (0, 0, 0), t[lvl], 'x', seed=sd, fill=0.5)
    top = desk(R, -520, z1 - 90, -340, z1 - 20, 0)
    lamp(R, -520, -480, 352, power=88, rng=760)
    lamps(R, NS3, 384, power=86)
    roll(R, -430, top, z1 - 55)
    item(R, 'bat', -500, t[2], z0 + 32, 50)
    return R, 'A hallway with a records room: a wall of filing cabinets and shelves of box files.', '2', 45, ((-290, 165, -260), (-700, 100, -700)), 'office'


def room2w_boiler():
    R = R_('room2w_boiler')
    junction(R, 'NS', 'dark', hub=(-576, -512, 576, 512), hh=448)
    tank(R, -540, -480, -330, -260, 360)
    tank(R, 330, 260, 540, 480, 360)
    pipes_x(R, ((-300, 400, 22), (300, 404, 18)), -576, 576)
    for (vx, vz) in ((-380, 200), (380, -200)):
        R.add([V(vx - 44, 1.5, vz - 44), V(vx + 44, 1.5, vz - 44), V(vx + 44, 1.5, vz + 44), V(vx - 44, 1.5, vz + 44)],
              [(0, 1), (1, 1), (1, 0), (0, 0)], VENT, cast=False)
    ceil_fan(R, 0, 0, 448)
    red_lamp(R, -300, 320, 448)
    lamps(R, ((300, -320), (0, -720), (0, 720)), 448, power=72, color=(232, 238, 255), size=36)
    return R, 'A boiler hall: two tanks, pipes under the roof, a ceiling fan turning over the walkway.', '2', 45, ((0, 165, -900), (-100, 200, 0)), ''


def room2w_gallery():
    R = R_('room2w_gallery')
    junction(R, 'NS', 'old', hub=(-384, -640, 384, 640), hh=640)
    for s in (-1, 1):
        xa, xb = sorted((s * 384.0, s * 224.0))
        R.box(xa, 304, -640, xb, 320, 640, DIRTY, skip='NS' + ('W' if s < 0 else 'E'), lux=14)
        railing(R, (s * 224, -640), (s * 224, 640), 320)
        for z in (-400, 0, 400):
            wall_light(R, s * 384, z, 470, 'E' if s < 0 else 'W', power=58, rng=520)
    lamps(R, ((0, -330), (0, 330)), 640, power=96, rng=1100, size=64)
    return R, 'A high hall with a railed gallery down each side that nothing leads up to.', '2', 50, ((0, 165, -900), (0, 300, 0)), ''


def room2w_lockdown():
    R = R_('room2w_lockdown')
    w, ch = 224.0, 416.0
    junction(R, 'NS', 'hcz', w=w, ch=ch)
    hz = STYLES['haz'][0].but(us=256, vs=256)
    for z in (-300, 300):
        R.box(-w, 0, z - 48, -150, ch, z + 48, hz, skip='TBW', lux=12)
        R.box(150, 0, z - 48, w, ch, z + 48, hz, skip='TBE', lux=12)
        R.box(-150, 330, z - 48, 150, ch, z + 48, hz, skip='T', lux=12)
        red_lamp(R, 0, z, 330, power=96, rng=640)
    sign_at(R, 'hcz', -w, 0, 'E', 230, 32, 250, sheet='misc')
    lamps(R, ((0, -700), (0, 700)), ch, power=70, color=(232, 238, 255), size=36)
    return R, 'A lockdown section: two blast frames in hazard paint, red lamps under each.', '2', 45, VIEW, ''


def room2w_dclass():
    R = R_('room2w_dclass')
    junction(R, 'NS', 'white', openings={'hubW': [door_op(0)]})
    x0, z0, x1, z1 = annex(R, 'x', -192, -1, -180, 180, 340, 320, 'white', door=0)
    dd = Mat('dclass_door.jpg', 256, cast=False)
    for z in (-760, -470, 470, 760):
        R.decal((-192, z - 76), (-192, z + 76), 0, 304, dd, (0, 0, 1, 1))
        R.decal((192, z + 76), (192, z - 76), 0, 304, dd, (0, 0, 1, 1))
    R.model('dclass_bed.x', x0 + 70, 0, 50, size=(100, 80, 228))
    bench(R, 150, 0, 90)
    lamp(R, (x0 + x1) / 2, 0, 320, power=80, size=36)
    lamps(R, NS3, 384, power=88, color=(250, 250, 250), size=56)
    role(R, 'sitd', x1 - 70, 0, -110, 0)
    item(R, 'indevration', x0 + 70, 84, 0, 50)
    return R, 'A white Class-D block. One cell is open, and occupied.', '2', 40, VIEW, ''


def room2w_pumps():
    R = R_('room2w_pumps')
    w = 224.0
    junction(R, 'NS', 'std', w=w, openings={'hubW': [(-80.0, 80.0, 150.0, 310.0)]})
    for z in (-640, -360, 360, 640):
        tank(R, 120, z - 64, 214, z + 64, 220)
    pipes_z(R, ((168, 300, 16), (140, 330, 10)))
    wall_fan(R, 'x', -w, -1, 0, 230)
    lamps(R, ((-60, -520), (-60, 520)), 384, power=84)
    return R, 'A pump corridor: a row of small tanks under a pipe run, a duct fan in the wall.', '2', 50, ((-80, 165, -900), (60, 150, 0)), ''


# =====================================================================  corners (doors on -z and +x)
def room2cw_tight():
    R = R_('room2cw_tight')
    junction(R, 'SE', 'board', w=176, ch=336)
    lamps(R, ((0, 0), (0, -640), (640, 0)), 336, power=80)
    return R, 'A low, narrow board-marked corner.', '2C', 70, VIEW, ''


def room2cw_round():
    R = R_('room2cw_round')
    junction2(R, 'SE', 'old', hub=(-384, -384, 384, 384), cut=160, hh=448)
    lamp(R, 0, 0, 448, power=118, rng=1000, size=64)
    lamps(R, ((0, -700), (700, 0)), 384, power=76)
    return R, 'A corner opened out into an eight-sided room.', '2C', 60, VIEW, ''


def room2cw_tall():
    R = R_('room2cw_tall')
    junction(R, 'SE', 'std', hub=(-256, -256, 256, 256), hh=576)
    ibeam(R, 'z', 0, -256, 256, 470)
    ibeam(R, 'x', 0, -256, 256, 420)
    pendant(R, 0, 0, 576, power=132, rng=1000)
    lamps(R, ((0, -680), (680, 0)), 384, power=74)
    return R, 'A corner under a tall shaft crossed by two beams.', '2C', 55, ((0, 165, -900), (40, 260, 0)), ''


def room2cw_bench():
    R = R_('room2cw_bench')
    junction(R, 'SE', 'ez', hub=(-256, -256, 256, 256))
    bench(R, -216, 0, 90)
    vending(R, -120, 256, 'S')
    painting(R, 110, 256, 'S')
    lamps(R, ((0, 0), (0, -640), (640, 0)), 384, power=96, color=(255, 250, 240), size=64)
    item(R, 'indevwater', -216, 54, 0, 25)
    return R, 'An office-zone corner with a bench, a vending machine and a painting.', '2C', 55, ((60, 165, -700), (-80, 140, 250)), ''


def room2cw_guard():
    R = R_('room2cw_guard')
    win = (-160.0, 160.0, 112.0, 288.0)
    junction(R, 'SE', 'board', openings={'hubN': [win]})
    annex(R, 'z', 192, +1, -224, 224, 256, 320, 'board', window=win)
    lamp(R, 0, 384, 320, power=70, rng=520, color=(255, 225, 190))
    lamps(R, ((0, -640), (640, 0)), 384, power=80)
    role(R, 'guard', 0, 0, 380, 180)
    item(R, 'bat', -100, 112, 224, 40)
    return R, 'A corner watched from a guard hatch.', '2C', 40, ((60, 165, -560), (-20, 150, 300)), ''


def room2cw_store():
    R = R_('room2cw_store')
    junction(R, 'SE', 'old', openings={'hubW': [door_op(0)]})
    x0, z0, x1, z1 = annex(R, 'x', -192, -1, -260, 260, 400, 352, 'board', door=0)
    t = shelf_unit(R, x0 + 8, z0 + 20, x0 + 72, z1 - 20, 0, height=250, levels=4)
    crate(R, x1 - 110, 0, z1 - 90, yaw=8)
    lamp(R, (x0 + x1) / 2, 0, 352, power=84, rng=700)
    lamps(R, ((0, 0), (0, -640), (640, 0)), 384, power=84)
    item(R, 'bat', x0 + 40, t[1], -120, 70)
    item(R, 'indevration', x0 + 40, t[2], 60, 50)
    item(R, 'firstaid', x0 + 40, t[1], 160, 30)
    roll(R, x1 - 200, 0, -150)
    return R, 'A corner with a store cupboard off it.', '2C', 45, ((40, 165, -300), (-560, 110, 100)), 'storage'


def room2cw_pipes():
    R = R_('room2cw_pipes')
    w, ch = 176.0, 352.0
    junction(R, 'SE', 'dark', w=w, ch=ch, openings={'hubN': [(-80.0, 80.0, 150.0, 310.0)]})
    m = RUST.but(us=2 * math.pi * 20, vs=256)
    R.tube((-116, 306, -990), (-116, 306, 116), 20, m, sides=8, lux=16)
    R.tube((-116, 306, 116), (990, 306, 116), 20, m, sides=8, lux=16)
    wall_fan(R, 'z', w, +1, 0, 230)
    red_lamp(R, 0, 0, ch)
    lamps(R, ((0, -680), (680, 0)), ch, power=66, color=(232, 238, 255), size=36)
    return R, 'A dark service corner: a pipe following the bend, a duct fan, a red lamp.', '2C', 50, VIEW, ''


def room2cw_pillar():
    R = R_('room2cw_pillar')
    junction(R, 'SE', 'std', hub=(-448, -448, 448, 448), hh=448)
    for (x, z) in ((-250, 250), (250, 250), (-250, -250)):
        pillar(R, x, z, 448)
    lamps(R, ((0, 0), (-330, 0), (0, 330)), 448, power=86, rng=820)
    crate(R, -370, 0, 380, yaw=20)
    return R, 'A pillared corner hall.', '2C', 55, VIEW, ''


def room2cw_lab():
    R = R_('room2cw_lab')
    win = (120.0, 400.0, 96.0, 256.0)
    junction(R, 'SE', 'lab', hub=(-192, -192, 448, 192), openings={'hubN': [door_op(-60), win]})
    x0, z0, x1, z1 = annex(R, 'z', 192, +1, -192, 448, 420, 352, 'lab', door=-60, window=win)
    glaze(R, 'z', 192, +1, win)
    top = desk(R, 140, z1 - 90, 420, z1 - 20, 0)
    workstation(R, 280, top, z1 - 50, yaw=0)
    cabinet_row(R, (x0 + 32, z1 - 250), (x0 + 32, z1 - 30), 0, 'E')
    ceil_light(R, 130, 480, 352, size=96, power=136, rng=900)
    lamps(R, ((0, 0), (0, -640), (700, 0)), 384, power=96, color=(245, 250, 255), size=64)
    roll(R, 200, top, z1 - 55)
    return R, 'A white-tiled corner with a small glazed laboratory.', '2C', 40, ((300, 165, -150), (120, 110, 560)), 'testing'


def room2cw_cells():
    R = R_('room2cw_cells')
    junction(R, 'SE', 'white')
    dd = Mat('dclass_door.jpg', 256, cast=False)
    for z in (-760, -470):
        R.decal((-192, z - 76), (-192, z + 76), 0, 304, dd, (0, 0, 1, 1))
    for x in (470, 760):
        R.decal((x - 76, 192), (x + 76, 192), 0, 304, dd, (0, 0, 1, 1))
    bench(R, 150, -600, 90)
    lamps(R, ((0, 0), (0, -640), (640, 0)), 384, power=88, color=(250, 250, 250), size=56)
    return R, 'A white corner of the Class-D block.', '2C', 50, VIEW, ''


# =====================================================================  T junctions (doors on -z, +x, -x)
def room3w_narrow():
    R = R_('room3w_narrow')
    junction(R, 'SEW', 'board', w=176, ch=336)
    lamps(R, ((0, 0), (0, -640), (640, 0), (-640, 0)), 336, power=78)
    return R, 'A low, narrow board-marked T junction.', '3', 70, VIEW, ''


def room3w_wide():
    R = R_('room3w_wide')
    w, ch = 256.0, 416.0
    junction(R, 'SEW', 'old', w=w, ch=ch)
    lamp(R, 0, 0, ch, power=110, rng=900, size=64)
    lamps(R, ((0, -660), (660, 0), (-660, 0)), ch, power=80)
    bench(R, 0, 216, 0)
    return R, 'A broad early-pattern T junction with a bench on the blank wall.', '3', 70, VIEW, ''


def room3w_oct():
    R = R_('room3w_oct')
    junction2(R, 'SEW', 'std', hub=(-448, -448, 448, 448), cut=160, hh=480)
    ceil_fan(R, 0, 0, 480)
    lamps(R, ((-250, 250), (250, 250), (0, -250)), 480, power=84, rng=820)
    vents(R, 0, 448, 'S', n=3, gap=130)
    return R, 'A T junction in an eight-sided hall under a ceiling fan.', '3', 55, VIEW, ''


def room3w_office():
    R = R_('room3w_office')
    win = (-100.0, 340.0, 96.0, 256.0)
    junction(R, 'SEW', 'ez', hub=(-448, -192, 448, 192), openings={'hubN': [door_op(-300), win]})
    x0, z0, x1, z1 = annex(R, 'z', 192, +1, -448, 448, 440, 352, 'ez', door=-300, window=win)
    glaze(R, 'z', 192, +1, win)
    top = meeting(R, 130, 480, 'x')
    whiteboard(R, 130, z1, 'S')
    ceil_light(R, 0, 480, 352, size=96, power=118, rng=860)
    lamps(R, ((0, 0), (0, -640), (700, 0), (-700, 0)), 384, power=94, color=(255, 250, 240), size=64)
    role(R, 'sci', -330, 0, 560, 180)
    roll(R, 200, top, 480)
    return R, 'A T junction overlooked by a glazed conference room. Someone is still in there.', '3', 40, ((60, 165, -500), (100, 130, 500)), 'office'


def room3w_console():
    R = R_('room3w_console')
    win = (-340.0, 100.0, 96.0, 256.0)
    junction(R, 'SEW', 'old', hub=(-448, -192, 448, 192), openings={'hubN': [door_op(300), win]})
    x0, z0, x1, z1 = annex(R, 'z', 192, +1, -448, 448, 400, 352, 'old', door=300, window=win)
    glaze(R, 'z', 192, +1, win)
    console(R, -280, z1 - 40, 'S')
    console(R, -70, z1 - 40, 'S')
    bench(R, x1 - 40, 460, 90)
    wall_light(R, x0, 460, 260, 'E', power=58, rng=460)
    wall_light(R, 140, z1, 300, 'S', power=58, rng=460)
    lamps(R, ((0, 0), (0, -640), (700, 0), (-700, 0)), 384, power=84)
    roll(R, 100, 0, 420)
    return R, 'A T junction with a glazed control room: two console units and a bench.', '3', 40, ((60, 165, -500), (-160, 130, 560)), 'testing'


def room3w_beams():
    R = R_('room3w_beams')
    junction(R, 'SEW', 'board', hub=(-384, -384, 384, 384), hh=544)
    ibeam(R, 'z', -150, -384, 384, 470)
    ibeam(R, 'z', 150, -384, 384, 470)
    ibeam(R, 'x', -150, -384, 384, 420)
    ibeam(R, 'x', 150, -384, 384, 420)
    pendant(R, 0, 0, 544, power=136, rng=1050)
    return R, 'A T junction under a tall shaft crossed by steel beams.', '3', 55, ((0, 165, -900), (0, 250, 0)), ''


def room3w_store():
    R = R_('room3w_store')
    win = (-160.0, 160.0, 0.0, 300.0)
    junction(R, 'SEW', 'std', openings={'hubN': [win]})
    x0, z0, x1, z1 = annex(R, 'z', 192, +1, -260, 260, 300, 320, 'std', window=win)
    t = shelf_unit(R, x0 + 8, z1 - 60, x1 - 8, z1 - 6, 0, height=250, levels=4)
    crate(R, x1 - 90, 0, z0 + 100, yaw=-10)
    lamp(R, 0, (z0 + z1) / 2, 320, power=74, rng=540, size=36)
    lamps(R, ((0, 0), (0, -640), (640, 0), (-640, 0)), 384, power=80)
    item(R, 'bat', -150, t[1], z1 - 34, 70)
    item(R, '18vbat', 60, t[2], z1 - 34, 30)
    roll(R, -60, 0, z0 + 120)
    return R, 'A T junction with an open store alcove on the blank side.', '3', 50, ((0, 165, -640), (0, 140, 400)), 'storage'


def room3w_pillars():
    R = R_('room3w_pillars')
    junction(R, 'SEW', 'old', hub=(-512, -512, 512, 512), hh=448)
    for sx in (-1, 1):
        for sz in (-1, 1):
            pillar(R, sx * 260, sz * 260, 448, style='old')
    lamps(R, ((0, 0), (-380, 380), (380, 380)), 448, power=92, rng=900)
    return R, 'A T junction in a square hall with four pillars.', '3', 55, VIEW, ''


def room3w_pipes():
    R = R_('room3w_pipes')
    w, ch = 176.0, 352.0
    junction(R, 'SEW', 'dark', w=w, ch=ch, openings={'hubN': [(-80.0, 80.0, 150.0, 310.0)]})
    pipes_x(R, ((116, 306, 20), (140, 330, 10)))
    R.tube((-116, 306, -990), (-116, 306, 116), 16, RUST.but(us=100, vs=256), sides=8, lux=16)
    wall_fan(R, 'z', w, +1, 0, 230)
    red_lamp(R, 0, 0, ch)
    lamps(R, ((0, -680), (680, 0), (-680, 0)), ch, power=64, color=(232, 238, 255), size=36)
    return R, 'A dark service T junction with pipes, a duct fan and a red lamp.', '3', 50, VIEW, ''


# =====================================================================  crossroads
def room4w_narrow():
    R = R_('room4w_narrow')
    junction(R, 'NSEW', 'board', w=176, ch=336)
    lamps(R, ((0, 0), (0, -640), (0, 640), (640, 0), (-640, 0)), 336, power=76)
    return R, 'A low, narrow board-marked crossroads.', '4', 70, VIEW, ''


def room4w_oct():
    R = R_('room4w_oct')
    junction2(R, 'NSEW', 'old', hub=(-448, -448, 448, 448), cut=192, hh=512)
    pendant(R, 0, 0, 512, power=140, rng=1100)
    return R, 'A crossroads in an eight-sided hall under one hanging lamp.', '4', 60, ((0, 165, -900), (0, 220, 0)), ''


def room4w_pillars():
    R = R_('room4w_pillars')
    junction(R, 'NSEW', 'std', hub=(-512, -512, 512, 512), hh=448)
    for sx in (-1, 1):
        for sz in (-1, 1):
            pillar(R, sx * 290, sz * 290, 448)
    lamp(R, 0, 0, 448, power=112, rng=1000, size=64)
    lamps(R, ((-400, -400), (400, 400)), 448, power=70, rng=700, size=36)
    return R, 'A crossroads in a square hall with a pillar towards each corner.', '4', 60, VIEW, ''


def room4w_bridge():
    R = R_('room4w_bridge')
    junction(R, 'NSEW', 'std', hub=(-384, -384, 384, 384), hh=608)
    bridge(R, 'x', 0, -384, 384, y=352)
    lamps(R, ((-250, -250), (250, 250)), 608, power=104, rng=1100, size=64)
    for f, x, z in (('S', -260, 384), ('N', 260, -384), ('W', 384, -260), ('E', -384, 260)):
        wall_light(R, x, z, 250, f, power=50, rng=440)
    return R, 'A tall crossroads with a railed walkway passing overhead.', '4', 50, ((-250, 165, -860), (60, 260, 0)), ''


def room4w_fan():
    R = R_('room4w_fan')
    junction(R, 'NSEW', 'dark', hub=(-448, -448, 448, 448), hh=544)
    bigfan(R, 0, 500, 0, radius=220)
    for c in (-250, 250):
        ibeam(R, 'z', c, -448, 448, 500)
        ibeam(R, 'x', c, -448, 448, 500)
    R.add([V(-128, 1.5, -128), V(128, 1.5, -128), V(128, 1.5, 128), V(-128, 1.5, 128)],
          [(0, 0), (2, 0), (2, 2), (0, 2)], GRATE, cast=False)
    for (x, z) in ((-330, -330), (330, 330)):
        lamp(R, x, z, 544, power=84, rng=900, color=(225, 235, 255), size=48)
    R.light(0, 440, 0, rng=900, color=(220, 232, 255), power=70, ent=False)
    return R, 'A dark crossroads under a big extractor fan framed by beams.', '4', 50, ((-200, 165, -860), (40, 300, 0)), ''


def room4w_dome():
    R = R_('room4w_dome')
    junction2(R, 'NSEW', 'old', hub=(-512, -512, 512, 512), cut=256, hh=640)
    ibeam(R, 'z', 0, -512, 512, 540)
    ibeam(R, 'x', 0, -512, 512, 500)
    pendant(R, 0, 0, 640, power=150, rng=1300)
    lamps(R, ((-260, -260), (260, 260), (-260, 260), (260, -260)), 640, power=60, rng=900, size=36)
    return R, 'A crossroads in a tall eight-sided hall.', '4', 55, ((0, 165, -900), (0, 280, 0)), ''


# =====================================================================  dead ends (door on -z)
def room1w_consoles():
    R = R_('room1w_consoles')
    junction(R, 'S', 'old', hub=(-448, -320, 448, 448), hh=352)
    console(R, -120, 408, 'S')
    console(R, 80, 408, 'S')
    bench(R, 330, 410, 0)
    wall_light(R, -448, 60, 270, 'E', power=60, rng=480)
    wall_light(R, 20, 448, 310, 'S', power=60, rng=480)
    wall_light(R, 448, 60, 270, 'W', power=60, rng=480)
    lamp(R, 0, -720, 384, power=74)
    R.waypoint(0, 66, -100)
    roll(R, -300, 0, 200)
    item(R, 'bat', 330, 54, 410, 50)
    return R, 'A dead-end control room: two console units against the wall, a bench, three wall lamps.', '1', 70, ((-360, 165, -240), (60, 110, 420)), 'testing'


def room1w_meeting():
    R = R_('room1w_meeting')
    junction(R, 'S', 'old', hub=(-400, -320, 400, 480), hh=336)
    top = meeting(R, 0, 110, 'z')
    whiteboard(R, 0, 480, 'S', yc=180)
    ceil_vent(R, 0, 110, 336)
    lamp(R, -220, 300, 336, power=80, rng=760)
    lamp(R, 0, -720, 384, power=74)
    R.waypoint(0, 66, -200)
    roll(R, 30, top, 180)
    return R, 'A dead-end meeting room: a long table, white chairs, a whiteboard, a red book left open.', '1', 60, ((-40, 165, -300), (20, 110, 470)), 'office'


def room1w_whitedoor():
    R = R_('room1w_whitedoor', amb=8)
    junction(R, 'S', 'old', hub=(-448, -320, 448, 512), hh=352)
    glow_door(R, 0, 512, 'S')
    vents(R, -448, 80, 'E', n=2, gap=130, yc=110, size=90)
    cabinet_row(R, (416, 100), (416, 400), 0, 'W')
    top = table(R, -150, -200, 150, -40, top=Mat('white.jpg', 256))
    book(R, 90, top, -110)
    lamp(R, 0, -720, 384, power=64)
    R.waypoint(0, 66, -250)
    roll(R, -60, top, -120)
    return R, 'A dark room at the end of a passage. In the far wall there is a doorway of white light with nothing behind it.', '1', 45, ((0, 190, -300), (0, 150, 500)), 'office'


def room1w_ward():
    R = R_('room1w_ward')
    junction(R, 'S', 'med', hub=(-448, -320, 448, 512), hh=352)
    beds(R, -440, -250, (-180, 20, 220, 420))
    beds(R, 250, 440, (120, 360))
    cabinet(R, 416, -240, 0, 'W')
    ceil_fan(R, 0, 120, 352)
    lamps(R, ((-150, 300), (150, -100)), 352, power=96, rng=860, color=(240, 250, 240))
    lamp(R, 0, -720, 384, power=74)
    R.waypoint(0, 66, -200)
    role(R, 'lie', 60, 0, 260, 30)
    item(R, 'firstaid', -345, 58, 20, 80)
    item(R, 'syringe', 345, 58, 120, 50)
    roll(R, 416, 180, -240)
    return R, 'A dead-end ward: six beds under a ceiling fan, and someone who did not make it out.', '1', 55, ((0, 165, -300), (-60, 80, 400)), 'medical'


def room1w_cache():
    R = R_('room1w_cache')
    AW = wmat('dark', 384)
    junction(R, 'S', 'dark', hub=(-320, -320, 320, 448), hh=384, openings={'hubE': [door_op(200)]})
    lift(R, 320, +1, 200, 0, 200, DEEP, AW)
    bw = wmat('std', 384).but(v0=DEEP + 384)
    out = [(-448, -100), (-448, 500), (320, 500), (320, -100)]
    R.walls(out, DEEP, DEEP + 384, bw, holes={2: [span(out[2], (320, 296), (320, 104)) + (DEEP, DEEP + 320)]})
    R.rect_floor(-448, -100, 320, 500, DEEP, CONC)
    R.rect_ceil(-448, -100, 320, 500, DEEP + 384, DIRTY)
    t = shelf_unit(R, -440, -60, -376, 460, DEEP, height=250, levels=4)
    t2 = shelf_unit(R, -300, 444, 100, 492, DEEP, height=250, levels=4)
    crate(R, -200, DEEP, 60, yaw=12)
    crate(R, -40, DEEP, 20, yaw=-18, kind=2)
    ceil_light(R, -100, 220, DEEP + 384, size=64, power=100, rng=860, color=(255, 236, 206))
    crate(R, -220, 0, 330, yaw=20)
    lamp(R, 0, 100, 384, power=84, color=(232, 238, 255))
    lamp(R, 0, -720, 384, power=70, color=(232, 238, 255), size=36)
    R.waypoint(0, 66, -100)
    sign_at(R, 'elevator', 320, -60, 'W', 150, 50, 250)
    item(R, 'bat', -408, t[1], 60, 100)
    item(R, 'firstaid', -408, t[2], 240, 60)
    item(R, 'nvgoggles', -408, t[1], 380, 20)
    item(R, 'key3', -150, t2[1], 468, 25)
    item(R, '18vbat', 20, t2[2], 468, 50)
    roll(R, -100, DEEP, 300)
    return R, 'A dead-end lobby with a lift down to a supply cache.', '1', 40, ((0, 165, -640), (150, 150, 250)), 'storage'


def room1w_tank():
    R = R_('room1w_tank')
    junction(R, 'S', 'hcz', hub=(-512, -384, 512, 576), hh=576, openings={'hubW': [(20.0, 180.0, 330.0, 490.0)]})
    tm = TANKM.but(us=2 * math.pi * 150 / 4, vs=440, v0=440)
    R.tube((0, 0, 150), (0, 440, 150), 150, tm, sides=14, caps=True, lux=14)
    R.box(-170, 0, -20, 170, 26, 320, DARK, skip='B', lux=12)
    m = RUST.but(us=120, vs=256)
    R.tube((0, 380, 150), (512, 380, 150), 22, m, sides=8, lux=16)
    R.tube((0, 300, 150), (0, 300, 576), 18, m, sides=8, lux=16)
    R.tube((-512, 200, -200), (-100, 200, 60), 16, m, sides=8, lux=16)
    wall_fan(R, 'x', -512, -1, 100, 410)
    red_lamp(R, 0, -200, 576, power=130, rng=1000)
    lamps(R, ((-330, 400), (330, 400)), 576, power=86, rng=1000, color=(232, 238, 255), size=48)
    lamp(R, 0, -720, 384, power=70, color=(232, 238, 255), size=36)
    R.waypoint(0, 66, -200)
    role(R, 'tech', -320, 0, -180, 60)
    top = desk(R, 300, -340, 470, -270, 0)
    item(R, 'gasmask', 380, top, -305, 40)
    item(R, 'bat', 440, top, -305, 60)
    return R, 'A dead-end plant room built round a coolant tank. A technician has stayed with it.', '1', 45, ((-380, 165, -330), (60, 220, 200)), ''


ALL = [room2w_narrow, room2w_wide, room2w_tall, room2w_ribs, room2w_oct, room2w_consoles, room2w_meeting,
       room2w_whitedoor, room2w_canteen, room2w_lab, room2w_generator, room2w_bridge, room2w_mezz, room2w_lift2,
       room2w_dogleg, room2w_checkpoint, room2w_cages, room2w_infirm, room2w_archive, room2w_boiler, room2w_gallery,
       room2w_lockdown, room2w_dclass, room2w_pumps,
       room2cw_tight, room2cw_round, room2cw_tall, room2cw_bench, room2cw_guard, room2cw_store, room2cw_pipes,
       room2cw_pillar, room2cw_lab, room2cw_cells,
       room3w_narrow, room3w_wide, room3w_oct, room3w_office, room3w_console, room3w_beams, room3w_store,
       room3w_pillars, room3w_pipes,
       room4w_narrow, room4w_oct, room4w_pillars, room4w_bridge, room4w_fan, room4w_dome,
       room1w_consoles, room1w_meeting, room1w_whitedoor, room1w_ward, room1w_cache, room1w_tank]
assert len(ALL) == 55
