"""Hook the two storage rooms of batch 35 (IndevU35.bb + generated IndevU35Data.bb) into the game, with the registry
pages and the four items. Run make_assets35.py, make_hd35.py, make_docs35.py and gen_b35.py --game first.
Safe to run twice. Originals are kept once as *.bak_u35."""
from wire33 import load, after_line, before_line
import os
import shutil
from make_docs35 import TITLES, DOCS
from data35 import U, ROOMS, ITEMS35

ROOT = r"I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9"


def save(rel, text):
    p = os.path.join(ROOT, rel)
    bak = p + '.bak_u35'
    if not os.path.exists(bak):
        shutil.copy2(p, bak)
    open(p, 'wb').write(text.encode('latin-1'))


NAMES = [l.strip() for l in open('b35_names.txt') if l.strip()]
ALIASES = [(ROOMS[k], tuple(['storage%s' % n, alias] + [u['num'].lower() for u in U if u['room'] == k]))
           for k, n, alias in (('E', '10', 'cellblock'), ('F', '11', 'bunker'))]

if __name__ == '__main__':
    done = []
    t, nl = load('Main.bb')
    t, c = after_line(t, 'Include "IndevU34Data.bb"', 'Include "IndevU35.bb"\nInclude "IndevU35Data.bb"\n', 'Include "IndevU35.bb"', nl)
    done.append(('Main include', c))
    t, c = after_line(t, 'IndevU34Events()', '\tIndevU35Events() ;Indev: batch 35, storage areas 10-11 (IndevU35.bb)\n', 'IndevU35Events()', nl)
    done.append(('Main events', c))
    al = ''
    for room, keys in ALIASES:
        al += '\t\t\t\t\t\t\tCase %s\n\t\t\t\t\t\t\t\troomName = "%s"\n' % (', '.join('"%s"' % k for k in keys), room)
    t, c = before_line(t, 'Case "blockhall", "blockd"', al, 'roomName = "room2b35cellblock"', nl)
    done.append(('Main teleport aliases', c))
    t, c = before_line(t, 'Case "candy983_lum", "candy983_clear"',
                       '\t\t\t\tCase %s\n\t\t\t\t\t;[Block]\n\t\t\t\t\tIndevUse35(SelectedItem) ;Indev: batch 35 items (IndevU35.bb)\n\t\t\t\t\t;[End Block]\n'
                       % ', '.join('"%s"' % n for n in ITEMS35), 'IndevUse35(SelectedItem)', nl)
    done.append(('Main item use', c))
    save('Main.bb', t)

    t, nl = load('MapSystem.bb')
    fr = ('\t\tCase %s\n\t\t\t;[Block]\n\t\t\tIndevFillU35(r) ;Indev: batch 35, table in IndevU35Data.bb\n\t\t\t;[End Block]\n'
          % ', '.join('"%s"' % n for n in NAMES))
    t, c = before_line(t, 'Case "room2blockhall"', fr, 'IndevFillU35(r)', nl)
    done.append(('MapSystem FillRoom', c))
    save('MapSystem.bb', t)

    t, nl = load('UpdateEvents.bb')
    ue = '\t\t\tCase "u35room"\n\t\t\t\t;[Block]\n\t\t\t\tUpdateIndevU35(e) ;Indev (IndevU35.bb)\n\t\t\t\t;[End Block]\n'
    t, c = before_line(t, 'Case "v02room"', ue, 'UpdateIndevU35(e)', nl)
    done.append(('UpdateEvents', c))
    save('UpdateEvents.bb', t)

    t, nl = load(r'Data\rooms.ini')
    if '[room2b35cellblock]' not in t:
        t = t.rstrip('\r\n') + nl + open('b35_rooms.ini.txt').read().replace('\n', nl)
        done.append(('rooms.ini', True))
    save(r'Data\rooms.ini', t)

    t, nl = load(r'Data\items.ini')
    if '[docarea10p1]' not in t:
        add = ''
        for n in DOCS:
            add += ('\n[%s]\ngroup = paper\nmodel = GFX\\items\\paper.x\ninvicon = GFX\\items\\INVpaper.png\n'
                    'document = GFX\\items\\%s.jpg\nscale = 0.003\nsound = 0\n' % (n, n))
        for n in ITEMS35:
            add += ('\n[%s]\ngroup = misc\nmodel = GFX\\items\\%s.b3d\ninvicon = GFX\\items\\INV%s.png\n'
                    'scale = 0.008\nsound = 2\n' % (n, n, n))
        t = t.rstrip('\r\n') + nl + add.replace('\n', nl)
        done.append(('items.ini', True))
    save(r'Data\items.ini', t)

    t, nl = load(r'Data\strings.ini')
    names = ''.join('%s = %s\n' % (k, TITLES[k]) for k in TITLES)
    t, c = after_line(t, 'docarea06p1 = ', names, 'docarea10p1 = ', nl)
    done.append(('strings.ini', c))
    save(r'Data\strings.ini', t)

    for d in done:
        print(d)
