"""Models the game code loads for the "sixteen SCPs" batch (GFX\\npcs):
   indev_bear.b3d     what SCP-1313 solves to      (front = +z, room units, origin on the floor)
   scp1515.b3d        a springhare-like rodent
   scp1513.b3d        the potted pet that was looked after
   scp1513b.b3d       the one that was not
All are built in room units, so the code scales them by RoomScale."""
import os
import numpy as np
from PIL import Image
from b3dkit import Mesh, write_b3d

NPCDIR = r"I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9\GFX\npcs"


def two_tone(name, left, right, seed):
    rng = np.random.default_rng(seed)
    a = np.zeros((64, 128, 3), dtype=float)
    a[:, :64] = left
    a[:, 64:] = right
    a += rng.normal(0, 9, (64, 128, 1))
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(os.path.join(NPCDIR, name))


A = (0.02, 0.05, 0.48, 0.95)      # left half of a two-tone texture
B = (0.52, 0.05, 0.98, 0.95)      # right half


def bear():
    m = Mesh()
    m.box((0, 150, 0), 72, 62, 132)
    m.box((0, 212, 58), 56, 26, 52)
    m.box((0, 176, 168), 44, 40, 42)
    m.box((0, 158, 222), 23, 19, 24)
    for s in (-1, 1):
        m.box((s * 34, 222, 150), 11, 12, 6)
        for z in (-92, 96):
            m.cyl((s * 48, 0, z), (s * 48, 104, z), 30, 26, sides=8)
    return m


def rodent():
    m = Mesh()
    m.box((0, 24, 0), 12, 12, 22)
    m.box((0, 37, 27), 9, 9, 10)
    m.box((0, 33, 39), 4, 4, 4)
    m.box((0, 10, 5), 8, 5, 9)                       # the pouch
    for s in (-1, 1):
        m.box((s * 5, 55, 24), 2.5, 10, 1.5)
        m.cyl((s * 9, 0, -12), (s * 9, 20, -8), 5, 6, sides=6)
        m.cyl((s * 7, 12, 16), (s * 7, 22, 14), 2.5, 3, sides=6)
    m.cyl((0, 22, -22), (0, 34, -64), 3.5, 1.5, sides=6)
    return m


def pet():
    m = Mesh()
    m.cyl((0, 0, 0), (0, 32, 0), 22, 29, sides=10, uvrect=B, capuv=B)
    m.box((0, 64, 0), 16, 14, 26, uvrect=A)
    m.box((0, 86, 30), 13, 12, 12, uvrect=A)
    m.box((0, 82, 44), 6, 5, 5, uvrect=A)
    for s in (-1, 1):
        m.box((s * 8, 102, 30), 4, 7, 2.5, uvrect=A)
        for z in (-16, 16):
            m.cyl((s * 9, 30, z * 0.6), (s * 10, 52, z), 3.5, 4, sides=6, uvrect=A)
    m.cyl((0, 70, -26), (0, 98, -46), 4, 1.5, sides=6, uvrect=A)
    for i in range(8):                                # a ruff of leaves round the neck
        a = i * np.pi / 4
        c, s = np.cos(a), np.sin(a)
        m.quad((c * 6 - s * 5, 80 + s * 6 + c * 5 - 80 + 80, 18), (c * 6 + s * 5, 80 + s * 6 - c * 5, 18),
               (c * 24 + s * 5, 80 + s * 24 - c * 5, 14), (c * 24 - s * 5, 80 + s * 24 + c * 5, 14), uvrect=A, double=True)
    return m


def feral():
    m = Mesh()
    m.box((0, 44, 0), 9, 8, 26, uvrect=A)
    m.box((0, 60, 30), 9, 9, 10, uvrect=A)
    for s in (-1, 1):
        m.box((s * 6, 76, 30), 2, 9, 2, uvrect=B)
        for z in (-20, 0, 20):
            m.cyl((s * 30, 0, z * 1.5), (s * 8, 40, z), 2.5, 3.5, sides=5, uvrect=B)
    m.cyl((0, 46, -26), (0, 20, -70), 4, 1, sides=5, uvrect=B)
    return m


if __name__ == '__main__':
    two_tone('scp1513.png', (72, 140, 52), (170, 96, 60), 1)
    two_tone('scp1513b.png', (104, 96, 50), (60, 44, 30), 2)
    print('bear', write_b3d(os.path.join(NPCDIR, 'indev_bear.b3d'), 'indev_bear.png', bear(), name='bear'))
    print('rodent', write_b3d(os.path.join(NPCDIR, 'scp1515.b3d'), 'indev_rodent.png', rodent(), name='rodent'))
    print('pet', write_b3d(os.path.join(NPCDIR, 'scp1513.b3d'), 'scp1513.png', pet(), name='pet'))
    print('feral', write_b3d(os.path.join(NPCDIR, 'scp1513b.b3d'), 'scp1513b.png', feral(), name='feral'))
