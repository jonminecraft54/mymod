"""Two new staff skins for the Class-D body model (same UV layout as janitor.jpg / scientist.jpg):
   GFX\\npcs\\indev_tech.jpg       plant technician: orange hi-vis shirt, charcoal trousers, "PLANT" on the back
   GFX\\npcs\\indev_archivist.jpg  records archivist: olive cardigan shirt, dark green tie, brown trousers
Only the clothing is recoloured; skin, hair and shoes are left alone."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

NPC = r"I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9\GFX\npcs"
SHIRT_F = (0, 0, 420, 362)
SHIRT_B = (0, 362, 420, 722)
PANTS = (380, 0, 1012, 452)


def blue(reg):
    return ((reg[..., 2] - reg[..., 0]) > 10) & (reg.sum(axis=2) > 90)


def pale(reg):
    lum = reg @ np.array([0.299, 0.587, 0.114])
    return (lum > 100) & (np.abs(reg[..., 0] - reg[..., 2]) < 26)


def tint(a, box, colour, gain=1.0, maskfn=None, floor=38):
    x0, y0, x1, y1 = box
    reg = a[y0:y1, x0:x1].copy()
    lum = reg @ np.array([0.299, 0.587, 0.114])
    mask = maskfn(reg) if maskfn else (lum > floor)   # the sheet background is near black
    m = np.asarray(Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.0))).astype(float) / 255.0
    shade = np.clip(lum / 200.0, 0, 1.25) * gain
    new = shade[..., None] * np.array(colour, dtype=float)[None, None, :]
    a[y0:y1, x0:x1] = reg * (1 - m[..., None]) + new * m[..., None]


def technician():
    a = np.asarray(Image.open(os.path.join(NPC, 'janitor.jpg')).convert('RGB')).astype(float)
    tint(a, SHIRT_F, (236, 120, 30), 1.45, blue)
    tint(a, SHIRT_B, (236, 120, 30), 1.45, blue)
    tint(a, PANTS, (66, 68, 74), 1.5, blue)
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    # reflective bands across chest and back
    for (y0, y1) in ((150, 172), (512, 534)):
        d.rectangle([70, y0, 330, y1], fill=(206, 206, 196))
    # the back print (the sheet is mirrored there, like the JANITOR print it replaces)
    f = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 46)
    txt = Image.new('RGBA', (300, 60), (0, 0, 0, 0))
    ImageDraw.Draw(txt).text((150, 30), "PLANT", font=f, fill=(40, 30, 20, 255), anchor='mm')
    txt = ImageOps.mirror(txt)
    patch = Image.new('RGB', (240, 60), (226, 116, 30))
    im.paste(patch, (80, 420))
    im.paste(txt, (50, 420), txt)
    im = im.filter(ImageFilter.GaussianBlur(0.4))
    im.save(os.path.join(NPC, 'indev_tech.jpg'), quality=92)


def archivist():
    a = np.asarray(Image.open(os.path.join(NPC, 'scientist.jpg')).convert('RGB')).astype(float)
    # the red tie first (so it isn't swallowed by the shirt tint)
    x0, y0, x1, y1 = SHIRT_F
    reg = a[y0:y1, x0:x1]
    tie = (reg[..., 0] > reg[..., 1] * 1.35) & (reg[..., 0] > 110)
    tint(a, SHIRT_F, (150, 146, 112), 0.95, pale)
    tint(a, SHIRT_B, (150, 146, 112), 0.95, pale)
    reg = a[y0:y1, x0:x1]
    reg[tie] = np.array([34.0, 70.0, 46.0])
    tint(a, PANTS, (96, 76, 58), 1.0)
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.4))
    im.save(os.path.join(NPC, 'indev_archivist.jpg'), quality=92)


if __name__ == '__main__':
    technician()
    archivist()
    s = Image.new('RGB', (1024, 512))
    for i, n in enumerate(('indev_tech.jpg', 'indev_archivist.jpg')):
        s.paste(Image.open(os.path.join(NPC, n)).resize((512, 512)), (i * 512, 0))
    s.save('out/npc_new.png')
    print('ok')
