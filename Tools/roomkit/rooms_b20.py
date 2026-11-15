"""Five rooms of the twentieth batch: SCP-3008 and four containment wings of two cells each. Code in IndevU20.bb.
The SCP texts are short summaries of SCP Wiki articles (CC BY-SA 3.0); the geometry and textures are our own.

  room2b20store3008  HCZ  SCP-3008's way in: a big furniture-store floor (aisles, beds, sofas, shelving), its staff
                          appear when the store "closes".
  room2b20wing999    LCZ  SCP-999 (east cell, the orange jelly that follows you and cheers you up) and SCP-131 (west
                          cell, two eye pods that follow you).
  room2b20wing529    LCZ  SCP-529 (east, half a cat) and SCP-111 (west, the dragon-snails).
  room2b20wing458    EZ   SCP-458 (east, the pizza box) and SCP-261 (west, the vending machine).
  room2b20wing2295   HCZ  SCP-241 (east, the cookbook) and SCP-113 (west, the red stone)."""
import json
import os
from rooms_b19 import *

HERE = os.path.dirname(os.path.abspath(__file__))
R_ = lambda name, amb=9: Room(name, luxel=6.0, ambient=amb, fill=0.14)
STYLES['store20'] = (Mat('officewall.jpg', 364), TILE, EZCEIL)
BLUE = Mat('indev_3008blue.png', 256)                     # made by make_assets20.py
YEL = Mat('indev_3008yellow.png', 256)
SOFA = Mat('indev_3008fabric.png', 128)
CAT529 = Mat('indev_poster20.png', cast=False)
RED261 = Mat('indev_261.png', 256)
PIZZA = Mat('indev_458.png', 64)


def cell_side(R, sgn, style, plate, slot, extra):
    """a containment cell on one side of the hub: the plate, the pivot of the SCP, the cell's own props"""
    x0, z0, x1, z1 = side(R, 192 * sgn, sgn, style, h=352)
    ceil_light(R, 516 * sgn, 0, 352, size=30, power=40, rng=520)
    plate19(R, 'cells', 192 * sgn, 160, 'W' if sgn > 0 else 'E', yc=260, w=100)
    named(R, slot, 600 * sgn, 0, 0)
    extra(R, sgn)


def wing(name, zone, desc, style, east, west, docs):
    R = R_(name, amb=9)
    junction(R, 'NS', style, openings={'hubE': [door_op(0)], 'hubW': [door_op(0)]})
    cell_side(R, +1, style, None, east[0], east[1])
    cell_side(R, -1, style, None, west[0], west[1])
    for i, d in enumerate(docs):
        item(R, d, 150 if i == 0 else -150, 0, -300 - 60 * i)
    ceil_light(R, 0, -500, 384, size=40, power=60, rng=700)
    ceil_light(R, 0, 500, 384, size=40, power=60, rng=700)
    return (R, 'W' + name[12:], desc, zone, 0.5, ((0, 165, -500), (500, 100, 0)))


def room2b20store3008():
    R = R_('room2b20store3008', amb=12)
    junction(R, 'NS', 'store20', hub=(-768, -640, 768, 640), hh=560)
    # aisles of shelving left and right of the main walk, with gaps to walk between them
    for sx in (-1, 1):
        for z in (-520, -200, 120, 440):
            R.box(sx * 260 if sx > 0 else -700, 0, z, 700 if sx > 0 else -260, 220, z + 60, METAL, top=METAL, lux=10)
            R.box(sx * 270 if sx > 0 else -690, 220, z + 4, 690 if sx > 0 else -270, 226, z + 56, BLUE, lux=10)
        R.box(sx * 760 - (8 if sx > 0 else 0), 380, -400, sx * 760 + (0 if sx > 0 else 8), 460, 400, YEL, lux=10)  # banner
    # a display bed and a sofa at the ends of the aisles
    R.box(300, 0, 560, 500, 50, 630, WOOD, skip='B', lux=10)
    R.box(304, 50, 564, 496, 70, 626, WHITEP, skip='B', lux=10)
    R.box(-500, 0, 560, -300, 45, 630, SOFA, skip='B', top=SOFA, lux=10)
    R.box(-500, 45, 610, -300, 100, 630, SOFA, skip='B', lux=10)
    for x in (-400, 400):
        for z in (-400, 0, 400):
            ceil_light(R, x, z, 560, size=60, power=70, rng=800, color=(255, 252, 240))
    for k in range(4):
        named(R, 'STAFF%d' % k, (-400, 400, -500, 500)[k], 0, (-360, 360, 280, -280)[k])
    named(R, 'SPEAKER', 0, 500, 0)
    reserve(R, 'NIGHT')
    item(R, 'doc20_3008', 120, 0, -600)
    item(R, 'firstaid', -500, 100, 590)
    return (R, 'STR', 'SCP-3008 (Heavy Containment): the floor of a furniture store that goes on further than the building does. Its staff come out at closing time.',
            2, 0.6, ((0, 165, -600), (0, 150, 600)))


def p999(R, s):
    R.box(min(720 * s, 776 * s), 0, 300, max(720 * s, 776 * s), 60, 380, VENT, lux=10)   # the vent it came in by


def p131(R, s):
    R.box(min(700 * s, 760 * s), 0, -100, max(700 * s, 760 * s), 60, 100, METAL, skip='B', top=METAL, lux=10)


def p529(R, s):
    R.box(min(660 * s, 760 * s), 0, 200, max(660 * s, 760 * s), 30, 340, SOFA, skip='B', top=SOFA, lux=10)   # the cat bed
    wall_decal(R, CAT529, 520 * s, 400, 'S', 120, 120, 200)


def p330(R, s):
    R.box(min(560 * s, 640 * s), 0, -40, max(560 * s, 640 * s), 90, 40, WOOD, skip='B', top=WOOD, lux=10)    # the pedestal


def p458(R, s):
    R.box(min(560 * s, 680 * s), 0, -60, max(560 * s, 680 * s), 76, 60, WOOD, skip='B', top=WOOD, lux=10)   # the table
    R.box(min(590 * s, 650 * s), 76, -30, max(590 * s, 650 * s), 82, 30, PIZZA, lux=10)


def p261(R, s):
    R.box(min(700 * s, 776 * s), 0, -70, max(700 * s, 776 * s), 220, 70, RED261, skip='B', lux=10)


def p2295(R, s):
    R.box(min(640 * s, 760 * s), 0, -60, max(640 * s, 760 * s), 50, 60, WOOD, skip='B', top=SOFA, lux=10)


def p113(R, s):
    R.box(min(570 * s, 630 * s), 0, -30, max(570 * s, 630 * s), 100, 30, CONC, skip='B', top=CONC, lux=10)


def room2b20wing999():
    return wing('room2b20wing999', 1, 'Containment wing, SCP-999 and SCP-131 (Light Containment): a playful jelly east, two eye pods west.',
                'cell', ('S999', p999), ('S131', p131), ['doc20_999', 'doc20_131'])


def room2b20wing529():
    return wing('room2b20wing529', 1, 'Containment wing, SCP-529 and SCP-111 (Light Containment): half a cat east, the dragon-snails west.',
                'cell', ('S529', p529), ('S111', p330), ['doc20_529', 'doc20_111'])


def room2b20wing458():
    return wing('room2b20wing458', 3, 'Containment wing, SCP-458 and SCP-261 (Entrance Zone): a pizza box east, a vending machine west.',
                'off19', ('S458', p458), ('S261', p261), ['doc20_458', 'doc20_261'])


def room2b20wing2295():
    return wing('room2b20wing2295', 2, 'Containment wing, SCP-241 and SCP-113 (Heavy Containment): a cookbook east, a red stone west.',
                'hcz', ('S241', p2295), ('S113', p113), ['doc20_241', 'doc20_113'])


ALL = [room2b20store3008, room2b20wing999, room2b20wing529, room2b20wing458, room2b20wing2295]
