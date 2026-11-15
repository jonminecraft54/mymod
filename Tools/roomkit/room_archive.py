"""room2archive - "Records Annex 3-C" (EZ, two doors).
Reference shots 10, 12: an office corridor that opens onto a records hall - rows of filing
cabinets, open shelving, a block of shelves in the middle of the floor, wall lamps and a
reddish cast to the light."""
from parts import *


def build():
    R = Room('room2archive', luxel=10, ambient=14, fill=0.15)
    A = {}
    H = 384.0
    W = EZWALL

    out = [(-192, -992), (-192, 992), (192, 992), (192, 704), (960, 704), (960, -704), (192, -704), (192, -992)]
    holes = {
        1: [span(out[1], (-96, 992), (96, 992)) + (0, 320)],
        7: [span(out[7], (96, -992), (-96, -992)) + (0, 320)],
    }
    R.walls(out, 0, H, W, holes=holes)
    door_neck(R, 'N', W, TILE)
    door_neck(R, 'S', W, TILE)
    R.door_marker(0, 0, 1024, 0, color=(52, 52, 56))
    R.door_marker(0, 0, -1024, 0, color=(52, 52, 56))
    R.rect_floor(-192, -992, 192, 992, 0, TILE)
    R.rect_floor(192, -704, 960, 704, 0, TILE)
    R.rect_ceil(-192, -992, 192, 992, H, EZCEIL)
    R.rect_ceil(192, -704, 960, 704, H, EZCEIL)
    # a dropped beam where the corridor meets the hall
    R.box(184, 336, -704, 200, H, 704, DARK, skip='T', lux=12)

    # ---- the shelf block between corridor and hall (reference shot 10)
    tb = shelf_unit(R, 216, -300, 300, 300, 0, height=272, levels=4, mat=WOOD)
    R.box(254, 0, -300, 262, 272, 300, DIRTY, skip='B', lux=12)
    A['block_shelf_a'] = (236, tb[1] + 4, -180)
    A['block_shelf_b'] = (236, tb[2] + 4, 90)
    A['block_shelf_c'] = (282, tb[1] + 4, 200)
    for lvl, sd in ((0, 21), (1, 22), (2, 23), (3, 24)):
        file_row(R, (-290, 290, 236), (0, 0, 0), tb[lvl], 'z', seed=sd, fill=0.4, keep_clear=[(-225, -135), (45, 135)])
        file_row(R, (-290, 290, 282), (0, 0, 0), tb[lvl], 'z', seed=sd + 10, fill=0.4, keep_clear=[(155, 245)])

    # ---- filing cabinets: a run down the east wall and two back-to-back islands
    cabinet_row(R, (926, -680), (926, 680), 0, 'W')
    for (z0, z1) in ((-520, -100), (100, 520)):
        cabinet_row(R, (548, z0), (548, z1), 0, 'W')
        cabinet_row(R, (612, z0), (612, z1), 0, 'E')
    R.box(520, 176, -500, 600, 232, -410, DARK, skip='B')         # the black storage box on the cabinets
    A['cab_top_a'] = (580, 180, 300)
    A['cab_top_b'] = (580, 180, -200)
    A['cab_east'] = (926, 180, 420)
    A['drawer'] = (894, 60, -360)          # the stuck drawer (front of an east-wall cabinet)

    # ---- shelving on the north and south walls
    tn = shelf_unit(R, 320, 640, 820, 696, 0, height=272, levels=4, mat=WOOD)
    ts = shelf_unit(R, 620, -696, 900, -640, 0, height=272, levels=4, mat=WOOD)
    A['north_shelf_a'] = (420, tn[1] + 4, 668)
    A['north_shelf_b'] = (700, tn[2] + 4, 668)
    A['south_shelf_a'] = (760, ts[1] + 4, -668)
    for lvl, sd in ((0, 41), (1, 42), (2, 43), (3, 44)):
        file_row(R, (330, 810, 668), (0, 0, 0), tn[lvl], 'x', seed=sd, fill=0.45, keep_clear=[(375, 465), (655, 745)])
        file_row(R, (630, 890, -668), (0, 0, 0), ts[lvl], 'x', seed=sd + 10, fill=0.4, keep_clear=[(715, 805)])

    # ---- the archivist's desk in the south-west corner of the hall
    top = desk(R, 300, -670, 520, -580, 0)
    A['desk_a'] = (360, top + 4, -625)
    A['desk_b'] = (460, top + 4, -625)
    R.model('officeseat_a.x', 410, 0, -520, rot=(0, 180, 0), scale=(3.5, 3.5, 3.5), size=(84, 160, 84))
    workstation(R, 410, top, -650, yaw=180)
    A['npc'] = (760, 0, 0)
    A['npc_hide'] = (760, 0, 600)

    # ---- ceiling fan over the islands
    R.box(574, 344, -2, 578, H, 2, DIRTY, skip='TB', lux=8)
    A['ceilfan'] = (576, 340, 0)

    # ---- lights: white in the corridor, red-tinted in the stacks, sconces on the west wall
    for z in (-760, 0, 760):
        ceil_light(R, 0, z, H, size=96, power=112, rng=740)
    for z in (-380, 380):
        ceil_light(R, 760, z, H, size=64, power=140, rng=900, color=(255, 150, 140))
    ceil_light(R, 400, 0, H, size=64, power=95, rng=700, color=(255, 190, 175))
    wall_light(R, -192, -380, 230, 'E')
    wall_light(R, -192, 380, 230, 'E')

    # ---- signs
    sign_at(R, 'records', -192, 0, 'E', 300, 75, 250)
    sign_at(R, 'n_quiet', 192, -850, 'W', 96, 96, 210)

    for z in (-700, 0, 700):
        R.waypoint(0, 66, z)
    R.waypoint(420, 66, 0)
    return R, A


if __name__ == '__main__':
    import time
    t = time.time()
    R, A = build()
    R.bake()
    print('bake %.1fs' % (time.time() - t))
    R.export('out')
    R.topview('out/archive_top.png')
    R.render((0, 165, -940), (60, 150, 0), 'out/archive_1.png')
    R.render((420, 165, -560), (760, 120, 300), 'out/archive_2.png')
    R.render((770, 165, 640), (760, 110, -300), 'out/archive_3.png')
    for k, v in A.items():
        print('  ', k, v)
