"""The forty-fifth batch (code in IndevU45.bb): the old SCP-939 containment chamber (after the user's two editor
screenshots), the Morgue and the Off-Shoot Hall (from the community suggestions), and the damaged wing (after
the user's three sketches).

  room2b47old939     HCZ  a white gallery corridor with three open observation windows over a deep, dark pit -
                          ribbed panels, a rust band, a red-lit hatch in the far wall, a ladder no one uses;
                          the audio-monitoring office and an old store off the corridor
  room2b47morgue     LCZ  the records office and the scrub room; through the Level 4 door the morgue: a wall of
                          cold-storage drawers, sheeted gurneys, two autopsy tables - one with someone still
                          strapped to it - and the operating lamp
  room3b47offshoot   LCZ  3-way  the Off-Shoot Hall: a T of halls so dark you see a few metres, holes in the
                          floor, and a jammed door with flames licking out of its seam
  room2b47damaged    HCZ  ref. sketch 1: a corner room with a rubble pile under a cracked window; sketch 3: a small
                          room with a fallen monitor and a smashed window; sketch 2: the east hall where the
                          ceiling came down - a turbine housing through two floors, rubble and slabs below the hole
"""
from rooms_b44 import *

DRAWERS = Mat('indev_b45drawers.png', cast=False)
CRACK = Mat('indev_b45crack.png', alpha=True, cast=False)
FLAME = Mat('indev_b45flame.png', alpha=True, cast=False, emit=200)
HOLE = Mat('indev_b45hole.png', alpha=True, cast=False)
PANEL45 = Mat('indev_b45panel.png', 384)
RUST = Mat('indev_b33shade.png', 64)


def rubble(R, x, z, n, spread, hmax, name, seed):
    rnd = random.Random(seed)
    for k in range(n):
        px, pz = x + rnd.uniform(-spread, spread), z + rnd.uniform(-spread, spread)
        r = rnd.uniform(14, 40)
        R.prism(octo(px, pz, r, rnd.choice((5, 6, 7))), 0, rnd.uniform(10, hmax), CONC36, caps='T')
    solid(R, (x - spread - 40, 0, z - spread - 40, x + spread + 40, hmax, z + spread + 40), name)


# ------------------------------------------------------------------------------------------------ the old 939 chamber
def room2b47old939():
    PIT = -420.0
    R, rooms = wing33('room2b47old939', 'lcz', {('W', -400): {'style': 'lcz'}, ('W', 400): {'style': 'lcz'}},
                      extra=[('E', -450), ('E', 0), ('E', 450)], amb=9)
    R.luxel = 16.0
    B = R.book
    WM, FM, CM = STYLES['lcz']
    hub_dress(R, 'lcz', [], pipes=False)
    # the windows: a short reveal through the wall and a waist-high parapet
    for c in (-450, 0, 450):
        hall(R, 192, c - 96, 256, c + 96, 0, 320, WM.but(vs=320, v0=320), FM, CM,
             holes={'W': [(c - 96, c + 96, 0, 320)], 'E': [(c - 96, c + 96, 0, 320)]})
        sbox(R, 192, 0, c - 96, 256, 110, c + 96, WM, 'parapet %d' % c)
        R.box(188, 110, c - 100, 260, 118, c + 100, METAL, lux=10)
    # the pit
    H = 330 - PIT
    hall(R, 256, -750, 1000, 750, PIT, H, PANEL45.but(vs=H, v0=330), Mat('concretefloor.jpg', 256), DARK,
         holes={'W': [(c - 96, c + 96, 0, 320) for c in (-450, 0, 450)]})
    B.areas.append((256, 1000, -750, 750, 330, PIT))
    for (x0, z0, x1, z1) in ((256, -750, 320, 750), (940, -750, 1000, 750), (320, -750, 940, -690), (320, 690, 940, 750)):
        sbox(R, x0, PIT + 300, z0, x1, PIT + 340, z1, Mat('indev_b45panel.png', 64), 'rust ledge %d %d' % (x0, z0))
    # the red-lit hatch in the far wall
    R.box(990, PIT, 220, 1000, PIT + 280, 380, Mat('red.jpg', 64, emit=120), lux=10)
    for (z0, z1) in ((200, 220), (380, 400)):
        R.box(980, PIT, z0, 1000, PIT + 300, z1, DARK, lux=10)
    R.box(980, PIT + 280, 200, 1000, PIT + 300, 400, DARK, lux=10)
    R.light(940, PIT + 160, 300, rng=520, color=(255, 50, 40), power=50)
    named(R, 'HATCH', 990, PIT + 140, 300)
    for dz in (-20, 20):                                                       # the ladder
        R.tube((990, PIT, -600 + dz), (990, PIT + 300, -600 + dz), 3, METAL, sides=6, caps=True)
    for y in range(int(PIT) + 30, int(PIT) + 300, 40):
        R.tube((990, y, -620), (990, y, -580), 2, METAL, sides=6, caps=False)
    # the pit floor: a drain, scattered bones, old blood
    R.prism(octo(630, 0, 40, 12), PIT, PIT + 1, DARK, caps='T')
    rnd = random.Random(939)
    for k in range(14):
        x, z = rnd.uniform(400, 900), rnd.uniform(-600, 600)
        R.box(x, PIT, z, x + rnd.uniform(16, 40), PIT + 4, z + 6, WHITE, lux=10)
    R.rect_floor(450, -300, 800, 200, PIT + 0.8, BLOOD)
    named(R, 'PIT', 630, PIT, 0)
    R.light(630, PIT + 200, -300, rng=600, color=(150, 140, 130), power=16)
    # W -400: audio monitoring - consoles, headphones, the reel-to-reel
    for z in (-596, -400):
        console30(R, -730, z, 'E', 'audio console %d' % z)
    sbox(R, -560, 0, -260, -440, 90, -160, METAL, 'reel to reel')
    R.prism(octo(-530, -210, 26, 10), 90, 96, DARK, caps='T')
    R.prism(octo(-470, -210, 26, 10), 90, 96, DARK, caps='T')
    named(R, 'REELS', -500, 100, -210)
    item(R, 'docb45_939', -480, 0, -560)
    red_pendant(R, -516, -400, 352, drop=60, power=40, rng=500)
    # W 400: the old store
    for k, z in enumerate((220, 400, 580)):
        sbox(R, -776, 0, z - 60, -680, 90, z + 60, CRATE35, 'old crate %d' % k)
    ceiling_fixture(R, -516, 400, 352, power=30, rng=500)
    for z in (-700, 0, 700):
        ceiling_fixture(R, 0, z, 384, power=56, rng=620)
    B.clear = [((-110, 0, -1000, 110, 200, 1000), 'gallery')]
    check_b42(R)
    return (R, 'O39', 'The old SCP-939 chamber (Heavy Containment): a white gallery corridor with open windows over a deep dark pit, a red-lit hatch in its far wall; the audio-monitoring office and an old store.',
            2, 0.5, ((100, 165, -450), (630, -420, 0)))


# ------------------------------------------------------------------------------------------------ the morgue
def room2b47morgue():
    R, rooms = wing33('room2b47morgue', 'lcz', {('W', -400): {'style': 'lcz'}, ('W', 400): {'style': 'cell30'}}, extra=[('E', 0)], amb=10)
    R.luxel = 16.0
    B = R.book
    hd_hub(R, 'lcz', sign_w=6)
    # W -400: records office
    office_desk(R, -700, -660, -580, -540, 'E', 'records desk', chair=(-545, -600))
    cabinets(R, -500, -690, -300, -650, 'records cabinets')
    item(R, 'docb45_morgue', -640, 76, -560)
    item(R, 'key4', -620, 76, -600, chance=35)
    pendant(R, -516, -400, 352, drop=60, power=40, rng=500)
    # W 400: the scrub room - basins, gowns, a drain
    for z in (220, 360, 500):
        sbox(R, -776, 70, z - 50, -700, 96, z + 50, WHITE, 'scrub basin %d' % z)
    R.prism(octo(-516, 400, 30, 10), 0, 1, DARK, caps='T')
    lockers(R, 'z', 680, -1, -700, -400)
    solid(R, (-700, 0, 650, -400, 300, 680), 'gown lockers')
    cell_light(R, -516, 400, 352)
    # E: the morgue
    passage(R, 4, mat=Mat('white.jpg', 256).but(vs=320, v0=320))
    hall(R, 256, -1000, 1000, 1000, 0, 400, Mat('indev_b33tile.png', 128).but(vs=400, v0=400), TILE96, WHITE,
         holes={'W': [(-96, 96, 0, 320)]})
    B.areas.append((256, 1000, -1000, 1000, 400, 0))
    sbox(R, 940, 0, -900, 1000, 300, 900, Mat('dirtymetal.jpg', 64), 'drawer wall')
    for z in (-600, 0, 600):
        decal30(R, DRAWERS, 940, z, 'W', 300, 300, 150, 'drawers %d' % z)
    named(R, 'DRAWERS', 930, 120, 300)
    for k, (x, z) in enumerate(((360, -800), (520, -800), (680, -800), (360, 800), (520, 800))):
        R.box(x - 40, 60, z - 90, x + 40, 70, z + 90, METAL, lux=10)
        for dx in (-34, 34):
            for dz in (-80, 80):
                R.tube((x + dx, 0, z + dz), (x + dx, 60, z + dz), 2.5, METAL, sides=6, caps=False)
        sbox(R, x - 34, 70, z - 84, x + 34, 96, z + 84, SHEET, 'sheeted body %d' % k)
        solid(R, (x - 40, 0, z - 90, x + 40, 70, z + 90), 'gurney %d' % k)
    for k, z in enumerate((-260, 260)):
        sbox(R, 560, 0, z - 110, 700, 90, z + 110, METAL, 'autopsy table %d' % (k + 1))
        R.prism(octo(630, z + 90, 10, 8), 90, 91, DARK, caps='T')
    # table 2: the one who was still alive
    R.box(590, 90, 170, 670, 110, 350, Mat('indev_b39mummy.png', 32), lux=10)
    for z in (200, 260, 320):
        R.box(584, 90, z, 676, 114, z + 10, DARK, lux=10)
    R.rect_floor(520, 120, 760, 420, 0.8, BLOOD)
    R.rect_floor(586, 166, 674, 354, 90.6, BLOOD)
    named(R, 'TABLE2', 630, 110, 260)
    sbox(R, 760, 0, 180, 820, 90, 240, METAL, 'instrument cart')
    R.prism(octo(630, 0, 80, 12), 360, 380, METAL, caps='TB')
    R.light(630, 330, 0, rng=600, color=(240, 250, 255), power=70)
    named(R, 'SPAWN106', 860, 0, -500)
    item(R, 'syringe', 790, 90, 210, chance=70)
    item(R, 'firstaid', 790, 90, 220, chance=50)
    for z in (-700, 700):
        ceiling_fixture(R, 630, z, 400, power=46, rng=600)
    check33(R)
    return (R, 'MRG', 'The Morgue (Light Containment): the records office and scrub room; behind the Level 4 door a wall of cold-storage drawers, sheeted gurneys, and two autopsy tables - one with someone still strapped to it.',
            1, 0.5, ((300, 165, -600), (630, 100, 260)))


# ------------------------------------------------------------------------------------------------ the off-shoot hall (3-way)
def room3b47offshoot():
    R = R_('room3b47offshoot', amb=2)
    R.book = Book()
    B = R.book
    R.luxel = 18.0
    junction(R, 'SEW', 'lcz', hub=(-192, -192, 192, 192))
    B.areas.append((-1024, 1024, -192, 192, 384))
    B.areas.append((-192, 192, -1024, 192, 384))
    # the holes: two sets; which set is real is decided each game (IndevU45.bb)
    for (x, z, tag) in ((-600, 40, 'A1'), (40, -620, 'A2'), (560, -40, 'B1'), (-40, -380, 'B2')):
        R.rect_floor(x - 80, z - 80, x + 80, z + 80, 0.6, HOLE)
        named(R, 'HOLE' + tag, x, 0, z)
    # the jammed door on the north wall of the west hall, flames at its seam
    R.box(-700, 0, 184, -500, 330, 192, DARK, lux=10)
    R.box(-690, 0, 180, -510, 310, 186, Mat('dirtymetal.jpg', 128), lux=10)
    decal30(R, FLAME, -600, 180, 'S', 180, 60, 30, 'flames low')
    decal30(R, FLAME, -600, 179, 'S', 30, 300, 160, 'flames seam')
    R.light(-600, 60, 140, rng=420, color=(255, 140, 50), power=40)
    named(R, 'FIREDOOR', -600, 120, 170)
    # one weak red lamp at the junction, nothing else
    R.light(0, 300, 0, rng=360, color=(255, 60, 50), power=14)
    named(R, 'SPAWN106', 0, 0, -800)
    item(R, 'docb45_offshoot', 120, 0, 120)
    B.clear = []
    check_b42(R)
    return (R, 'OFS', 'The Off-Shoot Hall (Light Containment, T-junction): three halls so dark you can barely see, holes in the floor, and a jammed door with flames licking from its seam.',
            1, 0.5, ((0, 165, -700), (0, 150, 0)), 3)


# ------------------------------------------------------------------------------------------------ the damaged wing
def room2b47damaged():
    R, rooms = wing33('room2b47damaged', 'conc36', {('W', -400): {'style': 'conc36'}, ('W', 400): {'style': 'conc36'}}, extra=[('E', 0)], amb=7)
    R.luxel = 16.0
    B = R.book
    hd_hub(R, 'conc36', sign_w=6)
    for (x, z) in ((-120, -600), (90, 500)):
        R.rect_floor(x - 60, z - 60, x + 60, z + 60, 0.6, Mat('indev_b36grime.png', 128, alpha=True))
    # W -400 (sketch 1): a rubble pile in the corner, a cracked window high on the wall
    rubble(R, -680, -610, 14, 46, 110, 'corner rubble', 1)
    decal30(R, GWIN, -776, -380, 'E', 220, 110, 230, 'window W1')
    decal30(R, CRACK, -771, -360, 'E', 220, 110, 232, 'crack W1')
    for (x, z) in ((-520, -300), (-600, -200)):
        R.box(x, 0.8, z, x + 26, 1.4, z + 34, WHITE, lux=10)
    R.light(-500, 300, -400, rng=420, color=(255, 230, 200), power=24)
    # W 400 (sketch 3): a small room - the monitor fallen off the desk, the window smashed
    table30(R, -700, 520, -560, 640, 'monitor desk')
    R.box(-620, 0, 440, -560, 40, 500, DARK, lux=10)                                # the fallen monitor
    solid(R, (-620, 0, 440, -560, 40, 500), 'fallen monitor')
    decal30(R, GWIN, -776, 300, 'E', 200, 110, 200, 'window W2')
    decal30(R, CRACK, -771, 300, 'E', 200, 110, 202, 'crack W2')
    rubble(R, -480, 250, 6, 30, 50, 'window debris', 3)
    R.light(-500, 300, 400, rng=420, color=(255, 230, 200), power=24)
    # E (sketch 2): the collapsed hall
    passage(R, 0)
    H = 400.0
    R.walls([(256, -1000), (256, 1000), (1000, 1000), (1000, -1000)], 0, H, CONC36.but(vs=H, v0=H), holes={0: [(904, 1096, 0, 320)]})
    R.rect_floor(256, -1000, 1000, 1000, 0, FLOOR36)
    for (x0, z0, x1, z1) in ((256, -1000, 1000, -220), (256, 220, 1000, 1000), (256, -220, 480, 220), (820, -220, 1000, 220)):
        R.rect_ceil(x0, z0, x1, z1, H, DARK)
    R.walls([(480, -220), (480, 220), (820, 220), (820, -220)][::-1], H, H + 400, CONC36.but(vs=400, v0=H + 400))
    R.rect_ceil(480, -220, 820, 220, H + 400, DARK)
    B.areas.append((256, 1000, -1000, 1000, H, 0))
    R.tube((500, 90, -150), (790, 70, 150), 80, Mat('dirtymetal.jpg', 128), sides=12, caps=True)   # the turbine housing
    solid(R, (420, 0, -230, 870, 170, 230), 'turbine')
    decal30(R, VAULTD, 720, -230, 'S', 160, 160, 120, 'fallen wheel')
    rubble(R, 640, -360, 10, 70, 90, 'rubble S', 5)
    rubble(R, 650, 360, 10, 70, 90, 'rubble N', 6)
    for k, (x, z) in enumerate(((380, -600), (860, 500), (330, 650))):
        sbox(R, x, 0, z, x + 120, 24, z + 70, CONC36, 'ceiling slab %d' % k)
    named(R, 'COLLAPSE', 650, 0, 0)
    item(R, 'docb45_collapse', 340, 24, 690)
    R.light(650, H + 300, 0, rng=900, color=(200, 210, 230), power=50)
    for z in (-700, 700):
        ceiling_fixture(R, 620, z, H, power=36, rng=520)
    red_emergency(R, 1000, 300, -500, 'W', 'red collapse', power=30)
    B.clear = [((300, 0, -100, 400, 200, 100), 'entrance')]
    check33(R)
    return (R, 'DMG', 'The Damaged Wing (Heavy Containment): rubble in the corner rooms under cracked windows, and the east hall where the ceiling came down - a turbine housing through two floors.',
            2, 0.5, ((300, 165, -700), (650, 200, 0)))


ALL = [room2b47old939, room2b47morgue, room3b47offshoot, room2b47damaged]
