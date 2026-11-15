"""Hook the three rooms of batch 38 (IndevU38.bb + generated IndevU38Data.bb) into the game, with the five notes
and SCP-1117-2 (food1117). Run make_assets38.py, make_docs38.py and gen_b38.py --game first. Safe to run twice.
Originals kept once as *.bak_u38. (Resets, per-frame update, fog, the ration and SCP-500 hooks, music slot 26 and
the save fields are hooked by hand: Indev.bb, IndevHazards.bb, IndevU26.bb, IndevRations.bb, IndevPills.bb,
Main.bb Music(26), IndevSide.bb - see Changelog 4x.)"""
from wire33 import load, after_line, before_line
import os
import shutil
from make_docs38 import TITLES, DOCS

ROOT = r"I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9"


def save(rel, text):
    p = os.path.join(ROOT, rel)
    bak = p + '.bak_u38'
    if not os.path.exists(bak):
        shutil.copy2(p, bak)
    open(p, 'wb').write(text.encode('latin-1'))


NAMES = [l.strip() for l in open('b38_names.txt') if l.strip()]
ALIASES = [('room2b40infhall', ('infhall', 'longhall', 'l40')),
           ('room2b40display', ('display', '1039', '1148', 'pending')),
           ('room2b40party', ('party', '1117', 'cake', 'social'))]

if __name__ == '__main__':
    done = []
    t, nl = load('Main.bb')
    t, c = after_line(t, 'Include "IndevU37Data.bb"', 'Include "IndevU38.bb"\nInclude "IndevU38Data.bb"\n', 'Include "IndevU38.bb"', nl)
    done.append(('Main include', c))
    t, c = after_line(t, 'IndevU37Events()', '\tIndevU38Events() ;Indev: batch 38, long hallway, display hall, party (IndevU38.bb)\n', 'IndevU38Events()', nl)
    done.append(('Main events', c))
    al = ''
    for room, keys in ALIASES:
        al += '\t\t\t\t\t\t\tCase %s\n\t\t\t\t\t\t\t\troomName = "%s"\n' % (', '.join('"%s"' % k for k in keys), room)
    t, c = before_line(t, 'Case "blockhall", "blockd"', al, 'roomName = "room2b40infhall"', nl)
    done.append(('Main teleport aliases', c))
    t, c = before_line(t, 'Case "gum1200", "jar1916", "pop3147", "cotton1921"',
                       '\t\t\t\tCase "food1117"\n\t\t\t\t\t;[Block]\n\t\t\t\t\tIndevUse38(SelectedItem) ;Indev: SCP-1117-2 (IndevU38.bb)\n\t\t\t\t\t;[End Block]\n',
                       'IndevUse38(SelectedItem)', nl)
    done.append(('Main item use', c))
    save('Main.bb', t)

    t, nl = load('MapSystem.bb')
    fr = ('\t\tCase %s\n\t\t\t;[Block]\n\t\t\tIndevFillU38(r) ;Indev: batch 38, table in IndevU38Data.bb\n\t\t\t;[End Block]\n'
          % ', '.join('"%s"' % n for n in NAMES))
    t, c = before_line(t, 'Case "room2blockhall"', fr, 'IndevFillU38(r)', nl)
    done.append(('MapSystem FillRoom', c))
    save('MapSystem.bb', t)

    t, nl = load('UpdateEvents.bb')
    ue = '\t\t\tCase "u38room"\n\t\t\t\t;[Block]\n\t\t\t\tUpdateIndevU38(e) ;Indev (IndevU38.bb)\n\t\t\t\t;[End Block]\n'
    t, c = before_line(t, 'Case "v02room"', ue, 'UpdateIndevU38(e)', nl)
    done.append(('UpdateEvents', c))
    save('UpdateEvents.bb', t)

    t, nl = load(r'Data\rooms.ini')
    if '[room2b40infhall]' not in t:
        t = t.rstrip('\r\n') + nl + open('b38_rooms.ini.txt').read().replace('\n', nl)
        done.append(('rooms.ini', True))
    save(r'Data\rooms.ini', t)

    t, nl = load(r'Data\items.ini')
    if '[docb38_1039]' not in t:
        add = ''
        for n in DOCS:
            add += ('\n[%s]\ngroup = paper\nmodel = GFX\\items\\paper.x\ninvicon = GFX\\items\\INVpaper.png\n'
                    'document = GFX\\items\\%s.jpg\nscale = 0.003\nsound = 0\n' % (n, n))
        add += ('\n[food1117]\nmodel = GFX\\items\\indevration.b3d\ninvicon = GFX\\items\\INVindevration.png\n'
                'texture override = GFX\\items\\food1117.png\nscale = 0.0012\ngroup = food\nsound = 2\n')
        t = t.rstrip('\r\n') + nl + add.replace('\n', nl)
        done.append(('items.ini', True))
    save(r'Data\items.ini', t)

    t, nl = load(r'Data\strings.ini')
    names = ''.join('%s = %s\n' % (k, TITLES[k]) for k in TITLES)
    t, c = after_line(t, 'docb37_028 = ', names, 'docb38_1039 = ', nl)
    done.append(('strings.ini', c))
    save(r'Data\strings.ini', t)

    for d in done:
        print(d)
