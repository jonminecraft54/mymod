"""room2overlook - "Lower Gallery" (EZ, two doors).
Reference shots 7, 9, 13: a long office corridor whose east side opens through a glass balustrade
onto a records pit one storey down, slanted roof beams, red pendant lamps, a body on the lower
floor - and an elevator door set in the corridor wall that takes you down there."""
from parts import *

WHITE = Mat('white.jpg', 256)
LOW = -448.0


def band_wall(R, a, b, y0, y1, floor_y):
    """Office wall panel for the first storey above floor_y, plain plaster above it, a steel band between."""
    top = floor_y + 384.0
    R.wall(a, b, y0, min(y1, top), EZWALL.but(v0=top))
    if y1 > top:
        R.wall(a, b, top, y1, WHITE)
        a2 = np.asarray(a, dtype=float)
        b2 = np.asarray(b, dtype=float)
        R.decal(a2, b2, top - 12, top + 12, RIVET, (0, 0, np.linalg.norm(b2 - a2) / 256.0, 1), off=2)


def build():
    R = Room('room2overlook', luxel=10, ambient=14, fill=0.15)
    A = {}
    CH, AH = 384.0, 576.0

    # ---- the corridor (grid level)
    R.rect_floor(-192, -992, 192, 992, 0, TILE)
    R.rect_ceil(-192, -992, 192, 992, CH, EZCEIL)
    a = (-192, -992)
    R.wall(a, (-192, 992), 0, CH, EZWALL, holes=[span(a, (-192, -496), (-192, -304)) + (0, 320),
                                                 span(a, (-192, 304), (-192, 496)) + (0, 320)])
    R.wall((192, 992), (192, 640), 0, CH, EZWALL)
    R.wall((192, -640), (192, -992), 0, CH, EZWALL)
    end_wall(R, 'N', -192, 192, CH, EZWALL, TILE)
    end_wall(R, 'S', -192, 192, CH, EZWALL, TILE)
    # the slab the corridor stands on, seen from the pit
    R.wall((192, -640), (192, 640), -32, 0, DARK)
    R.rect_ceil(-192, -640, 192, 640, -32, EZCEIL)
    glass_rail(R, (192, -640), (192, 640), 0)

    # ---- the pit / atrium
    R.rect_floor(-192, -640, 960, 640, LOW, TILE)
    R.rect_ceil(192, -640, 960, 640, AH, EZCEIL)
    R.wall((192, -640), (192, 640), CH, AH, WHITE)                    # above the corridor opening
    R.wall((-192, 640), (192, 640), LOW, -32, EZWALL.but(v0=LOW + 384))
    band_wall(R, (192, 640), (960, 640), LOW, AH, LOW)
    band_wall(R, (960, 640), (960, -640), LOW, AH, LOW)
    band_wall(R, (960, -640), (192, -640), LOW, AH, LOW)
    R.wall((192, -640), (-192, -640), LOW, -32, EZWALL.but(v0=LOW + 384))
    a = (-192, -640)
    R.wall(a, (-192, 640), LOW, -32, EZWALL.but(v0=LOW + 384),
           holes=[span(a, (-192, -496), (-192, -304)) + (LOW, LOW + 320)])
    # slanted roof beams
    for z in (-400, 0, 400):
        ax = np.array([384.0, 80.0, 0.0])
        ay = norm(np.array([-80.0, 384.0, 0.0])) * 22
        R.obox((576, 478, z), ax, ay, (0, 0, 22), DARK, skip='EW', lux=12)
    # red pendants over the pit
    for z in (-320, 320):
        pendant(R, 600, z, AH, power=150, rng=1150, color=(255, 236, 220))

    # ---- elevators (the two stops sit in different columns, see room_catwalk.py)
    A['elev_hi_door'], A['elev_hi_pivot'] = elevator(R, -192, 400, 0, -1, EZWALL)
    A['elev_lo_door'], A['elev_lo_pivot'] = elevator(R, -192, -400, LOW, -1, EZWALL)

    # ---- the office off the corridor (Dr. Imre, Records)
    R.rect_floor(-256, -496, -192, -304, 0, TILE)
    R.rect_ceil(-256, -496, -192, -304, 320, EZWALL)
    R.wall((-192, -496), (-256, -496), 0, 320, EZWALL)
    R.wall((-256, -304), (-192, -304), 0, 320, EZWALL)
    off = [(-736, -656), (-736, -144), (-256, -144), (-256, -656)]
    OH = 352.0
    R.walls(off, 0, OH, EZWALL.but(v0=OH, vs=352), holes={2: [span(off[2], (-256, -304), (-256, -496)) + (0, 320)]})
    R.rect_floor(-736, -656, -256, -144, 0, Mat('wood.jpg', 512))
    R.rect_ceil(-736, -656, -256, -144, OH, EZCEIL)
    ceil_light(R, -480, -400, OH, power=115, rng=640, color=(255, 240, 220))
    R.door_marker(-224, 0, -400, 90)
    A['office_door'] = (-224, 0, -400)
    top = desk(R, -700, -480, -600, -300, 0)
    A['office_desk'] = (-650, top + 4, -390)
    A['office_desk2'] = (-650, top + 4, -440)
    cabinet_row(R, (-728, -630), (-500, -630), 0, 'N')
    tt = shelf_unit(R, -500, -200, -290, -152, 0, height=240, levels=4)
    A['office_shelf'] = (-395, tt[2] + 4, -176)
    R.model('officeseat_a.x', -560, 0, -390, rot=(0, 90, 0), scale=(3.5, 3.5, 3.5), size=(84, 160, 84))
    workstation(R, -675, top, -330, yaw=90)
    file_row(R, (-490, -300, -176), (0, 0, 0), tt[1], 'x', seed=51)
    file_row(R, (-490, -300, -176), (0, 0, 0), tt[3], 'x', seed=52, fill=0.6)
    sign_at(R, 'nameplate', -192, -250, 'E', 96, 36, 256)

    # ---- lower floor: cubicle partitions, a counter, a desk
    PH = 176.0
    for (x0, z0, x1, z1) in ((320, -420, 336, -110), (336, -126, 660, -110), (560, 110, 576, 470), (576, 110, 820, 126),
                             (320, 300, 336, 560)):
        R.box(x0, LOW, z0, x1, LOW + PH, z1, WHITE, skip='B', top=DIRTY)
    R.box(720, LOW, -560, 900, LOW + 104, -460, WHITE, skip='B', top=WOOD)
    top = desk(R, 380, -380, 520, -300, LOW)
    A['pit_desk'] = (450, top + 4, -340)
    A['pit_desk2'] = (410, top + 4, -340)
    A['pit_counter'] = (810, LOW + 108, -510)
    A['body'] = (470, LOW, 250)
    A['pit_floor_item'] = (420, LOW + 10, 190)
    cabinet_row(R, (700, 608), (930, 608), LOW, 'S')
    A['pit_spawn'] = (700, LOW, 0)
    workstation(R, 490, top, -350, yaw=0)
    crate(R, 860, LOW, 300, yaw=25)
    crate(R, 840, LOW, 420, yaw=-10, kind=2)

    # ---- lights
    for z in (-800, 0, 800):
        ceil_light(R, 0, z, CH, size=96, power=118, rng=760)
    ceil_light(R, 0, -330, -32, size=64, power=62, rng=520, color=(255, 235, 210))
    ceil_light(R, 0, 330, -32, size=64, power=62, rng=520, color=(255, 235, 210))

    # ---- signs
    sign_at(R, 'elevator', -192, 180, 'E', 150, 50, 250)
    sign_at(R, 'g', -192, 270, 'E', 48, 36, 180)
    sign_at(R, 'gallery', -192, -180, 'E', 220, 56, LOW + 250)
    sign_at(R, 'b1', -192, -40, 'E', 48, 36, LOW + 250)
    sign_at(R, 'pit', 192, 760, 'W', 120, 46, 220)

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
    R.topview('out/overlook_top.png', y_cut=(-10, 380))
    R.topview('out/overlook_top2.png', y_cut=(-460, -40))
    R.render((0, 165, -940), (20, 150, 0), 'out/overlook_1.png')
    R.render((120, 165, -300), (700, -448, 200), 'out/overlook_2.png')
    R.render((880, LOW + 165, -560), (100, LOW + 200, 300), 'out/overlook_3.png')
    R.render((-60, LOW + 165, 500), (500, LOW + 100, -200), 'out/overlook_4.png')
    for k, v in A.items():
        print('  ', k, v)
