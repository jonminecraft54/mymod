"""Three rooms built from the reference photos (the eleventh batch, code in IndevT11.bb).

  room2hoistoffice   LCZ  Hoist Office, from photo 4: a control office with a filing-cabinet run, a desk under a
                          monitor wall, a HOIST / DOOR panel and a red warning lamp. A keycard and a log on the desk.
  room2shutterhall   HCZ  Shutter Hall, from photo 5: a long corridor with grey containment shutters on both sides
                          and hanging red lamps. Four shutters are closed for good, one has a closure log on the floor.
  room2machinecorr   LCZ  Machine Corridor, from photos 3 and 8: a corridor with a glass window onto a machine alcove
                          (cabinets, a service block with green status lights). A memo on the machine top.

Same conventions as rooms_b10.py: the corridor cell (junction) and the side rooms (annex) share the 2048 cell,
doors are door_op() holes in the hub walls, and gen_b11.py turns the room keys into T11_* constants."""
from rooms_b10 import *

SHUTTER = Mat('containment_doors.jpg', 256)


def R_(name, amb=11):
    """Built at 6 units per luxel, the same density as the tenth batch, so the atlas stays at or under 2048."""
    return Room(name, luxel=6.0, ambient=amb, fill=0.14)

# the handwritten notes of this batch (make_docs11.py writes them to GFX\items)
TEXTS = {
    'docho1b': ({0: 'Hoist Office - operator log', 1: 'HOIST switched to manual at 23:50.',
                 2: 'Load platform 3 reported weight over limit.', 4: 'Platform is empty. The sensor still',
                 5: 'reads it as full. Nobody has checked why.', 7: 'DOOR panel shows the blast door',
                 8: 'closed, but the light on the desk stays red.', 10: 'Do not rely on the panel. Walk down',
                 11: 'to the hoist and count the cables yourself.'}, '- Operator, shift C'),
    'docshut1b': ({0: 'Shutter 4 closure record', 1: 'Shutters 1 to 4 closed for containment.',
                   2: 'Shutter 4 closed with someone on the', 3: 'inside. The door never reopened.',
                   5: 'Logged again at 03:00 with the same', 6: 'name. Logged again at 04:00.',
                   8: 'Do not open shutter 4 for any reason.', 10: 'Re-check the log on the hour.'}, '- Security, B wing'),
    'docmach1b': ({0: 'Machine Alcove - service memo', 1: 'The green lights on unit 2 are not a fault.',
                   2: 'They blink in the same order as the', 3: 'lights on the far wall of the corridor.',
                   5: 'Stop watching the window at night.', 7: 'Service team B will not return to the alcove.',
                   9: 'The machines were already running', 10: 'when we arrived. Nobody remembers', 11: 'switching them on.'},
                  '- Service team A'),
}


def room2hoistoffice():
    """Photo 4: an office on the west side of the corridor. Filing cabinets along the north wall, a desk
    under the monitor wall with the HOIST / DOOR panel, a red lamp on the desk and a keycard on it."""
    R = R_('room2hoistoffice', amb=11)
    junction(R, 'NS', 'lcz', openings={'hubW': [door_op(0)]})
    x0, z0, x1, z1 = annex(R, 'x', -192, -1, -400, 400, 520, 352, 'std', door=0)
    # filing cabinets along the north wall, drawers facing into the room
    cabinet_row(R, (-700.0, 360.0), (-420.0, 360.0), 0, 'S', w=56.0)
    # monitor wall on the far (west) wall: three dark screens over a desk
    for z in (-120.0, 0.0, 120.0):
        R.box(-772, 150, z - 58, -760, 230, z + 58, DARK, skip='B', lux=10)
    dtop = desk(R, -740, -170, -640, 170, 0)
    chair(R, -600, 0, 'W')
    # the HOIST / DOOR panel, a steel box on the wall beside the screens
    R.box(-772, 120, -250, -760, 240, -170, DIRTY, skip='B', lux=10)
    R.box(-772, 126, -230, -762, 180, -190, DARK, lux=10)
    red_lamp(R, -700, 270, 352, power=50, rng=460)
    pendant(R, -560, 0, 352, power=110, rng=640)
    ceil_light(R, -470, 0, 352, size=48, power=80, rng=680, color=(255, 250, 236))
    # the far wall of this annex is x0 (the room runs west from the door at x1)
    plate7(R, 'level2', x0, 210, 'E', yc=250, w=170)
    # the things to find
    item(R, 'docho1b', -700, dtop, -60)
    item(R, 'key2', -670, dtop, 70)
    item(R, 'bat', -340, 0, 300)
    return (R, 'HOF', 'Hoist Office (Light Containment): a control office with a monitor wall and a HOIST / DOOR panel. A keycard and an operator log lie on the desk.',
            1, 0.6, ((-300, 165, -300), (-700, 150, 0)))


def room2shutterhall():
    """Photo 5: a long corridor (junction NS) with grey containment shutters on both sides. Two shutters on
    each wall, the lamps hang red, and shutter 4 (the north-east one) has the closure log in front of it."""
    R = R_('room2shutterhall', amb=9)
    junction(R, 'NS', 'hcz', w=192.0, ch=384.0)
    # shutters: flat leaves on both walls, facing into the corridor (decal() lifts the leaf towards its
    # normal, which points to the right of a..b, so the east wall runs south-to-north and the west north-to-south)
    for z0_, z1_ in ((-640.0, -400.0), (400.0, 640.0)):
        R.decal((192, z1_), (192, z0_), 0, 320, SHUTTER, (0, 0, 1, 1), off=2.0, cast=True)
        R.decal((-192, z0_), (-192, z1_), 0, 320, SHUTTER, (0, 0, 1, 1), off=2.0, cast=True)
    # frames around the shutters, on the corridor side of each wall (the wall is at x = +-192)
    for z0_, z1_ in ((-640.0, -400.0), (400.0, 640.0)):
        for s in (1, -1):
            xw = 192.0 * s
            xi = xw - 6.0 * s
            lo_x, hi_x = sorted((xw, xi))
            R.box(lo_x, 0, z0_ - 8, hi_x, 332, z0_, DARK, lux=10)
            R.box(lo_x, 0, z1_, hi_x, 332, z1_ + 8, DARK, lux=10)
    # lamps: the ceiling lights hang red over the corridor
    ceil_light(R, 0, 0, 384, size=48, power=80, rng=700, color=(255, 240, 220))
    pendant(R, 0, -500, 384, power=120, rng=720, color=(255, 120, 96))
    pendant(R, 0, 500, 384, power=120, rng=720, color=(255, 120, 96))
    red_lamp(R, 0, -120, 384, power=70, rng=520)
    red_lamp(R, 0, 120, 384, power=70, rng=520)
    # the things to find: the closure log on the floor in front of shutter 4
    item(R, 'docshut1b', 120, 0, 480)
    item(R, 'bat', -120, 0, -460)
    return (R, 'SHU', 'Shutter Hall (Heavy Containment): a long corridor with four grey containment shutters and red hanging lamps. A closure log lies on the floor in front of shutter 4.',
            2, 0.4, ((0, 150, -760), (0, 150, 760)))


def room2machinecorr():
    """Photos 3 and 8: a corridor whose east wall has a glass window onto a machine alcove. Cabinets along the
    alcove's far wall, a service block with status lights in the middle, and a memo on top of the block."""
    R = R_('room2machinecorr', amb=10)
    win = (-96.0, 96.0, 120.0, 260.0)
    junction(R, 'NS', 'lcz', openings={'hubE': [win]})
    x0, z0, x1, z1 = annex(R, 'x', 192, +1, -400, 400, 520, 352, 'std', window=win)
    # the glass in the window opening
    R.box(190, win[2], win[0], 194, win[3], win[1], GLASS, lux=10)
    # cabinets along the far (east) wall, drawers facing west into the alcove
    cabinet_row(R, (740.0, -340.0), (740.0, 340.0), 0, 'W', w=56.0)
    # the service block: a steel box with a top, and two status panels on its side
    R.box(520, 0, -220, 640, 220, 220, METAL, skip='B', top=METAL, lux=10)
    R.box(644, 110, -160, 648, 200, -60, LIGHTPANEL, lux=10)
    R.box(644, 110, 60, 648, 200, 160, LIGHTPANEL, lux=10)
    ceil_light(R, 470, 0, 352, size=40, power=76, rng=640, color=(240, 250, 255))
    ceil_light(R, 620, 0, 352, size=40, power=60, rng=520, color=(240, 250, 255))
    red_lamp(R, 300, 0, 352, power=40, rng=420)
    # the corridor side: a light over the window so the glass reads from the hall
    ceil_light(R, 0, 0, 384, size=40, power=60, rng=560, color=(255, 250, 236))
    # the things to find: the memo on top of the service block
    item(R, 'docmach1b', 580, 220, 0)
    item(R, 'firstaid', 340, 0, 250)
    return (R, 'MAC', 'Machine Corridor (Light Containment): a corridor with a glass window onto a machine alcove. A service memo lies on the machine top.',
            1, 0.5, ((-300, 170, -300), (620, 140, 0)))


ALL = [room2hoistoffice, room2shutterhall, room2machinecorr]
