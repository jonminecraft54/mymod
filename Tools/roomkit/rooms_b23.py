"""The twenty-third batch: SCP-6483, Nicolas Roberts, the reality bender who brings Christmas. Code in IndevU23.bb.
The SCP text is a short summary of scp-wiki.wikidot.com/scp-6483 (CC BY-SA 3.0); geometry and textures are our own.

  room2b23santa  LCZ  Site-322 corridor; east, SCP-6483's quarters: a peppermint-striped cell (his candy walls from
                      the 2019 breach, kept), a dinner table, a fireplace, a tree, and the Scranton Reality Anchor
                      monitor on the wall. Nick is there, in a maintenance uniform. Switch the anchor monitor off and
                      a Nativitatis Event begins."""
from rooms_b22 import *

MINT = Mat('indev_6483mint.png', 256)                 # made by make_assets23.py
SRA = Mat('indev_6483sra.png', cast=False)
FIRE = Mat('indev_6483fire.png', cast=False)
CLOTH = Mat('indev_6483cloth.png', 128)


def room2b23santa():
    R = R_('room2b23santa', amb=9)
    junction(R, 'NS', 'pillar', openings={'hubE': [door_op(0)]})
    ceil_light(R, 0, -600, 384, size=30, power=40, rng=600)
    ceil_light(R, 0, 600, 384, size=30, power=40, rng=600)
    STYLES['mint23'] = (MINT, WOOD, DARK)
    side(R, 192, +1, 'mint23', h=352, depth=600)
    # the dinner table with its cloth, two chairs
    R.box(420, 0, -330, 620, 76, -200, CLOTH, skip='B', top=CLOTH, lux=10)
    chair(R, 380, -265, 'E')
    chair(R, 660, -265, 'W')
    # the fireplace on the far wall
    R.box(800, 0, -120, 856, 200, 120, STONE, skip='B', lux=10)
    wall_decal(R, FIRE, 800, 0, 'W', 140, 90, 50)
    tree(R, 720, 320)
    for x, z, m in ((640, 260, GIFTR), (780, 220, GIFTG)):
        R.box(x - 22, 0, z - 22, x + 22, 36, z + 22, m, skip='B', lux=10)
    wall_decal(R, SRA, 420, -400, 'N', 100, 70, 170)               # the reality anchor monitor, on the south wall
    named(R, 'SRA', 420, 170, -390)
    named(R, 'NICK', 520, 0, 120)
    named(R, 'TABLE', 520, 90, -265)
    named(R, 'FIRE', 780, 50, 0)
    reserve(R, 'GLOW')
    ceil_light(R, 520, 0, 352, size=30, power=46, rng=600, color=(255, 236, 210))
    item(R, 'doc23_6483', 560, 76, -240)
    item(R, 'doc23_coix', 450, 76, -300)
    return (R, 'SNT', 'SCP-6483, Nicolas Roberts (Light Containment): the quarters of a reality bender who only ever makes Christmas, with peppermint walls and a reality anchor monitor.',
            1, 0.4, ((300, 165, 300), (520, 100, 0)))


ALL = [room2b23santa]
