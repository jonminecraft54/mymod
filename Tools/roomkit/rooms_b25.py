"""The twenty-fifth batch: 18 SCPs (scps_b25.py) in three six-cell blocks, and an office suite. Code in IndevU25.bb
and the generated IndevU25Table.bb / IndevU25Data.bb.

  room2b25block1..3  six cells each, as in rooms_b24.py; every SCP is clicked, and every one has a low-frequency
                     event of its own while you are near it.
  room2b25offices    Office suite (the user's reference images: the researcher's office with the filing cabinet and
                     observation window, the hoist control room, the records corridor, the break room): four offices
                     off a corridor. A researcher works in the first; the intercom pages now and then."""
from rooms_b24 import *
from scps_b25 import SCPS as SCPS25
from rooms_b21 import _Shift

COL25 = {n: Mat('indev_b25_%s.png' % n, 64) for n, *_ in SCPS25}      # made by make_assets25.py
CONSOLE = Mat('indev_b25console.png', cast=False)
NUMS25 = [n for n, *_ in SCPS25]


def block25(name, zone, style, nums):
    R = R_(name, amb=9)
    junction(R, 'NS', style, hub=(-192, -900, 192, 900),
             openings={'hubE': [door_op(z) for z in ZC], 'hubW': [door_op(z) for z in ZC]})
    data = {n: d for n, *d in SCPS25}
    for k, (s, c) in enumerate(CELLS6):
        n = nums[k]
        annex(R, 'x', 192 * s, s, c - 280, c + 280, 520, 352, style, door=c)
        ceil_light(R, 516 * s, c, 352, size=28, power=38, rng=500)
        plate19(R, 'cells', 192 * s, c + 150, 'W' if s > 0 else 'E', yc=260, w=90)
        named(R, 'S' + n, 600 * s, 100, c)
        prop(_Shift(R, c), s, data[n][1], COL25[n], n in REPLACED)
    for k, n in enumerate(nums):
        item(R, 'doc25_' + n, 130 if k < 3 else -130, 0, -760 + 300 * (k % 3) + 60)
    for z in (-750, -250, 250, 750):
        ceil_light(R, 0, z, 384, size=40, power=50, rng=700)
    return (R, 'B' + name[-1], 'Containment block, SCP-%s.' % ', SCP-'.join(nums), zone, 0.5,
            ((0, 165, -950), (0, 120, 600)))


def room2b25block1():
    return block25('room2b25block1', 1, 'cell', NUMS25[0:6])


def room2b25block2():
    return block25('room2b25block2', 2, 'pillar', NUMS25[6:12])


def room2b25block3():
    return block25('room2b25block3', 3, 'off19', NUMS25[12:18])


def room2b25offices():
    R = R_('room2b25offices', amb=9)
    st = 'off19'
    junction(R, 'NS', st, hub=(-192, -704, 192, 704),
             openings={'hubE': [door_op(-400), door_op(400)], 'hubW': [door_op(-400), door_op(400)]})
    for s, c in CELLS:
        annex(R, 'x', 192 * s, s, c - 300, c + 300, 520, 352, st, door=c)
    # east south: the researcher's office (filing cabinet, desk, chair, hanging lamp, observation window)
    R.box(700, 0, -680, 770, 200, -580, CABINET, skip='B', lux=10)
    dtop = desk(R, 560, -520, 760, -340, 0)
    chair(R, 520, -430, 'E')
    pendant(R, 640, -430, 352, power=90, rng=600, color=(255, 236, 200))
    wall_decal(R, GLASS, 776, -250, 'W', 200, 130, 200)
    named(R, 'RESEARCHER', 420, 0, -560)
    item(R, 'doc25_office', 640, dtop, -470)
    # east north: the control room (desk, consoles, HOIST / DOOR panel)
    R.box(700, 0, 120, 776, 110, 680, DARK, skip='B', top=PANELS, lux=10)
    wall_decal(R, CONSOLE, 776, 400, 'W', 360, 180, 210)
    dtop2 = desk(R, 450, 560, 620, 680, 0)
    chair(R, 530, 500, 'E')
    named(R, 'PANEL', 690, 190, 400)
    red_lamp(R, 600, 400, 352)
    # west south: records (a wall of filing cabinets)
    for z in range(-680, -140, 110):
        R.box(-776, 0, z, -700, 200, z + 100, CABINET, skip='B', lux=10)
    item(R, 'key3', -600, 0, -400, chance=70)
    ceil_light(R, -516, -400, 352, size=30, power=40, rng=520)
    # west north: the break room (table, two chairs, a vending machine)
    R.box(-600, 0, 330, -440, 76, 470, WOOD, skip='B', top=WOOD, lux=10)
    chair(R, -640, 400, 'E')
    chair(R, -400, 400, 'W')
    R.box(-776, 0, 600, -700, 220, 690, RED261, skip='B', lux=10)
    item(R, 'bat', -520, 76, 400)
    ceil_light(R, -516, 400, 352, size=30, power=40, rng=520)
    named(R, 'SPEAKER', 0, 340, 0)
    for z in (-500, 0, 500):
        ceil_light(R, 0, z, 384, size=40, power=55, rng=700)
    return (R, 'OFS', 'Office suite (Entrance Zone): a researcher\'s office, a hoist control room, records and a break room off one corridor.',
            3, 0.4, ((0, 165, -800), (300, 120, -400)))


ALL = [room2b25block1, room2b25block2, room2b25block3, room2b25offices]
