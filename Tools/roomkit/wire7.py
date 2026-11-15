"""Hook the ten seventh-batch rooms (IndevS10.bb + generated IndevS10Data.bb) into the game.
Run gen_b7.py --game first (it writes b7_names.txt and b7_rooms.ini.txt). Safe to run twice.
Originals are kept once as *.bak_s10."""
import os
import shutil
from make_assets5 import TITLES

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
    bak = p + '.bak_s10'
    if not os.path.exists(bak):
        shutil.copy2(p, bak)
    open(p, 'wb').write(text.encode('latin-1'))


NAMES = [l.strip() for l in open('b7_names.txt') if l.strip()]
ALIASES = [('room2subway052', ('subway', '052', '59st', 'train')), ('room2hall99', ('hall99', '953', 'kennels')),
           ('room2gameshow', ('gameshow', '024', 'stage')), ('room2diner', ('diner', '4258', 'freddys')),
           ('room2sheet', ('sheet', '6096')), ('room2block15', ('block15', '2701', 'cell667')),
           ('room2mailbox', ('mailbox', '1269')), ('room2psych', ('psych', '482', 'straitjacket')),
           ('room2realchar', ('realchar', '3325', 'rci')), ('room2wait1440', ('oldman', '1440', 'int142'))]

if __name__ == '__main__':
    done = []
    t, nl = load('Main.bb')
    t, c = after_line(t, 'Include "IndevS13Data.bb"', 'Include "IndevS10.bb"\nInclude "IndevS10Data.bb"\n', 'Include "IndevS10.bb"', nl)
    done.append(('Main include', c))
    t, c = after_line(t, 'IndevS13Events()', '\tIndevS10Events() ;Indev: the ten rooms of the seventh batch, 10 SCPs (IndevS10.bb)\n', 'IndevS10Events()', nl)
    done.append(('Main events', c))
    al = ''
    for room, keys in ALIASES:
        al += '\t\t\t\t\t\t\tCase %s\n\t\t\t\t\t\t\t\troomName = "%s"\n' % (', '.join('"%s"' % k for k in keys), room)
    t, c = before_line(t, 'Case "blockhall", "blockd"', al, 'roomName = "room2subway052"', nl)
    done.append(('Main teleport aliases', c))
    save('Main.bb', t)

    t, nl = load('MapSystem.bb')
    fr = '\t\tCase %s\n\t\t\t;[Block]\n\t\t\tIndevFillS10(r) ;Indev: seventh-batch rooms, table in IndevS10Data.bb\n\t\t\t;[End Block]\n' % ', '.join('"%s"' % n for n in NAMES)
    t, c = before_line(t, 'Case "room2blockhall"', fr, 'IndevFillS10(r)', nl)
    done.append(('MapSystem FillRoom', c))
    save('MapSystem.bb', t)

    t, nl = load('UpdateEvents.bb')
    ue = '\t\t\tCase "s10room"\n\t\t\t\t;[Block]\n\t\t\t\tUpdateIndevS10(e) ;Indev (IndevS10.bb)\n\t\t\t\t;[End Block]\n'
    t, c = before_line(t, 'Case "v02room"', ue, 'UpdateIndevS10(e)', nl)
    done.append(('UpdateEvents', c))
    save('UpdateEvents.bb', t)

    t, nl = load(r'Data\rooms.ini')
    if '[room2subway052]' not in t:
        add = open('b7_rooms.ini.txt').read()
        t = t.rstrip('\r\n') + nl + add.replace('\n', nl)
        done.append(('rooms.ini', True))
    save(r'Data\rooms.ini', t)

    t, nl = load(r'Data\items.ini')
    if '[doc052]' not in t:
        add = ''
        for n in sorted(TITLES):
            handwritten = n[-1] in 'bc'
            add += ('\n[%s]\ngroup = paper\nmodel = GFX\\items\\paper.x\ninvicon = GFX\\items\\%s\ndocument = GFX\\items\\%s.jpg\nscale = 0.003\n%ssound = 0\n'
                    % (n, 'INVnote.png' if handwritten else 'INVpaper.png', n, 'texture override = GFX\\items\\notetexture.jpg\n' if handwritten else ''))
        t = t.rstrip('\r\n') + nl + add.replace('\n', nl)
        done.append(('items.ini', True))
    save(r'Data\items.ini', t)

    t, nl = load(r'Data\strings.ini')
    names = ''.join('%s = %s\n' % (k, TITLES[k]) for k in sorted(TITLES))
    t, c = after_line(t, 'doc971b = Cabinet 26 Order Log', names, 'doc052 = Document SCP-052', nl)
    done.append(('strings.ini', c))
    save(r'Data\strings.ini', t)

    for d in done:
        print(d)
