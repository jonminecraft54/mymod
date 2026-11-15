"""The fiftieth batch (code in IndevU50.bb): a working research complex - five everyday rooms, three SCPs.
Original SCP:CB textures and props only; ordinary room2 tiles with the map's doors at both ends.

  room2b50lab02     LCZ  Research Laboratory 02: benches, consoles, sample fridges - and on the east bench, SCP-061,
                         a small device that gives orders you can't hear but obey (switch by the door)
  room2b50chem      LCZ  Chemical Storage: steel shelving, drums, an eyewash station; old pipes along the ceiling
  room2b50observe   HCZ  Experimental Observation Room: a gallery with a window wall over a sunken test chamber
                         (ref.: the observation pit screenshots); in the pit, SCP-162, the ball of hooks
  room2b50office    LCZ  Researcher Office: three desks, cabinets, the whiteboard, coffee gone cold
  room2b50specimen  HCZ  Small Specimen Storage: shelves of sealed jars, two freezers - and a corner where the
                         walls have gone dark and soft: SCP-020, the unseen mold
"""
from rooms_b47 import *

WM, FM, CM = STYLES['lcz']
TILE = FM
GLASSF = Mat('dirtymetal.jpg', 64)
MOLD = Mat('indev_b50mold.png', 128)


def lab_bench(R, x0, z0, x1, z1, name):
    sbox(R, x0, 0, z0, x1, 90, z1, WHITE, name)
    R.box(x0, 90, z0, x1, 94, z1, DARK, lux=10)                                    # the black bench top


def room2b50lab02():
    R = R_('room2b50lab02', amb=30)
    B = shell(R, 'lab', -560, 560, WM, luxel=20.0)
    # benches down both long walls, sinks and a fume hood
    for k, (z0, z1) in enumerate(((-900, -560), (-420, -80), (80, 420))):
        lab_bench(R, -560, z0, -440, z1, 'west bench %d' % k)
    lab_bench(R, 440, -900, 560, -560, 'east bench 0')
    lab_bench(R, 440, 80, 560, 420, 'east bench 1 (SCP-061)')
    model30(R, 'dclass_sink.x', -500, 90, -740, 90, (40, 30, 50), 'lab sink')
    sbox(R, 440, 0, -420, 560, 260, -200, METAL, 'fume hood')
    console30(R, 470, 700, 'W', 'lab console')
    sbox(R, -560, 0, 600, -460, 200, 760, WHITE, 'sample fridge')
    model30(R, 'monitor.x', -500, 94, 220, 90, (40, 40, 26), 'bench monitor')
    for k, z in enumerate((-250, 250)):
        chair(R, -400, z, 270, 'lab stool %d' % k)
    # SCP-061: a small grey box with a speaker grille on the east bench; its switch on the wall by the south door
    R.box(480, 94, 210, 540, 130, 290, METAL, lux=10)
    R.box(478, 100, 230, 480, 124, 270, VENT, lux=10)
    named(R, 'DEV61', 478, 112, 250)
    R.box(-180, 120, -990, -140, 170, -986, METAL, lux=10)
    named(R, 'SW61', -160, 145, -984)
    item(R, 'docb50_061', 500, 94, 360)
    item(R, 'docb50_lab', -500, 94, -300)
    item(R, 'eyedrops', -500, 94, 160, chance=40)
    for z in (-600, 0, 600):
        R.light(0, 320, z, rng=600, color=(245, 248, 255), power=126)
    B.clear = [((-110, 0, -1000, 110, 200, 1000), 'walkway')]
    check_b42(R)
    return (R, 'L02', 'Research Laboratory 02 (Light Containment): benches, sinks, a fume hood and sample fridges - and SCP-061 on the east bench. The switch is by the door.',
            1, 0.62, ((0, 165, -900), (480, 120, 250)))


def room2b50chem():
    R = R_('room2b50chem', amb=30)
    B = shell(R, 'chem', -500, 500, CONC, luxel=20.0)
    for k, (z0, z1) in enumerate(((-900, -500), (-400, 0), (100, 500), (600, 900))):
        shelf_unit(R, -500, z0, -420, z1, 'west shelves %d' % k, h=250)
    for k, (z0, z1) in enumerate(((-900, -500), (100, 500))):
        shelf_unit(R, 420, z0, 500, z1, 'east shelves %d' % k, h=250)
    for k, z in enumerate((-360, -260, -160)):                                     # drums
        model30(R, 'Tank2.x', 440, 0, z, 0, (60, 110, 60), 'drum %d' % k)
    sbox(R, 400, 0, 640, 500, 120, 760, METAL, 'eyewash station')
    R.box(440, 120, 680, 460, 220, 700, METAL, lux=10)
    named(R, 'LEAK', 440, 200, -260)
    decal30(R, Mat('indev_b36warn.png', cast=False), 500, 0, 'W', 120, 150, 220, 'chem warning', uv=(0, 0, 0.5, 0.5))
    item(R, 'docb50_chem', 450, 120, 700)
    item(R, 'gasmask', -460, 100, -300, chance=50)
    for z in (-600, 0, 600):
        R.light(0, 320, z, rng=560, color=(255, 240, 210), power=104)
    B.clear = [((-110, 0, -1000, 110, 200, 1000), 'walkway')]
    check_b42(R)
    return (R, 'CHM', 'Chemical Storage (Light Containment): steel shelving, drums, the eyewash station and the pipes overhead.',
            1, 0.7, ((0, 165, -900), (440, 120, -260)))


def room2b50observe():
    """ref.: the observation pit - a gallery on the west with a window wall, the test chamber sunk below it"""
    R = R_('room2b50observe', amb=30)
    R.book = Book()
    B = R.book
    R.luxel = 22.0
    H = 420.0
    X0, X1, PX, PY = -400.0, 1000.0, 200.0, -260.0
    hall(R, X0, -1024, PX, 1024, 0, H, CONC.but(vs=H, v0=H), CFLOOR, DARK,
         holes={'N': [(-96, 96, 0, 320)], 'S': [(-96, 96, 0, 320)], 'E': [(-700, 700, 110, 300)]})
    B.areas.append((X0, PX, -1024, 1024, H, 0))
    for (z0, z1) in ((-1024, -990), (990, 1024)):
        for (a, b) in ((X0, -112), (112, PX)):
            R.box(a, 0, z0, b, H, z1, CONC.but(vs=H, v0=H), lux=40)
        R.box(-112, 320, z0, 112, H, z1, CONC, lux=10)
    # the window frames (open, the glass long gone), mullions every 280
    for z in range(-700, 701, 280):
        R.box(PX - 20, 110, z - 12, PX + 20, 300, z + 12, Mat('white.jpg', 32), lux=10)
    R.box(PX - 20, 100, -712, PX + 20, 110, 712, Mat('white.jpg', 32), lux=10)
    # the pit: walls from PY up to the gallery floor, the far wall full height, a red-lit window in the north wall
    hall(R, PX, -800, X1, 800, PY, H - PY, CONC.but(vs=H - PY, v0=H), CFLOOR, DARK, holes={'W': [(-700, 700, 110, 300)]})
    B.areas.append((PX, X1, -800, 800, H, PY))
    R.box(PX, PY, -800, PX + 24, 0, 800, CONC, lux=20)                                 # gallery edge, the pit side
    R.box(700, 40, 790, 900, 160, 800, DARK, lux=10)
    R.light(800, 100, 760, rng=420, color=(255, 70, 60), power=72)
    # steps down into the pit from the gallery's south end, along the south pit wall
    for i in range(7):
        top = -(i + 1) * (-PY / 7)
        R.box(PX + 24 + i * 50, PY, -800, PX + 24 + (i + 1) * 50, top, -700, CFLOOR, lux=10)
    R.box(PX - 20, 0, -790, PX + 24, 100, -700, CONC, lux=10)
    named(R, 'HOOKS', 720, PY, 200)
    # the gallery: chairs and a desk at the window, the observation log
    sbox(R, -360, 0, 300, -220, 78, 500, METAL, 'observation desk')
    chair(R, -170, 400, 270, 'observer chair')
    item(R, 'docb50_162', -300, 78, 360)
    item(R, 'docb50_observe', -280, 78, 450)
    console30(R, X0 + 46, -400, 'E', 'gallery console')
    for z in (-600, 0, 600):
        R.light(-100, H - 70, z, rng=520, color=(250, 245, 235), power=104)
    R.light(600, 200, 0, rng=600, color=(235, 240, 255), power=72)
    B.clear = [((-110, 0, -1000, 110, 200, 1000), 'walkway')]
    check_b42(R)
    return (R, 'OBS', 'Experimental Observation Room (Heavy Containment): a gallery with a window wall over a sunken test chamber. In the pit: SCP-162.',
            2, 0.45, ((-200, 165, 0), (700, -100, 200)))


def room2b50office():
    R = R_('room2b50office', amb=30)
    B = shell(R, 'office', -500, 500, WM, luxel=20.0)
    office_desk(R, -500, -760, -380, -580, 'E', 'desk 1', chair=(-345, -670))
    office_desk(R, -500, -200, -380, -20, 'E', 'desk 2', chair=(-345, -110))
    office_desk(R, 380, 300, 500, 480, 'W', 'desk 3', chair=(345, 390))
    cabinets(R, 400, -900, 500, -700, 'office cabinets')
    for z in (600, 680):
        cab(R, -460, z, 90, 'old cabinet %d' % z)
    decal30(R, BOARD, 500, -200, 'W', 360, 180, 200, 'office whiteboard')
    item(R, 'docb50_office', -440, 78, -680)
    item(R, 'docb50_incidents', 440, 78, 380)
    item(R, 'radio', -440, 78, -100, chance=40)
    for z in (-600, 0, 600):
        R.light(0, 320, z, rng=560, color=(255, 245, 225), power=108)
    B.clear = [((-110, 0, -1000, 110, 200, 1000), 'walkway')]
    check_b42(R)
    return (R, 'OFF', 'Researcher Office (Light Containment): three desks, cabinets and the whiteboard; the coffee went cold a long time ago.',
            1, 0.52, ((0, 165, -900), (-440, 100, -680)))


def room2b50specimen():
    R = R_('room2b50specimen', amb=30)
    B = shell(R, 'spec', -420, 420, CONC, luxel=20.0)
    for k, (z0, z1) in enumerate(((-900, -560), (-440, -100), (100, 440))):
        shelf_unit(R, 340, z0, 420, z1, 'jar shelves %d' % k, h=230)
    for k, (z0, z1) in enumerate(((-900, -620), (-500, -220))):
        sbox(R, -420, 0, z0, -320, 160, z1, WHITE, 'freezer %d' % k)
        R.box(-322, 120, z0 + 20, -318, 140, z0 + 60, DARK, lux=10)
    # SCP-020: the north-west corner, walls and floor gone dark and soft
    for (x0, z0, x1, z1) in ((-420, 520, -410, 990), (-420, 980, -40, 990)):
        R.box(x0, 0, z0, x1, 300, z1, MOLD, lux=10)
    R.rect_floor(-410, 560, -60, 980, 0.6, MOLD)
    named(R, 'MOLD', -250, 0, 800)
    item(R, 'docb50_020', 360, 140, -300)
    item(R, 'docb50_specimen', -360, 160, -400)
    for z in (-600, 0, 600):
        R.light(0, 320, z, rng=520, color=(230, 240, 255), power=94)
    B.clear = [((-110, 0, -1000, 110, 200, 1000), 'walkway')]
    check_b42(R)
    return (R, 'SPC', 'Small Specimen Storage (Heavy Containment): shelves of sealed jars and two freezers. Do not linger by the north-west corner - SCP-020.',
            2, 0.58, ((0, 165, -900), (-250, 100, 800)))


ALL = [room2b50lab02, room2b50chem, room2b50observe, room2b50office, room2b50specimen]
