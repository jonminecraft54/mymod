"""Models the game code moves, shows and hides in the seventh batch (GFX\\npcs, room units, front = +z,
origin on the floor; the code scales them by RoomScale):
   scp052.b3d     the R4 subway car (after the reference photo): green riveted body, rattan seats, poles,
                  straps, bulbs; the three doors on its -x side are open holes for the sliding leaves
   scp052d.b3d    one door leaf (the code slides six of them)
   scp953f.b3d    a red fox with nine tails                     indev_dog.b3d   a kennel dog
   scp6096.b3d    a small figure under a big cotton sheet, the sheet trailing a metre behind
   scp1269.b3d    a black curbside mailbox on a white post   scp1269f.b3d  its red flag
   scp3325.b3d    an SCP-3325-1 "character" (round head, big eyes)  scp3325j.b3d  its jaw
   indev_shade.b3d  a studio guardian: tall, faceless, black   indev_cart.b3d  the liver delivery cart
   scp482.b3d     a black leather straitjacket on its hanger
The car is drawn full-bright by the code, so its atlas carries its own shading."""
import math
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from b3dkit import Mesh, write_b3d
from make_models4 import sphere

NPCDIR = r"I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9\GFX\npcs"
F = r"C:\Windows\Fonts"
rng = np.random.default_rng(52)


def pf(m, pts, hint, uvs):
    """polygon facing `hint` (flips the winding if needed)"""
    P = [np.asarray(p, dtype=float) for p in pts]
    n = np.zeros(3)
    for i in range(1, len(P) - 1):
        n += np.cross(P[i + 1] - P[0], P[i] - P[0])
    if np.dot(n, hint) < 0:
        P, uvs = P[::-1], list(uvs)[::-1]
    m.poly(P, uvs)


def cen(r, W=1024, H=1024):
    return ((r[0] + r[2]) / 2.0 / W, (r[1] + r[3]) / 2.0 / H)


def rect_uv(r, W=1024, H=1024):
    x0, y0, x1, y1 = r
    return (x0 / W, y0 / H, x1 / W, y1 / H)


def ellipsoid(m, c, rx, ry, rz, uv=(0, 0, 1, 1), seg=10, rings=6):
    cx, cy, cz = c
    u0, v0, u1, v1 = uv

    def P(a, b):
        return (cx + rx * math.cos(a) * math.cos(b), cy + ry * math.sin(a), cz + rz * math.cos(a) * math.sin(b))
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
            mid = np.mean(np.asarray(pts, dtype=float), axis=0) - np.asarray(c, dtype=float)
            pf(m, pts, mid, uvs)


def tail(m, pts, r0, r1, uv, sides=6):
    """a tapering tube along a polyline"""
    n = len(pts) - 1
    for i in range(n):
        ra = r0 + (r1 - r0) * i / n
        rb = r0 + (r1 - r0) * (i + 1) / n
        m.cyl(pts[i], pts[i + 1], ra, rb, sides=sides, uvrect=uv, caps=(i == n - 1))


# ===================================================================== SCP-052
# atlas regions (px in a 1024 x 1024 sheet)
EXT = (0, 0, 256, 384)          # 256 x 384 units of the outside skin (rivet rows, belt line)
INT = (256, 0, 512, 384)        # 256 x 300 units of the inside wall
CEIL = (512, 0, 768, 256)
FLOOR = (768, 0, 1024, 256)
RATTAN = (512, 256, 768, 384)
DEXT = (0, 384, 128, 640)       # a door leaf, outside
DINT = (128, 384, 256, 640)     # a door leaf, inside
POLE = (256, 384, 320, 448)
BLACK = (320, 384, 384, 448)
ROOF = (384, 384, 512, 512)
BULB = (512, 384, 576, 448)
NUM = (576, 384, 832, 512)
SIGNR = (832, 384, 1024, 512)
END = (0, 640, 256, 1024)
ADS = (256, 640, 1024, 704)
STRAP = (256, 448, 320, 512)


def subway_atlas():
    W = H = 1024
    im = Image.new('RGB', (W, H), (40, 40, 40))
    d = ImageDraw.Draw(im)
    green, dkg, rivet = (58, 74, 50), (40, 52, 36), (92, 104, 74)
    # outside skin: panel seams, rows of rivets, a belt rail below the windows
    x0, y0, x1, y1 = EXT
    d.rectangle(EXT, fill=green)
    for yy in (y0 + 10, y0 + 120, y0 + 262, y0 + 372):
        for xx in range(x0 + 6, x1, 14):
            d.ellipse([xx, yy, xx + 4, yy + 4], fill=rivet, outline=dkg)
    d.rectangle([x0, y0 + 250, x1, y0 + 258], fill=(76, 94, 64))
    d.line([(x0, y0 + 258), (x1, y0 + 258)], fill=(30, 38, 26), width=2)
    d.line([(x0 + 2, y0), (x0 + 2, y1)], fill=dkg, width=3)
    # inside wall: cream above, a darker dado below the windows
    x0, y0, x1, y1 = INT
    d.rectangle(INT, fill=(214, 198, 160))
    d.rectangle([x0, y0 + 250, x1, y1], fill=(150, 120, 80))
    d.line([(x0, y0 + 250), (x1, y0 + 250)], fill=(110, 86, 56), width=4)
    # ceiling, floor, rattan
    d.rectangle(CEIL, fill=(226, 214, 180))
    for xx in range(CEIL[0], CEIL[2], 64):
        d.line([(xx, CEIL[1]), (xx, CEIL[3])], fill=(200, 188, 156), width=2)
    d.rectangle(FLOOR, fill=(120, 52, 40))
    for yy in range(FLOOR[1], FLOOR[3], 12):
        d.line([(FLOOR[0], yy), (FLOOR[2], yy)], fill=(96, 40, 30), width=3)
    x0, y0, x1, y1 = RATTAN
    d.rectangle(RATTAN, fill=(206, 170, 90))
    for k in range(x0, x1, 6):
        d.line([(k, y0), (k, y1)], fill=(176, 138, 64), width=2)
    for k in range(y0, y1, 6):
        d.line([(x0, k), (x1, k)], fill=(226, 192, 110), width=1)
    # door leaves: a tall window in each
    for (r, body) in ((DEXT, green), (DINT, (214, 198, 160))):
        x0, y0, x1, y1 = r
        d.rectangle(r, fill=body)
        d.rectangle([x0 + 22, y0 + 30, x1 - 22, y0 + 130], fill=(26, 30, 34), outline=(20, 20, 20), width=4)
        d.line([(x0 + 30, y0 + 40), (x0 + 60, y0 + 120)], fill=(70, 80, 90), width=2)
        d.rectangle([x0, y0, x1 - 1, y1 - 1], outline=(30, 30, 30), width=3)
        d.line([(x1 - 6, y0), (x1 - 6, y1)], fill=(20, 20, 20), width=5)       # the rubber edge
    d.rectangle(POLE, fill=(222, 222, 216))
    d.rectangle(BLACK, fill=(26, 26, 26))
    d.rectangle(ROOF, fill=(60, 62, 60))
    d.rectangle(BULB, fill=(255, 246, 210))
    d.rectangle(STRAP, fill=(232, 228, 214))
    # the number, and the roll sign in the end window
    d.rectangle(NUM, fill=green)
    d.text(((NUM[0] + NUM[2]) // 2, (NUM[1] + NUM[3]) // 2), "100", font=ImageFont.truetype(os.path.join(F, 'arialbd.ttf'), 92), fill=(236, 232, 214), anchor='mm')
    d.rectangle(SIGNR, fill=(12, 12, 12))
    d.ellipse([SIGNR[0] + 10, SIGNR[1] + 20, SIGNR[0] + 90, SIGNR[1] + 100], fill=(236, 236, 230))
    d.text((SIGNR[0] + 50, SIGNR[1] + 60), "A", font=ImageFont.truetype(os.path.join(F, 'arialbd.ttf'), 60), fill=(10, 10, 10), anchor='mm')
    d.text((SIGNR[0] + 140, SIGNR[1] + 44), "8 AV", font=ImageFont.truetype(os.path.join(F, 'arialbd.ttf'), 30), fill=(236, 236, 230), anchor='mm')
    d.text((SIGNR[0] + 140, SIGNR[1] + 84), "EXP", font=ImageFont.truetype(os.path.join(F, 'arialbd.ttf'), 30), fill=(236, 236, 230), anchor='mm')
    # the end of the car: storm door with a window, the route sign window, a headlamp
    x0, y0, x1, y1 = END
    d.rectangle(END, fill=green)
    d.rectangle([x0 + 84, y0 + 70, x1 - 84, y1 - 40], fill=(48, 62, 42), outline=(28, 34, 24), width=4)
    d.rectangle([x0 + 98, y0 + 100, x1 - 98, y0 + 190], fill=(24, 28, 30))
    d.rectangle([x0 + 14, y0 + 100, x0 + 70, y0 + 170], fill=(24, 28, 30))
    d.rectangle([x1 - 70, y0 + 100, x1 - 14, y0 + 170], fill=(236, 236, 230))
    d.text((x1 - 42, y0 + 135), "A", font=ImageFont.truetype(os.path.join(F, 'arialbd.ttf'), 40), fill=(10, 10, 10), anchor='mm')
    d.ellipse([x0 + 30, y0 + 30, x0 + 54, y0 + 54], fill=(255, 240, 200))
    for yy in (y0 + 12, y1 - 20):
        for xx in range(x0 + 6, x1, 14):
            d.ellipse([xx, yy, xx + 4, yy + 4], fill=rivet, outline=dkg)
    # the advertising cards above the windows
    x0, y0, x1, y1 = ADS
    ads = [("FRESHA COLA", (200, 30, 30)), ("SEE YOUR DENTIST", (40, 90, 160)), ("MISS SUBWAYS 1932", (40, 120, 60)),
           ("CONEY ISLAND", (220, 140, 30)), ("BUY BONDS", (40, 40, 120)), ("STAY CLEAR OF DOORS", (20, 20, 20))]
    cw = (x1 - x0) // len(ads)
    for k, (t, c) in enumerate(ads):
        d.rectangle([x0 + k * cw + 2, y0 + 2, x0 + (k + 1) * cw - 3, y1 - 3], fill=(236, 230, 210), outline=(80, 70, 50), width=2)
        d.text((x0 + k * cw + cw // 2, (y0 + y1) // 2), t, font=ImageFont.truetype(os.path.join(F, 'arialbd.ttf'), 13), fill=c, anchor='mm')
    a = np.asarray(im).astype(float)
    n = np.asarray(Image.fromarray((rng.random((H // 4, W // 4)) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(3))).astype(float) / 255
    a *= (0.88 + 0.18 * n)[..., None]
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.5)).save(os.path.join(NPCDIR, 'indev_subway.png'))


def tiled_wall(m, axis, plane, out, a0, a1, y0, y1, region, tw, th, holes=(), ytop_v=None):
    """A wall in the plane `axis` = plane (axis 'x': runs along z), seen from `out` (+1/-1 on that axis),
    covering a0..a1 along its run and y0..y1, with rectangular holes [(c0, c1, hy0, hy1)].
    The atlas region repeats every tw units along the run and th units up (cut at tile edges)."""
    u0, v0, u1, v1 = rect_uv(region)
    cuts_s = sorted({a0, a1} | {h[0] for h in holes} | {h[1] for h in holes})
    cuts_y = sorted({y0, y1} | {h[2] for h in holes} | {h[3] for h in holes})

    def inside_hole(s, y):
        return any(h[0] <= s <= h[1] and h[2] <= y <= h[3] for h in holes)
    for i in range(len(cuts_s) - 1):
        for j in range(len(cuts_y) - 1):
            sa, sb, ya, yb = cuts_s[i], cuts_s[i + 1], cuts_y[j], cuts_y[j + 1]
            if sb - sa < 0.01 or yb - ya < 0.01 or inside_hole((sa + sb) / 2, (ya + yb) / 2):
                continue
            # split at tile edges
            ss = [sa] + [k * tw for k in range(int(math.floor(sa / tw)) + 1, int(math.ceil(sb / tw)))] + [sb]
            ys = [ya] + [k * th for k in range(int(math.floor(ya / th)) + 1, int(math.ceil(yb / th)))] + [yb]
            for p in range(len(ss) - 1):
                for q in range(len(ys) - 1):
                    s0, s1, t0, t1 = ss[p], ss[p + 1], ys[q], ys[q + 1]
                    if s1 - s0 < 0.01 or t1 - t0 < 0.01:
                        continue
                    base_s = math.floor((s0 + s1) / 2 / tw) * tw
                    base_t = math.floor((t0 + t1) / 2 / th) * th
                    fu0, fu1 = (s0 - base_s) / tw, (s1 - base_s) / tw
                    fv0, fv1 = (t0 - base_t) / th, (t1 - base_t) / th
                    U0, U1 = u0 + (u1 - u0) * fu0, u0 + (u1 - u0) * fu1
                    V0, V1 = v1 - (v1 - v0) * fv0, v1 - (v1 - v0) * fv1      # v runs down the image
                    if axis == 'x':
                        P = [(plane, t0, s0), (plane, t0, s1), (plane, t1, s1), (plane, t1, s0)]
                        hint = (out, 0, 0)
                    else:
                        P = [(s0, t0, plane), (s1, t0, plane), (s1, t1, plane), (s0, t1, plane)]
                        hint = (0, 0, out)
                    pf(m, P, hint, [(U0, V0), (U1, V0), (U1, V1), (U0, V1)])


def flat_rect(m, x0, z0, x1, z1, y, up, region, tw, tz):
    """a horizontal rectangle (floor if up > 0, ceiling otherwise), region tiled every tw x tz units"""
    u0, v0, u1, v1 = rect_uv(region)
    xs = [x0] + [k * tw for k in range(int(math.floor(x0 / tw)) + 1, int(math.ceil(x1 / tw)))] + [x1]
    zs = [z0] + [k * tz for k in range(int(math.floor(z0 / tz)) + 1, int(math.ceil(z1 / tz)))] + [z1]
    for i in range(len(xs) - 1):
        for j in range(len(zs) - 1):
            a, b, c, e = xs[i], xs[i + 1], zs[j], zs[j + 1]
            bx = math.floor((a + b) / 2 / tw) * tw
            bz = math.floor((c + e) / 2 / tz) * tz
            U0, U1 = u0 + (u1 - u0) * (a - bx) / tw, u0 + (u1 - u0) * (b - bx) / tw
            V0, V1 = v0 + (v1 - v0) * (c - bz) / tz, v0 + (v1 - v0) * (e - bz) / tz
            pf(m, [(a, y, c), (b, y, c), (b, y, e), (a, y, e)], (0, up, 0), [(U0, V0), (U1, V0), (U1, V1), (U0, V1)])


def box_r(m, x0, y0, z0, x1, y1, z1, region, skip=''):
    """an axis-aligned box with one region stretched over each face"""
    uv = rect_uv(region)
    u0, v0, u1, v1 = uv
    faces = {'S': ([(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0)], (0, 0, -1)),
             'N': ([(x1, y0, z1), (x0, y0, z1), (x0, y1, z1), (x1, y1, z1)], (0, 0, 1)),
             'E': ([(x1, y0, z0), (x1, y0, z1), (x1, y1, z1), (x1, y1, z0)], (1, 0, 0)),
             'W': ([(x0, y0, z1), (x0, y0, z0), (x0, y1, z0), (x0, y1, z1)], (-1, 0, 0)),
             'T': ([(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)], (0, 1, 0)),
             'B': ([(x0, y0, z1), (x1, y0, z1), (x1, y0, z0), (x0, y0, z0)], (0, -1, 0))}
    for k, (pts, hint) in faces.items():
        if k in skip:
            continue
        pf(m, pts, hint, [(u0, v1), (u1, v1), (u1, v0), (u0, v0)])


DOORS = (-560.0, 0.0, 560.0)
DHW = 85.0                       # half width of a door opening
DH = 256.0                       # door height
WX, WI = 200.0, 185.0            # outside skin, inside skin (half widths)
LX, LI = 820.0, 805.0            # outside / inside half lengths
WINY = (130.0, 250.0)


def windows():
    """window openings along one side (z ranges)"""
    out = []
    for (a, b) in ((-LI, -560 - DHW), (-560 + DHW, -DHW), (DHW, 560 - DHW), (560 + DHW, LI)):
        L = b - a
        if L < 250:
            continue            # the end bays carry the number instead
        n = 3
        w = (L - 40) / n - 24
        for k in range(n):
            c = a + 20 + (k + 0.5) * (L - 40) / n
            out.append((c - w / 2, c + w / 2))
    return out


def subway_car():
    m = Mesh()
    wins = windows()
    for side in (-1, 1):
        holes = [(c0, c1, WINY[0], WINY[1]) for (c0, c1) in wins]
        dholes = [(dz - DHW, dz + DHW, 0.0, DH) for dz in DOORS]
        # outside skin (the -x side has real door openings; the +x side shows shut doors)
        tiled_wall(m, 'x', side * WX, side, -LX, LX, -30.0, 330.0, EXT, 256.0, 384.0, holes + dholes)
        tiled_wall(m, 'x', side * WI, -side, -LI, LI, 0.0, 300.0, INT, 256.0, 300.0, holes + dholes)
        for (c0, c1) in wins:     # window reveals
            for (y, h) in ((WINY[0], (0, 1, 0)), (WINY[1], (0, -1, 0))):
                pf(m, [(side * WI, y, c0), (side * WX, y, c0), (side * WX, y, c1), (side * WI, y, c1)], h, [cen(BLACK)] * 4)
            for (z, h) in ((c0, (0, 0, 1)), (c1, (0, 0, -1))):
                pf(m, [(side * WI, WINY[0], z), (side * WX, WINY[0], z), (side * WX, WINY[1], z), (side * WI, WINY[1], z)], h, [cen(BLACK)] * 4)
        for dz in DOORS:
            if side < 0:
                # the doorway: jambs, lintel and a threshold plate
                for (z, h) in ((dz - DHW, (0, 0, 1)), (dz + DHW, (0, 0, -1))):
                    pf(m, [(side * WI, 0, z), (side * WX, 0, z), (side * WX, DH, z), (side * WI, DH, z)], h, [cen(BLACK)] * 4)
                pf(m, [(side * WI, DH, dz - DHW), (side * WX, DH, dz - DHW), (side * WX, DH, dz + DHW), (side * WI, DH, dz + DHW)], (0, -1, 0), [cen(POLE)] * 4)
                box_r(m, side * WX, -4, dz - DHW, side * WI, 0, dz + DHW, POLE, skip='B')
            else:
                # shut leaves on the far side, both faces
                for (lo, hi) in ((dz - DHW, dz), (dz, dz + DHW)):
                    box_r(m, side * WX, 0, lo, side * WI, DH, hi, BLACK, skip='EW')
                    u0, v0, u1, v1 = rect_uv(DEXT)
                    pf(m, [(WX, 0, lo), (WX, 0, hi), (WX, DH, hi), (WX, DH, lo)], (1, 0, 0), [(u0, v1), (u1, v1), (u1, v0), (u0, v0)])
                    u0, v0, u1, v1 = rect_uv(DINT)
                    pf(m, [(WI, 0, hi), (WI, 0, lo), (WI, DH, lo), (WI, DH, hi)], (-1, 0, 0), [(u0, v1), (u1, v1), (u1, v0), (u0, v0)])
        # the number on both end bays
        u0, v0, u1, v1 = rect_uv(NUM)
        for zc in (-LX + 85, LX - 85):
            z0, z1 = zc - 60, zc + 60
            off = side * (WX + 0.8)
            if side < 0:
                pf(m, [(off, 150, z1), (off, 150, z0), (off, 230, z0), (off, 230, z1)], (-1, 0, 0), [(u0, v1), (u1, v1), (u1, v0), (u0, v0)])
            else:
                pf(m, [(off, 150, z0), (off, 150, z1), (off, 230, z1), (off, 230, z0)], (1, 0, 0), [(u0, v1), (u1, v1), (u1, v0), (u0, v0)])
        # advertising cards above the windows, inside
        u0, v0, u1, v1 = rect_uv(ADS)
        off = side * (WI - 0.8)
        for (a, b) in ((-LI + 20, -560 - DHW - 10), (-560 + DHW + 10, -DHW - 10), (DHW + 10, 560 - DHW - 10), (560 + DHW + 10, LI - 20)):
            if side < 0:
                pf(m, [(off, 258, a), (off, 258, b), (off, 296, b), (off, 296, a)], (1, 0, 0), [(u0, v1), (u1, v1), (u1, v0), (u0, v0)])
            else:
                pf(m, [(off, 258, b), (off, 258, a), (off, 296, a), (off, 296, b)], (-1, 0, 0), [(u0, v1), (u1, v1), (u1, v0), (u0, v0)])
    # ends
    u0, v0, u1, v1 = rect_uv(END)
    for s in (-1, 1):
        z = s * LX
        P = [(-WX, -30, z), (WX, -30, z), (WX, 330, z), (-WX, 330, z)]
        pf(m, P if s > 0 else P, (0, 0, s), [(u0, v1), (u1, v1), (u1, v0), (u0, v0)] if s < 0 else [(u1, v1), (u0, v1), (u0, v0), (u1, v0)])
        tiled_wall(m, 'z', s * LI, -s, -WI, WI, 0.0, 300.0, INT, 256.0, 300.0, [(-50.0, 50.0, 0.0, 250.0)])
        u0d, v0d, u1d, v1d = rect_uv(DINT)
        pf(m, [(50, 0, s * LI), (-50, 0, s * LI), (-50, 250, s * LI), (50, 250, s * LI)], (0, 0, -s), [(u0d, v1d), (u1d, v1d), (u1d, v0d), (u0d, v0d)])
        # side-to-skin returns at the ends (between the skins)
        pf(m, [(-WX, -30, z), (-WI, -30, z), (-WI, 330, z), (-WX, 330, z)], (0, 0, s), [cen(BLACK)] * 4)
        pf(m, [(WI, -30, z), (WX, -30, z), (WX, 330, z), (WI, 330, z)], (0, 0, s), [cen(BLACK)] * 4)
        prof = [(-WX, 330), (-120, 362), (-120, 392), (120, 392), (120, 362), (WX, 330)]
        r0 = rect_uv(ROOF)
        pf(m, [(x, y, z) for (x, y) in prof], (0, 0, s), [cen(ROOF)] * 6)
    # roof
    for s in (-1, 1):
        pf(m, [(s * WX, 330, -LX), (s * WX, 330, LX), (s * 120, 362, LX), (s * 120, 362, -LX)], (s, 1.5, 0), [(0.375, 0.375), (0.5, 0.375), (0.5, 0.5), (0.375, 0.5)])
        pf(m, [(s * 120, 362, -LX), (s * 120, 362, LX), (s * 120, 392, LX), (s * 120, 392, -LX)], (s, 0, 0), [(0.375, 0.375), (0.5, 0.375), (0.5, 0.5), (0.375, 0.5)])
    pf(m, [(-120, 392, -LX), (120, 392, -LX), (120, 392, LX), (-120, 392, LX)], (0, 1, 0), [(0.375, 0.375), (0.5, 0.375), (0.5, 0.5), (0.375, 0.5)])
    # between the skins along the top and bottom edges
    for s in (-1, 1):
        pf(m, [(s * WI, 300, -LX), (s * WX, 300, -LX), (s * WX, 300, LX), (s * WI, 300, LX)], (0, -1, 0), [cen(BLACK)] * 4)
    # floor, ceiling, underframe, trucks and wheels
    flat_rect(m, -WI, -LI, WI, LI, 0.0, 1, FLOOR, 256.0, 256.0)
    flat_rect(m, -WI, -LI, WI, LI, 300.0, -1, CEIL, 256.0, 256.0)
    box_r(m, -170, -40, -780, 170, -2, 780, BLACK, skip='T')
    for zt in (-560.0, 560.0):
        box_r(m, -150, -92, zt - 90, 150, -40, zt + 90, BLACK)
        for zw in (zt - 56, zt + 56):
            for s in (-1, 1):
                m.cyl((s * 92, -72, zw), (s * 112, -72, zw), 38, sides=12, uvrect=rect_uv(BLACK))
    # seats along both walls in the bays, rattan
    for (a, b) in ((-LI, -560 - DHW), (-560 + DHW, -DHW), (DHW, 560 - DHW), (560 + DHW, LI)):
        for s in (-1, 1):
            xa, xb = sorted((s * WI, s * (WI - 62)))
            box_r(m, xa, 0, a + 12, xb, 44, b - 12, RATTAN, skip='B')
            xa, xb = sorted((s * WI, s * (WI - 12)))
            box_r(m, xa, 44, a + 12, xb, 118, b - 12, RATTAN, skip='B')
    # poles at the doors, rails overhead, straps, bulbs
    for dz in DOORS:
        for s in (-1, 1):
            for zz in (dz - DHW - 16, dz + DHW + 16):
                m.cyl((s * 150, 0, zz), (s * 150, 300, zz), 4, sides=6, uvrect=rect_uv(POLE), caps=False)
    for s in (-1, 1):
        m.cyl((s * 112, 252, -LI), (s * 112, 252, LI), 3.5, sides=6, uvrect=rect_uv(POLE), caps=False)
        for k in range(-11, 12):
            z = k * 70.0
            if any(abs(z - dz) < DHW + 10 for dz in DOORS):
                continue
            box_r(m, s * 112 - 2, 206, z - 5, s * 112 + 2, 250, z + 5, STRAP)
            box_r(m, s * 112 - 7, 200, z - 1.5, s * 112 + 7, 214, z + 1.5, STRAP)
        for zz in (-LI, LI):
            m.cyl((s * 112, 252, zz), (s * 112, 300, zz), 3, sides=6, uvrect=rect_uv(POLE), caps=False)
    for k in range(-5, 6):
        sphere(m, (0, 292, k * 150.0), 7, sy=0.7, seg=8, rings=4, uv=rect_uv(BULB))
    return m


def door_leaf():
    m = Mesh()
    box_r(m, -4, 0, -42.5, 4, DH, 42.5, BLACK, skip='EW')
    u0, v0, u1, v1 = rect_uv(DEXT)
    pf(m, [(-4, 0, 42.5), (-4, 0, -42.5), (-4, DH, -42.5), (-4, DH, 42.5)], (-1, 0, 0), [(u0, v1), (u1, v1), (u1, v0), (u0, v0)])
    u0, v0, u1, v1 = rect_uv(DINT)
    pf(m, [(4, 0, -42.5), (4, 0, 42.5), (4, DH, 42.5), (4, DH, -42.5)], (1, 0, 0), [(u0, v1), (u1, v1), (u1, v0), (u0, v0)])
    return m


# ===================================================================== tone sheets for the creatures
def tones(name, cols, seed, size=(256, 64), fur=0.0):
    """vertical bands of colour; band k is the uv rect (k/n, 0.05, (k+1)/n, 0.95)"""
    W, H = size
    n = len(cols)
    a = np.zeros((H, W, 3))
    for k, c in enumerate(cols):
        a[:, k * W // n:(k + 1) * W // n] = c
    r = np.random.default_rng(seed)
    a += r.normal(0, 8 + fur * 20, (H, W, 1))
    if fur:
        streak = np.asarray(Image.fromarray((r.random((H, W)) * 255).astype(np.uint8)).filter(ImageFilter.BoxBlur(1))).astype(float) / 255
        a *= (0.8 + 0.35 * streak)[..., None]
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(os.path.join(NPCDIR, name))


def band(k, n):
    return (k / n + 0.01, 0.05, (k + 1) / n - 0.01, 0.95)


def fox():
    m = Mesh()
    O, Wt, Bk = band(0, 3), band(1, 3), band(2, 3)
    ellipsoid(m, (0, 62, 0), 24, 22, 50, O)
    ellipsoid(m, (0, 56, 30), 16, 18, 20, Wt)               # chest
    ellipsoid(m, (0, 84, 54), 16, 15, 18, O)                # head
    m.cyl((0, 80, 66), (0, 76, 92), 9, 2.5, sides=8, uvrect=O)   # snout
    sphere(m, (0, 76, 93), 2.5, seg=6, rings=4, uv=Bk)
    for s in (-1, 1):
        pf(m, [(s * 6, 96, 50), (s * 15, 96, 54), (s * 12, 120, 50)], (0, 0, 1), [(O[0], O[3]), (O[2], O[3]), (O[0], O[1])])
        pf(m, [(s * 6, 96, 50), (s * 15, 96, 54), (s * 12, 120, 50)], (0, 0, -1), [(Bk[0], Bk[3]), (Bk[2], Bk[3]), (Bk[0], Bk[1])])
        sphere(m, (s * 6, 88, 69), 2.2, seg=6, rings=4, uv=(0.36, 0.2, 0.38, 0.22))
        for z in (-30, 30):
            m.cyl((s * 12, 0, z), (s * 14, 50, z * 0.9), 4.5, 6, sides=6, uvrect=Bk)
    # nine tails, fanned up and back
    for k in range(9):
        a = math.radians(-64 + 16 * k)
        pts = []
        for j in range(6):
            t = j / 5.0
            pts.append((math.sin(a) * (10 + 70 * t), 64 + 70 * t - 30 * t * t + 10 * math.cos(a), -46 - 40 * t))
        tail(m, pts, 7.5, 3.5, O, sides=6)
        sphere(m, pts[-1], 4.5, seg=6, rings=4, uv=Wt)
    return m


def dog():
    m = Mesh()
    C, Wt, Bk = band(0, 3), band(1, 3), band(2, 3)
    ellipsoid(m, (0, 52, 0), 18, 17, 42, C)
    ellipsoid(m, (0, 50, 26), 14, 15, 16, Wt)
    ellipsoid(m, (0, 78, 46), 13, 12, 14, C)
    m.cyl((0, 74, 56), (0, 70, 76), 7.5, 4.5, sides=8, uvrect=Wt)
    sphere(m, (0, 70, 77), 3, seg=6, rings=4, uv=Bk)
    for s in (-1, 1):
        pf(m, [(s * 4, 88, 42), (s * 12, 88, 46), (s * 9, 104, 42)], (0, 0, 1), [(C[0], C[3]), (C[2], C[3]), (C[0], C[1])])
        pf(m, [(s * 4, 88, 42), (s * 12, 88, 46), (s * 9, 104, 42)], (0, 0, -1), [(C[0], C[3]), (C[2], C[3]), (C[0], C[1])])
        sphere(m, (s * 5, 82, 57), 2, seg=6, rings=4, uv=Bk)
        for z in (-26, 26):
            m.cyl((s * 10, 0, z), (s * 11, 44, z * 0.9), 4, 5.5, sides=6, uvrect=C)
    tail(m, [(0, 60, -40), (0, 76, -50), (0, 88, -44), (0, 86, -34)], 5, 3, C)
    return m


def sheet6096():
    """a figure 1.55 m tall under a sheet, the sheet spreading and trailing a metre behind"""
    m = Mesh()
    U = (0.02, 0.02, 0.98, 0.98)
    seg, prof = 16, [(0, 0.0), (8, 26.0), (26, 34.0), (60, 38.0), (110, 44.0), (150, 50.0), (182, 58.0), (200, 66.0), (210, 76.0)]
    # rings from the top down: (height, radius) reversed so the hem is last
    rings = [(210 - h, r) for (h, r) in prof]
    rings = sorted(rings, key=lambda p: -p[0])

    def P(y, r, i):
        a = 2 * math.pi * i / seg
        wob = 1 + 0.10 * math.sin(a * 7 + y * 0.03) * min(1.0, (210 - y) / 80)
        back = 1.35 if math.cos(a) < -0.3 and y < 40 else 1.0
        return (r * wob * math.sin(a), y, r * wob * math.cos(a) * back)
    for j in range(len(rings) - 1):
        (ya, ra), (yb, rb) = rings[j], rings[j + 1]
        for i in range(seg):
            pts = [P(yb, rb, i), P(yb, rb, i + 1), P(ya, ra, i + 1), P(ya, ra, i)]
            v_a, v_b = j / (len(rings) - 1), (j + 1) / (len(rings) - 1)
            uvs = [(i / seg, v_b), ((i + 1) / seg, v_b), ((i + 1) / seg, v_a), (i / seg, v_a)]
            mid = np.mean(np.asarray(pts), axis=0) - np.array([0, (ya + yb) / 2, 0])
            if ra < 0.5:
                pts, uvs = pts[:3], uvs[:3]
            pf(m, pts, mid, uvs)
    # the train of the sheet, lying on the floor behind
    for k in range(8):
        z0, z1 = -60 - k * 17, -60 - (k + 1) * 17
        w0, w1 = 70 - k * 4, 70 - (k + 1) * 4
        y0, y1 = 2 + 2 * math.sin(k), 2 + 2 * math.sin(k + 1)
        pf(m, [(-w0, y0, z0), (w0, y0, z0), (w1, y1, z1), (-w1, y1, z1)], (0, 1, 0), [(0.1, k / 8), (0.9, k / 8), (0.9, (k + 1) / 8), (0.1, (k + 1) / 8)])
    return m


def sheet_tex():
    W = H = 256
    a = np.zeros((H, W, 3)) + 228
    x = np.arange(W)[None, :]
    folds = 0.82 + 0.18 * np.sin(x / W * 2 * np.pi * 7 + np.sin(np.arange(H)[:, None] / 40.0))
    a *= folds[..., None]
    a[..., 2] += 4
    r = np.random.default_rng(6096)
    a += r.normal(0, 4, (H, W, 1))
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.0)).save(os.path.join(NPCDIR, 'indev_sheet.png'))


def mailbox():
    m = Mesh()
    Bl, Wt, Rd = band(0, 3), band(1, 3), band(2, 3)
    m.box((0, 70, 0), 7, 70, 7, uvrect=Wt)                     # the post
    m.box((0, 141, -6), 13, 3, 40, uvrect=Wt)                  # the board it sits on
    m.box((0, 154, 0), 12, 10, 34, uvrect=Bl)                  # the box
    m.cyl((0, 164, -34), (0, 164, 34), 12, sides=10, uvrect=Bl)   # rounded top
    m.box((0, 160, 35), 11, 12, 1.5, uvrect=Bl)                # the door
    m.box((0, 164, 37.5), 2, 4, 1.5, uvrect=Wt)               # its latch
    return m


def mailbox_flag():
    m = Mesh()
    Rd = band(2, 3)
    m.box((0, 0, 9), 1, 2, 9, uvrect=Rd)       # the arm (pivot at the hinge, pointing +z when down)
    m.box((0, 0, 20), 1, 6, 4, uvrect=Rd)      # the flag
    return m


def puppet():
    """SCP-3325-1b: a round orange head with a wide mouth (the jaw is a separate model), big eyes"""
    m = Mesh()
    Fur, Eye, Pup, Mouth = band(0, 5), band(1, 5), band(2, 5), band(3, 5)
    ellipsoid(m, (0, 70, 0), 30, 42, 24, Fur, seg=12, rings=8)          # body
    ellipsoid(m, (0, 150, 4), 46, 40, 42, Fur, seg=14, rings=8)         # head
    for s in (-1, 1):
        ellipsoid(m, (s * 18, 172, 36), 14, 16, 10, Eye, seg=10, rings=6)
        ellipsoid(m, (s * 17, 170, 45), 6, 7, 3, Pup, seg=8, rings=4)
        m.cyl((s * 26, 104, 4), (s * 52, 70, 14), 9, 7, sides=8, uvrect=Fur)       # arms
        sphere(m, (s * 54, 66, 16), 10, seg=8, rings=4, uv=Fur)                  # hands
        m.cyl((s * 14, 34, 0), (s * 16, 0, 6), 11, 12, sides=8, uvrect=Fur)       # legs
        ellipsoid(m, (s * 16, 4, 14), 12, 6, 16, Pup, seg=8, rings=4)            # feet
        sphere(m, (s * 30, 186, -4), 12, seg=8, rings=4, uv=Fur)                 # ear tufts
    ellipsoid(m, (0, 156, 44), 8, 7, 7, Mouth, seg=8, rings=4)                    # nose
    ellipsoid(m, (0, 136, 30), 34, 8, 14, Mouth, seg=12, rings=4)                 # the upper lip / mouth roof
    return m


def puppet_jaw():
    m = Mesh()
    Fur, Mouth, Teeth = band(0, 5), band(3, 5), band(4, 5)
    ellipsoid(m, (0, -10, 18), 32, 12, 22, Fur, seg=12, rings=6)
    ellipsoid(m, (0, -2, 20), 26, 5, 16, Mouth, seg=10, rings=4)
    for k in range(-3, 4):
        m.box((k * 7, 3, 32 - abs(k) * 2), 2.2, 3.5, 1.5, uvrect=Teeth)
    return m


def shade():
    m = Mesh()
    Bk, Dk = band(0, 2), band(1, 2)
    m.cyl((0, 0, 0), (0, 230, 0), 52, 30, sides=12, uvrect=Bk)
    ellipsoid(m, (0, 262, 0), 24, 32, 24, Dk, seg=10, rings=6)
    for s in (-1, 1):
        m.cyl((s * 32, 220, 0), (s * 46, 90, 20), 9, 6, sides=6, uvrect=Bk)
    return m


def cart():
    m = Mesh()
    G, Am, Rd = band(0, 3), band(1, 3), band(2, 3)
    m.box((0, 34, 0), 26, 22, 38, uvrect=G)
    for (x, z) in ((-22, -30), (22, -30), (-22, 30), (22, 30)):
        m.cyl((x - 3, 8, z), (x + 3, 8, z), 8, sides=8, uvrect=G)
    m.box((0, 58, 0), 22, 2, 30, uvrect=G)
    ellipsoid(m, (0, 64, 0), 14, 7, 12, Rd, seg=8, rings=4)                # the liver, 1.5 kg of it
    m.cyl((0, 56, 34), (0, 76, 34), 2, sides=6, uvrect=G)
    sphere(m, (0, 80, 34), 4, seg=6, rings=4, uv=Am)
    return m


def jacket():
    """SCP-482 on its hanger: a black leather torso, sleeves crossed and strapped behind"""
    m = Mesh()
    L, S, Mt = band(0, 3), band(1, 3), band(2, 3)
    m.cyl((0, 210, 0), (0, 234, 0), 1.5, sides=6, uvrect=Mt)
    m.cyl((-30, 204, 0), (30, 204, 0), 2.5, sides=6, uvrect=Mt)                  # the hanger bar
    m.cyl((0, 120, 0), (0, 200, 0), 30, 34, sides=10, uvrect=L)                  # torso
    ellipsoid(m, (0, 202, 0), 34, 8, 16, L, seg=10, rings=4)
    m.cyl((0, 200, 0), (0, 214, 0), 12, 10, sides=8, uvrect=L)                   # collar
    for s in (-1, 1):                                                            # sleeves, crossed in front
        m.cyl((s * 30, 192, 2), (s * 12, 150, 26), 9, 8, sides=8, uvrect=L)
        m.cyl((s * 12, 150, 26), (-s * 26, 138, 24), 8, 7, sides=8, uvrect=L)
    for y in (132, 160, 186):                                                    # straps and buckles
        m.cyl((0, y - 3, 0), (0, y + 3, 0), 33, sides=12, uvrect=S, caps=False)
        m.box((0, y, 34), 3, 3, 1.5, uvrect=Mt)
    return m


def write_all():
    subway_atlas()
    tones('indev_fox.png', [(196, 78, 30), (236, 226, 210), (34, 26, 22)], 953, fur=0.6)
    tones('indev_jindo.png', [(226, 210, 176), (242, 238, 228), (40, 34, 30)], 31, fur=0.5)
    tones('indev_hound.png', [(170, 104, 48), (238, 234, 224), (30, 26, 24)], 32, fur=0.5)
    tones('indev_mailbox.png', [(22, 22, 24), (230, 230, 226), (196, 26, 22)], 1269)
    tones('indev_puppet.png', [(236, 120, 30), (250, 250, 246), (16, 16, 18), (170, 26, 40), (246, 244, 236)], 3325, fur=0.8)
    tones('indev_puppet2.png', [(150, 170, 100), (210, 214, 196), (40, 40, 36), (140, 70, 70), (220, 214, 196)], 3326, fur=0.8)
    tones('indev_shade.png', [(6, 6, 8), (16, 14, 18)], 24)
    tones('indev_cart.png', [(140, 144, 150), (255, 170, 40), (120, 20, 26)], 953)
    tones('indev_leather.png', [(20, 18, 18), (40, 36, 32), (150, 150, 150)], 482)
    sheet_tex()
    out = [('scp052.b3d', 'indev_subway.png', subway_car()), ('scp052d.b3d', 'indev_subway.png', door_leaf()),
           ('scp953f.b3d', 'indev_fox.png', fox()), ('indev_dog.b3d', 'indev_jindo.png', dog()),
           ('scp6096.b3d', 'indev_sheet.png', sheet6096()), ('scp1269.b3d', 'indev_mailbox.png', mailbox()),
           ('scp1269f.b3d', 'indev_mailbox.png', mailbox_flag()), ('scp3325.b3d', 'indev_puppet.png', puppet()),
           ('scp3325j.b3d', 'indev_puppet.png', puppet_jaw()), ('indev_shade.b3d', 'indev_shade.png', shade()),
           ('indev_cart.b3d', 'indev_cart.png', cart()), ('scp482.b3d', 'indev_leather.png', jacket())]
    for fn, tex, mesh in out:
        nv, nt = write_b3d(os.path.join(NPCDIR, fn), tex, mesh, name=fn.split('.')[0])
        print('%-16s %5d verts %5d tris' % (fn, nv, nt))
    return out


if __name__ == '__main__':
    write_all()
