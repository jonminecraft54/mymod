"""Eight containment wings of the twenty-first batch, sixteen SCPs (two cells each, east and west). Code in
IndevU21.bb. Four containment blocks of four cells (were eight two-cell wings, merged to save map slots). The SCP texts are short summaries of SCP Wiki articles (CC BY-SA 3.0); geometry is our own.

  room2b21wing038   LCZ  SCP-038 (the everything tree)            SCP-063 (the world's best toothbrush)
  room2b21wing1171  LCZ  SCP-1171 (the frosted window that talks)  SCP-507 (a man who keeps vanishing)
  room2b21wing2521  HCZ  SCP-2521 (it takes what is written down)  SCP-343 (an old man who says he is God)
  room2b21wing1437  HCZ  SCP-1437 (a hole to somewhere else)       SCP-1609 (the remains of a chair)
  room2b21wing2006  HCZ  SCP-2006 (it wants to scare you)          SCP-120 (the paddling pool that sends you away)
  room2b21wing151   EZ   SCP-151 (the painting of a wave)          SCP-050 (to the cleverest)
  room2b21wing216   EZ   SCP-216 (the safe of many combinations)   SCP-662 (the butler's bell)
  room2b21wing093   HCZ  SCP-093 (the red sea object)              SCP-1981 (the videotape)
The corridors use the pillared SCP:CB corridor (image 22) where it fits."""
from rooms_b20 import *

GREEN = Mat('indev_b21green.png', 128)          # made by make_assets21.py
WATER = Mat('indev_b21water.png', 128, cast=False)
WAVE = Mat('indev_b21wave.png', cast=False)
TV = Mat('indev_b21tv.png', cast=False)


def _lo(s, a, b):
    return min(a * s, b * s), max(a * s, b * s)


def prop_box(R, s, a, b, z0, z1, y1, mat, y0=0, top=None):
    x0, x1 = _lo(s, a, b)
    R.box(x0, y0, z0, x1, y1, z1, mat, skip='B', top=top or mat, lux=10)


def p038(R, s):                                             # the tree: trunk and crown
    R.tube((660 * s, 0, 0), (660 * s, 200, 0), 22, WOOD, sides=8, caps=True)
    prop_box(R, s, 580, 740, -80, 80, 300, GREEN, y0=180)


def p063(R, s):
    prop_box(R, s, 580, 680, -40, 40, 90, WOOD)              # a stand


def p1171(R, s):
    wall_decal(R, GLASS, 776 * s, 0, 'W' if s > 0 else 'E', 200, 160, 200)
    prop_box(R, s, 700, 776, -110, 110, 120, DARK)           # the sill


def p507(R, s):
    prop_box(R, s, 640, 760, -300, -120, 50, METAL)          # a bunk
    prop_box(R, s, 644, 756, -296, -124, 62, WHITEP, y0=50)


def p2521(R, s):
    prop_box(R, s, 600, 760, -60, 60, 76, DARK)              # an empty table: nothing written may be kept here


def p343(R, s):
    prop_box(R, s, 640, 760, 120, 300, 45, SOFA)             # an armchair
    prop_box(R, s, 740, 760, 120, 300, 110, SOFA, y0=45)


def p1437(R, s):
    R.prism(octo(620 * s, 0, 70), 0, 6, DARK, caps='T')     # the hole: a black disc on the floor


def p1609(R, s):
    for k in range(4):
        prop_box(R, s, 560 + k * 40, 590 + k * 40, -80 + k * 30, -60 + k * 30, 12, WOOD)   # splinters


def p2006(R, s):
    prop_box(R, s, 700, 776, -200, 200, 260, DARK)           # a heavy cabinet it hides in


def p120(R, s):
    R.prism(octo(600 * s, 0, 90), 0, 30, Mat('indev_3008blue.png', 256), caps='T')
    R.prism(octo(600 * s, 0, 80), 30, 31, WATER, caps='T')


def p151(R, s):
    wall_decal(R, WAVE, 776 * s, 0, 'W' if s > 0 else 'E', 220, 160, 200)


def p050(R, s):
    prop_box(R, s, 600, 660, -30, 30, 100, CONC)             # a plinth


def p216(R, s):
    prop_box(R, s, 680, 776, -70, 70, 130, METAL)            # the safe


def p662(R, s):
    prop_box(R, s, 600, 680, -40, 40, 90, WOOD)              # a side table with the bell


def p093(R, s):
    prop_box(R, s, 600, 680, -40, 40, 100, CONC)             # a plinth with the disc


def p1981(R, s):
    prop_box(R, s, 680, 776, -80, 80, 80, WOOD)              # the cabinet with the television
    wall_decal(R, TV, 776 * s, 0, 'W' if s > 0 else 'E', 110, 80, 130)


class _Shift:
    """the room, moved dz along z: lets the props of one cell be drawn round its own centre"""
    def __init__(self, R, dz):
        self.R, self.dz = R, dz

    def box(self, x0, y0, z0, x1, y1, z1, *a, **k):
        return self.R.box(x0, y0, z0 + self.dz, x1, y1, z1 + self.dz, *a, **k)

    def prism(self, pts, *a, **k):
        return self.R.prism([(x, z + self.dz) for x, z in pts], *a, **k)

    def tube(self, p0, p1, *a, **k):
        return self.R.tube((p0[0], p0[1], p0[2] + self.dz), (p1[0], p1[1], p1[2] + self.dz), *a, **k)

    def decal(self, a, b, *r, **k):
        return self.R.decal((a[0], a[1] + self.dz), (b[0], b[1] + self.dz), *r, **k)


CELLS = ((+1, -400), (+1, 400), (-1, -400), (-1, 400))      # side order: east south, east north, west south, west north


def block(name, zone, style, scps):
    """a long containment block: four cells, two each side, doors at z = -400 and 400 off a hub that runs the
    length of the room. Slot k holds the pivot of scps[k]."""
    R = R_(name, amb=9)
    junction(R, 'NS', style, hub=(-192, -704, 192, 704),
             openings={'hubE': [door_op(-400), door_op(400)], 'hubW': [door_op(-400), door_op(400)]})
    for k, (s, c) in enumerate(CELLS):
        annex(R, 'x', 192 * s, s, c - 300, c + 300, 520, 352, style, door=c)
        ceil_light(R, 516 * s, c, 352, size=30, power=40, rng=520)
        plate19(R, 'cells', 192 * s, c + 150, 'W' if s > 0 else 'E', yc=260, w=100)
        named(R, 'S' + scps[k], 600 * s, 0, c)
        globals()['p' + scps[k]](_Shift(R, c), s)
    for k, n in enumerate(scps):
        item(R, 'doc21_' + n, 120 if k % 2 else -120, 0, -620 + 400 * (k // 2) + 60 * (k % 2))
    for z in (-500, 0, 500):
        ceil_light(R, 0, z, 384, size=40, power=55, rng=700)
    desc = 'Containment block, SCP-%s.' % ', SCP-'.join(scps)
    return (R, 'B' + name[-1], desc, zone, 0.5, ((0, 165, -800), (0, 120, 400)))


def room2b21block1():
    return block('room2b21block1', 1, 'cell', ('038', '063', '1171', '507'))


def room2b21block2():
    return block('room2b21block2', 2, 'pillar', ('2521', '343', '1437', '1609'))


def room2b21block3():
    return block('room2b21block3', 1, 'cell', ('2006', '120', '093', '1981'))


def room2b21block4():
    return block('room2b21block4', 3, 'off19', ('151', '050', '216', '662'))


ALL = [room2b21block1, room2b21block2, room2b21block3, room2b21block4]
