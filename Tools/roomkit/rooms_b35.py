"""The thirty-fifth batch: two more deep storage areas, built with the batch-34 storage room (rooms_b34.py) and our
own architecture, after the user's reference images 107-114:
  room2b35cellblock  HCZ  Storage Area 10 (ref. 108): a cell block - barred cells with bunks and the occupants
                          visible inside, an upper tier of cells along a railed gallery, ceiling light panels, the
                          Foundation emblem painted on the floor; a surveillance room (ref. 113/114) and a guard
                          locker room
  room2b35bunker     EZ   Storage Area 11 (ref. 111 / 109 / 110 / 107): board-marked bunker concrete, square pillars,
                          oval bulkhead wall lamps, pallets of boxes in the west bays behind yellow rails; a generator
                          and lockdown room (ref. 112); an old stone passage (ref. 110) with arch ribs and lamps (107)
Every unit as in batch 34: a placard, an interaction, a side effect (data35.py; IndevU35.bb)."""
import rooms_b34 as K
from rooms_b34 import *
import data35
from make_docs35 import AREA as AREA35, PAGES as PAGES35

BARS = Mat('indev_b35bars.png', cast=False)
LOGO = Mat('indev_b35logo.png', cast=False)
CONC35 = Mat('indev_b35conc.png', 320)
LAMP35 = Mat('indev_b35lamp.png', cast=False)
STONE35 = Mat('indev_b35stone.png', 256)
CRATE35 = Mat('indev_b35crate.png', 96)
STYLES['stone35'] = (STONE35, Mat('concretefloor.jpg', 256), DARK)
STYLES['bunk35'] = (CONC35, Mat('concretefloor.jpg', 256), CONC35)
K.MODEL_SIZE.update({'scp517': (92, 216, 72), 'scp806': (72, 160, 62), 'scp1579': (100, 342, 82), 'scp1512': (150, 142, 90)})


def heads569(R, u, x, z):
    """three marble heads drifting over a ring on the floor"""
    R.prism(octo(x, z, 90, 16), YL, YL + 2, Mat('white.jpg', 64), caps='T')
    unitpiv(R, u, (x, YL + 170, z), [(x - 20, YL + 170, z - 60), (x + 10, YL + 240, z + 10), (x - 10, YL + 140, z + 70)], 0)
    solid(R, (x - 60, YL + 100, z - 100, x + 60, YL + 280, z + 100), 'heads 569')


def docs35(R, key):
    n = AREA35[key][0]
    for p in range(len(PAGES35[key])):
        item(R, 'docarea%sp%d' % (n, p + 1), 300 + (p % 2) * 70, 0, -160 + (p // 2) * 70)


# ------------------------------------------------------------------------------------------------ decoration
def deco_cellblock(R):
    """ref. 108: the upper tier - a gallery with a railing over the east cells, more barred cells above; the emblem"""
    sbox(R, 790, 40, -990, 830, 52, 990, CHECKER, 'gallery E')
    for z in range(-990, 991, 110):
        R.tube((794, 52, z), (794, 152, z), 2.5, METAL, sides=6, caps=True)
    R.tube((794, 152, -990), (794, 152, 990), 3, METAL, sides=6, caps=True)
    R.tube((794, 100, -990), (794, 100, 990), 2, METAL, sides=6, caps=True)
    solid(R, (790, 52, -990, 798, 156, 990), 'gallery rail E')
    for k in range(4):                                                         # the upper cells: bars facing the hall
        z0 = -980 + k * 490
        R.decal((830, z0 + 480), (830, z0), 52, 300, BARS, (0, 0, 2, 1), off=0.5)
    R.box(830, 300, -1000, 960, 352, 1000, CONC35, lux=10)
    solid(R, (830, 300, -1000, 960, 352, 1000), 'upper cells lintel')
    R.rect_floor(470, -180, 770, 180, YL + 1, LOGO)                             # the emblem on the floor
    for z in range(-900, 901, 300):                                            # long light panels down the hall
        R.box(560, 346, z - 60, 680, 352, z + 60, METAL, bottom=LIGHTPANEL, lux=10)
        R.light(620, 330, z, rng=620, color=(240, 244, 255), power=55)
    for z in (-600, 0, 600):
        R.light(880, 120, z, rng=420, color=(230, 236, 255), power=30)


def deco_bunker(R):
    """ref. 111: square concrete pillars, oval bulkhead lamps along the walls; ref. 109: pallets of boxes in the bays"""
    for z in (-520, 0, 420):
        sbox(R, 580, YL, z - 40, 660, 352, z + 40, CONC35.but(us=160), 'pillar %d' % z, skip='TB')
    for z in range(-900, 901, 300):
        decal30(R, LAMP35, 256, z, 'E', 50, 38, YL + 230, 'wall lamp W %d' % z)
        R.light(290, YL + 230, z, rng=480, color=(255, 236, 196), power=45)
    for z in (-990, 990):
        for x in (420, 780):
            R.light(x, YL + 230, z * 0.98, rng=420, color=(255, 236, 196), power=35)
    for zc in (-900, -720, -540, -360):                                        # ref. 109: pallets of boxes
        sbox(R, 272, YL, zc - 62, 372, YL + 12, zc + 62, Mat('wood.jpg', 128), 'pallet %d' % zc)
        sbox(R, 276, YL + 12, zc - 58, 330, YL + 60, zc - 4, CRATE35, 'crate a %d' % zc)
        sbox(R, 276, YL + 12, zc + 4, 330, YL + 60, zc + 58, CRATE35, 'crate b %d' % zc)
        sbox(R, 286, YL + 60, zc - 40, 326, YL + 96, zc + 30, CRATE35, 'crate c %d' % zc)
        if zc != -360:
            sbox(R, 334, YL + 12, zc - 50, 368, YL + 46, zc + 50, CRATE35, 'crate d %d' % zc)
    for zc in (-900, -720, -540, -360):                                        # yellow rails in front of the bays
        R.tube((388, YL, zc - 70), (388, YL + 100, zc - 70), 3, YEL, sides=6, caps=True)
        R.tube((388, YL, zc + 70), (388, YL + 100, zc + 70), 3, YEL, sides=6, caps=True)
        R.tube((388, YL + 100, zc - 70), (388, YL + 100, zc + 70), 3.5, YEL, sides=6, caps=True)
        solid(R, (385, YL, zc - 73, 391, YL + 104, zc + 73), 'bay rail %d' % zc)


# ------------------------------------------------------------------------------------------------ side rooms
def side_E(R, X1, X2):
    # X1: the surveillance room (ref. 113 / 114): the CAUTION sign, monitors, two desks
    decal30(R, SIGNS, -192, -130, 'E', 150, 75, 260, 'surveillance sign', uv=(0, 0.5, 0.5, 1.0))
    office_desk(R, -700, -660, -580, -540, 'W', 'block desk 1', chair=(-545, -600))
    office_desk(R, -700, -260, -580, -140, 'W', 'block desk 2', chair=(-545, -200))
    for z in (-560, -400, -240):
        decal30(R, WMON, -776, z, 'E', 120, 100, 230, 'block monitor %d' % z)
    decal30(R, CONSP, -516, -700, 'N', 240, 120, 200, 'block console panel')
    named(R, 'CAMS', -770, 230, -400)
    ceil_light(R, -516, -400, 352, size=36, power=30, rng=520, color=(200, 220, 255))
    # X2: the guard locker room
    lockers(R, 'x', -776, 1, 140, 660)
    solid(R, (-776, 0, 140, -746, 300, 660), 'guard lockers')
    bench30(R, -620, 300, -460, 350, 'guard bench 1')
    bench30(R, -620, 480, -460, 530, 'guard bench 2')
    item(R, 'key3', -540, 78, 325, chance=50)
    decal30(R, LOCKP, -516, 700, 'S', 150, 150, 200, 'block door panel')
    named(R, 'DOORS', -516, 200, 690)
    ceil_light(R, -516, 400, 352, size=44, power=50, rng=600)


def side_F(R, X1, X2):
    # X1: the generator and lockdown room (ref. 112): the switch panel, the console, two generators
    decal30(R, LOCKP, -776, -400, 'E', 200, 200, 190, 'bunker lockdown panel')
    named(R, 'LOCKDOWN', -770, 190, -400)
    for z in (-620, -180):
        sbox(R, -700, 0, z - 50, -480, 140, z + 50, Mat('dirtymetal.jpg', 128), 'generator %d' % z, top=CTRL)
        R.tube((-700, 120, z), (-776, 300, z), 6, Mat('Pipes.jpg', 128), sides=8, caps=True)
    sbox(R, -420, 0, -700, -300, 96, -620, Mat('dirtymetal.jpg', 128), 'bunker console', top=CONSP)
    ceil_light(R, -516, -400, 352, size=40, power=45, rng=600, color=(255, 230, 200))
    # X2: the old stone passage (ref. 110), arched ribs and lamps (ref. 107), a sealed door at the end
    for z in (160, 240, 580, 660):
        R.tube((-760, 0, z), (-760, 250, z), 10, STONE35, sides=8, caps=False)
        R.tube((-272, 0, z), (-272, 250, z), 10, STONE35, sides=8, caps=False)
        R.tube((-760, 250, z), (-516, 340, z), 10, STONE35, sides=8, caps=False)
        R.tube((-516, 340, z), (-272, 250, z), 10, STONE35, sides=8, caps=False)
        solid(R, (-770, 0, z - 10, -750, 250, z + 10), 'rib W %d' % z)
        solid(R, (-282, 0, z - 10, -262, 250, z + 10), 'rib E %d' % z)
        R.light(-516, 300, z, rng=300, color=(255, 200, 140), power=30)
    decal30(R, Mat('Door01.jpg', cast=False), -516, 700, 'S', 110, 220, 110, 'sealed door')
    named(R, 'SEALED', -516, 120, 690)


K.SIDE.update({'E': side_E, 'F': side_F})
K.CENTER.update({'E': {'569': -600, '517': 600, '2890': -880},
                 'F': {'1579': -760, '806': -260, '1512-EX': 230, '2816': 600, '1388': 750, '1912': 900}})


def build(key, style, x1, x2, amb, opt):
    K.U = data35.U
    K.ROOMS = data35.ROOMS
    K.SCREENS = [u for u in data35.U if u['unit'] == 'screen']
    K.PLAC = Mat('indev_b35plac.png', cast=False)
    K.SCR = Mat('indev_b35scr.png', cast=False)
    K.SIGNS = Mat('indev_b35signs.png', cast=False)
    K.OPT.clear()
    K.OPT.update(opt)
    K.OPT['docs'] = docs35
    K.OPT['floor'] = {'scp569': heads569}
    return K.storage_room(key, style, x1, x2, amb=amb)


def room2b35cellblock():
    R = build('E', 'lcz', 'cell30', 'cell30', 9, dict(cellbars=True, beams=False, signk=0, doorkey=3,
                                                   wall=Mat('whitewall.jpg', 364).but(vs=608, v0=608),
                                                   floormat=Mat('concretefloor.jpg', 256), ceil=DARK, decorate=deco_cellblock))
    return (R, 'BLK', 'Storage Area 10, the cell block (Heavy Containment): barred cells on two tiers round the Foundation emblem - SCP-746, -886, -799, the moths, the parasite, the amoebae, the coin-eater, the marble heads, Grandmother Predictions.',
            2, 0.7, ((0, 165, -650), (0, 150, 300)))


def room2b35bunker():
    R = build('F', 'std', 'cell30', 'stone35', 9, dict(beams=False, signk=1, doorkey=2, part=CONC35, wall=CONC35.but(vs=608, v0=608),
                                                     floormat=Mat('concretefloor.jpg', 256), ceil=CONC35, decorate=deco_bunker))
    return (R, 'BNK', 'Storage Area 11, the bunker (Entrance Zone): board-marked concrete, pillars and wall lamps - the cedar giant, the jewelled projector, the organ printer, the paintbrushes, the pocket watch; the generator room and the old stone passage.',
            3, 0.65, ((0, 165, -650), (0, 150, 300)))


ALL = [room2b35cellblock, room2b35bunker]
