"""room2cmaint - "Maintenance Corner" (LCZ, corner room: doors on -z and +x).
Reference shots 4, 8, 11: a narrow white corridor with a rivet band under a dark ceiling, red
pendant lamps, tiled floor, two grey SCP doors and the yellow CAUTION / ADMITTANCE sign."""
from parts import *

CTRL = Mat('controlpanel.jpg', 256, cast=False)


def build():
    R = Room('room2cmaint', luxel=10, ambient=14, fill=0.15)
    A = {}
    H = 352.0
    W = LCZWALL

    out = [(-192, -992), (-192, 192), (992, 192), (992, -192), (192, -192), (192, -992)]
    holes = {
        0: [span(out[0], (-192, -496), (-192, -304)) + (0, 320)],            # janitor closet
        1: [span(out[1], (-96, 192), (96, 192)) + (0, 320)],                 # electrical centre
        2: [span(out[2], (992, 96), (992, -96)) + (0, 320)],                 # map door (east)
        5: [span(out[5], (96, -992), (-96, -992)) + (0, 320)],               # map door (south)
    }
    R.walls(out, 0, H, W, holes=holes)
    door_neck(R, 'E', W, TILE)
    door_neck(R, 'S', W, TILE)
    R.door_marker(1024, 0, 0, 90, color=(52, 52, 56))
    R.door_marker(0, 0, -1024, 0, color=(52, 52, 56))
    R.rect_floor(-192, -992, 192, 192, 0, TILE)
    R.rect_floor(192, -192, 992, 192, 0, TILE)
    R.rect_ceil(-192, -992, 192, 192, H, DIRTY)
    R.rect_ceil(192, -192, 992, 192, H, DIRTY)

    # ---- electrical centre (north of the corner, level 2 card)
    R.rect_floor(-96, 192, 96, 256, 0, TILE)
    R.rect_ceil(-96, 192, 96, 256, 320, W)
    R.wall((-96, 192), (-96, 256), 0, 320, W)
    R.wall((96, 256), (96, 192), 0, 320, W)
    el = [(-416, 256), (-416, 800), (416, 800), (416, 256)]
    R.walls(el, 0, H, HCZWALL.but(v0=H, vs=352), holes={3: [span(el[3], (96, 256), (-96, 256)) + (0, 320)]})
    R.rect_floor(-416, 256, 416, 800, 0, LCZFLOOR)
    R.rect_ceil(-416, 256, 416, 800, H, DIRTY)
    R.door_marker(0, 0, 224, 0)
    A['elec_door'] = (0, 0, 224)
    # switchgear along the north wall, the lever between the cabinets
    for (x0, x1) in ((-400, -200), (200, 400)):
        R.box(x0, 0, 720, x1, 300, 796, DIRTY, skip='BN')
        R.decal((x0 + 8, 720), (x1 - 8, 720), 20, 290, CTRL, (0.0, 0.0, 0.5, 1.0), off=1.5)
    R.decal((-150, 800), (150, 800), 60, 300, CTRL, (0.5, 0.0, 1.0, 1.0))
    A['lever'] = (0, 190, 792)
    sign_at(R, 'remote', 0, 800, 'S', 110, 70, 300 - 2, sheet='misc')
    sign_at(R, 'on', -110, 800, 'S', 60, 26, 235, sheet='misc')
    sign_at(R, 'off', -110, 800, 'S', 60, 26, 150, sheet='misc')
    # supply shelves down the west wall
    t = shelf_unit(R, -408, 300, -340, 660, 0, height=250, levels=4)
    A['elec_shelf_a'] = (-374, t[1] + 4, 380)
    A['elec_shelf_b'] = (-374, t[1] + 4, 520)
    A['elec_shelf_c'] = (-374, t[2] + 4, 600)
    A['elec_shelf_d'] = (-374, t[0] + 4, 450)
    file_row(R, (310, 650, -374), (0, 0, 0), t[3], 'z', seed=11, fill=0.6)
    file_row(R, (560, 650, -374), (0, 0, 0), t[0], 'z', seed=12)
    crate(R, 300, 0, 640, yaw=8)
    top = desk(R, 250, 300, 400, 380, 0)
    A['elec_desk'] = (325, top + 4, 340)
    ceil_light(R, 0, 500, H, size=96, power=125, rng=760, color=(255, 240, 215))

    # ---- janitor closet (west of the south leg)
    R.rect_floor(-256, -496, -192, -304, 0, TILE)
    R.rect_ceil(-256, -496, -192, -304, 320, W)
    R.wall((-192, -496), (-256, -496), 0, 320, W)
    R.wall((-256, -304), (-192, -304), 0, 320, W)
    cl = [(-640, -608), (-640, -192), (-256, -192), (-256, -608)]
    R.walls(cl, 0, H, W, holes={2: [span(cl[2], (-256, -304), (-256, -496)) + (0, 320)]})
    R.rect_floor(-640, -608, -256, -192, 0, LCZFLOOR)
    R.rect_ceil(-640, -608, -256, -192, H, DIRTY)
    R.door_marker(-224, 0, -400, 90)
    A['closet_door'] = (-224, 0, -400)
    t = shelf_unit(R, -632, -600, -568, -220, 0, height=250, levels=4)
    A['closet_shelf_a'] = (-600, t[1] + 4, -520)
    A['closet_shelf_b'] = (-600, t[2] + 4, -300)
    R.box(-470, 0, -600, -350, 80, -500, WOOD, skip='B')
    R.box(-440, 80, -590, -370, 140, -520, WOOD, skip='B')
    A['closet_crate'] = (-405, 144, -555)
    file_row(R, (-590, -230, -600), (0, 0, 0), t[3], 'z', seed=13, fill=0.5)
    crate(R, -330, 0, -270, yaw=-15, kind=2)
    ceil_light(R, -448, -400, H, size=64, power=85, rng=560, color=(255, 235, 205))

    # ---- corridor lights: the red pendants
    pendant(R, 0, -640, H, power=150, rng=900)
    pendant(R, 0, 0, H, power=150, rng=900)
    pendant(R, 620, 0, H, power=150, rng=900)

    # ---- signs
    sign_at(R, 'electrical', 215, 192, 'S', 170, 76, 276, sheet='misc')
    sign_at(R, 'admittance', -150, 192, 'S', 96, 70, 272, sheet='misc')

    R.waypoint(0, 66, -600)
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
    R.topview('out/cmaint_top.png')
    R.render((0, 165, -940), (0, 150, 0), 'out/cmaint_1.png')
    R.render((900, 165, 60), (0, 150, 40), 'out/cmaint_2.png')
    R.render((330, 165, 300), (-200, 140, 760), 'out/cmaint_3.png')
    for k, v in A.items():
        print('  ', k, v)
