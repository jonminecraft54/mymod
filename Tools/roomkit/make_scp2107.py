r"""SCP-2107 "Diet Ghost": the can (GFX\items\scp2107.b3d + scp2107.png), its inventory icon (INVscp2107.png) and a
promotional poster for the storage room (GFX\map\indev_2107poster.png). Original artwork drawn here from the
article's description (scp-wiki.wikidot.com/scp-2107, CC BY-SA 3.0): a light blue can, the DIET GHOST logo, "SCARE
YOUR THIRST!" beneath it, and the "MADE WITH NATURAL GHOSTS!" sticker.

The model is a 12.2 x 6.6 standard drinks can in centimetres: a 32-sided body with the label wrapped round it, a
tapered shoulder and neck, a top lid with a ring pull, and a domed base. One 1024x1024 texture: the label in the top
three quarters, brushed aluminium below. items.ini scale 0.01 makes it 0.122 units tall.
   python make_scp2107.py"""
import math
import os
import struct
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = r'I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9'
ITEMS = os.path.join(ROOT, 'GFX', 'items')
FB = r'C:\Windows\Fonts\arialbd.ttf'
FI = r'C:\Windows\Fonts\impact.ttf' if os.path.exists(r'C:\Windows\Fonts\impact.ttf') else FB
BLUE = (126, 196, 236)


def ghost(d, cx, cy, s, fill, outline=None):
    """a cartoon ghost: a dome, a wavy hem, two eyes"""
    w = s * 0.9
    pts = [(cx - w / 2, cy)]
    pts += [(cx - w / 2 + w * k / 6, cy + s * 0.55 + (s * 0.12 if k % 2 else 0)) for k in range(7)]
    pts += [(cx + w / 2, cy)]
    d.ellipse([cx - w / 2, cy - w / 2, cx + w / 2, cy + w / 2], fill=fill, outline=outline, width=3 if outline else 0)
    d.polygon(pts, fill=fill)
    d.ellipse([cx - w * 0.22, cy - w * 0.12, cx - w * 0.08, cy + w * 0.08], fill=(30, 40, 60))
    d.ellipse([cx + w * 0.08, cy - w * 0.12, cx + w * 0.22, cy + w * 0.08], fill=(30, 40, 60))


def outlined(d, xy, text, font, fill, stroke, sw):
    d.text(xy, text, font=font, fill=fill, anchor='mm', stroke_width=sw, stroke_fill=stroke)


def label(W=1024, H=768):
    im = Image.new('RGB', (W, H), BLUE)
    d = ImageDraw.Draw(im)
    for y in range(H):                                             # a soft vertical sheen
        t = abs(y / H - 0.45)
        d.line([(0, y), (W, y)], fill=tuple(min(255, int(c + 30 * (0.5 - t))) for c in BLUE))
    d.rectangle([0, 0, W, 36], fill=(232, 240, 248))               # the white bands top and bottom
    d.rectangle([0, H - 36, W, H], fill=(232, 240, 248))
    for side in (0, W // 2):                                        # the logo twice, so one faces you from any side
        cx = side + W // 4
        ghost(d, cx, 210, 120, (250, 252, 255), (40, 70, 110))
        outlined(d, (cx, 380), 'DIET', ImageFont.truetype(FI, 96), (255, 255, 255), (30, 60, 110), 7)
        outlined(d, (cx, 480), 'GHOST', ImageFont.truetype(FI, 118), (255, 255, 255), (30, 60, 110), 8)
        d.text((cx + 150, 430), 'TM', font=ImageFont.truetype(FB, 20), fill=(30, 60, 110), anchor='mm')
        outlined(d, (cx, 585), 'SCARE YOUR THIRST!', ImageFont.truetype(FB, 36), (255, 248, 200), (30, 60, 110), 3)
    # the sticker
    sx, sy = W // 2 + 60, 660
    d.ellipse([sx - 92, sy - 60, sx + 92, sy + 60], fill=(250, 214, 60), outline=(150, 100, 20), width=4)
    d.text((sx, sy - 18), 'MADE WITH', font=ImageFont.truetype(FB, 22), fill=(90, 50, 10), anchor='mm')
    d.text((sx, sy + 12), 'NATURAL GHOSTS!', font=ImageFont.truetype(FB, 20), fill=(90, 50, 10), anchor='mm')
    d.text((W // 4, 690), '12 FL OZ (355 mL)', font=ImageFont.truetype(FB, 18), fill=(30, 60, 110), anchor='mm')
    return im


def metal(W, H):
    im = Image.new('RGB', (W, H), (196, 200, 206))
    d = ImageDraw.Draw(im)
    for y in range(0, H, 2):
        v = 190 + (y * 37 % 23)
        d.line([(0, y), (W, y)], fill=(v, v + 3, v + 8))
    return im.filter(ImageFilter.GaussianBlur(0.8))


def texture():
    tex = Image.new('RGB', (1024, 1024))
    tex.paste(label(), (0, 0))
    tex.paste(metal(1024, 256), (0, 768))
    tex.save(os.path.join(ITEMS, 'scp2107.png'))
    # the inventory icon: the can standing, three quarter view, drawn flat
    ic = Image.new('RGB', (64, 64), (0, 0, 0))
    lab = label().resize((260, 195)).crop((0, 0, 130, 195)).resize((34, 46))
    ic.paste(lab, (15, 11))
    d = ImageDraw.Draw(ic)
    d.rectangle([15, 6, 48, 11], fill=(200, 204, 210))
    d.rectangle([15, 56, 48, 59], fill=(170, 174, 180))
    d.rectangle([14, 6, 49, 59], outline=(90, 90, 96))
    ic.save(os.path.join(ITEMS, 'INVscp2107.png'))
    # a shop-style poster for the storage room
    po = Image.new('RGB', (384, 512), BLUE)
    p = ImageDraw.Draw(po)
    ghost(p, 192, 150, 150, (250, 252, 255), (40, 70, 110))
    outlined(p, (192, 300), 'DIET GHOST', ImageFont.truetype(FI, 64), (255, 255, 255), (30, 60, 110), 5)
    outlined(p, (192, 370), 'SCARE YOUR THIRST!', ImageFont.truetype(FB, 30), (255, 248, 200), (30, 60, 110), 3)
    p.text((192, 450), 'FOUNDATION PROPERTY - DO NOT DRINK', font=ImageFont.truetype(FB, 16), fill=(150, 20, 20), anchor='mm')
    p.rectangle([0, 0, 383, 511], outline=(30, 60, 110), width=10)
    po.save(os.path.join(ROOT, 'GFX', 'map', 'indev_2107poster.png'))


# ---------------------------------------------------------------- the model
def chunk(tag, body):
    return tag + struct.pack('<i', len(body)) + body


def cstr(s):
    return s.encode('latin-1') + b'\0'


def can_mesh(N=32):
    V, T = [], []

    def ring(r, y, v, nrm_y=0.0):
        start = len(V)
        for k in range(N + 1):
            a = 2 * math.pi * k / N
            c, s = math.cos(a), math.sin(a)
            l = math.sqrt(1 + nrm_y * nrm_y)
            V.append((r * c, y, r * s, c / l, nrm_y / l, s / l, k / N, v))
        return start

    def band(a, b):
        for k in range(N):
            T.append((a + k, b + k, a + k + 1))
            T.append((a + k + 1, b + k, b + k + 1))

    def cap(y, r, up, u0, v0, us, vs):
        c = len(V)
        V.append((0, y, 0, 0, 1 if up else -1, 0, u0, v0))
        s = len(V)
        for k in range(N + 1):
            a = 2 * math.pi * k / N
            V.append((r * math.cos(a), y, r * math.sin(a), 0, 1 if up else -1, 0, u0 + us * math.cos(a), v0 + vs * math.sin(a)))
        for k in range(N):
            T.append((c, s + k + 1, s + k) if up else (c, s + k, s + k + 1))

    R0, H = 3.3, 12.2
    # metal bands (v 0.76 .. 0.99) and the label (v 0.0 .. 0.75)
    b0 = ring(2.6, 0.0, 0.99, -1.0)                  # the base rim
    b1 = ring(R0, 0.6, 0.90, -0.4)
    l0 = ring(R0, 0.6, 0.745)                        # label bottom
    l1 = ring(R0, 10.6, 0.005)                       # label top
    m0 = ring(R0, 10.6, 0.80, 0.4)                   # the shoulder
    m1 = ring(2.65, 11.8, 0.88, 0.6)
    m2 = ring(2.65, 12.2, 0.95)                      # the lip
    band(b0, b1)
    band(l0, l1)
    band(m0, m1)
    band(m1, m2)
    cap(12.1, 2.6, True, 0.5, 0.875, 0.1, 0.1)       # the lid
    cap(0.25, 2.6, False, 0.5, 0.875, 0.1, 0.1)      # the domed base, seen from below
    # the ring pull: a thin flat loop on the lid
    s = len(V)
    for (x, z) in ((-0.6, -0.2), (0.9, -0.5), (0.9, 0.5), (-0.6, 0.2)):
        V.append((x, 12.25, z, 0, 1, 0, 0.3, 0.9))
    T += [(s, s + 2, s + 1), (s, s + 3, s + 2)]
    return V, T


def write_b3d(path, V, T):
    texs = chunk(b'TEXS', cstr('scp2107.png') + struct.pack('<2i5f', 1, 2, 0, 0, 1, 1, 0))
    brus = chunk(b'BRUS', struct.pack('<i', 1) + cstr('diet ghost') + struct.pack('<5f2i', 1, 1, 1, 1, 0.8, 1, 0) + struct.pack('<i', 0))
    vb = struct.pack('<3i', 1, 1, 2) + b''.join(struct.pack('<8f', *v) for v in V)
    tb = struct.pack('<i', 0) + b''.join(struct.pack('<3i', *t) for t in T)
    mesh = chunk(b'MESH', struct.pack('<i', 0) + chunk(b'VRTS', vb) + chunk(b'TRIS', tb))
    node = chunk(b'NODE', cstr('scp2107') + struct.pack('<10f', 0, 0, 0, 1, 1, 1, 1, 0, 0, 0) + mesh)
    open(path, 'wb').write(chunk(b'BB3D', struct.pack('<i', 1) + texs + brus + node))


if __name__ == '__main__':
    texture()
    V, T = can_mesh()
    write_b3d(os.path.join(ITEMS, 'scp2107.b3d'), V, T)
    print('scp2107: %d vertices, %d triangles; texture, icon and poster written' % (len(V), len(T)))
