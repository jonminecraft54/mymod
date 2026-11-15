r"""Eight SCP:CB rooms for CBRE-EX, from the reference images 51 to 59. Run:  python rooms_cbre.py [--nopreview]
Writes Tools\cbre\out\<room>.vmf (open them in CBRE-EX) and <room>_preview.jpg (a baked render of the same brushes).

Layout rules every room follows (SCP:CB room units, 2048 x 2048 per room cell, floor at y 0):
  * room2 rooms have their doorways at z = -1024 and z = +1024 (centred on x 0); the room4 junction also at x = +-1024.
    A doorway is a 192 x 320 hole in a 16 thick end wall that stops at the room edge. Doors are NOT brushes: the game
    places them in code (rooms.ini / FillRoom), so the hole is left open.
  * floor slabs 16 thick under y 0, ceiling slabs 16 thick over the ceiling height; walls 16 thick.
  * every face is a real texture of GFX\map (CBRE material = file name without extension) or a CBRE tool texture.
  * lights are CBRE 'light' / 'spotlight' entities under brush light fixtures; 'waypoint' entities along every walkable
    route (the NPC path network); props are 'model' entities naming files of GFX\map\Props."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cbre_vmf import Room

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')
DOOR_W, DOOR_H = 192, 320
T = 16
RF = 'tooltextures/remove_face'
HIDE = 'tooltextures/invisible_collision'


def door(c=0):
    return (c - DOOR_W / 2, c + DOOR_W / 2, 0, DOOR_H)


# ------------------------------------------------------------------------------------------------ building blocks
def shell(R, x0, x1, z0, z1, h, wall, floor, ceil, holes=None, skip=''):
    """a closed hall: floor slab, ceiling slab, four walls outside the interior x0..x1, z0..z1 (holes per side
    'x0' 'x1' 'z0' 'z1': lists of (c0, c1, h0, h1)). skip: sides left out (shared with another hall)"""
    holes = holes or {}
    R.box(x0 - T, -T, z0 - T, x1 + T, 0, z1 + T, wall, top=floor)
    R.box(x0 - T, h, z0 - T, x1 + T, h + T, z1 + T, wall, bottom=ceil)
    if 'x0' not in skip:
        R.wall_x(x0, z0, z1, 0, h, T, wall, holes.get('x0', ()), inner='+')
    if 'x1' not in skip:
        R.wall_x(x1, z0, z1, 0, h, T, wall, holes.get('x1', ()), inner='-')
    if 'z0' not in skip:
        R.wall_z(z0, x0 - T, x1 + T, 0, h, T, wall, holes.get('z0', ()), inner='+')
    if 'z1' not in skip:
        R.wall_z(z1, x0 - T, x1 + T, 0, h, T, wall, holes.get('z1', ()), inner='-')


def trims(R, x0, x1, z0, z1, holes=None, base='metal', band='scpcb_rivetband', band_y=None, sides='x0 x1 z0 z1'):
    """a baseboard (20 high, 4 proud) round the hall, broken at the doorways, and a riveted band at band_y"""
    holes = holes or {}
    for s in sides.split():
        hl = holes.get(s, ())
        for (y0, y1, m, d) in ((0, 20, base, 4),) + (((band_y, band_y + 24, band, 3),) if band_y else ()):
            if s == 'x0':
                R.wall_x(x0 + d, z0, z1, y0, y1, d, m, hl, inner='+')
            elif s == 'x1':
                R.wall_x(x1 - d, z0, z1, y0, y1, d, m, hl, inner='-')
            elif s == 'z0':
                R.wall_z(z0 + d, x0, x1, y0, y1, d, m, hl, inner='+')
            else:
                R.wall_z(z1 - d, x0, x1, y0, y1, d, m, hl, inner='-')


def fixture(R, x, z, h, w=112, l=36, along='x', color=(255, 248, 235), rng=720, intensity=1.0):
    """a ceiling light: steel housing, a diffuser panel underneath and a CBRE light just below it"""
    hw, hl = (w / 2, l / 2) if along == 'x' else (l / 2, w / 2)
    R.box(x - hw, h - 10, z - hl, x + hw, h, z + hl, 'metal', bottom='scpcb_lightpanel')
    R.box(x - hw - 4, h - 4, z - hl - 4, x + hw + 4, h, z + hl + 4, 'dirtymetal')
    R.light(x, h - 30, z, color=color, rng=rng, intensity=intensity)


def pilaster(R, x, z, h, face, w=48, d=16, mat='concretewall', cap='metal'):
    """a pilaster on a wall (face: the way it sticks out: +x -x +z -z), with a plinth and a cap block"""
    sx, sz = {'+x': (1, 0), '-x': (-1, 0), '+z': (0, 1), '-z': (0, -1)}[face]
    def blk(y0, y1, dd, ww):
        if sx:
            R.box(x, y0, z - ww / 2, x + sx * dd, y1, z + ww / 2, mat if cap is None else mat)
        else:
            R.box(x - ww / 2, y0, z, x + ww / 2, y1, z + sz * dd, mat)
    blk(0, h, d, w)
    if sx:
        R.box(x, 0, z - w / 2 - 6, x + sx * (d + 6), 28, z + w / 2 + 6, cap)
        R.box(x, h - 28, z - w / 2 - 6, x + sx * (d + 6), h, z + w / 2 + 6, cap)
    else:
        R.box(x - w / 2 - 6, 0, z, x + w / 2 + 6, 28, z + sz * (d + 6), cap)
        R.box(x - w / 2 - 6, h - 28, z, x + w / 2 + 6, h, z + sz * (d + 6), cap)


def beam_x(R, x0, x1, z, h, w=32, d=40, mat='metal'):
    R.box(x0, h - d, z - w / 2, x1, h, z + w / 2, mat)


def beam_z(R, z0, z1, x, h, w=32, d=40, mat='metal'):
    R.box(x - w / 2, h - d, z0, x + w / 2, h, z1, mat)


def pipe_z(R, x, y, z0, z1, r=10, mat='Pipes', clamps=256):
    """a pipe along z at (x, y), with clamp collars every `clamps` units"""
    R.prism(x, y, r, z0, z1, mat, n=8, along='z')
    z = z0 + clamps / 2
    while z < z1:
        R.box(x - r - 3, y - r - 3, z - 6, x + r + 3, y + r + 3, z + 6, 'dirtymetal')
        z += clamps


def pipe_x(R, z, y, x0, x1, r=10, mat='Pipes', clamps=256):
    R.prism(y, z, r, x0, x1, mat, n=8, along='x')
    x = x0 + clamps / 2
    while x < x1:
        R.box(x - 6, y - r - 3, z - r - 3, x + 6, y + r + 3, z + r + 3, 'dirtymetal')
        x += clamps


def cable_tray_z(R, x, y, z0, z1, w=64):
    """a cable tray: a perforated steel channel with a bundle of black cables in it"""
    R.box(x - w / 2, y - 4, z0, x + w / 2, y, z1, 'grating')
    R.box(x - w / 2, y - 4, z0, x - w / 2 + 3, y + 14, z1, 'metal')
    R.box(x + w / 2 - 3, y - 4, z0, x + w / 2, y + 14, z1, 'metal')
    for k, cx in enumerate((-16, -4, 9, 20)):
        R.prism(x + cx, y + 5 + (k % 2) * 3, 5, z0, z1, 'cable_black', n=6, along='z')


def vent_x(R, x, z, y, face, w=96, h=48):
    """a vent grille in a wall at x, with a steel frame"""
    R.decal(x, z, face, w, h, y, 'vent', depth=2)
    R.decal(x, z, face, w + 12, h + 12, y, 'metal', depth=1)


def railing_z(R, x, z0, z1, y, mat='yellowmetal'):
    """a handrail along z at the edge x: posts every 128, a top rail and a mid rail, and a kick plate"""
    z = z0
    while z <= z1 + 0.5:
        R.box(x - 3, y, z - 3, x + 3, y + 104, z + 3, mat)
        z += 128
    R.prism(x, y + 106, 4, z0 - 3, z1 + 3, mat, n=6, along='z')
    R.prism(x, y + 56, 3, z0, z1, mat, n=6, along='z')
    R.box(x - 2, y, z0, x + 2, y + 14, z1, 'metal')


def railing_x(R, z, x0, x1, y, mat='yellowmetal'):
    x = x0
    while x <= x1 + 0.5:
        R.box(x - 3, y, z - 3, x + 3, y + 104, z + 3, mat)
        x += 128
    R.prism(y + 106, z, 4, x0 - 3, x1 + 3, mat, n=6, along='x')
    R.prism(y + 56, z, 3, x0, x1, mat, n=6, along='x')
    R.box(x0, y, z - 2, x1, y + 14, z + 2, 'metal')


def shelving(R, x0, z0, x1, z1, h=256, levels=4, props=()):
    """a steel shelving unit: four uprights, `levels` shelf decks, cross bracing at the back"""
    for x in (x0, x1 - 6):
        for z in (z0, z1 - 6):
            R.box(x, 0, z, x + 6, h, z + 6, 'metal')
    for k in range(levels):
        y = 12 + k * (h - 24) / (levels - 1)
        R.box(x0, y, z0, x1, y + 4, z1, 'metalpanels')
        R.box(x0, y + 4, z0, x1, y + 10, z0 + 2, 'yellowmetal')        # the shelf's front lip
    for (file, fx, fy, fz, yaw, sc) in props:
        R.model(file, fx, fy, fz, yaw, sc)


def desk(R, x0, z0, x1, z1, top=78):
    """a desk: wooden top, a steel modesty panel, two drawer pedestals"""
    R.box(x0, top - 4, z0, x1, top, z1, 'wood')
    R.box(x0 + 4, 8, z1 - 6, x1 - 4, top - 4, z1 - 2, 'metal')
    R.box(x0, 0, z0 + 2, x0 + 40, top - 4, z1 - 2, 'scpcb_cabinet')
    R.box(x1 - 40, 0, z0 + 2, x1, top - 4, z1 - 2, 'scpcb_cabinet')


def bench(R, x0, z0, x1, z1, y=44):
    R.box(x0, y - 6, z0, x1, y, z1, 'wood')
    for x in (x0 + 8, x1 - 16):
        R.box(x, 0, z0 + 4, x + 8, y - 6, z1 - 4, 'metal')


def camera(R, x, z, y, face):
    """a wall-mounted security camera made of brushes: back plate, arm, body and lens hood (decorative; the
    working cameras of the game are spawned in code)"""
    sx = {'+x': 1, '-x': -1}.get(face, 0)
    sz = {'+z': 1, '-z': -1}.get(face, 0)
    if sx:
        R.box(x, y - 16, z - 12, x + sx * 4, y + 16, z + 12, 'metal')
        R.box(x + sx * 4, y - 3, z - 3, x + sx * 24, y + 3, z + 3, 'dirtymetal')
        R.box(x + sx * 20, y - 22, z - 10, x + sx * 60, y - 4, z + 10, 'white')
        R.box(x + sx * 60, y - 20, z - 8, x + sx * 66, y - 6, z + 8, 'metal_darker')
    else:
        R.box(x - 12, y - 16, z, x + 12, y + 16, z + sz * 4, 'metal')
        R.box(x - 3, y - 3, z + sz * 4, x + 3, y + 3, z + sz * 24, 'dirtymetal')
        R.box(x - 10, y - 22, z + sz * 20, x + 10, y - 4, z + sz * 60, 'white')
        R.box(x - 8, y - 20, z + sz * 60, x + 8, y - 6, z + sz * 66, 'metal_darker')


def waypoints_z(R, x, z0, z1, step=256):
    z = z0
    while z <= z1 + 0.5:
        R.waypoint(x, z)
        z += step


# ------------------------------------------------------------------------------------------------ the rooms
def storage():
    """image 51: an LCZ storage room - white walls, a black ceiling, a dark floor, steel shelving down both walls,
    benches in the middle, the Foundation banner and a red poster, a camera over the door"""
    R = Room('room2cbre_storage', 'LCZ storage hall (ref. 51)')
    x0, x1, z0, z1, h = -448, 448, -1008, 1008, 384
    holes = {'z0': [door()], 'z1': [door()]}
    shell(R, x0, x1, z0, z1, h, 'whitewall', 'concretefloor', 'metal_darker', holes)
    trims(R, x0, x1, z0, z1, holes, base='metal_darker', band='scpcb_rivetband', band_y=150)
    # the ceiling: a grid of steel beams and a black service void above them
    for z in range(-768, 769, 256):
        beam_x(R, x0, x1, z, h, w=24, d=32, mat='metal_darker')
    beam_z(R, z0, z1, 0, h, w=24, d=32, mat='metal_darker')
    for z in (-640, -128, 384, 896):
        fixture(R, -224, z, h - 32, along='z')
        fixture(R, 224, z, h - 32, along='z')
    # shelving bays down both long walls, between pilasters
    for zc in (-720, -400, 400, 720):
        for (sx0, sx1) in ((x0 + 4, x0 + 100), (x1 - 100, x1 - 4)):
            shelving(R, sx0, zc - 128, sx1, zc + 128, props=(
                ('crate1.x', (sx0 + sx1) / 2, 16, zc - 60, 0, 0.9), ('boxfile_a.x', (sx0 + sx1) / 2, 98, zc + 40, 90, 1.0),
                ('crate2.x', (sx0 + sx1) / 2, 180, zc, 0, 0.8)))
    for zc in (-880, -560, -240, 240, 560, 880):
        pilaster(R, x0, zc, h, '+x', mat='whitewall', cap='metal_darker')
        pilaster(R, x1, zc, h, '-x', mat='whitewall', cap='metal_darker')
    # the middle: the banner wall section, benches and the poster
    R.decal(x0 + 2, 0, 'E', 360, 128, 250, 'indev_b24banner')
    R.decal(x1 - 2, 0, 'W', 96, 136, 200, 'indev_b24poster')
    R.decal(x1 - 2, -160, 'W', 128, 128, 210, 'Logo_of_the_SCP_Foundation')
    bench(R, -150, -200, -90, 200)
    bench(R, 90, -200, 150, 200)
    R.model('scpcb_bench.x', 0, 0, -620, 90, 1.0)
    R.model('scpcb_bench.x', 0, 0, 620, 90, 1.0)
    # the camera over the south door, a sign and vents
    camera(R, 160, z0, 330, '+z')
    R.decal(0, z0 + 1, 'N', 160, 48, 360, 'scpcb_lczsign')
    R.decal(0, z1 - 1, 'S', 160, 48, 360, 'scpcb_lczsign')
    vent_x(R, x0, -160, 300, 'E')
    vent_x(R, x1, 160, 300, 'W')
    R.sound(0, 300, 0, 1, rng=8)
    waypoints_z(R, 0, -1000, 1000)
    for z in (-560, 560):
        R.waypoint(-250, z); R.waypoint(250, z)
    return R, [((0, 170, -960), (0, 120, 300)), ((-360, 200, 520), (300, 80, -300))]


def office():
    """image 52: a researcher's office - plaster walls with wooden wainscot, carpet, a suspended ceiling of light
    panels, two desks with terminals, filing cabinets, a whiteboard and a wall monitor; a glazed partition to the
    corridor"""
    R = Room('room2cbre_office', 'Researcher office (ref. 52)')
    h = 352
    # the corridor (x -192..192) and the office beside it (x 192..832)
    holes = {'z0': [door()], 'z1': [door()]}
    shell(R, -192, 832, -1008, 1008, h, 'officewall', 'tilefloor', 'ceiling', holes)
    R.box(192, 0, -480, 832, 1, 480, 'indev_carpet')                     # the office carpet, a hair proud
    # the partition: wall below, glazing above, a door gap at z 0
    for (a, b) in ((-480, -80), (80, 480)):
        R.box(192, 0, a, 208, 110, b, 'wood')
        R.box(192, 110, a, 208, 118, b, 'metal')
        R.box(198, 118, a, 202, 280, b, 'glass')
        R.box(192, 280, a, 208, h, b, 'officewall')
        for z in range(a, b + 1, 100):
            R.box(194, 118, z - 3, 206, 280, z + 3, 'metal')
    R.box(192, 300, -80, 208, h, 80, 'officewall')                      # the lintel over the office door
    R.box(192, 0, -1008, 208, h, -480, 'officewall')
    R.box(192, 0, 480, 208, h, 1008, 'officewall')
    # the office's own walls at z -480 / 480 (it is 960 long), wainscot and trims
    R.box(208, 0, -496, 832, h, -480, 'officewall')
    R.box(208, 0, 480, 832, h, 496, 'officewall')
    trims(R, 208, 832, -480, 480, sides='x1 z0 z1', base='wood')
    R.box(828, 20, -480, 832, 120, 480, 'wood')                          # the wainscot
    R.box(826, 120, -480, 832, 126, 480, 'wood')
    trims(R, -192, 192, -1008, 1008, holes, base='metal', band='scpcb_rivetband', band_y=130, sides='x0 z0 z1')
    # the suspended ceiling: a T-bar grid with light panels in it
    for x in range(256, 832, 128):
        beam_z(R, -480, 480, x, h, w=4, d=4, mat='white')
    for z in range(-448, 480, 128):
        beam_x(R, 208, 832, z, h, w=4, d=4, mat='white')
    for (x, z) in ((384, -256), (640, -256), (384, 256), (640, 256)):
        R.box(x - 60, h - 3, z - 60, x + 60, h, z + 60, 'metal', bottom='scpcb_lightpanel')
        R.light(x, h - 40, z, color=(255, 250, 238), rng=640)
    for z in (-768, -256, 256, 768):
        fixture(R, 0, z, h, along='z')
    # the desks and what is on them
    for (zc, yaw) in ((-220, 0), (220, 180)):
        desk(R, 560, zc - 70, 760, zc + 70)
        R.model('monitor.x', 660, 78, zc, 90, 1.0)
        R.model('keyboard.x', 620, 78, zc, 90, 1.0)
        R.model('officeseat_a.x', 520, 0, zc, 270, 1.0)
        R.model('mug.x', 600, 78, zc + 50, 0, 1.0)
        R.model('lamp1.x', 740, 78, zc - 50, 0, 1.0)
    # filing cabinets, a bookcase, the whiteboard and the monitor
    for z in (-430, -370):
        R.model('scpcb_cabinet.x', 790, 0, z, 270, 1.0)
    shelving(R, 300, 430, 520, 476, h=220, levels=5, props=(('scpcb_book.x', 360, 60, 452, 0, 1.0),
                                                              ('boxfile_a.x', 460, 120, 452, 0, 1.0)))
    R.decal(832 - 1, 0, 'W', 240, 120, 190, 'scpcb_whiteboard')
    R.decal(500, -480 + 1, 'N', 110, 110, 210, 'scpcb_wallmonitor')
    R.decal(330, 480 - 1, 'S', 96, 96, 300, 'scpcb_painting')
    R.decal(-191, -300, 'E', 160, 48, 250, 'scpcb_ezsign')
    vent_x(R, 832, 360, 320, 'W', w=64, h=32)
    R.model('lamp3.x', 300, 0, -420, 0, 1.0)
    pipe_z(R, -150, h - 24, -1008, 1008, r=8)
    pipe_z(R, -120, h - 20, -1008, 1008, r=6, mat='Pipes_NoRust2')
    waypoints_z(R, 0, -1000, 1000)
    for p in ((300, 0), (450, -200), (450, 200)):
        R.waypoint(*p)
    return R, [((0, 170, -900), (60, 120, 0)), ((300, 170, -380), (700, 90, 120))]


def gallery():
    """image 53: an observation gallery - a balcony walkway with a handrail and windows over a chamber 384 below,
    reached by a stair at the north end; columns carry the balcony"""
    R = Room('room2cbre_gallery', 'Observation balcony over a lower chamber (ref. 53)')
    h, pit = 512, -384
    holes = {'z0': [door(-320)], 'z1': [door(-320)]}
    # the upper walkway x -512..-128 at y 0, the chamber x -128..640 down at y -384
    R.box(-528, -T, -1024, -128, 0, 1024, 'metalpanels', top='scpcb_checkerplate')
    R.box(-128, pit - T, -1024, 656, pit, 1024, 'concrete', top='concretefloor')
    R.box(-528, h, -1024, 656, h + T, 1024, 'concrete', bottom='ceiling')
    R.wall_x(-512, -1008, 1008, 0, h, T, 'whitewall', inner='+')
    R.wall_x(640, -1008, 1008, pit, h, T, 'concretewall', inner='-')
    R.wall_z(-1008, -528, -128, 0, h, T, 'whitewall', holes['z0'], inner='+')
    R.wall_z(1008, -528, -128, 0, h, T, 'whitewall', holes['z1'], inner='-')
    R.wall_z(-1008, -128, 656, pit, h, T, 'concretewall', inner='+')
    R.wall_z(1008, -128, 656, pit, h, T, 'concretewall', inner='-')
    R.box(-144, pit, -1008, -128, 0, 1008, 'concretewall')               # the face of the balcony
    trims(R, -512, -128, -1008, 1008, holes, sides='x0 z0 z1', band_y=180)
    # the balcony edge: a railing, and glazed panes between steel mullions up to a transom
    railing_z(R, -136, -1000, 600, 0)
    for z in range(-1000, 1001, 250):
        R.box(-140, 0, z - 4, -128, 330, z + 4, 'metal')
    R.box(-140, 330, -1008, -128, 346, 1008, 'metal')
    R.box(-140, 346, -1008, -128, h, 1008, 'whitewall')
    # columns under the balcony edge and the chamber's equipment
    for z in (-640, 0, 640):
        R.prism(-96, z, 28, pit, 0, 'concrete', n=8)
        R.box(-128, pit, z - 40, -64, pit + 24, z + 40, 'metal')
    for z in (-512, 512):
        R.box(240, pit, z - 96, 432, pit + 160, z + 96, 'dirtymetal', top='metalpanels2')
        R.model('scpcb_console.x', 200, pit, z, 270, 1.0)
    R.box(300, pit, -64, 600, pit + 8, 64, 'hazard_stripe_wall_1789291234341')   # the test pad
    R.decal(640 - 1, 0, 'W', 256, 256, pit + 380, 'Logo_of_the_SCP_Foundation')
    for (x, z) in ((260, -600), (260, 0), (260, 600)):
        R.spot(x, h - 40, z, pitch=90, color=(240, 245, 255), rng=1100, inner=35, outer=70)
        R.box(x - 24, h - 30, z - 24, x + 24, h, z + 24, 'metal', bottom='scpcb_lightpanel')
    for z in (-700, -200, 300, 800):
        fixture(R, -320, z, h - 96, along='z', rng=600)
    beam_z(R, -1008, 1008, -320, h, w=32, d=96, mat='metal')
    # the stair down at the north end: 24 steps of 16 x 32
    for k in range(24):
        ytop = -16 * k
        R.box(-128 + 32 * k, pit, 680, -96 + 32 * k, ytop, 1008, 'metal', top='scpcb_checkerplate')
    railing_x(R, 676, -128, 640, -16 * 12, mat='yellowmetal')
    R.box(-128, 0, 600, -96, 120, 680, 'metal')                            # the newel post at the top
    pipe_z(R, 600, h - 30, -1008, 1008, r=14)
    pipe_z(R, 560, h - 30, -1008, 1008, r=10, mat='Pipes_NoRust2')
    R.decal(-511, 0, 'E', 160, 48, 260, 'scpcb_obssign')
    camera(R, 640, 0, h - 60, '-x')
    R.sound(200, pit + 100, 0, 2, rng=10)
    waypoints_z(R, -320, -1000, 1000)
    for z in (-768, -256, 256):
        R.waypoint(200, z, y=pit + 20)
    R.waypoint(-128, 840, y=20); R.waypoint(500, 840, y=pit + 20)
    return R, [((-420, 170, -900), (100, -150, 200)), ((560, pit + 170, -900), (-200, 60, 300))]


def machine_corridor():
    """images 54 and 59: an HCZ corridor - riveted steel and concrete, pilasters every 256 with lamp heads, a
    grated trench down the middle, and a big observation window onto a machine hall with tanks and pipework"""
    R = Room('room2cbre_hczmachine', 'HCZ pilaster corridor with machine window (ref. 54, 59)')
    h = 448
    holes = {'z0': [door()], 'z1': [door()], 'x1': [(-256, 256, 96, 320)]}
    shell(R, -224, 224, -1008, 1008, h, 'heavy_containment_wall_1789291243567', 'scpcb_checkerplate', 'metal', holes)
    trims(R, -224, 224, -1008, 1008, holes, base='hazard_stripe_wall_1789291234341', band='scpcb_rivetband', band_y=200)
    # the trench
    R.box(-48, -T, -1008, 48, 1, 1008, 'grating')
    for x in (-52, 48):
        R.box(x, 0, -1008, x + 4, 2, 1008, 'yellowmetal')
    # pilasters with lamp heads, and the beams between them
    for z in range(-896, 897, 256):
        if -300 < z < 300:
            pilaster(R, -224, z, h, '+x', w=56, d=24, mat='concretewall', cap='dirtymetal')
            continue
        for (x, f) in ((-224, '+x'), (224, '-x')):
            pilaster(R, x, z, h, f, w=56, d=24, mat='concretewall', cap='dirtymetal')
        beam_x(R, -224, 224, z, h, w=40, d=48, mat='dirtymetal')
    for z in (-768, -512, 512, 768):
        R.box(-200, 330, z - 12, -184, 354, z + 12, 'metal', faces={'x1': 'scpcb_lightpanel'})
        R.box(184, 330, z - 12, 200, 354, z + 12, 'metal', faces={'x0': 'scpcb_lightpanel'})
        R.light(-170, 342, z, color=(255, 236, 205), rng=520, intensity=0.9)
        R.light(170, 342, z, color=(255, 236, 205), rng=520, intensity=0.9)
    # the window: frame, sill, glass and the machine hall behind it
    R.box(224, 80, -272, 248, 96, 272, 'metal')
    R.box(224, 320, -272, 248, 336, 272, 'metal')
    for z in (-272, -8, 256):
        R.box(224, 96, z, 248, 320, z + 16, 'metal')
    R.box(234, 96, -256, 238, 320, 256, 'glass')
    R.box(240, -160 - T, -512, 800, -160, 512, 'dirtymetal', top='concretefloor')
    R.box(240, 560, -512, 800, 576, 512, 'dirtymetal', bottom='metal')
    R.wall_x(800, -512, 512, -160, 560, T, 'concretewall', inner='-')
    R.wall_z(-512, 240, 816, -160, 560, T, 'concretewall', inner='+')
    R.wall_z(512, 240, 816, -160, 560, T, 'concretewall', inner='-')
    R.box(240, -160, -512, 256, 80, 512, 'concretewall')                 # below the window
    R.box(240, 336, -512, 256, 560, 512, 'concretewall')                 # above it
    R.box(240, 80, -512, 256, 336, -272, 'concretewall')
    R.box(240, 80, 272, 256, 336, 512, 'concretewall')
    for z in (-300, 0, 300):
        R.prism(560, z, 90, -160, 260, 'tank1', n=12, cap='metal')
        R.box(470, -160, z - 100, 650, -130, z + 100, 'metal')
        R.prism(560, z, 20, 260, 560, 'Pipes', n=8)
    for y in (380, 440):
        pipe_z(R, 700, y, -512, 512, r=18)
    R.box(300, -160, -480, 360, 40, -380, 'ElecBox')
    R.decal(799, 0, 'W', 192, 96, 300, 'caution_tesla')
    for (x, z) in ((400, -350), (400, 350), (700, 0)):
        R.light(x, 500, z, color=(255, 180, 120), rng=600, intensity=0.8)
    # services in the corridor: a cable tray and two pipe runs
    cable_tray_z(R, -150, h - 60, -1008, 1008)
    pipe_z(R, 160, h - 30, -1008, 1008, r=14)
    pipe_z(R, 120, h - 26, -1008, 1008, r=8, mat='Pipes_NoRust2')
    R.decal(-223, 0, 'E', 128, 128, 220, 'miscsigns4')
    R.decal(0, -1007, 'N', 160, 48, 380, 'scpcb_hazmatsign')
    vent_x(R, -224, 400, 120, 'E')
    R.sound(500, 0, 0, 3, rng=10)
    waypoints_z(R, 0, -1000, 1000)
    return R, [((0, 170, -960), (0, 150, 200)), ((-150, 170, -380), (300, 120, 0))]


def hoist():
    """image 55: a hoist control room - consoles under a long window onto a shaft, a gantry beam with a trolley,
    chains and a load platform hanging over the pit"""
    R = Room('room2cbre_hoist', 'Hoist control room over a shaft (ref. 55)')
    h = 384
    holes = {'z0': [door()], 'z1': [door()]}
    shell(R, -512, 160, -1008, 1008, h, 'whitewall', 'tilefloor', 'ceiling', holes, skip='x1')
    trims(R, -512, 160, -1008, 1008, holes, sides='x0 z0 z1', band_y=150)
    # the window wall at x 160: solid under 110, glass to 300, solid above; a steel console shelf under it
    for (a, b) in ((-1008, -640), (640, 1008)):
        R.box(160, 0, a, 176, h, b, 'whitewall')
    R.box(160, 0, -640, 176, 110, 640, 'metalpanels2')
    R.box(166, 110, -640, 170, 300, 640, 'glass')
    for z in range(-640, 641, 160):
        R.box(160, 110, z - 4, 176, 300, z + 4, 'metal')
    R.box(160, 300, -640, 176, h, 640, 'whitewall')
    R.box(60, 0, -600, 160, 90, 600, 'dirtymetal', top='controlpanel')
    for z in (-420, -140, 140, 420):
        R.model('scpcb_console.x', 100, 0, z, 270, 1.0)
        R.model('officeseat_a.x', 10, 0, z, 90, 1.0)
    R.decal(-511, -300, 'E', 128, 96, 180, 'controlpanel2')
    R.decal(-511, 300, 'E', 110, 110, 210, 'scpcb_wallmonitor')
    R.box(-512, 0, -120, -470, 180, 120, 'ElecBox')
    for z in (-720, -240, 240, 720):
        fixture(R, -176, z, h, along='z')
    # the shaft x 176..752: down to y -1024, up to y 768
    R.box(176, -1024 - T, -640, 768, -1024, 640, 'concrete', top='concretefloor')
    R.box(176, 768, -656, 768, 784, 656, 'concrete', bottom='metal')
    R.wall_x(752, -640, 640, -1024, 768, T, 'concretewall', inner='-')
    R.wall_z(-640, 176, 768, -1024, 768, T, 'concretewall', inner='+')
    R.wall_z(640, 176, 768, -1024, 768, T, 'concretewall', inner='-')
    R.box(160, -1024, -640, 176, 0, 640, 'concretewall')
    R.box(160, h, -640, 176, 768, 640, 'concretewall')
    for y in (-768, -384):
        R.box(176, y, -640, 192, y + 24, 640, 'hazard_stripe_wall_1789291234341')
    # the gantry: a beam across the shaft, a trolley, four chains and the platform at y -200
    R.box(176, 704, -40, 752, 752, 40, 'yellowmetal')
    R.box(420, 670, -56, 520, 704, 56, 'dirtymetal')
    for (dx, dz) in ((-80, -80), (80, -80), (-80, 80), (80, 80)):
        R.prism(470 + dx * 0.25, dz * 0.25, 4, -176, 670, 'indev_chain', n=6)
    R.box(370, -200, -100, 570, -176, 100, 'scpcb_checkerplate')
    R.box(370, -176, -100, 570, -120, -96, 'yellowmetal')
    R.box(370, -176, 96, 570, -120, 100, 'yellowmetal')
    R.model('crate3.x', 470, -176, 0, 0, 1.2)
    for z in (-560, 560):
        R.prism(200, z, 12, -1024, 768, 'metal', n=8)                    # guide rails
    for (x, z) in ((300, -500), (650, 500)):
        R.spot(x, 740, z, pitch=90, rng=1600, color=(255, 230, 190), inner=25, outer=55)
    R.light(470, -600, 0, color=(255, 120, 60), rng=700, intensity=0.6)  # a warning glow in the pit
    R.decal(-511, 0, 'E', 128, 128, 230, 'miscsigns3')
    R.sound(470, 300, 0, 4, rng=12)
    waypoints_z(R, -200, -1000, 1000)
    R.waypoint(0, -800); R.waypoint(0, 800)
    return R, [((-400, 170, -900), (100, 100, 200)), ((-50, 170, 0), (500, -100, 0))]


def shutters():
    """image 56: a storage corridor lined with roll-up shutters - housings, guide rails, bollards and floor
    markings; one shutter is half up over a bay of crates"""
    R = Room('room2cbre_shutters', 'Storage shutter corridor (ref. 56)')
    h = 416
    holes = {'z0': [door()], 'z1': [door()]}
    bays = (-640, -128, 384)
    open_bay = 384
    side = {'x0': [], 'x1': []}
    for zc in bays:
        side['x0'].append((zc - 160, zc + 160, 0, 288))
        side['x1'].append((zc - 160, zc + 160, 0, 288))
    holes.update(side)
    shell(R, -256, 256, -1008, 1008, h, 'concretewall', 'concretefloor', 'metal', holes)
    trims(R, -256, 256, -1008, 1008, holes, base='yellowmetal', band='scpcb_rivetband', band_y=330)
    for zc in bays:
        for (sx, face, xi) in ((-1, '+x', -256), (1, '-x', 256)):
            xo = xi + sx * 448
            # the bay behind
            R.box(min(xi, xo), -T, zc - 176, max(xi, xo), 0, zc + 176, 'concrete', top='concretefloor')
            R.box(min(xi, xo), 288, zc - 176, max(xi, xo), 304, zc + 176, 'concrete', bottom='metal')
            R.wall_x(xo, zc - 176, zc + 176, 0, 288, T, 'concretewall', inner='-' if sx > 0 else '+')
            R.wall_z(zc - 176, min(xi, xo), max(xi, xo), 0, 288, T, 'concretewall', inner='+')
            R.wall_z(zc + 176, min(xi, xo), max(xi, xo), 0, 288, T, 'concretewall', inner='-')
            # the shutter: curtain (half up in one bay), housing box, guide rails
            low = 150 if (zc == open_bay and sx > 0) else 0
            R.box(xi + sx * 4, low, zc - 160, xi + sx * 10, 288, zc + 160, 'indev_shutter19')
            R.box(xi - sx * 2, 288, zc - 176, xi + sx * 30, 336, zc + 176, 'metal_darker')
            for z in (zc - 168, zc + 160):
                R.box(xi - sx * 4, 0, z, xi + sx * 14, 288, z + 8, 'metal')
            # bollards and the yellow box marking in front of it
            for z in (zc - 200, zc + 200):
                R.prism(xi - sx * 30, z, 10, 0, 90, 'yellowmetal', n=8)
            R.box(xi - sx * 64, 0, zc - 162, xi - sx * 60, 1, zc + 162, 'yellowmetal')
            R.decal(xi, zc + 230, face, 64, 64, 230, 'miscsigns5')
            R.light(xi + sx * 220, 250, zc, color=(240, 240, 255), rng=420, intensity=0.7)
    for zc in (-800, -384, 128, 640, 896):
        fixture(R, 0, zc, h - 20, along='x', w=144)
    for zc in (-640, -128, 384):
        for (x, z) in ((330, zc - 60), (330, zc + 70), (400, zc)):
            R.model('crate1.x', x, 0, z, 15, 1.0)
        R.model('crate2.x', -360, 0, zc, 0, 1.0)
    for z in range(-896, 897, 256):
        beam_x(R, -256, 256, z, h, w=24, d=36, mat='metal')
    cable_tray_z(R, -180, h - 50, -1008, 1008)
    pipe_z(R, 180, h - 30, -1008, 1008, r=12)
    R.box(-4, 0, -1008, 4, 1, 1008, 'yellowmetal')                        # the centre line
    R.decal(0, -1007, 'N', 160, 48, 380, 'scpcb_lczsign')
    camera(R, -256, 900, h - 60, '+x')
    waypoints_z(R, 0, -1000, 1000)
    R.waypoint(380, open_bay - 100)
    return R, [((0, 170, -960), (0, 120, 200)), ((-150, 170, 100), (300, 90, 384))]


def dclass():
    """image 57: a D-class cell block - a narrow corridor with four cells, each with a bed, a steel toilet and a
    sink, a numbered sign and a barred vent; the cell fronts have openings for the game's cell doors"""
    R = Room('room2cbre_dclass', 'D-class cells: bed, toilet, sink (ref. 57)')
    h = 352
    holes = {'z0': [door()], 'z1': [door()], 'x0': [], 'x1': []}
    cells = (-400, 400)
    for zc in cells:
        holes['x0'].append(door(zc))
        holes['x1'].append(door(zc))
    shell(R, -160, 160, -1008, 1008, h, 'dclass_wall', 'concretefloor', 'ceiling', holes)
    trims(R, -160, 160, -1008, 1008, holes, base='metal', band='scpcb_rivetband', band_y=140)
    n = 1
    for zc in cells:
        for (sx, face, xi) in ((-1, '+x', -160), (1, '-x', 160)):
            xo = xi + sx * 448
            x0, x1 = min(xi, xo), max(xi, xo)
            R.box(x0 - T, -T, zc - 208, x1 + T, 0, zc + 208, 'concrete', top='concretefloor')
            R.box(x0 - T, 288, zc - 208, x1 + T, 304, zc + 208, 'concrete', bottom='ceiling')
            R.wall_x(xo, zc - 192, zc + 192, 0, 288, T, 'dclass_wall', inner='-' if sx > 0 else '+')
            R.wall_z(zc - 192, x0 - T, x1 + T, 0, 288, T, 'dclass_wall', inner='+')
            R.wall_z(zc + 192, x0 - T, x1 + T, 0, 288, T, 'dclass_wall', inner='-')
            inner_x = xi + sx * 16
            # the frame round the cell opening, the number over it
            for z in (zc - 112, zc + 96):
                R.box(xi - sx * 8, 0, z, xi - sx * 2, 336, z + 16, 'metal')
            R.box(xi - sx * 8, 320, zc - 112, xi - sx * 2, 336, zc + 112, 'metal')
            R.decal(xi - sx * 8, zc, face, 64, 40, 300, 'dclass_number%d' % n)
            R.decal(xi - sx * 8, zc - 160, face, 64, 64, 200, 'dclass_sign')
            # the furniture: bed against the back wall, toilet and sink against the side wall
            R.model('dclass_bed.x', xo - sx * 70, 0, zc + 100, 0, 1.0)
            R.model('dclass_toilet.x', xo - sx * 50, 0, zc - 140, 90 * sx, 1.0)
            R.model('dclass_sink.x', inner_x + sx * 150, 60, zc - 180, 0, 1.0)
            R.box(inner_x + sx * 120, 0, zc - 192, inner_x + sx * 200, 50, zc - 176, 'metal')   # sink pedestal
            R.decal(xo - sx * 1, zc, 'W' if sx > 0 else 'E', 64, 32, 260, 'vent')
            R.decal(inner_x + sx * 150, zc - 191, 'N', 40, 56, 150, 'mat_glass')          # the mirror over the sink
            R.box(xo - sx * 160, 288 - 8, zc - 30, xo - sx * 100, 288, zc + 30, 'metal', bottom='scpcb_lightpanel')
            R.light(xo - sx * 130, 250, zc, color=(255, 245, 225), rng=420, intensity=0.8)
            R.waypoint(xi + sx * 200, zc)
            n += 1
    for z in (-800, -400, 0, 400, 800):
        fixture(R, 0, z, h, along='x', w=96)
    for z in (-700, 0, 700):
        beam_x(R, -160, 160, z, h, w=24, d=32)
    pipe_z(R, -120, h - 24, -1008, 1008, r=8)
    R.decal(-159, 0, 'E', 128, 128, 200, 'dclass_sheet')
    camera(R, 160, 0, h - 60, '-x')
    R.decal(0, -1007, 'N', 160, 48, 360, 'scpcb_lczsign')
    waypoints_z(R, 0, -1000, 1000)
    return R, [((0, 170, -960), (0, 120, 0)), ((-60, 170, 400), (500, 90, 420))]


def junction():
    """image 58: a four-way junction around a massive octagonal pillar - plinth and capital bands, radial beams,
    a coffered ceiling, direction signs on the pillar and lights round it"""
    R = Room('room4cbre_pillar', 'Four-way junction with a central pillar (ref. 58)')
    h = 448
    a = 448            # half-size of the central hall
    c = 192            # half-width of the four arms
    # the central hall and four arms; walls only where an arm does not join
    R.box(-a - T, -T, -a - T, a + T, 0, a + T, 'concrete', top='tilefloor')
    R.box(-a - T, h, -a - T, a + T, h + T, a + T, 'concrete', bottom='ceiling')
    for s in (-1, 1):
        R.wall_x(s * a, -a, -c, 0, h, T, 'whitewall', inner='+' if s < 0 else '-')
        R.wall_x(s * a, c, a, 0, h, T, 'whitewall', inner='+' if s < 0 else '-')
        R.wall_z(s * a, -a - T, -c, 0, h, T, 'whitewall', inner='+' if s < 0 else '-')
        R.wall_z(s * a, c, a + T, 0, h, T, 'whitewall', inner='+' if s < 0 else '-')
        # the arm along z (to the door at z = s * 1024) and along x
        z0, z1 = sorted((s * a, s * 1008))
        R.box(-c - T, -T, z0, c + T, 0, z1, 'concrete', top='tilefloor')
        R.box(-c - T, 384, z0, c + T, 400, z1, 'concrete', bottom='ceiling')
        R.wall_x(-c, z0, z1, 0, 384, T, 'whitewall', inner='+')
        R.wall_x(c, z0, z1, 0, 384, T, 'whitewall', inner='-')
        R.wall_z(s * 1008, -c - T, c + T, 0, 384, T, 'whitewall', [door()], inner='-' if s > 0 else '+')
        R.box(-c, 384, s * a - T if s > 0 else s * a, c, h, s * a if s > 0 else s * a + T, 'whitewall')
        x0, x1 = sorted((s * a, s * 1008))
        R.box(x0, -T, -c - T, x1, 0, c + T, 'concrete', top='tilefloor')
        R.box(x0, 384, -c - T, x1, 400, c + T, 'concrete', bottom='ceiling')
        R.wall_z(-c, x0, x1, 0, 384, T, 'whitewall', inner='+')
        R.wall_z(c, x0, x1, 0, 384, T, 'whitewall', inner='-')
        R.wall_x(s * 1008, -c - T, c + T, 0, 384, T, 'whitewall', [door()], inner='-' if s > 0 else '+')
        R.box(s * a - T if s > 0 else s * a, 384, -c, s * a if s > 0 else s * a + T, h, c, 'whitewall')
        trims(R, -c, c, z0, z1, sides='x0 x1', band_y=150)
        trims(R, x0, x1, -c, c, sides='z0 z1', band_y=150)
        for d in (600, 860):
            fixture(R, 0, s * d, 384, along='z', w=96)
            fixture(R, s * d, 0, 384, along='x', w=96)
            R.decal(s * d, -c + 1, 'N', 96, 64, 250, 'miscsigns') if d == 860 else None
        R.decal(0, s * 1008 - s, 'S' if s > 0 else 'N', 160, 48, 360, 'scpcb_lczsign')
    # the pillar: an octagon with plinth, capital and a metal band; signs on four faces
    R.prism(0, 0, 150, 0, h, 'concretewall', n=8)
    R.prism(0, 0, 170, 0, 40, 'concrete', n=8, cap='metal')
    R.prism(0, 0, 160, 40, 48, 'metal', n=8)
    R.prism(0, 0, 176, h - 56, h, 'concrete', n=8, cap='concrete')
    R.prism(0, 0, 156, 180, 204, 'scpcb_rivetband', n=8)
    for (cx, cz, f) in ((0, -150, 'S'), (0, 150, 'N'), (150, 0, 'E'), (-150, 0, 'W')):
        R.decal(cx * 0.93, cz * 0.93, f, 112, 72, 270, 'scpcb_ezsign' if f in 'NS' else 'scpcb_lczsign', depth=2)
    # radial beams from the capital to the corners, a coffer frame round them
    for s in (-1, 1):
        beam_x(R, 176, a, s * 0, h, w=40, d=56) if s > 0 else beam_x(R, -a, -176, 0, h, w=40, d=56)
        beam_z(R, 176, a, 0, h, w=40, d=56) if s > 0 else beam_z(R, -a, -176, 0, h, w=40, d=56)
        beam_x(R, -a, a, s * 320, h, w=24, d=32, mat='dirtymetal')
        beam_z(R, -a, a, s * 320, h, w=24, d=32, mat='dirtymetal')
    for (x, z) in ((300, 300), (-300, 300), (300, -300), (-300, -300)):
        R.box(x - 40, h - 8, z - 40, x + 40, h, z + 40, 'metal', bottom='scpcb_lightpanel')
        R.light(x, h - 40, z, color=(255, 248, 232), rng=700)
    for (x, z) in ((a - 2, 300), (-a + 2, -300)):
        R.decal(x, z, 'W' if x > 0 else 'E', 96, 48, 300, 'vent')
    camera(R, -a, -a + 60, h - 60, '+x')
    R.sound(0, 300, 0, 1, rng=8)
    for k in range(-1000, 1001, 250):
        if abs(k) > 260:
            R.waypoint(0, k); R.waypoint(k, 0)
    for (x, z) in ((260, 260), (-260, 260), (260, -260), (-260, -260)):
        R.waypoint(x, z)
    return R, [((0, 170, -980), (0, 160, 0)), ((-330, 170, -330), (200, 220, 200))]


ROOMS = [storage, office, gallery, machine_corridor, hoist, shutters, dclass, junction]

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    preview = '--nopreview' not in sys.argv
    only = [a for a in sys.argv[1:] if not a.startswith('--')]
    for fn in ROOMS:
        R, views = fn()
        if only and R.name not in only:
            continue
        nb, ne = R.write_vmf(os.path.join(OUT, R.name + '.vmf'))
        print('%-22s %4d brushes %3d entities' % (R.name, nb, ne), flush=True)
        if preview:
            try:
                R.render(views, os.path.join(OUT, R.name + '_preview.jpg'))
            except Exception as ex:
                print('   preview failed:', ex)
