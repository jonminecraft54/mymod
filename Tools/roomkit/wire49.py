"""Hook the SCP-806 screening room of batch 48 (IndevU48.bb + generated IndevU48Data.bb) into the game, with the
notes. Run make_docs49.py and gen_b47.py --game first. Safe to run twice. Originals kept once as *.bak_u49."""
from wire33 import load, after_line, before_line
import os
import shutil
from make_docs49 import TITLES, DOCS

ROOT = r"I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9"


def save(rel, text):
    p = os.path.join(ROOT, rel)
    bak = p + '.bak_u49'
    if not os.path.exists(bak):
        shutil.copy2(p, bak)
    open(p, 'wb').write(text.encode('latin-1'))


NAMES = [l.strip() for l in open('b49_names.txt') if l.strip()]
ALIASES = [('room2scp087b', ('087b', 'scp087b', '87b'))]

if __name__ == '__main__':
    done = []
    t, nl = load('Main.bb')
    t, c = after_line(t, 'Include "IndevU48Data.bb"', 'Include "IndevU49.bb"\nInclude "IndevU49Data.bb"\n', 'Include "IndevU49.bb"', nl)
    done.append(('Main include', c))
    t, c = after_line(t, '\tIndevU48Events()', '\tIndevU49Events() ;Indev: batch 49, SCP-087-B (IndevU49.bb)\n', 'IndevU49Events()', nl)
    done.append(('Main events', c))
    al = ''
    for room, keys in ALIASES:
        al += '\t\t\t\t\t\t\tCase %s\n\t\t\t\t\t\t\t\troomName = "%s"\n' % (', '.join('"%s"' % k for k in keys), room)
    t, c = before_line(t, 'Case "blockhall", "blockd"', al, 'roomName = "room2scp087b"', nl)
    done.append(('Main teleport aliases', c))
    save('Main.bb', t)

    t, nl = load('MapSystem.bb')
    fr = ('\t\tCase %s\n\t\t\t;[Block]\n\t\t\tIndevFillU49(r) ;Indev: batch 49, table in IndevU49Data.bb\n\t\t\t;[End Block]\n'
          % ', '.join('"%s"' % n for n in NAMES))
    t, c = before_line(t, 'Case "room2blockhall"', fr, 'IndevFillU49(r)', nl)
    done.append(('MapSystem FillRoom', c))
    save('MapSystem.bb', t)

    t, nl = load('UpdateEvents.bb')
    ue = '\t\t\tCase "u49room"\n\t\t\t\t;[Block]\n\t\t\t\tUpdateIndevU49(e) ;Indev (IndevU49.bb)\n\t\t\t\t;[End Block]\n'
    t, c = before_line(t, 'Case "v02room"', ue, 'UpdateIndevU49(e)', nl)
    done.append(('UpdateEvents', c))
    save('UpdateEvents.bb', t)

    t, nl = load(r'Data\rooms.ini')
    if '[room2scp087b]' not in t:
        t = t.rstrip('\r\n') + nl + open('b49_rooms.ini.txt').read().replace('\n', nl)
        done.append(('rooms.ini', True))
    save(r'Data\rooms.ini', t)

    t, nl = load(r'Data\items.ini')
    if '[docb49_orient]' not in t:
        add = ''
        for n in DOCS:
            add += ('\n[%s]\ngroup = paper\nmodel = GFX\\items\\paper.x\ninvicon = GFX\\items\\INVpaper.png\n'
                    'document = GFX\\items\\%s.jpg\nscale = 0.003\nsound = 0\n' % (n, n))
        t = t.rstrip('\r\n') + nl + add.replace('\n', nl)
        done.append(('items.ini', True))
    save(r'Data\items.ini', t)

    t, nl = load(r'Data\strings.ini')
    names = ''.join('%s = %s\n' % (k, TITLES[k]) for k in TITLES)
    names += ('reel806a = Film Reel (D: Class-D Footage)\nreel806b = Film Reel (SEC: Security Footage)\nreel806c = Film Reel (TOON: Animated Short)\n'
              'reel806d = Film Reel (LIVE: Staff Interview)\nreel806e = Film Reel (5.8s Loop)\n')
    t, c = after_line(t, 'docb46_173 = ', names, 'docb49_orient = ', nl)
    done.append(('strings.ini', c))
    save(r'Data\strings.ini', t)

    for d in done:
        print(d)
