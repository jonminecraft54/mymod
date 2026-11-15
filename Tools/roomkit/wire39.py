"""Hook the three rooms of batch 39 (IndevU39.bb + generated IndevU39Data.bb) into the game, with the five notes
and SCP-1176-1 (honey1176). Run make_assets39.py, make_docs39.py and gen_b39.py --game first. Safe to run twice.
Originals kept once as *.bak_u39. (Resets, per-frame update, fog, the ration and SCP-500 hooks, music slot 26 and
the save fields are hooked by hand: Indev.bb, IndevHazards.bb, IndevU26.bb, IndevRations.bb, IndevPills.bb,
Main.bb Music(26), IndevSide.bb - see Changelog 4x.)"""
from wire33 import load, after_line, before_line
import os
import shutil
from make_docs39 import TITLES, DOCS

ROOT = r"I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9"


def save(rel, text):
    p = os.path.join(ROOT, rel)
    bak = p + '.bak_u39'
    if not os.path.exists(bak):
        shutil.copy2(p, bak)
    open(p, 'wb').write(text.encode('latin-1'))


NAMES = [l.strip() for l in open('b39_names.txt') if l.strip()]
ALIASES = [('room2b41research', ('research', '586', '1176')), ('room2b41warehouse', ('warehouse', 'warehouseb', '1370', '1562')), ('room2b41testcon', ('testcon', '1013'))]

if __name__ == '__main__':
    done = []
    t, nl = load('Main.bb')
    t, c = after_line(t, 'Include "IndevU38Data.bb"', 'Include "IndevU39.bb"\nInclude "IndevU39Data.bb"\n', 'Include "IndevU39.bb"', nl)
    done.append(('Main include', c))
    t, c = after_line(t, 'IndevU38Events()', '\tIndevU39Events() ;Indev: batch 39, research, Warehouse B, Test Containment 4 (IndevU39.bb)\n', 'IndevU39Events()', nl)
    done.append(('Main events', c))
    al = ''
    for room, keys in ALIASES:
        al += '\t\t\t\t\t\t\tCase %s\n\t\t\t\t\t\t\t\troomName = "%s"\n' % (', '.join('"%s"' % k for k in keys), room)
    t, c = before_line(t, 'Case "blockhall", "blockd"', al, 'roomName = "room2b41research"', nl)
    done.append(('Main teleport aliases', c))
    t, c = before_line(t, 'Case "food1117"',
                       '\t\t\t\tCase "honey1176"\n\t\t\t\t\t;[Block]\n\t\t\t\t\tIndevUse39(SelectedItem) ;Indev: SCP-1176-1 (IndevU39.bb)\n\t\t\t\t\t;[End Block]\n',
                       'IndevUse39(SelectedItem)', nl)
    done.append(('Main item use', c))
    save('Main.bb', t)

    t, nl = load('MapSystem.bb')
    fr = ('\t\tCase %s\n\t\t\t;[Block]\n\t\t\tIndevFillU39(r) ;Indev: batch 39, table in IndevU39Data.bb\n\t\t\t;[End Block]\n'
          % ', '.join('"%s"' % n for n in NAMES))
    t, c = before_line(t, 'Case "room2blockhall"', fr, 'IndevFillU39(r)', nl)
    done.append(('MapSystem FillRoom', c))
    save('MapSystem.bb', t)

    t, nl = load('UpdateEvents.bb')
    ue = '\t\t\tCase "u39room"\n\t\t\t\t;[Block]\n\t\t\t\tUpdateIndevU39(e) ;Indev (IndevU39.bb)\n\t\t\t\t;[End Block]\n'
    t, c = before_line(t, 'Case "v02room"', ue, 'UpdateIndevU39(e)', nl)
    done.append(('UpdateEvents', c))
    save('UpdateEvents.bb', t)

    t, nl = load(r'Data\rooms.ini')
    if '[room2b41research]' not in t:
        t = t.rstrip('\r\n') + nl + open('b39_rooms.ini.txt').read().replace('\n', nl)
        done.append(('rooms.ini', True))
    save(r'Data\rooms.ini', t)

    t, nl = load(r'Data\items.ini')
    if '[docb39_1013]' not in t:
        add = ''
        for n in DOCS:
            add += ('\n[%s]\ngroup = paper\nmodel = GFX\\items\\paper.x\ninvicon = GFX\\items\\INVpaper.png\n'
                    'document = GFX\\items\\%s.jpg\nscale = 0.003\nsound = 0\n' % (n, n))
        add += ('\n[honey1176]\nmodel = GFX\\items\\indevration.b3d\ninvicon = GFX\\items\\INVindevration.png\n'
                'texture override = GFX\\items\\honey1176.png\nscale = 0.0012\ngroup = food\nsound = 2\n')
        t = t.rstrip('\r\n') + nl + add.replace('\n', nl)
        done.append(('items.ini', True))
    save(r'Data\items.ini', t)

    t, nl = load(r'Data\strings.ini')
    names = ''.join('%s = %s\n' % (k, TITLES[k]) for k in TITLES)
    t, c = after_line(t, 'docb38_1039 = ', names, 'docb39_1013 = ', nl)
    done.append(('strings.ini', c))
    save(r'Data\strings.ini', t)

    for d in done:
        print(d)
