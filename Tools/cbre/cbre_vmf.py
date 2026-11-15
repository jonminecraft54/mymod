r"""CBRE room writer: build an SCP:CB room once, out of brushes and CBRE entities, and write it as a .vmf that CBRE-EX
opens (File > Open), plus a lit preview render made with Tools\roomkit.

Everything written here is a format CBRE-EX itself reads (checked against its source, github.com/AnalogFeelings/cbre-ex):
  * VmfProvider:   world { solid { side { "plane" "(x y z) (x y z) (x y z)" "material" "<name>"
                   "uaxis" "[ux uy uz shift] scale" "vaxis" "[...] scale" "rotation" "0" } } } and entity { "classname" ... }
  * RMeshExport:   point entities light / spotlight / waypoint / soundemitter / model / screen
  * Light.cs:      light: color (Color255), intensity, range, hassprite;  spotlight: + angles, innerconeangle, outerconeangle
  * RMeshExport:   soundemitter: sound (int index), range;  model: file, angles, scale;  screen: imgpath
  * tool textures: tooltextures/invisible_collision, tooltextures/remove_face, tooltextures/block_light
CBRE (like Hammer) is Z-up: a room point (x, y-up, z) is written as CBRE (x, z, y). Its RMesh export swaps them back.
Units are SCP:CB room units: a room is 2048 x 2048, the floor at 0, doorways 192 wide and 320 high.

Textures are named as CBRE lists them once the game's GFX\map folder is added to its texture directories: the file
name without its extension (e.g. "whitewall", "tilefloor"). Props are file names in GFX\map\Props (e.g. "scpcb_chair.x")."""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
MAP = os.path.join(ROOT, 'GFX', 'map')
sys.path.insert(0, os.path.join(ROOT, 'Tools', 'roomkit'))

# texel scale per material: world units per texel (texture size / units it should cover)
COVER = {'whitewall': 364, 'officewall': 364, 'concretewall': 384, 'tilefloor': 256, 'concretefloor': 256,
         'ceiling': 256, 'metal': 256, 'dirtymetal': 256, 'misc': 210, 'metalpanels': 168, 'metalpanels2': 168,
         'vent': 128, 'pipes': 256, 'grating': 128, 'wood': 256, 'scpcb_cabinet': 176, 'scpcb_rivetband': 256,
         'scpcb_checkerplate': 128, 'old_whitewall': 384, 'dclass_wall': 256, 'metal3': 205, 'white': 256,
         'scpcb_lightpanel': 96, 'red': 64, 'yellowmetal': 256, 'hazard_stripe_wall_1789291234341': 256}


def tex_px(name):
    for ext in ('.jpg', '.png'):
        p = os.path.join(MAP, name + ext)
        if os.path.exists(p):
            try:
                from PIL import Image
                return Image.open(p).size[0], name + ext
            except Exception:
                return 512, name + ext
    return 512, None


def fmt(v):
    v = round(float(v), 3)
    return ('%d' % v) if v == int(v) else ('%g' % v)


class Room:
    """brushes and entities of one room, in room units (x, y up, z)"""

    def __init__(self, name, desc=''):
        self.name, self.desc = name, desc
        self.brushes = []      # (list of faces: [(p1, p2, p3) in room units, material, decal_uv_or_None])
        self.ents = []         # dicts
        self.preview = []      # callables(R) for the roomkit preview

    # ------------------------------------------------------------ brushes
    def box(self, x0, y0, z0, x1, y1, z1, mat, top=None, bottom=None, faces=None):
        """an axis-aligned box. mat for every face, or top / bottom / faces={'x0': m, 'x1': m, 'z0': m, ...}"""
        x0, x1 = sorted((x0, x1)); y0, y1 = sorted((y0, y1)); z0, z1 = sorted((z0, z1))
        f = dict(x0=mat, x1=mat, y0=bottom or mat, y1=top or mat, z0=mat, z1=mat)
        f.update(faces or {})
        quads = {  # each face as 4 corners; the plane is made from 3 of them and oriented outwards below
            'y1': [(x0, y1, z0), (x1, y1, z0), (x1, y1, z1)], 'y0': [(x0, y0, z0), (x1, y0, z0), (x1, y0, z1)],
            'x0': [(x0, y0, z0), (x0, y1, z0), (x0, y1, z1)], 'x1': [(x1, y0, z0), (x1, y1, z0), (x1, y1, z1)],
            'z0': [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0)], 'z1': [(x0, y0, z1), (x1, y0, z1), (x1, y1, z1)]}
        c = ((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2)
        self.brushes.append([(orient(quads[k], c), f[k]) for k in ('y1', 'y0', 'x0', 'x1', 'z0', 'z1')])
        mats = f
        self.preview.append(lambda R, a=(x0, y0, z0, x1, y1, z1), m=mats: R.box(*a, M(m['x0']), top=M(m['y1']), lux=10))

    def prism(self, cx, cz, r, y0, y1, mat, n=8, cap=None, along='y', length=None):
        """a regular n-sided prism: upright (along='y', centre cx, cz) or lying along x / z (cx, cz = the other two
        coordinates of its axis line, y0..y1 = its extent along the axis)"""
        pts = [(r * math.cos(2 * math.pi * (k + 0.5) / n), r * math.sin(2 * math.pi * (k + 0.5) / n)) for k in range(n)]
        faces = []
        if along == 'y':
            P = lambda a, b, h: (cx + a, h, cz + b)
            c = (cx, (y0 + y1) / 2, cz)
        elif along == 'x':
            P = lambda a, b, h: (h, cx + a, cz + b)        # cx = y, cz = z of the axis
            c = ((y0 + y1) / 2, cx, cz)
        else:
            P = lambda a, b, h: (cx + a, cz + b, h)        # cx = x, cz = y of the axis
            c = (cx, cz, (y0 + y1) / 2)
        for k in range(n):
            (a1, b1), (a2, b2) = pts[k], pts[(k + 1) % n]
            faces.append((orient([P(a1, b1, y0), P(a2, b2, y0), P(a2, b2, y1)], c), mat))
        faces.append((orient([P(*pts[0], y1), P(*pts[1], y1), P(*pts[2], y1)], c), cap or mat))
        faces.append((orient([P(*pts[0], y0), P(*pts[1], y0), P(*pts[2], y0)], c), cap or mat))
        self.brushes.append(faces)
        if along == 'y':
            self.preview.append(lambda R: R.prism([(cx + a, cz + b) for a, b in pts], y0, y1, M(mat), caps='TB'))
        else:
            p0, p1 = P(0, 0, y0), P(0, 0, y1)
            self.preview.append(lambda R: R.tube(p0, p1, r, M(mat), sides=n, caps=True))

    def decal(self, cx, cz, facing, w, h, yc, mat, depth=1.0):
        """a picture (sign, poster, label) as a thin brush standing proud of a wall; only its front shows,
        the other faces are tooltextures/remove_face so the export drops them"""
        facing = {'+x': 'E', '-x': 'W', '+z': 'N', '-z': 'S'}.get(facing, facing)
        hw, hh = w / 2, h / 2
        RF ='tooltextures/remove_face'
        if facing in ('E', 'W'):
            s = 1 if facing == 'E' else -1
            x0, x1 = sorted((cx, cx + s * depth))
            self.box(x0, yc - hh, cz - hw, x1, yc + hh, cz + hw, RF, faces={('x1' if s > 0 else 'x0'): mat})
        else:
            s = 1 if facing == 'N' else -1
            z0, z1 = sorted((cz, cz + s * depth))
            self.box(cx - hw, yc - hh, z0, cx + hw, yc + hh, z1, RF, faces={('z1' if s > 0 else 'z0'): mat})
        self.preview[-1] = lambda R, a=(cx, cz, facing, w, h, yc, mat): R_decal(R, *a)

    # ------------------------------------------------------------ walls with openings
    def wall_x(self, x, z0, z1, y0, y1, t, mat, holes=(), inner='+'):
        """a wall in the x = const plane from z0 to z1, t thick, growing away from the room side (inner '+': the
        room is at larger x, the wall from x - t to x). holes: (zc0, zc1, h0, h1)"""
        xa, xb = (x - t, x) if inner == '+' else (x, x + t)
        for a, b, segs in split(z0, z1, holes, y0, y1):
            for h0, h1 in segs:
                self.box(xa, h0, a, xb, h1, b, mat)

    def wall_z(self, z, x0, x1, y0, y1, t, mat, holes=(), inner='+'):
        za, zb = (z - t, z) if inner == '+' else (z, z + t)
        for a, b, segs in split(x0, x1, holes, y0, y1):
            for h0, h1 in segs:
                self.box(a, h0, za, b, h1, zb, mat)

    # ------------------------------------------------------------ entities
    def light(self, x, y, z, color=(255, 250, 240), rng=900, intensity=1.0):
        self.ents.append(dict(classname='light', origin=(x, y, z), color='%d %d %d' % color, intensity=fmt(intensity),
                              range=fmt(rng), hassprite='True'))
        self.preview.append(lambda R: R.light(x, y - 6, z, rng, color, 60 * intensity))

    def spot(self, x, y, z, pitch=90, yaw=0, color=(255, 240, 220), rng=900, intensity=1.0, inner=30, outer=60):
        self.ents.append(dict(classname='spotlight', origin=(x, y, z), color='%d %d %d' % color, intensity=fmt(intensity),
                              range=fmt(rng), hassprite='True', angles='%s %s 0' % (fmt(pitch), fmt(yaw)),
                              innerconeangle=fmt(inner), outerconeangle=fmt(outer)))

    def waypoint(self, x, z, y=20):
        self.ents.append(dict(classname='waypoint', origin=(x, y, z)))

    def sound(self, x, y, z, index, rng=6):
        self.ents.append(dict(classname='soundemitter', origin=(x, y, z), sound=str(index), range=fmt(rng)))

    def model(self, file, x, y, z, yaw=0, scale=1.0):
        s = fmt(scale)
        self.ents.append(dict(classname='model', origin=(x, y, z), file=file, angles='0 %s 0' % fmt(yaw),
                              scale='%s %s %s' % (s, s, s)))
        self.preview.append(lambda R: R.model(file, x, y, z, rot=(0, yaw, 0), scale=(scale,) * 3, size=(40, 60, 40)))

    # ------------------------------------------------------------ output
    def write_vmf(self, path):
        ids = iter(range(1, 1000000))
        out = ['versioninfo', '{', '\t"editorname" "CBRE-EX"', '\t"editorversion" "2.2"', '\t"editorbuild" "1"',
               '\t"mapversion" "1"', '\t"formatversion" "100"', '\t"prefab" "0"', '}',
               'visgroups', '{', '}', 'viewsettings', '{', '\t"bSnapToGrid" "1"', '\t"bShowGrid" "1"', '\t"nGridSpacing" "16"', '}',
               'world', '{', '\t"id" "%d"' % next(ids), '\t"mapversion" "1"', '\t"classname" "worldspawn"']
        for faces in self.brushes:
            out += ['\tsolid', '\t{', '\t\t"id" "%d"' % next(ids)]
            for (p1, p2, p3), mat in faces:
                n = normal(p1, p2, p3)
                u, v = tex_axes(n)
                sc = scale_of(mat)
                out += ['\t\tside', '\t\t{', '\t\t\t"id" "%d"' % next(ids),
                        '\t\t\t"plane" "(%s) (%s) (%s)"' % (C(p1), C(p2), C(p3)),
                        '\t\t\t"material" "%s"' % mat,
                        '\t\t\t"uaxis" "[%s 0] %s"' % (' '.join(fmt(k) for k in u), fmt(sc)),
                        '\t\t\t"vaxis" "[%s 0] %s"' % (' '.join(fmt(k) for k in v), fmt(sc)),
                        '\t\t\t"rotation" "0"', '\t\t}']
            out += ['\t\teditor', '\t\t{', '\t\t\t"color" "0 180 200"', '\t\t\t"visgroupshown" "1"', '\t\t}', '\t}']
        out += ['}']
        for e in self.ents:
            out += ['entity', '{', '\t"id" "%d"' % next(ids), '\t"classname" "%s"' % e['classname']]
            for k, v in e.items():
                if k in ('classname', 'origin'):
                    continue
                out.append('\t"%s" "%s"' % (k, v))
            out.append('\t"origin" "%s"' % C(e['origin']))
            out += ['\teditor', '\t{', '\t\t"color" "220 30 220"', '\t\t"visgroupshown" "1"', '\t}', '}']
        out += ['cameras', '{', '\t"activecamera" "-1"', '}', 'cordon', '{', '\t"mins" "(-1024 -1024 -64)"',
                '\t"maxs" "(1024 1024 1024)"', '\t"active" "0"', '}']
        open(path, 'w', newline='\r\n').write('\n'.join(out) + '\n')
        return len(self.brushes), len(self.ents)

    def render(self, views, path, size=(800, 450)):
        """a lit preview with Tools\roomkit (the same geometry, baked)"""
        import roomkit
        from PIL import Image
        R = roomkit.Room(self.name + '_cbrepreview', luxel=8.0, ambient=10, fill=0.16)
        for f in self.preview:
            f(R)
        R.bake(verbose=False, max_size=2048)
        ims = []
        for i, (eye, look) in enumerate(views):
            p = path.replace('.jpg', '_%d.png' % i)
            R.render(eye, look, p, size=size)
            ims.append(Image.open(p))
        W = size[0] * min(2, len(ims))
        H = size[1] * ((len(ims) + 1) // 2)
        sheet = Image.new('RGB', (W, H))
        for i, im in enumerate(ims):
            sheet.paste(im, ((i % 2) * size[0], (i // 2) * size[1]))
            os.remove(path.replace('.jpg', '_%d.png' % i))
        sheet.save(path, quality=88)


# ---------------------------------------------------------------- helpers
def C(p):
    """room (x, y-up, z) -> CBRE / Hammer (x, y, z-up)"""
    return '%s %s %s' % (fmt(p[0]), fmt(p[2]), fmt(p[1]))


def to_cbre(p):
    return (p[0], p[2], p[1])


def normal(p1, p2, p3):
    """the plane normal as CBRE computes it, in CBRE space: (p3 - p1) x (p2 - p1)"""
    a, b, c = to_cbre(p1), to_cbre(p2), to_cbre(p3)
    u = [c[i] - a[i] for i in range(3)]
    w = [b[i] - a[i] for i in range(3)]
    n = (u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0])
    l = math.sqrt(sum(k * k for k in n)) or 1
    return tuple(k / l for k in n)


def orient(tri, centre):
    """order the three points so the CBRE plane normal points out of the brush (away from its centre)"""
    p1, p2, p3 = tri
    n = normal(p1, p2, p3)
    d = [to_cbre(p1)[i] - to_cbre(centre)[i] for i in range(3)]
    if sum(n[i] * d[i] for i in range(3)) < 0:
        return (p1, p3, p2)
    return (p1, p2, p3)


def tex_axes(n):
    """Hammer's world-aligned texture axes for a face with CBRE normal n"""
    ax = max(range(3), key=lambda i: abs(n[i]))
    if ax == 2:
        return (1, 0, 0), (0, -1, 0)
    if ax == 0:
        return (0, 1, 0), (0, 0, -1)
    return (1, 0, 0), (0, 0, -1)


def scale_of(mat):
    if mat.startswith('tooltextures'):
        return 0.25
    px, _ = tex_px(mat)
    return COVER.get(mat.lower(), 256) / float(px)


def split(a0, a1, holes, y0, y1):
    """cut the span a0..a1 at the holes: [(a, b, [(h0, h1), ...]), ...] - solid parts full height, holes leave
    the strips below and above them"""
    cuts = sorted(holes)
    out, a = [], a0
    for c0, c1, h0, h1 in cuts:
        if c0 > a:
            out.append((a, c0, [(y0, y1)]))
        segs = []
        if h0 > y0:
            segs.append((y0, h0))
        if h1 < y1:
            segs.append((h1, y1))
        out.append((c0, c1, segs))
        a = c1
    if a < a1:
        out.append((a, a1, [(y0, y1)]))
    return out


_MATS = {}


def M(name):
    """a roomkit material for the preview"""
    import roomkit
    if name.startswith('tooltextures'):
        name = 'black'
    if name not in _MATS:
        px, f = tex_px(name)
        _MATS[name] = roomkit.Mat(f or 'white.jpg', COVER.get(name.lower(), 256))
    return _MATS[name]


def R_decal(R, cx, cz, facing, w, h, yc, mat):
    from v02kit import wall_decal
    import roomkit
    px, f = tex_px(mat)
    wall_decal(R, roomkit.Mat(f or 'white.jpg', cast=False), cx, cz, facing, w, h, yc)
