"""Six rooms of the nineteenth batch, from the reference images of 23 Oct 2026. Code in IndevU19.bb.

  room2b19office    EZ   Office 19-A (image 1): filing cabinet, desk, chair, a pendant lamp, two river photographs.
                         A researcher stands by the desk and talks.
  room2b19gallery   LCZ  Observation gallery (image 2): a balcony along the east wall over a tiled floor; two Class-D
                         wait on the floor.
  room2b19hoist     HCZ  Hoist control (image 4): consoles and the HOIST panel; a lift down to the hoist pit, an
                         overflow cell with a toilet, sinks and a bunk (image 6).
  room2b19storage   LCZ  Storage B (image 5): a long corridor of roll-up shutters. Now and then one rattles.
  room2b19h09       HCZ  SCP-H09 chamber (images 3, 8, 15-18): a sign-lined corridor; east, the chamber where the
                         neon emblem redraws itself, and sometimes shows itself behind bars.
  room2b19cells     LCZ  Cell Block D (images 6, 7, 14): two cells off the hub; knocking from D-19B.

The walkways (x -192..192 on the N-S line) are kept clear; furniture stands in the side rooms or against walls."""
import json
import os
from rooms_b18 import *

HERE = os.path.dirname(os.path.abspath(__file__))
R_ = lambda name, amb=9: Room(name, luxel=6.0, ambient=amb, fill=0.14)
PL19 = Mat('indev_plates19.png', cast=False)                 # made by make_assets19.py
PL19J = json.load(open(os.path.join(HERE, 'plates19.json')))
SHUT = Mat('indev_shutter19.png', cast=False)
RIVA = Mat('indev_river19a.png', cast=False)
RIVB = Mat('indev_river19b.png', cast=False)
POSTER = Mat('indev_poster19.png', cast=False)
STYLES['off19'] = (Mat('officewall.jpg', 364), TILE, EZCEIL)


def plate19(R, k, cx, cz, facing, yc=250, w=150):
    wall_decal(R, PL19, cx, cz, facing, w, w * 0.74, yc, uv=PL19J[k])


def toilet_set(R, x0, z0, facing):
    """a toilet, a sink and a bunk against the far wall of a cell (x0 = the wall, facing the room)"""
    s = -1 if facing == 'W' else 1
    R.box(min(x0, x0 + s * 60), 0, z0 - 30, max(x0, x0 + s * 60), 44, z0 + 30, WHITEP, skip='B', lux=10)      # toilet
    R.box(min(x0, x0 + s * 20), 44, z0 - 30, max(x0, x0 + s * 20), 100, z0 + 30, WHITEP, skip='B', lux=10)    # cistern
    R.box(min(x0, x0 + s * 50), 80, z0 + 70, max(x0, x0 + s * 50), 96, z0 + 150, WHITEP, lux=10)            # sink
    R.box(min(x0, x0 + s * 120), 0, z0 - 300, max(x0, x0 + s * 120), 50, z0 - 120, METAL, skip='B', lux=10)  # bunk
    R.box(min(x0, x0 + s * 116), 50, z0 - 296, max(x0, x0 + s * 116), 62, z0 - 124, WHITEP, skip='B', lux=10)


def room2b19office():
    R = R_('room2b19office', amb=8)
    junction(R, 'NS', 'off19', openings={'hubE': [door_op(0)]})
    x0, z0, x1, z1 = side(R, 192, +1, 'off19', h=352)
    R.box(700, 0, -360, 770, 200, -260, CABINET, skip='B', lux=10)              # the filing cabinet
    dtop = desk(R, 560, -120, 760, 60, 0)
    chair(R, 520, -30, 'E')
    pendant(R, 640, -30, 352, power=90, rng=600, color=(255, 236, 200))
    wall_decal(R, RIVA, 776, 200, 'W', 110, 110, 220)
    wall_decal(R, RIVB, 640, 400, 'S', 110, 110, 220)
    item(R, 'doc19off', 640, dtop, -60)
    item(R, 'key3', 700, dtop, 30, chance=60)
    named(R, 'DOCTOR', 420, 0, 200)
    plate19(R, 'office', 192, -150, 'W', yc=250, w=120)
    ceil_light(R, 0, -500, 384, size=40, power=60, rng=700)
    ceil_light(R, 0, 500, 384, size=40, power=60, rng=700)
    return (R, 'OFF', 'Office 19-A (Entrance Zone): a filing cabinet, a desk, two river photographs and a researcher who still waits for his transfer.',
            3, 0.5, ((300, 165, -300), (700, 80, 0)))


def room2b19gallery():
    R = R_('room2b19gallery', amb=10)
    junction(R, 'NS', 'lcz', hub=(-352, -512, 352, 512), hh=560)
    # the balcony along the east wall: deck, rail posts and the rail, out of reach above the floor
    R.box(220, 240, -512, 352, 262, 512, CONC, lux=10)
    for z in range(-480, 481, 80):
        R.box(222, 262, z - 3, 228, 352, z + 3, METAL, lux=10)
    R.box(222, 346, -512, 228, 356, 512, METAL, lux=10)
    for z in (-400, 0, 400):
        R.box(300, 0, z - 14, 328, 240, z + 14, CONC, lux=10)                      # the columns under it
    R.box(-352, 60, -200, -340, 140, -100, VENT, lux=10)                          # vents low on the west wall
    R.box(-352, 60, 100, -340, 140, 200, VENT, lux=10)
    named(R, 'GUARD', 300, 262, 0)
    named(R, 'DCLASS0', -150, 0, 100)
    named(R, 'DCLASS1', -100, 0, 180)
    item(R, 'doc19gal', -300, 0, -400)
    plate19(R, 'gallery', -352, 0, 'E', yc=420, w=150)
    for z in (-300, 300):
        pendant(R, 0, z, 560, power=110, rng=800, color=(255, 230, 210))
    return (R, 'GAL', 'Observation gallery (Light Containment): a balcony along the east wall, and two Class-D waiting on the tiled floor below for a test that was cancelled.',
            1, 0.4, ((-250, 165, -450), (200, 200, 300)))


def room2b19hoist():
    R = R_('room2b19hoist', amb=8)
    AW = wmat('hcz', 384)
    D = -704.0
    junction(R, 'NS', 'hcz', hub=(-352, -512, 352, 512), hh=384, openings={'hubW': [door_op(0)]})
    lift(R, -352, -1, 0, 0, 0, D, AW)
    sign_at(R, 'elevator', -352, -250, 'E', 150, 50, 250)
    plate19(R, 'hoist', -352, 300, 'E', yc=250, w=150)
    # the console wall, east
    R.box(300, 0, -300, 352, 110, 300, DARK, skip='B', top=PANELS, lux=10)
    R.box(330, 110, -300, 352, 300, 300, PANELS, skip='B', lux=10)
    dtop = desk(R, 210, -420, 330, -320, 0)
    chair(R, 180, -370, 'E')
    named(R, 'HOIST', 300, 170, 150)
    red_lamp(R, 300, 0, 384)
    item(R, 'doc19hoist', 260, dtop, -380)
    ceil_light(R, 0, 0, 384, size=44, power=60, rng=700)
    # the pit: an overflow cell under the hub
    X0, X1, ZH, HH = -352.0, 500.0, 360.0, 352.0
    out = [(X0, -ZH), (X0, ZH), (X1, ZH), (X1, -ZH)]
    BW = Mat('Old_Whitewall.jpg', 384).but(v0=D + HH)
    R.walls(out, D, D + HH, BW, holes={0: [span(out[0], (X0, -96), (X0, 96)) + (D, D + 320)]})
    R.rect_floor(X0, -ZH, X1, ZH, D, TILE)
    R.rect_ceil(X0, -ZH, X1, ZH, D + HH, DARK)
    plate19(R, 'pit', X1, 0, 'W', yc=D + 250, w=150)
    R.box(440, D, 60, 500, D + 44, 120, WHITEP, skip='B', lux=10)                  # toilet
    R.box(480, D + 44, 60, 500, D + 100, 120, WHITEP, skip='B', lux=10)
    R.box(450, D + 80, 160, 500, D + 96, 260, WHITEP, lux=10)                      # sink
    R.box(100, D, -360, 300, D + 50, -240, METAL, skip='B', lux=10)                # bunk
    R.box(104, D + 50, -356, 296, D + 62, -244, WHITEP, skip='B', lux=10)
    named(R, 'PITLAMP', 200, D + HH - 10, 0)
    ceil_light(R, 200, 0, D + HH, size=36, power=40, rng=600, color=(240, 240, 255))
    item(R, 'firstaid', 200, D, -300)
    return (R, 'HST', 'Hoist control (Heavy Containment): consoles, the HOIST panel, and a lift down to the hoist pit, where an overflow cell is kept.',
            2, 0.45, ((-200, 165, 300), (300, 170, 150)))


def room2b19storage():
    R = R_('room2b19storage', amb=10)
    junction(R, 'NS', 'store')
    for i, z in enumerate((-700, -350, 350, 700)):
        wall_decal(R, SHUT, -192, z, 'E', 200, 280, 140)
        wall_decal(R, SHUT, 192, z, 'W', 200, 280, 140)
        named(R, 'SHUT%d' % i, -180 if i % 2 else 180, 140, z)
    for z in (-600, 0, 600):
        pendant(R, 0, z, 384, power=110, rng=800, color=(255, 240, 220))
    plate19(R, 'storage', -192, 0, 'E', yc=260, w=140)
    item(R, 'doc19store', 150, 0, -100)
    return (R, 'STO', 'Storage B (Light Containment): a long corridor of roll-up shutters, none of them motorised.',
            1, 0.5, ((0, 165, -850), (0, 140, 400)))


def room2b19h09():
    R = R_('room2b19h09', amb=6)
    junction(R, 'NS', 'pillar', openings={'hubE': [door_op(0)]})
    plate19(R, 'h09', 192, -150, 'W', yc=260, w=120)
    ceil_light(R, 0, -600, 384, size=30, power=40, rng=600)
    ceil_light(R, 0, 600, 384, size=30, power=40, rng=600)
    x0, z0, x1, z1 = side(R, 192, +1, 'hcz', h=384, depth=600)
    named(R, 'MURAL', 840, 200, 0)                                               # the emblem's quads (IndevU19.bb)
    reserve(R, 'MURAL0')
    reserve(R, 'MURAL1')
    reserve(R, 'MURAL2')
    reserve(R, 'MURALX')
    reserve(R, 'GLOW')
    R.box(300, 0, -380, 360, 40, -300, METAL, skip='B', lux=10)                  # a step-stool left behind
    item(R, 'doc19h09', 330, 40, -340)
    ceil_light(R, 400, 0, 384, size=24, power=30, rng=600, color=(255, 140, 140))
    return (R, 'H09', 'SCP-H09 chamber (Heavy Containment): a mural of the Foundation emblem drawn in light, which melts and redraws itself.',
            2, 0.5, ((350, 165, 0), (840, 200, 0)))


def room2b19cells():
    R = R_('room2b19cells', amb=8)
    junction(R, 'NS', 'cell', openings={'hubE': [door_op(0)], 'hubW': [door_op(0)]})
    for x in (-192, 192):
        for z in (-260, 260):
            R.box(x - 24 if x > 0 else x, 0, z - 30, x if x > 0 else x + 24, 384, z + 30, CONC, lux=10)  # pilasters
    plate19(R, 'cells', 192, -170, 'W', yc=260, w=120)
    side(R, 192, +1, 'cell', h=352)
    toilet_set(R, 776, 100, 'W')
    plate19(R, 'cellA', 192, 160, 'W', yc=260, w=100)
    wall_decal(R, POSTER, 520, 400, 'S', 140, 140, 220)
    ceil_light(R, 516, 0, 352, size=30, power=36, rng=500)
    side(R, -192, -1, 'cell', h=352)
    toilet_set(R, -776, 100, 'E')
    plate19(R, 'cellB', -192, 160, 'E', yc=260, w=100)
    named(R, 'KNOCK', -700, 120, 0)
    ceil_light(R, -516, 0, 352, size=30, power=20, rng=420)
    item(R, 'doc19cell', 600, 0, -300)
    item(R, 'bat', -600, 0, 300)
    ceil_light(R, 0, 0, 384, size=40, power=50, rng=700)
    return (R, 'CEL', 'Cell Block D (Light Containment): two cells off the hub. The knocking from D-19B is the pipes.',
            1, 0.55, ((0, 165, -400), (500, 100, 100)))


ALL = [room2b19office, room2b19gallery, room2b19hoist, room2b19storage, room2b19h09, room2b19cells]
