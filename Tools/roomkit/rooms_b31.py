"""The thirty-first batch: SCP-467 (the confessional phone booth) and five anomalous items - SCP-178, SCP-198,
SCP-207, SCP-1079, SCP-1650. Code in IndevU31.bb; models from make_hd31.py, textures from make_assets31.py, notes from
make_docs31.py. SCP texts summarised from scp-wiki.wikidot.com (CC BY-SA 3.0); rooms and art our own. Style after the
user's reference images 77-79 (EZ offices: peach-striped walls, name plates by dark doors, drop ceilings, pendant
lamps, desks with monitors and office chairs, bookshelves) and the earlier white LCZ references.

Both rooms are built with the Site-42 bookkeeping (rooms_b30): every solid, model and picture is recorded and checked -
no overlaps, nothing in a wall or a doorway, no picture over a door button, a clear walk down every corridor.

  room2b31booth  EZ   the SCP-467 chamber (the booth, the guard post with confiscated devices, the recorder),
                      Dr. Rights' office, the research open office, the secretarial/security staff break room
  room2b31items  LCZ  the anomalous item wing: SCP-198's secure room (its case on a digital scale), SCP-207's
                      bio-containment locker room, SCP-178's Class 3 container room, the SCP-1079 locker and the
                      SCP-1650 artifact unit"""
from rooms_b30 import *

PL31 = Mat('indev_plates31.png', cast=False)
NODEV = Mat('indev_467nodev.png', cast=False)
ROSTER = Mat('indev_467roster.png', cast=False)
LOG467 = Mat('indev_467log.png', cast=False)
SCALE = Mat('indev_198scale.png', cast=False)
PROTO = Mat('indev_198proto.png', cast=False)
LOCK207 = Mat('indev_207lock.png', cast=False)
CLEAR = Mat('indev_207clear.png', cast=False)
LOCK178 = Mat('indev_178lock.png', cast=False)
WARN178 = Mat('indev_178warn.png', cast=False)
TAG1650 = Mat('indev_1650tag.png', cast=False)
WATCH = Mat('indev_1079watch.png', cast=False)
PLATES31 = ['scp467', 'rights', 'research', 'break', 'scp198', 'scp207', 'scp178', 'scp1079', 'iceberg', 'itemwing']


def nplate31(R, key, cx, cz, facing, yc=352, w=150):
    i = PLATES31.index(key)
    u0, v0 = (i % 2) * 0.5, (i // 2) * 128 / 640.0
    decal30(R, PL31, cx, cz, facing, w, w * 0.25, yc, 'plate ' + key, uv=(u0, v0, u0 + 0.5, v0 + 128 / 640.0))


def door_plates(R, rows):
    for (side, c, key) in rows:
        s = 1 if side == 'E' else -1
        nplate31(R, key, 192 * s, c, 'W' if s > 0 else 'E')


def pedestal(R, x, z, name, h=100, w=70, top=None):
    sbox(R, x - w / 2, 0, z - w / 2, x + w / 2, h, z + w / 2, PANELS, name, skip='B', top=top or CHECKER)
    return h


# ================================================================================================ SCP-467
def room2b31booth():
    R, rooms = wing('room2b31booth', 'ez', {('E', -400): {}, ('E', 400): {}, ('W', -400): {}, ('W', 400): {}}, amb=11)
    hub_dress(R, 'ez', [])
    door_plates(R, [('E', -400, 'scp467'), ('E', 400, 'rights'), ('W', -400, 'research'), ('W', 400, 'break')])
    for z in (-560, -180, 180, 560):
        pendant(R, 0, z, 384, power=55, rng=600)
    for z in (-370, 370):
        ceil_vent(R, 0, z, 384, size=80, drop=30)
    decal30(R, NODEV, 192, -120, 'W', 160, 80, 230, 'no devices sign')
    decal30(R, PAINT, -192, 0, 'E', 90, 90, 200, 'hub painting')
    # the SCP-467 chamber: the booth in the middle (door facing south), the guard post by the door, the recorder
    named(R, 'BOOTH', 560, 20, -420)
    bx0, bx1, bz0, bz1 = 485, 635, -495, -345
    for (a, b) in (((bx0, bz0), (bx0, bz1)), ((bx0, bz1), (bx1, bz1)), ((bx1, bz1), (bx1, bz0))):   # walls, not the door side
        R.collide_wall(a, b, 0, 330)
        R.collide_wall(b, a, 0, 330)
    for (a, b) in (((bx0, bz0), (bx0 + 30, bz0)), ((bx1 - 30, bz0), (bx1, bz0))):                    # the folded door leaves
        R.collide_wall(a, b, 0, 330)
        R.collide_wall(b, a, 0, 330)
    solid(R, (bx0 - 6, 0, bz0 - 50, bx1 + 6, 330, bz1 + 6), 'SCP-467 booth')
    office_desk(R, 380, -650, 520, -570, 'N', 'guard post', chair=(450, -535))
    sbox(R, 680, 0, -690, 776, 90, -600, DARK, 'device tray cabinet', top=METAL)
    item(R, 'radio', 720, 90, -650)                                                     # a confiscated radio
    item(R, 'doc467', 410, 76, -610)
    console30(R, 730, -200, 'W', 'recorder console')
    decal30(R, ROSTER, 516, -700, 'N', 150, 100, 220, 'guard roster')
    decal30(R, NODEV, 776, -420, 'W', 160, 80, 260, 'chamber no devices')
    decal30(R, LOG467, 516, -100, 'S', 210, 158, 220, 'test log board')
    named(R, 'LOG', 516, 220, -110)
    named(R, 'RECORDER', 700, 150, -200)
    ceil_light(R, 560, -420, 352, size=44, power=55, rng=600, color=(255, 236, 200))
    ceil_light(R, 360, -200, 352, size=36, power=40, rng=500)
    # Dr. Rights' office (ref. 78): a big desk with a lamp, a bookcase, cabinets
    office_desk(R, 520, 300, 700, 420, 'S', 'rights desk', chair=(610, 455))
    shelf_unit(R, 716, 520, 776, 690, 'rights bookcase')
    cabinets(R, 300, 640, 460, 690, 'rights cabinets')
    decal30(R, WB, 776, 330, 'W', 200, 100, 200, 'rights whiteboard')
    decal30(R, PAINT, 516, 100, 'N', 90, 90, 210, 'rights painting')
    named(R, 'RIGHTS', 610, 110, 360)
    item(R, 'doc467log', 560, 76, 330)
    pendant(R, 610, 360, 352, drop=60, power=65, rng=520)
    # the research open office (ref. 77): six desks in two rows, a whiteboard, a window of monitors
    for (x0, z0) in ((-700, -640), (-700, -480), (-540, -640), (-540, -480)):
        office_desk(R, x0, z0, x0 + 120, z0 + 80, 'S', 'research desk %d %d' % (x0, z0), chair=(x0 + 60, z0 + 115), lamp=False)
    decal30(R, WMON, -600, -700, 'N', 260, 100, 230, 'research monitor wall')
    decal30(R, WB, -776, -250, 'E', 200, 100, 200, 'research whiteboard')
    named(R, 'ICEBERG', -640, 110, -600)
    for z in (-560, -260):
        ceil_light(R, -516, z, 352, size=44, power=55, rng=600)
    # the secretarial / security staff break room: a table, chairs, a sofa, lockers, a vending machine
    table30(R, -620, 330, -460, 470, 'break table')
    for (x, z, f) in ((-660, 400, 'E'), (-420, 400, 'W')):
        model30(R, 'scpcb_chair.x', x, 0, z, {'E': 270, 'W': 90}[f], (40, 104, 40), 'break chair %d' % x)
    sbox(R, -776, 0, 560, -700, 50, 690, Mat('indev_3008fabric.png', 128), 'sofa seat')
    sbox(R, -776, 50, 560, -760, 110, 690, Mat('indev_3008fabric.png', 128), 'sofa back')
    lockers(R, 'z', 700, -1, -560, -300)
    solid(R, (-560, 0, 670, -300, 300, 700), 'break lockers')
    vending(R, -776, 175, 'E')
    solid(R, (-776, 0, 135, -732, 176, 215), 'vending machine')
    decal30(R, CLEAR, -776, 300, 'E', 120, 60, 230, 'clear drinks notice')
    named(R, 'BREAK', -540, 100, 400)
    ceil_light(R, -516, 400, 352, size=44, power=55, rng=600)
    check(R)
    return (R, 'BTH', 'SCP-467 wing (Entrance Zone): the confessional phone booth with its guard post, Dr. Rights\' office, the research open office and the staff break room.',
            3, 0.5, ((0, 165, -650), (0, 150, 300)))


# ================================================================================================ the item wing
def room2b31items():
    R, rooms = wing('room2b31items', 'lcz', {('E', -400): {'key': 3}, ('E', 400): {}, ('W', -400): {'key': 3}, ('W', 400): {}}, amb=10)
    hub_dress(R, 'lcz', [])
    door_plates(R, [('E', -400, 'scp198'), ('E', 400, 'scp207'), ('W', -400, 'scp178'), ('W', 400, 'scp1079')])
    for z in (-560, 0, 560):
        ceil_light(R, 0, z, 384, size=40, power=55, rng=700)
    decal30(R, POSTER24, 192, 0, 'W', 80, 110, 200, 'hub poster')
    decal30(R, BANNER, -192, 0, 'E', 240, 84, 240, 'hub banner')
    # SCP-198: the sealed case on a digital scale under a camera; the protocol card; the alarm lamp
    sbox(R, 480, 0, -460, 600, 70, -340, METAL, 'digital scale', top=CHECKER)
    sbox(R, 495, 70, -445, 585, 160, -355, Mat('glass.png', 128, alpha=True, cast=False), 'SCP-198 case')
    named(R, 'CASE198', 540, 100, -400)
    decal30(R, SCALE, 776, -400, 'W', 140, 88, 180, 'scale display')
    decal30(R, PROTO, 516, -700, 'N', 150, 150, 200, 'protocol 198 card')
    red_lamp(R, 700, -180, 352, power=40, rng=420)
    named(R, 'SCALE', 770, 180, -400)
    for (x, z) in ((330, -620), (330, -180)):
        model30(R, 'scpcb_chair.x', x, 0, z, 90, (40, 104, 40), 'guard chair %d' % z)
    ceil_light(R, 540, -400, 352, size=44, power=55, rng=600)
    # SCP-207: the waterproof locker, the crate, a decontamination sink, the test table
    sbox(R, 680, 0, 520, 776, 200, 690, Mat('yellowmetal.jpg', 256), 'SCP-207 locker')
    decal30(R, LOCK207, 776, 400, 'W', 150, 75, 230, 'locker 207 label')
    named(R, 'CRATE207', 560, 0, 600)
    solid(R, (440, 0, 520, 680, 60, 680), 'SCP-207 crate')
    table30(R, 400, 250, 560, 360, 'SCP-207 test table')
    item(R, 'scp207', 470, 78, 300)
    item(R, 'doc207', 520, 78, 330)
    model30(R, 'dclass_sink.x', 720, 60, 130, 0, (50, 30, 40), 'decon sink')
    ceil_light(R, 516, 400, 352, size=44, power=55, rng=600)
    # SCP-178: the Class 3 container, remote monitoring, the incident warning
    sbox(R, -620, 0, -520, -460, 110, -380, Mat('metal_darker.jpg', 128), 'SCP-178 container', top=PANELS)
    item(R, 'scp178', -540, 110, -450)
    decal30(R, LOCK178, -776, -450, 'E', 150, 75, 230, 'locker 178 label')
    decal30(R, WARN178, -516, -700, 'N', 150, 100, 220, 'incident 178 warning')
    named(R, 'WARN', -516, 220, -690)
    console30(R, -730, -200, 'E', 'remote monitor console')
    item(R, 'doc178', -680, 0, -620)
    ceil_light(R, -540, -400, 352, size=44, power=55, rng=600)
    # SCP-1079 and SCP-1650: the watchlist locker shelves, the artifact unit pedestal with its seizure tag
    shelf_unit(R, -776, 520, -716, 690, 'SCP-1079 locker shelves')
    item(R, 'scp1079', -746, 100, 600)
    item(R, 'doc1079', -600, 76, 300)
    decal30(R, WATCH, -776, 400, 'E', 150, 75, 230, 'watchlist notice')
    pedestal(R, -500, 560, 'SCP-1650 artifact unit')
    item(R, 'scp1650', -500, 100, 560)
    decal30(R, TAG1650, -500, 700, 'S', 120, 75, 160, 'seizure tag')
    table30(R, -660, 250, -520, 350, 'item wing table')
    item(R, 'doc1650', -580, 78, 280)
    ceil_light(R, -516, 400, 352, size=44, power=55, rng=600)
    check(R)
    return (R, 'ITM', 'Anomalous item wing (Light Containment): SCP-198 on its digital scale, the SCP-207 locker and crate, SCP-178\'s Class 3 container, the SCP-1079 locker and the SCP-1650 artifact unit.',
            1, 0.5, ((0, 165, -650), (0, 150, 300)))


ALL = [room2b31booth, room2b31items]
