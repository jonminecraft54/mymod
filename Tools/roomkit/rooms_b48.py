"""The forty-eighth batch (code in IndevU48.bb): SCP-806, the resurrection projector.

  room2scp806  HCZ  the screening room - one big dark hall the length of the tile: the silver screen across the
                    east end, the open floor before it where the copies form, rows of seats either side of the
                    walkway, the projector on its stand at the west, and Containment Locker 8 - the reel cage -
                    in the north-west corner. The projector, screen, rays and copies are made by the code.
"""
from rooms_b47 import *

SIGN48 = Mat('indev_806sign.png', cast=False)
SEAT = Mat('dirtymetal.jpg', 64)
FABRIC = Mat('indev_b33shade.png', 32)
CARPET = Mat('concretefloor.jpg', 128)


def seat_row(R, x, z0, z1, name):
    """a row of cinema seats facing east (the screen): a base, a seat and a back, one solid for the row"""
    R.box(x, 0, z0, x + 60, 40, z1, SEAT, lux=10)
    R.box(x, 40, z0, x + 60, 48, z1, FABRIC, lux=10)
    R.box(x - 12, 40, z0, x, 120, z1, FABRIC, lux=10)
    for z in range(int(z0) + 60, int(z1), 70):
        R.box(x - 12, 48, z - 3, x + 60, 70, z + 3, SEAT, lux=10)              # arm rests
    solid(R, (x - 12, 0, z0, x + 60, 120, z1), name)


def room2scp806():
    R = R_('room2scp806', amb=18)
    R.book = Book()
    B = R.book
    R.luxel = 24.0
    H = 640.0
    X0, X1 = -900.0, 1000.0
    hall(R, X0, -1024, X1, 1024, 0, H, CONC.but(vs=H, v0=H), CARPET, DARK,
         holes={'N': [(-96, 96, 0, 320)], 'S': [(-96, 96, 0, 320)]})
    B.areas.append((X0, X1, -1024, 1024, H, 0))
    for (z0, z1) in ((-1024, -990), (990, 1024)):                                  # thick end walls (buttons)
        for (a, b) in ((X0, -112), (112, X1)):
            R.box(a, 0, z0, b, H, z1, CONC.but(vs=H, v0=H), lux=40)
        R.box(-112, 320, z0, 112, H, z1, CONC, lux=10)
    # acoustic panels down the long walls, the steel band
    for x in range(-800, 1000, 200):
        for (zw, zf) in ((-990, -984), (984, 990)):
            R.box(x, 120, min(zw, zf), x + 160, 520, max(zw, zf), FABRIC, lux=10)
    # the screen wall: a black frame round where the code puts the silver screen (x 980, z -620..620, y 90..560)
    R.box(980, 0, -700, X1, 80, 700, DARK, lux=10)
    R.box(980, 570, -700, X1, 640, 700, DARK, lux=10)
    for z in (-700, 630):
        R.box(980, 0, z, X1, H, z + 70, DARK, lux=10)
    named(R, 'SCREEN', 978, 325, 0)
    named(R, 'FORM', 700, 0, 0)                                                     # where the copies form
    # the seats: rows either side of the walkway
    for k, x in enumerate((-470, -330, -190, 150, 236)):
        seat_row(R, x, -880, -160, 'seats S%d' % k)
        seat_row(R, x, 160, 880, 'seats N%d' % k)
    # the projector stand at the west; the code puts the projector on it
    sbox(R, -720, 0, -90, -560, 110, 90, METAL, 'projector stand')
    named(R, 'PROJ', -640, 110, 0)
    decal30(R, SIGN48, X0, -500, 'E', 300, 75, 300, 'screening sign', uv=(0, 0.5, 1, 1))
    # Containment Locker 8: the reel cage in the north-west corner, shelves inside, open front
    sbox(R, -900, 0, 560, -880, 300, 990, METAL, 'locker back')
    for k, y in enumerate((0, 90, 180)):
        R.box(-880, y + 40, 580, -760, y + 46, 970, METAL, lux=10)
    solid(R, (-880, 0, 580, -760, 230, 970), 'reel shelves')
    for z in (560, 970):
        R.box(-760, 0, z - 4, -740, 300, z + 4, DARK, lux=10)
    R.box(-900, 296, 556, -740, 304, 994, DARK, lux=10)
    decal30(R, SIGN48, -740, 765, 'E', 300, 75, 340, 'locker sign', uv=(0, 0, 1, 0.5))
    item(R, 'reel806a', -820, 86, 640)
    item(R, 'reel806b', -820, 86, 760)
    item(R, 'reel806c', -820, 176, 640)
    item(R, 'reel806d', -820, 176, 820)
    item(R, 'reel806e', -820, 266, 900)
    item(R, 'doc806', -820, 86, 900)
    item(R, 'docb48_locker', -820, 176, 920)
    item(R, 'docb48_tests', -600, 110, -60)
    # light: very little - the screen is the light when it runs
    R.light(-640, 360, 0, rng=640, color=(255, 236, 210), power=90)
    R.light(-760, 380, 760, rng=520, color=(255, 230, 190), power=80)
    for z in (-900, 900):
        R.light(0, 280, z, rng=300, color=(255, 210, 160), power=26)
    red_emergency(R, 980, 600, 760, 'W', 'red screen', power=18)
    B.clear = [((-110, 0, -1000, 110, 200, 1000), 'walkway'), ((300, 0, -500, 950, 200, 500), 'forming floor'),
               ((-540, 0, -150, -120, 200, 150), 'to the projector')]
    check_b42(R)
    return (R, 'S06', 'SCP-806 (Heavy Containment): the screening room - the silver screen, the seats, the projector on its stand and Containment Locker 8 with the reels. Somebody has to keep watching.',
            2, 0.55, ((-300, 165, -900), (700, 150, 0)))


ALL = [room2scp806]
