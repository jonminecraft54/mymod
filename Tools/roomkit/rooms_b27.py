"""The twenty-seventh batch: SCP-2107 "Diet Ghost". Code in IndevU27.bb; the can is made by make_scp2107.py.
The SCP text is a short summary of scp-wiki.wikidot.com/scp-2107 (CC BY-SA 3.0); room and art are our own.

  room2b27diet  LCZ  The CNSI storage room (the user's reference image: white walls, a black ceiling, a dark floor,
                     two white shelving units with the SECURE. CONTAIN. PROTECT. banner and a red poster, tables
                     along the walls, a camera in the corner) holding the cans on its shelves and a refrigerated
                     CNSI unit for trials; across the corridor, a break room with the vending machine that once
                     produced fifteen cans by itself."""
from rooms_b26 import *

DIETPOSTER = Mat('indev_2107poster.png', cast=False)
CARPET = Mat('indev_o_asphalt.png', 200)
STYLES['store27'] = (Mat('whitewall.jpg', 364), CARPET, DARK)
SHELF = Mat('white.jpg', 128)


def shelving(R, x0, z0, x1, z1, h=230, shelves=4):
    """a white shelving unit: two side panels and dark shelves, open front (towards -x)"""
    R.box(x0, 0, z0, x1, h, z0 + 8, SHELF, lux=10)
    R.box(x0, 0, z1 - 8, x1, h, z1, SHELF, lux=10)
    for k in range(shelves + 1):
        y = 10 + k * (h - 20) / shelves
        R.box(x0, y, z0 + 8, x1, y + 5, z1 - 8, DARK, lux=10)


def bench(R, x0, z0, x1, z1, top=78):
    R.box(x0, top - 6, z0, x1, top, z1, SHELF, lux=10)
    for x in (x0 + 20, x1 - 30):
        R.box(x, 0, z0 + 10, x + 10, top - 6, z1 - 10, DARK, lux=10)


def room2b27diet():
    R = R_('room2b27diet', amb=10)
    junction(R, 'NS', 'store27', openings={'hubE': [door_op(0)], 'hubW': [door_op(0)]})
    for z in (-600.0, 600.0):
        ceil_light(R, 0, z, 384, size=40, power=55, rng=700)
    plate19(R, 'storage', 192, -170, 'W', yc=270, w=120)
    # east: the CNSI storage room, as in the reference image
    side(R, 192, +1, 'store27', h=352, depth=560)
    shelving(R, 760, -240, 816, -100)
    shelving(R, 760, 100, 816, 240)
    wall_decal(R, POSTER24, 816, 0, 'W', 80, 110, 200)                       # WE ARE HERE TO PROTECT YOU
    wall_decal(R, BANNER, 520, -400, 'N', 320, 112, 230)                     # SECURE. CONTAIN. PROTECT.
    wall_decal(R, DIETPOSTER, 520, 400, 'S', 120, 160, 210)
    bench(R, 320, -390, 700, -330)
    bench(R, 320, 330, 700, 390)
    R.box(300, 0, 200, 400, 200, 300, WHITEP, skip='B', lux=10)              # the refrigerated CNSI unit
    R.box(395, 80, 220, 402, 160, 232, DARK, lux=10)                         # its handle
    named(R, 'FRIDGE', 410, 100, 250)
    R.box(800, 300, 340, 816, 330, 356, DARK, lux=10)                        # the camera's bracket
    ceil_light(R, 420, -200, 352, size=40, power=60, rng=620, color=(250, 248, 240))
    ceil_light(R, 620, 200, 352, size=40, power=60, rng=620, color=(250, 248, 240))
    for k, (x, y, z) in enumerate(((785, 70, -170), (785, 122, 170), (785, 175, -150))):
        item(R, 'scp2107', x, y, z)
    item(R, 'doc2107', 500, 78, -360)
    # west: the break room and its vending machine
    side(R, -192, -1, 'store27', h=352, depth=520)
    named(R, 'VEND', -700, 0, 200)
    R.box(-560, 0, -260, -400, 76, -100, WOOD, skip='B', top=WOOD, lux=10)
    chair(R, -600, -180, 'E')
    chair(R, -360, -180, 'W')
    wall_decal(R, DIETPOSTER, -776, -200, 'E', 100, 134, 200)
    ceil_light(R, -516, 0, 352, size=36, power=55, rng=600, color=(255, 244, 228))
    return (R, 'DGT', 'SCP-2107 storage (Light Containment): a CNSI storage room of Diet Ghost cans and a refrigerated unit, and a break room with the vending machine that once made fifteen of them.',
            1, 0.45, ((300, 165, 0), (816, 140, 0)))


ALL = [room2b27diet]
