r"""SCP-113's model: a small polished red jasper pebble, written as a Blitz3D .b3d (GFX\items\scp113.b3d).
The old file was a copy of SCP-348's bowl. The pebble is a flattened, slightly lumpy sphere with sphere-mapped UVs
for GFX\items\scp113.png (the item's "texture override"). It is sized like the old model so items.ini's scale
(0.0009) still fits. The old file is kept as scp113.b3d.bak_bowl.
   python make_scp113.py"""
import math
import os
import random
import shutil
import struct

ROOT = r'I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9'
OUT = os.path.join(ROOT, 'GFX', 'items', 'scp113.b3d')


def chunk(tag, body):
    return tag + struct.pack('<i', len(body)) + body


def cstr(s):
    return s.encode('latin-1') + b'\0'


def old_extent(path):
    """the half-size of the old model, from its VRTS chunk (normals and one 2D uv set)"""
    d = open(path, 'rb').read()
    i = d.find(b'VRTS')
    n = struct.unpack('<i', d[i + 4:i + 8])[0]
    fl, ts, tc = struct.unpack('<3i', d[i + 8:i + 20])
    stride = 12 + (12 if fl & 1 else 0) + (16 if fl & 2 else 0) + 4 * ts * tc
    xs, ys, zs = [], [], []
    for k in range((n - 12) // stride):
        x, y, z = struct.unpack('<3f', d[i + 20 + k * stride:i + 32 + k * stride])
        xs.append(x); ys.append(y); zs.append(z)
    return max(max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs)) / 2


def pebble(radius, rings=10, segs=16):
    rnd = random.Random(113)
    bumps = [(rnd.uniform(0, 2 * math.pi), rnd.uniform(0, math.pi), rnd.uniform(0.04, 0.09)) for _ in range(6)]
    verts, tris = [], []
    for i in range(rings + 1):
        v = i / rings
        th = v * math.pi
        for j in range(segs + 1):
            u = j / segs
            ph = u * 2 * math.pi
            nx, ny, nz = math.sin(th) * math.cos(ph), math.cos(th), math.sin(th) * math.sin(ph)
            r = 1.0
            for bp, bt, ba in bumps:                                   # a few soft lumps
                dot = math.sin(th) * math.sin(bt) * math.cos(ph - bp) + math.cos(th) * math.cos(bt)
                r += ba * max(0.0, dot) ** 3
            x, y, z = nx * r * radius * 1.15, ny * r * radius * 0.55, nz * r * radius * 0.9   # flattened, oval
            verts.append((x, y, z, nx, ny, nz, u, v))
    for i in range(rings):
        for j in range(segs):
            a = i * (segs + 1) + j
            b = a + segs + 1
            tris.append((a, b, a + 1))
            tris.append((a + 1, b, b + 1))
    return verts, tris


def write(path, verts, tris):
    texs = chunk(b'TEXS', cstr('scp113.png') + struct.pack('<2i5f', 1, 2, 0, 0, 1, 1, 0))
    brus = chunk(b'BRUS', struct.pack('<i', 1) + cstr('jasper') + struct.pack('<5f2i', 1, 1, 1, 1, 0.6, 1, 0) + struct.pack('<i', 0))
    vb = struct.pack('<3i', 1, 1, 2) + b''.join(struct.pack('<8f', *v) for v in verts)
    tb = struct.pack('<i', 0) + b''.join(struct.pack('<3i', *t) for t in tris)
    mesh = chunk(b'MESH', struct.pack('<i', 0) + chunk(b'VRTS', vb) + chunk(b'TRIS', tb))
    node = chunk(b'NODE', cstr('scp113') + struct.pack('<10f', 0, 0, 0, 1, 1, 1, 1, 0, 0, 0) + mesh)
    open(path, 'wb').write(chunk(b'BB3D', struct.pack('<i', 1) + texs + brus + node))


if __name__ == '__main__':
    src = OUT + '.bak_bowl' if os.path.exists(OUT + '.bak_bowl') else OUT
    half = old_extent(src)
    if not os.path.exists(OUT + '.bak_bowl'):
        shutil.copy2(OUT, OUT + '.bak_bowl')
    v, t = pebble(half * 0.9)
    write(OUT, v, t)
    print('scp113.b3d: %d vertices, %d triangles, radius %.1f (old half-size %.1f)' % (len(v), len(t), half * 0.9, half))
