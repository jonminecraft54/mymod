"""Hook the three Residential Sector wings of batch 43 (IndevU43.bb + generated IndevU43Data.bb) into the game,
with the six notes. Run make_assets40.py, make_docs43.py and gen_b40.py --game first. Safe to run twice.
Originals kept once as *.bak_u43. (Reset and save fields are hooked by hand: Indev.bb, IndevSide.bb.)"""
from wire33 import load, after_line, before_line
import os
import shutil
from make_docs43 import TITLES, DOCS

ROOT = r"I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9"


def save(rel, text):
    p = os.path.join(ROOT, rel)
    bak = p + '.bak_u43'
    if not os.path.exists(bak):
        shutil.copy2(p, bak)
    open(p, 'wb').write(text.encode('latin-1'))


NAMES = [l.strip() for l in open('b43_names.txt') if l.strip()]
ALIASES = [('room2b45lobby', ('lobby', 'liftlobby2', 'hoist')), ('room2b45checkpoint', ('checkpoint', 'guardbooth')), ('room2b45offices', ('offices', 'officewing'))]

if __name__ == '__main__':
    done = []
    t, nl = load('Main.bb')
    t, c = after_line(t, 'Include "IndevU42Data.bb"', 'Include "IndevU43.bb"\nInclude "IndevU43Data.bb"\n', 'Include "IndevU43.bb"', nl)
    done.append(('Main include', c))
    t, c = after_line(t, 'IndevU42Events()', '\tIndevU43Events() ;Indev: batch 43, lift lobby/checkpoint/offices (IndevU43.bb)\n', 'IndevU43Events()', nl)
    done.append(('Main events', c))
    al = ''
    for room, keys in ALIASES:
        al += '\t\t\t\t\t\t\tCase %s\n\t\t\t\t\t\t\t\troomName = "%s"\n' % (', '.join('"%s"' % k for k in keys), room)
    t, c = before_line(t, 'Case "blockhall", "blockd"', al, 'roomName = "room2b45lobby"', nl)
    done.append(('Main teleport aliases', c))
    save('Main.bb', t)

    t, nl = load('MapSystem.bb')
    fr = ('\t\tCase %s\n\t\t\t;[Block]\n\t\t\tIndevFillU43(r) ;Indev: batch 43, table in IndevU43Data.bb\n\t\t\t;[End Block]\n'
          % ', '.join('"%s"' % n for n in NAMES))
    t, c = before_line(t, 'Case "room2blockhall"', fr, 'IndevFillU43(r)', nl)
    done.append(('MapSystem FillRoom', c))
    save('MapSystem.bb', t)

    t, nl = load('UpdateEvents.bb')
    ue = '\t\t\tCase "u43room"\n\t\t\t\t;[Block]\n\t\t\t\tUpdateIndevU43(e) ;Indev (IndevU43.bb)\n\t\t\t\t;[End Block]\n'
    t, c = before_line(t, 'Case "v02room"', ue, 'UpdateIndevU43(e)', nl)
    done.append(('UpdateEvents', c))
    save('UpdateEvents.bb', t)

    t, nl = load(r'Data\rooms.ini')
    if '[room2b45lobby]' not in t:
        t = t.rstrip('\r\n') + nl + open('b43_rooms.ini.txt').read().replace('\n', nl)
        done.append(('rooms.ini', True))
    save(r'Data\rooms.ini', t)

    t, nl = load(r'Data\items.ini')
    if '[docb43_hoist]' not in t:
        add = ''
        for n in DOCS:
            add += ('\n[%s]\ngroup = paper\nmodel = GFX\\items\\paper.x\ninvicon = GFX\\items\\INVpaper.png\n'
                    'document = GFX\\items\\%s.jpg\nscale = 0.003\nsound = 0\n' % (n, n))
        t = t.rstrip('\r\n') + nl + add.replace('\n', nl)
        done.append(('items.ini', True))
    save(r'Data\items.ini', t)

    t, nl = load(r'Data\strings.ini')
    names = ''.join('%s = %s\n' % (k, TITLES[k]) for k in TITLES)
    t, c = after_line(t, 'docb42_127 = ', names, 'docb43_hoist = ', nl)
    done.append(('strings.ini', c))
    save(r'Data\strings.ini', t)

    for d in done:
        print(d)
