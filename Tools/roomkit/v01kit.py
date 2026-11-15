"""v01kit - corridor, corner, junction and dead-end rooms in the look of SCP:CB v0.1.

junction() lays out any of the five room shapes from a list of arms round a hub; annex() hangs a
side room (door or window) off any wall; the small feature functions dress it. Everything the game
code has to create (items, doors, fans, lifts, NPC spots) is recorded in R.spawns and written out
as Blitz by gen_v01.py, so the room files and the code can never disagree about a coordinate."""
from parts import *

CTRL = Mat('controlpanel.jpg', 256, cast=False)
CONC = Mat('concretefloor.jpg', 256)
STYLES = {
    'old':   (Mat('Old_Whitewall.jpg', 384), CONC, CONC),
    'board': (Mat('concretemoss.jpg', 512), CONC, DIRTY),
    'ez':    (Mat('officewall.jpg', 364), TILE, EZCEIL),
    'hcz':   (Mat('heavy_containment_wall_1789291243567.jpg', 512), HCZFLOOR, DIRTY),
    'std':   (Mat('standard_concrete_1789291464696.jpg', 512), CONC, DIRTY),
    'dark':  (Mat('concrete_wall_texture_1789291161197.jpg', 512), HCZFLOOR, DIRTY),
    'lab':   (Mat('lab_tile_wall_1789291261627.jpg', 512), TILE, Mat('white.jpg', 256)),
    'med':   (Mat('medibay.jpg', 384), TILE, Mat('white.jpg', 256)),
    'haz':   (Mat('hazard_stripe_wall_1789291234341.jpg', 512), CONC, DIRTY),
    'white': (Mat('white.jpg', 256), TILE, Mat('white.jpg', 256)),
}


def wmat(style, h):
    """wall material stretched so one repeat covers the wall height (band at the top, skirting at the floor)"""
    return STYLES[style][0].but(vs=h, v0=h)


def door_op(c, y0=0.0):
    return (c - 96.0, c + 96.0, y0, y0 + 320.0)


def junction(R, arms, style='old', w=192.0, ch=384.0, hub=None, hh=None, openings=None, waypoints=True):
    """arms: any of 'N' 'S' 'E' 'W'.  hub = (x0, z0, x1, z1), by default the w-square at the origin.
    openings = {wall key: [(c0, c1, y0, y1)]} with c in world units along the wall.
    Wall keys: hubN hubS hubE hubW, N_W N_E S_W S_E E_N E_S W_N W_S."""
    wallm, floorm, ceilm = STYLES[style]
    x0, z0, x1, z1 = hub or (-w, -w, w, w)
    hh = hh or ch
    op = openings or {}
    HW = wmat(style, hh)
    AW = wmat(style, ch)

    def wall(key, a, b, y0, y1, mat, extra=()):
        holes = list(extra)
        along_x = abs(a[0] - b[0]) > abs(a[1] - b[1])
        for (c0, c1, hy0, hy1) in op.get(key, ()):
            if along_x:
                s = sorted((abs(c0 - a[0]), abs(c1 - a[0])))
            else:
                s = sorted((abs(c0 - a[1]), abs(c1 - a[1])))
            holes.append((s[0], s[1], hy0, hy1))
        R.wall(a, b, y0, y1, mat, holes=holes)

    def mouth(a, p, q, present):
        return [span(a, p, q) + (0, ch)] if present else []

    # hub
    R.rect_floor(x0, z0, x1, z1, 0, floorm)
    R.rect_ceil(x0, z0, x1, z1, hh, ceilm)
    wall('hubN', (x0, z1), (x1, z1), 0, hh, HW, mouth((x0, z1), (-w, z1), (w, z1), 'N' in arms))
    wall('hubE', (x1, z1), (x1, z0), 0, hh, HW, mouth((x1, z1), (x1, w), (x1, -w), 'E' in arms))
    wall('hubS', (x1, z0), (x0, z0), 0, hh, HW, mouth((x1, z0), (w, z0), (-w, z0), 'S' in arms))
    wall('hubW', (x0, z0), (x0, z1), 0, hh, HW, mouth((x0, z0), (x0, -w), (x0, w), 'W' in arms))
    # arms
    if 'N' in arms:
        R.rect_floor(-w, z1, w, 992, 0, floorm)
        R.rect_ceil(-w, z1, w, 992, ch, ceilm)
        wall('N_W', (-w, z1), (-w, 992), 0, ch, AW)
        wall('N_E', (w, 992), (w, z1), 0, ch, AW)
        end_wall(R, 'N', -w, w, ch, AW, floorm)
    if 'S' in arms:
        R.rect_floor(-w, -992, w, z0, 0, floorm)
        R.rect_ceil(-w, -992, w, z0, ch, ceilm)
        wall('S_E', (w, z0), (w, -992), 0, ch, AW)
        wall('S_W', (-w, -992), (-w, z0), 0, ch, AW)
        end_wall(R, 'S', -w, w, ch, AW, floorm)
    if 'E' in arms:
        R.rect_floor(x1, -w, 992, w, 0, floorm)
        R.rect_ceil(x1, -w, 992, w, ch, ceilm)
        wall('E_N', (x1, w), (992, w), 0, ch, AW)
        wall('E_S', (992, -w), (x1, -w), 0, ch, AW)
        end_wall(R, 'E', -w, w, ch, AW, floorm)
    if 'W' in arms:
        R.rect_floor(-992, -w, x0, w, 0, floorm)
        R.rect_ceil(-992, -w, x0, w, ch, ceilm)
        wall('W_S', (x0, -w), (-992, -w), 0, ch, AW)
        wall('W_N', (-992, w), (x0, w), 0, ch, AW)
        end_wall(R, 'W', -w, w, ch, AW, floorm)
    if waypoints:
        R.waypoint(0, 66, 0)
        for a, (px, pz) in (('N', (0, 640)), ('S', (0, -640)), ('E', (640, 0)), ('W', (-640, 0))):
            if a in arms:
                R.waypoint(px, 66, pz)


def annex(R, axis, plane, sign, a0, a1, depth, h, style, door=None, window=None, key=0, jamb=64.0, y=0.0, spawn_door=True):
    """A side room behind a wall.  axis 'x': the wall is x = plane and the room lies towards sign * x,
    running a0..a1 along z ('z': the other way round).  door = centre of a 192 x 320 doorway along the
    wall; window = (c0, c1, y0, y1).  The corridor wall needs the matching opening (door_op / the
    window tuple).  Returns the interior (x0, z0, x1, z1)."""
    wallm, floorm, ceilm = STYLES[style]
    near = plane + sign * jamb
    far = near + sign * depth
    lo, hi = sorted((near, far))
    if axis == 'x':
        x0, x1, z0, z1 = lo, hi, a0, a1
    else:
        x0, x1, z0, z1 = a0, a1, lo, hi
    WM = wmat(style, h)

    def P(c, d):                      # c along the wall, d across it -> (x, z)
        return (d, c) if axis == 'x' else (c, d)

    cuts = []
    if door is not None:
        cuts.append((door - 96.0, door + 96.0, y, y + 320.0, floorm))
    if window is not None:
        cuts.append((window[0], window[1], window[2], window[3], DARK))
    # which interior wall is the near one, and its holes
    seg = {('x', 1): 0, ('x', -1): 2, ('z', 1): 3, ('z', -1): 1}[(axis, sign)]
    out = [(x0, z0), (x0, z1), (x1, z1), (x1, z0)]
    a = out[seg]
    holes = []
    for (c0, c1, hy0, hy1, _) in cuts:
        holes.append(span(a, P(c0, near), P(c1, near)) + (hy0, hy1))
    R.walls(out, y, y + h, WM, holes={seg: holes})
    R.rect_floor(x0, z0, x1, z1, y, floorm)
    R.rect_ceil(x0, z0, x1, z1, y + h, ceilm)
    # the reveals through the wall
    for (c0, c1, hy0, hy1, fm) in cuts:
        pa, pb = sorted((plane, near))
        q = [P(c0, pa), P(c1, pa), P(c1, pb), P(c0, pb)]
        poly_facing(R, [V(p[0], hy0, p[1]) for p in q], (0, 1, 0), fm)
        poly_facing(R, [V(p[0], hy1, p[1]) for p in q], (0, -1, 0), WM if fm is floorm else DARK)
        for (c, s) in ((c0, 1), (c1, -1)):
            e0, e1 = P(c, pa), P(c, pb)
            hint = (0, 0, s) if axis == 'x' else (s, 0, 0)
            poly_facing(R, [V(e0[0], hy0, e0[1]), V(e1[0], hy0, e1[1]), V(e1[0], hy1, e1[1]), V(e0[0], hy1, e0[1])],
                        hint, WM if fm is floorm else DARK)
    if door is not None:
        dp = P(door, plane + sign * jamb / 2)
        ang = 90 if axis == 'x' else 0
        R.door_marker(dp[0], y, dp[1], ang)
        if spawn_door:
            R.spawns.append(dict(kind='door', pos=(dp[0], y, dp[1]), angle=ang, key=key))
    return (x0, z0, x1, z1)


# --------------------------------------------------------------------- dressing
def lamp(R, x, z, ceil_y, power=96, rng=760, color=(255, 240, 220), size=44):
    ceil_light(R, x, z, ceil_y, size=size, power=power, rng=rng, color=color)


def arch(R, axis, c, w, ch, style='old', leg=44.0, lintel=52.0, depth=72.0, lit=True):
    """A concrete portal across a corridor (the v0.1 door-frame blocks), with a small lamp in each leg."""
    m = STYLES['std'][0].but(us=256, vs=256)
    d = depth / 2

    def bx(l0, l1, y0, y1):
        if axis == 'z':
            R.box(l0, y0, c - d, l1, y1, c + d, m, skip='B', lux=12)
        else:
            R.box(c - d, y0, l0, c + d, y1, l1, m, skip='B', lux=12)
    bx(-w, -w + leg, 0, ch)
    bx(w - leg, w, 0, ch)
    if axis == 'z':
        R.box(-w + leg, ch - lintel, c - d, w - leg, ch, c + d, m, skip='T', lux=12)
    else:
        R.box(c - d, ch - lintel, -w + leg, c + d, ch, w - leg, m, skip='T', lux=12)
    if lit:
        for s in (-1, 1):
            for f in (-1, 1):
                lx = s * (w - leg / 2)
                if axis == 'z':
                    wall_light(R, lx, c + f * d, 120, 'N' if f > 0 else 'S', power=30, rng=260, w=18, h=14, d=4)
                else:
                    wall_light(R, c + f * d, lx, 120, 'E' if f > 0 else 'W', power=30, rng=260, w=18, h=14, d=4)


def ibeam(R, axis, c, l0, l1, y, size=30.0):
    """A steel beam crossing overhead."""
    h = size / 2
    if axis == 'z':        # beam runs along x at z = c
        R.box(l0, y - h, c - h, l1, y + h, c + h, DIRTY, lux=14)
        R.box(l0, y + h, c - h * 1.8, l1, y + h + 5, c + h * 1.8, DIRTY, lux=14)
        R.box(l0, y - h - 5, c - h * 1.8, l1, y - h, c + h * 1.8, DIRTY, lux=14)
    else:
        R.box(c - h, y - h, l0, c + h, y + h, l1, DIRTY, lux=14)
        R.box(c - h * 1.8, y + h, l0, c + h * 1.8, y + h + 5, l1, DIRTY, lux=14)
        R.box(c - h * 1.8, y - h - 5, l0, c + h * 1.8, y - h, l1, DIRTY, lux=14)


def pillar(R, x, z, h, s=40.0, style='std'):
    m = STYLES[style][0].but(us=4 * s, vs=h, v0=h)
    R.box(x - s, 0, z - s, x + s, h, z + s, m, skip='TB', lux=12)
    R.box(x - s - 6, 0, z - s - 6, x + s + 6, 22, z + s + 6, DARK, skip='B', lux=10)


def bench(R, x, z, yaw=0):
    R.model('scpcb_bench.x', x, 0, z, rot=(0, yaw, 0), scale=(1, 1, 1),
            size=(144, 50, 44) if yaw % 180 == 0 else (44, 50, 144))


def lockers(R, axis, plane, sign, c0, c1, h=300.0, depth=30.0, w=88.0):
    """A run of steel locker fronts standing against a wall."""
    m = PANELS2.but(us=w, vs=h, v0=h)
    lo, hi = sorted((plane, plane + sign * depth))
    c = c0
    while c + w <= c1 + 0.1:
        if axis == 'x':
            R.box(lo, 0, c + 3, hi, h, c + w - 3, m, skip='B' + ('W' if sign > 0 else 'E'), lux=10)
        else:
            R.box(c + 3, 0, lo, c + w - 3, h, hi, m, skip='B' + ('S' if sign > 0 else 'N'), lux=10)
        c += w


def wall_fan(R, axis, plane, sign, c, y, size=160.0, depth=96.0, radius=70.0):
    """Duct recess behind a wall (the wall needs the opening (c - size/2, c + size/2, y - size/2, y + size/2))
    with a fan rotor in it."""
    s = size / 2
    far = plane + sign * depth
    for (dy, hint) in ((-s, (0, 1, 0)), (s, (0, -1, 0))):
        if axis == 'x':
            q = [V(plane, y + dy, c - s), V(far, y + dy, c - s), V(far, y + dy, c + s), V(plane, y + dy, c + s)]
        else:
            q = [V(c - s, y + dy, plane), V(c - s, y + dy, far), V(c + s, y + dy, far), V(c + s, y + dy, plane)]
        poly_facing(R, q, hint, DARK)
    for (dc, hs) in ((-s, 1), (s, -1)):
        if axis == 'x':
            q = [V(plane, y - s, c + dc), V(far, y - s, c + dc), V(far, y + s, c + dc), V(plane, y + s, c + dc)]
            hint = (0, 0, hs)
        else:
            q = [V(c + dc, y - s, plane), V(c + dc, y - s, far), V(c + dc, y + s, far), V(c + dc, y + s, plane)]
            hint = (hs, 0, 0)
        poly_facing(R, q, hint, DARK)
    if axis == 'x':
        q = [V(far, y - s, c - s), V(far, y - s, c + s), V(far, y + s, c + s), V(far, y + s, c - s)]
        hint = (-sign, 0, 0)
        pos = (plane + sign * depth * 0.45, y, c)
        yaw = 90
    else:
        q = [V(c - s, y - s, far), V(c + s, y - s, far), V(c + s, y + s, far), V(c - s, y + s, far)]
        hint = (0, 0, -sign)
        pos = (c, y, plane + sign * depth * 0.45)
        yaw = 0
    P = [np.asarray(p, dtype=float) for p in q]
    if np.dot(np.cross(P[3] - P[0], P[1] - P[0]), hint) < 0:
        P = [P[1], P[0], P[3], P[2]]
    R.add(P, [(0, 1), (1, 1), (1, 0), (0, 0)], VENT)
    R.spawns.append(dict(kind='fan', pos=pos, radius=radius, yaw=yaw))
    R.sound(pos[0], pos[1], pos[2], 9, 4.0)


def ceil_fan(R, x, z, ceil_y, drop=58.0, radius=140.0):
    R.box(x - 2, ceil_y - drop + 6, z - 2, x + 2, ceil_y, z + 2, DIRTY, skip='TB', lux=8)
    R.spawns.append(dict(kind='ceilfan', pos=(x, ceil_y - drop, z), radius=radius))


def item(R, name, x, y, z, chance=100):
    R.spawns.append(dict(kind='item', name=name, pos=(x, y, z), chance=chance))


def spot(R, x, y, z):
    """Where the room's NPC stands / lies (Objects[4])."""
    R.spawns.append(dict(kind='spot', pos=(x, y, z)))


def vent_block(R, x0, z0, x1, z1, h, lights=True, style='std'):
    """A free-standing concrete block with vent grilles low down and lamps high up (reference shot 12)."""
    m = STYLES[style][0].but(us=512, vs=h, v0=h)
    R.box(x0, 0, z0, x1, h, z1, m, skip='TB', lux=12)
    cx, cz = (x0 + x1) / 2, (z0 + z1) / 2
    for f, px, pz, L in (('S', cx, z0, x1 - x0), ('N', cx, z1, x1 - x0), ('E', x1, cz, z1 - z0), ('W', x0, cz, z1 - z0)):
        n = 2 if L >= 300 else 1
        for i in range(n):
            off = (i - (n - 1) / 2) * (L / n)
            qx, qz = (px + off, pz) if f in 'NS' else (px, pz + off)
            if lights:
                wall_light(R, qx, qz, min(h - 110, 300), f, power=52, rng=440, w=26, h=26, d=7)
            sg = {'S': 1, 'N': -1, 'E': 1, 'W': -1}[f]
            if f in 'NS':
                R.decal((qx - sg * 40, qz), (qx + sg * 40, qz), 40, 120, VENT, (0, 0, 1, 1), off=2)
            else:
                R.decal((qx, qz - sg * 40), (qx, qz + sg * 40), 40, 120, VENT, (0, 0, 1, 1), off=2)
