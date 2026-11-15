"""Hook the ten "sixteen SCPs" rooms (IndevS16.bb + generated IndevS16Data.bb) into the game.
Run gen_s16.py --game first (it writes s16_names.txt and s16_rooms.ini.txt). Safe to run twice."""
import os
import shutil
from make_docs4 import TITLES

ROOT = r"I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9"
NAMES = [l.strip() for l in open('s16_names.txt') if l.strip()]
ALIASES = [('room2siv', ('siv', 'smallitems', '1045', '1510', '1125')),
           ('room2bio', ('bio', 'bioholding', '1513', '1515', '1517', '1519')),
           ('room2origin', ('origin', '1512')), ('room2purge', ('purge', 'fanhall', '1518')),
           ('room2review', ('review', '1110', '1250')), ('room2lecture', ('lecture', '1313')),
           ('room2site41', ('site41', '1312')), ('room2cell49', ('cell49', '1516')),
           ('room2vault117', ('vault117', '1511')), ('room2bunker', ('bunker', '1514'))]


def load(rel):
    raw = open(os.path.join(ROOT, rel), 'rb').read()
    nl = b'\r\n' if b'\r\n' in raw else b'\n'
    return raw.decode('latin-1'), nl.decode()


def save(rel, text):
    p = os.path.join(ROOT, rel)
    bak = p + '.bak_s16'
    if not os.path.exists(bak):
        shutil.copy2(p, bak)
    open(p, 'wb').write(text.encode('latin-1'))


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


done = []
t, nl = load('Main.bb')
t, c = after_line(t, 'Include "IndevV02Data.bb"', 'Include "IndevS16.bb"\nInclude "IndevS16Data.bb"\n', 'Include "IndevS16.bb"', nl)
done.append(('Main include', c))
t, c = after_line(t, 'IndevV02Events()', '\tIndevS16Events() ;Indev: the ten rooms of the sixteen-SCP batch (IndevS16.bb)\n', 'IndevS16Events()', nl)
done.append(('Main events', c))
al = ''
for room, keys in ALIASES:
    al += '\t\t\t\t\t\t\tCase %s\n\t\t\t\t\t\t\t\troomName = "%s"\n' % (', '.join('"%s"' % k for k in keys), room)
t, c = before_line(t, 'Case "blockhall", "blockd"', al, 'roomName = "room2siv"', nl)
done.append(('Main teleport aliases', c))
save('Main.bb', t)

t, nl = load('MapSystem.bb')
fr = '\t\tCase %s\n\t\t\t;[Block]\n\t\t\tIndevFillS16(r) ;Indev: sixteen-SCP rooms, table in IndevS16Data.bb\n\t\t\t;[End Block]\n' % ', '.join('"%s"' % n for n in NAMES)
t, c = before_line(t, 'Case "room2blockhall"', fr, 'IndevFillS16(r)', nl)
done.append(('MapSystem FillRoom', c))
save('MapSystem.bb', t)

t, nl = load('UpdateEvents.bb')
ue = '\t\t\tCase "s16room"\n\t\t\t\t;[Block]\n\t\t\t\tUpdateIndevS16(e) ;Indev (IndevS16.bb)\n\t\t\t\t;[End Block]\n'
t, c = before_line(t, 'Case "v02room"', ue, 'UpdateIndevS16(e)', nl)
done.append(('UpdateEvents', c))
save('UpdateEvents.bb', t)

t, nl = load(r'Data\rooms.ini')
if '[room2siv]' not in t:
    add = open('s16_rooms.ini.txt').read()
    t = t.rstrip('\r\n') + nl + add.replace('\n', nl)
    done.append(('rooms.ini', True))
save(r'Data\rooms.ini', t)

t, nl = load(r'Data\items.ini')
if '[doc1045]' not in t:
    add = ''
    for n in sorted(TITLES):
        if n.endswith('b'):
            add += ('\n[%s]\ngroup = paper\nmodel = GFX\\items\\paper.x\ninvicon = GFX\\items\\INVnote.png\n'
                    'document = GFX\\items\\%s.jpg\nscale = 0.003\ntexture override = GFX\\items\\notetexture.jpg\nsound = 0\n' % (n, n))
        else:
            add += ('\n[%s]\ngroup = paper\nmodel = GFX\\items\\paper.x\ninvicon = GFX\\items\\INVpaper.png\n'
                    'document = GFX\\items\\%s.jpg\nscale = 0.003\nsound = 0\n' % (n, n))
    t = t.rstrip('\r\n') + nl + add.replace('\n', nl)
    done.append(('items.ini', True))
save(r'Data\items.ini', t)

t, nl = load(r'Data\strings.ini')
names = ''.join('%s = %s\n' % (k, TITLES[k]) for k in sorted(TITLES))
t, c = after_line(t, 'doc999b = Stores 4 Issue Note', names, 'doc1045 = Document SCP-1045', nl)
done.append(('strings.ini', c))
save(r'Data\strings.ini', t)

for d in done:
    print(d)
