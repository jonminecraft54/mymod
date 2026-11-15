"""Offline preview of b3dkit meshes (textured, lambert-shaded, z-buffered).
   python view_models.py            -> out/models5.png (every model of the seventh batch)"""
import math
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

NPCDIR = r"I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9\GFX\npcs"


def render(mesh, texfile, eye, look, size=(420, 320), fov=50.0, light=(0.4, 0.8, 0.5), bg=(28, 28, 32), fullbright=False):
    W, H = size
    tex = np.asarray(Image.open(os.path.join(NPCDIR, texfile)).convert('RGB')).astype(float)
    th, tw = tex.shape[:2]
    eye = np.asarray(eye, float)
    f = np.asarray(look, float) - eye
    f /= np.linalg.norm(f)
    r = np.cross([0, 1, 0], f)
    r /= np.linalg.norm(r)
    u = np.cross(f, r)
    Fc = (W / 2) / math.tan(math.radians(fov) / 2)
    col = np.zeros((H, W, 3)) + bg
    zb = np.full((H, W), np.inf)
    L = np.asarray(light, float)
    L /= np.linalg.norm(L)
    V = np.array([v[:3] for v in mesh.v])
    N = np.array([v[3:6] for v in mesh.v])
    UV = np.array([v[6:8] for v in mesh.v])
    C = np.stack([(V - eye) @ r, (V - eye) @ u, (V - eye) @ f], axis=1)
    for (a, b, c) in mesh.t:
        idx = (a, b, c)
        P = V[list(idx)]
        n = np.cross(P[1] - P[0], P[2] - P[0])           # b3dkit stores (p0, p[i+1], p[i]): clockwise from the front
        if np.dot(n, eye - P[0]) <= 0:
            continue
        z = C[list(idx), 2]
        if (z < 2).any():
            continue
        sx = W / 2 + C[list(idx), 0] / z * Fc
        sy = H / 2 - C[list(idx), 1] / z * Fc
        x0, x1 = max(0, int(sx.min())), min(W - 1, int(sx.max()) + 1)
        y0, y1 = max(0, int(sy.min())), min(H - 1, int(sy.max()) + 1)
        if x1 < x0 or y1 < y0:
            continue
        xs, ys = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
        den = (sy[1] - sy[2]) * (sx[0] - sx[2]) + (sx[2] - sx[1]) * (sy[0] - sy[2])
        if abs(den) < 1e-9:
            continue
        w0 = ((sy[1] - sy[2]) * (xs - sx[2]) + (sx[2] - sx[1]) * (ys - sy[2])) / den
        w1 = ((sy[2] - sy[0]) * (xs - sx[2]) + (sx[0] - sx[2]) * (ys - sy[2])) / den
        w2 = 1 - w0 - w1
        m = (w0 >= -1e-6) & (w1 >= -1e-6) & (w2 >= -1e-6)
        if not m.any():
            continue
        iz = w0 / z[0] + w1 / z[1] + w2 / z[2]
        depth = 1 / iz
        sub = zb[y0:y1 + 1, x0:x1 + 1]
        m &= depth < sub
        if not m.any():
            continue
        uu = (w0 * UV[a, 0] / z[0] + w1 * UV[b, 0] / z[1] + w2 * UV[c, 0] / z[2]) / iz
        vv = (w0 * UV[a, 1] / z[0] + w1 * UV[b, 1] / z[1] + w2 * UV[c, 1] / z[2]) / iz
        tx = np.clip((uu * tw).astype(int), 0, tw - 1)
        ty = np.clip((vv * th).astype(int), 0, th - 1)
        t = tex[ty, tx]
        nn = N[a] / max(1e-6, np.linalg.norm(N[a]))
        shade = 1.0 if fullbright else 0.35 + 0.75 * max(0.0, float(nn @ L))
        cs = col[y0:y1 + 1, x0:x1 + 1]
        cs[m] = np.clip(t[m] * shade, 0, 255)
        sub[m] = depth[m]
    return Image.fromarray(col.astype(np.uint8))


if __name__ == '__main__':
    import make_models5 as M
    meshes = {fn: (tex, mesh) for fn, tex, mesh in M.write_all()}
    views = [('scp052.b3d', (-700, 300, -1300), (0, 150, 0), True), ('scp052.b3d', (-120, 230, -700), (60, 140, 300), True),
             ('scp953f.b3d', (160, 140, 160), (0, 70, 0), False), ('indev_dog.b3d', (140, 110, 150), (0, 55, 0), False),
             ('scp6096.b3d', (260, 220, 260), (0, 100, -30), False), ('scp1269.b3d', (160, 200, 160), (0, 110, 0), False),
             ('scp3325.b3d', (100, 160, 300), (0, 110, 0), False), ('indev_shade.b3d', (260, 220, 300), (0, 150, 0), False),
             ('indev_cart.b3d', (120, 100, 140), (0, 40, 0), False), ('scp482.b3d', (120, 200, 200), (0, 170, 0), False)]
    tiles = []
    for fn, eye, look, fb in views:
        tex, mesh = meshes[fn]
        im = render(mesh, tex, eye, look, fullbright=fb)
        if fn == 'scp3325.b3d':
            jt, jm = meshes['scp3325j.b3d']
            # draw the jaw into the same view: offset its vertices to where the code hangs it
            for i, v in enumerate(jm.v):
                jm.v[i] = (v[0], v[1] + 130, v[2] + 6) + v[3:]
            mesh2 = M.Mesh()
            mesh2.v = list(mesh.v) + list(jm.v)
            mesh2.t = list(mesh.t) + [(a + len(mesh.v), b + len(mesh.v), c + len(mesh.v)) for (a, b, c) in jm.t]
            im = render(mesh2, tex, eye, look)
        ImageDraw.Draw(im).text((6, 4), fn, fill=(240, 220, 120))
        tiles.append(im)
    cols = 5
    sheet = Image.new('RGB', (420 * cols, 320 * ((len(tiles) + cols - 1) // cols)))
    for i, t in enumerate(tiles):
        sheet.paste(t, ((i % cols) * 420, (i // cols) * 320))
    os.makedirs('out', exist_ok=True)
    sheet.save('out/models5.png')
    print('out/models5.png')
