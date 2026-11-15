"""Extra preview renders of the eighth-batch rooms (out\\b7v_*.png -> out\\b7_views.jpg), for checking by eye."""
import sys
from PIL import Image
import rooms_b8 as B

D, UP = B.DEEP, B.UP
VIEWS = [
    (B.room2yule, 'a', (-330, 165, -480), (-600, 120, -760)),          # SCP-2983: the cereal shelves, the bowl
    (B.room2yule, 'b', (-330, 165, 380), (-600, 100, 700)),            # SCP-1933's cell
    (B.room2yule, 'c', (330, 165, -380), (480, 160, -620)),            # SCP-1225: the tree, the open sky
    (B.room2yule, 'd', (330, 165, 380), (600, 120, 700)),              # Kappa-31 staging
    (B.room2pinata, 'a', (720, 165, -300), (900, 80, 200)),            # inside the cell
    (B.room2pinata, 'b', (430, 165, 560), (430, 100, 840)),            # the cold store
    (B.room2pinata, 'c', (420, 165, -100), (410, 100, -480)),          # the incinerator
    (B.room2argos, 'a', (300, 165, -300), (700, 100, 300)),            # St. Nick's Workshop
    (B.room2demoncore, 'a', (150, D + 165, -800), (300, D + 140, 200)),  # from the control room, through the lead glass
    (B.room2chrono, 'a', (100, UP + 165, -700), (510, UP + 80, 200)),  # the launch deck
    (B.room2chrono, 'b', (400, 165, -300), (640, 150, -820)),          # the BTKAI unit
    (B.room2argos, 'b', (-60, D + 165, 0), (300, D + 100, -200)),      # the chute
]

if __name__ == '__main__':
    only = sys.argv[1:]
    cache = {}
    tiles = []
    for fn, tag, eye, look in VIEWS:
        if only and fn.__name__ not in only:
            continue
        if fn not in cache:
            R = fn()[0]
            R.bake(verbose=False)
            cache[fn] = R
        p = 'out/b8v_%s_%s.png' % (fn.__name__, tag)
        cache[fn].render(eye, look, p, size=(640, 360))
        tiles.append(p)
    cols = 4
    sheet = Image.new('RGB', (640 * cols, 360 * ((len(tiles) + cols - 1) // cols)))
    for i, p in enumerate(tiles):
        sheet.paste(Image.open(p), ((i % cols) * 640, (i // cols) * 360))
    sheet.save('out/b8_views.jpg', quality=88)
    print('ok')
