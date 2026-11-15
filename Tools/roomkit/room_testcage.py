"""room1testcage - "Test Chamber 4-A" / SCP-131 (Indev zone, dead end: door on -z).
Reference shots (second set) 14, 12, 13, 16: a white tiled chamber with a wire cage in the corner
(a table inside it), a flight of steps with a handrail up to a raised control office that looks
down through a window, and in the office a console wall with monitors, a lever and an SCP plate."""
from parts import *

CTRL = Mat('controlpanel.jpg', 256, cast=False)
LOGO = Mat('scplogo.jpg', 256, cast=False)
WHITE = Mat('white.jpg', 256)
UP = 192.0
H = 512.0


def build():
    R = Room('room1testcage', luxel=10, ambient=13, fill=0.15)
    A = {}
    W = LCZWALL.but(v0=512, vs=512, us=512)

    # ---- entry neck
    R.rect_floor(-192, -992, 192, -736, 0, TILE)
    R.rect_ceil(-192, -992, 192, -736, 384, WHITE)
    R.wall((-192, -992), (-192, -736), 0, 384, W)
    R.wall((192, -736), (192, -992), 0, 384, W)
    end_wall(R, 'S', -192, 192, 384, W, TILE)

    # ---- the chamber
    out = [(-640, -736), (-640, 640), (640, 640), (640, -736)]
    R.walls(out, 0, H, W, holes={
        2: [span(out[2], (640, -240), (640, -400)) + (320, 480)],            # fan duct, east wall
        3: [span(out[3], (192, -736), (-192, -736)) + (0, 384)]})
    R.rect_floor(-640, -736, 640, 640, 0, TILE)
    R.rect_ceil(-640, -736, 640, 640, H, DIRTY)
    for z in (-480, -160, 160, 480):                                           # ceiling ribs
        R.box(-640, H - 28, z - 14, 640, H, z + 14, DARK, skip='T', lux=14)

    # ---- the office block in the north-west corner (floor at 192), seen from the chamber
    a = (-640, 128)
    R.wall(a, (-64, 128), 0, H, W, holes=[span(a, (-560, 128), (-240, 128)) + (UP + 80, UP + 208)])
    a = (-64, 128)
    R.wall(a, (-64, 640), 0, H, W, holes=[span(a, (-64, 320), (-64, 512)) + (UP, H)])
    # inside the office
    a = (-96, 640)
    R.wall(a, (-96, 160), UP, H, W, holes=[span(a, (-96, 512), (-96, 320)) + (UP, H)])
    a = (-96, 160)
    R.wall(a, (-640, 160), UP, H, W, holes=[span(a, (-240, 160), (-560, 160)) + (UP + 80, UP + 208)])
    R.rect_floor(-640, 160, -96, 640, UP, TILE)
    # doorway through the east wall of the office
    R.rect_floor(-96, 320, -64, 512, UP, TILE)
    R.wall((-64, 320), (-96, 320), UP, H, W)
    R.wall((-96, 512), (-64, 512), UP, H, W)
    # the window
    R.rect_floor(-560, 128, -240, 160, UP + 80, DARK)
    R.rect_ceil(-560, 128, -240, 160, UP + 208, DARK)
    R.wall((-560, 128), (-560, 160), UP + 80, UP + 208, DARK)
    R.wall((-240, 160), (-240, 128), UP + 80, UP + 208, DARK)
    R.quad(V(-560, UP + 80, 144), V(-240, UP + 80, 144), V(-240, UP + 208, 144), V(-560, UP + 208, 144), GLASS,
           uvrect=(0, 0, 1.25, 0.5), lm=False)

    # ---- steps up the east side of the block, landing in front of the office doorway
    zt, yt = stairs(R, -64, 128, -256, 12, 16.0, 32.0, +1, 0, WHITE, top=TILE)
    R.box(-64, 0, 128, 128, UP, 640, WHITE, skip='BWN', top=TILE)
    railing(R, (128, 128), (128, 640), UP)
    # handrail down the open side of the steps
    ay = norm(V(0, 384, -192)) * 4
    R.obox(V(128, 96 + 92, -64), (0, 96, 192), ay, (4, 0, 0), METAL, lux=8)
    for i in range(0, 13, 3):
        z = -256 + i * 32
        y = i * 16
        R.box(124, y, z - 4, 132, y + 92, z + 4, METAL, skip='TB', lux=8)
    R.collide_wall((128, -288), (128, 128), 0, 330)
    R.collide_wall((128, 128), (128, -288), 0, 330)
    R.collide_wall((-64, -288), (-64, 128), 0, 330)

    # ---- the cage in the north-east corner: wire mesh, a gate with a proper door frame
    CH = 320.0
    R.box(224, 0, 246, 288, CH, 320, DIRTY, skip='B', lux=10)       # gate posts (the door buttons sit on these)
    R.box(224, 0, 512, 288, CH, 586, DIRTY, skip='B', lux=10)
    mesh_panel(R, (256, 192), (256, 246), 0, CH)
    mesh_panel(R, (256, 586), (256, 640), 0, CH)
    mesh_panel(R, (640, 192), (256, 192), 0, CH)
    R.add([V(256, CH, 192), V(640, CH, 192), V(640, CH, 640), V(256, CH, 640)],
          [(0, 0), (6, 0), (6, 7), (0, 7)], MESH, lm=False, coll=False)
    R.box(250, 0, 186, 262, CH, 198, DIRTY, skip='B', lux=10)
    R.box(250, CH - 8, 192, 262, CH, 640, DIRTY, lux=10)
    R.box(256, CH - 8, 186, 640, CH, 198, DIRTY, lux=10)
    R.door_marker(256, 0, 416, 90)
    A['cage_door'] = (256, 0, 416)
    top = desk(R, 430, 500, 580, 590, 0)
    A['pod'] = (505, top, 545)
    A['cage_item'] = (450, top + 4, 545)

    # ---- the office: console wall, lever, desk under the window
    R.decal((-600, 640), (-380, 640), UP + 30, UP + 250, CTRL, (0.0, 0.0, 0.5, 1.0))
    R.decal((-330, 640), (-130, 640), UP + 30, UP + 250, CTRL, (0.5, 0.0, 1.0, 1.0))
    R.decal((-430, 640), (-290, 640), UP + 262, UP + 310, LOGO, (0, 0.25, 1, 0.75))
    A['lever'] = (-355, UP + 150, 631)
    sign2(R, 'cagelock', -355, 640, 'S', 0.1, 0.1, 0) if False else None
    R.decal((-250, 640), (-140, 640), UP + 256, UP + 296, SIGN2, SIGNS2['cagelock'])
    top = desk(R, -560, 170, -260, 250, UP)
    A['desk_a'] = (-500, top + 4, 210)
    A['desk_b'] = (-330, top + 4, 210)
    workstation(R, -410, top, 200, yaw=0)
    R.model('officeseat_a.x', -420, UP, 320, rot=(0, 0, 0), scale=(3.5, 3.5, 3.5), size=(84, 160, 84))
    cabinet(R, -612, 420, UP, 'E')
    cabinet(R, -612, 480, UP, 'E')
    A['cab_top'] = (-612, UP + 180, 450)

    # ---- the duct fan in the east wall
    R.rect_floor(640, -400, 736, -240, 320, DARK)
    R.rect_ceil(640, -400, 736, -240, 480, DARK)
    R.wall((640, -240), (736, -240), 320, 480, DARK)
    R.wall((736, -400), (640, -400), 320, 480, DARK)
    R.quad(V(736, 320, -240), V(736, 320, -400), V(736, 480, -400), V(736, 480, -240), VENT, uvrect=(0, 0, 1, 1))
    A['fan'] = (684, 400, -320)
    R.sound(684, 400, -320, 9, 4.5)

    # ---- lights
    ceil_light(R, 200, -300, H, size=112, power=150, rng=1100)
    ceil_light(R, 420, 380, H, size=96, power=120, rng=900)
    ceil_light(R, -360, 400, H, size=80, power=110, rng=760, color=(255, 240, 220))
    ceil_light(R, 0, -864, 384, size=64, power=74, rng=540)

    # ---- signs
    sign2(R, 'test4a', 0, -736, 'N', 330, 82, 440)
    sign2(R, 'l_131', 640, 120, 'W', 88, 110, 220)
    sign2(R, 'n_pods', 640, 0, 'W', 88, 88, 220)

    R.waypoint(0, 66, -860)
    R.waypoint(0, 66, -400)
    return R, A


if __name__ == '__main__':
    import time
    t = time.time()
    R, A = build()
    R.bake()
    print('bake %.1fs' % (time.time() - t))
    R.export('out')
    R.topview('out/testcage_top.png')
    R.render((-420, 165, -660), (300, 150, 400), 'out/testcage_1.png')
    R.render((560, 165, -560), (-300, 220, 250), 'out/testcage_2.png')
    R.render((-180, UP + 165, 300), (-500, UP + 120, 640), 'out/testcage_3.png')
    for k, v in A.items():
        print('  ', k, v)
