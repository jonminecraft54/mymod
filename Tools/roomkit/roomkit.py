"""roomkit - procedural SCP:CB room builder.

Builds a room out of planar surfaces, bakes a lightmap for it (direct light with
soft shadows + ambient occlusion + a local fill term), writes the .rmesh the game
loads (LoadRMesh in MapSystem.bb) and renders preview images so the result can be
checked without starting the game.

Conventions (measured on the vanilla rooms):
  * 2048 units per map cell, door openings x -96..96, y 0..320 on the cell edge
  * left-handed, y up.  A triangle (a,b,c) faces the side (b-a)x(c-a) points to
  * UV v runs downwards (v=0 is the top of the image)
  * drawn layers: lightmap (2nd UV set, flag 2, name contains "_lm") + diffuse (flag 1)
    final colour = diffuse * lightmap * 2   ->  lightmap 127 is "fully lit"
"""
import math
import os
import numpy as np
from PIL import Image, ImageFilter
import rmesh

GAME = r"I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9"
MAPDIR = os.path.join(GAME, "GFX", "map")
F32 = np.float32


def V(*a):
    return np.array(a, dtype=np.float64)


def norm(v):
    v = np.asarray(v, dtype=np.float64)
    l = np.linalg.norm(v)
    return v / l if l > 1e-12 else v


# --------------------------------------------------------------------- materials
class Mat:
    """A texture + how it is laid on a surface.
    us / vs : world units per texture repeat (horizontal / vertical)
    v0      : the height (walls) that maps to v = 0, i.e. the top edge of the image"""

    def __init__(self, tex, us=256.0, vs=None, v0=0.0, alpha=False, emit=None, cast=True):
        self.tex = tex
        self.us = float(us)
        self.vs = float(vs if vs is not None else us)
        self.v0 = float(v0)
        self.alpha = alpha
        self.emit = emit
        self.cast = cast

    def but(self, **kw):
        m = Mat(self.tex, self.us, self.vs, self.v0, self.alpha, self.emit, self.cast)
        for k, v in kw.items():
            setattr(m, k, v)
        return m


LCZWALL = Mat('whitewall.jpg', 364, 352, 352)        # rivet band lands on y = 352 and y = 704
LCZFLOOR = Mat('concretefloor.jpg', 256)
LCZCEIL = Mat('white.jpg', 256)
EZWALL = Mat('officewall.jpg', 364, 384, 384)        # skirting at the floor, stripes under the ceiling
TILE = Mat('tilefloor.jpg', 512)
EZCEIL = Mat('ceiling.jpg', 512)
HCZWALL = Mat('concretewall.jpg', 384, 384, 384)
HCZFLOOR = Mat('metal3.jpg', 205)
METAL = Mat('metal.jpg', 256)
DIRTY = Mat('dirtymetal.jpg', 512)
DARK = Mat('misc.jpg', 210)
PANELS = Mat('metalpanels.jpg', 168)
PANELS2 = Mat('metalpanels2.jpg', 256)
CHECKER = Mat('scpcb_checkerplate.jpg', 128)
RIVET = Mat('scpcb_rivetband.jpg', 256, 32)
WOOD = Mat('wood.jpg', 512)
PIPES = Mat('Pipes.jpg', 256)
GRATE = Mat('grating.jpg', 128)
GLASS = Mat('glass.png', 256, alpha=True, cast=False)
LIGHTPANEL = Mat('scpcb_lightpanel.jpg', 96, emit=250, cast=False)
VENT = Mat('vent.jpg', 128)
CABINET = Mat('scpcb_cabinet.jpg', 64, 176)


# --------------------------------------------------------------------- surfaces
class Surf:
    """A planar convex polygon.  pts are listed counter-clockwise as seen from the
    visible side (bottom-left, bottom-right, top-right, top-left for a quad)."""

    def __init__(self, pts, uvs, mat, lm=True, coll=True, cast=None, emit=None, lux=None, tag=''):
        self.pts = np.asarray(pts, dtype=np.float64)
        self.uvs = np.asarray(uvs, dtype=np.float64)
        self.mat = mat
        self.lm = lm
        self.coll = coll
        self.cast = mat.cast if cast is None else cast
        self.emit = mat.emit if emit is None else emit
        self.lux = lux
        self.tag = tag
        p = self.pts
        n = np.zeros(3)
        for i in range(1, len(p) - 1):
            n += np.cross(p[i + 1] - p[0], p[i] - p[0])
        self.n = norm(n)
        a = norm(p[1] - p[0])
        b = norm(np.cross(self.n, a))
        s = (p - p[0]) @ a
        t = (p - p[0]) @ b
        self.o = p[0] + a * s.min() + b * t.min()
        self.a, self.b = a, b
        self.es = max(s.max() - s.min(), 1e-3)
        self.et = max(t.max() - t.min(), 1e-3)
        self.st = np.stack([s - s.min(), t - t.min()], axis=1)
        self.rect = None  # (x, y, w, h) in the atlas, inner area without padding
        self.lmuv = np.zeros((len(p), 2))

    def tris(self):
        return [(0, i + 1, i) for i in range(1, len(self.pts) - 1)]

    def area(self):
        return self.es * self.et


class Room:
    def __init__(self, name, luxel=12.0, ambient=17.0, fill=0.16):
        self.name = name
        self.luxel = float(luxel)
        self.ambient = float(ambient)
        self.fill = float(fill)
        self.surfs = []
        self.hidden = []      # invisible collision quads (list of 4 points)
        self.lights = []
        self.ents = []
        self.markers = []     # preview-only boxes (doors, props)
        self.spawns = []      # things the game code creates (items, doors, fans ...): see v01kit.py
        self.atlas = None
        self.atlas_size = 0

    # ---------------------------------------------------------------- low level
    def add(self, pts, uvs, mat, **kw):
        s = Surf(pts, uvs, mat, **kw)
        self.surfs.append(s)
        return s

    def quad(self, bl, br, tr, tl, mat, uvrect=None, uo=0.0, **kw):
        """A quad seen from the front.  Without uvrect the material's world scale is used:
        u runs along bl->br, v along the height (walls) or along tl->bl (flat surfaces)."""
        bl, br, tr, tl = [np.asarray(q, dtype=np.float64) for q in (bl, br, tr, tl)]
        if uvrect is not None:
            u0, v0, u1, v1 = uvrect
            uvs = [(u0, v1), (u1, v1), (u1, v0), (u0, v0)]
        else:
            w = np.linalg.norm(br - bl)
            h = np.linalg.norm(tl - bl)
            n = norm(np.cross(tl - bl, br - bl))
            if abs(n[1]) < 0.7:      # wall-like: v follows world height
                vb = (mat.v0 - bl[1]) / mat.vs
                vt = (mat.v0 - tl[1]) / mat.vs
                vbr = (mat.v0 - br[1]) / mat.vs
                vtr = (mat.v0 - tr[1]) / mat.vs
                u0 = uo / mat.us
                u1 = (uo + w) / mat.us
                uvs = [(u0, vb), (u1, vbr), (u1, vtr), (u0, vt)]
            else:                    # floor / ceiling / slope: planar from world x,z
                uvs = [(q[0] / mat.us, -q[2] / mat.vs) for q in (bl, br, tr, tl)]
        return self.add([bl, br, tr, tl], uvs, mat, **kw)

    # ---------------------------------------------------------------- walls
    def wall(self, a, b, y0, y1, mat, holes=(), uo=0.0, **kw):
        """Vertical wall seen from the front with a on the left and b on the right
        (xz points).  holes = [(s0, s1, hy0, hy1)] with s measured from a."""
        a = np.asarray(a, dtype=np.float64)
        b = np.asarray(b, dtype=np.float64)
        L = np.linalg.norm(b - a)
        d = (b - a) / L

        def P(s, y):
            q = a + d * s
            return V(q[0], y, q[1])

        def piece(s0, s1, ya, yb):
            if s1 - s0 < 0.01 or yb - ya < 0.01:
                return
            self.quad(P(s0, ya), P(s1, ya), P(s1, yb), P(s0, yb), mat, uo=uo + s0, **kw)

        cur = 0.0
        for (s0, s1, hy0, hy1) in sorted(holes):
            piece(cur, s0, y0, y1)
            piece(s0, s1, y0, hy0)
            piece(s0, s1, hy1, y1)
            cur = s1
        piece(cur, L, y0, y1)
        return L

    def walls(self, pts, y0, y1, mat, holes=None, closed=True, uo=0.0, **kw):
        """Room outline seen from the inside: list the corners clockwise (x right, z up).
        holes = {segment index: [(s0, s1, hy0, hy1)]}"""
        holes = holes or {}
        n = len(pts)
        last = n if closed else n - 1
        for i in range(last):
            L = self.wall(pts[i], pts[(i + 1) % n], y0, y1, mat, holes=holes.get(i, ()), uo=uo, **kw)
            uo += L

    def floor(self, pts, y, mat, **kw):
        """Horizontal polygon facing up.  pts = xz corners (any winding, convex)."""
        p = self._order(pts, ccw_from_above=True)
        P3 = [V(q[0], y, q[1]) for q in p]
        uvs = [(q[0] / mat.us, -q[1] / mat.vs) for q in p]
        return self.add(P3, uvs, mat, **kw)

    def ceil(self, pts, y, mat, **kw):
        p = self._order(pts, ccw_from_above=False)
        P3 = [V(q[0], y, q[1]) for q in p]
        uvs = [(q[0] / mat.us, -q[1] / mat.vs) for q in p]
        return self.add(P3, uvs, mat, **kw)

    @staticmethod
    def _order(pts, ccw_from_above):
        # "counter-clockwise seen from the front": for an up-facing polygon the viewer is above
        # (x right, z up on screen) -> counter-clockwise there.  Signed area tells which way pts go.
        p = [np.asarray(q, dtype=np.float64) for q in pts]
        area = 0.0
        for i in range(len(p)):
            j = (i + 1) % len(p)
            area += p[i][0] * p[j][1] - p[j][0] * p[i][1]
        is_ccw = area > 0
        if is_ccw != ccw_from_above:
            p = p[::-1]
        return p

    def rect_floor(self, x0, z0, x1, z1, y, mat, **kw):
        return self.floor([(x0, z0), (x1, z0), (x1, z1), (x0, z1)], y, mat, **kw)

    def rect_ceil(self, x0, z0, x1, z1, y, mat, **kw):
        return self.ceil([(x0, z0), (x1, z0), (x1, z1), (x0, z1)], y, mat, **kw)

    # ---------------------------------------------------------------- solids
    def box(self, x0, y0, z0, x1, y1, z1, mat, skip='', top=None, bottom=None, **kw):
        """Axis aligned solid seen from outside.  skip: any of 'N S E W T B' (+z -z +x -x top bottom)."""
        x0, x1 = min(x0, x1), max(x0, x1)
        y0, y1 = min(y0, y1), max(y0, y1)
        z0, z1 = min(z0, z1), max(z0, z1)
        if 'S' not in skip:
            self.wall((x0, z0), (x1, z0), y0, y1, mat, **kw)   # faces -z
        if 'E' not in skip:
            self.wall((x1, z0), (x1, z1), y0, y1, mat, **kw)   # faces +x
        if 'N' not in skip:
            self.wall((x1, z1), (x0, z1), y0, y1, mat, **kw)   # faces +z
        if 'W' not in skip:
            self.wall((x0, z1), (x0, z0), y0, y1, mat, **kw)   # faces -x
        if 'T' not in skip:
            self.rect_floor(x0, z0, x1, z1, y1, top or mat, **kw)
        if 'B' not in skip:
            self.rect_ceil(x0, z0, x1, z1, y0, bottom or mat, **kw)

    def prism(self, pts, y0, y1, mat, caps='TB', top=None, **kw):
        """Vertical solid from a convex xz polygon, seen from outside."""
        p = self._order(pts, ccw_from_above=True)
        # outward walls: walk so that the outside viewer sees a on the left -> counter-clockwise from above
        uo = 0.0
        for i in range(len(p)):
            uo += self.wall(p[i], p[(i + 1) % len(p)], y0, y1, mat, uo=uo, **kw)
        if 'T' in caps:
            self.floor(p, y1, top or mat, **kw)
        if 'B' in caps:
            self.ceil(p, y0, top or mat, **kw)

    def obox(self, c, ax, ay, az, mat, skip='', **kw):
        """Oriented box: centre c and three half-extent vectors (slanted beams, pipes ...)."""
        c, ax, ay, az = [np.asarray(q, dtype=np.float64) for q in (c, ax, ay, az)]
        if np.dot(np.cross(ax, ay), az) < 0:
            az = -az

        def face(o, r, u):       # outward normal = u x r
            self.quad(o - r - u, o + r - u, o + r + u, o - r + u, mat,
                      uvrect=(0, 0, 2 * np.linalg.norm(r) / mat.us, 2 * np.linalg.norm(u) / mat.vs), **kw)
        for (o, r, u, key) in ((az, -ax, ay, 'N'), (-az, ax, ay, 'S'), (ax, az, ay, 'E'),
                               (-ax, -az, ay, 'W'), (ay, ax, az, 'T'), (-ay, ax, -az, 'B')):
            if key in skip:
                continue
            # make sure the face looks away from the centre
            n = np.cross(u, r)
            if np.dot(n, o) < 0:
                r = -r
            face(c + o, r, u)

    def tube(self, p0, p1, radius, mat, sides=10, caps=False, **kw):
        """A pipe between two points."""
        p0 = np.asarray(p0, dtype=np.float64)
        p1 = np.asarray(p1, dtype=np.float64)
        ax = norm(p1 - p0)
        ref = V(0, 1, 0) if abs(ax[1]) < 0.9 else V(1, 0, 0)
        e1 = norm(np.cross(ax, ref))
        e2 = np.cross(ax, e1)
        L = np.linalg.norm(p1 - p0)
        ring = [e1 * math.cos(2 * math.pi * i / sides) * radius + e2 * math.sin(2 * math.pi * i / sides) * radius
                for i in range(sides + 1)]
        circ = 2 * math.pi * radius
        for i in range(sides):
            a, b = ring[i], ring[i + 1]
            bl, br, tr, tl = p0 + a, p0 + b, p1 + b, p1 + a
            if np.dot(np.cross(tl - bl, br - bl), a + b) < 0:
                bl, br, tr, tl = br, bl, tl, tr
            u0, u1 = i / sides * circ / mat.us, (i + 1) / sides * circ / mat.us
            self.quad(bl, br, tr, tl, mat, uvrect=(u0, 0, u1, L / mat.vs), **kw)
        if caps:
            for (pc, sgn) in ((p0, -1), (p1, 1)):
                pts = [pc + r for r in ring[:-1]]
                if np.dot(np.cross(pts[2] - pts[0], pts[1] - pts[0]), ax * sgn) < 0:
                    pts = pts[::-1]
                uvs = [(0.5 + 0.4 * math.cos(2 * math.pi * i / sides), 0.5 + 0.4 * math.sin(2 * math.pi * i / sides))
                       for i in range(sides)]
                self.add(pts, uvs, mat, **kw)

    def decal(self, a, b, y0, y1, mat, uvrect, off=1.5, **kw):
        """A flat picture (sign, vent, panel) on a wall: a..b seen from the front, lifted off the wall."""
        a = np.asarray(a, dtype=np.float64)
        b = np.asarray(b, dtype=np.float64)
        d = norm(b - a)
        nrm = V(d[1], -d[0])            # (rz, -rx) = up x right
        a2, b2 = a + nrm * off, b + nrm * off
        kw.setdefault('coll', True)
        kw.setdefault('cast', False)
        return self.quad(V(a2[0], y0, a2[1]), V(b2[0], y0, b2[1]), V(b2[0], y1, b2[1]), V(a2[0], y1, a2[1]),
                         mat, uvrect=uvrect, **kw)

    def collide(self, bl, br, tr, tl):
        self.hidden.append([np.asarray(q, dtype=np.float64) for q in (bl, br, tr, tl)])

    def collide_wall(self, a, b, y0, y1):
        self.collide(V(a[0], y0, a[1]), V(b[0], y0, b[1]), V(b[0], y1, b[1]), V(a[0], y1, a[1]))

    # ---------------------------------------------------------------- entities
    def light(self, x, y, z, rng=900.0, color=(255, 255, 255), power=1.0, radius=10.0, ent=True, fill=None):
        self.lights.append(dict(pos=V(x, y, z), rng=float(rng), color=np.array(color, dtype=np.float64) / 255.0,
                                power=float(power), radius=float(radius), ent=ent,
                                fill=self.fill if fill is None else fill))

    def waypoint(self, x, y, z):
        self.ents.append(dict({'class': 'waypoint'}, pos=(x, y, z)))

    def model(self, file, x, y, z, rot=(0, 0, 0), scale=(1, 1, 1), size=None):
        self.ents.append(dict({'class': 'model'}, file=file, pos=(x, y, z), rot=rot, scale=scale))
        if size:
            sx, sy, sz = size
            self.markers.append(((x - sx / 2, y, z - sz / 2, x + sx / 2, y + sy, z + sz / 2), (150, 120, 60)))

    def sound(self, x, y, z, sound, rng=5.0):
        self.ents.append(dict({'class': 'soundemitter'}, pos=(x, y, z), sound=sound, range=rng))

    def marker(self, x0, y0, z0, x1, y1, z1, color=(60, 60, 60)):
        self.markers.append(((x0, y0, z0, x1, y1, z1), color))

    def door_marker(self, x, y, z, angle, color=(45, 45, 48), w=204, h=312):
        if angle % 180 == 0:
            self.marker(x - w / 2, y, z - 8, x + w / 2, y + h, z + 8, color)
        else:
            self.marker(x - 8, y, z - w / 2, x + 8, y + h, z + w / 2, color)

    # ---------------------------------------------------------------- lightmap
    def _occluders(self):
        O, N, G1, G2, TRI, LO, HI = [], [], [], [], [], [], []
        for s in self.surfs:
            if not s.cast:
                continue
            p = s.pts
            if len(p) == 4 and abs(np.linalg.norm((p[1] - p[0]) + (p[3] - p[0]) - (p[2] - p[0]))) < 1e-3:
                parts = [(p[0], p[1] - p[0], p[3] - p[0], False)]
            else:
                parts = [(p[0], p[i] - p[0], p[i + 1] - p[0], True) for i in range(1, len(p) - 1)]
            for (o, e1, e2, tri) in parts:
                n = np.cross(e1, e2)
                nn = float(n @ n)
                if nn < 1e-9:
                    continue
                O.append(o)
                N.append(n / math.sqrt(nn))
                G1.append(np.cross(e2, n) / nn)
                G2.append(np.cross(n, e1) / nn)
                TRI.append(tri)
                c = np.array([o, o + e1, o + e2, o + e1 + e2] if not tri else [o, o + e1, o + e2])
                LO.append(c.min(axis=0))
                HI.append(c.max(axis=0))
        return (np.array(O), np.array(N), np.array(G1), np.array(G2), np.array(TRI),
                np.array(LO), np.array(HI))

    @staticmethod
    def _hits(Orig, D, occ, idx, backface=False):
        """For rays Orig + t*D, t in (0,1): which rays are blocked by the occluders idx.
        Returns (blocked, t of the nearest hit, nearest hit is a back face)."""
        O, N, G1, G2, TRI = occ[0][idx], occ[1][idx], occ[2][idx], occ[3][idx], occ[4][idx]
        S = len(Orig)
        blocked = np.zeros(S, dtype=bool)
        tnear = np.full(S, 2.0, dtype=F32)
        back = np.zeros(S, dtype=bool)
        if len(idx) == 0 or S == 0:
            return blocked, tnear, back
        O32, N32, G132, G232 = O.astype(F32), N.astype(F32), G1.astype(F32), G2.astype(F32)
        on = np.einsum('ij,ij->i', O32, N32)
        og1 = np.einsum('ij,ij->i', O32, G132)
        og2 = np.einsum('ij,ij->i', O32, G232)
        step = max(1, int(3_000_000 // max(1, len(idx))))
        for i0 in range(0, S, step):
            o = Orig[i0:i0 + step].astype(F32)
            d = D[i0:i0 + step].astype(F32)
            den = d @ N32.T
            with np.errstate(divide='ignore', invalid='ignore'):
                t = (on[None, :] - o @ N32.T) / den
            t = np.nan_to_num(t, nan=-1.0, posinf=-1.0, neginf=-1.0)
            ok = (t > 1e-4) & (t < 0.9995) & (np.abs(den) > 1e-9)
            a = (o @ G132.T) - og1[None, :] + t * (d @ G132.T)
            b = (o @ G232.T) - og2[None, :] + t * (d @ G232.T)
            inside = (a >= 0) & (b >= 0) & np.where(TRI[None, :], (a + b) <= 1.0, (a <= 1.0) & (b <= 1.0))
            hit = ok & inside
            blocked[i0:i0 + step] = hit.any(axis=1)
            if backface:
                tt = np.where(hit, t, 2.0)
                j = tt.argmin(axis=1)
                r = np.arange(len(o))
                tnear[i0:i0 + step] = tt[r, j]
                back[i0:i0 + step] = hit[r, j] & (den[r, j] > 0)
        return blocked, tnear, back

    def bake(self, ao_rays=14, ao_dist=220.0, shadow_samples=6, blur=0.55, verbose=True, max_size=4096):
        lm_surfs = [s for s in self.surfs if s.lm and not s.mat.alpha]
        # --- allocate luxel grids
        for s in lm_surfs:
            lux = s.lux or self.luxel
            s.w = int(max(2, math.ceil(s.es / lux)))
            s.h = int(max(2, math.ceil(s.et / lux)))
        size = 256
        while True:
            if self._pack(lm_surfs, size):
                break
            size *= 2
            if size > max_size:
                raise RuntimeError('lightmap does not fit in %d' % max_size)
        self.atlas_size = size
        atlas = np.zeros((size, size, 3), dtype=np.float64)
        filled = np.zeros((size, size), dtype=bool)

        occ = self._occluders()
        LO, HI = occ[5], occ[6]
        rng = np.random.default_rng(7)
        # fixed light-sample offsets (unit sphere) and cosine weighted hemisphere directions
        loff = rng.normal(size=(shadow_samples, 3))
        loff /= np.linalg.norm(loff, axis=1)[:, None]
        hemi = []
        for i in range(ao_rays):
            u = (i + 0.5) / ao_rays
            r = math.sqrt(u)
            ph = i * 2.399963
            hemi.append((r * math.cos(ph), r * math.sin(ph), math.sqrt(max(0.0, 1 - u))))
        hemi = np.array(hemi)

        total = sum(s.w * s.h for s in lm_surfs)
        if verbose:
            print('  %s: %d surfaces, %d luxels, atlas %d, %d occluders, %d lights' %
                  (self.name, len(lm_surfs), total, size, len(occ[0]), len(self.lights)))

        for s in lm_surfs:
            w, h = s.w, s.h
            ii, jj = np.meshgrid(np.arange(w), np.arange(h))
            sc = (ii + 0.5) / w * s.es
            tc = (jj + 0.5) / h * s.et
            P = s.o[None, None, :] + sc[..., None] * s.a + tc[..., None] * s.b
            P = P.reshape(-1, 3)
            Pb = P + s.n * 1.2
            S = len(P)
            E = np.zeros((S, 3))
            valid = self._inside(s, sc.reshape(-1), tc.reshape(-1))

            if s.emit is not None:
                E[:] = s.emit
                valid[:] = True
            else:
                slo, shi = Pb.min(axis=0), Pb.max(axis=0)
                # ---- ambient occlusion + buried sample detection
                near = np.where(np.all(HI >= slo - ao_dist, axis=1) & np.all(LO <= shi + ao_dist, axis=1))[0]
                occl = np.zeros(S)
                backs = np.zeros(S)
                for hd in hemi:
                    d = (s.a * hd[0] + s.b * hd[1] + s.n * hd[2]) * ao_dist
                    D = np.broadcast_to(d, (S, 3))
                    blk, tn, bk = self._hits(Pb, D, occ, near, backface=True)
                    occl += np.where(blk, 1.0 - np.minimum(tn, 1.0) * 0.85, 0.0)
                    backs += bk & (tn < 0.5)
                ao = 1.0 - 0.75 * occl / ao_rays
                valid &= backs < ao_rays * 0.45
                fillE = np.zeros((S, 3))
                for L in self.lights:
                    dv = L['pos'][None, :] - Pb
                    dist = np.linalg.norm(dv, axis=1)
                    if dist.min() > L['rng'] * 1.6:
                        continue
                    # local fill (no shadows): stands in for bounced light around each lamp
                    ff = np.clip(1.0 - (dist / (L['rng'] * 1.6)) ** 2, 0, 1) ** 2
                    half = 0.6 + 0.4 * np.clip((dv @ s.n) / np.maximum(dist, 1e-3), -1, 1)
                    fillE += (L['fill'] * L['power'] * ff * half)[:, None] * L['color'][None, :]
                    cosv = (dv @ s.n) / np.maximum(dist, 1e-3)
                    fall = np.clip(1.0 - (dist / L['rng']) ** 2, 0, 1) ** 2
                    act = np.where((cosv > 0.0) & (fall > 0.002))[0]
                    if len(act) == 0:
                        continue
                    lo = np.minimum(Pb[act].min(axis=0), L['pos'] - L['radius'])
                    hi = np.maximum(Pb[act].max(axis=0), L['pos'] + L['radius'])
                    cand = np.where(np.all(HI >= lo - 1, axis=1) & np.all(LO <= hi + 1, axis=1))[0]
                    vis = np.zeros(len(act))
                    for k in range(shadow_samples):
                        tgt = L['pos'] + loff[k] * L['radius']
                        blk, _, _ = self._hits(Pb[act], tgt[None, :] - Pb[act], occ, cand)
                        vis += ~blk
                    vis /= shadow_samples
                    e = L['power'] * fall[act] * (0.25 + 0.75 * cosv[act]) * vis
                    E[act] += e[:, None] * L['color'][None, :]
                E += (self.ambient + fillE) * ao[:, None]

            img = E.reshape(h, w, 3)
            vm = valid.reshape(h, w)
            img = self._dilate(img, vm)
            if blur > 0 and s.emit is None and min(w, h) > 2:
                pad = np.pad(img, ((2, 2), (2, 2), (0, 0)), mode='edge')
                pim = Image.fromarray(np.clip(pad, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(blur))
                img = np.asarray(pim).astype(np.float64)[2:-2, 2:-2]
            x, y = s.rect[0], s.rect[1]
            atlas[y - 1:y + h + 1, x - 1:x + w + 1] = np.pad(img, ((1, 1), (1, 1), (0, 0)), mode='edge')
            filled[y - 1:y + h + 1, x - 1:x + w + 1] = True
            # lightmap UVs
            s.lmuv = np.stack([(x + s.st[:, 0] / s.es * w) / size, (y + s.st[:, 1] / s.et * h) / size], axis=1)
        self.atlas = np.clip(atlas, 0, 255).astype(np.uint8)
        return self.atlas

    @staticmethod
    def _inside(s, sc, tc):
        """Luxel centre inside the (convex) polygon?"""
        n = len(s.st)
        if n == 4:
            # rectangles are fully covered by their own bounds
            e1 = s.st[1] - s.st[0]
            e2 = s.st[3] - s.st[0]
            if abs(e1 @ e2) < 1e-3:
                return np.ones(len(sc), dtype=bool)
        ins = np.ones(len(sc), dtype=bool)
        sgn = 0.0
        for i in range(n):
            a, b = s.st[i], s.st[(i + 1) % n]
            cr = (b[0] - a[0]) * (tc - a[1]) - (b[1] - a[1]) * (sc - a[0])
            if sgn == 0.0:
                c = s.st.mean(axis=0)
                sgn = 1.0 if (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]) > 0 else -1.0
            ins &= (cr * sgn) >= -1e-6
        return ins

    @staticmethod
    def _dilate(img, valid):
        if valid.all():
            return img
        if not valid.any():
            return img
        img = img.copy()
        valid = valid.copy()
        for _ in range(64):
            if valid.all():
                break
            acc = np.zeros_like(img)
            cnt = np.zeros(valid.shape)
            for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)):
                sh = np.roll(np.roll(img * valid[..., None], dy, axis=0), dx, axis=1)
                vs = np.roll(np.roll(valid, dy, axis=0), dx, axis=1).astype(float)
                if dy == 1: sh[0] = 0; vs[0] = 0
                if dy == -1: sh[-1] = 0; vs[-1] = 0
                if dx == 1: sh[:, 0] = 0; vs[:, 0] = 0
                if dx == -1: sh[:, -1] = 0; vs[:, -1] = 0
                acc += sh
                cnt += vs
            new = (~valid) & (cnt > 0)
            img[new] = acc[new] / cnt[new][:, None]
            valid |= new
        return img

    def _pack(self, surfs, size):
        order = sorted(surfs, key=lambda s: -(s.h + 2))
        x = y = 0
        rowh = 0
        for s in order:
            w, h = s.w + 2, s.h + 2
            if w > size:
                return False
            if x + w > size:
                x = 0
                y += rowh
                rowh = 0
            if y + h > size:
                return False
            s.rect = (x + 1, y + 1, s.w, s.h)
            x += w
            rowh = max(rowh, h)
        return True

    # ---------------------------------------------------------------- export
    def export(self, outdir=MAPDIR):
        lmname = self.name + '_lm1.png'
        Image.fromarray(self.atlas).save(os.path.join(outdir, lmname))
        groups = {}
        for s in self.surfs:
            key = (s.mat.tex, s.mat.alpha, s.lm and not s.mat.alpha)
            groups.setdefault(key, []).append(s)
        meshes = []
        for (tex, alpha, lm), ss in groups.items():
            if not os.path.exists(os.path.join(MAPDIR, tex)):
                raise FileNotFoundError('texture missing in GFX\\map: ' + tex)
            verts, tris = [], []
            for s in ss:
                base = len(verts)
                for p, uv, lu in zip(s.pts, s.uvs, s.lmuv):
                    verts.append((p[0], p[1], p[2], uv[0], uv[1], lu[0], lu[1], 255, 255, 255))
                for t in s.tris():
                    tris.append((base + t[0], base + t[1], base + t[2]))
            meshes.append(dict(tex=tex, alpha=alpha, lm=lmname if lm else None, verts=verts, tris=tris))
        hidden = []
        hv, ht = [], []
        for q in self.hidden:
            b = len(hv)
            hv += [tuple(p) for p in q]
            ht += [(b, b + 1, b + 2), (b, b + 2, b + 3)]
        for s in self.surfs:     # glass has no collision of its own
            if s.mat.alpha and s.coll:
                b = len(hv)
                hv += [tuple(p) for p in s.pts]
                ht += [(b, i + 1 + b, i + b) for i in range(1, len(s.pts) - 1)]
        if hv:
            hidden.append(dict(verts=hv, tris=ht))
        ents = list(self.ents)
        for L in self.lights:
            if not L['ent']:
                continue
            c = L['color']
            m = max(1e-3, c.max())
            ents.append(dict({'class': 'light'}, pos=tuple(L['pos']), range=L['rng'],
                             color='%d %d %d' % tuple(np.clip(c / m * 255, 0, 255).astype(int)),
                             intensity=min(1.25, max(0.5, L['power'] / 140.0))))
        path = os.path.join(outdir, self.name + '.rmesh')
        rmesh.write_rmesh(path, meshes, hidden, ents)
        nv = sum(len(m['verts']) for m in meshes)
        nt = sum(len(m['tris']) for m in meshes)
        allp = np.concatenate([s.pts for s in self.surfs])
        print('  wrote %s  (%d meshes, %d verts, %d tris, %d ents)  bounds x %.0f..%.0f y %.0f..%.0f z %.0f..%.0f' %
              (path, len(meshes), nv, nt, len(ents), allp[:, 0].min(), allp[:, 0].max(),
               allp[:, 1].min(), allp[:, 1].max(), allp[:, 2].min(), allp[:, 2].max()))
        return path

    # ---------------------------------------------------------------- preview
    _texcache = {}

    def _tex(self, name):
        if name not in Room._texcache:
            im = Image.open(os.path.join(MAPDIR, name)).convert('RGBA')
            im = im.resize((256, 256), Image.BILINEAR)
            Room._texcache[name] = np.asarray(im).astype(np.float64)
        return Room._texcache[name]

    def render(self, eye, look, path, fov=78.0, size=(960, 540), bright=1.0):
        W, H = size
        eye = np.asarray(eye, dtype=np.float64)
        f = norm(np.asarray(look, dtype=np.float64) - eye)
        r = norm(np.cross(V(0, 1, 0), f))
        u = np.cross(f, r)
        F = (W / 2) / math.tan(math.radians(fov) / 2)
        col = np.zeros((H, W, 3))
        zb = np.full((H, W), np.inf)
        atlas = self.atlas.astype(np.float64) if self.atlas is not None else None
        near = 4.0

        def draw(P, UV, LUV, tex, lit, alpha=1.0, flat=None):
            # P: Nx3 world polygon (convex) ; back-face cull like the game
            n = np.cross(P[2] - P[0], P[1] - P[0])      # pts run counter-clockwise seen from the front
            if flat is None and np.dot(n, eye - P[0]) <= 0:
                return
            C = np.stack([(P - eye) @ r, (P - eye) @ u, (P - eye) @ f], axis=1)
            A = np.concatenate([C, UV, LUV], axis=1)
            # clip to the near plane
            out = []
            for i in range(len(A)):
                a, b = A[i], A[(i + 1) % len(A)]
                ia, ib = a[2] >= near, b[2] >= near
                if ia:
                    out.append(a)
                if ia != ib:
                    t = (near - a[2]) / (b[2] - a[2])
                    out.append(a + (b - a) * t)
            if len(out) < 3:
                return
            A = np.array(out)
            sx = W / 2 + A[:, 0] / A[:, 2] * F
            sy = H / 2 - A[:, 1] / A[:, 2] * F
            iz = 1.0 / A[:, 2]
            for i in range(1, len(A) - 1):
                idx = (0, i, i + 1)
                x0, x1 = max(0, int(math.floor(min(sx[list(idx)])))), min(W - 1, int(math.ceil(max(sx[list(idx)]))))
                y0, y1 = max(0, int(math.floor(min(sy[list(idx)])))), min(H - 1, int(math.ceil(max(sy[list(idx)]))))
                if x1 < x0 or y1 < y0:
                    continue
                xs, ys = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
                ax, ay, bx, by, cx, cy = sx[idx[0]], sy[idx[0]], sx[idx[1]], sy[idx[1]], sx[idx[2]], sy[idx[2]]
                den = (by - cy) * (ax - cx) + (cx - bx) * (ay - cy)
                if abs(den) < 1e-9:
                    continue
                w0 = ((by - cy) * (xs - cx) + (cx - bx) * (ys - cy)) / den
                w1 = ((cy - ay) * (xs - cx) + (ax - cx) * (ys - cy)) / den
                w2 = 1 - w0 - w1
                m = (w0 >= -1e-6) & (w1 >= -1e-6) & (w2 >= -1e-6)
                if not m.any():
                    continue
                z = w0 * iz[idx[0]] + w1 * iz[idx[1]] + w2 * iz[idx[2]]
                depth = 1.0 / z
                sub = zb[y0:y1 + 1, x0:x1 + 1]
                m &= depth < sub
                if not m.any():
                    continue
                if flat is not None:
                    c = np.broadcast_to(np.array(flat, dtype=np.float64), m.shape + (3,))
                    a_ = np.ones(m.shape) * alpha
                else:
                    def interp(k):
                        return (w0 * A[idx[0], k] * iz[idx[0]] + w1 * A[idx[1], k] * iz[idx[1]] + w2 * A[idx[2], k] * iz[idx[2]]) / z
                    tu, tv, lu, lv = interp(3), interp(4), interp(5), interp(6)
                    T = self._tex(tex)
                    tx = (np.floor(tu * 256).astype(int)) % 256
                    ty = (np.floor(tv * 256).astype(int)) % 256
                    c = T[ty, tx, :3]
                    a_ = T[ty, tx, 3] / 255.0 * alpha
                    if lit and atlas is not None:
                        S = self.atlas_size
                        lx = np.clip(lu * S - 0.5, 0, S - 1.001)
                        ly = np.clip(lv * S - 0.5, 0, S - 1.001)
                        x_ = np.floor(lx).astype(int); y_ = np.floor(ly).astype(int)
                        fx = (lx - x_)[..., None]; fy = (ly - y_)[..., None]
                        lm = (atlas[y_, x_] * (1 - fx) * (1 - fy) + atlas[y_, x_ + 1] * fx * (1 - fy) +
                              atlas[y_ + 1, x_] * (1 - fx) * fy + atlas[y_ + 1, x_ + 1] * fx * fy)
                        c = c * np.minimum(1.0, lm * 2.0 / 255.0 * bright)
                    else:
                        c = c * 0.55
                cs = col[y0:y1 + 1, x0:x1 + 1]
                if alpha >= 0.999 and flat is not None or (flat is None and alpha >= 0.999 and not self._is_alpha(tex)):
                    cs[m] = c[m]
                    sub[m] = depth[m]
                else:
                    aa = a_[m][:, None] * 0.45
                    cs[m] = cs[m] * (1 - aa) + c[m] * aa

        opaque = [s for s in self.surfs if not s.mat.alpha]
        glass = [s for s in self.surfs if s.mat.alpha]
        for s in opaque:
            draw(s.pts, s.uvs, s.lmuv, s.mat.tex, s.lm)
        for (bx, colr) in self.markers:
            x0, y0, z0, x1, y1, z1 = bx
            c = [V(x0, y0, z0), V(x1, y0, z0), V(x1, y0, z1), V(x0, y0, z1), V(x0, y1, z0), V(x1, y1, z0), V(x1, y1, z1), V(x0, y1, z1)]
            for q in ((0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7), (4, 5, 6, 7), (0, 3, 2, 1)):
                P = np.array([c[k] for k in q])
                z = np.zeros((4, 2))
                shade = 0.6 + 0.4 * abs(norm(np.cross(P[1] - P[0], P[2] - P[0]))[1])
                draw(P, z, z, None, False, flat=np.array(colr) * shade)
        for s in glass:
            draw(s.pts, s.uvs, s.lmuv, s.mat.tex, False, alpha=0.999)
            draw(s.pts[::-1], s.uvs[::-1], s.lmuv[::-1], s.mat.tex, False, alpha=0.999)
        # light flares
        for L in self.lights:
            if not L['ent']:
                continue
            c = L['pos'] - eye
            zc = c @ f
            if zc > near:
                px, py = int(W / 2 + (c @ r) / zc * F), int(H / 2 - (c @ u) / zc * F)
                if 0 <= px < W and 0 <= py < H and zc < zb[py, px] + 30:
                    rad = max(3, int(2600 / zc))
                    yy, xx = np.ogrid[-rad:rad + 1, -rad:rad + 1]
                    g = np.exp(-(xx * xx + yy * yy) / (0.18 * rad * rad))
                    ya, yb_, xa, xb = max(0, py - rad), min(H, py + rad + 1), max(0, px - rad), min(W, px + rad + 1)
                    col[ya:yb_, xa:xb] += (g[ya - py + rad:yb_ - py + rad, xa - px + rad:xb - px + rad, None] *
                                           L['color'][None, None, :] * 230.0)
        Image.fromarray(np.clip(col, 0, 255).astype(np.uint8)).save(path)

    @staticmethod
    def _is_alpha(tex):
        if tex is None:
            return False
        if tex.lower().endswith('glass.png'):
            return True
        t = Room._texcache.get(tex)          # preview only: any texture that really has transparent pixels
        return t is not None and t[..., 3].min() < 250

    def topview(self, path, y_cut=None, size=900, pad=1100.0):
        """Plan view of everything below y_cut (walls as lines) - quick sanity check of the layout."""
        from PIL import ImageDraw
        im = Image.new('RGB', (size, size), (18, 18, 20))
        d = ImageDraw.Draw(im)

        def T(x, z):
            return (size / 2 + x / pad * size / 2, size / 2 - z / pad * size / 2)
        d.rectangle([T(-1024, 1024), T(1024, -1024)], outline=(70, 70, 120))
        for s in self.surfs:
            ymin, ymax = s.pts[:, 1].min(), s.pts[:, 1].max()
            if y_cut is not None and (ymin > y_cut[1] or ymax < y_cut[0]):
                continue
            if abs(s.n[1]) > 0.7:
                if s.n[1] > 0:
                    d.polygon([T(p[0], p[2]) for p in s.pts], fill=(40, 44, 48))
        for s in self.surfs:
            ymin, ymax = s.pts[:, 1].min(), s.pts[:, 1].max()
            if y_cut is not None and (ymin > y_cut[1] or ymax < y_cut[0]):
                continue
            if abs(s.n[1]) <= 0.7:
                a, b = s.pts[0], s.pts[1]
                d.line([T(a[0], a[2]), T(b[0], b[2])], fill=(220, 220, 220), width=1)
                m = (a + b) / 2
                d.line([T(m[0], m[2]), T(m[0] + s.n[0] * 30, m[2] + s.n[2] * 30)], fill=(90, 160, 90), width=1)
        for (bx, colr) in self.markers:
            d.rectangle([T(bx[0], bx[5]), T(bx[3], bx[2])], outline=(255, 160, 40))
        for L in self.lights:
            x, y = T(L['pos'][0], L['pos'][2])
            d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=tuple(int(c) for c in np.clip(L['color'] * 255, 0, 255)))
        for e in self.ents:
            if e['class'] == 'waypoint':
                x, y = T(e['pos'][0], e['pos'][2])
                d.ellipse([x - 3, y - 3, x + 3, y + 3], outline=(80, 200, 255))
        im.save(path)


# --------------------------------------------------------------------- shared building blocks
def door_neck(R, side, wall_mat, floor_mat, ceil_y=None, zwall=992.0, width=192.0, height=320.0):
    """The 32-deep door recess on a cell edge, like every vanilla room has.
    side: 'N' (+z) 'S' (-z) 'E' (+x) 'W' (-x).  The end wall itself is made by the caller with a
    192 x 320 hole; this adds the jambs, the lintel underside and the floor strip out to the edge."""
    hw = width / 2

    def X(p):   # rotate a point given for the north side onto the wanted side
        x, z = p
        return {'N': (x, z), 'S': (-x, -z), 'E': (z, -x), 'W': (-z, x)}[side]
    a, b = zwall, 1024.0
    # floor strip
    R.floor([X((-hw, a)), X((hw, a)), X((hw, b)), X((-hw, b))], 0, floor_mat)
    # lintel underside
    R.ceil([X((-hw, a)), X((hw, a)), X((hw, b)), X((-hw, b))], height, wall_mat)
    # jambs (seen from inside the recess)
    R.wall(X((-hw, a)), X((-hw, b)), 0, height, wall_mat)
    R.wall(X((hw, b)), X((hw, a)), 0, height, wall_mat)
