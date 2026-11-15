"""Hook the five eighth-batch rooms (IndevS08.bb + generated IndevS08Data.bb) into the game.
Run gen_b8.py --game first (it writes b8_names.txt and b8_rooms.ini.txt). Safe to run twice.
Originals are kept once as *.bak_s08."""
import os
import shutil
from make_assets6 import TITLES

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
    bak = p + '.bak_s08'
    if not os.path.exists(bak):
        shutil.copy2(p, bak)
    open(p, 'wb').write(text.encode('latin-1'))


NAMES = [l.strip() for l in open('b8_names.txt') if l.strip()]
ALIASES = [('room2yule', ('yule', '4y', '2983', '1933', '1225', '6895')), ('room2pinata', ('pinata', '956')),
           ('room2demoncore', ('demoncore', '095fr', '095-fr', '095')), ('room2argos', ('argos', '3355', 'stnick')),
           ('room2chrono', ('chrono', '4255', 'sleigh'))]

if __name__ == '__main__':
    done = []
    t, nl = load('Main.bb')
    t, c = after_line(t, 'Include "IndevS10Data.bb"', 'Include "IndevS08.bb"\nInclude "IndevS08Data.bb"\n', 'Include "IndevS08.bb"', nl)
    done.append(('Main include', c))
    t, c = after_line(t, 'IndevS10Events()', '\tIndevS08Events() ;Indev: the five rooms of the eighth batch, 8 SCPs (IndevS08.bb)\n', 'IndevS08Events()', nl)
    done.append(('Main events', c))
    al = ''
    for room, keys in ALIASES:
        al += '\t\t\t\t\t\t\tCase %s\n\t\t\t\t\t\t\t\troomName = "%s"\n' % (', '.join('"%s"' % k for k in keys), room)
    t, c = before_line(t, 'Case "blockhall", "blockd"', al, 'roomName = "room2yule"', nl)
    done.append(('Main teleport aliases', c))
    save('Main.bb', t)

    t, nl = load('MapSystem.bb')
    fr = '\t\tCase %s\n\t\t\t;[Block]\n\t\t\tIndevFillS08(r) ;Indev: eighth-batch rooms, table in IndevS08Data.bb\n\t\t\t;[End Block]\n' % ', '.join('"%s"' % n for n in NAMES)
    t, c = before_line(t, 'Case "room2blockhall"', fr, 'IndevFillS08(r)', nl)
    done.append(('MapSystem FillRoom', c))
    save('MapSystem.bb', t)

    t, nl = load('UpdateEvents.bb')
    ue = '\t\t\tCase "s08room"\n\t\t\t\t;[Block]\n\t\t\t\tUpdateIndevS08(e) ;Indev (IndevS08.bb)\n\t\t\t\t;[End Block]\n'
    t, c = before_line(t, 'Case "v02room"', ue, 'UpdateIndevS08(e)', nl)
    done.append(('UpdateEvents', c))
    save('UpdateEvents.bb', t)

    t, nl = load(r'Data\rooms.ini')
    if '[room2yule]' not in t:
        add = open('b8_rooms.ini.txt').read()
        t = t.rstrip('\r\n') + nl + add.replace('\n', nl)
        done.append(('rooms.ini', True))
    save(r'Data\rooms.ini', t)

    t, nl = load(r'Data\items.ini')
    if '[doc956]' not in t:
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
    t, c = after_line(t, 'doc953b = Hallway 99 Kennel Rules', names, 'doc956 = Document SCP-956', nl)
    done.append(('strings.ini', c))
    save(r'Data\strings.ini', t)

    for d in done:
        print(d)
