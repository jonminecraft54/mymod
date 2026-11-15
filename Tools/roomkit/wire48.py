"""Hook the SCP-806 screening room of batch 48 (IndevU48.bb + generated IndevU48Data.bb) into the game, with the
notes. Run make_docs48.py and gen_b47.py --game first. Safe to run twice. Originals kept once as *.bak_u48."""
from wire33 import load, after_line, before_line
import os
import shutil
from make_docs48 import TITLES, DOCS

ROOT = r"I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9"


def save(rel, text):
    p = os.path.join(ROOT, rel)
    bak = p + '.bak_u48'
    if not os.path.exists(bak):
        shutil.copy2(p, bak)
    open(p, 'wb').write(text.encode('latin-1'))


NAMES = [l.strip() for l in open('b48_names.txt') if l.strip()]
ALIASES = [('room2scp806', ('806', 'scp806', 'projector', 'screening'))]

if __name__ == '__main__':
    done = []
    t, nl = load('Main.bb')
    t, c = after_line(t, 'Include "IndevU47Data.bb"', 'Include "IndevU48.bb"\nInclude "IndevU48Data.bb"\n', 'Include "IndevU48.bb"', nl)
    done.append(('Main include', c))
    t, c = after_line(t, '\tIndevU47Events()', '\tIndevU48Events() ;Indev: batch 48, SCP-806 (IndevU48.bb)\n', 'IndevU48Events()', nl)
    done.append(('Main events', c))
    al = ''
    for room, keys in ALIASES:
        al += '\t\t\t\t\t\t\tCase %s\n\t\t\t\t\t\t\t\troomName = "%s"\n' % (', '.join('"%s"' % k for k in keys), room)
    t, c = before_line(t, 'Case "blockhall", "blockd"', al, 'roomName = "room2scp806"', nl)
    done.append(('Main teleport aliases', c))
    save('Main.bb', t)

    t, nl = load('MapSystem.bb')
    fr = ('\t\tCase %s\n\t\t\t;[Block]\n\t\t\tIndevFillU48(r) ;Indev: batch 48, table in IndevU48Data.bb\n\t\t\t;[End Block]\n'
          % ', '.join('"%s"' % n for n in NAMES))
    t, c = before_line(t, 'Case "room2blockhall"', fr, 'IndevFillU48(r)', nl)
    done.append(('MapSystem FillRoom', c))
    save('MapSystem.bb', t)

    t, nl = load('UpdateEvents.bb')
    ue = '\t\t\tCase "u48room"\n\t\t\t\t;[Block]\n\t\t\t\tUpdateIndevU48(e) ;Indev (IndevU48.bb)\n\t\t\t\t;[End Block]\n'
    t, c = before_line(t, 'Case "v02room"', ue, 'UpdateIndevU48(e)', nl)
    done.append(('UpdateEvents', c))
    save('UpdateEvents.bb', t)

    t, nl = load(r'Data\rooms.ini')
    if '[room2scp806]' not in t:
        t = t.rstrip('\r\n') + nl + open('b48_rooms.ini.txt').read().replace('\n', nl)
        done.append(('rooms.ini', True))
    save(r'Data\rooms.ini', t)

    t, nl = load(r'Data\items.ini')
    if '[docb48_orient]' not in t:
        add = ''
        for n in DOCS:
            add += ('\n[%s]\ngroup = paper\nmodel = GFX\\items\\paper.x\ninvicon = GFX\\items\\INVpaper.png\n'
                    'document = GFX\\items\\%s.jpg\nscale = 0.003\nsound = 0\n' % (n, n))
        for k, lab in (('a', 'D'), ('b', 'SEC'), ('c', 'TOON'), ('d', 'LIVE'), ('e', '5.8s')):
            add += ('\n[reel806%s]\nmodel = GFX\\items\\filmreel.x\ninvicon = GFX\\items\\INVreel806%s.png\nscale = 0.06\n'
                    'texture override = GFX\\items\\filmreel.png\ntexture flags = 5\nsound = 2\n' % (k, k))
        t = t.rstrip('\r\n') + nl + add.replace('\n', nl)
        done.append(('items.ini', True))
    save(r'Data\items.ini', t)

    t, nl = load(r'Data\strings.ini')
    names = ''.join('%s = %s\n' % (k, TITLES[k]) for k in TITLES)
    names += ('reel806a = Film Reel (D: Class-D Footage)\nreel806b = Film Reel (SEC: Security Footage)\nreel806c = Film Reel (TOON: Animated Short)\n'
              'reel806d = Film Reel (LIVE: Staff Interview)\nreel806e = Film Reel (5.8s Loop)\n')
    t, c = after_line(t, 'docb46_173 = ', names, 'docb48_orient = ', nl)
    done.append(('strings.ini', c))
    save(r'Data\strings.ini', t)

    for d in done:
        print(d)
