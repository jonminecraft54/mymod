"""v02kit - more pieces for the v0.1-style rooms: chamfered (octagonal) hubs, console units, meeting
tables, vending machines, cages, tanks, mezzanines, overhead bridges, glazed windows, NPC roles."""
from v01kit import *

WOODT = Mat('wood.jpg', 512)
WB = Mat('scpcb_whiteboard.jpg', 256, cast=False)
PAINT = Mat('scpcb_painting.jpg', 256, cast=False)
WMON = Mat('scpcb_wallmonitor.jpg', 256, cast=False)
VEND = Mat('scpcb_vending.jpg', 256, cast=False)
TANKM = PANELS2
YAW = {'S': 0, 'E': 90, 'N': 180, 'W': 270}        # yaw that turns a model's -z front to face that way


def junction2(R, arms, style='old', w=192.0, ch=384.0, hub=None, hh=None, cut=0.0, openings=None, waypoints=True):
    """junction() with the hub corners cut off by `cut` (an eight-sided hall when cut > 0)."""
    if cut <= 0:
        return junction(R, arms, style, w, ch, hub, hh, openings, waypoints)
    wallm, floorm, ceilm = STYLES[style]
    x0, z0, x1, z1 = hub
    hh = hh or ch
    op = openings or {}
    HW = wmat(style, hh)
    AW = wmat(style, ch)
    c = cut
    poly = [(x0, z0 + c), (x0, z1 - c), (x0 + c, z1), (x1 - c, z1), (x1, z1 - c), (x1, z0 + c), (x1 - c, z0), (x0 + c, z0)]
    R.floor(poly, 0, floorm)
    R.ceil(poly, hh, ceilm)

    def holes_for(key, a, along_x, extra):
        hs = list(extra)
        for (c0, c1, hy0, hy1) in op.get(key, ()):
            s = sorted((abs(c0 - a[0]), abs(c1 - a[0]))) if along_x else sorted((abs(c0 - a[1]), abs(c1 - a[1])))
            hs.append((s[0], s[1], hy0, hy1))
        return hs
    sides = {0: ('hubW', 'W', False), 2: ('hubN', 'N', True), 4: ('hubE', 'E', False), 6: ('hubS', 'S', True)}
    mouths = {'N': ((-w, z1), (w, z1)), 'E': ((x1, w), (x1, -w)), 'S': ((w, z0), (-w, z0)), 'W': ((x0, -w), (x0, w))}
    for i in range(8):
        a, b = poly[i], poly[(i + 1) % 8]
        extra = []
        if i in sides:
            key, arm, along_x = sides[i]
            if arm in arms:
                p, q = mouths[arm]
                extra = [span(a, p, q) + (0, ch)]
            R.wall(a, b, 0, hh, HW, holes=holes_for(key, a, along_x, extra))
        else:
            R.wall(a, b, 0, hh, HW)
    junction_arms(R, arms, style, w, ch, (x0, z0, x1, z1), op, AW)
    if waypoints:
        R.waypoint(0, 66, 0)
        for a, (px, pz) in (('N', (0, 720)), ('S', (0, -720)), ('E', (720, 0)), ('W', (-720, 0))):
            if a in arms:
                R.waypoint(px, 66, pz)


def junction_arms(R, arms, style, w, ch, hub, op, AW):
    wallm, floorm, ceilm = STYLES[style]
    x0, z0, x1, z1 = hub

    def wall(key, a, b):
        holes = []
        along_x = abs(a[0] - b[0]) > abs(a[1] - b[1])
        for (c0, c1, hy0, hy1) in op.get(key, ()):
            s = sorted((abs(c0 - a[0]), abs(c1 - a[0]))) if along_x else sorted((abs(c0 - a[1]), abs(c1 - a[1])))
            holes.append((s[0], s[1], hy0, hy1))
        R.wall(a, b, 0, ch, AW, holes=holes)
    if 'N' in arms:
        R.rect_floor(-w, z1, w, 992, 0, floorm)
        R.rect_ceil(-w, z1, w, 992, ch, ceilm)
        wall('N_W', (-w, z1), (-w, 992))
        wall('N_E', (w, 992), (w, z1))
        end_wall(R, 'N', -w, w, ch, AW, floorm)
    if 'S' in arms:
        R.rect_floor(-w, -992, w, z0, 0, floorm)
        R.rect_ceil(-w, -992, w, z0, ch, ceilm)
        wall('S_E', (w, z0), (w, -992))
        wall('S_W', (-w, -992), (-w, z0))
        end_wall(R, 'S', -w, w, ch, AW, floorm)
    if 'E' in arms:
        R.rect_floor(x1, -w, 992, w, 0, floorm)
        R.rect_ceil(x1, -w, 992, w, ch, ceilm)
        wall('E_N', (x1, w), (992, w))
        wall('E_S', (992, -w), (x1, -w))
        end_wall(R, 'E', -w, w, ch, AW, floorm)
    if 'W' in arms:
        R.rect_floor(-992, -w, x0, w, 0, floorm)
        R.rect_ceil(-992, -w, x0, w, ch, ceilm)
        wall('W_S', (x0, -w), (-992, -w))
        wall('W_N', (-992, w), (x0, w))
        end_wall(R, 'W', -w, w, ch, AW, floorm)


# --------------------------------------------------------------------- furniture
def console(R, x, z, wall_facing, y=0.0):
    """A console unit (screens at the back) standing with its back to a wall that faces `wall_facing`."""
    R.model('scpcb_console.x', x, y, z, rot=(0, YAW[wall_facing], 0), scale=(1, 1, 1),
            size=(192, 208, 80) if wall_facing in 'NS' else (80, 208, 192))


def chair(R, x, z, look, y=0.0):
    """look: the way the sitter faces ('N' 'S' 'E' 'W')."""
    R.model('scpcb_chair.x', x, y, z, rot=(0, YAW[look], 0), scale=(1, 1, 1), size=(40, 104, 40))


def book(R, x, y, z, yaw=20):
    R.model('scpcb_book.x', x, y, z, rot=(0, yaw, 0), scale=(1, 1, 1), size=(28, 6, 20))


def table(R, x0, z0, x1, z1, y=0.0, h=78.0, top=None):
    """Plain table on four legs.  Returns the top height."""
    top = top or DIRTY
    R.box(x0, y + h - 8, z0, x1, y + h, z1, top, lux=8)
    for (px, pz) in ((x0 + 6, z0 + 6), (x1 - 14, z0 + 6), (x0 + 6, z1 - 14), (x1 - 14, z1 - 14)):
        R.box(px, y, pz, px + 8, y + h - 8, pz + 8, DIRTY, skip='TB', lux=8)
    return y + h


def meeting(R, cx, cz, along='x', length=360.0, width=150.0, y=0.0, with_book=True):
    """Conference table with chairs down both sides and one at each end (reference: the meeting room)."""
    if along == 'x':
        top = table(R, cx - length / 2, cz - width / 2, cx + length / 2, cz + width / 2, y)
        for dx in (-length / 4, length / 4):
            chair(R, cx + dx, cz - width / 2 - 40, 'N', y)
            chair(R, cx + dx, cz + width / 2 + 40, 'S', y)
        chair(R, cx - length / 2 - 40, cz, 'E', y)
    else:
        top = table(R, cx - width / 2, cz - length / 2, cx + width / 2, cz + length / 2, y)
        for dz in (-length / 4, length / 4):
            chair(R, cx - width / 2 - 40, cz + dz, 'E', y)
            chair(R, cx + width / 2 + 40, cz + dz, 'W', y)
        chair(R, cx, cz - length / 2 - 40, 'N', y)
    if with_book:
        book(R, cx - 40, top, cz + 10)
    return top


def wall_decal(R, mat, cx, cz, facing, w, h, yc, uv=(0, 0, 1, 1)):
    hw = w / 2
    if facing == 'S':
        a, b = (cx - hw, cz), (cx + hw, cz)
    elif facing == 'N':
        a, b = (cx + hw, cz), (cx - hw, cz)
    elif facing == 'E':
        a, b = (cx, cz - hw), (cx, cz + hw)
    else:
        a, b = (cx, cz + hw), (cx, cz - hw)
    R.decal(a, b, yc - h / 2, yc + h / 2, mat, uv)


def whiteboard(R, cx, cz, facing, yc=190.0):
    wall_decal(R, WB, cx, cz, facing, 240, 120, yc)


def painting(R, cx, cz, facing, yc=200.0):
    wall_decal(R, PAINT, cx, cz, facing, 96, 96, yc)


def wallmonitor(R, cx, cz, facing, yc=210.0):
    wall_decal(R, WMON, cx, cz, facing, 110, 110, yc)


def vents(R, cx, cz, facing, n=2, gap=110.0, yc=90.0, size=80.0):
    for i in range(n):
        off = (i - (n - 1) / 2) * gap
        if facing in 'NS':
            wall_decal(R, VENT, cx + off, cz, facing, size, size, yc)
        else:
            wall_decal(R, VENT, cx, cz + off, facing, size, size, yc)


def vending(R, cx, cz, facing):
    """A vending machine: a box with the printed front on the side that faces `facing`."""
    n = {'N': (0, 1), 'S': (0, -1), 'E': (1, 0), 'W': (-1, 0)}[facing]
    if facing in 'NS':
        x0, x1, z0, z1 = cx - 40, cx + 40, min(cz, cz + n[1] * 44), max(cz, cz + n[1] * 44)
    else:
        x0, x1, z0, z1 = min(cx, cx + n[0] * 44), max(cx, cx + n[0] * 44), cz - 40, cz + 40
    R.box(x0, 0, z0, x1, 176, z1, DARK.but(us=512), skip='B', lux=10)
    wall_decal(R, VEND, cx + n[0] * 44, cz + n[1] * 44, facing, 80, 176, 88)


def ceil_vent(R, x, z, ceil_y, size=90.0, drop=44.0):
    """The boxy air handler hanging off the ceiling in the meeting room shot."""
    h = size / 2
    R.box(x - h, ceil_y - drop, z - h, x + h, ceil_y, z + h, Mat('white.jpg', 256), skip='TB', lux=10)
    R.add([V(x + h, ceil_y - drop, z - h), V(x - h, ceil_y - drop, z - h), V(x - h, ceil_y - drop, z + h),
           V(x + h, ceil_y - drop, z + h)], [(0, 1), (1, 1), (1, 0), (0, 0)], VENT)


def glow_door(R, cx, cz, facing, w=150.0, h=290.0, power=120.0):
    """A doorway-shaped panel of flat white light (the white door of the reference shot)."""
    wall_decal(R, WHITEGLOW, cx, cz, facing, w, h, h / 2)
    n = {'N': (0, 1), 'S': (0, -1), 'E': (1, 0), 'W': (-1, 0)}[facing]
    R.light(cx + n[0] * 70, 150, cz + n[1] * 70, rng=900, color=(255, 255, 255), power=power, radius=30)


def tank(R, x0, z0, x1, z1, h=320.0):
    R.box(x0, 0, z0, x1, h, z1, TANKM.but(us=x1 - x0 if (x1 - x0) > (z1 - z0) else z1 - z0, vs=h, v0=h), skip='B', lux=12)
    R.box(x0 - 4, h, z0 - 4, x1 + 4, h + 10, z1 + 4, DARK, lux=12)


def pilasters(R, axis, plane, sign, c0, c1, step, h, depth=18.0, width=44.0, style='std'):
    m = STYLES[style][0].but(us=width * 2, vs=h, v0=h)
    lo, hi = sorted((plane, plane + sign * depth))
    c = c0
    while c <= c1 + 0.1:
        if axis == 'x':
            R.box(lo, 0, c - width / 2, hi, h, c + width / 2, m, skip='TB' + ('W' if sign > 0 else 'E'), lux=12)
        else:
            R.box(c - width / 2, 0, lo, c + width / 2, h, hi, m, skip='TB' + ('S' if sign > 0 else 'N'), lux=12)
        c += step


def pipes_z(R, runs, z0=-990.0, z1=990.0):
    for (x, y, r) in runs:
        R.tube((x, y, z0), (x, y, z1), r, RUST.but(us=2 * math.pi * r, vs=256), sides=8, lux=16)


def pipes_x(R, runs, x0=-990.0, x1=990.0):
    for (z, y, r) in runs:
        R.tube((x0, y, z), (x1, y, z), r, RUST.but(us=2 * math.pi * r, vs=256), sides=8, lux=16)


def bridge(R, axis, c, l0, l1, y=336.0, width=160.0):
    """A railed walkway crossing overhead from wall to wall (scenery: nothing leads up to it)."""
    h = width / 2
    if axis == 'x':        # runs along x at z = c
        R.box(l0, y - 16, c - h, l1, y, c + h, DARK, skip='EW', top=DIRTY, lux=12)
        railing(R, (l0, c - h), (l1, c - h), y)
        railing(R, (l0, c + h), (l1, c + h), y)
    else:
        R.box(c - h, y - 16, l0, c + h, y, l1, DARK, skip='NS', top=DIRTY, lux=12)
        railing(R, (c - h, l0), (c - h, l1), y)
        railing(R, (c + h, l0), (c + h, l1), y)


def cage(R, x0, z0, x1, z1, h=288.0, open_side=None, gap=(0, 0)):
    """A wire-mesh cage.  open_side 'N' 'S' 'E' 'W' leaves a gap (c0, c1) in that side."""
    for side, a, b in (('S', (x0, z0), (x1, z0)), ('N', (x1, z1), (x0, z1)), ('E', (x1, z0), (x1, z1)), ('W', (x0, z1), (x0, z0))):
        if side == open_side:
            g0, g1 = gap
            if side in 'NS':
                zz = a[1]
                lo, hi = sorted((a[0], b[0]))
                if g0 - lo > 4:
                    mesh_panel(R, (lo, zz), (g0, zz), 0, h)
                if hi - g1 > 4:
                    mesh_panel(R, (g1, zz), (hi, zz), 0, h)
            else:
                xx = a[0]
                lo, hi = sorted((a[1], b[1]))
                if g0 - lo > 4:
                    mesh_panel(R, (xx, lo), (xx, g0), 0, h)
                if hi - g1 > 4:
                    mesh_panel(R, (xx, g1), (xx, hi), 0, h)
        else:
            mesh_panel(R, a, b, 0, h)
    for (px, pz) in ((x0, z0), (x1, z0), (x1, z1), (x0, z1)):
        R.box(px - 5, 0, pz - 5, px + 5, h, pz + 5, DIRTY, skip='B', lux=10)
    R.add([V(x0, h, z0), V(x1, h, z0), V(x1, h, z1), V(x0, h, z1)],
          [(0, 0), ((x1 - x0) / 64, 0), ((x1 - x0) / 64, (z1 - z0) / 64), (0, (z1 - z0) / 64)], MESH, lm=False, coll=False)


def glaze(R, axis, plane, sign, win, jamb=64.0):
    """Glass in an annex window (win = (c0, c1, y0, y1))."""
    d = plane + sign * jamb / 2
    c0, c1, y0, y1 = win
    if axis == 'x':
        R.quad(V(d, y0, c0), V(d, y0, c1), V(d, y1, c1), V(d, y0 + (y1 - y0), c0), GLASS, uvrect=(0, 0, (c1 - c0) / 256, 0.5), lm=False)
    else:
        R.quad(V(c0, y0, d), V(c1, y0, d), V(c1, y1, d), V(c0, y1, d), GLASS, uvrect=(0, 0, (c1 - c0) / 256, 0.5), lm=False)


def beds(R, x0, x1, zs):
    white = Mat('white.jpg', 256)
    for z in zs:
        R.box(x0, 0, z - 46, x1, 46, z + 46, DIRTY, skip='B', lux=10)
        R.box(x0 + 4, 46, z - 42, x1 - 4, 58, z + 42, white, skip='B', lux=10)


def role(R, kind, x, y, z, yaw=0):
    """The room's NPC: 'guard', 'tech', 'sci' (alive, they talk), 'sit' / 'sitd' / 'lie' / 'liej' (bodies)."""
    R.spawns.append(dict(kind='spot', pos=(x, y, z), role=kind, yaw=yaw))


def roll(R, x, y, z):
    """One roll on the mod's rare-item table for the room's tag (see IndevRareSpawn.bb)."""
    R.spawns.append(dict(kind='roll', pos=(x, y, z)))


def bigfan(R, x, y, z, radius=220.0):
    R.spawns.append(dict(kind='bigfan', pos=(x, y, z), radius=radius))
    R.sound(x, y, z, 9, 6.0)


def lift(R, wall_x, direction, za, ya, zb, yb, wall_mat):
    """Lift with stops (za, ya) and (zb, yb) behind the wall x = wall_x; stop a starts open."""
    d1, p1 = elevator(R, wall_x, za, ya, direction, wall_mat)
    d2, p2 = elevator(R, wall_x, zb, yb, direction, wall_mat)
    R.spawns.append(dict(kind='lift', a=d1, ap=p1, b=d2, bp=p2))
    return d1, d2
