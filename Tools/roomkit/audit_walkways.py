"""Find solid geometry that stands in the walkway of a mod room: the player's path through the hub and the arms.
Two strips are checked, the north-south path (|x| < HW, |z| < ZL) and the east-west path (|z| < HW, |x| < ZL), at
body height. A solid triangle that overlaps a strip (exact triangle-rectangle test, in the xz plane) and reaches the
body's height is reported. Door holes are not solid, so a wall with an open hole is not reported.
   python audit_walkways.py            every mod room made after the vanilla maps (mtime > 2025-09-08)
   python audit_walkways.py NAME ...   just those rooms, with every blocking triangle listed"""
import datetime
import glob
import os
import sys
from rmesh import read_rmesh

MAP = r"I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9\GFX\map"
HW = 40.0          # half-width of a walkway in room units (a player needs about 38 either side)
ZL = 900.0         # the strips stop short of the cell edges, where the doors are
Y0, Y1 = 4.0, 70.0  # body height in room units


def _axis_overlap(tri, lo, hi, axis):
    proj = [p[axis] for p in tri]
    return not (max(proj) < lo or min(proj) > hi)


def _tri_rect(tri, x0, x1, z0, z1):
    """separating-axis test between a 2D triangle (x, z) and an axis-aligned rectangle"""
    if not (_axis_overlap(tri, x0, x1, 0) and _axis_overlap(tri, z0, z1, 1)):
        return False
    for i in range(3):
        a, b = tri[i], tri[(i + 1) % 3]
        nx, nz = -(b[1] - a[1]), (b[0] - a[0])
        if abs(nx) + abs(nz) < 1e-9:
            continue
        pt = [p[0] * nx + p[1] * nz for p in tri]
        rc = [x * nx + z * nz for x in (x0, x1) for z in (z0, z1)]
        if max(pt) < min(rc) or min(pt) > max(rc):
            return False
    return True


STRIPS = [('NS', -HW, HW, -ZL, ZL), ('EW', -256.0, 256.0, -HW, HW)]     # the hub and the door passages
TALL = 250.0     # taller than this is a wall, which is not in the way; shorter is furniture or a fitting


def blockers(path):
    d = read_rmesh(path)
    out = []
    for src in list(d['meshes']) + list(d['hidden']):
        vs, ts = src['verts'], src['tris']
        for t in ts:
            p = [vs[i] for i in t]
            ys = [q[2 - 1] if False else q[1] for q in p]
            if max(ys) < Y0 or min(ys) > Y1:
                continue
            if max(ys) - min(ys) < 2.0 or max(ys) - min(ys) >= TALL:
                continue
            tri = [(q[0], q[2]) for q in p]
            for name, x0, x1, z0, z1 in STRIPS:
                if _tri_rect(tri, x0, x1, z0, z1):
                    out.append((name, round(min(q[0] for q in tri)), round(max(q[0] for q in tri)),
                                round(min(q[1] for q in tri)), round(max(q[1] for q in tri)),
                                round(min(ys)), round(max(ys))))
                    break
    return out


def summary(path):
    hits = blockers(path)
    return hits


if __name__ == '__main__':
    if len(sys.argv) > 1:
        names = sys.argv[1:]
        files = [os.path.join(MAP, n + '.rmesh') for n in names]
    else:
        cut = datetime.datetime(2025, 9, 8).timestamp()
        files = sorted(f for f in glob.glob(os.path.join(MAP, '*.rmesh')) if os.path.getmtime(f) > cut)
    bad = {}
    for f in files:
        h = summary(f)
        if h:
            bad[os.path.basename(f)[:-6]] = h
    for name in sorted(bad):
        h = bad[name]
        print('%-28s %3d blocking triangles, first: %s x %s..%s z %s..%s y %s..%s' % ((name, len(h), h[0][0]) + h[0][1:]))
    print('%d of %d mod rooms have solid geometry in a walkway' % (len(bad), len(files)))
