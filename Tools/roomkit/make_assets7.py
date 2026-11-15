"""Assets for the ninth batch (4 SCPs: 457, 016, 152, 280):
   GFX\\map\\indev_labels7.png (+labels7.json)         yellow SCP labels
   GFX\\map\\indev_doorplates7.png (+doorplates7.json) black door plates (the reference corridor's)
   GFX\\map\\indev_plates7.png (+plates7.json)         name plates and warning signs
   GFX\\map\\indev_props7.png (+props7.json)           printed things: hose reel, fire suit, dented door, experiment board ...
   GFX\\map\\indev_neon7.png (+neon7.json)             things that glow: UV tubes, gauges, the IR monitor
   GFX\\map\\indev_perlite.png, indev_char0..5.png     fireproof board, and what SCP-457 chars into it
   GFX\\npcs\\indev_firesuit.jpg, indev_mopp.jpg       NPC skins
   GFX\\items\\doc*.jpg                                8 documents (own wording, after the wiki articles)"""
import json
import math
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from make_assets3 import MAPDIR, font, wear, mottle
from make_assets5 import ft, save_map, noise, skin
from make_docs2 import typed, note, ITEMS
import make_npctex as NT

SCPS = [('457', 'EUCLID'), ('016', 'KETER'), ('152', 'SAFE'), ('280', 'KETER')]
CLS = {'SAFE': (30, 120, 40), 'EUCLID': (200, 130, 20), 'KETER': (180, 24, 20)}


def labels():
    W, H = 1024, 256
    im = Image.new('RGB', (W, H), (20, 20, 20))
    d = ImageDraw.Draw(im)
    rects = {}
    for i, (num, cls) in enumerate(SCPS):
        x, y = i * 256, 0
        rects[num] = (x / W, y / H, (x + 256) / W, (y + 256) / H)
        d.rectangle([x, y, x + 255, y + 255], fill=(238, 236, 228))
        d.rectangle([x, y, x + 255, y + 70], fill=(236, 208, 34))
        d.text((x + 12, y + 6), "SCP", font=font(46), fill=(20, 20, 20))
        cx, cy = x + 204, y + 36
        d.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], outline=(20, 20, 20), width=4)
        d.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], outline=(20, 20, 20), width=3)
        for k in range(3):
            a = math.radians(90 + 120 * k)
            d.line([(cx + 11 * math.cos(a), cy - 11 * math.sin(a)), (cx + 28 * math.cos(a), cy - 28 * math.sin(a))], fill=(20, 20, 20), width=5)
        d.text((x + 12, y + 80), "SCP-" + num, font=font(36), fill=(20, 20, 20))
        d.text((x + 12, y + 126), "OBJECT CLASS:", font=font(17), fill=(20, 20, 20))
        d.text((x + 12, y + 148), cls, font=font(30), fill=CLS[cls])
        tx, ty = x + 54, y + 218
        d.polygon([(tx, ty - 30), (tx - 34, ty + 28), (tx + 34, ty + 28)], fill=(236, 208, 34), outline=(20, 20, 20))
        d.text((tx, ty + 6), "!", font=font(34), fill=(20, 20, 20), anchor='mm')
        d.rectangle([x + 150, y + 190, x + 244, y + 246], fill=(26, 26, 28))
        d.rectangle([x, y, x + 255, y + 255], outline=(30, 30, 30), width=3)
    save_map(wear(im, 71), 'indev_labels7.png')
    json.dump(rects, open('labels7.json', 'w'), indent=1)


DOORPLATES = [('457', 'SCP-457', 'EUCLID'), ('016', 'SCP-016', 'KETER'), ('152', 'SCP-152', 'SAFE'), ('280', 'SCP-280', 'KETER'),
              ('d0161', 'D-016-1', 'FLOODED'), ('d0162', 'D-016-2', 'SEALED'), ('lab016', 'LAB 016', 'BC-L5'), ('decon', 'DECON', 'UV / OPA')]


def doorplates():
    W, H = 1024, 512
    im = Image.new('RGB', (W, H), (16, 16, 16))
    d = ImageDraw.Draw(im)
    rects = {}
    for i, (k, top, bottom) in enumerate(DOORPLATES):
        x, y = (i % 4) * 256, (i // 4) * 256
        rects[k] = (x / W, y / H, (x + 256) / W, (y + 256) / H)
        d.rectangle([x + 4, y + 4, x + 251, y + 251], fill=(26, 26, 27))
        d.rectangle([x + 14, y + 14, x + 241, y + 241], outline=(150, 150, 146), width=5)
        sz = 54
        while d.textlength(top, font=font(sz)) > 210:
            sz -= 2
        d.text((x + 128, y + 92), top, font=font(sz), fill=(228, 226, 220), anchor='mm')
        d.line([(x + 34, y + 134), (x + 222, y + 134)], fill=(150, 150, 146), width=4)
        sz = 40
        while d.textlength(bottom, font=font(sz)) > 200:
            sz -= 2
        d.text((x + 128, y + 182), bottom, font=font(sz), fill=(228, 226, 220), anchor='mm')
    save_map(wear(im, 72), 'indev_doorplates7.png')
    json.dump(rects, open('doorplates7.json', 'w'), indent=1)


PLATES = [('c457', 'CONTAINMENT CHAMBER 457'), ('firepost', 'FIRE POST 457 - SUITS AND HOSES'), ('three', 'ENTER IN GROUPS OF THREE'),
          ('mistrun', 'MIST SYSTEM MUST RUN AT ALL TIMES'), ('allot', 'FUEL: DAILY ALLOTMENT ONLY'), ('blast', 'BLAST SHIELD'),
          ('airlock1', 'AIRLOCK 1'), ('airlock2', 'AIRLOCK 2'), ('hose', 'EMERGENCY HOSE  2.1 MPa'), ('fuel', 'FUEL INJECTOR'),
          ('bcl5', 'BC-L5 CONTAINMENT - SCP-016'), ('sigma', 'CODE SIGMA LOCKDOWN POINT'), ('coldroom', 'COLD ROOM  0 C OR BELOW'),
          ('uvfirst', 'RUN UV CYCLE BEFORE ENTRY'), ('mopp', 'MOPP EQUIPMENT'), ('nodrain', 'TANK DRAIN - LEVEL 4 ONLY'),
          ('reading', 'READING ROOM 49'), ('quiet', 'QUIET'), ('level2', 'CLEARANCE LEVEL 2 AND ABOVE'),
          ('lastpage', 'LEAVE OPEN AT THE LAST PAGE'), ('editions', 'SCAN ARCHIVE - PRIOR EDITIONS'),
          ('dark280', 'DARK CELL 280'), ('nolight', 'NO LIGHT BEYOND THIS DOOR'), ('lampctl', 'CELL LIGHTING CONTROL'),
          ('onemetre', 'KEEP ONE METRE FROM SCP-280'), ('irgear', 'IR GOGGLES / ID STROBES'), ('noequip', 'LEAVE NO EQUIPMENT INSIDE'),
          ('lamp', 'INSPECTION LAMP'), ('flood', 'FLOODLIGHTS'), ('uvrun', 'UV CYCLE')]
WARN = ('three', 'mistrun', 'allot', 'sigma', 'uvfirst', 'nodrain', 'nolight', 'onemetre', 'noequip', 'flood', 'quiet')


def plates():
    W, H, RH = 1024, 1024, 64
    im = Image.new('RGB', (W, H), (20, 20, 20))
    d = ImageDraw.Draw(im)
    rects = {}
    for i, (k, text) in enumerate(PLATES):
        x, y = (i % 2) * 512, (i // 2) * RH
        rects[k] = (x / W, y / H, (x + 512) / W, (y + RH) / H)
        yellow = k in WARN
        blue = k in ('reading', 'level2', 'lastpage', 'editions')
        bg = (22, 40, 70) if blue else (22, 22, 22)
        d.rectangle([x, y, x + 511, y + RH - 1], fill=bg)
        d.rectangle([x + 3, y + 3, x + 508, y + RH - 4], outline=(220, 180, 40) if yellow else (130, 130, 130), width=4)
        sz = 44
        while d.textlength(text, font=font(sz)) > 470:
            sz -= 2
        d.text((x + 256, y + RH // 2), text, font=font(sz), fill=(250, 214, 40) if yellow else (240, 238, 230), anchor='mm')
    save_map(wear(im, 73), 'indev_plates7.png')
    json.dump(rects, open('plates7.json', 'w'), indent=1)


def props():
    W, H = 1024, 1024
    im = Image.new('RGB', (W, H), (230, 228, 220))
    d = ImageDraw.Draw(im)
    R = {}

    def box(k, x0, y0, x1, y1):
        R[k] = (x0 / W, y0 / H, x1 / W, y1 / H)

    # the hose reel on its red board
    d.rectangle([0, 0, 255, 255], fill=(170, 26, 22))
    d.ellipse([38, 38, 218, 218], fill=(40, 40, 44), outline=(20, 20, 20), width=4)
    for r in range(84, 30, -9):
        d.ellipse([128 - r, 128 - r, 128 + r, 128 + r], outline=(196, 190, 170), width=5)
    d.ellipse([110, 110, 146, 146], fill=(150, 150, 156))
    d.rectangle([200, 190, 244, 204], fill=(210, 170, 40))
    d.text((128, 238), "FIRE HOSE", font=ft('arialbd.ttf', 20), fill=(250, 240, 230), anchor='mm')
    box('hosereel', 0, 0, 256, 256)
    # an aluminised fire suit hanging in a locker
    d.rectangle([256, 0, 511, 319], fill=(60, 64, 70))
    d.rectangle([288, 22, 478, 312], fill=(36, 38, 42))
    d.ellipse([350, 34, 416, 100], fill=(196, 200, 206))
    d.rectangle([362, 54, 404, 76], fill=(60, 50, 20))
    d.polygon([(328, 100), (438, 100), (462, 290), (304, 290)], fill=(190, 194, 200))
    for yy in range(120, 290, 34):
        d.line([(312, yy), (454, yy)], fill=(150, 154, 160), width=2)
    d.rectangle([374, 100, 392, 290], fill=(120, 124, 130))
    box('firesuit', 256, 0, 512, 320)
    # the fuel log on a clipboard
    d.rectangle([512, 0, 767, 191], fill=(120, 90, 60))
    d.rectangle([526, 20, 753, 181], fill=(240, 236, 224))
    d.rectangle([610, 6, 670, 26], fill=(150, 150, 156))
    for k, ln in enumerate(("FUEL LOG  SCP-457", "MON  1 allotment  OK", "TUE  1 allotment  OK", "WED  1 allotment  OK", "THU  3 (!!)  incident", "FRI  0  mist only")):
        d.text((536, 34 + k * 23), ln, font=ft('courbd.ttf' if k in (0, 4) else 'cour.ttf', 15), fill=(170, 30, 30) if k == 4 else (30, 30, 30))
    box('fuellog', 512, 0, 768, 192)
    # biohazard sign
    d.rectangle([768, 0, 1023, 255], fill=(250, 214, 40))
    cx, cy = 896, 132
    for a in (90, 210, 330):
        px, py = cx + 46 * math.cos(math.radians(a)), cy - 46 * math.sin(math.radians(a))
        d.ellipse([px - 46, py - 46, px + 46, py + 46], outline=(20, 20, 20), width=14)
    d.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], fill=(250, 214, 40))
    d.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], outline=(20, 20, 20), width=8)
    d.text((896, 236), "BIOHAZARD  BC-L5", font=ft('arialbd.ttf', 20), fill=(20, 20, 20), anchor='mm')
    box('biohaz', 768, 0, 1024, 256)
    # the reinforced door of D-016-2's quarters, seen from inside: knuckle dents
    d.rectangle([0, 256, 255, 639], fill=(96, 100, 106))
    for yy in (268, 448, 624):
        for xx in range(14, 250, 26):
            d.ellipse([xx - 4, yy - 4, xx + 4, yy + 4], fill=(70, 72, 78))
    rng = np.random.default_rng(162)
    for _ in range(22):
        px, py = rng.integers(40, 216), rng.integers(300, 600)
        r = rng.integers(10, 22)
        d.ellipse([px - r, py - r, px + r, py + r], fill=(60, 62, 68))
        d.ellipse([px - r + 4, py - r + 5, px + r - 2, py + r - 1], fill=(120, 124, 130))
        d.ellipse([px - 4, py - 3, px + 5, py + 6], fill=(92, 30, 26))
    box('dent', 0, 256, 256, 640)
    # the experiment board in the lab
    d.rectangle([256, 320, 767, 575], fill=(244, 244, 240))
    d.rectangle([256, 320, 767, 575], outline=(150, 150, 150), width=6)
    rows = ["SUBJECT   STRESSOR        RESULT", "D-016-1   rising water    gills, fins, sonar", "D-016-2   rising water    fists; tried the door",
            "D-016-3   rising water    gas organ (shot)", "D-016-4   none, 'wings'   bled out", "D-016-5   drop + timer    silk; held the cable",
            "", "NO STRESS = NO CHANGE = PHASE 3"]
    for k, ln in enumerate(rows):
        col = (170, 30, 30) if k == 7 else ((20, 40, 120) if k else (20, 20, 20))
        d.text((272, 338 + k * 28), ln, font=ft('courbd.ttf' if k in (0, 7) else 'cour.ttf', 17), fill=col)
    box('exptable', 256, 320, 768, 576)
    # UV warning
    d.rectangle([768, 256, 1023, 383], fill=(110, 40, 160))
    d.text((896, 296), "UV-C", font=ft('arialbd.ttf', 44), fill=(255, 255, 255), anchor='mm')
    d.text((896, 350), "PROTECT EYES AND SKIN", font=ft('arialbd.ttf', 16), fill=(255, 230, 120), anchor='mm')
    box('uvsign', 768, 256, 1024, 384)
    # binder spines for the scan archive: one "edition" each
    d.rectangle([768, 384, 1023, 511], fill=(50, 44, 40))
    for k in range(12):
        x0 = 772 + k * 21
        col = [(96, 60, 40), (70, 50, 44), (110, 80, 50), (60, 44, 40)][k % 4]
        d.rectangle([x0, 388, x0 + 18, 508], fill=col)
        d.rectangle([x0 + 3, 400, x0 + 15, 440], fill=(230, 224, 200))
        d.text((x0 + 9, 420), str(140 + k * 7), font=ft('arial.ttf', 8), fill=(20, 20, 20), anchor='mm')
    box('edition', 768, 384, 1024, 512)
    # the goggle rack: hooks, tags, nothing on them
    d.rectangle([256, 576, 767, 767], fill=(70, 74, 80))
    for k in range(6):
        cx = 300 + k * 80
        d.rectangle([cx - 3, 610, cx + 3, 650], fill=(170, 172, 178))
        d.arc([cx - 14, 640, cx + 14, 668], 0, 180, fill=(170, 172, 178), width=5)
        d.rectangle([cx - 26, 690, cx + 26, 716], fill=(236, 230, 210))
        d.text((cx, 703), "OUT", font=ft('courbd.ttf', 15), fill=(170, 30, 30), anchor='mm')
    d.text((512, 742), "IR GOGGLES - SIGN OUT / SIGN IN", font=ft('arialbd.ttf', 17), fill=(230, 230, 230), anchor='mm')
    box('irrack', 256, 576, 768, 768)
    # the torch sign-out sheet
    d.rectangle([768, 512, 1023, 703], fill=(240, 236, 224))
    for k, ln in enumerate(("HAND LAMPS", "1  Reyes   OUT", "2  Reyes   OUT", "3  (flat)", "4  missing", "strobe tags: bin")):
        d.text((782, 524 + k * 28), ln, font=ft('courbd.ttf' if k == 0 else 'cour.ttf', 17), fill=(30, 30, 30))
    box('lamps', 768, 512, 1024, 704)
    # a floor drain grate with scorch round it, and a quiet-please card
    d.rectangle([0, 640, 255, 895], fill=(70, 70, 72))
    for k in range(9):
        d.rectangle([24 + k * 24, 664, 36 + k * 24, 872], fill=(18, 18, 20))
    d.rectangle([16, 656, 240, 880], outline=(120, 120, 124), width=6)
    box('drain', 0, 640, 256, 896)
    d.rectangle([768, 704, 1023, 895], fill=(22, 40, 70))
    d.text((896, 760), "QUIET", font=ft('georgiab.ttf', 60), fill=(240, 238, 230), anchor='mm')
    d.text((896, 830), "the book is being read", font=ft('georgiai.ttf', 20), fill=(200, 210, 230), anchor='mm')
    box('quietcard', 768, 704, 1024, 896)
    save_map(wear(im, 74), 'indev_props7.png')
    json.dump(R, open('props7.json', 'w'), indent=1)


def neon():
    W, H = 1024, 512
    im = Image.new('RGB', (W, H), (6, 8, 6))
    d = ImageDraw.Draw(im)
    R = {}
    # the chamber panel under the blast window: amber
    d.rectangle([0, 0, 511, 255], fill=(20, 12, 2))
    for k, ln in enumerate(("CHAMBER 457", "MIST SYSTEM   RUNNING", "HUMIDITY      96 %", "CHAMBER TEMP  61 C", "FUEL FLOW     ALLOTMENT", "BLAST SHIELD  OPEN")):
        d.text((16, 14 + k * 38), ln, font=ft('courbd.ttf', 24), fill=(255, 176, 40))
    R['chamber'] = (0, 0, 0.5, 0.5)
    # the IR monitor of the dark cell
    d.rectangle([512, 0, 1023, 255], fill=(4, 22, 8))
    for yy in range(0, 256, 4):
        d.line([(512, yy), (1023, yy)], fill=(6, 30, 12))
    d.ellipse([730, 50, 800, 128], fill=(2, 8, 4))
    d.polygon([(716, 120), (814, 120), (834, 250), (696, 250)], fill=(2, 8, 4))
    d.line([(716, 140), (650, 200)], fill=(2, 8, 4), width=14)
    d.line([(814, 140), (880, 200)], fill=(2, 8, 4), width=14)
    for cx in (750, 782):
        d.ellipse([cx - 9, 78, cx + 9, 96], fill=(220, 255, 220))
    d.text((524, 8), "IR  CELL 280  CAM 1", font=ft('courbd.ttf', 18), fill=(120, 255, 140))
    d.text((524, 230), "LIGHTS: OFF", font=ft('courbd.ttf', 18), fill=(120, 255, 140))
    R['irmon'] = (0.5, 0, 1, 0.5)
    # UV tube (a strip), the scale readout, the cold room readout, the reading-room camera feed
    a = np.asarray(im).astype(float)
    yy = np.arange(64)[:, None]
    glow = np.exp(-((yy - 32) / 13.0) ** 2)
    a[256:320, 0:512, 0] = 150 * glow + 40
    a[256:320, 0:512, 1] = 60 * glow + 6
    a[256:320, 0:512, 2] = 255 * glow + 60
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    R['uv'] = (0, 0.5, 0.5, 0.625)
    d.rectangle([0, 320, 255, 447], fill=(6, 20, 8))
    d.text((128, 364), "12.412 kg", font=ft('courbd.ttf', 36), fill=(90, 255, 110), anchor='mm')
    d.text((128, 420), "SCALE ARMED", font=ft('courbd.ttf', 20), fill=(90, 255, 110), anchor='mm')
    R['scale'] = (0, 0.625, 0.25, 0.875)
    d.rectangle([256, 320, 511, 447], fill=(4, 10, 30))
    d.text((384, 364), "-4.0 C", font=ft('courbd.ttf', 48), fill=(120, 190, 255), anchor='mm')
    d.text((384, 420), "COLD ROOM 016", font=ft('courbd.ttf', 20), fill=(120, 190, 255), anchor='mm')
    R['cold'] = (0.25, 0.625, 0.5, 0.875)
    d.rectangle([512, 256, 1023, 511], fill=(30, 32, 34))
    d.rectangle([700, 380, 830, 420], fill=(70, 62, 50))
    d.rectangle([740, 366, 792, 382], fill=(120, 96, 60))
    d.ellipse([744, 300, 790, 330], fill=(200, 196, 170))
    d.line([(767, 256), (767, 300)], fill=(90, 90, 90), width=2)
    d.text((524, 264), "READING ROOM  CAM 1", font=ft('courbd.ttf', 18), fill=(200, 200, 200))
    R['cam'] = (0.5, 0.5, 1, 1)
    im.save(os.path.join(MAPDIR, 'indev_neon7.png'))
    json.dump(R, open('neon7.json', 'w'), indent=1)


def perlite():
    """the chamber lining: pale fireproof boards, seams every 128, scorched from the floor up"""
    S = 256
    n = noise(S, S, 457, 6, 1.5)
    a = np.zeros((S, S, 3)) + np.array([198, 196, 188.0])
    a *= (0.86 + 0.24 * n)[..., None]
    for k in (0, 128):
        a[:, k:k + 3] *= 0.6
        a[k:k + 3, :] *= 0.6
    rng = np.random.default_rng(458)
    a += rng.normal(0, 5, (S, S, 1))
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(os.path.join(MAPDIR, 'indev_perlite.png'))
    # scorch: black, alpha strongest at the centre
    b = np.zeros((S, S, 4), dtype=np.uint8)
    yy, xx = np.mgrid[0:S, 0:S]
    r = np.sqrt((xx - S / 2) ** 2 + (yy - S / 2) ** 2) / (S / 2)
    al = np.clip((1.0 - r) * 1.5 + (noise(S, S, 459, 5, 1.0) - 0.5) * 0.9, 0, 1) * 210
    b[..., 0], b[..., 1], b[..., 2], b[..., 3] = 14, 12, 10, al.astype(np.uint8)
    Image.fromarray(b).save(os.path.join(MAPDIR, 'indev_scorch.png'))


CHAR = ["HUNGRY", "FUEL. MORE.", "NO WATER", "WATER OFF. I SLEEP.", "WANT TO BURN", "THEY BURN"]


def char_messages():
    W, H = 512, 160
    for k, text in enumerate(CHAR):
        n = noise(H, W, 460 + k, 6, 1.5)
        base = (np.zeros((H, W, 3)) + np.array([198, 196, 188.0])) * (0.86 + 0.24 * n)[..., None]
        mask = Image.new('L', (W, H), 0)
        d = ImageDraw.Draw(mask)
        sz = 110
        while d.textlength(text, font=ft('impact.ttf', sz)) > W - 50:
            sz -= 4
        d.text((W // 2, H // 2), text, font=ft('impact.ttf', sz), fill=255, anchor='mm')
        m = np.asarray(mask.filter(ImageFilter.GaussianBlur(2.2))).astype(float) / 255.0
        m = np.clip((m + (noise(H, W, 470 + k, 3, 0.8) - 0.5) * 0.7 - 0.35) * 4, 0, 1)
        halo = np.asarray(mask.filter(ImageFilter.GaussianBlur(12))).astype(float) / 255.0
        out = base * (1 - halo * 0.55)[..., None]
        out = out * (1 - m[..., None]) + m[..., None] * np.array([26, 20, 16.0])
        Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(os.path.join(MAPDIR, 'indev_char%d.png' % k))


def skins():
    skin('janitor.jpg', 'indev_firesuit.jpg', (204, 208, 214), (194, 198, 204), 1.3, NT.blue)
    skin('janitor.jpg', 'indev_mopp.jpg', (100, 108, 64), (90, 98, 58), 1.4, NT.blue)


def lastpage():
    """a copier's copy of SCP-152's last page: vellum, black ink, one phrase that would not translate"""
    W, H = 581, 819
    n = noise(H, W, 152, 8, 3.0)
    a = (np.zeros((H, W, 3)) + np.array([226, 214, 184.0])) * (0.9 + 0.18 * n)[..., None]
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 34], fill=(236, 236, 232))
    d.text((W // 2, 17), "COPY - SCP-152 - LAST PAGE - NOT FOR REMOVAL", font=ft('courbd.ttf', 14), fill=(60, 60, 60), anchor='mm')
    lines = ["...and so the lights of the Site went", "out in their order: Light, then Heavy,", "then the unfinished halls, then the",
             "offices; and the Old Machine kept every", "door it wished to keep.", "",
             "Of the one in orange, numbered 9341,", "it is set down that he came up in the", "lift, and read this page, and went", "down again.", "",
             "What he did next is told differently", "in every edition.", "", "In this one he"]
    y = 90
    for ln in lines:
        d.text((64, y), ln, font=ft('georgiai.ttf', 25), fill=(24, 20, 16))
        y += 40
    rng = np.random.default_rng(1520)
    x = 240
    for _ in range(7):
        pts = [(x + rng.integers(0, 26), y - 40 + rng.integers(0, 30)) for _ in range(4)]
        d.line(pts, fill=(24, 20, 16), width=3)
        d.arc([x, y - 44, x + 22, y - 22], int(rng.integers(0, 180)), int(rng.integers(200, 360)), fill=(24, 20, 16), width=2)
        x += 34
    d.text((64, y + 30), "(seven characters; no known script)", font=ft('cour.ttf', 14), fill=(90, 80, 70))
    im.filter(ImageFilter.GaussianBlur(0.4)).save(os.path.join(ITEMS, 'doc152b.jpg'), quality=90)


def docs():
    typed('doc457', [('Clearance Level', '3'), ('Item #', 'SCP-457'), ('Object Class', 'Euclid')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'SCP-457 is kept in a 5 m x 5 m chamber lined with at least 23 cm of fireproofing, behind a blast window with a '
              'shield, and reached through two airlocks. {The misting sprinklers run at all times.} One dry shelter on the '
              'wall is allowed.'),
        ('p', 'Staff enter in threes, in sealed flame-retardant suits, to deliver the daily fuel allotment or to repair the '
              'sprinklers. If it turns hostile, drive it back to its shelter with the hoses.'),
        ('h', 'Description:'),
        ('p', 'SCP-457 is a thinking being made of flame. At its smallest it is a single flame that jumps to whatever will '
              'burn. {With more fuel it grows, takes a human shape, and becomes cleverer.} Past a certain size it splits '
              'in two, and the two fight.'),
        ('p', 'It writes by charring letters into surfaces and, rarely, speaks. It has wrecked sprinklers, laid traps, and '
              'tried to talk staff into feeding it or letting it out.'),
        ('h', 'Addendum:'),
        ('p', 'Asked how it felt about humans, it said: they burn. {Do not feed it past the allotment. Do not believe what it writes.}'),
    ])
    typed('doc016', [('Clearance Level', '4'), ('Item #', 'SCP-016'), ('Object Class', 'Keter')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'SCP-016 stays in its petri dish, in the containment cube, in a cold room held at or below 0 C. It lives up to '
              'six hours on hard surfaces and several minutes in air. {Strong ultraviolet light disinfects surfaces.} '
              'An outbreak means a Code Sigma lockdown.'),
        ('h', 'Description:'),
        ('p', 'SCP-016 is a blood-borne pathogen found in a miner who cut himself in a deep coal seam. It starts like a '
              'cold: itching eyes, a cough. Then a slow bleed into the lungs. Then the host bleeds out from everywhere at '
              'once. A host who lives through that carries it dormant.'),
        ('p', '{Under severe stress it changes tactics: it rewrites the host and rebuilds the body to meet the threat.} '
              'Most do not survive the rebuilding. Those who do stop bleeding, and become aggressive.'),
        ('h', 'Addendum:'),
        ('p', 'Two subjects in flooding rooms: one grew gills, one grew fists and tried the door. A calm subject told to '
              'think about wings simply bled.'),
    ])
    typed('doc152', [('Clearance Level', '2'), ('Item #', 'SCP-152'), ('Object Class', 'Safe')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'SCP-152 is kept in the reading room: one lamp, one camera, one copier, one chair, one desk. {When not in use '
              'it is left open at its last page} so that additions are seen at once. A guard is posted outside. Keep quiet '
              'near the room.'),
        ('h', 'Description:'),
        ('p', 'SCP-152 is a large leather-bound book. Every entry describes an end of humanity, from the sun failing in '
              '6000 BC to the last few years, each followed to the death of the last human. Each history is accurate '
              'until a few decisions go differently.'),
        ('p', 'It reads in whatever language the reader finds easiest, down to their own slang. Nothing will mark its '
              'pages. {New entries appear on the last page without warning.}'),
        ('h', 'Incident 152-05:'),
        ('p', 'When it updates, the book is gone for exactly one second. Dr. Jansen holds that it does not change: each '
              'time, we are sent a new edition.'),
    ])
    typed('doc280', [('Clearance Level', '4'), ('Item #', 'SCP-280'), ('Object Class', 'Keter')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'SCP-280 is kept in a 5 m x 5 m cell in total darkness. {No equipment is left inside.} Staff entering wear '
              'infrared goggles and carry a strong light.'),
        ('p', 'If it attacks, light the person under attack and keep lighting until it backs away. Do nothing aggressive. '
              '{Stay one metre from it.}'),
        ('h', 'Description:'),
        ('p', 'SCP-280 is a black, human-shaped mass with long thin fingers and no visible legs. It glides towards any '
              'human with its hands held out and tears at them until they are dead. It is solid only when it chooses, and '
              'stays intangible until the moment it attacks.'),
        ('p', 'It retreats slowly from light, showing two white eyes that do not see. {If its surroundings are fully lit, '
              'or a bright burst hits it, it vanishes and reappears somewhere else.}'),
        ('h', 'Addendum:'),
        ('p', 'In the dark it is taken for a shadow or a coat. People have walked through it and reported only dread.'),
    ])
    NOTES = {
        'doc457b': ({0: 'Fire Post 457 - shift notes', 1: 'Mist ON. Always. Check twice.', 2: 'One press of FUEL per day.',
                     3: 'Every extra press and it', 4: 'stands taller and thinks more.', 6: 'It writes on the back wall.',
                     7: 'Last week: WATER OFF. I SLEEP.', 8: 'Novak believed it.', 10: 'Novak is still in the chamber.',
                     11: 'So is his card. Level 4.', 12: 'Suit up. Hug the west wall.'}, '- Fire crew'),
        'doc016b': ({0: 'BC-L5 lab - read before entry', 1: 'A tray went down in the cold', 2: 'room. Culture on the floor.',
                     3: 'RUN THE UV FIRST. Full cycle.', 4: 'Mask or suit, or stay out.', 6: 'D-016-2 is still in his cell.',
                     7: 'Do not touch him bare-handed.', 9: 'If you catch it: do NOT rest.', 10: 'Calm hosts bleed out.',
                     11: 'Frightened ones change.'}, '- Duty officer'),
        'doc280b': ({0: 'Dark Cell 280 - handover', 1: 'LAMP lever: it backs into the', 2: 'corner and shows its eyes.',
                     3: 'You can work by the door.', 5: 'FLOOD lever: DO NOT.', 6: 'Fully lit, it leaves the cell.',
                     7: 'It comes back out HERE.', 9: 'Reyes went in without the lamp', 10: 'to fetch his goggles. He and',
                     11: 'the goggles are still in there.'}, '- Night tech'),
    }
    for name, (rows, sign) in NOTES.items():
        note(name, rows, sign=sign)
    lastpage()
    return NOTES


TITLES = {
    'doc457': 'Document SCP-457', 'doc457b': 'Fire Post 457 Shift Notes',
    'doc016': 'Document SCP-016', 'doc016b': 'BC-L5 Lab Entry Note',
    'doc152': 'Document SCP-152', 'doc152b': 'Copy of the Last Page',
    'doc280': 'Document SCP-280', 'doc280b': 'Dark Cell 280 Handover Note',
}


if __name__ == '__main__':
    labels()
    doorplates()
    plates()
    props()
    neon()
    perlite()
    char_messages()
    skins()
    notes = docs()
    assert set(TITLES) == {'doc' + n for n, _ in SCPS} | set(notes) | {'doc152b'}
    print('batch 9 assets, %d documents' % len(TITLES))
