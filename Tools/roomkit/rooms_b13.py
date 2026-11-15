"""Six rooms for sixteen SCPs (the thirteenth batch, code in IndevU13.bb). Design notes: b13_design.md.

  room2safewing    LCZ  break room (377 cookies, 978 camera, 3041 knife), isolated-PC room (3045)
  room2biowing     HCZ  vase chamber (019), ball locker (3046, the phone rings), biohazard shelf (3056)
  room2doorhall    HCZ  door 249 in the west wall of the south arm (walk through it and you come out somewhere
                        else), the white 3038 door in the north arm, the dark farmhouse (1983) east
  room2menagerie   HCZ  enclosure (247) east, stores with the dragon box (1762) west
  room2pool354     HCZ  lift down to the red pool chamber (354)
  room2incidents   LCZ  Weissnacht office (4666), records with the sweater (1337), Miss J's PC (5094) in the hub

Geometry: junction() hubs with arms N and S (the arms are 384 wide, x -192..192). A side room from annex() sits
behind a door_op() hole; its interior runs 256..776 along x for the east side and -776..-256 for the west side
(depth 520, 64 of wall at the jamb), and -400..400 along z. gen_b13.py turns the room keys into U13_* constants."""
from rooms_b12 import *

R_ = lambda name, amb=11: Room(name, luxel=6.0, ambient=amb, fill=0.14)
WHITEP = Mat('white.jpg', 256)
REDPOOL = Mat('indev_redpool.png', 128, alpha=True, cast=False)     # made by make_assets13.py


def side(R, plane, sign, style, h=352, depth=520):
    """the standard side room of this batch, its door in the hub wall at z = 0. Returns the interior."""
    return annex(R, 'x', plane, sign, -400, 400, depth, h, style, door=0)


def room2safewing():
    """LCZ break room with the cookies, the camera and the knife; the PC room to the west."""
    R = R_('room2safewing', amb=12)
    junction(R, 'NS', 'lcz', openings={'hubE': [door_op(0)], 'hubW': [door_op(0)]})
    # east: the break room. Cabinets against the far wall, a table with the cookie box, a fridge
    x0, z0, x1, z1 = side(R, 192, +1, 'lcz')
    cabinet_row(R, (740.0, -180.0), (740.0, 340.0), 0, 'W', w=56.0)
    R.box(640, 0, -390, 740, 176, -320, METAL, skip='B', lux=10)          # the fridge
    dtop = desk(R, 380, -120, 530, 120, 0)
    chair(R, 580, 0, 'W')
    ceil_light(R, 516, 0, 352, size=44, power=80, rng=700, color=(255, 246, 236))
    plate7(R, 'quiet', x1, 0, 'W', yc=250, w=170)
    item(R, 'doc377', 440, dtop, 40)
    item(R, 'cookie377', 460, dtop, -60)
    item(R, 'doc978', 600, 0, 240)
    item(R, 'camera978', 620, 0, 180)
    item(R, 'doc3041', 640, 0, -40)
    item(R, 'knife3041', 560, 0, -20)
    # west: the isolated PC room. A desk, the tower under it, one lamp
    x0, z0, x1, z1 = side(R, -192, -1, 'lcz')
    desk(R, -700, -120, -600, 120, 0)
    chair(R, -520, 0, 'E')
    R.box(-700, 76, 80, -660, 150, 120, DARK, lux=10)                     # the tower on the desk
    ceil_light(R, -516, 0, 352, size=40, power=70, rng=640, color=(240, 250, 255))
    plate7(R, 'nolight', x0, 0, 'E', yc=250, w=170)
    item(R, 'doc3045', -650, 76, 0)
    return (R, 'SAF', 'Safe Wing break room (Light Containment): fortune cookies, an old camera and a knife. An isolated PC room to the west.',
            1, 0.35, ((300, 165, -300), (620, 150, 60)))


def room2biowing():
    """HCZ: the vase chamber to the east (SCP-019 on the floor), the ball locker to the west (SCP-3046, the
    phone on the wall), and the biohazard shelf (SCP-3056) in the same locker room."""
    R = R_('room2biowing', amb=9)
    junction(R, 'NS', 'hcz', openings={'hubE': [door_op(0)], 'hubW': [door_op(0)]})
    # east: the vase chamber. The vase is an eight-sided prism on the floor, a red lamp over it
    x0, z0, x1, z1 = side(R, 192, +1, 'hcz', h=384)
    R.prism(octo(600, 0, 80), 0, 300, DIRTY, caps='TB')
    red_lamp(R, 600, 0, 384, power=70, rng=560)
    ceil_light(R, 470, 0, 384, size=40, power=60, rng=700, color=(255, 240, 220))
    item(R, 'doc019', 440, 0, 240)
    plate7(R, 'onemetre', x1, 0, 'W', yc=250, w=200)
    # west: the ball locker and the biohazard shelf
    x0, z0, x1, z1 = side(R, -192, -1, 'hcz', h=384)
    cabinet_row(R, (-740.0, -340.0), (-740.0, 340.0), 0, 'E', w=56.0)
    named(R, 'PHONE', -560, 150, 390)
    ceil_light(R, -516, 0, 384, size=40, power=60, rng=700, color=(240, 250, 255))
    item(R, 'doc3046', -560, 0, -180)
    item(R, 'doc3056', -560, 0, 200)
    item(R, 'firstaid', -420, 0, 0)
    plate7(R, 'uvrun', x0, 0, 'E', yc=250, w=170)
    return (R, 'BIO', 'Biohazard wing (Heavy Containment): a vase chamber, a ball locker with a phone that rings, and a viral sample shelf.',
            2, 0.5, ((250, 165, -120), (600, 120, 60)))


def room2doorhall():
    """HCZ: the south arm has door 249 in its west wall (a real door, see IndevU13.bb), the north arm has the
    white door 3038, and the east hub door opens onto the dark farmhouse (SCP-1983)."""
    R = R_('room2doorhall', amb=11)
    junction(R, 'NS', 'hcz', openings={'hubE': [door_op(0)], 'S_W': [door_op(-300)]})
    # east: the dark farmhouse. A table with the note, low light
    x0, z0, x1, z1 = side(R, 192, +1, 'hcz')
    dtop = desk(R, 430, -90, 570, 90, 0)
    chair(R, 620, 0, 'W')
    item(R, 'doc1983', 480, dtop, 20)
    ceil_light(R, 516, 0, 352, size=36, power=34, rng=520, color=(255, 230, 200))
    # 249: a door in the south arm's west wall, facing the hall. Behind it, nothing but a dark wall (the far side
    # is not a room; the door is taken in IndevU13.bb before anyone gets through)
    R.box(-290, 0, -396, -190, 340, -204, DARK, lux=8)
    ndoor(R, '249', -192, 0, -300, 90, 0, False)
    # 3038: a white door panel on the north arm's west wall. Decoration only, there is no way through
    R.box(-194, 0, 200, -190, 320, 340, WHITEP, skip='B', lux=10)
    item(R, 'doc3038', -120, 0, 280)
    ceil_light(R, -120, 0, 384, size=44, power=110, rng=900, color=(255, 246, 236))
    ceil_light(R, 120, 0, 384, size=44, power=90, rng=800, color=(255, 246, 236))
    ceil_light(R, 0, -300, 384, size=44, power=100, rng=860, color=(255, 246, 236))
    plate7(R, 'lastpage', -192, 500, 'E', yc=250, w=180)
    return (R, 'DRH', 'Door Hall (Heavy Containment): door 249 in the south arm, the white door 3038 in the north arm, and a dark farmhouse room (SCP-1983) east.',
            2, 0.45, ((0, 165, -300), (-192, 150, -300)))


def room2menagerie():
    """HCZ: the 247 enclosure east (a striped low shape, its feed bowl and the note), the stores west (the
    cardboard box of SCP-1762 on a shelf, the note on the floor)."""
    R = R_('room2menagerie', amb=10)
    junction(R, 'NS', 'hcz', openings={'hubE': [door_op(0)], 'hubW': [door_op(0)]})
    x0, z0, x1, z1 = side(R, 192, +1, 'hcz', h=384, depth=640)
    R.box(470, 0, -40, 560, 80, 50, DIRTY, lux=10)                       # the cat, on the floor
    R.box(520, 0, -170, 580, 22, -120, METAL, lux=10)                    # the feed bowl
    item(R, 'doc247', 430, 0, 180)
    ceil_light(R, 516, 0, 384, size=44, power=80, rng=760, color=(255, 246, 236))
    plate7(R, 'lampctl', x1, 0, 'W', yc=250, w=170)
    # west: the stores
    x0, z0, x1, z1 = side(R, -192, -1, 'hcz', h=384)
    R.box(-740, 90, -60, -660, 190, 40, WOOD, skip='B', lux=10)          # the shelf with the box
    item(R, 'doc1762', -600, 0, 120)
    item(R, 'bat', -600, 0, -180)
    ceil_light(R, -516, 0, 384, size=40, power=70, rng=700, color=(255, 240, 220))
    return (R, 'MEN', 'Menagerie (Heavy Containment): a striped enclosure east with a feed bowl, and the stores west with a silver cardboard box marked HERE BE DRAGONS.',
            2, 0.6, ((300, 165, -300), (620, 100, 0)))


def room2pool354():
    """HCZ: the hub with a lift on its west wall, down to a basement hall with a red pool (SCP-354). The lift and
    the stops are the same as the lift lobby of batch 10."""
    R = R_('room2pool354', amb=9)
    AW = wmat('hcz', 384)
    D = -704.0
    junction(R, 'NS', 'hcz', hub=(-352, -512, 352, 512), hh=352, openings={'hubW': [door_op(0)]})
    lift(R, -352, -1, 0, 0, 0, D, AW)
    sign_at(R, 'elevator', -352, -250, 'E', 150, 50, 250)
    # the pool chamber, under the lobby's east half
    X0, X1, ZH, HH = -352.0, 700.0, 520.0, 384.0
    out = [(X0, -ZH), (X0, ZH), (X1, ZH), (X1, -ZH)]
    BW = wmat('dark', HH).but(v0=D + HH)
    R.walls(out, D, D + HH, BW, holes={0: [span(out[0], (X0, -96), (X0, 96)) + (D, D + 320)]})
    R.rect_floor(X0, -ZH, X1, ZH, D, HCZFLOOR)
    R.rect_ceil(X0, -ZH, X1, ZH, D + HH, DIRTY)
    # the red pool: a fluid sheet in a sunken basin, with a concrete edge either side
    R.rect_floor(60, -300, 620, 300, D + 4, REDPOOL, lux=10)
    R.box(40, D - 20, -320, 640, D + 4, -300, CONC, skip='B', top=CONC, lux=10)
    R.box(40, D - 20, 300, 640, D + 4, 320, CONC, skip='B', top=CONC, lux=10)
    ceil_light(R, 200, 0, D + HH, size=48, power=70, rng=760, color=(255, 240, 230))
    red_lamp(R, 500, -200, D + HH, power=50, rng=500)
    item(R, 'doc354', -120, D, 300)
    item(R, 'firstaid', -120, D, -300)
    return (R, 'POL', 'Red Pool chamber (Heavy Containment): a lift down to a basement hall with a red pool. Hostile things climb out of it.',
            2, 0.3, ((-150, D + 150, -420), (300, D + 4, 60)))


def room2incidents():
    """LCZ: the Weissnacht office east (SCP-4666's letter), the records west with the sweater (SCP-1337), and in the
    north arm of the hub, Miss J's PC (SCP-5094)."""
    R = R_('room2incidents', amb=11)
    junction(R, 'NS', 'lcz', openings={'hubE': [door_op(0)], 'hubW': [door_op(0)]})
    # east: the Weissnacht office. A desk, a calendar board on the far wall, the letter
    x0, z0, x1, z1 = side(R, 192, +1, 'lcz')
    dtop = desk(R, 420, -120, 560, 120, 0)
    chair(R, 620, 0, 'W')
    R.box(x1 - 10, 120, -180, x1, 260, -30, WOOD, skip='B', lux=10)     # the calendar board
    item(R, 'doc4666', 470, dtop, 40)
    ceil_light(R, 516, 0, 352, size=44, power=76, rng=700, color=(255, 246, 236))
    plate7(R, 'nodrain', x1, 0, 'W', yc=250, w=170)
    # west: the records room. Cabinets, the note, one lamp
    x0, z0, x1, z1 = side(R, -192, -1, 'lcz')
    cabinet_row(R, (-740.0, -340.0), (-740.0, 340.0), 0, 'E', w=56.0)
    item(R, 'doc1337', -560, 0, -80)
    item(R, 'sweater1337', -560, 0, -130)
    item(R, 'bat', -600, 0, 200)
    ceil_light(R, -516, 0, 352, size=40, power=70, rng=640, color=(240, 250, 255))
    # the north arm: Miss J's PC on a small table at the east side of the arm, clear of the path up the middle
    desk(R, 60, 230, 180, 330, 0)
    R.box(100, 76, 260, 160, 170, 300, DARK, lux=10)                      # the monitor
    item(R, 'doc5094', 130, 76, 280)
    named(R, 'PC', 130, 123, 258)                                  # the monitor's front (IndevU13.bb)
    reserve(R, 'SCREEN')                                            # the screen's quad, made in IndevU13.bb
    return (R, 'INC', 'Incidents room (Light Containment): the Weissnacht office with a letter, the records room with a red sweater, and a school PC in the north arm.',
            3, 0.5, ((0, 165, -40), (-500, 110, -40)))


ALL = [room2safewing, room2biowing, room2doorhall, room2menagerie, room2pool354, room2incidents]
