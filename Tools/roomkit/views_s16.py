"""Extra preview renders of the sixteen-SCP rooms (out\\s16v_*.png), for checking by eye."""
from PIL import Image
import rooms_s16 as S

D = S.DEEP
VIEWS = [
    (S.room2site41, 'a', (560, 165, -200), (800, 130, 560)),      # through the fence to the cell door
    (S.room2site41, 'b', (300, 165, 200), (480, 150, -100)),      # the gate and the signs
    (S.room2cell49, 'a', (330, 165, 250), (460, 80, -340)),       # the cards
    (S.room2bunker, 'a', (140, D + 165, -330), (-300, D + 150, 440)),   # locker door
    (S.room2bio, 'a', (420, 165, -150), (790, 110, -600)),        # freezer
    (S.room2bio, 'b', (560, 165, 120), (300, 40, 400)),           # pots
    (S.room2review, 'a', (-330, 165, -200), (-560, 120, 400)),    # consoles
    (S.room2lecture, 'a', (-576, 165, -100), (-576, 190, 540)),   # the board
    (S.room2purge, 'a', (0, 165, -420), (-448, 300, 100)),        # fans + fountain
    (S.room2origin, 'a', (-200, 165, -460), (150, 100, 200)),     # tendrils
    (S.room2vault117, 'a', (0, 165, -500), (-192, 150, 0)),       # upstairs lift door
    (S.room2siv, 'a', (560, 165, 120), (780, 100, 285)),          # the die
]

if __name__ == '__main__':
    cache = {}
    tiles = []
    for fn, tag, eye, look in VIEWS:
        if fn not in cache:
            R = fn()[0]
            R.bake(verbose=False)
            cache[fn] = R
        p = 'out/s16v_%s_%s.png' % (fn.__name__, tag)
        cache[fn].render(eye, look, p, size=(640, 360))
        tiles.append(p)
    sheet = Image.new('RGB', (640 * 4, 360 * 3))
    for i, p in enumerate(tiles):
        sheet.paste(Image.open(p), ((i % 4) * 640, (i // 4) * 360))
    sheet.save('out/s16_views.jpg', quality=88)
    print('ok')
