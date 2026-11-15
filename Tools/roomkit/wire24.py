"""Hook the six rooms of batch 22 (IndevU22.bb + generated IndevU22Data.bb) into the game, with
the six notes.
Run make_assets21.py, make_docs24.py (notes) and gen_b21.py --game first (it writes
b24_names.txt and b24_rooms.ini.txt). Safe to run twice. Originals are kept once as *.bak_u24."""
import os
import shutil
from make_docs24 import TITLES

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
    bak = p + '.bak_u24'
    if not os.path.exists(bak):
        shutil.copy2(p, bak)
    open(p, 'wb').write(text.encode('latin-1'))


NAMES = [l.strip() for l in open('b24_names.txt') if l.strip()]
ALIASES = [('room2b24block1', ('block24a', 'scp018', 'scp027', 'scp101', 'scp134', 'scp181', 'scp262')), ('room2b24block2', ('block24b', 'scp300', 'scp314', 'scp387', 'scp423', 'scp426', 'scp432')), ('room2b24block3', ('block24c', 'scp504', 'scp524', 'scp847', 'scp871', 'scp1230', 'scp1733')), ('room2b24block4', ('block24d', 'scp2030', 'scp2317', 'scp409', 'scp191', 'scp2399', 'scp1000')), ('room2b24store6h', ('store6h', '6h', 'scp087', '087'))]

if __name__ == '__main__':
    done = []
    t, nl = load('Main.bb')
    t, c = after_line(t, 'Include "IndevU18Data.bb"', 'Include "IndevU18.bb"\nInclude "IndevU18Data.bb"\n', 'Include "IndevU19.bb"', nl)
    done.append(('Main include', c))
    t, c = after_line(t, 'IndevU17Events()', '\tIndevU18Events() ;Indev: The Hollowcrest, six hotel rooms (IndevU18.bb)\n', 'IndevU18Events()', nl)
    done.append(('Main events', c))
    al = ''
    for room, keys in ALIASES:
        al += '\t\t\t\t\t\t\tCase %s\n\t\t\t\t\t\t\t\troomName = "%s"\n' % (', '.join('"%s"' % k for k in keys), room)
    t, c = before_line(t, 'Case "blockhall", "blockd"', al, 'roomName = "room2b24block1"', nl)
    done.append(('Main teleport aliases', c))
    save('Main.bb', t)

    t, nl = load('MapSystem.bb')
    fr = ('\t\tCase %s\n\t\t\t;[Block]\n\t\t\tIndevFillU24(r) ;Indev: batch 24, table in IndevU24Data.bb\n\t\t\t;[End Block]\n'
          % ', '.join('"%s"' % n for n in NAMES))
    t, c = before_line(t, 'Case "room2blockhall"', fr, 'IndevFillU24(r)', nl)
    done.append(('MapSystem FillRoom', c))
    save('MapSystem.bb', t)

    t, nl = load('UpdateEvents.bb')
    ue = '\t\t\tCase "u24room"\n\t\t\t\t;[Block]\n\t\t\t\tUpdateIndevU24(e) ;Indev (IndevU24.bb)\n\t\t\t\t;[End Block]\n'
    t, c = before_line(t, 'Case "v02room"', ue, 'UpdateIndevU24(e)', nl)
    done.append(('UpdateEvents', c))
    save('UpdateEvents.bb', t)

    t, nl = load(r'Data\rooms.ini')
    if '[room2b24block1]' not in t:
        add = open('b24_rooms.ini.txt').read()
        t = t.rstrip('\r\n') + nl + add.replace('\n', nl)
        done.append(('rooms.ini', True))
    save(r'Data\rooms.ini', t)

    t, nl = load(r'Data\items.ini')
    if '[doc24_018]' not in t:
        add = ''
        for n in sorted(TITLES):
            add += ('\n[%s]\ngroup = paper\nmodel = GFX\\items\\paper.x\ninvicon = GFX\\items\\INVpaper.png\n'
                    'document = GFX\\items\\%s.jpg\nscale = 0.003\nsound = 0\n' % (n, n))
        t = t.rstrip('\r\n') + nl + add.replace('\n', nl)
        done.append(('items.ini', True))
    save(r'Data\items.ini', t)

    t, nl = load(r'Data\strings.ini')
    names = ''.join('%s = %s\n' % (k, TITLES[k]) for k in sorted(TITLES))
    t, c = after_line(t, 'doc23_6483 = ', names, 'doc24_018 = ', nl)
    done.append(('strings.ini', c))
    save(r'Data\strings.ini', t)

    for d in done:
        print(d)
