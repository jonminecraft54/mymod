"""The forty-ninth batch (code in IndevU49.bb): SCP-087-B.

  room2scp087b  LCZ  the way in: an old brick room with the map's doors at both ends and, in the east wall, a narrow
                     opening onto stairs that go down into the dark. Past the bottom step the code takes over: the
                     hallways and staircases of SCP-087-B are made as you go (IndevU49.bb).
"""
from rooms_b47 import *

BRICK = Mat('indev_087bbrick.png', 160)
SIGN49B = Mat('indev_087bsign.png', cast=False)


def room2scp087b():
    R = R_('room2scp087b', amb=24)
    R.book = Book()
    B = R.book
    R.luxel = 20.0
    H = 384.0
    X0, X1 = -400.0, 420.0
    hall(R, X0, -1024, X1, 1024, 0, H, BRICK.but(vs=H, v0=H), CFLOOR, DARK,
         holes={'N': [(-96, 96, 0, 320)], 'S': [(-96, 96, 0, 320)], 'E': [(-80, 80, 0, 300)]})
    B.areas.append((X0, X1, -1024, 1024, H, 0))
    for (z0, z1) in ((-1024, -990), (990, 1024)):                                  # thick end walls (buttons)
        for (a, b) in ((X0, -112), (112, X1)):
            R.box(a, 0, z0, b, H, z1, BRICK.but(vs=H, v0=H), lux=40)
        R.box(-112, 320, z0, 112, H, z1, BRICK, lux=10)
    # the stairwell: a narrow brick shaft east of the opening, the steps dropping into the dark
    SX0, SX1, SY = X1, 900.0, -280.0
    hall(R, SX0, -80, SX1, 80, SY, H - SY, BRICK.but(vs=H - SY, v0=H), CFLOOR, DARK, holes={'W': [(-80, 80, 0, 300)]})
    B.areas.append((SX0, SX1, -80, 80, H, SY))
    n = 8
    for i in range(n):
        top = -(i + 1) * (-SY / n)
        R.box(SX0 + i * 40, SY, -80, SX0 + (i + 1) * 40, top, 80, CFLOOR, lux=10)
        # the old concrete balustrade down the north side (ref.: the first stairwell screenshot), stepped with the stairs
        R.box(SX0 + i * 40, top, 56, SX0 + (i + 1) * 40, top + 90, 80, Mat('concrete.jpg', 64), lux=10)
        if i % 2 == 0:
            R.box(SX0 + i * 40 + 12, top + 90, 52, SX0 + i * 40 + 28, top + 96, 80, Mat('concrete.jpg', 64), lux=10)
    R.box(SX1 - 8, SY, -80, SX1, H, 80, DARK, lux=10)                                # nothing at the bottom but black
    named(R, 'DESCENT', 820, SY, 0)
    decal30(R, SIGN49B, X1, 0, 'W', 200, 50, 340, 'stairwell sign')
    item(R, 'docb49_087b', -300, 0, -200)
    sbox(R, -400, 0, -260, -320, 80, -140, METAL, 'old desk')
    for z in (-600, 0, 600):
        R.light(-100, H - 70, z, rng=560, color=(255, 225, 190), power=80)
    R.light(300, 300, 0, rng=420, color=(255, 230, 190), power=60)                 # by the opening
    R.light(520, 260, 0, rng=330, color=(255, 214, 170), power=34)                 # one weak bulb over the top steps
    B.clear = [((-110, 0, -1000, 110, 200, 1000), 'walkway'), ((110, 0, -70, 400, 200, 70), 'to the stairs')]
    check_b42(R)
    return (R, '87B', 'SCP-087-B (Light Containment): an old brick room with a narrow stairwell going down into the dark. Nobody has found the bottom.',
            1, 0.4, ((-200, 165, -700), (700, 0, 0)))


ALL = [room2scp087b]
