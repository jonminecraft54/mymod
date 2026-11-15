"""One room built from the reference photo the tenth and eleventh batches did not use (the twelfth batch,
code in IndevT12.bb).

  room2balconycells   HCZ  Balcony Cell Block, from photo 2 (173brihhght.webp): a double-height tiled cell hall with
                           a gallery along the west wall, reached by a stair from the south end and railed over the
                           pit. Red pendants hang from the dark ceiling, two vent grilles sit high on the far wall.
                           A cell log lies on the gallery desk, a battery on the floor of the gallery.

Same conventions as rooms_b11.py: the hall is a junction hub with the corridor arms running north and south, and
gen_b12.py turns the room key into T12_* constants."""
from rooms_b11 import *

HALL = (-768.0, -640.0, 192.0, 640.0)   # the hall: x0, z0, x1, z1
HH = 640.0                              # hall height (the photo's ceiling is high and dark)
GAL = 256.0                             # the gallery floor height
STAIR_Z = -560.0                        # the stair starts at the south end of the hall


def R_(name, amb=9):
    """Built at 6 units per luxel, the same density as the tenth and eleventh batches."""
    return Room(name, luxel=6.0, ambient=amb, fill=0.14)

# the handwritten note of this batch (make_docs12.py writes it to GFX\items)
TEXTS = {
    'docbal1b': ({0: 'Cell Block C - gallery log', 1: 'Cells C-07 to C-12 locked at 22:00.',
                  2: 'Block warden on the gallery all night.', 4: 'Cell C-09 answers the knock twice.',
                  5: 'Nobody has opened it since.', 7: 'Do not stand at the railing after',
                  8: 'the red lamps come on.', 10: 'The men below stop walking', 11: 'when you look up.'},
                 '- Block warden, C wing'),
}


def room2balconycells():
    """Photo 2: the hall in the middle, a gallery along the west wall. The stair climbs north from the south-west
    corner (an 80-unit strip is left between the south wall and the stair foot, so the stair can be reached),
    and the gallery is a solid block with a tiled top and a railing over the pit. The west wall behind the
    gallery has a dark door panel."""
    R = R_('room2balconycells', amb=9)
    junction(R, 'NS', 'pillar', hub=HALL, hh=HH)
    WALL = STYLES['pillar'][0]
    # the stair: 16 steps, each 16 high and 32 deep, from the south end up to the gallery floor
    stairs(R, -768.0, -512.0, STAIR_Z, 16, 16.0, 32.0, +1, 0, WALL, top=TILE)
    z_top = STAIR_Z + 16 * 32.0
    # the gallery: a solid block, tiled on top, from the top of the stair to the north wall
    R.box(-768, 0, z_top, -512, GAL, 640, WALL, skip='B', top=TILE, lux=10)
    railing(R, (-512.0, z_top), (-512.0, 640.0), GAL)
    # the dark door panel on the back wall, above the gallery floor (no way through: a store behind it)
    R.box(-768, GAL, -120, -760, GAL + 320, 120, DARK, lux=10)
    # the far wall: two vent grilles, high, one each side of the north arm
    for x0, x1 in ((-480.0, -400.0), (-340.0, -260.0)):
        R.box(x0, 160, 628, x1, 240, 640, VENT, lux=10)
    # lights: red pendants over the pit, a white ceiling lamp for the pit, and the gallery lamps
    for z in (-380.0, 0.0, 380.0):
        pendant(R, -300, z, HH, power=80, rng=900, color=(255, 150, 120))
    ceil_light(R, -300, 0, HH, size=56, power=110, rng=1000, color=(255, 245, 230))
    ceil_light(R, -300, -380, HH, size=48, power=90, rng=900, color=(255, 245, 230))
    ceil_light(R, -300, 380, HH, size=48, power=90, rng=900, color=(255, 245, 230))
    red_lamp(R, -640, -160, HH, power=60, rng=600)
    ceil_light(R, -640, 200, HH, size=40, power=60, rng=700, color=(255, 240, 220))
    # the gallery desk, under the lamp, with its chair on the tiled top
    dtop = desk(R, -740, 60, -640, 240, GAL)
    chair(R, -600, 150, 'W', y=GAL)
    # the things to find
    item(R, 'docbal1b', -700, dtop, 150)
    item(R, 'bat', -560, GAL, 400)
    item(R, 'firstaid', 100, 0, -400)
    return (R, 'BAL', 'Balcony Cell Block (Heavy Containment): a double-height cell hall with a railed gallery up a stair. A cell log lies on the gallery desk.',
            2, 0.4, ((60, 170, -560), (-640, 150, 300)))


ALL = [room2balconycells]
