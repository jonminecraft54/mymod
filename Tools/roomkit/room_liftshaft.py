"""room2liftshaft - "Maintenance Shaft 4" (Indev zone, two doors).
Reference shots (second set) 8, 10: a concrete corridor with a red pendant lamp and a freight lift,
and a tall shaft crossed by pipes with chains hanging off them, a balcony rail high on one side,
dark vapour on the floor and a red glow by the lift door at the bottom."""
from parts import *

LOW = -704.0
TOP = 640.0


def build():
    R = Room('room2liftshaft', luxel=12, ambient=8, fill=0.12)
    A = {}
    CH = 384.0
    W = HCZWALL
    SW = HCZWALL.but(v0=TOP, vs=448)
    FL = LCZFLOOR
    ZC = -320.0

    # ---- corridor (grid level)
    R.rect_floor(-192, -992, 192, 992, 0, FL)
    R.rect_ceil(-192, -992, 192, 992, CH, DIRTY)
    end_wall(R, 'N', -192, 192, CH, W, FL)
    end_wall(R, 'S', -192, 192, CH, W, FL)
    R.wall((-192, -992), (-192, -480), 0, CH, W)
    R.wall((-192, 480), (-192, 992), 0, CH, W)
    a = (192, 992)
    R.wall(a, (192, -992), 0, CH, W, holes=[span(a, (192, ZC + 96), (192, ZC - 96)) + (0, 320)])
    railing(R, (-192, -480), (-192, 480), 0)
    R.wall((-192, 480), (-192, -480), -32, 0, DARK)                 # slab edge seen from the shaft
    R.rect_ceil(-192, -480, 192, 480, -32, DIRTY)

    # ---- the shaft and the room at its foot (which runs under the corridor to the lift)
    R.rect_floor(-832, -480, 192, 480, LOW, FL)
    R.rect_ceil(-832, -480, -192, 480, TOP, DIRTY)
    R.wall((-832, -480), (-832, 480), LOW, TOP, SW)
    R.wall((-832, 480), (-192, 480), LOW, TOP, SW)
    R.wall((-192, 480), (192, 480), LOW, -32, SW)
    R.wall((192, -480), (-192, -480), LOW, -32, SW)
    R.wall((-192, -480), (-832, -480), LOW, TOP, SW)
    R.wall((-192, 480), (-192, -480), CH, TOP, SW)                  # above the corridor opening
    a = (192, 480)
    R.wall(a, (192, -480), LOW, -32, SW, holes=[span(a, (192, ZC + 96), (192, ZC - 96)) + (LOW, LOW + 320)])

    # ---- the lift: two stops stacked 704 apart
    A['elev_hi_door'], A['elev_hi_pivot'] = elevator(R, 192, ZC, 0, +1, W)
    A['elev_lo_door'], A['elev_lo_pivot'] = elevator(R, 192, ZC, LOW, +1, W)

    # ---- pipes across the shaft, chains hanging off them
    def pipe(p0, p1, r):
        R.tube(p0, p1, r, RUST.but(us=2 * math.pi * r, vs=256), sides=8, lux=16)
    runs = [(-420, -260, 30), (-600, 20, 24), (-340, 250, 22), (-680, -470, 28), (-520, 440, 20)]
    for (x, y, r) in runs:
        pipe((x, y, -480), (x, y, 480), r)
    pipe((-832, 120, 260), (-192, 120, 260), 18)
    pipe((-832, -360, -300), (-192, -360, -300), 18)
    import random
    rng = random.Random(4)
    for (x, y, r) in runs[:4]:
        for z in (-330, -150, 60, 240, 390):
            if rng.random() < 0.6:
                chain(R, x, z + rng.randint(-20, 20), y - r, min(rng.choice((180, 260, 340)), (y - r) - (LOW + 40)))
    A['fan'] = (-512, 590, 0)
    R.sound(-512, 560, 0, 4, 9.0)

    # ---- the foot of the shaft: stores, crates, vapour vents
    t1 = shelf_unit(R, -824, -440, -764, -120, LOW, height=250, levels=4)
    t2 = shelf_unit(R, -640, 424, -340, 472, LOW, height=250, levels=4)
    A['shelf_a'] = (-794, t1[1] + 4, -360)
    A['shelf_b'] = (-794, t1[2] + 4, -200)
    A['shelf_c'] = (-560, t2[1] + 4, 448)
    A['shelf_d'] = (-420, t2[2] + 4, 448)
    file_row(R, (-430, -130, -794), (0, 0, 0), t1[3], 'z', seed=71, fill=0.5)
    crate(R, -740, LOW, 250, yaw=12)
    crate(R, -690, LOW, 390, yaw=-20)
    crate(R, -720, LOW + 78, 300, yaw=40, kind=2)
    A['pod'] = (-610, LOW, 330)
    A['vent_a'] = (-470, LOW + 10, -120)
    A['vent_b'] = (-600, LOW + 10, 120)
    for (vx, vz) in ((-470, -120), (-600, 120)):
        R.add([V(vx - 40, LOW + 1.5, vz - 40), V(vx + 40, LOW + 1.5, vz - 40), V(vx + 40, LOW + 1.5, vz + 40),
               V(vx - 40, LOW + 1.5, vz + 40)], [(0, 1), (1, 1), (1, 0), (0, 0)], VENT, cast=False)
    top = desk(R, -120, 380, 60, 450, LOW)
    A['desk_a'] = (-70, top + 4, 415)
    A['desk_b'] = (10, top + 4, 415)

    # ---- lights: cold light from the fan well, red lamp by the lower lift door, pendants upstairs
    for (x, z) in ((-700, -340), (-320, 340)):
        ceil_light(R, x, z, TOP, size=96, power=120, rng=1500, color=(215, 230, 255))
    R.box(150, LOW + 330, ZC - 22, 192, LOW + 356, ZC + 22, REDLAMP, skip='E')
    R.light(120, LOW + 300, ZC, rng=900, color=(255, 52, 40), power=140)
    ceil_light(R, 0, 200, -32, size=48, power=60, rng=620, color=(255, 235, 210))
    pendant(R, 0, -720, CH, power=130, rng=820)
    pendant(R, 0, 720, CH, power=130, rng=820)
    wall_light(R, 192, 0, 250, 'W', power=60, rng=460)

    # ---- signs
    sign2(R, 'shaft4', 192, 330, 'W', 300, 76, 250)
    sign2(R, 'freight', 192, ZC - 240, 'W', 150, 56, 250)
    sign2(R, 'b2', 192, ZC - 250, 'W', 60, 46, LOW + 250)

    for z in (-700, 0, 700):
        R.waypoint(0, 66, z)
    return R, A


if __name__ == '__main__':
    import time
    t = time.time()
    R, A = build()
    R.bake()
    print('bake %.1fs' % (time.time() - t))
    R.export('out')
    R.topview('out/liftshaft_top.png', y_cut=(-10, 380))
    R.render((0, 165, -940), (-60, 150, 0), 'out/liftshaft_1.png')
    R.render((120, LOW + 165, -200), (-700, LOW + 500, 200), 'out/liftshaft_2.png')
    R.render((-100, 165, 200), (-600, -500, -100), 'out/liftshaft_3.png')
    for k, v in A.items():
        print('  ', k, v)
