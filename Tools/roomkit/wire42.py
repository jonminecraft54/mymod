"""Hook the four rooms of batch 42 (IndevU42.bb + generated IndevU42Data.bb) into the game, with the notes and the
two items (flare1577, bracelets154). Run make_assets42.py, make_docs42.py and gen_b42.py --game first. Safe to run
twice. Originals kept once as *.bak_u42. (Reset, per-frame update, SCP-500 cure and save fields are hooked by
hand: Indev.bb, IndevHazards.bb, IndevPills.bb, IndevSide.bb.)"""
from wire33 import load, after_line, before_line
import os
import shutil
from make_docs42 import TITLES, DOCS

ROOT = r"I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9"
ITEMS42 = ['flare1577', 'bracelets154']


def save(rel, text):
    p = os.path.join(ROOT, rel)
    bak = p + '.bak_u42'
    if not os.path.exists(bak):
        shutil.copy2(p, bak)
    open(p, 'wb').write(text.encode('latin-1'))


NAMES = [l.strip() for l in open('b42_names.txt') if l.strip()]
ALIASES = [('room2b44panopticon', ('panopticon', 'facilityb')), ('room3b44toybox', ('toybox', 'cblock', '127', '439', '1577')),
           ('room4b44vault', ('vault', 'dvault', '4139', '154')), ('room2b44cellar', ('cellar', 'eblock', '466'))]

if __name__ == '__main__':
    done = []
    t, nl = load('Main.bb')
    t, c = after_line(t, 'Include "IndevU41Data.bb"', 'Include "IndevU42.bb"\nInclude "IndevU42Data.bb"\n', 'Include "IndevU42.bb"', nl)
    done.append(('Main include', c))
    t, c = after_line(t, 'IndevU41Events()', '\tIndevU42Events() ;Indev: batch 42, Panopticon, Toy Box, Vault, Cellar (IndevU42.bb)\n', 'IndevU42Events()', nl)
    done.append(('Main events', c))
    al = ''
    for room, keys in ALIASES:
        al += '\t\t\t\t\t\t\tCase %s\n\t\t\t\t\t\t\t\troomName = "%s"\n' % (', '.join('"%s"' % k for k in keys), room)
    t, c = before_line(t, 'Case "blockhall", "blockd"', al, 'roomName = "room2b44panopticon"', nl)
    done.append(('Main teleport aliases', c))
    t, c = before_line(t, 'Case "food1117"',
                       '\t\t\t\tCase %s\n\t\t\t\t\t;[Block]\n\t\t\t\t\tIndevUse42(SelectedItem) ;Indev: batch 42 items (IndevU42.bb)\n\t\t\t\t\t;[End Block]\n'
                       % ', '.join('"%s"' % n for n in ITEMS42), 'IndevUse42(SelectedItem)', nl)
    done.append(('Main item use', c))
    save('Main.bb', t)

    t, nl = load('MapSystem.bb')
    fr = ('\t\tCase %s\n\t\t\t;[Block]\n\t\t\tIndevFillU42(r) ;Indev: batch 42, table in IndevU42Data.bb\n\t\t\t;[End Block]\n'
          % ', '.join('"%s"' % n for n in NAMES))
    t, c = before_line(t, 'Case "room2blockhall"', fr, 'IndevFillU42(r)', nl)
    done.append(('MapSystem FillRoom', c))
    save('MapSystem.bb', t)

    t, nl = load('UpdateEvents.bb')
    ue = '\t\t\tCase "u42room"\n\t\t\t\t;[Block]\n\t\t\t\tUpdateIndevU42(e) ;Indev (IndevU42.bb)\n\t\t\t\t;[End Block]\n'
    t, c = before_line(t, 'Case "v02room"', ue, 'UpdateIndevU42(e)', nl)
    done.append(('UpdateEvents', c))
    save('UpdateEvents.bb', t)

    t, nl = load(r'Data\rooms.ini')
    if '[room2b44panopticon]' not in t:
        t = t.rstrip('\r\n') + nl + open('b42_rooms.ini.txt').read().replace('\n', nl)
        done.append(('rooms.ini', True))
    save(r'Data\rooms.ini', t)

    t, nl = load(r'Data\items.ini')
    if '[docb42_127]' not in t:
        add = ''
        for n in DOCS:
            add += ('\n[%s]\ngroup = paper\nmodel = GFX\\items\\paper.x\ninvicon = GFX\\items\\INVpaper.png\n'
                    'document = GFX\\items\\%s.jpg\nscale = 0.003\nsound = 0\n' % (n, n))
        for n in ITEMS42:
            add += ('\n[%s]\nmodel = GFX\\items\\indevration.b3d\ninvicon = GFX\\items\\INVindevration.png\n'
                    'texture override = GFX\\items\\%s.png\nscale = 0.0012\nsound = 2\n' % (n, n))
        t = t.rstrip('\r\n') + nl + add.replace('\n', nl)
        done.append(('items.ini', True))
    save(r'Data\items.ini', t)

    t, nl = load(r'Data\strings.ini')
    names = ''.join('%s = %s\n' % (k, TITLES[k]) for k in TITLES)
    t, c = after_line(t, 'docb41_break = ', names, 'docb42_127 = ', nl)
    done.append(('strings.ini', c))
    save(r'Data\strings.ini', t)

    for d in done:
        print(d)
