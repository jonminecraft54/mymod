"""Hook the six rooms of the thirteenth batch (IndevU13.bb + generated IndevU13Data.bb) into the game.
Run gen_b13.py --game first (it writes b13_names.txt and b13_rooms.ini.txt), and make_docs13.py for the notes.
Safe to run twice. Originals are kept once as *.bak_u13."""
import os
import shutil
from make_docs13 import TITLES

ROOT = r"I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9"


def load(rel):
    raw = open(os.path.join(ROOT, rel), 'rb').read()
    nl = b'\r\n' if b'\r\n' in raw else b'\n'
    return raw.decode('latin-1'), nl.decode()


def after_line(text, anchor, block, marker, nl):
    if marker in text:
        return text, False
    i = text.index(anchor)
    j = text.index(nl, i) + len(nl)
    return text[:j] + block.replace('\n', nl) + text[j:], True


def before_line(text, anchor, block, marker, nl):
    if marker in text:
        return text, False
    i = text.index(anchor)
    j = text.rfind(nl, 0, i) + len(nl)
    return text[:j] + block.replace('\n', nl) + text[j:], True


def save(rel, text):
    p = os.path.join(ROOT, rel)
    bak = p + '.bak_u13'
    if not os.path.exists(bak):
        shutil.copy2(p, bak)
    open(p, 'wb').write(text.encode('latin-1'))


NAMES = [l.strip() for l in open('b13_names.txt') if l.strip()]
ALIASES = [('room2safewing', ('safewing', 'breakroom')), ('room2biowing', ('biowing', 'vase')),
           ('room2doorhall', ('doorhall', 'door249')), ('room2menagerie', ('menagerie', 'enclosure')),
           ('room2pool354', ('pool354', 'redpool')), ('room2incidents', ('incidents', 'weissnacht'))]

if __name__ == '__main__':
    done = []
    t, nl = load('Main.bb')
    t, c = after_line(t, 'Include "IndevT12Data.bb"', 'Include "IndevU13.bb"\nInclude "IndevU13Data.bb"\n', 'Include "IndevU13.bb"', nl)
    done.append(('Main include', c))
    t, c = after_line(t, 'IndevT12Events()', '\tIndevU13Events() ;Indev: the six rooms of the thirteenth batch (IndevU13.bb)\n', 'IndevU13Events()', nl)
    done.append(('Main events', c))
    al = ''
    for room, keys in ALIASES:
        al += '\t\t\t\t\t\t\tCase %s\n\t\t\t\t\t\t\t\troomName = "%s"\n' % (', '.join('"%s"' % k for k in keys), room)
    t, c = before_line(t, 'Case "blockhall", "blockd"', al, 'roomName = "room2safewing"', nl)
    done.append(('Main teleport aliases', c))
    save('Main.bb', t)

    t, nl = load('MapSystem.bb')
    fr = '\t\tCase %s\n\t\t\t;[Block]\n\t\t\tIndevFillU13(r) ;Indev: thirteenth-batch rooms, table in IndevU13Data.bb\n\t\t\t;[End Block]\n' % ', '.join('"%s"' % n for n in NAMES)
    t, c = before_line(t, 'Case "room2blockhall"', fr, 'IndevFillU13(r)', nl)
    done.append(('MapSystem FillRoom', c))
    save('MapSystem.bb', t)

    t, nl = load('UpdateEvents.bb')
    ue = '\t\t\tCase "u13room"\n\t\t\t\t;[Block]\n\t\t\t\tUpdateIndevU13(e) ;Indev (IndevU13.bb)\n\t\t\t\t;[End Block]\n'
    t, c = before_line(t, 'Case "v02room"', ue, 'UpdateIndevU13(e)', nl)
    done.append(('UpdateEvents', c))
    save('UpdateEvents.bb', t)

    t, nl = load(r'Data\rooms.ini')
    if '[room2safewing]' not in t:
        add = open('b13_rooms.ini.txt').read()
        t = t.rstrip('\r\n') + nl + add.replace('\n', nl)
        done.append(('rooms.ini', True))
    save(r'Data\rooms.ini', t)

    t, nl = load(r'Data\items.ini')
    if '[doc377]' not in t:
        add = ''
        for n in sorted(TITLES):
            add += ('\n[%s]\ngroup = paper\nmodel = GFX\\items\\paper.x\ninvicon = GFX\\items\\INVpaper.png\ndocument = GFX\\items\\%s.jpg\nscale = 0.003\nsound = 0\n'
                    % (n, n))
        t = t.rstrip('\r\n') + nl + add.replace('\n', nl)
        done.append(('items.ini', True))
    save(r'Data\items.ini', t)

    t, nl = load(r'Data\strings.ini')
    names = ''.join('%s = %s\n' % (k, TITLES[k]) for k in sorted(TITLES))
    t, c = after_line(t, 'docbal1b = ', names, 'doc377 = ', nl)
    done.append(('strings.ini', c))
    save(r'Data\strings.ini', t)

    for d in done:
        print(d)
