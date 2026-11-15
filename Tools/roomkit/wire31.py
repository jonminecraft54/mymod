"""Hook the three rooms of batch 31 (IndevU31.bb + generated IndevU31Data.bb) into the game, with the notes and the
two items (scp820jp, herbicide867). Run make_assets29.py, make_scp820.py, make_docs31.py and gen_b29.py --game
first. Safe to run twice. Originals are kept once as *.bak_u31."""
import os
import shutil
from make_docs31 import TITLES, DOCS

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
    bak = p + '.bak_u31'
    if not os.path.exists(bak):
        shutil.copy2(p, bak)
    open(p, 'wb').write(text.encode('latin-1'))


NAMES = [l.strip() for l in open('b31_names.txt') if l.strip()]
ALIASES = [('room2b31booth', ('467', 'scp467', 'booth', 'phonebooth')),
           ('room2b31items', ('178', '198', '207', '1079', '1650', 'itemwing'))]

if __name__ == '__main__':
    done = []
    t, nl = load('Main.bb')
    t, c = after_line(t, 'Include "IndevU30Data.bb"', 'Include "IndevU31.bb"\nInclude "IndevU31Data.bb"\n', 'Include "IndevU31.bb"', nl)
    done.append(('Main include', c))
    t, c = after_line(t, 'IndevU30Events()', '\tIndevU31Events() ;Indev: batch 31, SCP-467 and five items (IndevU31.bb)\n', 'IndevU31Events()', nl)
    done.append(('Main events', c))
    al = ''
    for room, keys in ALIASES:
        al += '\t\t\t\t\t\t\tCase %s\n\t\t\t\t\t\t\t\troomName = "%s"\n' % (', '.join('"%s"' % k for k in keys), room)
    t, c = before_line(t, 'Case "blockhall", "blockd"', al, 'roomName = "room2b31booth"', nl)
    done.append(('Main teleport aliases', c))
    t, c = before_line(t, 'Case "candy983_lum", "candy983_clear"',
                       '\t\t\t\tCase "scp178", "scp198", "scp207", "scp1079", "scp1650"\n\t\t\t\t\t;[Block]\n\t\t\t\t\tIndevUse31(SelectedItem) ;Indev: SCP-178/198/207/1079/1650 (IndevU31.bb)\n\t\t\t\t\t;[End Block]\n',
                       'IndevUse31(SelectedItem)', nl)
    done.append(('Main item use', c))
    save('Main.bb', t)

    t, nl = load('MapSystem.bb')
    fr = ('\t\tCase %s\n\t\t\t;[Block]\n\t\t\tIndevFillU31(r) ;Indev: batch 31, table in IndevU31Data.bb\n\t\t\t;[End Block]\n'
          % ', '.join('"%s"' % n for n in NAMES))
    t, c = before_line(t, 'Case "room2blockhall"', fr, 'IndevFillU31(r)', nl)
    done.append(('MapSystem FillRoom', c))
    save('MapSystem.bb', t)

    t, nl = load('UpdateEvents.bb')
    ue = '\t\t\tCase "u31room"\n\t\t\t\t;[Block]\n\t\t\t\tUpdateIndevU31(e) ;Indev (IndevU31.bb)\n\t\t\t\t;[End Block]\n'
    t, c = before_line(t, 'Case "v02room"', ue, 'UpdateIndevU31(e)', nl)
    done.append(('UpdateEvents', c))
    save('UpdateEvents.bb', t)

    t, nl = load(r'Data\rooms.ini')
    if '[room2b31booth]' not in t:
        add = open('b31_rooms.ini.txt').read()
        t = t.rstrip('\r\n') + nl + add.replace('\n', nl)
        done.append(('rooms.ini', True))
    save(r'Data\rooms.ini', t)

    t, nl = load(r'Data\items.ini')
    if '[doc467]' not in t:
        add = ''
        for n in sorted(DOCS):
            add += ('\n[%s]\ngroup = paper\nmodel = GFX\\items\\paper.x\ninvicon = GFX\\items\\INVpaper.png\n'
                    'document = GFX\\items\\%s.jpg\nscale = 0.003\nsound = 0\n' % (n, n))
        for n in ('scp178', 'scp198', 'scp207', 'scp1079', 'scp1650'):
            add += ('\n[%s]\ngroup = misc\nmodel = GFX\\items\\%s.b3d\ninvicon = GFX\\items\\INV%s.png\n'
                    'scale = %s\nsound = 2\n' % (n, n, n, '0.008'))
        t = t.rstrip('\r\n') + nl + add.replace('\n', nl)
        done.append(('items.ini', True))
    save(r'Data\items.ini', t)

    t, nl = load(r'Data\strings.ini')
    names = ''.join('%s = %s\n' % (k, TITLES[k]) for k in sorted(TITLES))
    t, c = after_line(t, 'phone4433 = ', names, 'doc467 = ', nl)
    done.append(('strings.ini', c))
    save(r'Data\strings.ini', t)

    for d in done:
        print(d)
