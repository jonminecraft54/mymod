"""Hook the seven sixth-batch rooms (IndevS13.bb + generated IndevS13Data.bb) into the game.
Run gen_b6.py --game first (it writes b6_names.txt and b6_rooms.ini.txt). Safe to run twice."""
import os
import shutil
from make_assets4 import TITLES

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
NAMES = [l.strip() for l in open('b6_names.txt') if l.strip()]
ALIASES = [('room2scps4', ('cont4l', '4l', '1079', '1916', '1200', '971')),
           ('room2storage13', ('storage13', 'unit13', '1080', '1081', '1082', '1083')),
           ('room2beefbelly', ('beefbelly', 'canteen2', '2789')), ('room2grocery', ('grocery', 'aisle3', '3182')),
           ('room2testhouse', ('testhouse', 'salesman', '1879')), ('room2nagasaki', ('nagasaki', 'teddy', '1145')),
           ('room2ltstorage', ('ltstorage', 'kiosk', '1921'))]


def save(rel, text):
    p = os.path.join(ROOT, rel)
    bak = p + '.bak_s13'
    if not os.path.exists(bak):
        shutil.copy2(p, bak)
    open(p, 'wb').write(text.encode('latin-1'))


done = []
t, nl = load('Main.bb')
t, c = after_line(t, 'Include "IndevS16Data.bb"', 'Include "IndevS13.bb"\nInclude "IndevS13Data.bb"\n', 'Include "IndevS13.bb"', nl)
done.append(('Main include', c))
t, c = after_line(t, 'IndevS16Events()', '\tIndevS13Events() ;Indev: the seven rooms of the sixth batch, 13 SCPs (IndevS13.bb)\n', 'IndevS13Events()', nl)
done.append(('Main events', c))
al = ''
for room, keys in ALIASES:
    al += '\t\t\t\t\t\t\tCase %s\n\t\t\t\t\t\t\t\troomName = "%s"\n' % (', '.join('"%s"' % k for k in keys), room)
t, c = before_line(t, 'Case "blockhall", "blockd"', al, 'roomName = "room2scps4"', nl)
done.append(('Main teleport aliases', c))
save('Main.bb', t)

t, nl = load('MapSystem.bb')
fr = '\t\tCase %s\n\t\t\t;[Block]\n\t\t\tIndevFillS13(r) ;Indev: sixth-batch rooms, table in IndevS13Data.bb\n\t\t\t;[End Block]\n' % ', '.join('"%s"' % n for n in NAMES)
t, c = before_line(t, 'Case "room2blockhall"', fr, 'IndevFillS13(r)', nl)
done.append(('MapSystem FillRoom', c))
save('MapSystem.bb', t)

t, nl = load('UpdateEvents.bb')
ue = '\t\t\tCase "s13room"\n\t\t\t\t;[Block]\n\t\t\t\tUpdateIndevS13(e) ;Indev (IndevS13.bb)\n\t\t\t\t;[End Block]\n'
t, c = before_line(t, 'Case "v02room"', ue, 'UpdateIndevS13(e)', nl)
done.append(('UpdateEvents', c))
save('UpdateEvents.bb', t)

t, nl = load(r'Data\rooms.ini')
if '[room2scps4]' not in t:
    add = open('b6_rooms.ini.txt').read()
    t = t.rstrip('\r\n') + nl + add.replace('\n', nl)
    done.append(('rooms.ini', True))
save(r'Data\rooms.ini', t)

t, nl = load(r'Data\items.ini')
if '[doc1079]' not in t:
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
t, c = after_line(t, 'doc1519b = Lamplighter Feeding Rota', names, 'doc1079 = Document SCP-1079', nl)
done.append(('strings.ini', c))
save(r'Data\strings.ini', t)

for d in done:
    print(d)
