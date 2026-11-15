"""The twenty-ninth batch: SCP-820-JP, SCP-867, SCP-120 and Lunar Area-32. Code in IndevU29.bb; textures from
make_assets29.py, the knife from make_scp820.py, the notes from make_docs29.py. SCP texts summarised from
scp-wiki.wikidot.com (CC BY-SA 3.0); rooms and art are our own.

  room2b29blade   HCZ  SCP-820-JP's inspection dock: a deep tank where an unmanned submarine circles without stopping
                       and surfaces at the dock for inspection (the knife is in its hatch); across the corridor the
                       "tourist" stall that grew round it - souvenirs, pennants, cookies, a pig mascot.
  room2b29spruce  HCZ  Bio-Containment Section E: a grove of four blood-red spruces (SCP-867) on soil under irrigation
                       pipes, a remote rover; across the corridor the NBC prep and herbicide decontamination room.
  room2b29pool    EZ   SCP-120's fortified outbuilding: the pink paddling pool on its dais under guard, and the
                       operators' room with the destination chart and the dial. High above (y 3072, sealed off - only
                       SCP-120 reaches it) is Lunar Area-32:
                         surface    SCP-120 Reception (destination point 9), the observatory with Earth over the
                                    mare, the cargo bay with the supply lander's airlock (the way home)
                         sub-level 1 (by lift)  the sealed SCP-001 vault, the SCP-L001 records terminal, the SCP-2219
                                    test room with its remote proxy, anomalous item storage"""
import os
from PIL import Image
from rooms_b28 import *

NEEDLE867 = Mat('indev_867needle.png', 96)
BARK867 = Mat('indev_867bark.png', 128)
SIGN867 = Mat('indev_867sign.png', cast=False)
DECON = Mat('indev_867decon.png', cast=False)
SOIL = Mat('indev_soil.png', 256)
PINK = Mat('indev_120pink.png', 128)
CHART = Mat('indev_120chart.png', cast=False)
SIGN120 = Mat('indev_120sign.png', cast=False)
REG = Mat('indev_regolith.png', 256)
LWALL = Mat('indev_lunarwall.png', 256)
VIEW = Mat('indev_earthview.png', cast=False)
LA32 = Mat('indev_la32sign.png', cast=False)
LEVELS = Mat('indev_la32levels.png', cast=False)
DOOR001 = Mat('indev_001door.png', cast=False)
L001 = Mat('indev_l001screen.png', cast=False)
LABEL2219 = Mat('indev_2219label.png', cast=False)
STALL = Mat('indev_820stall.png', cast=False)
PENNANT = Mat('indev_820pennant.png', alpha=True, cast=False)
WARN820 = Mat('indev_820warn.png', cast=False)
HATCH = Mat('containment_doors.jpg', 256)
TANKW = Mat('indev_820water.png', 128, alpha=True, cast=False)
CRATE = Mat('wood.jpg', 256)
SPACE = Mat('misc.jpg', 210)
STYLES['lunar29'] = (LWALL, CHECKER, Mat('white.jpg', 256))
Y = 3072.0          # Lunar Area-32, surface level
Y1 = Y - 640.0      # Sub-Level 1


def assets():
    im = Image.open(os.path.join(MAPDIR, 'indev_b21water.png')).convert('RGBA')
    im.putalpha(150)
    im.save(os.path.join(MAPDIR, 'indev_820water.png'))


assets()


# ------------------------------------------------------------------------------------------------ SCP-820-JP
def room2b29blade():
    R = R_('room2b29blade', amb=9)
    junction(R, 'NS', 'hcz', openings={'hubE': [door_op(0)], 'hubW': [door_op(0)]})
    for z in (-600.0, 600.0):
        ceil_light(R, 0, z, 384, size=40, power=55, rng=700)
    # east: the inspection dock. A raised tank 410 x 660, the water 120 up; the submarine (made by the code) circles
    side(R, 192, +1, 'hcz', h=352)
    x0, x1, z0, z1 = 340.0, 750.0, -330.0, 330.0
    for (a, b, c, d) in ((x0, z0, x1, z0 + 16), (x0, z1 - 16, x1, z1), (x0, z0, x0 + 16, z1), (x1 - 16, z0, x1, z1)):
        R.box(a, 0, b, c, 130, d, PANELS, top=CHECKER, lux=10)
    R.rect_floor(x0 + 16, z0 + 16, x1 - 16, z1 - 16, 2, DARK)
    R.rect_floor(x0 + 16, z0 + 16, x1 - 16, z1 - 16, 118, TANKW, coll=False)
    R.box(x0 - 60, 0, z0 - 50, x0, 30, z0 + 160, CHECKER, skip='B', lux=10)     # the step up to the dock
    R.box(560, 130, z0 - 4, 680, 136, z0 + 60, GRATE, lux=10)                     # the dock plate over the rim
    named(R, 'SUBC', 545, 60, 0)                                                   # the middle of the tank, under water
    named(R, 'DOCK', 620, 122, -230)                                               # where it surfaces
    wall_decal(R, WARN820, 776, 0, 'W', 150, 100, 230)
    R.box(300, 0, 340, 500, 80, 390, METAL, skip='B', top=PANELS, lux=10)          # the inspection bench
    R.box(320, 80, 350, 420, 104, 380, GLASS, lux=10)                              # an empty display case
    item(R, 'doc820jp', 450, 80, 360)
    red_lamp(R, 700, -360, 352, power=60, rng=500)
    ceil_light(R, 545, 0, 352, size=60, power=70, rng=720, color=(220, 236, 255))
    ceil_light(R, 360, 300, 352, size=30, power=40, rng=500)
    # west: the stall that grew. Counter, sign, pennants, cookie box, a pig mascot, a queue of rope posts
    side(R, -192, -1, 'lcz', h=352)
    R.box(-740, 0, -300, -600, 96, 300, WOOD, skip='B', top=WOOD, lux=10)          # the counter
    wall_decal(R, STALL, -776, 0, 'E', 360, 112, 250)
    for z, f in ((-400, 'N'), (400, 'S')):
        wall_decal(R, PENNANT, -516, z, f, 480, 80, 320)
    R.box(-700, 96, -60, -640, 126, 40, Mat('indev_2107poster.png', 64), lux=10)   # the cookie box
    named(R, 'COOKIES', -670, 120, -10)
    R.prism(octo(-420, 260, 46, 8), 0, 150, PINK, caps='T')                        # the pig mascot: body
    R.box(-450, 150, 230, -390, 220, 290, PINK, lux=10)                            # head
    R.box(-440, 170, 220, -400, 196, 232, Mat('indev_120pink.png', 32), lux=10)    # snout
    named(R, 'PIG', -420, 190, 230)
    for z in (-200, -60, 80):
        R.tube((-460, 0, z), (-460, 100, z), 5, METAL, sides=6, caps=True)        # queue posts
    R.box(-462, 84, -200, -458, 90, 80, Mat('indev_6483cloth.png', 64), lux=10)    # the rope
    ceil_light(R, -516, -150, 352, size=40, power=65, rng=600, color=(255, 236, 200))
    ceil_light(R, -516, 200, 352, size=40, power=55, rng=600, color=(255, 236, 200))
    return (R, 'BLD', 'SCP-820-JP inspection dock (Heavy Containment): an unmanned submarine circles a deep tank and surfaces for inspection; across the corridor, the souvenir stall that grew round the knife.',
            2, 0.5, ((300, 165, -300), (600, 80, 0)))


# ------------------------------------------------------------------------------------------------ SCP-867
def spruce867(R, x, z, h=330):
    R.tube((x, 0, z), (x, h * 0.35, z), 14, BARK867, sides=6, caps=False)
    for k in range(5):
        y0 = h * (0.18 + 0.16 * k)
        R.prism(octo(x, z, 135 * (1 - 0.18 * k), 8), y0, y0 + h * 0.17, NEEDLE867, caps='TB')
    R.tube((x, h * 0.98, z), (x, h * 1.08, z), 6, NEEDLE867, sides=5, caps=True)


TREES867 = ((430, -230), (660, -230), (430, 230), (660, 230))


def room2b29spruce():
    R = R_('room2b29spruce', amb=9)
    junction(R, 'NS', 'hcz', openings={'hubE': [door_op(0)], 'hubW': [door_op(0)]})
    for z in (-600.0, 600.0):
        ceil_light(R, 0, z, 384, size=40, power=55, rng=700)
    wall_decal(R, SIGN867, 192, -230, 'W', 200, 100, 250)
    # east: Section E - soil, the four trees, irrigation overhead, the rover parked by the door
    side(R, 192, +1, 'hcz', h=352)
    R.rect_floor(300, -390, 770, 390, 1.5, SOIL)
    for k, (x, z) in enumerate(TREES867):
        # the tree itself is the HD model GFX\map\props\scp867.b3d (make_hd29.py), placed by the code at this pivot;
        # the room keeps only a ring of mulch round its foot and an invisible collision ring round the trunk
        R.floor(octo(x, z, 70, 10), 2.5, Mat('indev_o_mud.png', 128))
        ring = octo(x, z, 34, 8)
        for i in range(8):
            R.collide_wall(ring[i], ring[(i + 1) % 8], 0, 300)
            R.collide_wall(ring[(i + 1) % 8], ring[i], 0, 300)
        named(R, 'T%d' % k, x, 40, z)
    for z in (-230, 230):
        R.tube((270, 320, z), (770, 320, z), 6, PIPES, sides=6, caps=True)
        for x in (430, 660):
            R.tube((x, 320, z), (x, 300, z), 4, METAL, sides=5, caps=True)        # the sprinkler heads
    R.box(290, 0, -60, 370, 40, 60, DARK, skip='B', lux=10)                       # the rover
    R.box(300, 40, -40, 360, 70, 40, METAL, skip='B', lux=10)
    R.tube((330, 70, 0), (330, 120, 0), 4, METAL, sides=5, caps=True)
    for zz in (-62, 62):
        for xx in (305, 355):
            R.tube((xx, 14, zz), (xx, 14, zz + (8 if zz > 0 else -8)), 14, DARK, sides=8, caps=True)
    named(R, 'ROVER', 330, 80, 0)
    ceil_light(R, 545, 0, 352, size=60, power=95, rng=800, color=(255, 236, 230))
    for z in (-330, 330):
        ceil_light(R, 545, z, 352, size=40, power=60, rng=600, color=(255, 240, 235))
    red_lamp(R, 740, 0, 352, power=40, rng=500)
    # west: NBC prep and decontamination - lockers, the herbicide shower stall, a quarantine bed
    side(R, -192, -1, 'hcz', h=352)
    for z in (-360, -280, -200):
        R.box(-776, 0, z, -720, 220, z + 72, CABINET, skip='B', lux=10)
    item(R, 'hazmatsuit', -700, 0, -280)
    R.box(-560, 0, 240, -540, 260, 390, PANELS2, lux=10)                          # the shower stall
    R.box(-776, 0, 230, -560, 6, 390, GRATE, lux=10)
    R.tube((-670, 280, 310), (-670, 250, 310), 14, METAL, sides=8, caps=True)
    wall_decal(R, DECON, -776, 310, 'E', 130, 130, 170)
    named(R, 'SHOWER', -670, 120, 310)
    R.box(-480, 0, -390, -300, 50, -300, METAL, skip='B', lux=10)                 # the quarantine bed
    R.box(-476, 50, -386, -304, 62, -304, WHITEP, skip='B', lux=10)
    R.box(-620, 0, -60, -520, 76, 60, METAL, skip='B', top=PANELS, lux=10)
    item(R, 'herbicide867', -580, 76, -20)
    item(R, 'herbicide867', -560, 76, 30)
    item(R, 'doc867', -600, 76, 20)
    ceil_light(R, -516, 0, 352, size=44, power=70, rng=700, color=(230, 255, 235))
    return (R, 'SPR', 'SCP-867 Bio-Containment Section E (Heavy Containment): four blood-red spruces under irrigation, and the NBC prep and herbicide decontamination room.',
            2, 0.6, ((290, 175, 0), (760, 150, 0)))


# ------------------------------------------------------------------------------------------------ SCP-120 + Lunar Area-32
def hall(R, x0, z0, x1, z1, y, h, wall, floor, ceil, holes=None):
    """a hall at height y; holes per side {'W','N','E','S'}: [(c0, c1)] doorways (192 x 320) or (c0, c1, y0, y1)"""
    pts = [(x0, z0), (x0, z1), (x1, z1), (x1, z0)]
    hh = {}
    for side_, seg, conv in (('W', 0, lambda c: c - z0), ('N', 1, lambda c: c - x0), ('E', 2, lambda c: z1 - c),
                             ('S', 3, lambda c: x1 - c)):
        for hole in (holes or {}).get(side_, ()):
            c0, c1 = hole[0], hole[1]
            hy0, hy1 = (hole[2], hole[3]) if len(hole) > 2 else (y, y + 320)
            s0, s1 = sorted((conv(c0), conv(c1)))
            hh.setdefault(seg, []).append((s0, s1, hy0, hy1))
    R.walls(pts, y, y + h, wall, holes=hh)
    R.rect_floor(x0, z0, x1, z1, y, floor)
    R.rect_ceil(x0, z0, x1, z1, y + h, ceil)


def shelves(R, x0, z0, x1, z1, y, h=230, n=4):
    R.box(x0, y, z0, x1, y + h, z0 + 8, WHITEP, lux=10)
    R.box(x0, y, z1 - 8, x1, y + h, z1, WHITEP, lux=10)
    for k in range(n + 1):
        yy = y + 10 + k * (h - 20) / n
        R.box(x0, yy, z0 + 8, x1, yy + 5, z1 - 8, DARK, lux=10)
        if 0 < k < n:
            R.box(x0 + 10, yy + 5, z0 + 20, x1 - 10, yy + 40, z0 + 60, CRATE, lux=10)


def doorway(c):
    return (c - 96, c + 96)


def room2b29pool():
    R = Room('room2b29pool', luxel=8.0, ambient=11, fill=0.15)
    junction(R, 'NS', 'ez', openings={'hubE': [door_op(0)], 'hubW': [door_op(0)]})
    for z in (-600.0, 600.0):
        ceil_light(R, 0, z, 384, size=40, power=55, rng=700)
    wall_decal(R, SIGN120, 192, -230, 'W', 200, 100, 250)
    # ---- east: the fortified outbuilding - the pool on a dais under guard
    side(R, 192, +1, 'hcz', h=352)
    R.prism(octo(520, 0, 250, 16), 0, 12, CHECKER, caps='T')                      # the dais
    ring = octo(520, 0, 205, 20)
    for i in range(len(ring)):                                                     # the inflatable rings
        a, b = ring[i], ring[(i + 1) % len(ring)]
        R.tube((a[0], 30, a[1]), (b[0], 30, b[1]), 20, PINK, sides=8, caps=True)
        R.tube((a[0], 62, a[1]), (b[0], 62, b[1]), 16, PINK, sides=8, caps=True)
    R.floor(octo(520, 0, 200, 20), 13, PINK)
    named(R, 'POOL', 520, 40, 0)
    named(R, 'RETURN', 330, 30, -300)
    R.box(640, 0, 300, 770, 90, 390, METAL, skip='B', top=PANELS, lux=10)          # the guard post
    chair(R, 700, 270, 'S')
    wall_decal(R, WMON, 776, 340, 'W', 90, 90, 190)
    R.box(760, 300, -380, 776, 330, -350, DARK, lux=10)                            # the camera's bracket
    for x in (330, 710):
        for z in (-380, 380):
            R.box(x - 20, 0, z - 20, x + 20, 352, z + 20, CONC, skip='B', lux=10)  # blast pillars
    ceil_light(R, 520, 0, 352, size=70, power=70, rng=760, color=(255, 236, 246))
    ceil_light(R, 700, 330, 352, size=30, power=40, rng=500)
    # ---- west: the operators' room - the chart, the dial, monitors
    side(R, -192, -1, 'ez', h=352)
    R.box(-776, 0, -300, -660, 90, 300, DARK, skip='B', top=CTRL, lux=10)          # the console
    wall_decal(R, CHART, -776, -150, 'E', 150, 188, 210)
    named(R, 'CHART', -760, 210, -150)
    named(R, 'DIAL', -700, 110, 100)
    for z in (100, 260):
        wall_decal(R, WMON, -776, z, 'E', 100, 100, 210)
    chair(R, -600, 100, 'W')
    item(R, 'doc120', -700, 90, -250)
    item(R, 'doc120_22', -700, 90, 200)
    ceil_light(R, -516, 0, 352, size=44, power=65, rng=700)

    # ================= Lunar Area-32 - surface level (y = Y)
    # SCP-120 Reception: x -400..240, z -440..440. West: the lift; north: the observatory; east: the cargo bay
    hall(R, -400, -440, 240, 440, Y, 448, LWALL, CHECKER, WHITEP,
         holes={'W': [doorway(0)], 'N': [doorway(-80)], 'E': [doorway(0)]})
    R.floor(octo(-80, 0, 150, 16), Y + 1, Mat('indev_o_stripes.png', 64))         # destination point 9
    R.floor(octo(-80, 0, 120, 16), Y + 1.5, Mat('metal3.jpg', 205))
    named(R, 'ARRIVE', -80, Y + 30, 0)
    wall_decal(R, LA32, -80, -440, 'N', 320, 160, Y + 280)
    wall_decal(R, LEVELS, -400, 260, 'E', 120, 160, Y + 190)
    R.box(80, Y, -420, 220, Y + 90, -300, METAL, skip='B', top=PANELS, lux=10)    # the reception desk
    item(R, 'docla32', 150, Y + 90, -360)
    for z in (-300, 300):
        ceil_light(R, -80, z, Y + 448, size=60, power=70, rng=820, color=(235, 242, 255))
    ceil_light(R, -80, 0, Y + 448, size=50, power=60, rng=700, color=(220, 225, 240))
    lift(R, -400, -1, 0, Y, 0, Y1, LWALL)
    # the observatory: x -1008..240, z 440..800, a long window north onto the mare
    hall(R, -1008, 440, 240, 800, Y, 384, LWALL, CARPET, WHITEP,
         holes={'S': [doorway(-80)], 'N': [(-900, 100, Y + 60, Y + 330)]})
    R.decal((-900, 800), (100, 800), Y + 60, Y + 330, GLASS, (0, 0, 4, 1), off=0.5)
    R.box(-900, Y, 760, 100, Y + 60, 800, LWALL, skip='B', top=PANELS, lux=10)     # the sill
    for x in (-600, -300):
        chair(R, x, 700, 'N', Y)
    R.box(-160, Y, 650, 0, Y + 120, 720, METAL, skip='B', lux=10)                  # the telescope's pier
    R.tube((-80, Y + 120, 685), (-60, Y + 200, 740), 16, DARK, sides=8, caps=True)
    named(R, 'OBS', -400, Y + 200, 790)
    ceil_light(R, -400, 600, Y + 384, size=40, power=35, rng=700, color=(200, 210, 255))
    # outside: the regolith, a few rocks, the black sky and Earth on the backdrop
    R.rect_floor(-1008, 800, 240, 1008, Y - 30, REG)
    R.decal((-1008, 1008), (240, 1008), Y - 30, Y + 440, VIEW, (0, 0, 1, 1), off=0)
    R.decal((-1008, 1008), (240, 1008), Y + 440, Y + 700, SPACE, (0, 0, 1, 1), off=0)
    R.decal((240, 1008), (240, 800), Y - 30, Y + 700, SPACE, (0, 0, 1, 1), off=0)
    R.decal((-1008, 800), (-1008, 1008), Y - 30, Y + 700, SPACE, (0, 0, 1, 1), off=0)
    R.rect_ceil(-1008, 800, 240, 1008, Y + 700, SPACE)
    for (x, z, s) in ((-700, 900, 40), (-200, 960, 60), (60, 880, 28)):
        R.prism(octo(x, z, s, 5), Y - 30, Y - 30 + s * 0.6, REG, caps='T')
    R.light(-300, Y + 650, 950, rng=1100, color=(255, 255, 250), power=110)        # the sun on the plain
    R.light(-700, Y + 300, 900, rng=700, color=(230, 235, 255), power=50)
    # the cargo bay: x 240..1008, z -1008..1008, 640 high. The lander's airlock east, freight lift south
    hall(R, 240, -1008, 1008, 1008, Y, 640, LWALL, CHECKER, Mat('metal.jpg', 256), holes={'W': [doorway(0)]})
    wall_decal(R, HATCH, 1008, 500, 'W', 260, 300, Y + 160)
    named(R, 'LANDER', 990, Y + 150, 500)
    wall_decal(R, HATCH, 620, -1008, 'N', 320, 320, Y + 170)
    named(R, 'FREIGHT', 620, Y + 150, -990)
    R.box(380, Y, -400, 384, Y + 1, 400, Mat('indev_o_stripes.png', 64), lux=10)   # the quarantine line
    for (x, z, n) in ((520, 700, 3), (760, 760, 2), (820, -700, 3), (480, -760, 2)):
        for k in range(n):
            R.box(x - 60, Y + k * 100, z - 60, x + 60, Y + (k + 1) * 100, z + 60, CRATE, lux=10)
    R.box(600, Y, -300, 900, Y + 240, -100, PANELS2, lux=10)                       # a cargo container
    R.box(600, Y, 150, 900, Y + 240, 350, PANELS2, lux=10)
    for (x, z) in ((620, -600), (620, 0), (620, 600)):
        ceil_light(R, x, z, Y + 640, size=80, power=80, rng=1000, color=(240, 245, 255))
    # ================= Sub-Level 1 (y = Y1), by the lift
    hall(R, -400, -160, 800, 160, Y1, 352, LWALL, CHECKER, WHITEP,
         holes={'W': [doorway(0)], 'N': [doorway(520)], 'S': [doorway(-80), doorway(520)]})
    wall_decal(R, LEVELS, -300, 160, 'S', 100, 130, Y1 + 200)
    # the SCP-001 vault door, north wall, sealed
    R.tube((-80, Y1 + 150, 158), (-80, Y1 + 150, 140), 130, METAL, sides=20, caps=True)
    R.decal((-170, 139), (10, 139), Y1 + 60, Y1 + 240, DOOR001, (0, 0, 1, 1), off=0.3)
    named(R, 'VAULT', -80, Y1 + 150, 140)
    # the jurisdiction registry (the facility dossier's list), on the south wall between the two doorways
    wall_decal(R, Mat('indev_la32registry.png', cast=False), 220, -160, 'N', 200, 250, Y1 + 175)
    named(R, 'REGISTRY', 220, Y1 + 175, -150)
    for x in (100, 300, 700):
        ceil_light(R, x, 0, Y1 + 352, size=44, power=60, rng=700, color=(235, 242, 255))
    ceil_light(R, -250, 0, Y1 + 352, size=44, power=55, rng=600, color=(235, 242, 255))
    # SCP-L001 records, north: x 280..760, z 160..700
    hall(R, 280, 160, 760, 700, Y1, 320, LWALL, CARPET, WHITEP, holes={'S': [doorway(520)]})
    R.box(560, Y1, 600, 740, Y1 + 80, 690, DARK, skip='B', top=PANELS, lux=10)
    wall_decal(R, L001, 650, 700, 'S', 180, 135, Y1 + 170)
    named(R, 'TERM', 650, Y1 + 150, 680)
    for x in range(300, 520, 70):
        R.box(x, Y1, 620, x + 60, Y1 + 200, 700, CABINET, skip='B', lux=10)
    ceil_light(R, 520, 430, Y1 + 320, size=40, power=55, rng=600, color=(200, 255, 210))
    # SCP-2219, south-west: x -360..200, z -700..-160. The locker, the remote proxy console
    hall(R, -360, -700, 200, -160, Y1, 320, LWALL, CHECKER, WHITEP, holes={'N': [doorway(-80)]})
    R.box(-340, Y1, -690, -240, Y1 + 230, -600, CABINET, skip='B', lux=10)
    wall_decal(R, LABEL2219, -290, -600, 'N', 60, 60, Y1 + 150)
    named(R, 'LOCKER', -290, Y1 + 140, -590)
    R.box(-20, Y1, -690, 180, Y1 + 90, -600, DARK, skip='B', top=CTRL, lux=10)
    wall_decal(R, WMON, 80, -700, 'N', 120, 100, Y1 + 190)
    named(R, 'PROXY', 80, Y1 + 120, -600)
    chair(R, 80, -540, 'S', Y1)
    item(R, 'doc2219', 140, Y1 + 90, -640)
    ceil_light(R, -80, -430, Y1 + 320, size=44, power=60, rng=640)
    # anomalous item storage, south-east: x 280..760, z -700..-160
    hall(R, 280, -700, 760, -160, Y1, 320, LWALL, CHECKER, WHITEP, holes={'N': [doorway(520)]})
    for (a, b, c, d) in ((690, -660, 750, -480), (690, -400, 750, -220), (300, -660, 360, -480)):
        shelves(R, a, b, c, d, Y1)
    item(R, 'firstaid', 720, Y1 + 10, -560)
    ceil_light(R, 520, -430, Y1 + 320, size=44, power=60, rng=640)
    return (R, 'POL', 'SCP-120 outbuilding (Entrance Zone): the pink paddling pool under guard and the operators\' dial room. Its ninth destination - Lunar Area-32 on Mare Imbrium - is built into the same room, far above.',
            3, 0.55, ((300, 165, -300), (520, 40, 0)))


ALL = [room2b29blade, room2b29spruce, room2b29pool]
