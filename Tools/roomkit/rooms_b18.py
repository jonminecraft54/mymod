"""Six rooms of The Hollowcrest (batch 18). Original design, inspired only by the general idea of a quiet, old hotel.
Code in IndevU18.bb.

  room2hcrecep      HCZ  Night reception: a counter with the ledger, the anomaly register and a keycard; a key rack;
                         a small staff office east.
  room2hcguest117   HCZ  Guest Room 117: a bed, a desk, a wardrobe and a telephone that is not connected. It rings.
  room2hcservice    HCZ  Service lift: a lift between the lobby and a service corridor. Its floor display flips
                         between G and S while you stand near it.
  room2hcboiler     HCZ  Boiler chamber: a boiler, pipes and a control panel. The panel reads 90 with the boiler off.
  room2hckitchen    LCZ  Cold kitchen: steel counters, a fridge that starts again while you are alone, a store west.
  room2hcballroom   HCZ  Silent ballroom: a long hall with a stage, a broken chandelier and echoing footsteps.

Helpers are from rooms_b17.py (the hotel plates and carpet) and rooms_b13.py (side rooms, lifts, desks)."""
import json
import os
from rooms_b17 import *

HERE = os.path.dirname(os.path.abspath(__file__))
R_ = lambda name, amb=9: Room(name, luxel=6.0, ambient=amb, fill=0.14)
STYLES['recep18'] = (HOTELW, OLDWOOD, DARK)
STYLES['guest18'] = (HOTELW, HOTELC, DARK)
STYLES['ball18'] = (HOTELW, STAGEF, DARK)
HPL18 = Mat('indev_hollowplates18.png', cast=False)      # made by make_assets18.py
HPL18J = json.load(open(os.path.join(HERE, 'hollowplates18.json')))


def plate18(R, k, cx, cz, facing, yc=250, w=150):
    wall_decal(R, HPL18, cx, cz, facing, w, w * 0.74, yc, uv=HPL18J[k])


def room2hcrecep():
    R = R_('room2hcrecep', amb=9)
    junction(R, 'NS', 'recep18', openings={'hubE': [door_op(0)]})
    # the counter runs along the west side of the hub, clear of the north-south path: the ledger, the register, a keycard
    R.box(-170, 0, -140, -104, 110, 140, OLDWOOD, skip='B', top=OLDWOOD, lux=10)
    item(R, 'doc18led', -137, 110, -60)
    item(R, 'doc18hc', -137, 110, 40)
    item(R, 'key2', -137, 110, -100)
    # the key rack: a board of hooks on the west wall
    R.box(-190, 120, -150, -176, 260, 150, WOOD, skip='B', lux=10)
    plate18(R, 'recep', -190.0, 0.0, 'E', yc=300, w=150)
    ceil_light(R, 0, 0, 384, size=44, power=80, rng=800, color=(255, 226, 170))
    # the staff office, east
    x0, z0, x1, z1 = side(R, 192, +1, 'recep18')
    dtop = desk(R, 420, -120, 560, 120, 0)
    chair(R, 620, 0, 'W')
    item(R, 'bat', 470, dtop, 40)
    ceil_light(R, 516, 0, 352, size=36, power=50, rng=600, color=(255, 226, 170))
    plate18(R, 'staff', x1, 0, 'W', yc=250, w=150)
    return (R, 'REC', 'The Hollowcrest reception (Heavy Containment): a counter with the night ledger and the anomaly register, a key rack, and a staff office east.',
            2, 0.4, ((0, 165, -300), (0, 110, 0)))


def room2hcguest117():
    R = R_('room2hcguest117', amb=8)
    junction(R, 'NS', 'guest18', openings={'hubE': [door_op(0)]})
    x0, z0, x1, z1 = side(R, 192, +1, 'guest18', h=352)
    R.box(560, 0, -300, 760, 52, -120, WOOD, skip='B', lux=10)                 # the bed frame
    R.box(566, 52, -294, 754, 74, -126, WHITEP, skip='B', lux=10)              # the mattress
    R.box(650, 0, 200, 760, 300, 340, WOOD, skip='B', lux=10)                  # the wardrobe
    dtop = desk(R, 290, -140, 380, 0, 0)
    chair(R, 420, -70, 'W')
    named(R, 'PHONE', 300, dtop, -110)                                         # the telephone, on the desk
    item(R, 'key2', 340, dtop, -40)
    item(R, 'doc18g117', 600, 74, -200)
    ceil_light(R, 516, 0, 352, size=28, power=26, rng=520, color=(255, 214, 160))
    plate18(R, 'r117', x1, 0, 'W', yc=260, w=150)
    return (R, 'GST', 'Guest Room 117 (Heavy Containment): a bed, a desk, a wardrobe and a telephone that is not connected to anything.',
            2, 0.6, ((150, 165, -20), (300, 110, -110)))


def room2hcservice():
    """The lobby with the service lift on its west wall, and the service corridor under the lobby's east half
    (the same lift code as the lift lobby of batch 17)."""
    R = R_('room2hcservice', amb=9)
    AW = wmat('lcz', 384)
    D = -704.0
    junction(R, 'NS', 'lcz', hub=(-352, -512, 352, 512), hh=352, openings={'hubW': [door_op(0)]})
    lift(R, -352, -1, 0, 0, 0, D, AW)
    sign_at(R, 'elevator', -352, -250, 'E', 150, 50, 250)
    plate18(R, 'svc', -352, 300, 'E', yc=250, w=150)
    named(R, 'DISPLAY', -340, 200, 150)            # the floor display beside the lift door (quads in IndevU18.bb)
    reserve(R, 'DISPLAYG')                          # the G quad, shown first
    reserve(R, 'DISPLAYS')                          # the S quad, shown when it flips
    # the service corridor under the east half
    X0, X1, ZH, HH = -352.0, 500.0, 300.0, 384.0
    out = [(X0, -ZH), (X0, ZH), (X1, ZH), (X1, -ZH)]
    BW = wmat('dark', HH).but(v0=D + HH)
    R.walls(out, D, D + HH, BW, holes={0: [span(out[0], (X0, -96), (X0, 96)) + (D, D + 320)]})
    R.rect_floor(X0, -ZH, X1, ZH, D, CONC)
    R.rect_ceil(X0, -ZH, X1, ZH, D + HH, DIRTY)
    plate18(R, 'staff', X1, 0, 'W', yc=D + 250, w=150)
    R.box(200, D, -260, 480, D + 96, -200, METAL, skip='B', lux=10)            # a service trolley
    ceil_light(R, 200, 0, D + HH, size=44, power=60, rng=640, color=(240, 240, 255))
    item(R, 'bat', 100, D, 150)
    return (R, 'SVC', 'Service lift (Heavy Containment): a lift between the lobby and a service corridor. Its floor display does not always show the floor you are on.',
            2, 0.3, ((-200, 150, 300), (-340, 200, 150)))


def room2hcboiler():
    R = R_('room2hcboiler', amb=8)
    junction(R, 'NS', 'hcz', openings={'hubE': [door_op(0)]})
    side(R, 192, +1, 'hcz', h=384, depth=600)
    R.prism(octo(560, 0, 140), 0, 300, METAL, caps='TB')                       # the boiler
    R.tube((560, 300, 0), (560, 360, 0), 26, METAL, sides=8, caps=True)       # the flue
    R.tube((700, 0, -200), (700, 300, -200), 20, METAL, sides=8, caps=True)   # a pipe up the wall
    R.box(820, 120, -60, 848, 230, 60, DIRTY, skip='B', lux=10)              # the control panel, on the far wall
    named(R, 'PANEL', 812, 170, 0)                                             # where you stand to press it
    ceil_light(R, 500, 0, 384, size=36, power=40, rng=600, color=(255, 160, 90))
    item(R, 'doc18boil', 420, 0, -220)
    item(R, 'firstaid', 300, 0, 240)
    plate18(R, 'boiler', 856, 0, 'W', yc=300, w=150)
    return (R, 'BLR', 'Boiler chamber (Heavy Containment): an old boiler with a control panel that is warm to the touch. The gauge reads ninety with the boiler off.',
            2, 0.35, ((120, 165, 0), (560, 160, 0)))


def room2hckitchen():
    R = R_('room2hckitchen', amb=10)
    junction(R, 'NS', 'ward', openings={'hubW': [door_op(0)], 'hubE': [door_op(0)]})
    # east: the kitchen. Steel counters down both sides, the fridge on the far wall
    side(R, 192, +1, 'ward', h=352)
    R.box(300, 0, -330, 700, 90, -260, METAL, skip='B', top=METAL, lux=10)
    R.box(300, 0, 260, 700, 90, 330, METAL, skip='B', top=METAL, lux=10)
    R.box(640, 0, -60, 760, 170, 60, METAL, skip='B', lux=10)                   # the fridge
    named(R, 'FRIDGE', 700, 80, 0)                                                # its pivot, in front of it
    item(R, 'doc18kit', 420, 90, -295)
    item(R, 'key5', 500, 90, 290)
    ceil_light(R, 516, 0, 352, size=36, power=70, rng=640, color=(240, 250, 255))
    plate18(R, 'kitchen', 776, 0, 'W', yc=262, w=150)
    # west: the store
    side(R, -192, -1, 'ward', h=352)
    R.box(-740, 0, -200, -640, 150, 200, METAL, skip='B', lux=10)              # a shelving unit
    ceil_light(R, -516, 0, 352, size=36, power=50, rng=560, color=(240, 250, 255))
    return (R, 'KIT', 'Cold kitchen (Light Containment): steel counters, a fridge that starts up when you are alone, and a store to the west.',
            1, 0.45, ((120, 165, 0), (700, 110, 0)))


def room2hcballroom():
    """A long hall, the stage at the west end, the broken chandelier over the floor. The arms run north and south."""
    R = R_('room2hcballroom', amb=7)
    junction(R, 'NS', 'ball18', hub=(-640, -400, 640, 400), hh=560)
    R.box(-640, 0, -300, -420, 50, 300, STAGEF, skip='B', top=STAGEF, lux=10)  # the stage
    item(R, 'key2', -520, 50, 0)
    item(R, 'doc18ball', -470, 50, 200)
    R.box(-70, 470, -70, 70, 500, 70, METAL, lux=10)                           # the chandelier
    R.box(-200, 420, -10, 200, 430, 10, METAL, lux=10)                         # its broken bar, still hanging
    ceil_light(R, -300, 0, 560, size=40, power=40, rng=700, color=(255, 230, 190))
    ceil_light(R, 300, 0, 560, size=40, power=40, rng=700, color=(255, 230, 190))
    named(R, 'ECHO0', 400, 0, -250)                                              # the places the footsteps come from
    named(R, 'ECHO1', 400, 0, 250)
    named(R, 'ECHO2', 0, 0, 0)
    return (R, 'BAL', 'The Silent Ballroom (Heavy Containment): a long hall with a stage at one end, a broken chandelier, and a keycard on the stage.',
            2, 0.55, ((-300, 165, 250), (300, 120, -250)))


ALL = [room2hcrecep, room2hcguest117, room2hcservice, room2hcboiler, room2hckitchen, room2hcballroom]
