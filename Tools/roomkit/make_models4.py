"""Models the game code moves around in the sixth batch (GFX\\npcs, room units, front = +z):
   scp1145.b3d   the Nagasaki teddy: 30 cm, faceless but for a stub of snout
   scp1080t.b3d  the pallet the broken tug left against the store door (moved by code when fixed)"""
import math
import os
import numpy as np
from b3dkit import Mesh, write_b3d

NPCDIR = r"I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9\GFX\npcs"


def sphere(m, c, r, sy=1.0, seg=10, rings=6, uv=(0, 0, 1, 1)):
    cx, cy, cz = c
    u0, v0, u1, v1 = uv

    def P(a, b):
        return (cx + r * math.cos(a) * math.cos(b), cy + r * sy * math.sin(a), cz + r * math.cos(a) * math.sin(b))
    for j in range(-rings // 2, rings // 2):
        a0, a1 = math.pi * j / rings, math.pi * (j + 1) / rings
        for i in range(seg):
            b0, b1 = 2 * math.pi * i / seg, 2 * math.pi * (i + 1) / seg
            pts = [P(a0, b0), P(a0, b1), P(a1, b1), P(a1, b0)]
            uvs = [(u0 + (u1 - u0) * i / seg, v1), (u0 + (u1 - u0) * (i + 1) / seg, v1),
                   (u0 + (u1 - u0) * (i + 1) / seg, v0), (u0 + (u1 - u0) * i / seg, v0)]
            if j == rings // 2 - 1:
                pts, uvs = pts[:3], uvs[:3]
            elif j == -rings // 2:
                pts, uvs = pts[1:], uvs[1:]
            P3 = [np.asarray(p) for p in pts]
            n = np.cross(P3[2] - P3[0], P3[1] - P3[0])
            mid = np.mean(P3, axis=0) - np.asarray(c)
            if np.dot(n, mid) < 0:
                pts, uvs = pts[::-1], uvs[::-1]
            m.poly(pts, uvs)


def teddy():
    m = Mesh()
    sphere(m, (0, 15, 0), 12, sy=1.15)          # body
    sphere(m, (0, 35, 1), 9.5)                  # head
    sphere(m, (0, 33, 9.5), 3.6, sy=0.8, seg=8, rings=4)   # the stub of snout
    for s in (-1, 1):
        sphere(m, (s * 7, 43, 0), 3.2, seg=8, rings=4)      # ears
        sphere(m, (s * 12, 20, 2), 4.2, sy=1.5, seg=8, rings=4)   # arms
        sphere(m, (s * 6, 4, 4), 4.6, sy=0.9, seg=8, rings=4)     # legs
    return m


def pallet():
    m = Mesh()
    crate = (0.51, 0.13, 0.74, 0.24)            # the SECURE STORAGE print on indev_props4.png
    wood = (0.02, 0.27, 0.48, 0.37)             # the kiosk's brown sign board, as plain wood
    m.box((0, 6, 0), 62, 6, 50, wood)
    m.box((0, 52, 0), 58, 40, 46, crate)
    m.box((0, 96, 0), 50, 4, 40, wood)
    return m


if __name__ == '__main__':
    print('teddy', write_b3d(os.path.join(NPCDIR, 'scp1145.b3d'), 'indev_teddy.png', teddy(), name='teddy'))
    print('pallet', write_b3d(os.path.join(NPCDIR, 'scp1080t.b3d'), 'indev_props4.png', pallet(), name='pallet'))
