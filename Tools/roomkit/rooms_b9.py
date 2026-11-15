"""Four rooms for four SCPs (the ninth batch, code in IndevS04.bb).

  room2burn457   HCZ    Fire Post 457, and a lift down to the chamber: the gallery behind the blast window, the two
                        airlocks, the fireproofed chamber with its misting sprinklers and dry shelter (SCP-457)
  room2cold016   HCZ    BC-L5, the reference corridor a fourth time: the UV decon lock and the cold room with the
                        dish (SCP-016), D-016-1's flooded quarters, D-016-2's cell, the lab
  room2read152   HCZ    the scan archive, and a lift up to Reading Room 49: the guard, the desk, the book (SCP-152)
  room2dark280   Indev  the hall from the second reference shot: a chamfered block in the middle of a tiled hall,
                        a door in the block (the dark cell, SCP-280), a door in each side wall

Same conventions as rooms_b8.py; gen_b9.py turns names into S04_* constants."""
from rooms_b8 import *

L7 = json.load(open(os.path.join(HERE, 'labels7.json')))
DP7 = json.load(open(os.path.join(HERE, 'doorplates7.json')))
P7 = json.load(open(os.path.join(HERE, 'plates7.json')))
PR7 = json.load(open(os.path.join(HERE, 'props7.json')))
N7 = json.load(open(os.path.join(HERE, 'neon7.json')))
LAB7 = Mat('indev_labels7.png', cast=False)
DPL7 = Mat('indev_doorplates7.png', cast=False)
PLT7 = Mat('indev_plates7.png', cast=False)
PROPS7 = Mat('indev_props7.png', cast=False)
NEON7 = Mat('indev_neon7.png', emit=215, cast=False)
PERL = Mat('indev_perlite.png', 256)
SCORCH = Mat('indev_scorch.png', alpha=True, cast=False)
REDP = Mat('indev_sleighred.png', 64)
class BandMat(Mat):
    """a wall material with a fixed vertical layout: its dark band stays at one height however tall the wall is"""

    def but(self, **kw):
        kw.pop('vs', None)
        kw.pop('v0', None)
        m = BandMat(self.tex, self.us, self.vs, self.v0, self.alpha, self.emit, self.cast)
        for k, v in kw.items():
            setattr(m, k, v)
        return m


STYLES['pillar'] = (BandMat('whitewall.jpg', 364, 352, 352), TILE, DARK)
STYLES['read'] = (Mat('officewall.jpg', 364), CARPET, EZCEIL)


def label7(R, num, cx, cz, facing, yc=214.0, size=76.0):
    wall_decal(R, LAB7, cx, cz, facing, size, size, yc, uv=L7[num])


def doorplate7(R, k, cx, cz, facing, yc=258.0, size=68.0):
    wall_decal(R, DPL7, cx, cz, facing, size, size, yc, uv=DP7[k])


def plate7(R, k, cx, cz, facing, yc=352.0, w=230.0, h=None):
    wall_decal(R, PLT7, cx, cz, facing, w, h or w * 0.125, yc, uv=P7[k])


def prop7(R, k, cx, cz, facing, w, h, yc):
    wall_decal(R, PROPS7, cx, cz, facing, w, h, yc, uv=PR7[k])


def neon7(R, k, cx, cz, facing, w, h, yc):
    wall_decal(R, NEON7, cx, cz, facing, w, h, yc, uv=N7[k])


def box_room(R, x0, z0, x1, z1, style, h=352.0, y=0.0, holes=None):
    """A rectangular room seen from inside.  holes = {wall: [(c0, c1, y0, y1)]} with c in absolute units along
    the wall; walls: 0 west, 1 north, 2 east, 3 south."""
    wallm, floorm, ceilm = STYLES[style]
    out = [(x0, z0), (x0, z1), (x1, z1), (x1, z0)]
    hs = {}
    for seg, lst in (holes or {}).items():
        ref = out[seg][1] if seg in (0, 2) else out[seg][0]
        hs[seg] = [tuple(sorted((abs(c0 - ref), abs(c1 - ref)))) + (hy0, hy1) for (c0, c1, hy0, hy1) in lst]
    R.walls(out, y, y + h, wmat(style, h).but(v0=y + h), holes=hs)
    R.rect_floor(x0, z0, x1, z1, y, floorm)
    R.rect_ceil(x0, z0, x1, z1, y + h, ceilm)
    return (x0, z0, x1, z1)


def doorway(R, axis, a, b, c, y, floorm, wallm, w=192.0, h=320.0):
    """The lining of a door opening through a wall.  axis = the way the wall runs ('x' or 'z'), its thickness
    spans a..b, c = the centre of the opening along the wall."""
    c0, c1 = c - w / 2, c + w / 2
    if axis == 'z':
        poly_facing(R, [V(a, y, c0), V(b, y, c0), V(b, y, c1), V(a, y, c1)], (0, 1, 0), floorm, lux=10)
        poly_facing(R, [V(a, y + h, c0), V(b, y + h, c0), V(b, y + h, c1), V(a, y + h, c1)], (0, -1, 0), wallm, lux=10)
        poly_facing(R, [V(a, y, c0), V(b, y, c0), V(b, y + h, c0), V(a, y + h, c0)], (0, 0, 1), wallm, lux=10)
        poly_facing(R, [V(a, y, c1), V(b, y, c1), V(b, y + h, c1), V(a, y + h, c1)], (0, 0, -1), wallm, lux=10)
    else:
        poly_facing(R, [V(c0, y, a), V(c0, y, b), V(c1, y, b), V(c1, y, a)], (0, 1, 0), floorm, lux=10)
        poly_facing(R, [V(c0, y + h, a), V(c0, y + h, b), V(c1, y + h, b), V(c1, y + h, a)], (0, -1, 0), wallm, lux=10)
        poly_facing(R, [V(c0, y, a), V(c0, y, b), V(c0, y + h, b), V(c0, y + h, a)], (1, 0, 0), wallm, lux=10)
        poly_facing(R, [V(c1, y, a), V(c1, y, b), V(c1, y + h, b), V(c1, y + h, a)], (-1, 0, 0), wallm, lux=10)


# =====================================================================  HCZ
def room2burn457():
    R = R_('room2burn457', amb=9)
    AW = wmat('hcz', 384)
    junction(R, 'NS', 'hcz', openings={'hubW': [door_op(0)], 'hubE': [door_op(0)]})
    lift(R, -192, -1, 0, 0, 0, D, AW)
    plate7(R, 'c457', -192, 0, 'E', yc=352, w=240)
    sign_at(R, 'elevator', -192, -250, 'E', 150, 50, 250)
    label7(R, '457', -192, 250, 'E')
    plate7(R, 'three', -192, -560, 'E', yc=250, w=240)
    lamps(R, NS3, 384, power=74, color=(255, 232, 214), size=36)
    # ---- Fire Post 457, upstairs: suits, extinguishers, the hose reel, the fuel log
    x0, z0, x1, z1 = annex(R, 'x', 192, +1, -400, 400, 500, 352, 'std', door=0)
    plate7(R, 'firepost', 192, 0, 'W', yc=352, w=250)
    for z in (-320.0, -220.0, -120.0, 120.0, 220.0, 320.0):
        R.box(x1 - 46, 0, z - 44, x1, 230, z + 44, PANELS2.but(us=88, vs=230, v0=230), skip='BE', lux=10)
        prop7(R, 'firesuit', x1 - 46, z, 'W', 80, 110, 130)
    prop7(R, 'hosereel', 520, z1, 'S', 130, 130, 180)
    for k in range(4):
        x = 330.0 + k * 44
        R.tube((x, 0, z0 + 24), (x, 78, z0 + 24), 11, REDP.but(us=70), sides=8, caps=True, lux=14)
        R.tube((x, 78, z0 + 24), (x, 92, z0 + 24), 4, DARK, sides=6, caps=True, lux=20)
    dtop = desk(R, 290, 300, 450, 380, 0)
    prop7(R, 'fuellog', 370, z1, 'S', 120, 90, 200)
    R.model('scpcb_bench.x', 520, 0, -200, rot=(0, 0, 0), scale=(1, 1, 1), size=(144, 50, 44))
    ceil_fan(R, 500, 0, 352, radius=120)
    for z in (-220.0, 220.0):
        ceil_light(R, 440, z, 352, size=48, power=80, rng=680, color=(255, 240, 224))
    # ---- the containment level, down the lift
    HX, HZ, HH = 1000.0, 700.0, 420.0
    out = [(-192, -HZ), (-192, HZ), (HX, HZ), (HX, -HZ)]
    BW = wmat('dark', HH).but(v0=D + HH)
    R.walls(out, D, D + HH, BW, holes={0: [span(out[0], (-192, -96), (-192, 96)) + (D, D + 320)],
                                       1: [(500 - 80 + 192, 500 + 80 + 192, D + 220, D + 380)]})
    R.rect_floor(-192, -HZ, HX, HZ, D, HCZFLOOR)
    R.rect_ceil(-192, -HZ, HX, HZ, D + HH, DIRTY)
    wall_fan(R, 'z', HZ, +1, 500, D + 300)
    WX, T = 330.0, 14.0
    win = (-170.0, 170.0, D + 110, D + 280)
    # the wall between the gallery and the chamber / airlock 1: blast window, airlock door
    both_faces(R, (WX, -HZ), (WX, 344), D, D + HH, PERL, ('E', 'W'), holes=[(-616, -424, D, D + 320), win], mat2=BW, t=T)
    R.box(WX - T, D, 330, WX + T, D + HH, 344, BW, skip='TBS', lux=10)
    reveals(R, 'z', WX - T, WX + T, -616, -424, D, D + 320, LEAD)
    reveals(R, 'z', WX - T, WX + T, win[0], win[1], win[2], win[3], LEAD)
    glass_quad(R, (WX, win[0]), (WX, win[1]), win[2], win[3])
    # the chamber's north and south walls, the wall between the two airlocks
    both_faces(R, (WX, 330), (HX, 330), D, D + HH, PERL, ('S', 'N'), mat2=BW, t=T)
    both_faces(R, (WX + T, -330), (HX, -330), D, D + HH, PERL, ('N', 'S'), holes=[(604, 796, D, D + 320)], t=T)
    reveals(R, 'x', -330 - T, -330 + T, 604, 796, D, D + 320, LEAD)
    both_faces(R, (574, -HZ), (574, -330 - T), D, D + HH, PERL, ('E', 'W'), holes=[(-616, -424, D, D + 320)], t=T)
    reveals(R, 'z', 574 - T, 574 + T, -616, -424, D, D + 320, LEAD)
    ndoor(R, 'AL1', WX, D, -520, 90, key=3)
    ndoor(R, 'AL2', 574, D, -520, 90)
    ndoor(R, 'AL3', 700, D, -330, 0)
    # the chamber: fireproof boards on every face, a wet floor with a drain, sprinkler mains, the dry shelter
    wall_facing(R, (HX - 2, -316), (HX - 2, 316), D, D + HH, PERL, 'W')
    R.rect_floor(WX + T, -316, HX - 2, 316, D + 1.0, CONC)
    flat(R, 620, -50, 720, 50, D + 1.8, PROPS7, PR7['drain'])
    for z in (-200.0, 0.0, 200.0):
        R.tube((WX + T + 6, D + HH - 26, z), (HX - 8, D + HH - 26, z), 7, RUST.but(us=44, vs=256), sides=6, lux=18)
        for x in (430.0, 590.0, 750.0, 910.0):
            R.tube((x, D + HH - 44, z), (x, D + HH - 26, z), 4, DIRTY, sides=5, lux=24)
    R.box(880, D + 190, 204, HX - 2, D + 204, 316, DIRTY, lux=10)
    R.box(868, D, 204, 880, D + 204, 316, PERL, skip='B', lux=10)
    named(R, 'FLAME', 942, D, 262)
    named(R, 'WIN', 430, D, 0)
    named(R, 'CENTER', 670, D, 0)
    named(R, 'CHAR', HX - 5, D + 230, -120)
    R.tube((670, D + HH - 66, 0), (670, D + HH, 0), 14, RUST.but(us=88), sides=8, lux=16)
    named(R, 'FUELP', 670, D + HH - 76, 0)
    prop7(R, 'hosereel', 480, -316, 'N', 110, 110, D + 150)
    named(R, 'HOSE', 480, D + 150, -306)
    plate7(R, 'hose', 480, -316, 'N', yc=D + 240, w=170)
    named(R, 'BODY', 420, D, 250)
    for (cx, cz, f, s) in ((HX - 2, 120.0, 'W', 300.0), (700.0, 316.0, 'S', 280.0), (WX + T, 230.0, 'E', 200.0)):
        wall_decal(R, SCORCH, cx, cz, f, s, s, D + 150)
    flat(R, 820, 160, 990, 316, D + 1.6, SCORCH, lm=False, coll=False)
    flat(R, 380, -80, 520, 80, D + 1.6, SCORCH, lm=False, coll=False)
    R.light(930, D + 110, 250, rng=640, color=(255, 140, 50), power=74, ent=False)
    ceil_light(R, 600, -160, D + HH, size=40, power=40, rng=560, color=(255, 214, 190))
    # the airlocks
    plate7(R, 'airlock1', WX - T, -520, 'W', yc=D + 352, w=180)
    plate7(R, 'airlock2', 574 - T, -520, 'W', yc=D + 352, w=180)
    plate7(R, 'c457', 700, -330 - T, 'S', yc=D + 352, w=220)
    ceil_light(R, 450, -520, D + HH, size=40, power=60, rng=460, color=(240, 244, 255))
    red_lamp(R, 790, -520, D + HH, power=60, rng=460)
    # the gallery: the console under the window, the mist lever, the read-out
    R.box(250, D, -180, 304, D + 86, 180, DARK, skip='B', top=METAL, lux=10)
    for (z, mat) in ((-80.0, REDP), (80.0, Mat('indev_gold.png', 64))):
        R.prism(octo(277, z, 12), D + 86, D + 94, mat, caps='T', lux=20)
    named(R, 'FUEL', 277, D + 96, -80)
    named(R, 'SHIELD', 277, D + 96, 80)
    plate7(R, 'fuel', WX - T, -110, 'W', yc=D + 312, w=140)
    plate7(R, 'blast', WX - T, 110, 'W', yc=D + 312, w=140)
    named(R, 'SHUTTER', WX - T - 8, D + 375, 0)
    neon7(R, 'chamber', WX - T, -300, 'W', 190, 95, D + 200)
    plate7(R, 'allot', WX - T, -300, 'W', yc=D + 120, w=190)
    lever(R, 'SPRINK', WX - T - 4, D + 150, 250, 270, up=True)
    plate7(R, 'mistrun', WX - T, 250, 'W', yc=D + 230, w=170)
    # the pump room behind the chamber, the tech, the documents
    R.box(700, D, 520, 960, D + 250, 690, PANELS2.but(us=260, vs=250, v0=D + 250), skip='B', top=DARK, lux=10)
    for x in (740.0, 830.0, 920.0):
        R.tube((x, D + 250, 600), (x, D + HH, 600), 12, RUST.but(us=75), sides=8, lux=16)
    R.tube((400, D + 60, 690), (700, D + 60, 690), 10, RUST.but(us=63), sides=8, lux=16)
    named(R, 'TECH', 60, D, 420)
    ttop = table(R, -160, 560, 0, 660, y=D)
    bigfan(R, 60, D + HH - 12, -420, radius=110)
    for (x, z) in ((60.0, 0.0), (60.0, 520.0), (560.0, 520.0)):
        ceil_light(R, x, z, D + HH, size=56, power=70, rng=780, color=(232, 240, 255))
    reserve(R, 'FLAMEM')
    reserve(R, 'FLAME2M')
    reserve(R, 'CHARM')
    reserve(R, 'SHUTM')
    item(R, 'doc457', -80, ttop, 610)
    item(R, 'doc457b', 370, dtop, 340)
    item(R, 'hazmatsuit', 640, 0, 0, 35)
    return (R, 'BRN', 'Fire Post 457 (Indev): suits and hoses, and a lift down to the fireproofed chamber where SCP-457 burns under the sprinklers.',
            2, 0.4, ((40, D + 165, -300), (700, D + 150, 80)))


def room2cold016():
    """The reference corridor a fourth time, as a biological containment wing."""
    R = R_('room2cold016')
    w, ch = 224.0, 448.0
    win = (-150.0, 150.0, 100.0, 330.0)
    junction(R, 'NS', 'lcz', w=w, ch=ch, openings={'S_W': [door_op(-560)], 'N_W': [door_op(560)],
                                                   'S_E': [door_op(-560)], 'N_E': [door_op(560)], 'hubE': [win]})
    WM = wmat('lcz', ch)
    for c in (-800, -330, 330, 800):
        chamfer_pilaster(R, -w, +1, c, ch, WM)
        chamfer_pilaster(R, w, -1, c, ch, WM)
        R.box(-w, ch - 64, c - 36, w, ch, c + 36, WM.but(us=256), skip='T', lux=12)
    plate7(R, 'bcl5', -w, 0, 'E', yc=310, w=260)
    plate7(R, 'sigma', -w, 0, 'E', yc=262, w=230)
    prop7(R, 'biohaz', -w, 0, 'E', 110, 110, 170)
    label7(R, '016', w, 190, 'W', size=56)
    lamps(R, ((0, -560), (0, 0), (0, 560)), ch, power=92, rng=900, size=32)
    # ---- west: D-016-2's quarters (south) and D-016-1's flooded quarters (north)
    annex(R, 'x', -w, -1, -860, -260, 448, 352, 'cell', door=-560)
    doorplate7(R, 'd0162', -w, -560 + 132, 'E')
    annex(R, 'x', -w, -1, 260, 860, 448, 352, 'white', door=560)
    doorplate7(R, 'd0161', -w, 560 - 132, 'E')
    # D-016-2: he grew fists and tried the door; the water went down afterwards
    beds(R, -730, -590, (-790,))
    flat(R, -720, -840, -310, -300, 0.8, WATERM, lm=False, coll=False)
    prop7(R, 'dent', -288, -380, 'W', 130, 195, 150)
    named(R, 'BODY2', -470, 0, -430)
    red_lamp(R, -512, -560, 352, power=44, rng=560)
    # D-016-1: a glass wall across the room, the far half full of water
    GX = -520.0
    glass_quad(R, (GX, 260), (GX, 860), 0, 300)
    R.box(GX - 6, 300, 260, GX + 6, 352, 860, DARK, lux=10)
    for z in (264.0, 560.0, 856.0):
        R.box(GX - 5, 0, z - 4, GX + 5, 300, z + 4, DARK, skip='TB', lux=10)
    R.quad(V(GX - 3, 0, 260), V(GX - 3, 0, 860), V(GX - 3, 280, 860), V(GX - 3, 280, 260), WATERM, uvrect=(0, 0, 2.4, 1.1), lm=False, coll=False)
    flat(R, -736, 260, GX, 860, 280, WATERM, lm=False, coll=False)
    R.light(-630, 200, 560, rng=520, color=(90, 150, 230), power=60, ent=False)
    named(R, 'FISHA', -630, 130, 350)
    named(R, 'FISHB', -630, 130, 770)
    wall_decal(R, CTRL, -400, 860, 'S', 60, 60, 150)
    named(R, 'DRAIN', -400, 150, 852)
    plate7(R, 'nodrain', -400, 860, 'S', yc=215, w=170)
    R.model('scpcb_bench.x', -370, 0, 560, rot=(0, 90, 0), scale=(1, 1, 1), size=(44, 50, 144))
    ceil_light(R, -400, 560, 352, size=40, power=60, rng=520, color=(230, 240, 255))
    # ---- east, south: the UV decon lock; east, middle: the cold room behind the corridor window
    LM, CM_ = wmat('lab', 352), wmat('cold', 352)
    box_room(R, 288, -860, 736, -260, 'lab', holes={0: [(-656, -464, 0, 320)], 1: [(416, 608, 0, 320)]})
    doorway(R, 'z', w, 288, -560, 0, STYLES['lab'][1], LM)
    R.door_marker(256, 0, -560, 90)
    R.spawns.append(dict(kind='door', pos=(256, 0, -560), angle=90, key=3))
    doorplate7(R, 'decon', w, -560 + 132, 'W')
    doorplate7(R, '016', w, -560 - 132, 'W')
    box_room(R, 288, -200, 736, 200, 'cold', holes={0: [win], 3: [(416, 608, 0, 320)], 2: [(-180, -20, 170, 330)]})
    reveals(R, 'z', w, 288, win[0], win[1], win[2], win[3], DARK)
    glaze(R, 'x', w, +1, win)
    doorway(R, 'x', -260, -200, 512, 0, STYLES['cold'][1], CM_)
    ndoor(R, 'COLD', 512, 0, -230, 0)
    wall_fan(R, 'x', 736, +1, -100, 250)
    # the lock: UV tubes, the cycle button, the shower, MOPP lockers
    neon7(R, 'uv', 736, -560, 'W', 480, 26, 304)
    neon7(R, 'uv', 512, -860, 'N', 380, 26, 304)
    R.light(520, 270, -560, rng=640, color=(170, 110, 255), power=62, ent=False)
    ceil_light(R, 420, -420, 352, size=36, power=50, rng=460, color=(240, 240, 255))
    wall_decal(R, CTRL, 672, -260, 'S', 56, 56, 150)
    named(R, 'UVBTN', 672, 150, -268)
    plate7(R, 'uvrun', 672, -260, 'S', yc=205, w=110)
    plate7(R, 'coldroom', 352, -260, 'S', yc=250, w=118)
    plate7(R, 'uvfirst', 352, -260, 'S', yc=205, w=118)
    prop7(R, 'uvsign', 288, -360, 'E', 120, 60, 230)
    R.tube((380, 250, -780), (380, 352, -780), 7, DIRTY, sides=6, lux=18)
    R.prism(octo(380, -780, 24), 240, 250, DIRTY, caps='B', lux=16)
    flat(R, 340, -820, 420, -740, 0.8, PROPS7, PR7['drain'])
    lockers(R, 'z', -860, +1, 440, 704, h=250)
    plate7(R, 'mopp', 572, -860, 'N', yc=300, w=170)
    # the cold room: the cube on its plinth, the dish, the tray somebody dropped, supplies, frost
    top = plinth(R, 560, 0, h=90, s=40)
    glass_box(R, 524, top, -36, 596, top + 92, 36)
    R.prism(octo(560, 0, 15), top + 10, top + 15, WHITE, caps='T', top=FLESH.but(us=24), lux=20)
    named(R, 'DISH', 560, top + 24, 0)
    R.box(408, 0, 92, 452, 5, 132, METAL, skip='B', lux=14)
    flat(R, 396, 70, 476, 150, 0.9, FLESH.but(us=70), lm=False, coll=False)
    for (gx, gz) in ((420.0, 150.0), (462.0, 120.0), (400.0, 118.0)):
        R.prism(octo(gx, gz, 7), 0, 3, GLASS, caps='T', lm=False, coll=False)
    named(R, 'TRAY', 432, 6, 112)
    cabinet(R, 660, 168, 0, 'S')
    named(R, 'SUPPLY', 660, 100, 126)
    neon7(R, 'cold', 736, 110, 'W', 110, 55, 250)
    for (cx, cz, f) in ((512.0, 200.0, 'S'), (736.0, 40.0, 'W')):
        wall_decal(R, FROST, cx, cz, f, 260, 260, 170)
    ceil_light(R, 512, 0, 352, size=48, power=66, rng=560, color=(200, 228, 255))
    # ---- east, north: the lab
    lx0, lz0, lx1, lz1 = annex(R, 'x', w, +1, 260, 860, 448, 352, 'lab', door=560)
    doorplate7(R, 'lab016', w, 560 - 132, 'W')
    dtop = desk(R, 400, 780, 660, 850, 0)
    workstation(R, 460, dtop, 815, 180)
    chair(R, 460, 720, 'N')
    prop7(R, 'exptable', lx1, 560, 'W', 300, 150, 210)
    R.box(300, 0, 280, 380, 190, 350, WHITE, skip='B', lux=10)
    wall_decal(R, FROST, 340, 350, 'N', 76, 180, 96)
    prop7(R, 'biohaz', 340, lz0, 'N', 70, 70, 250)
    named(R, 'DOC', 560, 0, 520)
    ceil_fan(R, 512, 640, 352, radius=110)
    ceil_light(R, 512, 420, 352, size=48, power=86, rng=640, color=(250, 250, 255))
    reserve(R, 'FISHM')
    item(R, 'doc016', 580, dtop, 815)
    item(R, 'doc016b', 150, 0, -470)
    item(R, 'gasmask', 600, 0, -780, 70)
    item(R, 'firstaid', -660, 58, -790, 60)
    return (R, 'COL', 'BC-L5 wing (Indev): a UV decon lock and the cold room that holds SCP-016, with the quarters of two of its test subjects.',
            2, 0.65, ((0, 165, -940), (0, 190, 0)))


def room2read152():
    R = R_('room2read152')
    AW = wmat('hcz', 384)
    junction(R, 'NS', 'hcz', openings={'hubW': [door_op(0)], 'hubE': [door_op(0)]})
    lift(R, -192, -1, 0, 0, 0, UP, AW)
    plate7(R, 'reading', -192, 0, 'E', yc=352, w=220)
    sign_at(R, 'elevator', -192, -250, 'E', 150, 50, 250)
    label7(R, '152', -192, 250, 'E')
    plate7(R, 'level2', -192, -560, 'E', yc=250, w=230)
    lamps(R, NS3, 384, power=76, color=(255, 236, 214), size=36)
    # ---- the scan archive: a copy of every edition the book has been
    x0, z0, x1, z1 = annex(R, 'x', 192, +1, -360, 360, 460, 352, 'ez', door=0)
    plate7(R, 'editions', 192, 0, 'W', yc=352, w=240)
    for (za, zb) in ((300.0, 352.0), (-352.0, -300.0)):
        t = shelf_unit(R, 290, za, 690, zb, 0, height=250, levels=4)
        for y in t[1:]:
            for k in range(4):
                xa = 300 + k * 96
                tbox(R, xa, y, za + 8, xa + 88, y + 44, zb - 8, PROPS7, PR7['edition'], top=(0.76, 0.38, 0.78, 0.4))
    dtop = desk(R, 560, -70, 700, 70, 0)
    R.box(580, dtop, -46, 670, dtop + 26, 46, BEIGE, lux=10)
    chair(R, 500, 0, 'E')
    named(R, 'ARCH', 400, 0, 150)
    ceil_light(R, 480, 0, 352, size=64, power=96, rng=760, color=(255, 240, 220))
    # ---- Reading Room 49, up the lift: the guard's landing, the room, the desk, the book
    X0, X1, ZH, HH = -192.0, 1000.0, 520.0, 400.0
    out = [(X0, -ZH), (X0, ZH), (X1, ZH), (X1, -ZH)]
    UW = wmat('read', HH).but(v0=UP + HH)
    R.walls(out, UP, UP + HH, UW, holes={0: [span(out[0], (X0, -96), (X0, 96)) + (UP, UP + 320)]})
    R.rect_floor(X0, -ZH, X1, ZH, UP, CARPET)
    R.rect_ceil(X0, -ZH, X1, ZH, UP + HH, EZCEIL)
    PX, T = 330.0, 12.0
    both_faces(R, (PX, -ZH), (PX, ZH), UP, UP + HH, UW, ('E', 'W'), holes=[(-96, 96, UP, UP + 320)], t=T)
    reveals(R, 'z', PX - T, PX + T, -96, 96, UP, UP + 320, DARK)
    ndoor(R, 'READ', PX, UP, 0, 90, key=2)
    plate7(R, 'reading', PX - T, 0, 'W', yc=UP + 352, w=200)
    plate7(R, 'level2', PX - T, 220, 'W', yc=UP + 170, w=190)
    prop7(R, 'quietcard', PX - T, -230, 'W', 160, 120, UP + 210)
    plate7(R, 'quiet', X0, 300, 'E', yc=UP + 240, w=170)
    named(R, 'GUARD', 190, UP, -150)
    R.model('scpcb_bench.x', 20, UP, 470, rot=(0, 0, 0), scale=(1, 1, 1), size=(144, 50, 44))
    neon7(R, 'cam', 60, -ZH, 'N', 200, 100, UP + 220)
    ceil_fan(R, 60, 260, UP + HH, radius=120)
    ceil_light(R, 60, -160, UP + HH, size=56, power=84, rng=700, color=(255, 236, 214))
    dtop2 = desk(R, 600, -70, 760, 70, UP)
    R.box(610, dtop2, -48, 750, dtop2 + 4, 48, DARK, lux=10)
    named(R, 'BOOK', 680, dtop2 + 4, 0)
    chair(R, 680, -140, 'N', y=UP)
    pendant(R, 680, 0, UP + HH, power=120, rng=760)
    R.box(880, UP, -430, 990, UP + 104, -320, BEIGE, skip='B', top=DARK, lux=10)
    named(R, 'PRINTER', 935, UP + 110, -375)
    R.box(962, UP + 344, 482, 992, UP + 372, 512, DARK, lux=12)
    R.tube((960, UP + 356, 484), (936, UP + 344, 462), 7, DARK, sides=6, caps=True, lux=20)
    neon7(R, 'scale', X1, 0, 'W', 130, 65, UP + 210)
    red_lamp(R, 960, 0, UP + HH, power=30, rng=360)
    plate7(R, 'lastpage', 680, ZH, 'S', yc=UP + 250, w=260)
    reserve(R, 'BOOKM')
    item(R, 'doc152', 600, dtop, 30)
    return (R, 'RDR', 'Reading Room 49 (Indev): the scan archive, and a lift up to the locked room where SCP-152 lies open at its last page.',
            2, 0.2, ((400, UP + 165, -400), (700, UP + 70, 0)))


# =====================================================================  Indev zone
def room2dark280():
    """The second reference shot: a tiled hall, dark, with a big chamfered block in the middle of it; a door
    in the block and one in each side wall."""
    R = R_('room2dark280', amb=8)
    hh, ch = 448.0, 384.0
    hub = (-640.0, -700.0, 640.0, 700.0)
    fan_hole = (340.0, 500.0, 220.0, 380.0)
    junction2(R, 'NS', 'pillar', w=192.0, ch=ch, hub=hub, hh=hh, cut=180.0,
              openings={'hubW': [door_op(0), fan_hole], 'hubE': [door_op(0)]}, waypoints=False)
    # the way round the block (the middle of the hub is inside the cell)
    for (x, z) in ((0, -720), (0, -520), (-450, -480), (-450, 480), (450, -480), (450, 480), (0, 520), (0, 720)):
        R.waypoint(x, 66, z)
    wall_fan(R, 'x', -640, -1, 420, 300)
    # the block: outside faces (counter-clockwise from above = seen from outside), the door in its east face
    c0, cc = 300.0, 100.0
    core = [(-c0 + cc, -c0), (c0 - cc, -c0), (c0, -c0 + cc), (c0, c0 - cc), (c0 - cc, c0), (-c0 + cc, c0), (-c0, c0 - cc), (-c0, -c0 + cc)]
    WMc = wmat('pillar', hh)
    R.walls(core, 0, hh, WMc, holes={2: [(c0 - cc - 96, c0 - cc + 96, 0, 320)]})
    R.box(-c0 + cc, 0, -c0 - 6, c0 - cc, 22, -c0, DARK, skip='BN', lux=10)
    R.box(-c0 + cc, 0, c0, c0 - cc, 22, c0 + 6, DARK, skip='BS', lux=10)
    R.box(-c0 - 6, 0, -c0 + cc, -c0, 22, c0 - cc, DARK, skip='BE', lux=10)
    for (za, zb) in ((-c0 + cc, -104.0), (104.0, c0 - cc)):
        R.box(c0, 0, za, c0 + 6, 22, zb, DARK, skip='BW', lux=10)
    # the cell inside it: bare, unlit
    ci, ck = 276.0, 112.0
    cell = [(-ci, -ci + ck), (-ci, ci - ck), (-ci + ck, ci), (ci - ck, ci), (ci, ci - ck), (ci, -ci + ck), (ci - ck, -ci), (-ci + ck, -ci)]
    CMd = wmat('dark', 400)
    R.walls(cell, 0, 400, CMd, holes={4: [(ci - ck - 96, ci - ck + 96, 0, 320)]})
    R.floor(cell, 0.6, CONC)
    R.ceil(cell, 400, DARK)
    doorway(R, 'z', ci, c0, 0, 0, CONC, DARK)
    ndoor(R, 'CELL', (ci + c0) / 2, 0, 0, 90, key=3, old=True)
    plate7(R, 'dark280', c0, 0, 'E', yc=352, w=200)
    plate7(R, 'nolight', c0, 150, 'E', yc=236, w=96)
    label7(R, '280', c0, -150, 'E', size=70)
    doorplate7(R, '280', -130, -c0, 'S', yc=250)
    plate7(R, 'onemetre', 60, -c0, 'S', yc=250, w=236)
    plate7(R, 'noequip', 0, c0, 'N', yc=250, w=236)
    named(R, 'HOME', -180, 0, 180)
    for k, (x, z) in enumerate(((0.0, -540.0), (-470.0, 0.0), (470.0, 0.0), (0.0, 540.0))):
        named(R, 'TP%d' % k, x, 0, z)
    named(R, 'CELLC', 0, 0, 0)
    named(R, 'BODY', 150, 0, -170)
    named(R, 'LAMPFX', 190, 397, 0)
    named(R, 'FLOODFX', 0, 397, 0)
    # ---- west: cell lighting control
    cx0, cz0, cx1, cz1 = annex(R, 'x', -640, -1, -300, 300, 280, 352, 'std', door=0)
    plate7(R, 'lampctl', -640, 0, 'E', yc=352, w=220)
    lever(R, 'LAMP', cx0 + 4, 150, -90, 90, up=False)
    lever(R, 'FLOOD', cx0 + 4, 150, 90, 90, up=False)
    plate7(R, 'lamp', cx0, -90, 'E', yc=222, w=130)
    plate7(R, 'flood', cx0, 90, 'E', yc=222, w=130)
    neon7(R, 'irmon', -844, cz0, 'N', 220, 110, 210)
    dtop = desk(R, -950, -290, -750, -220, 0)
    chair(R, -850, -170, 'S')
    named(R, 'TECH', -800, 0, 190)
    ceil_light(R, -844, 0, 352, size=40, power=56, rng=520, color=(232, 240, 255))
    # ---- east: the equipment store
    sx0, sz0, sx1, sz1 = annex(R, 'x', 640, +1, -300, 300, 280, 352, 'std', door=0)
    plate7(R, 'irgear', 640, 0, 'W', yc=352, w=220)
    prop7(R, 'irrack', sx1, 0, 'W', 330, 124, 200)
    prop7(R, 'lamps', 844, sz0, 'N', 130, 98, 200)
    t = shelf_unit(R, 720, 236, 970, 296, 0, height=220, levels=3)
    for y in t[1:]:
        R.box(740, y, 246, 800, y + 30, 286, DARK, lux=12)
        R.box(840, y, 246, 950, y + 22, 286, BEIGE, lux=12)
    crate(R, 760, 0, -220, yaw=12)
    ceil_fan(R, 844, 60, 352, radius=110)
    ceil_light(R, 844, -120, 352, size=40, power=60, rng=520, color=(255, 236, 214))
    # ---- the hall is kept dim
    for (x, z) in ((-470.0, -540.0), (470.0, -540.0), (-470.0, 540.0), (470.0, 540.0)):
        ceil_light(R, x, z, hh, size=36, power=48, rng=640, color=(226, 232, 244))
    lamps(R, ((0, -860), (0, 860)), ch, power=58, rng=620, size=32)
    reserve(R, 'S280M')
    reserve(R, 'EYEM')
    reserve(R, 'LAMPM')
    reserve(R, 'POOLM')
    reserve(R, 'FLOODM')
    reserve(R, 'FPOOLM')
    item(R, 'doc280b', -850, dtop, -255)
    item(R, 'doc280', 760, 60, -220)
    item(R, 'bat', 900, 0, -200, 60)
    return (R, 'DRK', 'Dark Cell 280 (Indev): a chamfered block in the middle of a dim tiled hall. SCP-280 is kept inside it, in the dark.',
            4, 0.6, ((-70, 150, -940), (90, 170, 0)))


ALL = [room2burn457, room2cold016, room2read152, room2dark280]
