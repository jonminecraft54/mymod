"""Hook the three Residential Sector wings of batch 45 (IndevU44.bb + generated IndevU45Data.bb) into the game,
with the six notes. Run make_assets40.py, make_docs46.py and gen_b40.py --game first. Safe to run twice.
Originals kept once as *.bak_u46. (Reset and save fields are hooked by hand: Indev.bb, IndevSide.bb.)"""
from wire33 import load, after_line, before_line
import os
import shutil
from make_docs46 import TITLES, DOCS

ROOT = r"I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9"


def save(rel, text):
    p = os.path.join(ROOT, rel)
    bak = p + '.bak_u46'
    if not os.path.exists(bak):
        shutil.copy2(p, bak)
    open(p, 'wb').write(text.encode('latin-1'))


NAMES = [l.strip() for l in open('b46_names.txt') if l.strip()]
ALIASES = [('room2b49checkpoint', ('checkpoint9', 'cp9')), ('room2b49hidden', ('sectorr', 'harrison')), ('room2b49perslift', ('perslift', 'lowercomplex')), ('room2b49sealed', ('sealedwing', 'sealed'))]

if __name__ == '__main__':
    done = []
    t, nl = load('Main.bb')
    t, c = after_line(t, 'Include "IndevU45Data.bb"', 'Include "IndevU46.bb"\nInclude "IndevU46Data.bb"\n', 'Include "IndevU46.bb"', nl)
    done.append(('Main include', c))
    t, c = after_line(t, 'IndevU45Events()', '\tIndevU46Events() ;Indev: batch 46, alternate timeline (IndevU46.bb)\n', 'IndevU46Events()', nl)
    done.append(('Main events', c))
    al = ''
    for room, keys in ALIASES:
        al += '\t\t\t\t\t\t\tCase %s\n\t\t\t\t\t\t\t\troomName = "%s"\n' % (', '.join('"%s"' % k for k in keys), room)
    t, c = before_line(t, 'Case "blockhall", "blockd"', al, 'roomName = "room2b49hidden"', nl)
    done.append(('Main teleport aliases', c))
    save('Main.bb', t)

    t, nl = load('MapSystem.bb')
    fr = ('\t\tCase %s\n\t\t\t;[Block]\n\t\t\tIndevFillU46(r) ;Indev: batch 46, table in IndevU46Data.bb\n\t\t\t;[End Block]\n'
          % ', '.join('"%s"' % n for n in NAMES))
    t, c = before_line(t, 'Case "room2blockhall"', fr, 'IndevFillU46(r)', nl)
    done.append(('MapSystem FillRoom', c))
    save('MapSystem.bb', t)

    t, nl = load('UpdateEvents.bb')
    ue = '\t\t\tCase "u46room"\n\t\t\t\t;[Block]\n\t\t\t\tUpdateIndevU46(e) ;Indev (IndevU46.bb)\n\t\t\t\t;[End Block]\n'
    t, c = before_line(t, 'Case "v02room"', ue, 'UpdateIndevU46(e)', nl)
    done.append(('UpdateEvents', c))
    save('UpdateEvents.bb', t)

    t, nl = load(r'Data\rooms.ini')
    if '[room2b49hidden]' not in t:
        t = t.rstrip('\r\n') + nl + open('b46_rooms.ini.txt').read().replace('\n', nl)
        done.append(('rooms.ini', True))
    save(r'Data\rooms.ini', t)

    t, nl = load(r'Data\items.ini')
    if '[docb46_timeline]' not in t:
        add = ''
        for n in DOCS:
            add += ('\n[%s]\ngroup = paper\nmodel = GFX\\items\\paper.x\ninvicon = GFX\\items\\INVpaper.png\n'
                    'document = GFX\\items\\%s.jpg\nscale = 0.003\nsound = 0\n' % (n, n))
        t = t.rstrip('\r\n') + nl + add.replace('\n', nl)
        done.append(('items.ini', True))
    save(r'Data\items.ini', t)

    t, nl = load(r'Data\strings.ini')
    names = ''.join('%s = %s\n' % (k, TITLES[k]) for k in TITLES)
    t, c = after_line(t, 'docb45_939 = ', names, 'docb46_timeline = ', nl)
    done.append(('strings.ini', c))
    save(r'Data\strings.ini', t)

    for d in done:
        print(d)

