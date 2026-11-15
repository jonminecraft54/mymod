"""The twenty-second batch: SCP-112-PT ("Santa Claus's bones"), a Christmas containment room. Code in IndevU22.bb.
The SCP text is a short summary of the SCP Foundation Portuguese branch article (scp-pt-br.wikidot.com/scp-112-pt,
CC BY-SA 3.0); geometry and textures are our own.

  room2b22xmas  LCZ  a pillared corridor (image 24); east, the reliquary chamber: a stone reliquary with the bones in
                     a bishop's robe under glass, a decorated tree, presents and coloured lights. The spirit,
                     SCP-112-PT-1, manifests by the reliquary, talks, leaves a gift and fades after two minutes."""
from rooms_b21 import *

ROBE = Mat('indev_112robe.png', 128)                 # made by make_assets22.py
GIFTR = Mat('indev_112giftr.png', 64)
GIFTG = Mat('indev_112giftg.png', 64)
STONE = Mat('Old_Whitewall.jpg', 256)


def tree(R, x, z):
    R.tube((x, 0, z), (x, 60, z), 12, WOOD, sides=8, caps=True)
    for k, (r, y0) in enumerate(((110, 60), (85, 140), (60, 210), (34, 270))):
        R.prism(octo(x, z, r), y0, y0 + 90 - k * 10, GREEN, caps='TB')
    R.box(x - 10, 350, z - 10, x + 10, 372, z + 10, Mat('indev_3008yellow.png', 256), lux=10)   # the star


def room2b22xmas():
    R = R_('room2b22xmas', amb=8)
    junction(R, 'NS', 'pillar', openings={'hubE': [door_op(0)]})
    ceil_light(R, 0, -600, 384, size=30, power=40, rng=600, color=(255, 220, 200))
    ceil_light(R, 0, 600, 384, size=30, power=40, rng=600, color=(220, 255, 220))
    side(R, 192, +1, 'store', h=352, depth=600)
    # the reliquary: a stone chest, the bones in their robe on top under a glass case
    R.box(560, 0, -90, 760, 80, 90, STONE, skip='B', top=STONE, lux=10)
    R.box(580, 80, -60, 740, 92, 60, ROBE, lux=10)
    R.prism(octo(600, 0, 14), 92, 112, WHITEP, caps='TB')                     # the skull, at the head end
    for k in range(5):
        R.box(630 + k * 20, 92, -20, 640 + k * 20, 96, 20, WHITEP, lux=10)   # ribs through the robe
    R.box(570, 80, -80, 750, 150, 80, GLASS, lux=10)
    named(R, 'RELIC', 540, 100, 0)
    named(R, 'SPIRIT', 470, 0, -180)
    tree(R, 700, 300)
    for x, z, m in ((620, 220, GIFTR), (760, 220, GIFTG), (640, 380, GIFTG), (560, 300, GIFTR)):
        R.box(x - 24, 0, z - 24, x + 24, 40, z + 24, m, skip='B', lux=10)
    ceil_light(R, 640, -250, 352, size=24, power=40, rng=500, color=(255, 80, 70))
    ceil_light(R, 640, 250, 352, size=24, power=40, rng=500, color=(80, 255, 110))
    ceil_light(R, 400, 0, 352, size=30, power=40, rng=600, color=(255, 236, 200))
    item(R, 'doc22_112', 420, 0, 300)
    return (R, 'XMS', 'SCP-112-PT, Santa Claus\'s bones (Light Containment): a reliquary chamber decorated for Christmas. Sometimes an old man in a bishop\'s robe is waiting by it.',
            1, 0.6, ((300, 165, -300), (680, 120, 100)))


ALL = [room2b22xmas]
