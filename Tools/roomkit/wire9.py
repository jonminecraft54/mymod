"""Hook the four ninth-batch rooms (IndevS04.bb + generated IndevS04Data.bb) into the game.
Run gen_b9.py --game first (it writes b9_names.txt and b9_rooms.ini.txt). Safe to run twice.
Originals are kept once as *.bak_s04."""
import os
import shutil
from make_assets7 import TITLES

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
    bak = p + '.bak_s04'
    if not os.path.exists(bak):
        shutil.copy2(p, bak)
    open(p, 'wb').write(text.encode('latin-1'))


NAMES = [l.strip() for l in open('b9_names.txt') if l.strip()]
ALIASES = [('room2burn457', ('burn457', '457', 'fireman')), ('room2cold016', ('cold016', '016', 'bcl5')),
           ('room2read152', ('read152', '152', 'readingroom')), ('room2dark280', ('dark280', '280', 'darkcell'))]

if __name__ == '__main__':
    done = []
    t, nl = load('Main.bb')
    t, c = after_line(t, 'Include "IndevS08Data.bb"', 'Include "IndevS04.bb"\nInclude "IndevS04Data.bb"\n', 'Include "IndevS04.bb"', nl)
    done.append(('Main include', c))
    t, c = after_line(t, 'IndevS08Events()', '\tIndevS04Events() ;Indev: the four rooms of the ninth batch, 4 SCPs (IndevS04.bb)\n', 'IndevS04Events()', nl)
    done.append(('Main events', c))
    al = ''
    for room, keys in ALIASES:
        al += '\t\t\t\t\t\t\tCase %s\n\t\t\t\t\t\t\t\troomName = "%s"\n' % (', '.join('"%s"' % k for k in keys), room)
    t, c = before_line(t, 'Case "blockhall", "blockd"', al, 'roomName = "room2burn457"', nl)
    done.append(('Main teleport aliases', c))
    save('Main.bb', t)

    t, nl = load('MapSystem.bb')
    fr = '\t\tCase %s\n\t\t\t;[Block]\n\t\t\tIndevFillS04(r) ;Indev: ninth-batch rooms, table in IndevS04Data.bb\n\t\t\t;[End Block]\n' % ', '.join('"%s"' % n for n in NAMES)
    t, c = before_line(t, 'Case "room2blockhall"', fr, 'IndevFillS04(r)', nl)
    done.append(('MapSystem FillRoom', c))
    save('MapSystem.bb', t)

    t, nl = load('UpdateEvents.bb')
    ue = '\t\t\tCase "s04room"\n\t\t\t\t;[Block]\n\t\t\t\tUpdateIndevS04(e) ;Indev (IndevS04.bb)\n\t\t\t\t;[End Block]\n'
    t, c = before_line(t, 'Case "v02room"', ue, 'UpdateIndevS04(e)', nl)
    done.append(('UpdateEvents', c))
    save('UpdateEvents.bb', t)

    t, nl = load(r'Data\rooms.ini')
    if '[room2burn457]' not in t:
        add = open('b9_rooms.ini.txt').read()
        t = t.rstrip('\r\n') + nl + add.replace('\n', nl)
        done.append(('rooms.ini', True))
    save(r'Data\rooms.ini', t)

    t, nl = load(r'Data\items.ini')
    if '[doc457]' not in t:
        add = ''
        for n in sorted(TITLES):
            handwritten = n[-1] == 'b' and n != 'doc152b'
            add += ('\n[%s]\ngroup = paper\nmodel = GFX\\items\\paper.x\ninvicon = GFX\\items\\%s\ndocument = GFX\\items\\%s.jpg\nscale = 0.003\n%ssound = 0\n'
                    % (n, 'INVnote.png' if handwritten else 'INVpaper.png', n, 'texture override = GFX\\items\\notetexture.jpg\n' if handwritten else ''))
        t = t.rstrip('\r\n') + nl + add.replace('\n', nl)
        done.append(('items.ini', True))
    save(r'Data\items.ini', t)

    t, nl = load(r'Data\strings.ini')
    names = ''.join('%s = %s\n' % (k, TITLES[k]) for k in sorted(TITLES))
    t, c = after_line(t, 'doc956b = Cell 956 Night Log', names, 'doc457 = Document SCP-457', nl)
    done.append(('strings.ini', c))
    save(r'Data\strings.ini', t)

    for d in done:
        print(d)
