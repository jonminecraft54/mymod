r"""The Gate V access card, in the style of the game's keycards (GFX\items\keycard.x with a texture override):
the user's blue card template (image 89: the blue band, SCP / Secure. Contain. Protect, the white stripe, the chip and
the arrow) completed like the game's level cards - a "V" level box, GATE V ACCESS CARD on the stripe, a serial
number, the warning line - and an inventory icon rendered from it at the angle of the game's own icons.
     GFX\items\keycardgatev.png   GFX\items\INVkeygatev.png
   python make_keygatev.py"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = r'I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9'
ITEMS = os.path.join(ROOT, 'GFX', 'items')
SRC = r'C:\Users\Computer\AppData\Local\Temp\claude\5f091e0c700b8823\26a70fcf-4472-4ddb-a1ca-a030fd032c01\images\89.png'
FB = r'C:\Windows\Fonts\arialbd.ttf'
FI = r'C:\Windows\Fonts\impact.ttf' if os.path.exists(r'C:\Windows\Fonts\impact.ttf') else FB
BLUE = (16, 16, 236)


def texture():
    im = Image.open(SRC).convert('RGB').resize((512, 512), Image.LANCZOS)
    d = ImageDraw.Draw(im)
    # the level box, as on the game's cards: a white rounded square with a dark rim and the level in the card colour
    d.rounded_rectangle([380, 108, 498, 226], 10, fill=(255, 255, 255), outline=(20, 20, 30), width=6)
    d.text((439, 170), 'V', font=ImageFont.truetype(FI, 112), fill=BLUE, anchor='mm')
    # the stripe: what the card is, its serial number
    d.text((10, 270), 'GATE V ACCESS CARD', font=ImageFont.truetype(FI, 44), fill=(10, 10, 14), anchor='lm')
    d.text((10, 327), '05-0591326-GATEV', font=ImageFont.truetype(FB, 20), fill=BLUE, anchor='lm')
    d.text((240, 327), 'EMERGENCY EXIT - UNDERGROUND', font=ImageFont.truetype(FB, 13), fill=(60, 60, 70), anchor='lm')
    # the warning on the lower band
    f1, f2 = ImageFont.truetype(FB, 17), ImageFont.truetype(FB, 15)
    d.text((256, 392), 'WARNING: Use of this card outside an authorised', font=f2, fill=(255, 255, 255), anchor='mm')
    d.text((256, 414), 'evacuation will result in IMMEDIATE RECONTAINMENT', font=f2, fill=(255, 255, 255), anchor='mm')
    d.text((256, 470), 'VALID AT GATE V ONLY', font=f1, fill=(200, 210, 255), anchor='mm')
    im.save(os.path.join(ITEMS, 'keycardgatev.png'))
    return im


def warp(src, quad, size):
    """perspective-map the whole of src onto the quad (tl, tr, br, bl) of an image of `size`"""
    W, H = size
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = quad
    # solve the homography from the unit square to the quad
    A, B = [], []
    for (u, v), (x, y) in zip(((0, 0), (1, 0), (1, 1), (0, 1)), quad):
        A.append([u, v, 1, 0, 0, 0, -u * x, -v * x]); B.append(x)
        A.append([0, 0, 0, u, v, 1, -u * y, -v * y]); B.append(y)
    h = np.linalg.solve(np.array(A, float), np.array(B, float))
    Hm = np.linalg.inv(np.array([[h[0], h[1], h[2]], [h[3], h[4], h[5]], [h[6], h[7], 1.0]]))
    yy, xx = np.mgrid[0:H, 0:W].astype(float)
    pts = np.stack([xx.ravel() + 0.5, yy.ravel() + 0.5, np.ones(W * H)])
    uvw = Hm @ pts
    u, v = uvw[0] / uvw[2], uvw[1] / uvw[2]
    s = np.asarray(src, np.float32)
    sh, sw = s.shape[:2]
    inside = (u >= 0) & (u < 1) & (v >= 0) & (v < 1)
    out = np.zeros((H * W, 3), np.float32)
    out[inside] = s[(v[inside] * sh).astype(int), (u[inside] * sw).astype(int)]
    return Image.fromarray(out.reshape(H, W, 3).astype(np.uint8)), inside.reshape(H, W)


def icon(tex):
    S = 768                                                     # drawn large, scaled down (anti-aliased)
    card = tex
    quad = [(20, 150), (700, 40), (750, 560), (70, 720)]       # tilted, filling the frame, like the game's own icons
    face, mask = warp(card, quad, (S, S))
    out = Image.new('RGB', (S, S), (0, 0, 0))
    # the card's edge: a thin dark slab under the face
    edge = Image.new('RGB', (S, S), (0, 0, 0))
    ed = ImageDraw.Draw(edge)
    ed.polygon([(p[0] + 6, p[1] + 10) for p in quad], fill=(10, 10, 60))
    out.paste(edge, (0, 0))
    m = Image.fromarray((mask * 255).astype(np.uint8))
    # shade the face a little: lighter at the top left, as if lit from there
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    shade = np.clip(1.08 - (xx + yy) / (2.0 * S) * 0.22, 0.85, 1.08)[..., None]
    face = Image.fromarray(np.clip(np.asarray(face, np.float32) * shade, 0, 255).astype(np.uint8))
    out.paste(face, (0, 0), m)
    od = ImageDraw.Draw(out)
    od.line(quad + [quad[0]], fill=(200, 200, 220), width=3)    # a bright rim, as on the real icons
    out = out.resize((256, 256), Image.LANCZOS)
    out.save(os.path.join(ITEMS, 'INVkeygatev.png'))
    return out


if __name__ == '__main__':
    t = texture()
    icon(t)
    sheet = Image.new('RGB', (512 + 256, 512))
    sheet.paste(t, (0, 0))
    sheet.paste(Image.open(os.path.join(ITEMS, 'INVkeygatev.png')), (512, 0))
    sheet.save(os.path.join(ROOT, 'Tools', 'roomkit', 'previews', 'keygatev.png'))
    print('Gate V card: texture and icon written')
