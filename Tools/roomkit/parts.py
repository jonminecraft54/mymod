"""Shared building blocks for the Indev rooms (built on roomkit)."""
import json
import math
import os
import numpy as np
from roomkit import *

HERE = os.path.dirname(os.path.abspath(__file__))
SIGNS = json.load(open(os.path.join(HERE, 'signs.json')))
SIGN = Mat('indev_signs.png', cast=False)
MSIGN = Mat('miscsigns.jpg', cast=False)
WHITEGLOW = Mat('indev_glow.png', 64, emit=255, cast=False)
# rects in the vanilla miscsigns.jpg sheet
MS = dict(admittance=(0.02, 0.265, 0.375, 0.52), timeswitch=(0.02, 0.535, 0.375, 0.80),
          electrical=(0.405, 0.265, 0.975, 0.515), maintenance=(0.405, 0.53, 0.975, 0.78),
          hcz=(0.005, 0.205, 0.375, 0.255), ez=(0.005, 0.145, 0.375, 0.20), lcz=(0.38, 0.19, 0.745, 0.245),
          on=(0.795, 0.04, 0.957, 0.11), off=(0.795, 0.145, 0.957, 0.215),
          remote=(0.027, 0.825, 0.262, 0.975), primary=(0.282, 0.825, 0.515, 0.975), secondary=(0.535, 0.825, 0.77, 0.975))


def span(a, p, q):
    """distances of two points from a wall start a -> (s0, s1) sorted"""
    a = np.asarray(a, dtype=float)
    s0 = float(np.linalg.norm(np.asarray(p, dtype=float) - a))
    s1 = float(np.linalg.norm(np.asarray(q, dtype=float) - a))
    return (min(s0, s1), max(s0, s1))


def sign(R, name, a, b, y0, y1, sheet='indev'):
    """a..b: the wall stretch seen from the front (left -> right)."""
    if sheet == 'indev':
        R.decal(a, b, y0, y1, SIGN, SIGNS[name])
    else:
        R.decal(a, b, y0, y1, MSIGN, MS[name])


def sign_at(R, name, cx, cz, facing, w, h, yc, sheet='indev'):
    """A sign centred on (cx, cz) on a wall whose visible side faces `facing` ('N','S','E','W' = +z,-z,+x,-x)."""
    hw = w / 2
    if facing == 'S':      # wall faces -z, viewer looks +z: left = -x
        a, b = (cx - hw, cz), (cx + hw, cz)
    elif facing == 'N':    # wall faces +z, viewer looks -z: left = +x
        a, b = (cx + hw, cz), (cx - hw, cz)
    elif facing == 'E':    # wall faces +x, viewer looks -x: left = -z
        a, b = (cx, cz - hw), (cx, cz + hw)
    else:                  # wall faces -x, viewer looks +x: left = +z
        a, b = (cx, cz + hw), (cx, cz - hw)
    sign(R, name, a, b, yc - h / 2, yc + h / 2, sheet)


def ceil_light(R, x, z, y, size=96, power=150, rng=950, color=(255, 250, 240), drop=28, emit=250, ent=True, fill=None):
    """A flush ceiling light panel + the light it throws."""
    h = size / 2
    R.add([V(x + h, y - 1.0, z - h), V(x - h, y - 1.0, z - h), V(x - h, y - 1.0, z + h), V(x + h, y - 1.0, z + h)],
          [(0, 1), (1, 1), (1, 0), (0, 0)], LIGHTPANEL.but(emit=emit), cast=False)
    R.light(x, y - drop, z, rng=rng, color=color, power=power, ent=ent, fill=fill)


def wall_light(R, cx, cz, y, facing, power=70, rng=420, color=(255, 240, 215), w=28, h=40, d=10):
    """A small glowing wall fitting (the sconces in the office corridors)."""
    n = {'N': (0, 1), 'S': (0, -1), 'E': (1, 0), 'W': (-1, 0)}[facing]
    if facing in 'EW':
        x0, x1 = sorted((cx, cx + n[0] * d))
        z0, z1 = cz - w / 2, cz + w / 2
    else:
        z0, z1 = sorted((cz, cz + n[1] * d))
        x0, x1 = cx - w / 2, cx + w / 2
    R.box(x0, y - h / 2, z0, x1, y + h / 2, z1, LIGHTPANEL.but(emit=235), cast=False)
    R.light(cx + n[0] * (d + 14), y, cz + n[1] * (d + 14), rng=rng, color=color, power=power, radius=6)


def pendant(R, x, z, ceil_y, power=150, rng=900, color=(255, 245, 230)):
    """The vanilla red hanging lamp (lamp2.x) and its light."""
    R.model('lamp2.x', x, ceil_y - 56, z, size=(60, 40, 60))
    R.light(x, ceil_y - 70, z, rng=rng, color=color, power=power)


def railing(R, a, b, y, h=96.0, post=104.0, mat=None, coll_h=130.0):
    """Posts + top and mid rail along an axis-aligned xz segment standing on height y."""
    mat = mat or METAL
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    L = np.linalg.norm(b - a)
    d = (b - a) / L
    n = int(max(1, round(L / post)))
    for i in range(n + 1):
        p = a + d * (L * i / n)
        R.box(p[0] - 4, y, p[1] - 4, p[0] + 4, y + h - 8, p[1] + 4, mat, skip='TB', lux=8)
    x0, x1 = sorted((a[0], b[0]))
    z0, z1 = sorted((a[1], b[1]))
    R.box(x0 - 5, y + h - 8, z0 - 5, x1 + 5, y + h, z1 + 5, mat, lux=8)
    R.box(x0 - 3, y + h * 0.45, z0 - 3, x1 + 3, y + h * 0.45 + 6, z1 + 3, mat, lux=8)
    R.collide_wall(a, b, y, y + coll_h)
    R.collide_wall(b, a, y, y + coll_h)


def glass_rail(R, a, b, y, h=112.0, post=192.0):
    """Glass balustrade with steel posts and handrail (the overlook in the reference shot)."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    L = np.linalg.norm(b - a)
    d = (b - a) / L
    n = int(max(1, round(L / post)))
    for i in range(n + 1):
        p = a + d * (L * i / n)
        R.box(p[0] - 4, y, p[1] - 4, p[0] + 4, y + h, p[1] + 4, DIRTY, skip='B', lux=8)
    x0, x1 = sorted((a[0], b[0]))
    z0, z1 = sorted((a[1], b[1]))
    R.box(x0 - 5, y + h, z0 - 5, x1 + 5, y + h + 8, z1 + 5, DIRTY, lux=8)
    R.box(x0 - 4, y, z0 - 4, x1 + 4, y + 10, z1 + 4, DIRTY, skip='B', lux=8)
    for (p, q) in ((a, b), (b, a)):
        R.quad(V(p[0], y + 10, p[1]), V(q[0], y + 10, q[1]), V(q[0], y + h, q[1]), V(p[0], y + h, p[1]), GLASS,
               uvrect=(0, 0, L / 256.0, 0.4), lm=False, coll=False)
    R.collide_wall(a, b, y, y + 150)
    R.collide_wall(b, a, y, y + 150)


def elevator(R, wall_x, zc, y, direction, wall_mat, name=None, height=384.0, jamb=48.0, light=85):
    """Elevator shaft behind a wall at x = wall_x (the wall itself needs a 192 x 320 hole at zc).
    direction = +1: the cabin lies towards +x, -1: towards -x.
    Returns (door position, pivot position) in room units for the game code."""
    s = direction
    x_in = wall_x + s * jamb                 # cabin's near wall
    x_far = x_in + s * 560.0
    z0, z1 = zc - 280.0, zc + 280.0
    xa, xb = sorted((x_in, x_far))
    cab = METAL
    # jamb through the wall
    ja, jb = sorted((wall_x, x_in))
    R.rect_floor(ja, zc - 96, jb, zc + 96, y, CHECKER)
    R.rect_ceil(ja, zc - 96, jb, zc + 96, y + 320, DARK)
    if s > 0:
        R.wall((wall_x, zc + 96), (x_in, zc + 96), y, y + 320, DARK)
        R.wall((x_in, zc - 96), (wall_x, zc - 96), y, y + 320, DARK)
    else:
        R.wall((wall_x, zc - 96), (x_in, zc - 96), y, y + 320, DARK)
        R.wall((x_in, zc + 96), (wall_x, zc + 96), y, y + 320, DARK)
    # cabin interior
    R.rect_floor(xa, z0, xb, z1, y, CHECKER)
    R.rect_ceil(xa, z0, xb, z1, y + height, DIRTY)
    pts = [(xa, z0), (xa, z1), (xb, z1), (xb, z0)]        # clockwise seen from above
    hole_seg = 0 if s > 0 else 2                          # west wall (xa) or east wall (xb)
    a = pts[hole_seg]
    hs = span(a, (a[0], zc - 96), (a[0], zc + 96))
    R.walls(pts, y, y + height, cab, holes={hole_seg: [(hs[0], hs[1], y, y + 320)]})
    # dark kick band and a handrail round the cabin
    for (p, q) in ((1, 2), (2, 3), (3, 0), (0, 1)):
        if (p, q) == ((0, 1) if s > 0 else (2, 3)):
            continue
        pa, pb = np.array(pts[p], dtype=float), np.array(pts[q], dtype=float)
        dd = (pb - pa) / np.linalg.norm(pb - pa)
        nn = np.array([dd[1], -dd[0]])
        R.decal(pa + dd * 2, pb - dd * 2, y, y + 40, DARK, (0, 0.55, 2.0, 0.7), off=2)
        r0, r1 = pa + dd * 40 + nn * 10, pb - dd * 40 + nn * 10
        R.box(min(r0[0], r1[0]) - 3, y + 150, min(r0[1], r1[1]) - 3, max(r0[0], r1[0]) + 3, y + 158,
              max(r0[1], r1[1]) + 3, DIRTY, lux=8)
    xc = (xa + xb) / 2
    ceil_light(R, xc, zc, y + height, size=128, power=light, rng=620, color=(235, 245, 255))
    door = (wall_x + s * jamb / 2, y, zc)
    pivot = (xc, y + 240.0, zc)
    R.door_marker(door[0], y, zc, 90, color=(70, 70, 76), w=192, h=320)
    return door, pivot


def shelf_unit(R, x0, z0, x1, z1, y, height=256.0, levels=4, mat=None, back=None):
    """Open steel shelving: four uprights and `levels` boards.  Returns the top y of each board."""
    mat = mat or DIRTY
    x0, x1 = sorted((x0, x1))
    z0, z1 = sorted((z0, z1))
    for (px, pz) in ((x0, z0), (x1 - 6, z0), (x0, z1 - 6), (x1 - 6, z1 - 6)):
        R.box(px, y, pz, px + 6, y + height, pz + 6, mat, skip='B', lux=8)
    tops = []
    for i in range(levels):
        by = y + 24 + (height - 30) * i / max(1, levels - 1)
        R.box(x0, by - 6, z0, x1, by, z1, mat, lux=8)
        tops.append(by)
    if back:
        bx0, bz0, bx1, bz1 = back
        R.box(bx0, y, bz0, bx1, y + height, bz1, mat, skip='B', lux=10)
    return tops


def cabinet(R, cx, cz, y, facing, w=56.0, d=64.0, h=176.0):
    """Filing cabinet: steel box with the drawer front texture on the side that faces `facing`."""
    if facing in 'NS':
        x0, x1, z0, z1 = cx - w / 2, cx + w / 2, cz - d / 2, cz + d / 2
    else:
        x0, x1, z0, z1 = cx - d / 2, cx + d / 2, cz - w / 2, cz + w / 2
    R.box(x0, y, z0, x1, y + h, z1, DIRTY, skip='B' + facing, lux=10)
    fr = (0.0, 0.0, 1.0, 1.0)
    if facing == 'S':
        R.quad(V(x0, y, z0), V(x1, y, z0), V(x1, y + h, z0), V(x0, y + h, z0), CABINET, uvrect=fr, lux=8)
    elif facing == 'N':
        R.quad(V(x1, y, z1), V(x0, y, z1), V(x0, y + h, z1), V(x1, y + h, z1), CABINET, uvrect=fr, lux=8)
    elif facing == 'E':
        R.quad(V(x1, y, z0), V(x1, y, z1), V(x1, y + h, z1), V(x1, y + h, z0), CABINET, uvrect=fr, lux=8)
    else:
        R.quad(V(x0, y, z1), V(x0, y, z0), V(x0, y + h, z0), V(x0, y + h, z1), CABINET, uvrect=fr, lux=8)


def cabinet_row(R, a, b, y, facing, w=56.0):
    """A run of filing cabinets from a to b (centres along the back line)."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    L = np.linalg.norm(b - a)
    n = int(max(1, L // w))
    d = (b - a) / L
    for i in range(n):
        c = a + d * (w * (i + 0.5))
        cabinet(R, c[0], c[1], y, facing, w=w)


def desk(R, x0, z0, x1, z1, y, h=76.0):
    """Plain office desk: wooden top on two panel legs.  Returns the top height."""
    x0, x1 = sorted((x0, x1))
    z0, z1 = sorted((z0, z1))
    R.box(x0, y + h - 8, z0, x1, y + h, z1, WOOD, lux=8)
    if (x1 - x0) >= (z1 - z0):
        R.box(x0 + 6, y, z0 + 6, x0 + 14, y + h - 8, z1 - 6, DIRTY, skip='TB', lux=10)
        R.box(x1 - 14, y, z0 + 6, x1 - 6, y + h - 8, z1 - 6, DIRTY, skip='TB', lux=10)
    else:
        R.box(x0 + 6, y, z0 + 6, x1 - 6, y + h - 8, z0 + 14, DIRTY, skip='TB', lux=10)
        R.box(x0 + 6, y, z1 - 14, x1 - 6, y + h - 8, z1 - 6, DIRTY, skip='TB', lux=10)
    return y + h


def end_wall(R, side, x0, x1, y1, mat, floor_mat, zwall=992.0):
    """The wall on a cell edge with the standard door hole + recess.  x0..x1 is the wall's extent
    across the doorway (given for the north side; other sides are rotated)."""
    def X(p):
        x, z = p
        return {'N': (x, z), 'S': (-x, -z), 'E': (z, -x), 'W': (-z, x)}[side]
    a, b = X((x0, zwall)), X((x1, zwall))
    hs = span(a, X((-96, zwall)), X((96, zwall)))
    R.wall(a, b, 0, y1, mat, holes=[(hs[0], hs[1], 0, 320)])
    door_neck(R, side, mat, floor_mat, zwall=zwall)
    dp = X((0, 1024.0))
    R.door_marker(dp[0], 0, dp[1], 0 if side in 'NS' else 90, color=(52, 52, 56))


def file_row(R, a, b, y, along, seed=1, fill=0.5, keep_clear=()):
    """A row of box files standing on a shelf board.  a..b is the run along `along` ('x' or 'z'),
    the other coordinate is fixed.  keep_clear = [(lo, hi)] stretches left empty for items."""
    import random
    rng = random.Random(seed)
    lo, hi, fixed = a
    pos = lo + 8
    kind = 0
    while pos < hi - 8:
        if rng.random() > fill:
            pos += rng.choice((30, 44, 60))
            continue
        run = rng.randint(3, 7)
        kind = 1 - kind
        for _ in range(run):
            if pos >= hi - 8:
                break
            if not any(c0 <= pos <= c1 for (c0, c1) in keep_clear):
                f = 'boxfile_a.x' if kind else 'boxfile_b.x'
                lean = rng.choice((0, 0, 0, 0, 8, -6))
                if along == 'x':
                    R.model(f, pos, y, fixed, rot=(0, 0, lean), scale=(3, 3, 3), size=(12, 54, 42))
                else:
                    R.model(f, fixed, y, pos, rot=(0, 90, lean), scale=(3, 3, 3), size=(42, 54, 12))
            pos += 14
        pos += rng.choice((6, 18, 34))


def crate(R, x, y, z, yaw=0, kind=1):
    if kind == 1:
        R.model('crate1.x', x, y, z, rot=(0, yaw, 0), scale=(3, 3, 3), size=(123, 78, 84))
    else:
        R.model('crate2.x', x, y, z, rot=(0, yaw, 0), scale=(4, 4, 4), size=(136, 40, 72))


def workstation(R, x, y, z, yaw=0):
    R.model('monitor.x', x, y, z, rot=(0, yaw, 0), scale=(1.6, 1.6, 1.6), size=(68, 62, 20))


# --------------------------------------------------------------------- second batch (Indev zone)
SIGNS2 = json.load(open(os.path.join(HERE, 'signs2.json'))) if os.path.exists(os.path.join(HERE, 'signs2.json')) else {}
SIGN2 = Mat('indev_signs2.png', cast=False)
MESH = Mat('indev_mesh.png', 64, alpha=True, cast=False)
CHAIN = Mat('indev_chain.png', 32, alpha=True, cast=False)
BRICK = Mat('brick_wall_texture_1789291170340.jpg', 384, 384, 384)
RUST = Mat('Pipes.jpg', 256, 256)
REDLAMP = Mat('red.jpg', 64, emit=210, cast=False)


def sign2(R, name, cx, cz, facing, w, h, yc):
    """A sign from the second sheet, centred on (cx, cz) on a wall facing N / S / E / W."""
    hw = w / 2
    if facing == 'S':
        a, b = (cx - hw, cz), (cx + hw, cz)
    elif facing == 'N':
        a, b = (cx + hw, cz), (cx - hw, cz)
    elif facing == 'E':
        a, b = (cx, cz - hw), (cx, cz + hw)
    else:
        a, b = (cx, cz + hw), (cx, cz - hw)
    R.decal(a, b, yc - h / 2, yc + h / 2, SIGN2, SIGNS2[name])


def poly_facing(R, pts, hint, mat, **kw):
    """Planar polygon given as 3D points in any winding; it is flipped so that it faces `hint`.
    UVs: wall-like (u along the horizontal run, v by height) or planar x/z for flat-ish ones."""
    P = [np.asarray(p, dtype=float) for p in pts]
    n = np.zeros(3)
    for i in range(1, len(P) - 1):
        n += np.cross(P[i + 1] - P[0], P[i] - P[0])
    if np.dot(n, np.asarray(hint, dtype=float)) < 0:
        P = P[::-1]
        n = -n
    n = norm(n)
    if abs(n[1]) < 0.7:
        h = norm(np.cross(V(0, 1, 0), n))
        uvs = [(float(p @ h) / mat.us, (mat.v0 - p[1]) / mat.vs) for p in P]
    else:
        uvs = [(p[0] / mat.us, -p[2] / mat.vs) for p in P]
    return R.add(P, uvs, mat, **kw)


def mesh_panel(R, a, b, y0, y1, coll=True):
    """Wire mesh between two xz points (drawn both ways by the game, collides like a wall)."""
    L = float(np.linalg.norm(np.asarray(b, dtype=float) - np.asarray(a, dtype=float)))
    R.quad(V(a[0], y0, a[1]), V(b[0], y0, b[1]), V(b[0], y1, b[1]), V(a[0], y1, a[1]), MESH,
           uvrect=(0, 0, L / 64.0, (y1 - y0) / 64.0), lm=False, coll=coll)


def chain(R, x, z, y_top, length):
    """A chain hanging from y_top: two crossed alpha strips, no collision."""
    for (dx, dz) in ((9, 0), (0, 9)):
        R.quad(V(x - dx, y_top - length, z - dz), V(x + dx, y_top - length, z + dz), V(x + dx, y_top, z + dz),
               V(x - dx, y_top, z - dz), CHAIN, uvrect=(0, 0, 1, length / 144.0), lm=False, coll=False)


def stairs(R, x0, x1, z0, steps, rise, run, direction, y0, mat, top=None):
    """Solid steps rising along z (direction +1 / -1) starting at z0, plus the invisible ramp the
    player actually walks on (laid over the step noses, like the vanilla stair rooms)."""
    for i in range(steps):
        za, zb = z0 + direction * i * run, z0 + direction * (i + 1) * run
        zlo, zhi = sorted((za, zb))
        R.box(x0, y0, zlo, x1, y0 + (i + 1) * rise, zhi, mat, skip='B' + ('N' if direction > 0 and i < steps - 1 else '')
              + ('S' if direction < 0 and i < steps - 1 else ''), top=top or mat, lux=10)
    zb0 = z0 - direction * run
    zt = z0 + direction * (steps - 1) * run
    yt = y0 + steps * rise
    a, b, c, d = V(x0, y0, zb0), V(x1, y0, zb0), V(x1, yt, zt), V(x0, yt, zt)
    R.collide(a, b, c, d)
    return z0 + direction * steps * run, yt
