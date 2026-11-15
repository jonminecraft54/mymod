"""Models for the eighth batch (GFX\\npcs, room units, front = +z, origin on the floor):
   scp956.b3d        the pinata: a four-legged paper animal in rings of crepe fringe
   indev_unicycle.b3d  Sir Nicholas's unicycle
   scp4255s.b3d      SCP-4255-1 (the replica): a red and gold sleigh on curled runners, temporal coils at the back
   indev_reindeer.b3d  one of the eight heat-proof reindeer models
   scp1225.b3d       the glass ornament (a spindle with a cap and a loop)
   indev_parcel.b3d  a St. Nick package"""
import math
import os
import numpy as np
from b3dkit import Mesh, write_b3d
from make_models5 import tones, band, ellipsoid, tail, pf
from make_models4 import sphere

NPCDIR = r"I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9\GFX\npcs"


def pinata():
    m = Mesh()
    n = 6
    B = [band(k, n) for k in range(n)]
    # fringe rings round the body, each its own colour
    for k in range(9):
        z = -46 + k * 11.5
        m.cyl((0, 70, z - 5), (0, 70, z + 5), 30 - abs(k - 4) * 1.6, 33 - abs(k - 4) * 1.6, sides=14, uvrect=B[k % 5], caps=(k in (0, 8)))
    for k in range(4):
        y = 92 + k * 9
        m.cyl((0, y, 50), (0, y + 9, 60), 13 - k * 0.5, 14 - k * 0.5, sides=10, uvrect=B[(k + 2) % 5], caps=False)
    ellipsoid(m, (0, 130, 70), 14, 13, 18, B[0], seg=10, rings=6)            # head
    m.cyl((0, 126, 82), (0, 122, 100), 8, 6, sides=8, uvrect=B[1])          # snout
    for s in (-1, 1):
        sphere(m, (s * 7, 134, 84), 2.6, seg=6, rings=4, uv=B[5])          # eyes
        m.cyl((s * 7, 140, 66), (s * 10, 166, 62), 4, 1.5, sides=6, uvrect=B[2])   # ears
        for z in (-34, 34):
            m.cyl((s * 18, 0, z), (s * 18, 52, z), 6, 7, sides=8, uvrect=B[(z > 0) + 3])
    tail(m, [(0, 74, -50), (0, 70, -64), (0, 58, -72)], 3.5, 1.5, B[4])
    return m


def unicycle():
    m = Mesh()
    T, Mt, S = band(0, 3), band(1, 3), band(2, 3)
    r = 28.0
    # the tyre: a ring of short segments round the axle (axle along x)
    seg = 16
    for i in range(seg):
        a0, a1 = 2 * math.pi * i / seg, 2 * math.pi * (i + 1) / seg
        p0 = (0, r + r * math.sin(a0), r * math.cos(a0))
        p1 = (0, r + r * math.sin(a1), r * math.cos(a1))
        m.cyl(p0, p1, 3.2, sides=6, uvrect=T, caps=False)
    for i in range(8):
        a = 2 * math.pi * i / 8
        m.cyl((0, r, 0), (0, r + (r - 3) * math.sin(a), (r - 3) * math.cos(a)), 0.8, sides=4, uvrect=Mt, caps=False)
    for s in (-1, 1):
        m.cyl((s * 5, r, 0), (s * 4, 72, 0), 1.4, sides=6, uvrect=Mt)       # the fork
    m.cyl((0, 70, 0), (0, 98, -2), 1.8, sides=6, uvrect=Mt)
    ellipsoid(m, (0, 101, -2), 7, 3, 13, S, seg=10, rings=4)              # seat
    for s in (-1, 1):
        m.cyl((s * 6, r, 0), (s * 10, r + 8, 6), 1.0, sides=4, uvrect=Mt)
        m.box((s * 11, r + 8, 7), 1.5, 1, 4, uvrect=S)                      # pedals
    return m


def sleigh():
    m = Mesh()
    R, G, Bk, Glow = band(0, 4), band(1, 4), band(2, 4), band(3, 4)
    # the body: a tub, lower at the front, a high curled dash and a tall back
    m.box((0, 70, -20), 72, 34, 110, uvrect=R)
    m.box((0, 112, -112), 72, 50, 14, uvrect=R)                            # the seat back
    m.box((0, 118, -92), 64, 6, 22, uvrect=Bk)                             # the seat
    for k in range(10):                                                    # the dash scrolls up and over at the front
        a0, a1 = math.pi * k / 10, math.pi * (k + 1) / 10
        y0, z0 = 104 + 40 * math.sin(a0), 90 + 26 * math.cos(a0) - 26
        y1, z1 = 104 + 40 * math.sin(a1), 90 + 26 * math.cos(a1) - 26
        pf(m, [(-72, y0, z0), (72, y0, z0), (72, y1, z1), (-72, y1, z1)], (0, math.sin((a0 + a1) / 2), math.cos((a0 + a1) / 2)), [(R[0], R[3]), (R[2], R[3]), (R[2], R[1]), (R[0], R[1])])
    for s in (-1, 1):
        # gold trim along the top edges and a scroll on each side
        m.box((s * 73, 104, -20), 2.5, 3, 110, uvrect=G)
        m.box((s * 73, 46, -20), 2.5, 3, 110, uvrect=G)
        for k in range(6):
            a = k / 6.0 * 2 * math.pi
            m.box((s * 74, 76 + 14 * math.sin(a), 20 + 14 * math.cos(a)), 1.5, 3, 3, uvrect=G)
        # runners: down from the body, along the floor, curling up in front
        pts = [(s * 58, 36, -126), (s * 58, 6, -110), (s * 58, 3, -40), (s * 58, 3, 60), (s * 58, 10, 120), (s * 58, 40, 150), (s * 58, 70, 140), (s * 58, 74, 118)]
        tail(m, pts, 5, 3.5, G, sides=6)
        for z in (-80, 0, 80):
            m.cyl((s * 58, 6, z), (s * 50, 36, z), 3, sides=6, uvrect=G)
    # the Department of Chronology's temporal coils on the back
    for s in (-1, 1):
        m.cyl((s * 34, 130, -128), (s * 34, 176, -128), 12, sides=10, uvrect=Glow)
        for k in range(4):
            m.cyl((s * 34, 136 + k * 10, -128), (s * 34, 140 + k * 10, -128), 15, sides=10, uvrect=G, caps=False)
    return m


def reindeer():
    m = Mesh()
    Br, Wt, Dk, Rd = band(0, 4), band(1, 4), band(2, 4), band(3, 4)
    ellipsoid(m, (0, 92, 0), 20, 22, 46, Br, seg=12, rings=6)
    ellipsoid(m, (0, 88, 30), 17, 20, 18, Wt, seg=10, rings=6)            # pale chest
    m.cyl((0, 104, 34), (0, 136, 56), 11, 9, sides=8, uvrect=Br)          # neck
    ellipsoid(m, (0, 140, 64), 10, 10, 16, Br, seg=10, rings=6)            # head
    m.cyl((0, 136, 74), (0, 132, 86), 7, 5, sides=8, uvrect=Dk)
    for s in (-1, 1):
        sphere(m, (s * 7, 144, 72), 2, seg=6, rings=4, uv=Dk)
        for z in (-32, 30):
            m.cyl((s * 12, 0, z), (s * 13, 72, z * 0.9), 4.5, 6, sides=6, uvrect=Br)
            m.cyl((s * 12, 0, z), (s * 12, 8, z), 5, 5, sides=6, uvrect=Dk)
        # antlers: a main beam with three tines
        base = (s * 6, 150, 60)
        tip = (s * 26, 190, 40)
        tail(m, [base, (s * 16, 170, 56), tip], 2.6, 1.4, Wt, sides=5)
        for (f, dz, dy) in ((0.4, 12, 14), (0.7, 14, 16), (0.95, -6, 18)):
            p = (base[0] + (tip[0] - base[0]) * f, base[1] + (tip[1] - base[1]) * f, base[2] + (tip[2] - base[2]) * f)
            m.cyl(p, (p[0] + s * 3, p[1] + dy, p[2] + dz), 1.6, 0.6, sides=5, uvrect=Wt)
    m.cyl((-22, 96, 10), (22, 96, 10), 23, sides=12, uvrect=Rd, caps=False)   # the harness band
    tail(m, [(0, 100, -44), (0, 96, -54)], 4, 2, Wt)
    return m


def ornament():
    m = Mesh()
    Gl, Gd, Ag = band(0, 3), band(1, 3), band(2, 3)
    prof = [(0, 0.5), (3, 2.0), (7, 4.0), (11, 5.2), (14, 5.0), (17, 3.6), (19, 2.4), (20, 2.2)]
    for (ya, ra), (yb, rb) in zip(prof[:-1], prof[1:]):
        m.cyl((0, -ya, 0), (0, -yb, 0), ra, rb, sides=10, uvrect=Gd if 9 < ya < 13 else Gl, caps=False)
    m.cyl((0, 0, 0), (0, 3, 0), 1.6, sides=8, uvrect=Ag)
    for i in range(8):
        a0, a1 = 2 * math.pi * i / 8, 2 * math.pi * (i + 1) / 8
        m.cyl((0, 4 + 1.6 * math.sin(a0), 1.6 * math.cos(a0)), (0, 4 + 1.6 * math.sin(a1), 1.6 * math.cos(a1)), 0.35, sides=4, uvrect=Ag, caps=False)
    return m


def parcel():
    m = Mesh()
    P, S = (0.51, 0.01, 0.74, 0.12), (0.52, 0.06, 0.53, 0.07)
    m.box((0, 15, 0), 20, 15, 26, uvrect=P)
    m.box((0, 15, 0), 20.6, 15.6, 2, uvrect=S)
    m.box((0, 15, 0), 2, 15.6, 26.6, uvrect=S)
    return m


def write_all():
    tones('indev_pinata.png', [(240, 80, 150), (250, 210, 50), (80, 170, 240), (100, 200, 90), (250, 140, 50), (20, 20, 20)], 956, fur=0.7)
    tones('indev_unicycle.png', [(30, 30, 32), (190, 192, 196), (170, 30, 30)], 6895)
    tones('indev_sleigh.png', [(176, 24, 28), (226, 186, 72), (30, 22, 20), (120, 200, 255)], 4255)
    tones('indev_reindeer.png', [(110, 76, 48), (226, 214, 190), (40, 30, 24), (190, 30, 30)], 8, fur=0.5)
    tones('indev_ornament.png', [(200, 30, 40), (230, 190, 80), (200, 200, 206)], 1225)
    out = [('scp956.b3d', 'indev_pinata.png', pinata()), ('indev_unicycle.b3d', 'indev_unicycle.png', unicycle()),
           ('scp4255s.b3d', 'indev_sleigh.png', sleigh()), ('indev_reindeer.b3d', 'indev_reindeer.png', reindeer()),
           ('scp1225.b3d', 'indev_ornament.png', ornament()), ('indev_parcel.b3d', 'indev_props6.png', parcel())]
    for fn, tex, mesh in out:
        nv, nt = write_b3d(os.path.join(NPCDIR, fn), tex, mesh, name=fn.split('.')[0])
        print('%-20s %5d verts %5d tris' % (fn, nv, nt))
    return out


if __name__ == '__main__':
    write_all()
