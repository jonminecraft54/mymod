"""room1newscproom rebuilt: the SCP storage cells of SCP-963, SCP-109 and SCP-2295.

The old hand-made mesh was unfinished: skewed walls, cells with no doors, door signs reading SCP-1025 and SCP-860,
almost no light, and SCP-109's cell beyond the room's own grid cell (over the next room). This builds the same room
(a dead end, entered from the south) with the room kit: a lit hall, three cells behind doors - SCP-963 west, SCP-2295
east, SCP-109 north - each with a pedestal, a lamp and a proper plate. The items keep their spots (IndevFill963,
IndevFill109; 109's moved into its new cell) and the doors are made in IndevFill963 (Indev963.bb).
   python room_scpstorage.py --game"""
import json
import os
import sys
from PIL import Image, ImageDraw, ImageFont
from rooms_b26 import *

PL = [('963', 'SCP-963'), ('109', 'SCP-109'), ('2295', 'SCP-2295'), ('store', 'SCP STORAGE'), ('safe', 'SAFE-CLASS')]


def plates():
    W = H = 512
    im = Image.new('RGB', (W, H), (24, 24, 24))
    d = ImageDraw.Draw(im)
    rects = {}
    for i, (k, text) in enumerate(PL):
        x, y = (i % 3) * 170, (i // 3) * 128
        rects[k] = (x / W, y / H, min(x + 168, W) / W, min(y + 124, H) / H)
        d.rectangle([x + 4, y + 4, x + 164, y + 120], fill=(20, 20, 20), outline=(170, 170, 170), width=4)
        size = 40
        while d.textlength(text, font=ImageFont.truetype(r'C:\Windows\Fonts\arialbd.ttf', size)) > 146:
            size -= 2
        d.text((x + 84, y + 62), text, font=ImageFont.truetype(r'C:\Windows\Fonts\arialbd.ttf', size), fill=(235, 235, 230), anchor='mm')
    im.save(os.path.join(MAPDIR, 'indev_scpstore_plates.png'))
    return rects


RECTS = plates()
PLS = Mat('indev_scpstore_plates.png', cast=False)


def plate(R, k, cx, cz, facing, yc=260, w=120):
    wall_decal(R, PLS, cx, cz, facing, w, w * 0.74, yc, uv=RECTS[k])


def pedestal(R, x, z, top, mat=CONC):
    R.box(x - 60, 0, z - 60, x + 60, top - 12, z + 60, mat, skip='B', lux=10)
    R.box(x - 70, top - 12, z - 70, x + 70, top, z + 70, METAL, skip='B', top=DARK, lux=10)   # the padded plate


def room1newscproom():
    R = Room('room1newscproom', luxel=6.0, ambient=11, fill=0.16)
    hub = (-448.0, -320.0, 448.0, 640.0)
    junction(R, 'S', 'store', hub=hub, hh=384,
             openings={'hubW': [door_op(376)], 'hubE': [door_op(320)], 'hubN': [door_op(0)]})
    # west: SCP-963 (the amulet on its padded pedestal)
    annex(R, 'x', -448, -1, 96, 656, 480, 352, 'store', door=376, spawn_door=False)
    pedestal(R, -752, 376, 175)
    plate(R, '963', -448, 376 + 150, 'E', yc=260, w=110)
    ceil_light(R, -752, 376, 352, size=34, power=60, rng=560, color=(255, 240, 220))
    # east: SCP-2295 (the bear in its toy chest)
    annex(R, 'x', 448, +1, 40, 600, 480, 352, 'store', door=320, spawn_door=False)
    R.box(694, 0, 259, 814, 160, 379, WOOD, skip='B', top=Mat('indev_3008fabric.png', 128), lux=10)
    plate(R, '2295', 448, 320 + 150, 'W', yc=260, w=110)
    ceil_light(R, 754, 320, 352, size=34, power=60, rng=560, color=(255, 236, 210))
    # north: SCP-109 (the canteen on a pedestal)
    annex(R, 'z', 640, +1, -300, 300, 320, 352, 'store', door=0, spawn_door=False)
    pedestal(R, 0, 880, 185)
    plate(R, '109', 150, 640, 'S', yc=260, w=110)
    ceil_light(R, 0, 880, 352, size=34, power=60, rng=560, color=(240, 246, 255))
    # the hall
    plate(R, 'store', -448, -100, 'E', yc=300, w=180)
    plate(R, 'safe', 448, -100, 'W', yc=300, w=180)
    for z in (-150.0, 350.0):
        ceil_light(R, 0, z, 384, size=44, power=70, rng=760, color=(255, 246, 232))
    R.box(-440, 0, -300, -380, 200, -140, CABINET, skip='B', lux=10)              # a filing cabinet by the door
    return R


if __name__ == '__main__':
    R = room1newscproom()
    R.bake(verbose=False, max_size=2048)
    out = MAPDIR if '--game' in sys.argv else 'out'
    R.export(out)
    R.render((0, 165, -700), (0, 140, 600), 'out/scpstore.png', size=(768, 432))
    R.render((-200, 165, 376), (-752, 150, 376), 'out/scpstore_963.png', size=(768, 432))
    print('room1newscproom rebuilt ->', out)
