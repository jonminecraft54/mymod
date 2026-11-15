"""Extra preview renders of the seventh-batch rooms (out\\b7v_*.png -> out\\b7_views.jpg), for checking by eye."""
import sys
from PIL import Image
import rooms_b7 as B

D, UP = B.DEEP, B.UP
VIEWS = [
    (B.room2subway052, 'a', (360, D + 200, 640), (560, D - 120, 900)),        # the pit steps at the north end
    (B.room2subway052, 'b', (680, D - 40, -700), (680, D + 60, 900)),        # down in the pit, along the track
    (B.room2hall99, 'a', (0, 165, 860), (0, 160, -600)),                     # from the cell end, back down the kennels
    (B.room2hall99, 'b', (400, 165, 500), (640, 60, 820)),                    # inside the open cell
    (B.room2gameshow, 'a', (20, UP + 165, -440), (700, 300, -440)),          # the booth window over the stage
    (B.room2gameshow, 'b', (330, 165, 0), (750, 60, -460)),                  # the light-up floor
    (B.room2mailbox, 'a', (560, 165, -100), (900, 80, -560)),                # living room to the bathroom doorway
    (B.room2mailbox, 'b', (380, 165, -700), (500, 120, -40)),                # the front of the house
    (B.room2realchar, 'a', (330, 165, -200), (896, 180, 0)),                 # the studio set
    (B.room2realchar, 'b', (500, D + 165, -300), (250, D + 100, -760)),      # the glass chamber and the pens
    (B.room2block15, 'a', (500, 165, 160), (300, 140, 160)),                 # inside Cell 667 looking out
    (B.room2psych, 'a', (500, 165, 0), (520, 120, -560)),                    # the padded cells
    (B.room2sheet, 'a', (0, 165, -350), (400, 120, -500)),                   # Holding 6096-B through its window
    (B.room2diner, 'a', (700, 165, -300), (976, 190, -140)),                 # the windows
    (B.room2wait1440, 'a', (-500, 165, 400), (-500, 120, -300)),             # through the one-way glass
    (B.room2subway052, 'c', (0, 165, -700), (-192, 150, 0)),                 # the corridor upstairs
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
        p = 'out/b7v_%s_%s.png' % (fn.__name__, tag)
        cache[fn].render(eye, look, p, size=(640, 360))
        tiles.append(p)
    cols = 4
    sheet = Image.new('RGB', (640 * cols, 360 * ((len(tiles) + cols - 1) // cols)))
    for i, p in enumerate(tiles):
        sheet.paste(Image.open(p), ((i % cols) * 640, (i // cols) * 360))
    sheet.save('out/b7_views.jpg', quality=88)
    print('ok')
