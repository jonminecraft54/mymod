"""Hook the four legacy rooms of batch 47 (IndevU47.bb + generated IndevU47Data.bb) into the game, with the four
notes. Run make_docs47.py and gen_b47.py --game first. Safe to run twice. Originals kept once as *.bak_u47."""
from wire33 import load, after_line, before_line
import os
import shutil
from make_docs47 import TITLES, DOCS

ROOT = r"I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9"


def save(rel, text):
    p = os.path.join(ROOT, rel)
    bak = p + '.bak_u47'
    if not os.path.exists(bak):
        shutil.copy2(p, bak)
    open(p, 'wb').write(text.encode('latin-1'))


NAMES = [l.strip() for l in open('b47_names.txt') if l.strip()]
ALIASES = [('room2closetsolderones', ('oldstart', 'oldstartroom')), ('room2oldconference', ('oldconference', 'oldconf')),
           ('room2oldmedibay', ('oldmedibay', 'oldmedbay')), ('room2oldcores', ('oldcores', 'corechambers'))]

if __name__ == '__main__':
    done = []
    t, nl = load('Main.bb')
    t, c = after_line(t, 'Include "IndevU46Data.bb"', 'Include "IndevU47.bb"\nInclude "IndevU47Data.bb"\n', 'Include "IndevU47.bb"', nl)
    done.append(('Main include', c))
    t, c = after_line(t, '\tIndevU46Events()', '\tIndevU47Events() ;Indev: batch 47, legacy rooms (IndevU47.bb)\n', 'IndevU47Events()', nl)
    done.append(('Main events', c))
    al = ''
    for room, keys in ALIASES:
        al += '\t\t\t\t\t\t\tCase %s\n\t\t\t\t\t\t\t\troomName = "%s"\n' % (', '.join('"%s"' % k for k in keys), room)
    t, c = before_line(t, 'Case "blockhall", "blockd"', al, 'roomName = "room2oldcores"', nl)
    done.append(('Main teleport aliases', c))
    save('Main.bb', t)

    t, nl = load('MapSystem.bb')
    fr = ('\t\tCase %s\n\t\t\t;[Block]\n\t\t\tIndevFillU47(r) ;Indev: batch 47, table in IndevU47Data.bb\n\t\t\t;[End Block]\n'
          % ', '.join('"%s"' % n for n in NAMES))
    t, c = before_line(t, 'Case "room2blockhall"', fr, 'IndevFillU47(r)', nl)
    done.append(('MapSystem FillRoom', c))
    save('MapSystem.bb', t)

    t, nl = load('UpdateEvents.bb')
    ue = '\t\t\tCase "u47room"\n\t\t\t\t;[Block]\n\t\t\t\tUpdateIndevU47(e) ;Indev (IndevU47.bb)\n\t\t\t\t;[End Block]\n'
    t, c = before_line(t, 'Case "v02room"', ue, 'UpdateIndevU47(e)', nl)
    done.append(('UpdateEvents', c))
    save('UpdateEvents.bb', t)

    t, nl = load(r'Data\rooms.ini')
    if '[room2oldcores]' not in t:
        t = t.rstrip('\r\n') + nl + open('b47_rooms.ini.txt').read().replace('\n', nl)
        done.append(('rooms.ini', True))
    save(r'Data\rooms.ini', t)

    t, nl = load(r'Data\items.ini')
    if '[docb47_orient]' not in t:
        add = ''
        for n in DOCS:
            add += ('\n[%s]\ngroup = paper\nmodel = GFX\\items\\paper.x\ninvicon = GFX\\items\\INVpaper.png\n'
                    'document = GFX\\items\\%s.jpg\nscale = 0.003\nsound = 0\n' % (n, n))
        t = t.rstrip('\r\n') + nl + add.replace('\n', nl)
        done.append(('items.ini', True))
    save(r'Data\items.ini', t)

    t, nl = load(r'Data\strings.ini')
    names = ''.join('%s = %s\n' % (k, TITLES[k]) for k in TITLES)
    t, c = after_line(t, 'docb46_173 = ', names, 'docb47_orient = ', nl)
    done.append(('strings.ini', c))
    save(r'Data\strings.ini', t)

    for d in done:
        print(d)
