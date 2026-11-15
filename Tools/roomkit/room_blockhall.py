"""room2blockhall - "Containment Block D" / SCP-017 (Indev zone, two doors).
Reference shots (second set) 1, 3, 11: a big unlit hall with a concrete block standing in a sunken
floor, a row of lamps and a row of vents on each face of the block, concrete-sided ramps running
down either side, and railed walkways along the walls with small wall lamps."""
from parts import *

PIT = -256.0
H = 448.0


def build():
    R = Room('room2blockhall', luxel=12, ambient=8, fill=0.12)
    A = {}
    W = HCZWALL.but(v0=H, vs=448)
    PW = HCZWALL.but(v0=0, vs=256)
    FL = LCZFLOOR

    # ---- shell: landings north and south, walkways east and west, the pit between them
    end_wall(R, 'S', -896, 896, H, W, FL)
    end_wall(R, 'N', -896, 896, H, W, FL)
    R.wall((-896, -992), (-896, 992), 0, H, W)
    R.wall((896, 992), (896, -992), 0, H, W)
    R.rect_ceil(-896, -992, 896, 992, H, DIRTY)
    R.rect_floor(-896, -992, 896, -640, 0, FL)
    R.rect_floor(-896, 640, 896, 992, 0, FL)
    R.rect_floor(-896, -640, -672, 640, 0, HCZFLOOR)
    R.rect_floor(672, -640, 896, 640, 0, HCZFLOOR)
    R.rect_floor(-672, -640, 672, 640, PIT, FL)
    R.wall((480, -640), (-480, -640), PIT, 0, PW)
    R.wall((-672, 640), (672, 640), PIT, 0, PW)
    R.wall((-672, -640), (-672, 640), PIT, 0, PW)
    R.wall((672, 640), (672, -640), PIT, 0, PW)

    # ---- the two ramps down from the south landing, each with a concrete side wall
    for sx in (-1, 1):
        xa, xb = sorted((sx * 672.0, sx * 480.0))
        R.add([V(xa, 0, -640), V(xb, 0, -640), V(xb, PIT, -64), V(xa, PIT, -64)],
              [(xa / 256, 0), (xb / 256, 0), (xb / 256, 2.46), (xa / 256, 2.46)], FL)
        xi = sx * 480.0
        poly_facing(R, [V(xi, 0, -640), V(xi, PIT, -640), V(xi, PIT, -64)], (-sx, 0, 0), PW)
        ay = norm(V(0, 576, 256)) * 44
        R.obox(V(sx * 500.0, -128, -352) + ay, (0, -128, 288), ay, (20, 0, 0), DARK, lux=12)
        R.box(sx * 500 - 26, PIT, -64, sx * 500 + 26, PIT + 100, -20, DARK, skip='B', lux=10)
        R.box(sx * 500 - 26, 0, -676, sx * 500 + 26, 100, -640, DARK, skip='B', lux=10)

    # ---- railings round the pit
    railing(R, (-474, -640), (474, -640), 0)
    railing(R, (-672, 640), (672, 640), 0)
    railing(R, (-672, -640), (-672, 640), 0)
    railing(R, (672, -640), (672, 640), 0)

    # ---- the block: 576 square, floor of the pit to the ceiling
    B = 288.0
    blk = [(-B, -B), (B, -B), (B, B), (-B, B)]             # outward walls: counter-clockwise from above
    a = blk[0]
    R.wall(blk[0], blk[1], PIT, H, W, holes=[span(a, (-96, -B), (96, -B)) + (-176, -48)])   # south face + slit
    R.wall(blk[1], blk[2], PIT, H, W)
    R.wall(blk[2], blk[3], PIT, H, W)
    R.wall(blk[3], blk[0], PIT, H, W)
    for i in range(4):                                      # steel band under the ceiling
        pa, pb = np.array(blk[i], dtype=float), np.array(blk[(i + 1) % 4], dtype=float)
        R.decal(pa, pb, H - 44, H - 12, RIVET, (0, 0, 2.25, 1), off=2)
        R.decal(pa, pb, PIT, PIT + 26, DARK, (0, 0.62, 3, 0.70), off=2)
    # lamps and vents on every face
    faces = (('S', 0, -B), ('N', 0, B), ('E', B, 0), ('W', -B, 0))
    for f, fx, fz in faces:
        for off in (-176, 0, 176):
            cx, cz = (fx + off, fz) if f in 'NS' else (fx, fz + off)
            wall_light(R, cx, cz, 300, f, power=64, rng=540, w=30, h=30, d=8)
            if f == 'S' and off == 0:
                continue
            if f in 'NS':
                sgn = 1 if f == 'S' else -1
                R.decal((cx - sgn * 36, cz), (cx + sgn * 36, cz), -214, -142, VENT, (0, 0, 1, 1), off=2)
            else:
                sgn = 1 if f == 'E' else -1
                R.decal((cx, cz - sgn * 36), (cx, cz + sgn * 36), -214, -142, VENT, (0, 0, 1, 1), off=2)

    # ---- inside the block: the floodlit cell and the hanging acrylic cage
    G = WHITEGLOW
    C = 224.0
    R.rect_floor(-96, -B, 96, -C, -176, DARK)               # the slit through the wall
    R.rect_ceil(-96, -B, 96, -C, -48, DARK)
    R.wall((-96, -B), (-96, -C), -176, -48, DARK)
    R.wall((96, -C), (96, -B), -176, -48, DARK)
    R.quad(V(-96, -176, -256), V(96, -176, -256), V(96, -48, -256), V(-96, -48, -256), GLASS,
           uvrect=(0, 0, 0.75, 0.5), lm=False)
    cell = [(-C, -C), (-C, C), (C, C), (C, -C)]
    R.walls(cell, PIT, 192, G, holes={3: [span(cell[3], (96, -C), (-96, -C)) + (-176, -48)]})
    R.rect_floor(-C, -C, C, C, PIT + 4, G)
    R.rect_ceil(-C, -C, C, C, 192, G)
    for (p, q) in (((-64, -64), (64, -64)), ((64, -64), (64, 64)), ((64, 64), (-64, 64)), ((-64, 64), (-64, -64))):
        R.quad(V(p[0], -176, p[1]), V(q[0], -176, q[1]), V(q[0], -48, q[1]), V(p[0], -48, p[1]), GLASS,
               uvrect=(0, 0, 0.5, 0.5), lm=False, coll=False)
    R.box(-66, -182, -66, 66, -176, 66, DIRTY, lux=10)       # cage floor plate
    R.box(-66, -48, -66, 66, -42, 66, DIRTY, lux=10)         # cage roof plate
    R.box(-3, -42, -3, 3, 192, 3, DARK, skip='TB', lux=10)   # the cable it hangs from
    A['shadow'] = (0, -120, 0)
    R.light(0, -90, -330, rng=520, color=(255, 255, 255), power=70, ent=False)      # glow spilling from the slit

    # ---- the lamp circuit lever and a work desk on the pit's north wall
    A['lever'] = (0, PIT + 190, 631)
    sign2(R, 'lampreset', -140, 640, 'S', 150, 56, PIT + 200)
    top = desk(R, 150, 560, 330, 630, PIT)
    A['desk_a'] = (200, top + 4, 595)
    A['desk_b'] = (280, top + 4, 595)
    tt = shelf_unit(R, -420, 584, -180, 634, PIT, height=230, levels=4)
    A['shelf_a'] = (-360, tt[1] + 4, 609)
    A['shelf_b'] = (-240, tt[2] + 4, 609)
    crate(R, -560, PIT, 540, yaw=18)
    crate(R, 560, PIT, 520, yaw=-10, kind=2)
    A['landing_doc'] = (260, 0, -800)

    # ---- walkway wall lamps (reference shot 11) and entry lights
    for z in (-480, -160, 160, 480):
        wall_light(R, -896, z, 250, 'E', power=54, rng=450)
        wall_light(R, 896, z, 250, 'W', power=54, rng=450)
    ceil_light(R, 0, -820, H, size=64, power=84, rng=640, color=(255, 240, 220))
    ceil_light(R, 0, 820, H, size=64, power=84, rng=640, color=(255, 240, 220))

    # ---- signs
    sign2(R, 'blockd', 0, -992, 'N', 330, 82, 392)
    sign2(R, 'blockd', 0, 992, 'S', 330, 82, 392)
    sign2(R, 'l_017', 300, -992, 'N', 96, 120, 220)
    sign2(R, 'd_shadow', -200, -B, 'S', 84, 84, -110)
    sign2(R, 'c_lamps', 200, -B, 'S', 84, 84, -110)
    sign2(R, 'c_lamps', -300, 640, 'S', 84, 84, PIT + 300 - 60)

    for (x, z) in ((0, -816), (-784, -816), (-784, 816), (0, 816)):
        R.waypoint(x, 66, z)
    return R, A


if __name__ == '__main__':
    import time
    t = time.time()
    R, A = build()
    R.bake()
    print('bake %.1fs' % (time.time() - t))
    R.export('out')
    R.topview('out/blockhall_top.png')
    R.render((0, 165, -940), (0, 60, 0), 'out/blockhall_1.png')
    R.render((0, PIT + 165, -600), (0, 0, 0), 'out/blockhall_2.png')
    R.render((-784, 165, -500), (300, -100, 300), 'out/blockhall_3.png')
    R.render((0, PIT + 165, -480), (0, PIT + 140, -200), 'out/blockhall_4.png', fov=60)
    for k, v in A.items():
        print('  ', k, v)
