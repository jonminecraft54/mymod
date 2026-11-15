"""room2ventcore - "Ventilation Core / SCP-015 annex" (HCZ, two doors).
Reference shots 5, 6: a heavy-containment tunnel lined with locker bays that opens into a dark
plant hall - checker-plate floor, concrete piers, big pipes, tall white-and-yellow tanks, red
emergency light and a column of black smoke."""
from parts import *

FLOOR = HCZFLOOR
RUST = Mat('Pipes.jpg', 256, 256)
RED = Mat('red.jpg', 64, emit=210, cast=False)


def build():
    R = Room('room2ventcore', luxel=10, ambient=11, fill=0.13)
    A = {}
    TH, HH = 384.0, 608.0
    W = HCZWALL

    # ---- the plant hall
    hall = [(-704, -448), (-704, 448), (704, 448), (704, -448)]
    holes = {
        0: [span(hall[0], (-704, -160), (-704, 160)) + (160, 480)],            # fan duct
        1: [span(hall[1], (-256, 448), (256, 448)) + (0, TH)],                 # north tunnel mouth
        3: [span(hall[3], (256, -448), (-256, -448)) + (0, TH)],               # south tunnel mouth
    }
    R.walls(hall, 0, HH, W.but(v0=768), holes=holes)
    R.rect_floor(-704, -448, 704, 448, 0, FLOOR)
    R.rect_ceil(-704, -448, 704, 448, HH, DIRTY)

    # ---- the two tunnels with their locker bays (reference shot 6)
    for sgn, side in ((1, 'N'), (-1, 'S')):
        z0, z1 = sorted((sgn * 448.0, sgn * 992.0))
        R.rect_floor(-256, z0, 256, z1, 0, FLOOR)
        R.rect_ceil(-256, z0, 256, z1, TH, DIRTY)
        R.wall((-256, z0), (-256, z1), 0, TH, W)
        R.wall((256, z1), (256, z0), 0, TH, W)
        end_wall(R, side, -256, 256, TH, W, FLOOR)
        for zc in (sgn * 560.0, sgn * 720.0, sgn * 880.0):
            for sx in (-1, 1):
                x0, x1 = sorted((sx * 256.0, sx * 228.0))
                R.box(x0, 0, zc - 44, x1, 320, zc + 44, PANELS2.but(us=176, vs=320, v0=320), skip='B' + ('W' if sx < 0 else 'E'))
    A['locker_a'] = (-226, 150, -720)
    A['locker_b'] = (226, 150, -720)
    A['locker_c'] = (226, 150, 720)

    # ---- extraction fan duct in the west wall
    R.rect_floor(-880, -160, -704, 160, 160, DARK)
    R.rect_ceil(-880, -160, -704, 160, 480, DARK)
    R.wall((-704, -160), (-880, -160), 160, 480, DARK)
    R.wall((-880, 160), (-704, 160), 160, 480, DARK)
    R.quad(V(-880, 160, -160), V(-880, 160, 160), V(-880, 480, 160), V(-880, 480, -160), VENT, uvrect=(0, 0, 2, 2))
    for (y0, y1, z0, z1) in ((144, 160, -176, 176), (480, 496, -176, 176), (160, 480, -176, -160), (160, 480, 160, 176)):
        R.box(-704, y0, z0, -692, y1, z1, Mat('yellowmetal.jpg', 64), skip='W', lux=8)
    A['fan'] = (-790, 320, 0)
    R.sound(-760, 320, 0, 4, 6.0)

    # ---- concrete piers (reference shot 5)
    for (px, pz) in ((-180, 190), (180, -190)):
        R.box(px - 48, 0, pz - 48, px + 48, HH, pz + 48, W.but(us=192), skip='TB')
        R.box(px - 56, 0, pz - 56, px + 56, 40, pz + 56, DARK, skip='B', lux=8)
        R.box(px - 56, 300, pz - 56, px + 56, 330, pz + 56, DARK, lux=8)

    # ---- tanks: tall white-over-yellow units (metalpanels2)
    TANK = PANELS2.but(us=256, vs=336, v0=336)
    R.box(-690, 0, -436, -470, 336, -250, TANK, skip='B')
    R.box(-690, 0, 250, -470, 336, 436, TANK, skip='B')
    R.box(300, 0, -436, 560, 336, -300, TANK, skip='B')

    # ---- SCP-015: the pipe mass that has grown through the east side of the hall
    def pipe(p0, p1, r, sides=10):
        R.tube(p0, p1, r, RUST.but(us=2 * math.pi * r, vs=256), sides=sides, lux=14)
    pipe((640, 120, -448), (640, 120, 448), 58)                 # main along the east wall
    pipe((640, 300, -448), (640, 300, 448), 36)
    pipe((600, 0, 300), (600, HH, 300), 40)                     # risers
    pipe((520, 0, 380), (520, HH, 380), 26)
    pipe((660, 0, -330), (660, HH, -330), 30)
    pipe((704, 220, 60), (420, 220, 60), 44)                    # stub that ends in the hall - the leaking one
    pipe((420, 220, 60), (360, 60, 150), 44)
    pipe((360, 60, 150), (300, 0, 240), 44)
    pipe((704, 430, -150), (330, 520, -260), 22)                # the ones that make no sense
    pipe((704, 90, 250), (450, 608, 420), 18)
    pipe((560, 0, -120), (700, 500, 20), 20)
    pipe((704, 500, 380), (250, 560, 448), 16)
    pipe((480, 0, 200), (704, 380, 330), 14)
    pipe((704, 560, -60), (500, 608, 140), 30)
    pipe((640, 178, -200), (540, 178, -200), 14)                # valve stub
    A['valve'] = (536, 178, -200)
    A['smoke_a'] = (330, 30, 200)
    A['smoke_b'] = (420, 230, 60)
    A['smoke_c'] = (520, 40, -60)
    A['burst'] = (470, 190, 60)
    R.sound(560, 200, 0, 8, 5.0)

    # ---- observation desk on the safe (west) side, where the papers are
    top = desk(R, -420, 330, -260, 410, 0)
    A['desk_a'] = (-380, top + 4, 370)
    A['desk_b'] = (-300, top + 4, 370)
    A['lever'] = (-440, 190, -442)
    crate(R, -600, 0, -120, yaw=15)
    crate(R, -610, 0, 20, yaw=-8, kind=2)
    A['npc'] = (-540, 0, 150)

    # ---- lights: one white lamp on the west side, red emergency lamps over the pipes
    ceil_light(R, -420, -120, HH, size=64, power=105, rng=900, color=(235, 240, 255))
    for (x, z) in ((330, 250), (330, -250)):
        R.box(x - 22, HH - 26, z - 22, x + 22, HH, z + 22, RED, skip='T')
        R.light(x, HH - 60, z, rng=1150, color=(255, 52, 40), power=165)
    ceil_light(R, 0, -720, TH, size=48, power=72, rng=640, color=(255, 240, 220))
    ceil_light(R, 0, 720, TH, size=48, power=72, rng=640, color=(255, 240, 220))

    # ---- signs
    sign_at(R, 'ventcore', -480, 448, 'S', 300, 76, 420)
    sign_at(R, 'fanstart', -440, -448, 'N', 150, 60, 290)
    sign_at(R, 'm_mask', 256, -640, 'W', 84, 84, 210)
    sign_at(R, 'm_mask', -256, 640, 'E', 84, 84, 210)
    sign_at(R, 'l_015', 430, -448, 'N', 190, 95, 400)
    sign_at(R, 'd_tools', 610, -448, 'N', 100, 100, 400)

    for z in (-720, 0, 720):
        R.waypoint(0, 40, z)
    return R, A


if __name__ == '__main__':
    import time
    t = time.time()
    R, A = build()
    R.bake()
    print('bake %.1fs' % (time.time() - t))
    R.export('out')
    R.topview('out/ventcore_top.png')
    R.render((0, 165, -940), (0, 150, 0), 'out/ventcore_1.png')
    R.render((-520, 165, 300), (500, 180, -100), 'out/ventcore_2.png', bright=1.0)
    R.render((120, 165, -380), (-760, 300, 60), 'out/ventcore_3.png')
    for k, v in A.items():
        print('  ', k, v)
