"""room1whitedoor - containment chamber for SCP-055 (HCZ, dead end: door on -z).
Reference shot 14: a wide, low, almost unlit room with a rough dark floor and nothing in it
but a doorway of flat white light in the middle of the far wall."""
from parts import *

DARKWALL = Mat('concretewall.jpg', 384, 384, 384)
ROUGH = Mat('concretefloor.jpg', 256)


def build():
    R = Room('room1whitedoor', luxel=12, ambient=7, fill=0.10)
    A = {}
    NH, CH = 384.0, 448.0

    # ---- the airlock between the map door and the chamber
    lock = [(-192, -992), (-192, -800), (192, -800), (192, -992)]
    R.walls(lock, 0, NH, DARKWALL, holes={
        1: [span(lock[1], (-96, -800), (96, -800)) + (0, 320)],
        3: [span(lock[3], (96, -992), (-96, -992)) + (0, 320)]})
    R.rect_floor(-192, -992, 192, -800, 0, ROUGH)
    R.rect_ceil(-192, -992, 192, -800, NH, DIRTY)
    door_neck(R, 'S', DARKWALL, ROUGH)
    R.door_marker(0, 0, -1024, 0, color=(52, 52, 56))
    # jamb through the chamber wall (z -800 .. -768)
    R.rect_floor(-96, -800, 96, -736, 0, ROUGH)
    R.rect_ceil(-96, -800, 96, -736, 320, DARKWALL)
    R.wall((-96, -800), (-96, -736), 0, 320, DARKWALL)
    R.wall((96, -736), (96, -800), 0, 320, DARKWALL)
    R.door_marker(0, 0, -768, 0)
    A['inner_door'] = (0, 0, -768)
    ceil_light(R, 0, -896, NH, size=48, power=78, rng=520, color=(255, 240, 220))

    # ---- the chamber
    ch = [(-896, -736), (-896, 896), (896, 896), (896, -736)]
    R.walls(ch, 0, CH, DARKWALL.but(v0=CH, vs=448), holes={
        1: [span(ch[1], (-80, 896), (80, 896)) + (0, 288)],
        3: [span(ch[3], (96, -736), (-96, -736)) + (0, 320)]})
    R.rect_floor(-896, -736, 896, 896, 0, ROUGH)
    R.rect_ceil(-896, -736, 896, 896, CH, DIRTY)
    # skirting line round the room, like the reference
    for i in range(4):
        a, b = np.array(ch[i], dtype=float), np.array(ch[(i + 1) % 4], dtype=float)
        if i == 1:
            R.decal(a, (-80, 896), 0, 26, DARK, (0, 0.62, 6, 0.70), off=2)
            R.decal((80, 896), b, 0, 26, DARK, (0, 0.62, 6, 0.70), off=2)
        elif i == 3:
            R.decal(a, (96, -736), 0, 26, DARK, (0, 0.62, 6, 0.70), off=2)
            R.decal((-96, -736), b, 0, 26, DARK, (0, 0.62, 6, 0.70), off=2)
        else:
            R.decal(a, b, 0, 26, DARK, (0, 0.62, 12, 0.70), off=2)

    # ---- the white door: a recess where every surface is flat white light
    G = WHITEGLOW
    R.rect_floor(-80, 896, 80, 1008, 0, G)
    R.rect_ceil(-80, 896, 80, 1008, 288, G)
    R.wall((-80, 896), (-80, 1008), 0, 288, G)
    R.wall((-80, 1008), (80, 1008), 0, 288, G)
    R.wall((80, 1008), (80, 896), 0, 288, G)
    A['white'] = (0, 0, 960)
    A['white_mouth'] = (0, 0, 896)
    # the glow it throws into the room (the only real light in here)
    R.light(0, 150, 850, rng=1500, color=(255, 255, 255), power=150, radius=40, fill=0.10)
    R.light(0, 150, 700, rng=900, color=(255, 255, 255), power=40, radius=30, ent=False, fill=0.05)

    # ---- signs in the airlock
    sign_at(R, 'l_055', -192, -896, 'E', 150, 75, 230)
    sign_at(R, 'n_055', 192, -896, 'W', 170, 64, 220)

    A['note_floor'] = (140, 10, -620)
    A['player_out'] = (0, 0, -600)
    R.waypoint(0, 66, -880)
    R.waypoint(0, 66, -500)
    R.waypoint(0, 66, 300)
    return R, A


if __name__ == '__main__':
    import time
    t = time.time()
    R, A = build()
    R.bake()
    print('bake %.1fs' % (time.time() - t))
    R.export('out')
    R.topview('out/whitedoor_top.png')
    R.render((0, 165, -700), (0, 140, 900), 'out/whitedoor_1.png', fov=72)
    R.render((0, 165, -980), (0, 150, 0), 'out/whitedoor_2.png')
    R.render((300, 165, 500), (-100, 120, 950), 'out/whitedoor_3.png')
    for k, v in A.items():
        print('  ', k, v)
