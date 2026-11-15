"""indev_signs.png - one 1024x1024 atlas of wall signs for the new rooms (SCP:CB plate style)."""
import os, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = r"I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9\GFX\map\indev_signs.png"
F = r"C:\Windows\Fonts"
def font(sz, bold=True):
    return ImageFont.truetype(os.path.join(F, 'arialbd.ttf' if bold else 'arial.ttf'), sz)

W = H = 1024
im = Image.new('RGB', (W, H), (20, 20, 20))
d = ImageDraw.Draw(im)
rects = {}

def fit(text, w, h, bold=True, maxsz=200):
    sz = maxsz
    while sz > 6:
        f = font(sz, bold)
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

BLK, WHT, YEL, RED, BLU = (22, 22, 22), (235, 233, 226), (232, 196, 28), (190, 28, 24), (30, 80, 170)
# row 0: wide black name plates  (512 x 128)
plate('atrium',    0,   0, 512, 128, "SERVICE ATRIUM 2-C", BLK, WHT, border=(120, 120, 120))
plate('gallery',   512, 0, 512, 128, "LOWER GALLERY", BLK, WHT, border=(120, 120, 120))
plate('records',   0, 128, 512, 128, "RECORDS ANNEX 3-C", BLK, WHT, border=(120, 120, 120))
plate('ventcore',  512, 128, 512, 128, "VENTILATION CORE", BLK, YEL, border=(120, 110, 40))
# row 2: elevator plates (256 x 128)
plate('elevator',  0, 256, 384, 128, "ELEVATOR", BLK, WHT, border=(120, 120, 120))
plate('upper',     384, 256, 320, 128, "UPPER STORE", BLK, WHT, border=(120, 120, 120))
plate('fanstart',  704, 256, 320, 128, "EXTRACTION FAN\nMANUAL START", BLK, YEL, border=(120, 110, 40))
# row 3: caution / danger signs (256 x 256)
plate('c_level2',  0, 384, 256, 256, "LEVEL 2\nCLEARANCE\nREQUIRED", YEL, BLK, head="CAUTION", headbg=BLK, headfg=YEL)
plate('d_tools',   256, 384, 256, 256, "DO NOT USE\nTOOLS ON\nPIPEWORK", WHT, BLK, head="DANGER", headbg=RED, headfg=WHT)
plate('m_mask',    512, 384, 256, 256, "RESPIRATOR\nREQUIRED\nBEYOND\nTHIS POINT", BLU, WHT, border=WHT)
plate('n_quiet',   768, 384, 256, 256, "RECORDS MAY\nNOT LEAVE\nTHE ANNEX", WHT, BLK, head="NOTICE", headbg=BLU, headfg=WHT)
# row 4: containment labels (384 x 192) and notices
plate('l_015',     0, 640, 384, 192, "SCP-015\nEUCLID", WHT, BLK, border=BLK, head="CONTAINMENT ANNEX", headbg=BLK, headfg=WHT, headh=0.3)
plate('l_055',     384, 640, 384, 192, "SCP-055\n[UNKNOWN]", WHT, BLK, border=BLK, head="CONTAINMENT CHAMBER", headbg=BLK, headfg=WHT, headh=0.3)
plate('nameplate', 768, 640, 256, 96, "DR. A. IMRE\nRECORDS", (60, 46, 30), (220, 200, 150))
plate('pit',       768, 736, 256, 96, "NO ENTRY\nBELOW", RED, WHT, border=WHT)
# row 5: the 055 notice + misc
plate('n_055',     0, 832, 512, 192, "THERE IS NOTHING BEHIND THIS DOOR.\nIF YOU REMEMBER READING THIS,\nYOU HAVE ALREADY BEEN INSIDE.", YEL, BLK, head="NOTICE", headbg=BLK, headfg=YEL, headh=0.26)
plate('l1',        512, 832, 128, 96, "L1", BLK, WHT, border=(120, 120, 120))
plate('l2',        640, 832, 128, 96, "L2", BLK, WHT, border=(120, 120, 120))
plate('b1',        768, 832, 128, 96, "B1", BLK, WHT, border=(120, 120, 120))
plate('g',         896, 832, 128, 96, "G", BLK, WHT, border=(120, 120, 120))
plate('fan_on',    512, 928, 256, 96, "FAN: RUN", (30, 110, 40), WHT, border=WHT)
plate('fan_off',   768, 928, 256, 96, "FAN: TRIPPED", RED, WHT, border=WHT)
# the blacked-out object number on the 055 label

# wear: grain, smudges, darker edges, a few scratches (matches the grubby vanilla sign sheets)
a = np.asarray(im).astype(np.float64)
rng = np.random.default_rng(31)
g = rng.normal(0, 9, (H, W))
sm = np.asarray(Image.fromarray(((rng.random((H // 8, W // 8))) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)
                .filter(ImageFilter.GaussianBlur(6))).astype(np.float64) / 255.0
a = a * (0.80 + 0.28 * sm[..., None]) + g[..., None]
im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
d2 = ImageDraw.Draw(im)
for _ in range(140):
    x, y = rng.integers(0, W), rng.integers(0, H)
    l = int(rng.integers(6, 40)); ang = rng.random() * 6.28
    c = int(rng.integers(40, 110))
    d2.line([(x, y), (x + l * np.cos(ang), y + l * np.sin(ang))], fill=(c, c, c), width=1)
im = im.filter(ImageFilter.GaussianBlur(0.5))
im.save(OUT)
json.dump(rects, open('signs.json', 'w'), indent=1)
im.save('out/indev_signs_preview.png')
print('wrote', OUT, len(rects), 'signs')
