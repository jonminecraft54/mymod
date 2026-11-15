"""Fan rotors for the new rooms (unit radius, scaled in FillRoom):
   GFX\\map\\indev_fan.b3d       axial duct fan, 5 pitched blades, spins round its local Z
   GFX\\map\\indev_ceilfan.b3d   ceiling fan, 4 long blades, spins round its local Y
   GFX\\map\\indev_fan.png       shared texture: left half blade, right half hub
"""
import math
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from b3dkit import Mesh, write_b3d

MAPDIR = r"I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9\GFX\map"


def texture():
    W = H = 256
    rng = np.random.default_rng(15)
    a = np.zeros((H, W, 3))
    # blade: brushed dark steel, lighter leading edge, hazard-yellow tip, grime towards the root
    v = np.linspace(0, 1, H)[:, None]
    u = np.linspace(0, 1, W // 2)[None, :]
    base = 92 + 26 * np.sin(u * 3.0) + rng.normal(0, 5, (H, W // 2))
    streak = np.asarray(Image.fromarray((rng.random((H, 1)) * 255).astype(np.uint8)).resize((W // 2, H))).astype(float)
    base += (streak - 128) * 0.10
    base *= 0.72 + 0.28 * v
    base += 40 * np.exp(-(u / 0.07) ** 2)
    blade = np.stack([base * 0.98, base, base * 1.04], axis=2)
    tip = (v > 0.90)
    blade = np.where(tip[..., None], np.array([196.0, 160.0, 24.0])[None, None, :] * (0.8 + 0.2 * rng.random((H, W // 2, 1))), blade)
    for y in range(0, H, 9):       # diagonal hazard hatching on the tip
        pass
    a[:, :W // 2] = blade
    # hub: dark disc with a bolt circle
    hub = Image.new('RGB', (W // 2, H), (38, 38, 40))
    d = ImageDraw.Draw(hub)
    cx, cy = W // 4, H // 2
    d.ellipse([cx - 58, cy - 58, cx + 58, cy + 58], fill=(74, 74, 78), outline=(20, 20, 20), width=3)
    d.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], fill=(110, 110, 114), outline=(25, 25, 25), width=2)
    for i in range(6):
        ang = i * math.pi / 3
        bx, by = cx + 40 * math.cos(ang), cy + 40 * math.sin(ang)
        d.ellipse([bx - 5, by - 5, bx + 5, by + 5], fill=(150, 150, 150), outline=(20, 20, 20))
    hub = np.asarray(hub.filter(ImageFilter.GaussianBlur(0.6))).astype(float)
    hub += rng.normal(0, 4, hub.shape)
    a[:, W // 2:] = hub
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(os.path.join(MAPDIR, 'indev_fan.png'))


def axial():
    m = Mesh()
    HUB = (0.5, 0.0, 1.0, 1.0)
    BL = (0.0, 0.0, 0.5, 1.0)
    m.cyl((0, 0, -0.16), (0, 0, 0.16), 0.24, sides=14, uvrect=(0.52, 0.05, 0.98, 0.2), capuv=HUB)
    m.cyl((0, 0, 0.16), (0, 0, 0.30), 0.24, 0.08, sides=14, uvrect=(0.52, 0.05, 0.98, 0.2), caps=False)
    n = 5
    for i in range(n):
        ang = 2 * math.pi * i / n
        rad = np.array([math.cos(ang), math.sin(ang), 0.0])
        tan = np.array([-math.sin(ang), math.cos(ang), 0.0])
        ax = np.array([0.0, 0.0, 1.0])
        pts, uvs = [], []
        rows = 4
        for k in range(rows + 1):
            t = k / rows
            r = 0.20 + 0.78 * t
            half = 0.16 + 0.17 * math.sin(t * math.pi * 0.85)       # blade chord widens then tapers
            pitch = math.radians(38 - 20 * t)
            chord = tan * math.cos(pitch) + ax * math.sin(pitch)
            pts.append((rad * r - chord * half, rad * r + chord * half))
            uvs.append(t)
        for k in range(rows):
            (a0, b0), (a1, b1) = pts[k], pts[k + 1]
            m.poly([a0, b0, b1, a1], [(0.02, uvs[k]), (0.48, uvs[k]), (0.48, uvs[k + 1]), (0.02, uvs[k + 1])], double=True)
    return m


def ceiling():
    m = Mesh()
    HUB = (0.5, 0.0, 1.0, 1.0)
    m.cyl((0, -0.07, 0), (0, 0.07, 0), 0.15, sides=14, uvrect=(0.52, 0.05, 0.98, 0.2), capuv=HUB)
    m.cyl((0, -0.12, 0), (0, -0.07, 0), 0.06, 0.15, sides=14, uvrect=(0.52, 0.05, 0.98, 0.2), caps=False)
    n = 4
    for i in range(n):
        ang = 2 * math.pi * i / n
        rad = np.array([math.cos(ang), 0.0, math.sin(ang)])
        tan = np.array([-math.sin(ang), 0.0, math.cos(ang)])
        up = np.array([0.0, 1.0, 0.0])
        pitch = math.radians(12)
        chord = tan * math.cos(pitch) + up * math.sin(pitch)
        r0, r1, half = 0.14, 1.0, 0.085
        # the arm, then the paddle
        a0, b0 = rad * r0 - chord * 0.03, rad * r0 + chord * 0.03
        a1, b1 = rad * 0.34 - chord * 0.03, rad * 0.34 + chord * 0.03
        m.poly([a0, b0, b1, a1], [(0.52, 0.9), (0.60, 0.9), (0.60, 0.98), (0.52, 0.98)], double=True)
        p0, q0 = rad * 0.32 - chord * half, rad * 0.32 + chord * half
        p1, q1 = rad * r1 - chord * (half * 1.25), rad * r1 + chord * (half * 1.25)
        m.poly([p0, q0, q1, p1], [(0.02, 0.0), (0.48, 0.0), (0.48, 0.88), (0.02, 0.88)], double=True)
    return m


if __name__ == '__main__':
    texture()
    print('indev_fan.b3d', write_b3d(os.path.join(MAPDIR, 'indev_fan.b3d'), 'indev_fan.png', axial(), name='fan'))
    print('indev_ceilfan.b3d', write_b3d(os.path.join(MAPDIR, 'indev_ceilfan.b3d'), 'indev_fan.png', ceiling(), name='ceilfan'))
