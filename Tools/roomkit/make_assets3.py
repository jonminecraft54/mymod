"""Assets for the "sixteen SCPs" batch:
   GFX\\map\\indev_labels3.png (+ labels3.json)   the yellow door label for each of the 16 SCPs
   GFX\\map\\indev_plates3.png (+ plates3.json)   room name plates
   GFX\\map\\indev_*.png                           small material textures for the exhibits
   GFX\\npcs\\indev_text.jpg, indev_flat_*.jpg     skins: the Written Man, the Site 41 figures
   GFX\\items\\doc<number>.jpg                     one document per SCP (own wording, after the wiki articles)
"""
import json
import math
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from make_docs2 import typed

ROOT = r"I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9"
MAPDIR = os.path.join(ROOT, 'GFX', 'map')
NPCDIR = os.path.join(ROOT, 'GFX', 'npcs')
F = r"C:\Windows\Fonts"

SCPS = [('1045', 'SAFE'), ('1110', 'EUCLID'), ('1125', 'EUCLID'), ('1250', 'SAFE'),
        ('1312', 'SAFE'), ('1313', 'KETER'), ('1510', 'SAFE'), ('1511', 'EUCLID'),
        ('1512', 'KETER'), ('1513', 'SAFE'), ('1514', 'KETER'), ('1515', 'EUCLID'),
        ('1516', 'EUCLID'), ('1517', 'EUCLID'), ('1518', 'KETER'), ('1519', 'SAFE')]
CLS = {'SAFE': (30, 120, 40), 'EUCLID': (200, 130, 20), 'KETER': (180, 24, 20)}


def font(sz):
    return ImageFont.truetype(os.path.join(F, 'arialbd.ttf'), sz)


def wear(im, seed):
    W, H = im.size
    a = np.asarray(im).astype(np.float64)
    rng = np.random.default_rng(seed)
    sm = np.asarray(Image.fromarray((rng.random((H // 8, W // 8)) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)
                    .filter(ImageFilter.GaussianBlur(6))).astype(np.float64) / 255.0
    a = a * (0.80 + 0.28 * sm[..., None]) + rng.normal(0, 8, (H, W))[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.5))


def labels():
    W = H = 1024
    im = Image.new('RGB', (W, H), (20, 20, 20))
    d = ImageDraw.Draw(im)
    rects = {}
    for i, (num, cls) in enumerate(SCPS):
        x, y = (i % 4) * 256, (i // 4) * 256
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
    wear(im, 31).save(os.path.join(MAPDIR, 'indev_labels3.png'))
    json.dump(rects, open('labels3.json', 'w'), indent=1)


def plates():
    W, H = 1024, 512
    im = Image.new('RGB', (W, H), (20, 20, 20))
    d = ImageDraw.Draw(im)
    rects = {}
    names = [('siv', 'SMALL ITEMS VAULT'), ('bio', 'BIOLOGICAL HOLDING'), ('review', 'SURVEILLANCE REVIEW'),
             ('site41', 'SITE 41 - NO ENTRY'), ('lecture', 'LECTURE ROOM 2'), ('origin', 'PROCEDURE 1512-ALPHA'),
             ('cell49', 'HUMANOID CELL 49'), ('vault', 'VAULT 117'), ('bunker', 'SECURE BUNKER'), ('purge', 'FAN PURGE')]
    for i, (key, text) in enumerate(names):
        x, y = (i % 2) * 512, (i // 2) * 102
        rects[key] = (x / W, y / H, (x + 512) / W, (y + 102) / H)
        yellow = key in ('site41', 'origin', 'purge')
        d.rectangle([x, y, x + 511, y + 101], fill=(22, 22, 22))
        d.rectangle([x + 3, y + 3, x + 508, y + 98], outline=(120, 110, 40) if yellow else (120, 120, 120), width=4)
        sz = 60
        while d.textlength(text, font=font(sz)) > 470:
            sz -= 2
        d.text((x + 256, y + 51), text, font=font(sz), fill=(232, 196, 28) if yellow else (235, 233, 226), anchor='mm')
    wear(im, 32).save(os.path.join(MAPDIR, 'indev_plates3.png'))
    json.dump(rects, open('plates3.json', 'w'), indent=1)


def mottle(name, base, var, seed, size=128, sigma=3.0, folder=MAPDIR):
    rng = np.random.default_rng(seed)
    n = np.asarray(Image.fromarray((rng.random((size, size)) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(sigma))).astype(float) / 255.0
    a = np.array(base, dtype=float)[None, None, :] + (n[..., None] - 0.5) * 2 * np.array(var, dtype=float)[None, None, :]
    a += rng.normal(0, 4, (size, size, 1))
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(os.path.join(folder, name))


def textures():
    mottle('indev_bronze.png', (150, 104, 48), (60, 46, 26), 1)
    mottle('indev_leaf.png', (58, 122, 46), (34, 50, 26), 2)
    mottle('indev_flesh.png', (168, 96, 84), (46, 36, 30), 3)
    mottle('indev_foam.png', (206, 196, 150), (22, 22, 20), 4, sigma=1.5)
    mottle('indev_root.png', (112, 54, 40), (44, 26, 20), 5, sigma=4.0)
    mottle('indev_soil.png', (66, 48, 34), (26, 20, 16), 6, sigma=1.5)
    # candy: bright spheres on white frost
    rng = np.random.default_rng(7)
    im = Image.new('RGB', (128, 128), (226, 234, 240))
    d = ImageDraw.Draw(im)
    cols = [(220, 40, 60), (250, 200, 40), (60, 170, 80), (70, 110, 220), (240, 120, 30), (200, 70, 200)]
    for _ in range(26):
        x, y, r = rng.integers(6, 122), rng.integers(6, 122), rng.integers(7, 12)
        c = cols[rng.integers(0, len(cols))]
        d.ellipse([x - r, y - r, x + r, y + r], fill=c)
        d.ellipse([x - r // 2, y - r // 2, x - r // 5, y - r // 5], fill=(255, 255, 255))
    im.save(os.path.join(MAPDIR, 'indev_candy.png'))
    # dice / card faces
    im = Image.new('RGB', (256, 128), (232, 200, 60))
    d = ImageDraw.Draw(im)
    for i, wd in enumerate(('Yes', 'No', 'Maybe')):
        d.rectangle([i * 85 + 2, 2, i * 85 + 82, 82], outline=(60, 50, 20), width=3)
        d.text((i * 85 + 42, 42), wd, font=font(24 if wd != 'Maybe' else 18), fill=(40, 34, 20), anchor='mm')
    d.rectangle([0, 86, 255, 127], fill=(238, 236, 228))
    d.text((128, 106), "They'll make up your mind!", font=font(15), fill=(190, 28, 24), anchor='mm')
    im.save(os.path.join(MAPDIR, 'indev_dice.png'))
    # soap bubble (alpha sprite)
    S = 128
    yy, xx = np.mgrid[0:S, 0:S]
    r = np.sqrt((xx - 64) ** 2 + (yy - 64) ** 2) / 60.0
    rim = np.exp(-((r - 0.92) / 0.07) ** 2)
    body = np.clip(1 - r, 0, 1) ** 0.4 * 0.16 * (r < 1)
    hl = np.exp(-(((xx - 44) ** 2 + (yy - 40) ** 2) / 140.0))
    al = np.clip(rim * 0.85 + body + hl * 0.8, 0, 1) * (r < 1.06)
    rgba = np.zeros((S, S, 4), dtype=np.uint8)
    rgba[..., 0] = np.clip(200 + 55 * np.sin(xx / 9.0), 0, 255)
    rgba[..., 1] = np.clip(220 + 35 * np.sin(yy / 7.0), 0, 255)
    rgba[..., 2] = 255
    rgba[..., 3] = (al * 255).astype(np.uint8)
    Image.fromarray(rgba).save(os.path.join(MAPDIR, 'indev_bubble.png'))
    # skins: the Written Man is nothing but words; the Site 41 figures are one flat colour each
    W = 1024
    im = Image.new('RGB', (W, W), (236, 232, 222))
    d = ImageDraw.Draw(im)
    words = ['brazo', 'mano', 'pierna', 'pecho', 'cara', 'ojo', 'boca', 'pie', 'dedo', 'cuello', 'espalda', 'hombro', 'rodilla', 'piel']
    rng = np.random.default_rng(1516)
    y = 0
    while y < W:
        x = -int(rng.integers(0, 60))
        sz = int(rng.integers(16, 30))
        f = ImageFont.truetype(os.path.join(F, 'times.ttf' if os.path.exists(os.path.join(F, 'times.ttf')) else 'arial.ttf'), sz)
        while x < W:
            wd = words[int(rng.integers(0, len(words)))]
            d.text((x, y), wd, font=f, fill=(24, 22, 20))
            x += int(d.textlength(wd + ' ', font=f))
        y += sz + 2
    im.save(os.path.join(NPCDIR, 'indev_text.jpg'), quality=90)
    for nm, c in (('white', (232, 232, 228)), ('black', (16, 16, 18)), ('orange', (226, 120, 30))):
        Image.new('RGB', (64, 64), c).save(os.path.join(NPCDIR, 'indev_flat_%s.jpg' % nm), quality=92)


def textures2():
    """Textures the room meshes and the game code use for the exhibits themselves."""
    mottle('indev_stone.png', (188, 180, 160), (30, 28, 26), 11, sigma=2.5)
    mottle('indev_waxpaper.png', (226, 206, 160), (16, 16, 18), 12, sigma=5.0)
    mottle('indev_terracotta.png', (170, 96, 60), (24, 16, 12), 17, sigma=2.0)
    mottle('indev_bear.png', (52, 36, 24), (20, 14, 10), 13, sigma=1.2, folder=NPCDIR)
    mottle('indev_rodent.png', (150, 118, 80), (30, 24, 18), 14, sigma=1.2, folder=NPCDIR)
    mottle('indev_petleaf.png', (70, 136, 50), (36, 46, 24), 15, sigma=1.6, folder=NPCDIR)
    mottle('indev_petstem.png', (96, 84, 44), (26, 24, 16), 16, sigma=1.6, folder=NPCDIR)
    # crystal: pale facets
    rng = np.random.default_rng(21)
    im = Image.new('RGB', (128, 128), (150, 200, 230))
    d = ImageDraw.Draw(im)
    for _ in range(40):
        p = [(int(rng.integers(0, 128)), int(rng.integers(0, 128))) for _ in range(3)]
        v = int(rng.integers(-40, 40))
        d.polygon(p, fill=(170 + v, 215 + v // 2, 240 + v // 4))
    im.filter(ImageFilter.GaussianBlur(0.8)).save(os.path.join(MAPDIR, 'indev_crystal.png'))
    # slime: grey, glossy, with holes (alpha)
    S = 256
    n = np.asarray(Image.fromarray((rng.random((S, S)) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(9))).astype(float)
    n = (n - n.min()) / (n.max() - n.min())
    g = np.asarray(Image.fromarray((rng.random((S, S)) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2))).astype(float) / 255.0
    yy, xx = np.mgrid[0:S, 0:S]
    edge = np.minimum.reduce([xx, yy, S - 1 - xx, S - 1 - yy]) / 28.0
    al = np.clip((n - 0.34) * 5.0, 0, 1) * np.clip(edge, 0, 1)
    rgba = np.zeros((S, S, 4), dtype=np.uint8)
    rgba[..., 0] = np.clip(112 + 60 * g, 0, 255)
    rgba[..., 1] = np.clip(116 + 60 * g, 0, 255)
    rgba[..., 2] = np.clip(108 + 56 * g, 0, 255)
    rgba[..., 3] = (al * 215).astype(np.uint8)
    Image.fromarray(rgba).save(os.path.join(MAPDIR, 'indev_slime.png'))
    # the board in Lecture Room 2: ordinary algebra with the last lines wiped
    im = Image.new('RGB', (512, 256), (240, 242, 238))
    d = ImageDraw.Draw(im)
    hand = ImageFont.truetype(os.path.join(F, 'segoesc.ttf'), 22)
    lines = ['let  x = 3a - 7,   y = a(b + 2)', '4x - 2(y - 9) = 5b + a', '12a - 28 - 2ab - 4a + 18 = 5b + a',
             '7a - 2ab - 5b = 10', 'a(7 - 2b) = 10 + 5b', 'a = ']
    for i, t in enumerate(lines):
        d.text((26, 14 + i * 36), t, font=hand, fill=(24, 40, 120))
    sm = Image.new('L', (512, 256), 0)
    ds = ImageDraw.Draw(sm)
    ds.ellipse([120, 170, 500, 250], fill=200)
    sm = sm.filter(ImageFilter.GaussianBlur(14))
    im = Image.composite(Image.new('RGB', (512, 256), (226, 228, 226)), im, sm)
    d = ImageDraw.Draw(im)
    d.text((300, 216), 'DO NOT FINISH', font=font(22), fill=(190, 28, 24))
    d.rectangle([0, 0, 511, 255], outline=(120, 120, 120), width=6)
    im.save(os.path.join(MAPDIR, 'indev_board1313.png'))
    # the three word cards of Cell 49
    im = Image.new('RGB', (384, 128), (238, 234, 222))
    d = ImageDraw.Draw(im)
    tf = ImageFont.truetype(os.path.join(F, 'times.ttf'), 46)
    for i, wd in enumerate(('PAN', 'VENDA', 'PILA')):
        d.rectangle([i * 128 + 3, 3, i * 128 + 124, 124], outline=(90, 90, 90), width=3)
        d.text((i * 128 + 64, 64), wd, font=tf if wd != 'VENDA' else ImageFont.truetype(os.path.join(F, 'times.ttf'), 36),
               fill=(20, 20, 20), anchor='mm')
    im.save(os.path.join(MAPDIR, 'indev_cards.png'))
    # furniture SCP-1516 has made: the same words as its skin, as a wall / furniture texture
    Image.open(os.path.join(NPCDIR, 'indev_text.jpg')).resize((512, 512), Image.LANCZOS).save(os.path.join(MAPDIR, 'indev_words.jpg'), quality=90)
    # an ash-grey unlabelled cassette
    im = Image.new('RGB', (128, 64), (128, 128, 126))
    d = ImageDraw.Draw(im)
    d.rectangle([2, 2, 125, 61], outline=(70, 70, 70), width=2)
    d.rectangle([24, 16, 104, 44], fill=(96, 96, 96), outline=(60, 60, 60))
    for cx in (46, 82):
        d.ellipse([cx - 9, 21, cx + 9, 39], fill=(40, 40, 40))
    wear(im, 33).save(os.path.join(MAPDIR, 'indev_tape.png'))


def docs():
    typed('doc1045', [('Clearance Level', '1'), ('Item #', 'SCP-1045'), ('Object Class', 'Safe')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'SCP-1045 is kept in the Small Items Vault. No open flame is brought within 5 m of it except to test it.'),
        ('h', 'Description:'),
        ('p', 'SCP-1045 is a square wooden candle lantern, 15 x 15 x 32 cm, with sides of waxed paper round a glass cup. '
              'When a candle burns in it, each side shows the shadow of a small human figure from a different angle, '
              'writhing as if in the flame. It moves faster as the candle burns down.'),
        ('p', 'Whatever the candle was made of, the residue is rendered human fat.'),
        ('h', 'Note:'),
        ('p', 'A stub of scented candle has been left in the cup. Scented candles give the shadow a voice. '
              '{Lighting it costs you your nerve and gains you nothing.}'),
    ])
    typed('doc1110', [('Clearance Level', '2'), ('Item #', 'SCP-1110'), ('Object Class', 'Euclid')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'Footage of SCP-1110 is confiscated and reviewed only in the Surveillance Review room. Losses are made good from Foundation funds.'),
        ('h', 'Description:'),
        ('p', 'SCP-1110 is a robbery that happens only on camera. Two figures with covered faces - one in a grey hood, one '
              'in a skull-like mask - are seen holding up a counter and leaving with a case. Nobody present sees, '
              'hears or feels them. Afterwards what the recording showed being taken is missing.'),
        ('h', 'Note for this room:'),
        ('p', 'The review monitor is wired to the camera over the property counter. {Whatever is lying on that counter '
              'when the footage is played will be gone when it ends.} Take what you need first, or do not press play.'),
    ])
    typed('doc1125', [('Clearance Level', '2'), ('Item #', 'SCP-1125'), ('Object Class', 'Euclid')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'Specimens stay in opaque crates in the Small Items Vault. Nobody touches one with bare skin.'),
        ('h', 'Description:'),
        ('p', 'SCP-1125 is a yellow wooden die whose faces read Yes, No and Maybe, sold in a blister pack marked '
              '"The Factory". Anyone who touches it feels they must ask it a yes-or-no question and roll. On Maybe they '
              'roll again. They then do what it says.'),
        ('p', 'Use grows. Subjects end by being unable to decide anything without it, and resist having it taken away.'),
        ('h', 'Note:'),
        ('p', 'One die is out of its pack on the table. A Yes steadies you. A No takes your wind. {Every roll makes the '
              'next one harder to refuse - three is too many.}'),
    ])
    typed('doc1250', [('Clearance Level', '3'), ('Item #', 'SCP-1250'), ('Object Class', 'Safe')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'Blank tapes are kept in a double-locked safe. Used tapes are labelled and filed, and may be played by any permitted staff.'),
        ('h', 'Description:'),
        ('p', 'SCP-1250 is a stock of ash-grey audio cassettes and video tapes with no markings. They record normally, '
              'but what plays back is not quite what happened: a word, a piece of furniture, sometimes who was in the '
              'room. Date, time and place are always right. The tapes are thought to record a neighbouring course of events.'),
        ('h', 'Note:'),
        ('p', 'The deck on the desk is loaded with a tape recorded in this corridor system today. {It will tell you how '
              'near the sculpture is. About one time in three it is describing somewhere that is not quite here.}'),
    ])
    typed('doc1312', [('Clearance Level', '3'), ('Item #', 'SCP-1312'), ('Object Class', 'Safe')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'SCP-1312 is held behind a 2 m electric fence. Every exit is guarded. Nothing and nobody goes in without authorisation.'),
        ('h', 'Description:'),
        ('p', 'SCP-1312 is the unfinished Site 41, which moved three kilometres north during construction with its staff inside. '
              'It is now staffed by featureless figures of one flat colour each.'),
        ('b', '- White ones direct tests and write reports about whatever has been caught.'),
        ('b', '- Black ones catch it. They can say one thing: "containment breach".'),
        ('b', '- Orange ones do as the white ones signal.'),
        ('p', 'They are docile until they notice something that does not belong. Then they contain it.'),
        ('h', 'Note:'),
        ('p', 'This annex holds a section of Site 41 that came with the rest. {Past the fence you are the anomaly. '
              'If the black one reaches you, you will sit in their cell until they lose interest.}'),
    ])
    typed('doc1313', [('Clearance Level', '4'), ('Item #', 'SCP-1313'), ('Object Class', 'Keter')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'SCP-1313 is not contained. No member of staff may know the whole problem. Schools are watched for bear attacks.'),
        ('h', 'Description:'),
        ('p', 'SCP-1313 is a sequence of ordinary algebra whose answer is not a number but one adult female grizzly bear, '
              'usually angry. It need not be written down: following every step in your head to the end is enough, and '
              'the bear appears in or near whoever finished.'),
        ('p', 'Skipping steps does nothing. Solving the inverse does not put the bear back.'),
        ('h', 'Note:'),
        ('p', 'Lecture Room 2 was sealed with most of it still on the board. {Do not stand and work it through.} If you '
              'do, the lights will go and you will not be alone: leave the room at once.'),
    ])
    typed('doc1510', [('Clearance Level', '2'), ('Item #', 'SCP-1510'), ('Object Class', 'Safe')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'SCP-1510 is kept dry and cool in the Small Items Vault, polished and checked for rust every two weeks.'),
        ('h', 'Description:'),
        ('p', 'SCP-1510 is a bronze Roman infantry helmet of about 107 BCE. Worn by a man of 28 to 35 it brings out '
              'SCP-1510-1, who gives his name as Publius Carthephilus Aetius, a legionary under Gaius Marius, and speaks '
              'classical Latin. The wearer remembers nothing of the time the helmet was on.'),
        ('p', 'He was violent at first. He has been cooperative since the seventh interview.'),
        ('h', 'Note:'),
        ('p', 'Put it on and you lose some seconds you will not get back. {He is a soldier: he binds wounds before he '
              'does anything else.} You wake tired, with your nerves in rags.'),
    ])
    typed('doc1511', [('Clearance Level', '2'), ('Item #', 'SCP-1511'), ('Object Class', 'Euclid')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'Outposts watch both ends of the route. Each new object is numbered, tagged and recorded until it leaves.'),
        ('h', 'Description:'),
        ('p', 'SCP-1511 are crystalline objects four to six metres tall that appear at one point, float 1,630 km along '
              'a fixed route and vanish at the other end. Stone figures circle each one. When an object settles to the '
              'ground the figures come to life, tend it, and speak - each of an afterlife of its own, about to begin.'),
        ('p', 'One object was found wrecked. It gave out glass tablets calling itself a prison vessel.'),
        ('h', 'Note:'),
        ('p', 'The piece on the plinth is from one of the broken figures. It still speaks. {Listening to it is restful.} '
              'Now and then it says something else.'),
    ])
    typed('doc1512', [('Clearance Level', '4'), ('Item #', 'SCP-1512'), ('Object Class', 'Keter')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'Procedure 1512-Alpha runs without a break: staff compute the topology of the point of origin by hand, in '
              'real time, {while not believing the result.} Speed and accuracy slow the growth. Machines do not work.'),
        ('h', 'Description:'),
        ('p', 'SCP-1512 is a root-like mass of red-brown tendrils three to five centimetres thick, weighing more than '
              '80,000 tonnes. It grows whenever the procedure lapses. The tendrils ooze a grey slime that burns skin and '
              'leaves anyone who touches it dizzy and lost.'),
        ('h', 'Note:'),
        ('p', 'A tendril has come up through this hall and laid slime across the floor. There is a worksheet at each end. '
              '{Hold the pencil to the sheet until the working is done and the slime draws back for about a minute.} Cross then.'),
    ])
    typed('doc1513', [('Clearance Level', '1'), ('Item #', 'SCP-1513'), ('Object Class', 'Safe')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'Grown instances live in observation units floored with soil, changed every 14 days. The packet stays in a locker.'),
        ('h', 'Description:'),
        ('p', 'SCP-1513 is a plastic packet of about eleven sunflower seeds marked GROW-A-PET. A planted seed grows '
              'whether or not it is watered. Cared for, it takes the shape of a cat or dog over one to four weeks, then '
              'comes to life: rooted to the spot, friendly, reaching for anyone who comes near.'),
        ('p', 'Left without light and water it grows a hard stem, pulls itself out of the pot and keeps away from people.'),
        ('h', 'Note:'),
        ('p', 'The one in the middle pot was looked after. {It likes being stroked, and so will you.} The one that was '
              'not looked after is somewhere in this room.'),
    ])
    typed('doc1514', [('Clearance Level', '4'), ('Item #', 'SCP-1514'), ('Object Class', 'Keter')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'One qualified member of staff inspects SCP-1514-1A every 20 minutes. {Nobody tampers with it. Anything '
              'beyond a routine inspection is met with immediate termination.}'),
        ('h', 'Description:'),
        ('p', 'SCP-1514 is a 1983 nuclear deterrent hidden behind the Strategic Defense Initiative. SCP-1514-1A is a '
              'steel unit 1.5 x 0.9 x 0.6 m whose dials show the condition of something kept alive inside it in a dark '
              'red fluid. Once an hour it signals a ring of armed satellites, SCP-1514-2.'),
        ('p', 'If the signal ever stops, the satellites act.'),
        ('h', 'Note:'),
        ('p', 'The inspection is overdue and the alarm is sounding. A touch on the panel logs it. Do not hold on.'),
    ])
    typed('doc1515', [('Clearance Level', '2'), ('Item #', 'SCP-1515'), ('Object Class', 'Euclid')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'The known population is kept on a reserve near Alice Springs. The specimens here are held in a wire '
              'enclosure for study. Any found outside the perimeter are destroyed.'),
        ('h', 'Description:'),
        ('p', 'SCP-1515 is a rodent like a springhare, with longer claws and larger teeth. It hunts in fives, and only '
              'one kind of prey: a mammal early in pregnancy. It takes the unborn young, stitches itself a pouch and '
              'carries it there. The young never survives and neither, often, does the rodent. No reason for the '
              'behaviour has been found.'),
        ('h', 'Note:'),
        ('p', '{They have no interest in you.} They will chirp, which is how a hunt begins. That is all it is.'),
    ])
    typed('doc1516', [('Clearance Level', '3'), ('Item #', 'SCP-1516'), ('Object Class', 'Euclid')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'SCP-1516 lives in a humanoid cell furnished with things it has made. It is fed written words for food. '
              'It is never given a word for anything harmful.'),
        ('h', 'Description:'),
        ('p', 'SCP-1516 is a living figure 1.9 m tall made entirely of printed Spanish words, each part of the body '
              'being the word for that part. It makes no sound: the noise appears as words in the air. When it touches a '
              'single written noun, the word lifts off the paper and becomes the thing - if it understands the thing.'),
        ('h', 'Note:'),
        ('p', 'Three cards are on the desk: PAN, VENDA, PILA. {Pass it one and take what comes back through the tray. '
              'It will only do this once for you.}'),
    ])
    typed('doc1517', [('Clearance Level', '3'), ('Item #', 'SCP-1517'), ('Object Class', 'Euclid')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'All specimens and egg cases are kept frozen. Remains of anyone infected are burned.'),
        ('h', 'Description:'),
        ('p', 'SCP-1517 is an insect like a brightly coloured cicada. Its eggs come in hard sugar spheres about 3 cm '
              'across that look like sweets, some hundreds to a sphere. When the shell breaks the nymphs go for the '
              'nearest living tissue, eat it and turn it into confectionery. They numb what they eat. The victim feels nothing.'),
        ('p', 'It was found in the back room of a sweet shop.'),
        ('h', 'Note:'),
        ('p', 'The freezer door has been left ajar. {Shut it before they thaw.} They are not gobstoppers. Do not put one in your mouth.'),
    ])
    typed('doc1518', [('Clearance Level', '4'), ('Item #', 'SCP-1518'), ('Object Class', 'Keter')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'SCP-1518 sits in a foam shell in a foam-lined vault. Shells are rotated every three hours; {fans drive '
              'loose bubbles into the walls.} No water within 10 m. It is never moved across water.'),
        ('h', 'Description:'),
        ('p', 'SCP-1518 is a dead limestone fountain 1.8 m tall, full of something like water that cannot be spilled. '
              'It lets go of bubbles that never burst. A bubble that meets a solid shrinks and takes an equal volume of '
              'the solid with it. One that meets liquid swallows it and grows. A body is mostly liquid.'),
        ('h', 'Note:'),
        ('p', 'Several are loose in this hall. {Press FAN PURGE at either end: for half a minute the fans pin them to '
              'the east wall.} Walk through then. Do not let one touch you.'),
    ])
    typed('doc1519', [('Clearance Level', '2'), ('Item #', 'SCP-1519'), ('Object Class', 'Safe')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'The original is kept in a 30-litre tank of saline and fed three times a day. Copies are built for tests and destroyed after.'),
        ('h', 'Description:'),
        ('p', 'SCP-1519 is a cylinder of about half a kilogram made from twenty pieces of human tissue round a single '
              'heart, with a ring of teeth at each end. Fed, it gives off electric current, and its ends will seal '
              'themselves onto almost any device that wants power. A Florentine note of about 1500 calls them lamplighters.'),
        ('p', 'One built from human parts runs for about four years.'),
        ('h', 'Note:'),
        ('p', 'The cradle beside the tank charges a cell in about three minutes. {Press the cradle and take what it has made.}'),
    ])


if __name__ == '__main__':
    os.makedirs('out', exist_ok=True)
    labels()
    plates()
    textures()
    textures2()
    docs()
    print('assets + 16 documents written')
