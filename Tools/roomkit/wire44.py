"""Hook the three Residential Sector wings of batch 44 (IndevU44.bb + generated IndevU44Data.bb) into the game,
with the six notes. Run make_assets40.py, make_docs44.py and gen_b40.py --game first. Safe to run twice.
Originals kept once as *.bak_u44. (Reset and save fields are hooked by hand: Indev.bb, IndevSide.bb.)"""
from wire33 import load, after_line, before_line
import os
import shutil
from make_docs44 import TITLES, DOCS

ROOT = r"I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9"


def save(rel, text):
    p = os.path.join(ROOT, rel)
    bak = p + '.bak_u44'
    if not os.path.exists(bak):
        shutil.copy2(p, bak)
    open(p, 'wb').write(text.encode('latin-1'))


NAMES = [l.strip() for l in open('b44_names.txt') if l.strip()]
ALIASES = [('room2b46old1074', ('old1074', 'oldwing', 'room104')), ('room2b46cryo', ('cryo', 'cryogenic')), ('room2b46theatre', ('theatre2', 'testtheatre')), ('room2b46gravity', ('gravity', 'gravlab')), ('room2b46geology', ('geology', 'geosite', 'crystal')), ('room2b46o5vault', ('o5', 'o5vault', 'records'))]

if __name__ == '__main__':
    done = []
    t, nl = load('Main.bb')
    t, c = after_line(t, 'Include "IndevU43Data.bb"', 'Include "IndevU44.bb"\nInclude "IndevU44Data.bb"\n', 'Include "IndevU44.bb"', nl)
    done.append(('Main include', c))
    t, c = after_line(t, 'IndevU43Events()', '\tIndevU44Events() ;Indev: batch 44, old 1074 wing and five sites (IndevU44.bb)\n', 'IndevU44Events()', nl)
    done.append(('Main events', c))
    al = ''
    for room, keys in ALIASES:
        al += '\t\t\t\t\t\t\tCase %s\n\t\t\t\t\t\t\t\troomName = "%s"\n' % (', '.join('"%s"' % k for k in keys), room)
    t, c = before_line(t, 'Case "blockhall", "blockd"', al, 'roomName = "room2b46cryo"', nl)
    done.append(('Main teleport aliases', c))
    save('Main.bb', t)

    t, nl = load('MapSystem.bb')
    fr = ('\t\tCase %s\n\t\t\t;[Block]\n\t\t\tIndevFillU44(r) ;Indev: batch 44, table in IndevU44Data.bb\n\t\t\t;[End Block]\n'
          % ', '.join('"%s"' % n for n in NAMES))
    t, c = before_line(t, 'Case "room2blockhall"', fr, 'IndevFillU44(r)', nl)
    done.append(('MapSystem FillRoom', c))
    save('MapSystem.bb', t)

    t, nl = load('UpdateEvents.bb')
    ue = '\t\t\tCase "u44room"\n\t\t\t\t;[Block]\n\t\t\t\tUpdateIndevU44(e) ;Indev (IndevU44.bb)\n\t\t\t\t;[End Block]\n'
    t, c = before_line(t, 'Case "v02room"', ue, 'UpdateIndevU44(e)', nl)
    done.append(('UpdateEvents', c))
    save('UpdateEvents.bb', t)

    t, nl = load(r'Data\rooms.ini')
    if '[room2b46cryo]' not in t:
        t = t.rstrip('\r\n') + nl + open('b44_rooms.ini.txt').read().replace('\n', nl)
        done.append(('rooms.ini', True))
    save(r'Data\rooms.ini', t)

    t, nl = load(r'Data\items.ini')
    if '[docb44_1074]' not in t:
        add = ''
        for n in DOCS:
            add += ('\n[%s]\ngroup = paper\nmodel = GFX\\items\\paper.x\ninvicon = GFX\\items\\INVpaper.png\n'
                    'document = GFX\\items\\%s.jpg\nscale = 0.003\nsound = 0\n' % (n, n))
        t = t.rstrip('\r\n') + nl + add.replace('\n', nl)
        done.append(('items.ini', True))
    save(r'Data\items.ini', t)

    t, nl = load(r'Data\strings.ini')
    names = ''.join('%s = %s\n' % (k, TITLES[k]) for k in TITLES)
    t, c = after_line(t, 'docb43_hoist = ', names, 'docb44_1074 = ', nl)
    done.append(('strings.ini', c))
    save(r'Data\strings.ini', t)

    for d in done:
        print(d)
