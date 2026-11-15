"""Two rooms of the seventeenth batch: The Forgotten Hotel (anomalous room H-17). Code in IndevU17.bb.

  room2hotelcorr    HCZ  floor H: a corridor with room H-16 (a plain guest room) east and the anomalous room H-17 west.
                         H-17's phone rings, its door number changes for a moment, and its light flickers while you
                         are in it. Footsteps come from the far end of the corridor when you are alone in it.
  room2hotellift    HCZ  lift lobby: a clerk at the desk and a lift down to a laundry. The lift stops at those two
                         floors only.

Original design: the carpet, the wallpaper and the plates are made in make_assets17.py; the walls, doors and lights
are SCP:CB's own (the corridor wall style, the annex door, the wall and ceiling lamps). gen_b17.py turns the keys
into U17_* constants. Same geometry conventions as rooms_b13.py."""
import json
import os
from rooms_b13 import *

HERE = os.path.dirname(os.path.abspath(__file__))
R_ = lambda name, amb=9: Room(name, luxel=6.0, ambient=amb, fill=0.14)

HOTELW = Mat('indev_hotelpaper17.png', 512)                 # made by make_assets17.py
HOTELC = Mat('indev_hotelcarpet17.png', 512)
STYLES['hotel17'] = (HOTELW, HOTELC, DARK)
HPL = Mat('indev_hotelplates17.png', cast=False)
HPLJ = json.load(open(os.path.join(HERE, 'hotelplates17.json')))


def hplate(R, k, cx, cz, facing, yc=250, w=150):
    """a room-number plate on a wall (the square of the plate sheet)"""
    wall_decal(R, HPL, cx, cz, facing, w, w, yc, uv=HPLJ[k])


def room2hotelcorr():
    """The corridor: lamps along both arms, sconces, and the two guest rooms off the hub. H-16 is east and plain;
    H-17 is west and is the one the code watches (room units x < -256, |z| < 400)."""
    R = R_('room2hotelcorr', amb=9)
    junction(R, 'NS', 'hotel17', openings={'hubE': [door_op(0)], 'hubW': [door_op(0)]})
    for z in (-700.0, -350.0, 350.0, 700.0):
        ceil_light(R, 0, z, 384, size=40, power=44, rng=620, color=(255, 214, 160))
    for z in (-600.0, 600.0):
        wall_light(R, -190.0, z, 210, 'E', power=34, rng=360, color=(255, 200, 130))
        wall_light(R, 190.0, z, 210, 'W', power=34, rng=360, color=(255, 200, 130))
    hplate(R, 'h14', -190.0, -250.0, 'E', yc=250, w=120)
    hplate(R, 'stairs', 190.0, -250.0, 'W', yc=250, w=120)
    # room H-16, east: a plain guest room. A bed, a dresser of postcards, the housekeeping note on the bed
    x0, z0, x1, z1 = side(R, 192, +1, 'hotel17')
    R.box(560, 0, -300, 760, 52, -120, WOOD, skip='B', lux=10)              # the bed frame
    R.box(566, 52, -294, 754, 74, -126, WHITEP, skip='B', lux=10)           # the mattress
    R.box(640, 0, 180, 760, 110, 260, WOOD, skip='B', top=WOOD, lux=10)     # the dresser
    ceil_light(R, 516, 0, 352, size=36, power=40, rng=560, color=(255, 214, 160))
    hplate(R, 'h16', x1, 0, 'W', yc=250, w=150)
    item(R, 'doc17hk', 640, 74, -200)
    # room H-17, west: the anomalous one. A bed, the dresser with the register and the phone, the key on the bed
    x0, z0, x1, z1 = side(R, -192, -1, 'hotel17')
    R.box(-760, 0, -300, -560, 52, -120, WOOD, skip='B', lux=10)
    R.box(-754, 52, -294, -566, 74, -126, WHITEP, skip='B', lux=10)
    R.box(-760, 0, 180, -640, 110, 260, WOOD, skip='B', top=WOOD, lux=10)
    named(R, 'PHONE', -700, 110, 220)                                       # the phone on the dresser
    named(R, 'LIGHT17', -516, 330, 0)                                       # the flickering lamp, high up
    reserve(R, 'LIGHTM')                                                    # the lamp's entity (IndevU17.bb)
    named(R, 'FAR', 0, 60, 900)                                             # the far end of the corridor, for the footsteps
    named(R, 'DOORPLATE', -188, 348, 0)                                     # the number plate over H-17's door (a runtime quad)
    reserve(R, 'PLATE17')                                                   # the plate reading H-17 (IndevU17.bb)
    reserve(R, 'PLATE71')                                                   # the plate reading H-71, shown while you pass
    item(R, 'doc17reg', -700, 110, 190)
    item(R, 'key2', -670, 74, -200)
    ceil_light(R, -516, 0, 352, size=30, power=18, rng=460, color=(255, 200, 150))
    return (R, 'COR', 'The Forgotten Hotel, floor H (Heavy Containment): a corridor with room H-16 east and the anomalous room H-17 west.',
            2, 0.5, ((60, 170, -120), (-600, 150, 0)))


def room2hotellift():
    """The lobby: a clerk's desk across the middle, the lift on the west wall down to the laundry. The laundry is a
    concrete hall with steel washers, under the lobby's east half (as the pool chamber of batch 13)."""
    R = R_('room2hotellift', amb=9)
    AW = wmat('hotel17', 384)
    D = -704.0
    junction(R, 'NS', 'hotel17', hub=(-352, -512, 352, 512), hh=352, openings={'hubW': [door_op(0)]})
    lift(R, -352, -1, 0, 0, 0, D, AW)
    sign_at(R, 'elevator', -352, -250, 'E', 150, 50, 250)
    hplate(R, 'lift', -352, 300, 'E', yc=250, w=150)
    dtop = desk(R, 90, 160, 300, 280, 0)
    named(R, 'CLERK', 120, 0, 340)                                          # the clerk stands behind the desk
    item(R, 'doc17cl', 200, dtop, 220)
    ceil_light(R, -200, -300, 352, size=48, power=70, rng=700, color=(255, 232, 196))
    ceil_light(R, 200, 300, 352, size=48, power=60, rng=700, color=(255, 232, 196))
    # the laundry
    X0, X1, ZH, HH = -352.0, 700.0, 520.0, 384.0
    out = [(X0, -ZH), (X0, ZH), (X1, ZH), (X1, -ZH)]
    BW = wmat('dark', HH).but(v0=D + HH)
    R.walls(out, D, D + HH, BW, holes={0: [span(out[0], (X0, -96), (X0, 96)) + (D, D + 320)]})
    R.rect_floor(X0, -ZH, X1, ZH, D, CONC)
    R.rect_ceil(X0, -ZH, X1, ZH, D + HH, DIRTY)
    hplate(R, 'laundry', X1, 0, 'W', yc=D + 250, w=150)
    R.box(300, D, -420, 680, D + 96, -360, METAL, skip='B', lux=10)         # the row of washers
    ceil_light(R, 200, 0, D + HH, size=44, power=64, rng=700, color=(240, 240, 255))
    item(R, 'bat', -120, D, 300)
    return (R, 'LOB', 'The Forgotten Hotel, lift lobby (Heavy Containment): a clerk at the desk, and the lift down to the laundry.',
            2, 0.3, ((-200, 150, 300), (120, 150, 340)))


ALL = [room2hotelcorr, room2hotellift]
