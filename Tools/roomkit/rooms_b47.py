"""The forty-seventh batch (code in IndevU47.bb): legacy rooms for the Indev zone, built after early screenshots -
bare stained concrete under a black ceiling, a riveted steel band round the top of every wall, plain white
wooden chairs, the old grey cabinets, and every door the old single steel slab with a red push button.

  room2closetsolderones  the old starting room: the gear laid out on a steel table (gas mask, battery,
                         orientation sheet), cabinets, chairs, and the blinding white doorway at the end
  room2oldconference     the early conference room: one long table, white chairs (one knocked over), the
                         whiteboard, a red book, the vent box in the ceiling
  room2oldmedibay        the first medical bay: whitewashed walls, beds, cabinets, a sink, the treatment table
  room2oldcores          the early core chambers: three bays off one corridor - the bell on its pedestal,
                         the refining machine's two booths, and the old man's corroded chamber
"""
from rooms_b46 import *

CONC = Mat('concretewall.jpg', 256)
WHITEW = Mat('Old_Whitewall.jpg', 256)
CFLOOR = Mat('concretefloor.jpg', 256)
BAND = Mat('dirtymetal.jpg', 64)
GLOW = Mat('white.jpg', 64)
BOARD = Mat('scpcb_whiteboard.jpg', cast=False)
H = 384.0


def shell(R, name, x0, x1, wall, luxel=20.0, amb=None):
    """the whole tile from z -1024 to 1024 (the map's doors at both ends), x0..x1 wide, a black ceiling, the
    riveted band at the top and a dark skirting at the floor; thick end walls so the door buttons sit on a wall"""
    R.book = Book()
    B = R.book
    R.luxel = luxel
    hall(R, x0, -1024, x1, 1024, 0, H, wall.but(vs=H, v0=H), CFLOOR, DARK,
         holes={'N': [(-96, 96, 0, 320)], 'S': [(-96, 96, 0, 320)]})
    B.areas.append((x0, x1, -1024, 1024, H, 0))
    for (z0, z1) in ((-1024, -990), (990, 1024)):
        for (a, b) in ((x0, -112), (112, x1)):
            R.box(a, 0, z0, b, H, z1, wall.but(vs=H, v0=H), lux=40)
        R.box(-112, 320, z0, 112, H, z1, wall, lux=10)                           # over the door
    # the riveted steel band under the ceiling and the dark skirting, all round
    for (a0, a1, b0, b1) in ((x0, x0 + 6, -990, 990), (x1 - 6, x1, -990, 990)):
        R.box(a0, H - 34, b0, a1, H - 10, b1, BAND, lux=10)
        R.box(a0, 0, b0, a1, 18, b1, DARK, lux=10)
    for z in (-990, 984):
        R.box(x0, H - 34, z, x1, H - 10, z + 6, BAND, lux=10)
    return B


def chair(R, x, z, yaw, name):
    model30(R, 'scpcb_chair.x', x, 0, z, yaw, (40, 104, 40), name)


def cab(R, x, z, yaw, name):
    model30(R, 'scpcb_cabinet.x', x, 0, z, yaw, (56, 176, 64), name)


# ------------------------------------------------------------------------------------------------ the old starting room
def room2closetsolderones():
    R = R_('room2closetsolderones', amb=30)
    B = shell(R, 'start', -420, 420, CONC)
    # the gear table in the middle of the room
    sbox(R, -200, 0, -360, 60, 80, -120, METAL, 'gear table')
    item(R, 'gasmask', -140, 80, -300)
    item(R, 'bat', -40, 80, -200)
    item(R, 'docb47_orient', 10, 80, -300)
    model30(R, 'scpcb_book.x', -150, 80, -160, 20, (28, 6, 20), 'red book')
    # the cabinets and the chairs along the east wall
    for k, z in enumerate((-700, -620, -540)):
        cab(R, 380, z, 270, 'cabinet %d' % k)
    for k, z in enumerate((200, 300)):
        chair(R, 380, z, 270, 'east chair %d' % k)
    sbox(R, 250, 0, 500, 420, 80, 760, METAL, 'side bench')
    model30(R, 'dclass_sink.x', 395, 80, 640, 270, (40, 30, 50), 'sink')
    # the blinding white doorway in the west wall (ref.: the white door at the end of the old room)
    R.box(-420, 0, 260, -414, 300, 400, GLOW, lux=10)
    named(R, 'GLOW', -400, 150, 330)
    R.light(-360, 150, 330, rng=420, color=(255, 255, 255), power=180)
    for k, z in enumerate((-260, 140)):
        R.box(-420, 120, z, -414, 220, z + 70, VENT, lux=10)
    for z in (-600, 0, 600):
        model30(R, 'scpcb_pendant.x', 0, H, z, 0, (72, 1, 72), 'pendant %d' % z)
        R.light(0, H - 110, z, rng=560, color=(255, 240, 220), power=80)
    B.clear = [((-110, 0, -1000, 110, 200, -380), 'S walk'), ((-110, 0, -100, 110, 200, 1000), 'N walk')]
    check_b42(R)
    return (R, 'OSR', '[Indev Zone] The old starting room: the gear laid out on a steel table - gas mask, battery, an orientation sheet - old cabinets, white chairs, and a white doorway you cannot look into.',
            4, 0.3, ((0, 165, -900), (-200, 120, -240)))


# ------------------------------------------------------------------------------------------------ conference
def room2oldconference():
    R = R_('room2oldconference', amb=30)
    B = shell(R, 'conf', -500, 500, CONC)
    table30(R, -100, -360, 100, 360, 'long table')
    for k, z in enumerate((-260, -80, 100, 280)):
        chair(R, -150, z, 90, 'west chair %d' % k)
    for k, z in enumerate((-260, 100)):
        chair(R, 150, z, 270, 'east chair %d' % k)
    # the knocked-over chair
    R.model('scpcb_chair.x', 180, 20, 260, rot=(90, 200, 0), scale=(1, 1, 1))
    solid(R, (120, 0, 200, 260, 50, 330), 'fallen chair')
    model30(R, 'scpcb_book.x', -40, 78, -200, 15, (28, 6, 20), 'red book')
    item(R, 'docb47_meeting', 30, 78, 120)
    # the whiteboard and a sheet pinned to it
    decal30(R, BOARD, 500, 0, 'W', 420, 200, 200, 'whiteboard')
    named(R, 'BOARD', 490, 200, 0)
    # the vent box in the ceiling
    R.box(-80, H - 50, -560, 80, H, -440, Mat('white.jpg', 32), lux=10)
    R.box(-60, H - 52, -540, 60, H - 50, -460, VENT, lux=10)
    for z in (-500, 0, 500):
        R.light(0, H - 60, z, rng=520, color=(250, 245, 235), power=72)
    cab(R, -460, 700, 90, 'cabinet')
    B.clear = [((-110, 0, -1000, 110, 200, -380), 'S walk'), ((-110, 0, 380, 110, 200, 1000), 'N walk')]
    check_b42(R)
    return (R, 'OCF', '[Indev Zone] The early conference room: one long table, white chairs - one of them knocked over - the whiteboard, a red book, the vent box in the ceiling.',
            4, 0.45, ((0, 165, -900), (0, 100, 0)))


# ------------------------------------------------------------------------------------------------ medical bay
def room2oldmedibay():
    R = R_('room2oldmedibay', amb=30)
    B = shell(R, 'med', -560, 560, WHITEW)
    for k, z in enumerate((-640, -280, 80, 440)):
        model30(R, 'dclass_bed.x', -490, 0, z, 0, (100, 80, 228), 'bed %d' % k)
    # the treatment table and its lamp
    sbox(R, 220, 0, -120, 340, 90, 120, Mat('op-table-light-blood.jpg', 128), 'treatment table')
    R.light(280, 300, 0, rng=420, color=(255, 255, 250), power=120)
    model30(R, 'lamp2.x', 280, 90, 100, 0, (20, 40, 20), 'table lamp')
    for k, z in enumerate((-700, -620, -540, -460)):
        cab(R, 520, z, 270, 'med cabinet %d' % k)
    sbox(R, 440, 0, 400, 560, 90, 700, WHITE, 'counter')
    model30(R, 'dclass_sink.x', 540, 90, 550, 270, (40, 30, 50), 'med sink')
    item(R, 'firstaid', 480, 90, 460)
    item(R, 'eyedrops', 500, 90, 640, chance=60)
    item(R, 'docb47_medical', 260, 90, -60)
    R.rect_floor(-300, -200, -200, -60, 0.8, BLOOD)
    for z in (-560, 0, 560):
        R.light(0, H - 60, z, rng=600, color=(240, 248, 255), power=88)
    B.clear = [((-110, 0, -1000, 110, 200, 1000), 'walk')]
    check_b42(R)
    return (R, 'OMB', '[Indev Zone] The first medical bay: whitewashed walls, a row of beds, the treatment table under its lamp, cabinets and a sink.',
            4, 0.6, ((0, 165, -900), (280, 100, 0)))


# ------------------------------------------------------------------------------------------------ the early core chambers
def room2oldcores():
    R = R_('room2oldcores', amb=30)
    B = shell(R, 'cores', -300, 1000, CONC, luxel=22.0)
    # the bays: dividing walls running east from the corridor, a low front wall with a gap for each bay
    for z in (-340, 340):
        sbox(R, 324, 0, z - 12, 1000, H, z + 12, CONC, 'bay wall %d' % z)
    for (z0, z1) in ((-990, -760), (-540, -340), (-340, -120), (120, 340), (340, 540), (760, 990)):
        sbox(R, 300, 0, z0, 324, H, z1, CONC, 'bay front %d' % z0)
    for zc in (-650, 0, 650):
        R.box(300, 320, zc - 110, 324, H, zc + 110, CONC, lux=10)
    # bay 1: the bell on its pedestal
    sbox(R, 620, 0, -720, 720, 110, -620, Mat('dirtymetal.jpg', 64), 'bell pedestal')
    item(R, 'scp513', 670, 110, -670)
    R.light(670, 330, -670, rng=360, color=(255, 236, 200), power=80)
    # bay 2: the refining machine - two booths and the panel between them
    sbox(R, 560, 0, -280, 760, 300, -120, Mat('dirtymetal.jpg', 128), 'input booth')
    sbox(R, 560, 0, 120, 760, 300, 280, Mat('dirtymetal.jpg', 128), 'output booth')
    sbox(R, 820, 0, -110, 1000, 260, 110, METAL, 'machine panel')
    R.box(814, 130, -40, 820, 210, 40, Mat('indev_b33shade.png', 32), lux=10)      # the dial plate
    named(R, 'DIAL', 812, 170, 0)
    R.light(600, 330, 0, rng=420, color=(240, 240, 255), power=68)
    # bay 3: the old man's chamber - a corroded floor, the walls eaten through at the bottom
    R.rect_floor(360, 360, 1000, 980, 0.6, DARK)
    R.rect_floor(500, 500, 900, 900, 0.9, BLOOD)
    named(R, 'PIT', 700, 0, 650)
    R.light(650, 330, 650, rng=380, color=(255, 120, 90), power=44)
    item(R, 'docb47_cores', -250, 90, -300)
    sbox(R, -300, 0, -380, -200, 90, -220, METAL, 'note desk')
    for z in (-700, 0, 700):
        R.light(0, H - 60, z, rng=520, color=(255, 240, 220), power=68)
    B.clear = [((-110, 0, -1000, 110, 200, 1000), 'corridor'), ((110, 0, -100, 300, 200, 100), 'to bay 2')]
    check_b42(R)
    return (R, 'OCO', '[Indev Zone] The early core chambers: three bays off one corridor - the bell on its pedestal, the refining machine with its two booths, and the old man\'s corroded chamber.',
            4, 0.75, ((0, 165, -900), (700, 150, 0)))


ALL = [room2closetsolderones, room2oldconference, room2oldmedibay, room2oldcores]
