"""room2cobserve - "Observation 4-C" / SCP-999 (Indev zone, corner room: doors on -z and +x).
Reference shots (second set) 9, 4, 18: an eight-sided concrete tunnel with lamps set in its roof,
turning into a square corridor with a checker-plate strip down the floor, a yellow SCP label by
an observation window, and behind the window a bare holding room."""
from parts import *

WHITE = Mat('white.jpg', 256)


def build():
    R = Room('room2cobserve', luxel=10, ambient=10, fill=0.14)
    A = {}
    H = 384.0
    W = HCZWALL
    FL = LCZFLOOR

    # ---- leg A: the eight-sided tunnel (z -992 .. -256)
    z0, z1 = -992.0, -256.0
    R.rect_floor(-128, z0, 128, z1, 0, FL)
    R.rect_ceil(-96, z0, 96, z1, H, DIRTY)
    R.wall((-192, z0), (-192, z1), 64, 288, W)
    R.wall((192, z1), (192, z0), 64, 288, W)
    for sx in (-1, 1):
        poly_facing(R, [V(sx * 128, 0, z0), V(sx * 128, 0, z1), V(sx * 192, 64, z1), V(sx * 192, 64, z0)], (-sx, 1, 0), W)
        poly_facing(R, [V(sx * 192, 288, z0), V(sx * 192, 288, z1), V(sx * 96, H, z1), V(sx * 96, H, z0)], (-sx, -1, 0), W)
    # south end: the wall round the map door, cut to the tunnel's outline
    for sx in (-1, 1):
        poly_facing(R, [V(sx * 128, 0, z0), V(sx * 96, 0, z0), V(sx * 96, H, z0), V(sx * 192, 288, z0), V(sx * 192, 64, z0)],
                    (0, 0, 1), W)
    poly_facing(R, [V(-96, 320, z0), V(96, 320, z0), V(96, H, z0), V(-96, H, z0)], (0, 0, 1), W)
    door_neck(R, 'S', W, FL)
    R.door_marker(0, 0, -1024, 0, color=(52, 52, 56))
    # north end of the tunnel: the four corners left over where it meets the square corner hall
    for sx in (-1, 1):
        poly_facing(R, [V(sx * 192, 0, z1), V(sx * 128, 0, z1), V(sx * 192, 64, z1)], (0, 0, 1), W)
        poly_facing(R, [V(sx * 192, 288, z1), V(sx * 96, H, z1), V(sx * 192, H, z1)], (0, 0, 1), W)
    for z in (-880, -624, -368):
        ceil_light(R, 0, z, H, size=56, power=92, rng=620, color=(240, 244, 255))

    # ---- the corner and leg B
    out = [(-192, -256), (-192, 192), (992, 192), (992, -192), (192, -192), (192, -256)]
    holes = {
        1: [span(out[1], (256, 192), (448, 192)) + (0, 320),                  # door to the holding room
            span(out[1], (544, 192), (864, 192)) + (96, 256)],                 # observation window
        2: [span(out[2], (992, 96), (992, -96)) + (0, 320)],
    }
    R.walls(out, 0, H, W, holes=holes, closed=False)
    door_neck(R, 'E', W, FL)
    R.door_marker(1024, 0, 0, 90, color=(52, 52, 56))
    R.rect_floor(-192, -256, 192, 192, 0, FL)
    R.rect_floor(192, -192, 992, 192, 0, FL)
    R.rect_ceil(-192, -256, 192, 192, H, DIRTY)
    R.rect_ceil(192, -192, 992, 192, H, DIRTY)
    R.add([V(224, 1.5, -56), V(960, 1.5, -56), V(960, 1.5, 56), V(224, 1.5, 56)],
          [(0, 0), (5.75, 0), (5.75, 0.875), (0, 0.875)], CHECKER, cast=False)
    pendant(R, 0, -30, H, power=120, rng=820)
    ceil_light(R, 620, 0, H, size=56, power=96, rng=700, color=(240, 244, 255))

    # ---- through the 64-thick wall: door jamb and window reveal
    R.rect_floor(256, 192, 448, 256, 0, FL)
    R.rect_ceil(256, 192, 448, 256, 320, W)
    R.wall((256, 192), (256, 256), 0, 320, W)
    R.wall((448, 256), (448, 192), 0, 320, W)
    R.door_marker(352, 0, 224, 0)
    A['pen_door'] = (352, 0, 224)
    R.rect_floor(544, 192, 864, 256, 96, DARK)
    R.rect_ceil(544, 192, 864, 256, 256, DARK)
    R.wall((544, 192), (544, 256), 96, 256, DARK)
    R.wall((864, 256), (864, 192), 96, 256, DARK)
    R.quad(V(544, 96, 224), V(864, 96, 224), V(864, 256, 224), V(544, 256, 224), GLASS, uvrect=(0, 0, 1.25, 0.625), lm=False)

    # ---- SCP-999's holding room
    PH = 320.0
    PW = LCZWALL.but(v0=PH, vs=320)
    pen = [(224, 256), (224, 832), (928, 832), (928, 256)]
    R.walls(pen, 0, PH, PW, holes={3: [span(pen[3], (864, 256), (544, 256)) + (96, 256),
                                       span(pen[3], (448, 256), (256, 256)) + (0, 320)]})
    R.rect_floor(224, 256, 928, 832, 0, TILE)
    R.rect_ceil(224, 256, 928, 832, PH, WHITE)
    ceil_light(R, 420, 560, PH, size=80, power=128, rng=820, color=(255, 236, 206))
    ceil_light(R, 760, 560, PH, size=80, power=128, rng=820, color=(255, 236, 206))
    # a low bed, a feeding bowl stand, a few blocks to push around
    R.box(700, 0, 700, 900, 28, 812, WOOD, skip='B', lux=10)
    R.box(712, 28, 712, 888, 40, 800, Mat('cloth.jpg', 128), skip='B', lux=10)
    R.box(250, 0, 740, 330, 60, 810, DIRTY, skip='B', lux=10)
    for (x, z, s, m) in ((480, 760, 22, Mat('red.jpg', 64)), (540, 790, 16, Mat('yellowmetal.jpg', 64)),
                         (430, 800, 14, Mat('red.jpg', 64))):
        R.box(x - s, 0, z - s, x + s, 2 * s, z + s, m, skip='B', lux=8)
    A['blob'] = (576, 0, 540)
    A['bowl'] = (290, 64, 775)
    A['pen_item'] = (800, 44, 756)

    # ---- signs
    sign2(R, 'l_999', 928, 192, 'S', 84, 105, 190)
    sign2(R, 'observe', 600, -192, 'N', 300, 76, 250)
    sign2(R, 'n_999', 224, 520, 'E', 84, 84, 200)

    R.waypoint(0, 66, -700)
    R.waypoint(0, 66, 0)
    R.waypoint(600, 66, 0)
    return R, A


if __name__ == '__main__':
    import time
    t = time.time()
    R, A = build()
    R.bake()
    print('bake %.1fs' % (time.time() - t))
    R.export('out')
    R.topview('out/cobserve_top.png')
    R.render((0, 165, -960), (0, 160, 0), 'out/cobserve_1.png')
    R.render((-100, 165, 60), (900, 150, 60), 'out/cobserve_2.png')
    R.render((300, 165, 320), (760, 60, 700), 'out/cobserve_3.png')
    for k, v in A.items():
        print('  ', k, v)
