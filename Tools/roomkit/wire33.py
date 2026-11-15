"""Hook the four rooms of batch 33 (IndevU33.bb + generated IndevU33Data.bb) into the game, with the notes and the
eight items. Run make_assets33.py, make_hd33.py, make_docs33.py and gen_b33.py --game first. Safe to run twice.
Originals are kept once as *.bak_u33."""
import os
import shutil
from make_docs33 import TITLES, DOCS

ROOT = r"I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9"
ITEMS33 = ['key1007', 'drive4876', 'book4890', 'zapper232', 'gun865', 'coin762', 'case667', 'book7042']


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
    bak = p + '.bak_u33'
    if not os.path.exists(bak):
        shutil.copy2(p, bak)
    open(p, 'wb').write(text.encode('latin-1'))


NAMES = [l.strip() for l in open('b33_names.txt') if l.strip()]
ALIASES = [('room2b33toys', ('1007', '3537', '3938', '4876', '4890', 'hall8', 'wondertainment')),
           ('room2b33archive', ('232', '252', '667', '696', '762', '865', 'site73')),
           ('room2b33bio', ('1563', '2394', '3419', '7042', '7284', 'site84')),
           ('room2b33deep', ('l043', '3743', '4612', '4712', '5079', '5512', '5267', 'site91', 'vault4612'))]

if __name__ == '__main__':
    done = []
    t, nl = load('Main.bb')
    t, c = after_line(t, 'Include "IndevU32Data.bb"', 'Include "IndevU33.bb"\nInclude "IndevU33Data.bb"\n', 'Include "IndevU33.bb"', nl)
    done.append(('Main include', c))
    t, c = after_line(t, 'IndevU32Events()', '\tIndevU33Events() ;Indev: batch 33, SCP storage and VAULT 4612 (IndevU33.bb)\n', 'IndevU33Events()', nl)
    done.append(('Main events', c))
    al = ''
    for room, keys in ALIASES:
        al += '\t\t\t\t\t\t\tCase %s\n\t\t\t\t\t\t\t\troomName = "%s"\n' % (', '.join('"%s"' % k for k in keys), room)
    t, c = before_line(t, 'Case "blockhall", "blockd"', al, 'roomName = "room2b33toys"', nl)
    done.append(('Main teleport aliases', c))
    t, c = before_line(t, 'Case "candy983_lum", "candy983_clear"',
                       '\t\t\t\tCase %s\n\t\t\t\t\t;[Block]\n\t\t\t\t\tIndevUse33(SelectedItem) ;Indev: batch 33 items (IndevU33.bb)\n\t\t\t\t\t;[End Block]\n'
                       % ', '.join('"%s"' % n for n in ITEMS33), 'IndevUse33(SelectedItem)', nl)
    done.append(('Main item use', c))
    save('Main.bb', t)

    t, nl = load('MapSystem.bb')
    fr = ('\t\tCase %s\n\t\t\t;[Block]\n\t\t\tIndevFillU33(r) ;Indev: batch 33, table in IndevU33Data.bb\n\t\t\t;[End Block]\n'
          % ', '.join('"%s"' % n for n in NAMES))
    t, c = before_line(t, 'Case "room2blockhall"', fr, 'IndevFillU33(r)', nl)
    done.append(('MapSystem FillRoom', c))
    save('MapSystem.bb', t)

    t, nl = load('UpdateEvents.bb')
    ue = '\t\t\tCase "u33room"\n\t\t\t\t;[Block]\n\t\t\t\tUpdateIndevU33(e) ;Indev (IndevU33.bb)\n\t\t\t\t;[End Block]\n'
    t, c = before_line(t, 'Case "v02room"', ue, 'UpdateIndevU33(e)', nl)
    done.append(('UpdateEvents', c))
    save('UpdateEvents.bb', t)

    t, nl = load(r'Data\rooms.ini')
    if '[room2b33toys]' not in t:
        add = open('b33_rooms.ini.txt').read()
        t = t.rstrip('\r\n') + nl + add.replace('\n', nl)
        done.append(('rooms.ini', True))
    save(r'Data\rooms.ini', t)

    t, nl = load(r'Data\items.ini')
    if '[doc1007]' not in t:
        add = ''
        for n in DOCS:
            add += ('\n[%s]\ngroup = paper\nmodel = GFX\\items\\paper.x\ninvicon = GFX\\items\\INVpaper.png\n'
                    'document = GFX\\items\\%s.jpg\nscale = 0.003\nsound = 0\n' % (n, n))
        for n in ITEMS33:
            add += ('\n[%s]\ngroup = misc\nmodel = GFX\\items\\%s.b3d\ninvicon = GFX\\items\\INV%s.png\n'
                    'scale = %s\nsound = 2\n' % (n, n, n, '0.008'))
        t = t.rstrip('\r\n') + nl + add.replace('\n', nl)
        done.append(('items.ini', True))
    save(r'Data\items.ini', t)

    t, nl = load(r'Data\strings.ini')
    names = ''.join('%s = %s\n' % (k, TITLES[k]) for k in TITLES)
    t, c = after_line(t, 'docgatev = ', names, 'doc1007 = ', nl)
    done.append(('strings.ini', c))
    save(r'Data\strings.ini', t)

    for d in done:
        print(d)
