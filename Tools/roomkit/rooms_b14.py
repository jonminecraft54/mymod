"""Two rooms for two SCPs (the fourteenth batch, code in IndevU14.bb).

  room2lampshop     LCZ  SCP-4035: a lamp with a stained-glass shade on a desk in a side room, a bulb in the storage
                         room to the west. A bulb in the socket and the salesman appears.
  room2saddlestall  HCZ  SCP-3886: a stall with straw and a rack, the saddle on it, and the animal in the straw. A
                         tack room east with the photograph and the journal page.

Same conventions as rooms_b13.py: junction hubs with corridor arms, side rooms from side() behind door_op() holes,
and gen_b14.py turns the room keys into U14_* constants."""
from rooms_b13 import *

R_ = lambda name, amb=11: Room(name, luxel=6.0, ambient=amb, fill=0.14)
STAINED = Mat('indev_stained4035.png', 256)            # made by make_assets14.py


def room2lampshop():
    """The lamp room. The shade is a wide cylinder over a short iron base, on the desk; the lamp's pivot is the
    centre of the shade, where the click is aimed."""
    R = R_('room2lampshop', amb=10)
    junction(R, 'NS', 'lcz', openings={'hubE': [door_op(0)], 'hubW': [door_op(0)]})
    x0, z0, x1, z1 = side(R, 192, +1, 'lcz')
    dtop = desk(R, 400, -140, 600, 140, 0)
    R.tube((520, dtop, 0), (520, dtop + 26, 0), 46, METAL, sides=10, caps=True)          # the base
    R.tube((520, dtop + 40, 0), (520, dtop + 130, 0), 118, STAINED, sides=12, caps=True)  # the shade
    named(R, 'LAMP', 520, dtop + 85, 0)
    item(R, 'doc4035', 450, dtop, -70)
    ceil_light(R, 516, 0, 352, size=40, power=60, rng=640, color=(255, 230, 190))
    plate7(R, 'lamp', x1, 0, 'W', yc=250, w=170)
    # the storage room to the west: the bulb in a crate, the cabinets
    x0, z0, x1, z1 = side(R, -192, -1, 'lcz')
    R.box(-700, 0, -120, -600, 80, 120, WOOD, skip='B', lux=10)                          # the crate
    item(R, 'bulb', -650, 80, 0)
    cabinet_row(R, (-740.0, -340.0), (-740.0, -160.0), 0, 'E', w=56.0)
    ceil_light(R, -516, 0, 352, size=40, power=70, rng=640, color=(240, 250, 255))
    plate7(R, 'noequip', x0, 0, 'E', yc=250, w=170)
    return (R, 'LSH', 'Lamp Room (Light Containment): a stained-glass lamp on a desk, with a storage room west holding the bulbs.',
            1, 0.45, ((300, 165, -300), (520, 150, 0)))


def room2saddlestall():
    """The stall. A partition with a gap, straw on the floor, a rack holding the saddle and the animal (a dark
    block until it is modelled) in the straw. The tack room east has the photograph and the journal page."""
    R = R_('room2saddlestall', amb=11)
    junction(R, 'NS', 'hcz', openings={'hubE': [door_op(0)], 'hubW': [door_op(0)]})
    # east: the tack room
    x0, z0, x1, z1 = side(R, 192, +1, 'hcz')
    dtop = desk(R, 420, -120, 580, 120, 0)
    chair(R, 620, 0, 'W')
    item(R, 'photo3886', 470, dtop, 60)
    item(R, 'doc3886b', 500, dtop, -50)
    ceil_light(R, 516, 0, 352, size=36, power=40, rng=600, color=(255, 230, 190))
    plate7(R, 'quiet', x1, 0, 'W', yc=250, w=170)
    # west: the stall
    x0, z0, x1, z1 = side(R, -192, -1, 'hcz')
    R.rect_floor(-740, -360, -300, 360, 1.5, STRAW, coll=False, lux=10)
    R.box(-530, 0, -380, -522, 140, -80, WOOD, lux=10)                  # the partition, with a gap
    R.box(-530, 0, 80, -522, 140, 380, WOOD, lux=10)
    R.box(-740, 0, -40, -730, 150, 40, METAL, lux=10)                  # the rack post
    R.box(-730, 118, -40, -680, 132, 40, METAL, lux=10)                # the rack shelf
    R.box(-725, 132, -36, -685, 150, 36, DARK, lux=10)                 # the saddle on the rack
    named(R, 'SADDLE', -705, 140, 0)
    named(R, 'ANIMAL', -620, 40, 60)                                   # the animal's centre, in the straw
    reserve(R, 'ANIMALM')                                              # the animal's entity (IndevU14.bb)
    item(R, 'doc3886', -600, 0, -160)
    ceil_light(R, -516, 0, 384, size=40, power=80, rng=760, color=(255, 200, 160))
    ceil_light(R, -640, 0, 384, size=40, power=70, rng=720, color=(255, 200, 160))
    plate7(R, 'nolight', x0, 0, 'E', yc=250, w=170)
    return (R, 'STL', 'Stall (Heavy Containment): straw, a rack with a black saddle, and the animal that stands up in the straw when the saddle is lifted.',
            2, 0.55, ((-150, 165, 0), (-705, 140, 0)))


ALL = [room2lampshop, room2saddlestall]
