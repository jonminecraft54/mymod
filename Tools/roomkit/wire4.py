"""Hook the 55 "w series" rooms (IndevV02.bb + generated IndevV02Data.bb) into the game.
Run gen_v02.py first (it writes v02_names.txt and v02_rooms.ini.txt). Safe to run twice."""
import os
import shutil

ROOT = r"I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9"
NAMES = [l.strip() for l in open('v02_names.txt') if l.strip()]


def load(rel):
    raw = open(os.path.join(ROOT, rel), 'rb').read()
    nl = b'\r\n' if b'\r\n' in raw else b'\n'
    return raw.decode('latin-1'), nl.decode()


def save(rel, text):
    p = os.path.join(ROOT, rel)
    bak = p + '.bak_v02'
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
t, c = after_line(t, 'Include "IndevV01Data.bb"', 'Include "IndevV02.bb"\nInclude "IndevV02Data.bb"\n', 'Include "IndevV02.bb"', nl)
done.append(('Main include', c))
t, c = after_line(t, 'IndevV01Events()', '\tIndevV02Events() ;Indev: the shared event of the 55 "w series" filler rooms (IndevV02.bb)\n', 'IndevV02Events()', nl)
done.append(('Main events', c))
save('Main.bb', t)

t, nl = load('MapSystem.bb')
fr = ''
for i in range(0, len(NAMES), 14):          # a few Case lines rather than one enormous one
    names = ', '.join('"%s"' % n for n in NAMES[i:i + 14])
    fr += '\t\tCase %s\n\t\t\t;[Block]\n\t\t\tIndevFillV02(r) ;Indev: "w series" filler rooms, table in IndevV02Data.bb\n\t\t\t;[End Block]\n' % names
t, c = before_line(t, 'Case "room2blockhall"', fr, 'IndevFillV02(r)', nl)
done.append(('MapSystem FillRoom', c))
save('MapSystem.bb', t)

t, nl = load('UpdateEvents.bb')
ue = '\t\t\tCase "v02room"\n\t\t\t\t;[Block]\n\t\t\t\tUpdateIndevV02(e) ;Indev (IndevV02.bb)\n\t\t\t\t;[End Block]\n'
t, c = before_line(t, 'Case "v01room"', ue, 'UpdateIndevV02(e)', nl)
done.append(('UpdateEvents', c))
save('UpdateEvents.bb', t)

# rare-item categories: IndevRoomTag falls back to the generated table
t, nl = load('IndevRareSpawn.bb')
if 'IndevV02Tag(n)' not in t:
    i = t.index('Function IndevRoomTag$(r.Rooms)')
    j = t.index('\tReturn ""' + nl + 'End Function', t.index('End Select', i))
    t = t[:j] + '\tReturn IndevV02Tag(n) ;Indev: the generated "w series" rooms carry their category in IndevV02Data.bb' + nl + t[j + len('\tReturn ""' + nl):]
    done.append(('IndevRareSpawn tag', True))
save('IndevRareSpawn.bb', t)

t, nl = load(r'Data\rooms.ini')
if '[room2w_narrow]' not in t:
    add = open('v02_rooms.ini.txt').read()
    t = t.rstrip('\r\n') + nl + add.replace('\n', nl)
    done.append(('rooms.ini', True))
save(r'Data\rooms.ini', t)

for d in done:
    print(d)
