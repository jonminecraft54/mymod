"""Hook the four deep storage rooms of batch 34 (IndevU34.bb + generated IndevU34Data.bb) into the game, with the
registry pages and the ten items. Run make_assets34.py, make_hd34.py, make_docs34.py and gen_b34.py --game first.
Safe to run twice. Originals are kept once as *.bak_u34."""
from wire33 import load, after_line, before_line
import os
import shutil
from make_docs34 import TITLES, DOCS
from data34 import U, ROOMS, ITEMS34

ROOT = r"I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9"


def save(rel, text):
    p = os.path.join(ROOT, rel)
    bak = p + '.bak_u34'
    if not os.path.exists(bak):
        shutil.copy2(p, bak)
    open(p, 'wb').write(text.encode('latin-1'))


NAMES = [l.strip() for l in open('b34_names.txt') if l.strip()]
ALIASES = [(ROOMS[k], tuple(['storage%s' % n] + [u['num'].lower() for u in U if u['room'] == k]))
           for k, n in (('A', '06'), ('B', '07'), ('C', '08'), ('D', '09'))]

if __name__ == '__main__':
    done = []
    t, nl = load('Main.bb')
    t, c = after_line(t, 'Include "IndevU33Data.bb"', 'Include "IndevU34.bb"\nInclude "IndevU34Data.bb"\n', 'Include "IndevU34.bb"', nl)
    done.append(('Main include', c))
    t, c = after_line(t, 'IndevU33Events()', '\tIndevU34Events() ;Indev: batch 34, deep storage areas 06-09 (IndevU34.bb)\n', 'IndevU34Events()', nl)
    done.append(('Main events', c))
    al = ''
    for room, keys in ALIASES:
        al += '\t\t\t\t\t\t\tCase %s\n\t\t\t\t\t\t\t\troomName = "%s"\n' % (', '.join('"%s"' % k for k in keys), room)
    t, c = before_line(t, 'Case "blockhall", "blockd"', al, 'roomName = "room2b34humanoid"', nl)
    done.append(('Main teleport aliases', c))
    t, c = before_line(t, 'Case "candy983_lum", "candy983_clear"',
                       '\t\t\t\tCase %s\n\t\t\t\t\t;[Block]\n\t\t\t\t\tIndevUse34(SelectedItem) ;Indev: batch 34 items (IndevU34.bb)\n\t\t\t\t\t;[End Block]\n'
                       % ', '.join('"%s"' % n for n in ITEMS34), 'IndevUse34(SelectedItem)', nl)
    done.append(('Main item use', c))
    save('Main.bb', t)

    t, nl = load('MapSystem.bb')
    fr = ('\t\tCase %s\n\t\t\t;[Block]\n\t\t\tIndevFillU34(r) ;Indev: batch 34, table in IndevU34Data.bb\n\t\t\t;[End Block]\n'
          % ', '.join('"%s"' % n for n in NAMES))
    t, c = before_line(t, 'Case "room2blockhall"', fr, 'IndevFillU34(r)', nl)
    done.append(('MapSystem FillRoom', c))
    save('MapSystem.bb', t)

    t, nl = load('UpdateEvents.bb')
    ue = '\t\t\tCase "u34room"\n\t\t\t\t;[Block]\n\t\t\t\tUpdateIndevU34(e) ;Indev (IndevU34.bb)\n\t\t\t\t;[End Block]\n'
    t, c = before_line(t, 'Case "v02room"', ue, 'UpdateIndevU34(e)', nl)
    done.append(('UpdateEvents', c))
    save('UpdateEvents.bb', t)

    t, nl = load(r'Data\rooms.ini')
    if '[room2b34humanoid]' not in t:
        t = t.rstrip('\r\n') + nl + open('b34_rooms.ini.txt').read().replace('\n', nl)
        done.append(('rooms.ini', True))
    save(r'Data\rooms.ini', t)

    t, nl = load(r'Data\items.ini')
    if '[docarea06p1]' not in t:
        add = ''
        for n in DOCS:
            add += ('\n[%s]\ngroup = paper\nmodel = GFX\\items\\paper.x\ninvicon = GFX\\items\\INVpaper.png\n'
                    'document = GFX\\items\\%s.jpg\nscale = 0.003\nsound = 0\n' % (n, n))
        for n in ITEMS34:
            add += ('\n[%s]\ngroup = misc\nmodel = GFX\\items\\%s.b3d\ninvicon = GFX\\items\\INV%s.png\n'
                    'scale = 0.008\nsound = 2\n' % (n, n, n))
        t = t.rstrip('\r\n') + nl + add.replace('\n', nl)
        done.append(('items.ini', True))
    save(r'Data\items.ini', t)

    t, nl = load(r'Data\strings.ini')
    names = ''.join('%s = %s\n' % (k, TITLES[k]) for k in TITLES)
    t, c = after_line(t, 'doc1007 = ', names, 'docarea06p1 = ', nl)
    done.append(('strings.ini', c))
    save(r'Data\strings.ini', t)

    for d in done:
        print(d)
