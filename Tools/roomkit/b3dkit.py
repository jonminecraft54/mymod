"""Minimal Blitz3D .b3d writer: one node, one mesh, one texture, vertex normals + 1 UV set."""
import struct
import math
import numpy as np


def _chunk(tag, payload):
    return tag + struct.pack('<i', len(payload)) + payload


def _cstr(s):
    return s.encode('latin-1') + b'\x00'


class Mesh:
    def __init__(self):
        self.v = []   # (x,y,z, nx,ny,nz, u,v)
        self.t = []

    def poly(self, pts, uvs, double=False):
        """Convex polygon, points counter-clockwise seen from the front (same rule as roomkit)."""
        pts = [np.asarray(p, dtype=np.float64) for p in pts]
        n = np.zeros(3)
        for i in range(1, len(pts) - 1):
            n += np.cross(pts[i + 1] - pts[0], pts[i] - pts[0])
        ln = np.linalg.norm(n)
        n = n / ln if ln > 1e-12 else np.array([0.0, 1.0, 0.0])
        b = len(self.v)
        for p, uv in zip(pts, uvs):
            self.v.append((p[0], p[1], p[2], n[0], n[1], n[2], uv[0], uv[1]))
        for i in range(1, len(pts) - 1):
            self.t.append((b, b + i + 1, b + i))
        if double:
            b = len(self.v)
            for p, uv in zip(pts, uvs):
                self.v.append((p[0], p[1], p[2], -n[0], -n[1], -n[2], uv[0], uv[1]))
            for i in range(1, len(pts) - 1):
                self.t.append((b, b + i, b + i + 1))

    def quad(self, bl, br, tr, tl, uvrect=(0, 0, 1, 1), double=False):
        u0, v0, u1, v1 = uvrect
        self.poly([bl, br, tr, tl], [(u0, v1), (u1, v1), (u1, v0), (u0, v0)], double)

    def box(self, c, hx, hy, hz, uvrect=(0, 0, 1, 1)):
        c = np.asarray(c, dtype=np.float64)
        X, Y, Z = np.array([hx, 0, 0.0]), np.array([0, hy, 0.0]), np.array([0, 0, hz * 1.0])
        for (o, r, u) in ((-Z, X, Y), (Z, -X, Y), (X, Z, Y), (-X, -Z, Y), (Y, X, Z), (-Y, X, -Z)):
            if np.dot(np.cross(u, r), o) < 0:
                r = -r
            self.quad(c + o - r - u, c + o + r - u, c + o + r + u, c + o - r + u, uvrect)

    def cyl(self, p0, p1, r0, r1=None, sides=12, uvrect=(0, 0, 1, 1), caps=True, capuv=None):
        p0 = np.asarray(p0, dtype=np.float64)
        p1 = np.asarray(p1, dtype=np.float64)
        r1 = r0 if r1 is None else r1
        ax = (p1 - p0) / np.linalg.norm(p1 - p0)
        ref = np.array([0, 1.0, 0]) if abs(ax[1]) < 0.9 else np.array([1.0, 0, 0])
        e1 = np.cross(ax, ref)
        e1 /= np.linalg.norm(e1)
        e2 = np.cross(ax, e1)
        u0, v0, u1, v1 = uvrect
        dirs = [e1 * math.cos(2 * math.pi * i / sides) + e2 * math.sin(2 * math.pi * i / sides) for i in range(sides + 1)]
        for i in range(sides):
            a, b = dirs[i], dirs[i + 1]
            bl, br, tr, tl = p0 + a * r0, p0 + b * r0, p1 + b * r1, p1 + a * r1
            ua, ub = u0 + (u1 - u0) * i / sides, u0 + (u1 - u0) * (i + 1) / sides
            uvs = [(ua, v1), (ub, v1), (ub, v0), (ua, v0)]
            pts = [bl, br, tr, tl]
            if np.dot(np.cross(tl - bl, br - bl), a + b) < 0:
                pts = pts[::-1]
                uvs = uvs[::-1]
            self.poly(pts, uvs)
        if caps:
            cu0, cv0, cu1, cv1 = capuv or uvrect
            for (pc, rr, sgn) in ((p0, r0, -1), (p1, r1, 1)):
                if rr < 1e-6:
                    continue
                pts = [pc + d * rr for d in dirs[:-1]]
                uvs = [((cu0 + cu1) / 2 + (cu1 - cu0) / 2 * math.cos(2 * math.pi * i / sides),
                        (cv0 + cv1) / 2 + (cv1 - cv0) / 2 * math.sin(2 * math.pi * i / sides)) for i in range(sides)]
                if np.dot(np.cross(pts[2] - pts[0], pts[1] - pts[0]), ax * sgn) < 0:
                    pts = pts[::-1]
                    uvs = uvs[::-1]
                self.poly(pts, uvs)


def write_b3d(path, texture, mesh, name='mesh', fx=0, shininess=0.0):
    texs = _cstr(texture) + struct.pack('<ii', 1, 2) + struct.pack('<fffff', 0, 0, 1, 1, 0)
    brus = struct.pack('<i', 1) + _cstr('mat') + struct.pack('<ffff', 1, 1, 1, 1) + struct.pack('<f', shininess) \
        + struct.pack('<ii', 1, fx) + struct.pack('<i', 0)
    vr = struct.pack('<iii', 1, 1, 2)
    for v in mesh.v:
        vr += struct.pack('<8f', *v)
    tr = struct.pack('<i', 0)
    for t in mesh.t:
        tr += struct.pack('<3i', *t)
    m = struct.pack('<i', -1) + _chunk(b'VRTS', vr) + _chunk(b'TRIS', tr)
    node = _cstr(name) + struct.pack('<3f', 0, 0, 0) + struct.pack('<3f', 1, 1, 1) + struct.pack('<4f', 1, 0, 0, 0) \
        + _chunk(b'MESH', m)
    body = struct.pack('<i', 1) + _chunk(b'TEXS', texs) + _chunk(b'BRUS', brus) + _chunk(b'NODE', node)
    with open(path, 'wb') as f:
        f.write(_chunk(b'BB3D', body))
    return len(mesh.v), len(mesh.t)
