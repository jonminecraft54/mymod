"""Hook the two rooms of the seventeenth batch (The Forgotten Hotel, IndevU17.bb + generated IndevU17Data.bb) into the
game, with the three notes.
Run make_assets17.py (textures and plates), make_docs17.py (notes) and gen_b17.py --game first (it writes
b17_names.txt and b17_rooms.ini.txt). Safe to run twice. Originals are kept once as *.bak_u17."""
import os
import shutil
from make_docs17 import TITLES

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
    bak = p + '.bak_u17'
    if not os.path.exists(bak):
        shutil.copy2(p, bak)
    open(p, 'wb').write(text.encode('latin-1'))


NAMES = [l.strip() for l in open('b17_names.txt') if l.strip()]
ALIASES = [('room2hotelcorr', ('hotel', 'floorh')), ('room2hotellift', ('lobby', 'hotellift'))]

if __name__ == '__main__':
    done = []
    t, nl = load('Main.bb')
    t, c = after_line(t, 'Include "IndevU15.bb"', 'Include "IndevU17.bb"\nInclude "IndevU17Data.bb"\n', 'Include "IndevU17.bb"', nl)
    done.append(('Main include', c))
    t, c = after_line(t, 'IndevU14Events()', '\tIndevU17Events() ;Indev: The Forgotten Hotel, floor H and the lift lobby (IndevU17.bb)\n', 'IndevU17Events()', nl)
    done.append(('Main events', c))
    al = ''
    for room, keys in ALIASES:
        al += '\t\t\t\t\t\t\tCase %s\n\t\t\t\t\t\t\t\troomName = "%s"\n' % (', '.join('"%s"' % k for k in keys), room)
    t, c = before_line(t, 'Case "blockhall", "blockd"', al, 'roomName = "room2hotelcorr"', nl)
    done.append(('Main teleport aliases', c))
    save('Main.bb', t)

    t, nl = load('MapSystem.bb')
    fr = ('\t\tCase %s\n\t\t\t;[Block]\n\t\t\tIndevFillU17(r) ;Indev: The Forgotten Hotel, table in IndevU17Data.bb\n\t\t\t;[End Block]\n'
          % ', '.join('"%s"' % n for n in NAMES))
    t, c = before_line(t, 'Case "room2blockhall"', fr, 'IndevFillU17(r)', nl)
    done.append(('MapSystem FillRoom', c))
    save('MapSystem.bb', t)

    t, nl = load('UpdateEvents.bb')
    ue = '\t\t\tCase "u17room"\n\t\t\t\t;[Block]\n\t\t\t\tUpdateIndevU17(e) ;Indev (IndevU17.bb)\n\t\t\t\t;[End Block]\n'
    t, c = before_line(t, 'Case "v02room"', ue, 'UpdateIndevU17(e)', nl)
    done.append(('UpdateEvents', c))
    save('UpdateEvents.bb', t)

    t, nl = load(r'Data\rooms.ini')
    if '[room2hotelcorr]' not in t:
        add = open('b17_rooms.ini.txt').read()
        t = t.rstrip('\r\n') + nl + add.replace('\n', nl)
        done.append(('rooms.ini', True))
    save(r'Data\rooms.ini', t)

    t, nl = load(r'Data\items.ini')
    if '[doc17reg]' not in t:
        add = ''
        for n in sorted(TITLES):
            add += ('\n[%s]\ngroup = paper\nmodel = GFX\\items\\paper.x\ninvicon = GFX\\items\\INVpaper.png\n'
                    'document = GFX\\items\\%s.jpg\nscale = 0.003\nsound = 0\n' % (n, n))
        t = t.rstrip('\r\n') + nl + add.replace('\n', nl)
        done.append(('items.ini', True))
    save(r'Data\items.ini', t)

    t, nl = load(r'Data\strings.ini')
    names = ''.join('%s = %s\n' % (k, TITLES[k]) for k in sorted(TITLES))
    t, c = after_line(t, 'doc5094 = ', names, 'doc17reg = ', nl)
    done.append(('strings.ini', c))
    save(r'Data\strings.ini', t)

    for d in done:
        print(d)
