"""The twenty-fourth batch: 25 SCPs (scps_b24.py) in four six-cell containment blocks and a storage lobby with a lift.
Code in IndevU24.bb and the generated IndevU24Table.bb / IndevU24Data.bb.

  room2b24block1..4  six cells each (three a side, doors at z = -600, 0, 600 off a hub the length of the room);
                     24 SCPs. Slot k is the pivot of the block's k-th SCP. Six cells to a room keeps the map from
                     running out of slots.
  room2b24store6h    Storage Room 6H (the user's Amensia reference image): white shelving, benches along the
                     walls, a SECURE. CONTAIN. PROTECT. banner and a poster; a lift on the west wall goes down to
                     the top landing of SCP-087's stairwell."""
from rooms_b23 import *
from scps_b24 import SCPS
from scp_models import REPLACED
from rooms_b21 import _Shift

COL = {n: Mat('indev_b24_%s.png' % n, 64) for n, *_ in SCPS}      # made by make_assets24.py
BANNER = Mat('indev_b24banner.png', cast=False)
POSTER24 = Mat('indev_b24poster.png', cast=False)
STAIRS = Mat('indev_b24stair.png', cast=False)
ZC = (-600, 0, 600)
CELLS6 = [(s, z) for s in (+1, -1) for z in ZC]            # slot order: east south, mid, north; west south, mid, north


def prop(R, s, kind, m, replaced=False):
    """the SCP's object in its cell, drawn round z = 0 (the caller shifts it). replaced: the SCP has a real model
    (scp_models.py), so only its stand (plinth, table, bed) is drawn, not the coloured stand-in"""
    if replaced and kind in ('figure', 'crate', 'tank', 'door'):
        return
    def bx(a, b, z0, z1, y0, y1, mat):
        x0, x1 = sorted((a * s, b * s))
        R.box(x0, y0, z0, x1, y1, z1, mat, skip='B', top=mat, lux=10)
    if kind == 'plinth':
        bx(580, 660, -40, 40, 0, 90, CONC)
        if not replaced:
            bx(595, 645, -25, 25, 90, 130, m)
    elif kind == 'table':
        bx(560, 720, -80, 80, 0, 76, WOOD)
        if not replaced:
            bx(600, 680, -40, 40, 76, 96, m)
    elif kind == 'crate':
        bx(600, 720, -60, 60, 0, 90, m)
    elif kind == 'bed':
        bx(640, 760, -200, -40, 0, 50, METAL)
        bx(644, 756, -196, -44, 50, 62, WHITEP if replaced else m)
    elif kind == 'figure':
        bx(620, 680, -30, 30, 0, 190, m)
    elif kind == 'tank':
        bx(580, 700, -60, 60, 0, 30, METAL)
        bx(600, 680, -40, 40, 30, 110, m)
        R.box(min(585 * s, 695 * s), 30, -55, max(585 * s, 695 * s), 160, 55, GLASS, lux=10)
    elif kind == 'door':
        bx(760, 776, -60, 60, 0, 220, m)
    elif kind == 'poster':
        R.decal((776 * s, 70 * s), (776 * s, -70 * s), 130, 230, m, (0, 0, 1, 1))


def block(name, zone, style, nums):
    R = R_(name, amb=9)
    junction(R, 'NS', style, hub=(-192, -900, 192, 900),
             openings={'hubE': [door_op(z) for z in ZC], 'hubW': [door_op(z) for z in ZC]})
    data = {n: d for n, *d in SCPS}
    for k, (s, c) in enumerate(CELLS6):
        n = nums[k]
        annex(R, 'x', 192 * s, s, c - 280, c + 280, 520, 352, style, door=c)
        ceil_light(R, 516 * s, c, 352, size=28, power=38, rng=500)
        plate19(R, 'cells', 192 * s, c + 150, 'W' if s > 0 else 'E', yc=260, w=90)
        named(R, 'S' + n, 600 * s, 100, c)
        prop(_Shift(R, c), s, data[n][1], COL[n], n in REPLACED)
    for k, n in enumerate(nums):
        item(R, 'doc24_' + n, 130 if k < 3 else -130, 0, -760 + 300 * (k % 3) + 60)
    for z in (-750, -250, 250, 750):
        ceil_light(R, 0, z, 384, size=40, power=50, rng=700)
    return (R, 'B' + name[-1], 'Containment block, SCP-%s.' % ', SCP-'.join(nums), zone, 0.5,
            ((0, 165, -950), (0, 120, 600)))


NUMS = [n for n, *_ in SCPS if n != '087']


def room2b24block1():
    return block('room2b24block1', 1, 'cell', NUMS[0:6])


def room2b24block2():
    return block('room2b24block2', 2, 'pillar', NUMS[6:12])


def room2b24block3():
    return block('room2b24block3', 1, 'cell', NUMS[12:18])


def room2b24block4():
    return block('room2b24block4', 3, 'off19', NUMS[18:24])


def room2b24store6h():
    """Storage 6H: the lobby above, shelving and benches; the lift on the west wall; SCP-087's landing below."""
    R = R_('room2b24store6h', amb=9)
    AW = wmat('lcz', 384)
    D = -704.0
    junction(R, 'NS', 'lcz', hub=(-352, -512, 352, 512), hh=384, openings={'hubW': [door_op(0)]})
    lift(R, -352, -1, 0, 0, 0, D, AW)
    sign_at(R, 'elevator', -352, -250, 'E', 150, 50, 250)
    for z in (-200, 200):                                                       # the white shelving units
        R.box(290, 0, z - 60, 352, 220, z + 60, WHITEP, skip='B', lux=10)
        for y in (60, 120, 180):
            R.box(286, y, z - 60, 290, y + 6, z + 60, DARK, lux=10)
    R.box(110, 0, 430, 290, 70, 512, WHITEP, skip='B', top=WHITEP, lux=10)     # benches in the corners, clear of the walk
    R.box(110, 0, -512, 290, 70, -430, WHITEP, skip='B', top=WHITEP, lux=10)
    wall_decal(R, BANNER, 352, 0, 'W', 340, 120, 290)
    wall_decal(R, POSTER24, -352, 300, 'E', 80, 110, 220)
    ceil_light(R, -150, 0, 384, size=44, power=60, rng=700)
    ceil_light(R, 150, 0, 384, size=44, power=60, rng=700)
    item(R, 'doc24_087', 200, 70, 470)
    # SCP-087's top landing below: a small concrete landing and the first flight going down into the dark
    X0, X1, ZH, HH = -352.0, 300.0, 300.0, 352.0
    out = [(X0, -ZH), (X0, ZH), (X1, ZH), (X1, -ZH)]
    BW = Mat('concretewall.jpg', 384).but(v0=D + HH)
    R.walls(out, D, D + HH, BW, holes={0: [span(out[0], (X0, -96), (X0, 96)) + (D, D + 320)]})
    R.rect_floor(X0, -ZH, X1, ZH, D, CONC)
    R.rect_ceil(X0, -ZH, X1, ZH, D + HH, DARK)
    for k in range(6):                                                          # steps going down, cut off by the wall
        R.box(100 + k * 30, D - 2, -120, 130 + k * 30, D + 4 - k * 4, 120, CONC, lux=10)
    wall_decal(R, STAIRS, 300, 0, 'W', 240, 240, D + 140)
    named(R, 'S087', 160, D + 100, 0)
    ceil_light(R, -100, 0, D + HH, size=24, power=18, rng=400, color=(220, 220, 200))
    return (R, 'S6H', 'Storage Room 6H (Light Containment): shelving, benches and posters, and a lift down to the top landing of SCP-087.',
            1, 0.5, ((200, 165, -400), (-352, 150, 0)))


ALL = [room2b24block1, room2b24block2, room2b24block3, room2b24block4, room2b24store6h]
