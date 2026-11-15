"""Build every Indev room into the game folder and dump the anchor points the Blitz code uses."""
import json
import sys
import time
import roomkit
import room_catwalk, room_overlook, room_cmaint, room_archive, room_ventcore, room_whitedoor
import room_blockhall, room_testcage, room_liftshaft, room_cobserve, room_store4

MODS = [room_catwalk, room_overlook, room_cmaint, room_archive, room_ventcore, room_whitedoor,
        room_blockhall, room_testcage, room_liftshaft, room_cobserve, room_store4]
VIEWS = {
    'room2catwalk': [((0, 165, -940), (0, 260, 0)), ((330, 517, 560), (-300, 412, -100))],
    'room2overlook': [((0, 165, -940), (20, 150, 0)), ((880, -283, -560), (100, -248, 300))],
    'room2cmaint': [((900, 165, 60), (0, 150, 40)), ((330, 165, 300), (-200, 140, 760))],
    'room2archive': [((0, 165, -940), (60, 150, 0)), ((420, 165, -560), (760, 120, 300))],
    'room2ventcore': [((0, 165, -940), (0, 150, 0)), ((-520, 165, 300), (500, 180, -100))],
    'room1whitedoor': [((0, 165, -700), (0, 140, 900)), ((0, 165, -980), (0, 150, 0))],
    'room2blockhall': [((-784, 165, -500), (300, -100, 300)), ((0, -91, -600), (0, 0, 0))],
    'room1testcage': [((-420, 165, -660), (300, 150, 400)), ((560, 165, -560), (-300, 220, 250))],
    'room2liftshaft': [((0, 165, -940), (-60, 150, 0)), ((120, -539, -200), (-700, -204, 200))],
    'room2cobserve': [((0, 165, -960), (0, 160, 0)), ((-100, 165, 60), (900, 150, 60))],
    'room1store4': [((0, 165, -700), (-100, 120, 400)), ((500, 165, 100), (-500, 100, 500))],
}

if __name__ == '__main__':
    out = roomkit.MAPDIR if '--game' in sys.argv else 'out'
    anchors = {}
    t0 = time.time()
    only = [a for a in sys.argv[1:] if not a.startswith('--')]
    for m in MODS:
        if only and m.__name__ not in only:
            continue
        R, A = m.build()
        R.bake()
        R.export(out)
        anchors[R.name] = {k: [round(float(c), 1) for c in v] for k, v in A.items()}
        if '--views' in sys.argv:
            for i, (eye, look) in enumerate(VIEWS[R.name]):
                R.render(eye, look, 'out/final_%s_%d.png' % (R.name, i + 1))
    if not only:
        json.dump(anchors, open('anchors.json', 'w'), indent=1)
    print('done in %.1fs -> %s' % (time.time() - t0, out))
