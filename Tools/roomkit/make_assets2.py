"""Assets for the second (Indev zone) batch of rooms:
   GFX\\map\\indev_signs2.png (+ signs2.json)   wall signs and the yellow SCP door labels
   GFX\\map\\indev_mesh.png                     wire mesh for the test cage (alpha)
   GFX\\map\\indev_chain.png                    hanging chain strip (alpha)
   GFX\\map\\indev_017.png                      SCP-017, a child-sized shadow (alpha sprite)
   GFX\\npcs\\scp131.b3d + scp131a.png / scp131b.png   the Eye Pods
   GFX\\npcs\\scp999.b3d + scp999.png                  the Tickle Monster
"""
import json
import math
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from b3dkit import Mesh, write_b3d

ROOT = r"I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9"
MAPDIR = os.path.join(ROOT, 'GFX', 'map')
NPCDIR = os.path.join(ROOT, 'GFX', 'npcs')
F = r"C:\Windows\Fonts"


def font(sz, bold=True):
    return ImageFont.truetype(os.path.join(F, 'arialbd.ttf' if bold else 'arial.ttf'), sz)


# ------------------------------------------------------------------ signs
def signs():
    W = H = 1024
    im = Image.new('RGB', (W, H), (20, 20, 20))
    d = ImageDraw.Draw(im)
    rects = {}

    def fit(text, w, h, maxsz=200):
        sz = maxsz
        while sz > 6:
            f = font(sz)
            bb = d.multiline_textbbox((0, 0), text, font=f, spacing=sz * 0.12, align='center')
            if bb[2] - bb[0] <= w and bb[3] - bb[1] <= h:
                return f, bb
            sz -= 2
        return f, bb

    def plate(name, x, y, w, h, text, bg, fg, border=None, head=None, headbg=None, headfg=None, headh=0.36):
        rects[name] = (x / W, y / H, (x + w) / W, (y + h) / H)
        d.rectangle([x, y, x + w - 1, y + h - 1], fill=bg)
        if border:
            d.rectangle([x + 3, y + 3, x + w - 4, y + h - 4], outline=border, width=4)
        ty, th = y, h
        if head:
            hh = int(h * headh)
            d.rectangle([x + 8, y + 8, x + w - 9, y + hh], fill=headbg)
            f, bb = fit(head, w - 40, hh - 22)
            d.text((x + w / 2 - (bb[2] + bb[0]) / 2, y + 8 + (hh - 8) / 2 - (bb[3] + bb[1]) / 2), head, font=f, fill=headfg)
            ty, th = y + hh, h - hh
        f, bb = fit(text, w - 36, th - 26)
        d.multiline_text((x + w / 2 - (bb[2] + bb[0]) / 2, ty + th / 2 - (bb[3] + bb[1]) / 2), text, font=f, fill=fg,
                         spacing=f.size * 0.12, align='center')

    def label(name, x, y, num, cls, colour):
        """The yellow door label of the reference shots: SCP header, item number, class, hazard mark."""
        w, h = 256, 320
        rects[name] = (x / W, y / H, (x + w) / W, (y + h) / H)
        d.rectangle([x, y, x + w - 1, y + h - 1], fill=(238, 236, 228))
        d.rectangle([x, y, x + w - 1, y + 78], fill=(236, 208, 34))
        d.text((x + 14, y + 6), "SCP", font=font(50), fill=(20, 20, 20))
        cx, cy = x + 200, y + 38
        d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], outline=(20, 20, 20), width=4)
        d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], outline=(20, 20, 20), width=3)
        for k in range(3):
            a = math.radians(90 + 120 * k)
            d.line([(cx + 12 * math.cos(a), cy - 12 * math.sin(a)), (cx + 30 * math.cos(a), cy - 30 * math.sin(a))], fill=(20, 20, 20), width=5)
        d.text((x + 14, y + 60), "Secure. Contain. Protect.", font=font(11), fill=(40, 40, 40))
        d.text((x + 14, y + 92), num, font=font(34), fill=(20, 20, 20))
        d.text((x + 14, y + 134), "OBJECT CLASS:", font=font(17), fill=(20, 20, 20))
        d.text((x + 14, y + 156), cls, font=font(28), fill=colour)
        # hazard triangle
        tx, ty = x + 70, y + 250
        d.polygon([(tx, ty - 52), (tx - 52, ty + 40), (tx + 52, ty + 40)], fill=(236, 208, 34), outline=(20, 20, 20))
        d.text((tx, ty + 6), "!", font=font(56), fill=(20, 20, 20), anchor='mm')
        d.rectangle([x + 136, y + 200, x + 240, y + 300], fill=(26, 26, 28))
        d.rectangle([x, y, x + w - 1, y + h - 1], outline=(30, 30, 30), width=3)

    BLK, WHT, YEL, RED, BLU = (22, 22, 22), (235, 233, 226), (232, 196, 28), (190, 28, 24), (30, 80, 170)
    plate('blockd', 0, 0, 512, 128, "CONTAINMENT BLOCK D", BLK, WHT, border=(120, 120, 120))
    plate('shaft4', 512, 0, 512, 128, "MAINTENANCE SHAFT 4", BLK, YEL, border=(120, 110, 40))
    plate('test4a', 0, 128, 512, 128, "TEST CHAMBER 4-A", BLK, WHT, border=(120, 120, 120))
    plate('observe', 512, 128, 512, 128, "OBSERVATION 4-C", BLK, WHT, border=(120, 120, 120))
    plate('stores4', 0, 256, 320, 128, "STORES 4", BLK, WHT, border=(120, 120, 120))
    plate('lampreset', 320, 256, 352, 128, "LAMP CIRCUIT\nRESET", BLK, YEL, border=(120, 110, 40))
    plate('cagelock', 672, 256, 352, 128, "CAGE LOCK", BLK, YEL, border=(120, 110, 40))
    label('l_017', 0, 384, "SCP-017", "KETER", (180, 24, 20))
    label('l_131', 256, 384, "SCP-131", "SAFE", (30, 120, 40))
    label('l_999', 512, 384, "SCP-999", "SAFE", (30, 120, 40))
    plate('d_shadow', 768, 384, 256, 256, "CAST NO\nSHADOW ON\nTHE CAGE", WHT, BLK, head="DANGER", headbg=RED, headfg=WHT)
    plate('c_lamps', 0, 704, 256, 256, "KEEP ALL\nLAMPS LIT", YEL, BLK, head="CAUTION", headbg=BLK, headfg=YEL)
    plate('n_999', 256, 704, 256, 256, "IT HAS BEEN\nFED. IT WILL\nSAY IT HAS\nNOT.", WHT, BLK, head="NOTICE", headbg=BLU, headfg=WHT)
    plate('n_pods', 512, 704, 256, 256, "EYE PODS ARE\nNOT TO LEAVE\nTHE CHAMBER\nUNESCORTED", WHT, BLK, head="NOTICE", headbg=BLU, headfg=WHT)
    plate('freight', 768, 640, 256, 96, "FREIGHT LIFT", BLK, WHT, border=(120, 120, 120))
    plate('b2', 768, 736, 128, 96, "B2", BLK, WHT, border=(120, 120, 120))
    plate('up', 896, 736, 128, 96, "UP", BLK, WHT, border=(120, 120, 120))
    plate('locked', 768, 832, 256, 64, "LOCKED", RED, WHT, border=WHT)
    plate('released', 768, 896, 256, 64, "RELEASED", (30, 110, 40), WHT, border=WHT)
    plate('pry', 0, 960, 512, 64, "STORES - SIGN OUT ALL ISSUE", BLK, WHT)
    plate('lit', 512, 960, 256, 64, "LAMPS: 6 / 6", (30, 110, 40), WHT, border=WHT)

    a = np.asarray(im).astype(np.float64)
    rng = np.random.default_rng(77)
    g = rng.normal(0, 9, (H, W))
    sm = np.asarray(Image.fromarray((rng.random((H // 8, W // 8)) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)
                    .filter(ImageFilter.GaussianBlur(6))).astype(np.float64) / 255.0
    a = a * (0.80 + 0.28 * sm[..., None]) + g[..., None]
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    d2 = ImageDraw.Draw(im)
    for _ in range(140):
        x, y = rng.integers(0, W), rng.integers(0, H)
        l = int(rng.integers(6, 40))
        ang = rng.random() * 6.28
        c = int(rng.integers(40, 110))
        d2.line([(x, y), (x + l * np.cos(ang), y + l * np.sin(ang))], fill=(c, c, c), width=1)
    im = im.filter(ImageFilter.GaussianBlur(0.5))
    im.save(os.path.join(MAPDIR, 'indev_signs2.png'))
    json.dump(rects, open('signs2.json', 'w'), indent=1)
    im.save('out/indev_signs2_preview.png')


# ------------------------------------------------------------------ alpha textures
def mesh_tex():
    S = 128
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i in range(0, S + 1, 32):
        d.line([(i, 0), (i, S)], fill=(74, 76, 80, 255), width=5)
        d.line([(0, i), (S, i)], fill=(74, 76, 80, 255), width=5)
    for i in range(0, S + 1, 32):
        d.line([(i - 1, 0), (i - 1, S)], fill=(128, 130, 134, 255), width=1)
        d.line([(0, i - 1), (S, i - 1)], fill=(128, 130, 134, 255), width=1)
    im.save(os.path.join(MAPDIR, 'indev_mesh.png'))


def chain_tex():
    W, H = 32, 256
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for k in range(8):
        y = k * 32
        if k % 2 == 0:
            d.ellipse([7, y + 1, 24, y + 34], outline=(34, 32, 30, 255), width=5)
            d.ellipse([9, y + 3, 22, y + 32], outline=(70, 66, 60, 255), width=1)
        else:
            d.rectangle([13, y - 4, 18, y + 36], fill=(30, 28, 26, 255))
            d.line([(14, y - 4), (14, y + 36)], fill=(66, 62, 58, 255), width=1)
    im.save(os.path.join(MAPDIR, 'indev_chain.png'))


def shadow_tex():
    W, H = 128, 256
    a = np.zeros((H, W))
    yy, xx = np.mgrid[0:H, 0:W]

    def blob(cx, cy, rx, ry, s=1.0):
        return s * np.clip(1.4 - np.sqrt(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2) * 1.4, 0, 1)
    a = np.maximum(a, blob(64, 44, 26, 30))          # head
    a = np.maximum(a, blob(64, 120, 32, 62))         # body
    a = np.maximum(a, blob(34, 122, 12, 54))         # arms
    a = np.maximum(a, blob(94, 122, 12, 54))
    a = np.maximum(a, blob(50, 206, 14, 50))         # legs
    a = np.maximum(a, blob(78, 206, 14, 50))
    al = np.asarray(Image.fromarray((np.clip(a * 1.6, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3.5)))
    rgba = np.zeros((H, W, 4), dtype=np.uint8)
    rgba[..., 3] = al
    Image.fromarray(rgba).save(os.path.join(MAPDIR, 'indev_017.png'))


# ------------------------------------------------------------------ SCP-131
def pod_tex(name, body, dark):
    S = 256
    rng = np.random.default_rng(len(name) * 7 + 131)
    a = np.zeros((S, S, 3))
    v = np.linspace(0, 1, S)[:, None]
    # left 3/4: body skin, lighter towards the tip (v = 0 is the tip)
    base = np.array(body, dtype=float)[None, None, :] * (1.05 - 0.35 * v)[..., None]
    base = base + rng.normal(0, 5, (S, S, 1))
    a[:, :] = np.broadcast_to(base, (S, S, 3))
    # a darker band low on the body and the wheel
    a[int(S * 0.86):, :192] = np.array(dark, dtype=float) * 0.8
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    # right quarter top: the eye (white, blue iris, pupil, highlight)
    d.rectangle([192, 0, 255, 127], fill=(232, 232, 226))
    d.ellipse([200, 40, 248, 88], fill=(40, 110, 200), outline=(20, 50, 110), width=2)
    d.ellipse([214, 54, 234, 74], fill=(8, 8, 12))
    d.ellipse([228, 50, 236, 58], fill=(245, 245, 250))
    # right quarter bottom: wheel tread
    d.rectangle([192, 128, 255, 255], fill=(36, 36, 38))
    for y in range(132, 256, 12):
        d.line([(192, y), (255, y)], fill=(62, 62, 64), width=3)
    im = im.filter(ImageFilter.GaussianBlur(0.5))
    im.save(os.path.join(NPCDIR, name))


def pod_mesh():
    m = Mesh()
    BODY = (0.02, 0.02, 0.72, 0.84)
    EYE = (0.76, 0.01, 0.99, 0.49)
    TREAD = (0.76, 0.52, 0.99, 0.98)
    # the wheel it rolls on
    m.cyl((-0.10, 0.13, 0), (0.10, 0.13, 0), 0.13, sides=12, uvrect=TREAD, capuv=TREAD)
    # teardrop body (lathe), tip up
    prof = [(0.20, 0.10), (0.33, 0.22), (0.37, 0.38), (0.34, 0.54), (0.25, 0.70), (0.13, 0.86), (0.04, 0.96), (0.0, 1.0)]
    n = len(prof) - 1
    for i in range(n):
        (r0, y0), (r1, y1) = prof[i], prof[i + 1]
        v0 = BODY[3] - (BODY[3] - BODY[1]) * i / n
        v1 = BODY[3] - (BODY[3] - BODY[1]) * (i + 1) / n
        m.cyl((0, y0, 0), (0, y1, 0), r0, max(r1, 0.0005), sides=14, uvrect=(BODY[0], v1, BODY[2], v0), caps=False)
    m.cyl((0, 0.08, 0), (0, 0.10, 0), 0.19, 0.20, sides=14, uvrect=(BODY[0], 0.86, BODY[2], 0.99), caps=True,
          capuv=(0.02, 0.88, 0.2, 0.98))
    # the eye: a shallow disc on the front (+z is forward)
    m.cyl((0, 0.47, 0.30), (0, 0.47, 0.375), 0.15, 0.13, sides=14, uvrect=(0.77, 0.02, 0.80, 0.06), caps=True, capuv=EYE)
    return m


# ------------------------------------------------------------------ SCP-999
def blob_tex():
    S = 256
    rng = np.random.default_rng(999)
    yy, xx = np.mgrid[0:S, 0:S]
    v = yy / S
    a = np.zeros((S, S, 3))
    a[..., 0] = 244 - 40 * v
    a[..., 1] = 150 - 70 * v
    a[..., 2] = 28 + 10 * v
    for _ in range(26):                      # lighter bubbles in the jelly
        cx, cy, r = rng.integers(0, S), rng.integers(0, S), rng.integers(5, 22)
        g = np.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / (r * r))
        a += g[..., None] * np.array([18.0, 44.0, 30.0])
    for _ in range(6):                       # glossy highlights
        cx, cy, r = rng.integers(20, S - 20), rng.integers(10, S // 2), rng.integers(6, 14)
        g = np.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / (r * r))
        a += g[..., None] * 90
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2)).save(os.path.join(NPCDIR, 'scp999.png'))


def blob_mesh():
    m = Mesh()

    def lump(cx, cz, R, Hh, sides=14):
        prof = [(1.0, 0.0), (1.06, 0.14), (0.98, 0.36), (0.80, 0.60), (0.52, 0.82), (0.22, 0.95), (0.0, 1.0)]
        n = len(prof) - 1
        for i in range(n):
            (r0, y0), (r1, y1) = prof[i], prof[i + 1]
            m.cyl((cx, y0 * Hh, cz), (cx, y1 * Hh, cz), r0 * R, max(r1 * R, 0.0005), sides=sides,
                  uvrect=(0, 1 - (i + 1) / n, 1, 1 - i / n), caps=False)
    lump(0, 0, 0.50, 0.46)
    lump(0.34, 0.20, 0.24, 0.24, 10)
    lump(-0.30, 0.26, 0.20, 0.20, 10)
    lump(0.06, -0.40, 0.22, 0.22, 10)
    lump(-0.36, -0.18, 0.17, 0.30, 10)       # the pseudopod it waves
    return m


if __name__ == '__main__':
    os.makedirs('out', exist_ok=True)
    signs()
    mesh_tex()
    chain_tex()
    shadow_tex()
    pod_tex('scp131a.png', (214, 104, 34), (120, 56, 20))     # burnt orange
    pod_tex('scp131b.png', (222, 184, 48), (130, 104, 26))    # mustard yellow
    print('scp131.b3d', write_b3d(os.path.join(NPCDIR, 'scp131.b3d'), 'scp131a.png', pod_mesh(), name='pod'))
    blob_tex()
    print('scp999.b3d', write_b3d(os.path.join(NPCDIR, 'scp999.b3d'), 'scp999.png', blob_mesh(), name='blob', shininess=0.6))
    print('assets written')
