"""room1store4 - "Stores 4" (Indev zone, dead end: door on -z).
Reference shots (second set) 5, 15, 17: a dim brick storeroom - a row of stalls with half-height
fronts and one door ajar, open shelving, a long green crate on the floor, a hooded lamp, and a
closet nook with dark shelves."""
from parts import *


def build():
    R = Room('room1store4', luxel=10, ambient=9, fill=0.13)
    A = {}
    H = 352.0
    W = BRICK.but(v0=H, vs=352)
    FL = LCZFLOOR

    # ---- entry neck
    R.rect_floor(-192, -992, 192, -736, 0, FL)
    R.rect_ceil(-192, -992, 192, -736, H, DIRTY)
    R.wall((-192, -992), (-192, -736), 0, H, W)
    R.wall((192, -736), (192, -992), 0, H, W)
    end_wall(R, 'S', -192, 192, H, W, FL)

    # ---- the store
    out = [(-640, -736), (-640, 640), (640, 640), (640, -736)]
    R.walls(out, 0, H, W, holes={3: [span(out[3], (192, -736), (-192, -736)) + (0, H)]})
    R.rect_floor(-640, -736, 640, 640, 0, FL)
    R.rect_ceil(-640, -736, 640, 640, H, DIRTY)
    for i in range(4):
        pa, pb = np.array(out[i], dtype=float), np.array(out[(i + 1) % 4], dtype=float)
        if i == 3:
            R.decal(pa, (192, -736), 0, 24, DARK, (0, 0.62, 3, 0.70), off=2)
            R.decal((-192, -736), pb, 0, 24, DARK, (0, 0.62, 3, 0.70), off=2)
        else:
            R.decal(pa, pb, 0, 24, DARK, (0, 0.62, 8, 0.70), off=2)

    # ---- the stalls along the north wall (reference shot 5)
    ZF = 300.0                                    # stall fronts
    PAN = PANELS2.but(us=192, vs=208, v0=208)
    for x in (-256, 128, 512):                    # dividers, with a post up to the ceiling
        R.box(x - 8, 0, ZF, x + 8, 208, 640, PAN, skip='BN')
        R.box(x - 10, 0, ZF - 10, x + 10, H, ZF + 10, DARK, skip='TB', lux=10)
    R.box(-640, 0, ZF - 10, -620, H, ZF + 10, DARK, skip='TBW', lux=10)
    for (x0, x1) in ((-640, -256), (-256, 128), (128, 512)):
        gap0 = x0 + 150                           # each front: low wall, a doorway, low wall
        gap1 = gap0 + 104
        R.box(x0 + 8, 0, ZF - 6, gap0, 128, ZF + 6, PAN.but(vs=128, v0=128), skip='B')
        R.box(gap1, 0, ZF - 6, x1 - 8, 128, ZF + 6, PAN.but(vs=128, v0=128), skip='B')
        R.box(x0 + 8, 196, ZF - 5, x1 - 8, 208, ZF + 5, DARK, lux=10)
    # the stall door left ajar (middle stall)
    R.obox((-112, 100, ZF - 58), (0, 0, 50), (0, 100, 0), (4, 0, 0), PAN.but(us=104, vs=200, v0=200), lux=10)
    # in the stalls
    t1 = shelf_unit(R, -630, 560, -290, 630, 0, height=250, levels=4)
    A['stall_a1'] = (-560, t1[1] + 4, 596)
    A['stall_a2'] = (-400, t1[2] + 4, 596)
    file_row(R, (-620, -300, 596), (0, 0, 0), t1[3], 'x', seed=81, fill=0.5)
    crate(R, -64, 0, 520, yaw=6)
    A['crate'] = (-64, 60, 500)
    A['crate_drop'] = (-64, 10, 400)
    t3 = shelf_unit(R, 150, 560, 490, 630, 0, height=250, levels=4)
    A['stall_c1'] = (230, t3[1] + 4, 596)
    A['stall_c2'] = (400, t3[2] + 4, 596)
    file_row(R, (160, 480, 596), (0, 0, 0), t3[0], 'x', seed=82, fill=0.5)

    # ---- the closet nook at the east end (reference shot 15): dark shelving, wall to wall
    for y in (60, 130, 200, 270):
        R.box(524, y - 6, 420, 636, y, 636, DARK, lux=10)
    R.box(524, 0, 414, 532, 290, 422, DARK, skip='B', lux=10)
    A['nook_a'] = (580, 134, 520)
    A['nook_b'] = (580, 204, 580)

    # ---- open shelving and the long crate along the west wall (reference shot 17)
    t4 = shelf_unit(R, -632, -500, -568, -180, 0, height=270, levels=5)
    t5 = shelf_unit(R, -632, -160, -568, 160, 0, height=270, levels=5)
    A['west_a'] = (-600, t4[1] + 4, -420)
    A['west_b'] = (-600, t4[2] + 4, -260)
    A['west_c'] = (-600, t5[1] + 4, 60)
    file_row(R, (-150, 150, -600), (0, 0, 0), t5[3], 'z', seed=83, fill=0.5)
    R.box(-420, 0, -690, -160, 44, -610, Mat('metal_darker.jpg', 256), skip='B')
    R.box(-380, 44, -684, -250, 96, -618, WOOD, skip='B')
    crate(R, 470, 0, -560, yaw=-14, kind=2)
    crate(R, 520, 0, -420, yaw=22)
    top = desk(R, 300, -700, 520, -630, 0)
    A['desk_a'] = (360, top + 4, -665)
    A['desk_b'] = (460, top + 4, -665)

    # ---- ceiling fan, hooded lamps
    R.box(-2, 300, -202, 2, H, -198, DIRTY, skip='TB', lux=8)
    A['ceilfan'] = (0, 294, -200)
    pendant(R, -330, 60, H, power=128, rng=860, color=(255, 232, 200))
    pendant(R, 300, -260, H, power=128, rng=860, color=(255, 232, 200))
    ceil_light(R, 0, -864, H, size=48, power=66, rng=520, color=(255, 236, 210))
    wall_light(R, 320, 640, 250, 'S', power=58, rng=420)

    # ---- signs
    sign2(R, 'stores4', -430, -736, 'N', 200, 80, 260)
    sign2(R, 'pry', 430, -736, 'N', 300, 38, 280)

    R.waypoint(0, 66, -860)
    R.waypoint(0, 66, -300)
    return R, A


if __name__ == '__main__':
    import time
    t = time.time()
    R, A = build()
    R.bake()
    print('bake %.1fs' % (time.time() - t))
    R.export('out')
    R.topview('out/store4_top.png')
    R.render((0, 165, -700), (-100, 120, 400), 'out/store4_1.png')
    R.render((500, 165, 100), (-500, 100, 500), 'out/store4_2.png')
    R.render((300, 165, 100), (-640, 100, -400), 'out/store4_3.png')
    for k, v in A.items():
        print('  ', k, v)
