"""room2catwalk - "Service Atrium 2-C" (LCZ, two doors).
Reference shots 1-3: a tall hall with chamfered corners, a railed bridge crossing overhead,
a door set back in a low portal at each end and a vent high on the wall."""
from parts import *


def build():
    R = Room('room2catwalk', luxel=10, ambient=15, fill=0.15)
    H, UP = 704.0, 352.0
    A = {}

    # ---- the hall: octagon, chamfered corners
    out = [(-256, -768), (-416, -608), (-416, 608), (-256, 768), (256, 768), (416, 608), (416, -608), (256, -768)]
    holes = {}
    # west wall (seg 1): the fan duct, the loft doorway upstairs
    a = out[1]
    holes[1] = [span(a, (-416, -560), (-416, -400)) + (448, 608), span(a, (-416, -96), (-416, 96)) + (UP, UP + 320)]
    # north wall (seg 3) / south wall (seg 7): the low portals
    holes[3] = [span(out[3], (-192, 768), (192, 768)) + (0, 384)]
    holes[7] = [span(out[7], (-192, -768), (192, -768)) + (0, 384)]
    # east wall (seg 5): upper elevator door, lower elevator door
    a = out[5]
    holes[5] = [span(a, (416, 352), (416, 544)) + (UP, UP + 320), span(a, (416, -544), (416, -352)) + (0, 320)]
    R.walls(out, 0, H, LCZWALL, holes=holes)
    R.floor(out, 0, LCZFLOOR)
    R.ceil(out, H, LCZCEIL)

    # ---- the two portals (necks) to the map doors
    for sgn, side in ((1, 'N'), (-1, 'S')):
        z0, z1 = sorted((sgn * 768.0, sgn * 992.0))
        R.rect_floor(-192, z0, 192, z1, 0, LCZFLOOR)
        R.rect_ceil(-192, z0, 192, z1, 384, LCZCEIL)
        if sgn > 0:
            R.wall((-192, 768), (-192, 992), 0, 384, LCZWALL)
            R.wall((192, 992), (192, 768), 0, 384, LCZWALL)
        else:
            R.wall((192, -768), (192, -992), 0, 384, LCZWALL)
            R.wall((-192, -992), (-192, -768), 0, 384, LCZWALL)
        end_wall(R, side, -192, 192, 384, LCZWALL, LCZFLOOR)

    # ---- the bridge and the east gallery (walk surface y = 352, on the rivet band of the wall)
    R.box(-336, UP - 16, -112, 416, UP, 112, DARK, skip='EW', top=DIRTY)
    R.box(-416, UP - 16, -208, -336, UP, 208, DARK, skip='W', top=DIRTY)       # landing at the loft door
    R.box(256, UP - 16, 112, 416, UP, 608, DARK, skip='ES', top=DIRTY)
    railing(R, (-336, -112), (416, -112), UP)
    railing(R, (-336, 112), (256, 112), UP)
    railing(R, (-336, -208), (-336, -112), UP)
    railing(R, (-416, -208), (-336, -208), UP)
    railing(R, (-336, 112), (-336, 208), UP)
    railing(R, (-416, 208), (-336, 208), UP)
    railing(R, (256, 112), (256, 608), UP)
    railing(R, (256, 608), (416, 608), UP)
    # brackets under the bridge where it meets the walls
    for sx in (-1, 1):
        for sz in (-96, 96):
            x0, x1 = sorted((sx * 416, sx * 376))
            R.box(x0, UP - 56, sz - 8, x1, UP - 16, sz + 8, DARK, skip='T', lux=8)

    # ---- west loft ("Upper Store") behind a level 2 door
    LT = UP + 320
    R.rect_floor(-480, -96, -416, 96, UP, DIRTY)
    R.rect_ceil(-480, -96, -416, 96, LT, LCZWALL)
    R.wall((-416, -96), (-480, -96), UP, LT, LCZWALL)
    R.wall((-480, 96), (-416, 96), UP, LT, LCZWALL)
    loft = [(-992, -320), (-992, 320), (-480, 320), (-480, -320)]
    R.walls(loft, UP, LT, LCZWALL.but(v0=LT, vs=320), holes={2: [span(loft[2], (-480, 96), (-480, -96)) + (UP, LT)]})
    R.rect_floor(-992, -320, -480, 320, UP, LCZFLOOR)
    R.rect_ceil(-992, -320, -480, 320, LT, LCZCEIL)
    ceil_light(R, -736, 0, LT, power=112, rng=700)
    R.door_marker(-448, UP, 0, 90)
    A['loft_door'] = (-448, UP, 0)
    # shelving along the west and north walls of the loft, a crate table in the middle
    t1 = shelf_unit(R, -984, -280, -920, -40, UP, height=240, levels=4)
    t2 = shelf_unit(R, -984, 40, -920, 280, UP, height=240, levels=4)
    t3 = shelf_unit(R, -860, 256, -580, 312, UP, height=240, levels=4)
    R.box(-760, UP, -120, -640, UP + 72, -8, WOOD, skip='B')
    A['loft_shelf_a'] = (-952, t1[1] + 4, -160)
    A['loft_shelf_b'] = (-952, t2[2] + 4, 160)
    A['loft_shelf_c'] = (-710, t3[1] + 4, 284)
    A['loft_crate'] = (-700, UP + 76, -64)
    file_row(R, (-270, -50, -952), (0, 0, 0), t1[2], 'z', seed=3)
    file_row(R, (-270, -50, -952), (0, 0, 0), t1[0], 'z', seed=4, fill=0.5)
    file_row(R, (50, 270, -952), (0, 0, 0), t2[1], 'z', seed=5)
    file_row(R, (50, 270, -952), (0, 0, 0), t2[3], 'z', seed=6, fill=0.6)
    file_row(R, (-850, -590, 284), (0, 0, 0), t3[2], 'x', seed=7)
    crate(R, -600, UP, -230, yaw=20)
    crate(R, -560, UP, 150, yaw=-12, kind=2)
    A['ground_doc'] = (300, 10, -250)
    A['bridge_mid'] = (0, UP, 0)

    # ---- elevator: ground stop on the east wall, upper stop on the gallery (offset along z so the
    #      two cabins never share a column - UpdateElevators tests a 280 unit box round each pivot)
    A['elev_lo_door'], A['elev_lo_pivot'] = elevator(R, 416, -448, 0, +1, LCZWALL)
    A['elev_hi_door'], A['elev_hi_pivot'] = elevator(R, 416, 448, UP, +1, LCZWALL, height=336)

    # ---- the fan duct, high on the west wall
    R.rect_floor(-512, -560, -416, -400, 448, DARK)
    R.rect_ceil(-512, -560, -416, -400, 608, DARK)
    R.wall((-416, -560), (-512, -560), 448, 608, DARK)
    R.wall((-512, -400), (-416, -400), 448, 608, DARK)
    R.quad(V(-512, 448, -560), V(-512, 448, -400), V(-512, 608, -400), V(-512, 608, -560), VENT, uvrect=(0, 0, 1, 1))
    for (y0, y1, z0, z1) in ((440, 448, -568, -392), (608, 616, -568, -392), (448, 608, -568, -560), (448, 608, -400, -392)):
        R.box(-416, y0, z0, -410, y1, z1, DIRTY, skip='W', lux=8)
    A['fan'] = (-456, 528, -480)
    R.sound(-456, 528, -480, 9, 4.5)

    # ---- lights
    ceil_light(R, 0, -420, H, size=112, power=142, rng=1150)
    ceil_light(R, 0, 420, H, size=112, power=142, rng=1150)
    ceil_light(R, 0, -880, 384, size=64, power=70, rng=520)
    ceil_light(R, 0, 880, 384, size=64, power=70, rng=520)

    # ---- signs
    sign_at(R, 'atrium', 0, 768, 'S', 360, 90, 470)
    sign_at(R, 'atrium', 0, -768, 'N', 360, 90, 470)
    sign_at(R, 'elevator', 416, -170, 'W', 200, 66, 250)
    sign_at(R, 'l1', 416, -320, 'W', 56, 42, 262)
    sign_at(R, 'l2', 416, 300, 'W', 64, 48, UP + 180)
    sign_at(R, 'c_level2', -416, 165, 'E', 84, 84, UP + 276)
    sign_at(R, 'upper', -416, -175, 'E', 150, 60, UP + 276)

    for z in (-600, 0, 600):
        R.waypoint(0, 66, z)
    return R, A


if __name__ == '__main__':
    import time
    t = time.time()
    R, A = build()
    R.bake()
    print('bake %.1fs' % (time.time() - t))
    R.export('out')
    R.topview('out/catwalk_top.png', y_cut=(-10, 340))
    R.topview('out/catwalk_top2.png', y_cut=(345, 800))
    R.render((0, 165, -940), (0, 260, 0), 'out/catwalk_1.png')
    R.render((-300, 165, 560), (250, 330, -200), 'out/catwalk_2.png')
    R.render((330, 352 + 165, 560), (-300, 352 + 60, -100), 'out/catwalk_3.png')
    R.render((-700, 352 + 165, -250), (-950, 352 + 100, 200), 'out/catwalk_4.png')
    for k, v in A.items():
        print('  ', k, v)
