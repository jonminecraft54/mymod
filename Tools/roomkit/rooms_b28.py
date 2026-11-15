"""The twenty-eighth batch: SCP-983, the birthday monkey. Code in IndevU28.bb; models and candies in make_scp983.py.
SCP text summarised from scp-wiki.wikidot.com/scp-983 (CC BY-SA 3.0); room and art are our own.

  room2b28monkey  LCZ  SCP-983's containment chamber in the style of the user's storage-room image (white walls, a
                       black ceiling, a dark floor, the banner and the red poster, white shelving and benches): the
                       monkey on a pedestal, Emergency Kit 135r on the wall by the door (the sing-along guidelines),
                       a board of today's personnel birthdays, and a sample case of collected candies."""
from rooms_b27 import *

KIT = Mat('indev_983kit.png', cast=False)
BOARD = Mat('indev_983board.png', cast=False)


def assets():
    from PIL import Image, ImageDraw, ImageFont
    F = r'C:\Windows\Fonts\arialbd.ttf'
    im = Image.new('RGB', (256, 320), (190, 30, 30))
    d = ImageDraw.Draw(im)
    d.rectangle([10, 10, 246, 310], outline=(240, 240, 240), width=6)
    d.text((128, 70), 'EMERGENCY', font=ImageFont.truetype(F, 34), fill=(255, 255, 255), anchor='mm')
    d.text((128, 115), 'KIT 135r', font=ImageFont.truetype(F, 40), fill=(255, 255, 255), anchor='mm')
    d.rectangle([60, 160, 196, 230], fill=(240, 240, 240))
    d.text((128, 195), 'SING-ALONG', font=ImageFont.truetype(F, 20), fill=(190, 30, 30), anchor='mm')
    d.text((128, 270), 'BREAK GLASS ON YOUR BIRTHDAY', font=ImageFont.truetype(F, 13), fill=(255, 230, 230), anchor='mm')
    im.save(os.path.join(MAPDIR, 'indev_983kit.png'))
    im = Image.new('RGB', (384, 256), (60, 70, 60))
    d = ImageDraw.Draw(im)
    d.rectangle([8, 8, 376, 248], outline=(150, 120, 80), width=10)
    d.text((192, 50), 'BIRTHDAYS TODAY', font=ImageFont.truetype(F, 32), fill=(240, 240, 230), anchor='mm')
    d.text((192, 110), 'Check this board before', font=ImageFont.truetype(F, 22), fill=(220, 220, 210), anchor='mm')
    d.text((192, 140), 'handling SCP-983.', font=ImageFont.truetype(F, 22), fill=(220, 220, 210), anchor='mm')
    d.text((192, 200), '(see the duty officer)', font=ImageFont.truetype(F, 18), fill=(180, 190, 180), anchor='mm')
    im.save(os.path.join(MAPDIR, 'indev_983board.png'))


assets()


def room2b28monkey():
    R = R_('room2b28monkey', amb=10)
    junction(R, 'NS', 'store27', openings={'hubE': [door_op(0)]})
    for z in (-600.0, 600.0):
        ceil_light(R, 0, z, 384, size=40, power=55, rng=700)
    # the chamber
    side(R, 192, +1, 'store27', h=352, depth=560)
    R.box(520, 0, -70, 660, 100, 70, CONC, skip='B', lux=10)                 # the pedestal
    R.box(510, 100, -80, 670, 108, 80, DARK, skip='B', top=Mat('indev_3008fabric.png', 128), lux=10)
    named(R, 'MONKEY', 590, 150, 0)                                         # its chest: where you look to pick it up
    shelving(R, 760, -330, 816, -190)
    shelving(R, 760, 190, 816, 330)
    wall_decal(R, POSTER24, 816, 0, 'W', 80, 110, 220)
    wall_decal(R, BANNER, 520, -400, 'N', 320, 112, 230)
    bench(R, 320, 330, 700, 390)
    wall_decal(R, KIT, 300, -400, 'N', 70, 88, 160)                          # Emergency Kit 135r, by the door
    named(R, 'KIT', 300, 150, -380)
    wall_decal(R, BOARD, 470, 400, 'S', 160, 106, 200)                       # today's birthdays
    named(R, 'BOARD', 470, 190, 380)
    R.box(600, 78, 345, 700, 110, 375, GLASS, lux=10)                        # the candy sample case on the bench
    named(R, 'CASE', 650, 100, 360)
    ceil_light(R, 590, 0, 352, size=40, power=70, rng=640, color=(255, 246, 228))
    ceil_light(R, 360, 250, 352, size=34, power=50, rng=560, color=(250, 248, 240))
    item(R, 'doc983', 400, 78, 360)
    item(R, 'doc135r', 330, 78, 345)
    return (R, 'MKY', 'SCP-983 (Light Containment): the birthday monkey on its pedestal, Emergency Kit 135r by the door, and a board of today\'s birthdays.',
            1, 0.55, ((330, 165, 0), (590, 130, 0)))


ALL = [room2b28monkey]
