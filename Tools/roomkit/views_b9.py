"""Extra preview renders of the ninth-batch rooms (out/b9v_*.png -> out/b9_views.jpg), for checking by eye."""
import sys
from PIL import Image
import rooms_b9 as B

D, UP = B.DEEP, B.UP
VIEWS = [
    (B.room2burn457, 'a', (700, D + 165, -280), (930, D + 100, 260)),      # inside the chamber: the dry shelter
    (B.room2burn457, 'b', (300, 165, -300), (700, 120, 200)),              # Fire Post 457, upstairs
    (B.room2burn457, 'c', (380, D + 165, -640), (574, D + 150, -500)),     # airlock 1
    (B.room2burn457, 'd', (-100, D + 165, 300), (600, D + 150, 560)),      # the gallery and the pump room
    (B.room2cold016, 'a', (60, 170, -40), (560, 130, 10)),                 # the cold room through the corridor window
    (B.room2cold016, 'b', (330, 165, -740), (640, 150, -300)),             # the UV decon lock
    (B.room2cold016, 'c', (-320, 165, 380), (-640, 130, 640)),             # D-016-1's tank
    (B.room2cold016, 'd', (-320, 165, -320), (-600, 60, -720)),            # D-016-2's quarters
    (B.room2cold016, 'e', (330, 165, 320), (650, 150, 760)),               # the lab
    (B.room2cold016, 'f', (640, 165, -120), (430, 60, 110)),               # inside the cold room
    (B.room2read152, 'a', (-120, UP + 165, 330), (330, UP + 150, -120)),   # the guard's landing
    (B.room2read152, 'b', (300, 165, -250), (600, 120, 320)),              # the scan archive
    (B.room2dark280, 'a', (560, 165, -330), (300, 150, 10)),               # the cell door in the block
    (B.room2dark280, 'b', (160, 165, 0), (-180, 100, 180)),                # inside the cell
    (B.room2dark280, 'c', (-720, 165, 220), (-980, 150, -60)),             # cell lighting control
    (B.room2dark280, 'd', (720, 165, -250), (980, 180, 100)),              # the equipment store
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
        p = 'out/b9v_%s_%s.png' % (fn.__name__, tag)
        cache[fn].render(eye, look, p, size=(640, 360))
        tiles.append(p)
    cols = 4
    sheet = Image.new('RGB', (640 * cols, 360 * ((len(tiles) + cols - 1) // cols)))
    for i, p in enumerate(tiles):
        sheet.paste(Image.open(p), ((i % cols) * 640, (i // cols) * 360))
    sheet.save('out/b9_views.jpg', quality=88)
    print('ok')
