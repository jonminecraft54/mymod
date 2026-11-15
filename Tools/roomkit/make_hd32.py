r"""High-detail models for batch 32, Gate V (original work):
  GFX\map\props\gatev_hatch.b3d   the exit's round vault hatch, swung open: a 30 cm thick steel disc with a stepped
                                  rim, 16 locking bolts, a central hub and a three-spoke wheel, two massive hinge arms
                                  and their knuckles, scuffed yellow-black hazard paint round the edge
  GFX\map\props\gatev_mtf.b3d     a Nine-Tailed Fox operative as the player sees them against the light: helmet with
                                  goggles, gas mask, plate carrier with pouches, gloves, boots, a rifle at the ready -
                                  dark, almost a silhouette
   python make_hd32.py"""
import math
import os
import random
from PIL import Image, ImageDraw, ImageFilter
from make_hd29 import Model, grid, tube, lathe, card, nrm, cross, sub, add, render, PROPS, PREV
from make_hd30 import blob, quad, xform, rot, noise_tex

RND = random.Random(320)


def save(im, name):
    im.save(os.path.join(PROPS, name))


def hatch():
    st = noise_tex(256, (112, 116, 120), 9, 0.6, 3201)
    d = ImageDraw.Draw(st)
    for _ in range(80):
        x, y = RND.randrange(256), RND.randrange(256)
        d.line([(x, y), (x + RND.randint(-30, 30), y + RND.randint(-3, 3))], fill=(150, 154, 158), width=1)
    save(st, 'gatev_steel.png')
    hz = Image.new('RGB', (256, 64), (220, 180, 30))
    d = ImageDraw.Draw(hz)
    for x in range(-64, 256, 32):
        d.polygon([(x, 64), (x + 16, 64), (x + 48, 0), (x + 32, 0)], fill=(24, 24, 24))
    save(hz.filter(ImageFilter.GaussianBlur(0.6)), 'gatev_hazard.png')
    save(noise_tex(64, (60, 62, 66), 8, 0.6, 3202), 'gatev_dark.png')
    M = Model()
    s = M.surf('steel', 'gatev_steel.png', shine=0.6)
    hz_ = M.surf('hazard', 'gatev_hazard.png', shine=0.4)
    dk = M.surf('dark', 'gatev_dark.png', shine=0.5)
    R0 = 170.0
    # the disc: lathe round y, then laid on its side (face towards -z when shut); built shut, swung open below
    lathe(s, [(0, 0), (R0 - 30, 0), (R0 - 26, 6), (R0 - 26, 22), (R0 - 20, 26)], 48, lambda i: i / 4.0)
    lathe(hz_, [(R0 - 20, 26), (R0, 30), (R0, 48)], 48, lambda i: i / 2.0)
    lathe(s, [(R0, 48), (R0 - 8, 52), (R0 - 40, 52), (0, 52)], 48, lambda i: i / 3.0)
    lathe(dk, [(36, -2), (40, -14), (30, -22), (0, -24)], 24, lambda i: i / 3.0)               # the hub
    for k in range(3):                                                                       # the wheel
        a = math.radians(k * 120)
        tube(dk, [(0, -20, 0), (100 * math.cos(a), -40, 100 * math.sin(a))], lambda i: 6, 8)
    ring = [(100 * math.cos(2 * math.pi * j / 32), -40, 100 * math.sin(2 * math.pi * j / 32)) for j in range(33)]
    tube(dk, ring, lambda i: 7, 8, vrep=0.02)
    for k in range(16):                                                                      # locking bolts
        a = 2 * math.pi * k / 16
        c = ((R0 + 6) * math.cos(a), 38, (R0 + 6) * math.sin(a))
        tube(s, [c, add(c, (math.cos(a) * 26, 0, math.sin(a) * 26))], lambda i: 8, 8)
    for z in (-60, 60):                                                                      # hinge arms
        blob(s, (R0 + 40, 26, z), (44, 14, 18), e=0.45, rings=6, segs=12)
        tube(dk, [(R0 + 80, 26, z - 26), (R0 + 80, 26, z + 26)], lambda i: 18, 12)
    # stand it up: disc axis from +y to +z, then swing it open 105 degrees round the hinge line
    hinge = (R0 + 80, 0, 0)
    for surf in (s, hz_, dk):
        xform(surf, 0, rot('x', -90))
        xform(surf, 0, rot('y', -105, (R0 + 80, 0, 0)))
    return M


def mtf():
    save(noise_tex(128, (34, 36, 34), 8, 0.8, 3203), 'gatev_kit.png')
    save(noise_tex(64, (20, 20, 22), 6, 0.6, 3204), 'gatev_black.png')
    save(Image.new('RGB', (32, 32), (90, 110, 90)), 'gatev_lens.png')
    M = Model()
    k = M.surf('kit', 'gatev_kit.png', shine=0.2)
    b = M.surf('black', 'gatev_black.png', shine=0.4)
    l = M.surf('lens', 'gatev_lens.png', shine=1.0)
    # room units, about 290 tall, standing, rifle at the low ready, facing -z
    for e in (-1, 1):
        tube(k, [(e * 16, 20, 2), (e * 17, 80, 0), (e * 15, 140, -4)], lambda i: (10, 11, 13)[i], 10)       # legs
        blob(k, (e * 16, 85, -9), (10, 9, 9), rings=6, segs=10)                                            # knee pads
        blob(b, (e * 16, 10, -6), (11, 10, 18), e=0.7, rings=6, segs=10)                                   # boots
    blob(k, (0, 152, 0), (26, 16, 16), rings=8, segs=14)                                                   # hips
    blob(k, (0, 200, 0), (30, 42, 18), e=0.8, rings=10, segs=16)                                           # torso
    blob(b, (0, 205, -6), (32, 38, 18), e=0.45, rings=8, segs=14)                                          # plate carrier
    for x in (-18, 0, 18):
        blob(k, (x, 180, -22), (8, 10, 5), e=0.5, rings=4, segs=8)                                          # pouches
    tube(k, [(0, 240, 0), (0, 252, 0)], lambda i: 9, 10)                                                    # neck
    blob(b, (0, 270, 0), (17, 20, 18), rings=10, segs=14)                                                  # helmet
    blob(b, (0, 262, -12), (12, 10, 8), rings=8, segs=10)                                                  # gas mask
    for e in (-1, 1):
        blob(l, (e * 7, 270, -17), (5, 4, 2), rings=5, segs=8)                                             # goggles
        tube(k, [(e * 34, 236, 0), (e * 38, 200, -12), (e * 18 if e < 0 else e * 14, 190, -36)], lambda i: (8, 7, 6)[i], 9)  # arms
        blob(b, (e * 16 if e < 0 else e * 12, 190, -38), (6, 6, 6), rings=5, segs=8)                       # gloves
    tube(b, [(-4, 196, -20), (4, 186, -80)], lambda i: 5, 8)                                               # the rifle
    blob(b, (0, 184, -40), (5, 12, 6), e=0.5, rings=4, segs=8)                                              # magazine
    tube(b, [(4, 186, -80), (6, 184, -110)], lambda i: 2, 6)                                               # barrel
    return M


if __name__ == '__main__':
    out = {}
    for name, fn in (('gatev_hatch', hatch), ('gatev_mtf', mtf)):
        m = fn()
        m.write(os.path.join(PROPS, name + '.b3d'))
        out[name] = m
        print('%-12s %6d triangles' % (name, m.tris()))
    a = render(out['gatev_hatch'], PROPS, (-240, 200, -420), (180, 120, -60), size=(500, 500), fov=55, bg=(40, 40, 44))
    b = render(out['gatev_mtf'], PROPS, (90, 190, -260), (0, 150, 0), size=(500, 500), fov=50, bg=(200, 210, 220))
    sheet = Image.new('RGB', (1000, 500))
    sheet.paste(a, (0, 0))
    sheet.paste(b, (500, 0))
    sheet.save(os.path.join(PREV, 'hd32_models.png'))
    print('previews written')
