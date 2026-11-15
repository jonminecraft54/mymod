"""Hook the five rooms of batch 37 (IndevU37.bb + generated IndevU37Data.bb) into the game, with the five notes.
Run make_assets37.py, make_docs37.py and gen_b37.py --game first. Safe to run twice. Originals kept once as *.bak_u37.
(The resets, per-frame update, fog, SCP-914 recipe and save fields are hooked by hand: Indev.bb, IndevHazards.bb,
IndevU26.bb, IndevPills.bb, IndevSide.bb - see Changelog 4w.)"""
from wire33 import load, after_line, before_line
import os
import shutil
from make_docs37 import TITLES, DOCS

ROOT = r"I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9"


def save(rel, text):
    p = os.path.join(ROOT, rel)
    bak = p + '.bak_u37'
    if not os.path.exists(bak):
        shutil.copy2(p, bak)
    open(p, 'wb').write(text.encode('latin-1'))


NAMES = [l.strip() for l in open('b37_names.txt') if l.strip()]
ALIASES = [('room1scp028', ('028', 'scp028', 'knowledge', 'yard')),
           ('room2b39reactor', ('reactor', 'heavywater', '006b')),
           ('room2b39archive', ('archive39', 'deeparchive', 'shelves')),
           ('room2b39hall', ('balcony', 'hall39', 'balconyhall')),
           ('room2b39cells', ('cells39', 'dblock', 'cellblock39'))]

if __name__ == '__main__':
    done = []
    t, nl = load('Main.bb')
    t, c = after_line(t, 'Include "IndevU36Data.bb"', 'Include "IndevU37.bb"\nInclude "IndevU37Data.bb"\n', 'Include "IndevU37.bb"', nl)
    done.append(('Main include', c))
    t, c = after_line(t, 'IndevU36Events()', '\tIndevU37Events() ;Indev: batch 37, SCP-028, reactor, archive, hall, cells (IndevU37.bb)\n', 'IndevU37Events()', nl)
    done.append(('Main events', c))
    al = ''
    for room, keys in ALIASES:
        al += '\t\t\t\t\t\t\tCase %s\n\t\t\t\t\t\t\t\troomName = "%s"\n' % (', '.join('"%s"' % k for k in keys), room)
    t, c = before_line(t, 'Case "blockhall", "blockd"', al, 'roomName = "room1scp028"', nl)
    done.append(('Main teleport aliases', c))
    save('Main.bb', t)

    t, nl = load('MapSystem.bb')
    fr = ('\t\tCase %s\n\t\t\t;[Block]\n\t\t\tIndevFillU37(r) ;Indev: batch 37, table in IndevU37Data.bb\n\t\t\t;[End Block]\n'
          % ', '.join('"%s"' % n for n in NAMES))
    t, c = before_line(t, 'Case "room2blockhall"', fr, 'IndevFillU37(r)', nl)
    done.append(('MapSystem FillRoom', c))
    save('MapSystem.bb', t)

    t, nl = load('UpdateEvents.bb')
    ue = '\t\t\tCase "u37room"\n\t\t\t\t;[Block]\n\t\t\t\tUpdateIndevU37(e) ;Indev (IndevU37.bb)\n\t\t\t\t;[End Block]\n'
    t, c = before_line(t, 'Case "v02room"', ue, 'UpdateIndevU37(e)', nl)
    done.append(('UpdateEvents', c))
    save('UpdateEvents.bb', t)

    t, nl = load(r'Data\rooms.ini')
    if '[room1scp028]' not in t:
        t = t.rstrip('\r\n') + nl + open('b37_rooms.ini.txt').read().replace('\n', nl)
        done.append(('rooms.ini', True))
    save(r'Data\rooms.ini', t)

    t, nl = load(r'Data\items.ini')
    if '[docb37_028]' not in t:
        add = ''
        for n in DOCS:
            add += ('\n[%s]\ngroup = paper\nmodel = GFX\\items\\paper.x\ninvicon = GFX\\items\\INVpaper.png\n'
                    'document = GFX\\items\\%s.jpg\nscale = 0.003\nsound = 0\n' % (n, n))
        t = t.rstrip('\r\n') + nl + add.replace('\n', nl)
        done.append(('items.ini', True))
    save(r'Data\items.ini', t)

    t, nl = load(r'Data\strings.ini')
    names = ''.join('%s = %s\n' % (k, TITLES[k]) for k in TITLES)
    t, c = after_line(t, 'docb36_1200 = ', names, 'docb37_028 = ', nl)
    done.append(('strings.ini', c))
    save(r'Data\strings.ini', t)

    for d in done:
        print(d)
