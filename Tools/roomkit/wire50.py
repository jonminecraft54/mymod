"""Hook the SCP-806 screening room of batch 48 (IndevU48.bb + generated IndevU48Data.bb) into the game, with the
notes. Run make_docs50.py and gen_b47.py --game first. Safe to run twice. Originals kept once as *.bak_u50."""
from wire33 import load, after_line, before_line
import os
import shutil
from make_docs50 import TITLES, DOCS

ROOT = r"I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9"


def save(rel, text):
    p = os.path.join(ROOT, rel)
    bak = p + '.bak_u50'
    if not os.path.exists(bak):
        shutil.copy2(p, bak)
    open(p, 'wb').write(text.encode('latin-1'))


NAMES = [l.strip() for l in open('b50_names.txt') if l.strip()]
ALIASES = [('room2b50lab02', ('lab02', 'scp061', '061')), ('room2b50chem', ('chemstore', 'chemical')), ('room2b50observe', ('observation', 'scp162', '162')), ('room2b50office', ('researchoffice', 'resoffice')), ('room2b50specimen', ('specimen', 'scp020', '020'))]

if __name__ == '__main__':
    done = []
    t, nl = load('Main.bb')
    t, c = after_line(t, 'Include "IndevU49Data.bb"', 'Include "IndevU50.bb"\nInclude "IndevU50Data.bb"\n', 'Include "IndevU50.bb"', nl)
    done.append(('Main include', c))
    t, c = after_line(t, '\tIndevU49Events()', '\tIndevU50Events() ;Indev: batch 50, research complex (IndevU50.bb)\n', 'IndevU50Events()', nl)
    done.append(('Main events', c))
    al = ''
    for room, keys in ALIASES:
        al += '\t\t\t\t\t\t\tCase %s\n\t\t\t\t\t\t\t\troomName = "%s"\n' % (', '.join('"%s"' % k for k in keys), room)
    t, c = before_line(t, 'Case "blockhall", "blockd"', al, 'roomName = "room2b50specimen"', nl)
    done.append(('Main teleport aliases', c))
    save('Main.bb', t)

    t, nl = load('MapSystem.bb')
    fr = ('\t\tCase %s\n\t\t\t;[Block]\n\t\t\tIndevFillU50(r) ;Indev: batch 50, table in IndevU50Data.bb\n\t\t\t;[End Block]\n'
          % ', '.join('"%s"' % n for n in NAMES))
    t, c = before_line(t, 'Case "room2blockhall"', fr, 'IndevFillU50(r)', nl)
    done.append(('MapSystem FillRoom', c))
    save('MapSystem.bb', t)

    t, nl = load('UpdateEvents.bb')
    ue = '\t\t\tCase "u50room"\n\t\t\t\t;[Block]\n\t\t\t\tUpdateIndevU50(e) ;Indev (IndevU50.bb)\n\t\t\t\t;[End Block]\n'
    t, c = before_line(t, 'Case "v02room"', ue, 'UpdateIndevU50(e)', nl)
    done.append(('UpdateEvents', c))
    save('UpdateEvents.bb', t)

    t, nl = load(r'Data\rooms.ini')
    if '[room2b50lab02]' not in t:
        t = t.rstrip('\r\n') + nl + open('b50_rooms.ini.txt').read().replace('\n', nl)
        done.append(('rooms.ini', True))
    save(r'Data\rooms.ini', t)

    t, nl = load(r'Data\items.ini')
    if '[docb50_orient]' not in t:
        add = ''
        for n in DOCS:
            add += ('\n[%s]\ngroup = paper\nmodel = GFX\\items\\paper.x\ninvicon = GFX\\items\\INVpaper.png\n'
                    'document = GFX\\items\\%s.jpg\nscale = 0.003\nsound = 0\n' % (n, n))
        t = t.rstrip('\r\n') + nl + add.replace('\n', nl)
        done.append(('items.ini', True))
    save(r'Data\items.ini', t)

    t, nl = load(r'Data\strings.ini')
    names = ''.join('%s = %s\n' % (k, TITLES[k]) for k in TITLES)
    t, c = after_line(t, 'docb49_087b = ', names, 'docb50_061 = ', nl)
    done.append(('strings.ini', c))
    save(r'Data\strings.ini', t)

    for d in done:
        print(d)
