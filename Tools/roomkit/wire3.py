"""Hook the 24 v0.1-style rooms (IndevV01.bb + generated IndevV01Data.bb) into the game.
Run gen_v01.py first (it writes v01_names.txt and v01_rooms.ini.txt). Safe to run twice."""
import os
import shutil

ROOT = r"I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9"
NAMES = [l.strip() for l in open('v01_names.txt') if l.strip()]


def load(rel):
    raw = open(os.path.join(ROOT, rel), 'rb').read()
    nl = b'\r\n' if b'\r\n' in raw else b'\n'
    return raw.decode('latin-1'), nl.decode()


def save(rel, text):
    p = os.path.join(ROOT, rel)
    bak = p + '.bak_v01'
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
t, c = after_line(t, 'Include "IndevAnnex2.bb"', 'Include "IndevV01.bb"\nInclude "IndevV01Data.bb"\n', 'Include "IndevV01.bb"', nl)
done.append(('Main include', c))
t, c = after_line(t, 'CreateEvent("room1store4", "room1store4", 0)',
                  '\tIndevV01Events() ;Indev: the shared event of the 24 v0.1-style filler rooms (IndevV01.bb)\n', 'IndevV01Events()', nl)
done.append(('Main events', c))
save('Main.bb', t)

t, nl = load('MapSystem.bb')
names = ', '.join('"%s"' % n for n in NAMES)
fr = ('\t\tCase %s\n\t\t\t;[Block]\n\t\t\tIndevFillV01(r) ;Indev: v0.1-style filler rooms, table in IndevV01Data.bb\n\t\t\t;[End Block]\n' % names)
t, c = before_line(t, 'Case "room2blockhall"', fr, 'IndevFillV01(r)', nl)
done.append(('MapSystem FillRoom', c))
save('MapSystem.bb', t)

t, nl = load('UpdateEvents.bb')
ue = '\t\t\tCase "v01room"\n\t\t\t\t;[Block]\n\t\t\t\tUpdateIndevV01(e) ;Indev (IndevV01.bb)\n\t\t\t\t;[End Block]\n'
t, c = before_line(t, 'Case "room2blockhall"', ue, 'UpdateIndevV01(e)', nl)
done.append(('UpdateEvents', c))
save('UpdateEvents.bb', t)

t, nl = load(r'Data\rooms.ini')
if '[room2v_hall]' not in t:
    add = open('v01_rooms.ini.txt').read()
    t = t.rstrip('\r\n') + nl + add.replace('\n', nl)
    done.append(('rooms.ini', True))
save(r'Data\rooms.ini', t)

for d in done:
    print(d)
