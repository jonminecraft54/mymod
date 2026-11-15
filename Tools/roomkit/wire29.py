"""Hook the three rooms of batch 29 (IndevU29.bb + generated IndevU29Data.bb) into the game, with the notes and the
two items (scp820jp, herbicide867). Run make_assets29.py, make_scp820.py, make_docs29.py and gen_b29.py --game
first. Safe to run twice. Originals are kept once as *.bak_u29."""
import os
import shutil
from make_docs29 import TITLES, DOCS

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
    bak = p + '.bak_u29'
    if not os.path.exists(bak):
        shutil.copy2(p, bak)
    open(p, 'wb').write(text.encode('latin-1'))


NAMES = [l.strip() for l in open('b29_names.txt') if l.strip()]
ALIASES = [('room2b29blade', ('820', '820jp', 'scp820', 'blade')), ('room2b29spruce', ('867', 'scp867', 'spruce')),
           ('room2b29pool', ('120', 'scp120', 'pool', 'lunar', 'moon', 'area32'))]

if __name__ == '__main__':
    done = []
    t, nl = load('Main.bb')
    t, c = after_line(t, 'Include "IndevU28Data.bb"', 'Include "IndevU29.bb"\nInclude "IndevU29Data.bb"\n', 'Include "IndevU29.bb"', nl)
    done.append(('Main include', c))
    t, c = after_line(t, 'IndevU28Events()', '\tIndevU29Events() ;Indev: batch 29, SCP-820-JP / SCP-867 / SCP-120 (IndevU29.bb)\n', 'IndevU29Events()', nl)
    done.append(('Main events', c))
    al = ''
    for room, keys in ALIASES:
        al += '\t\t\t\t\t\t\tCase %s\n\t\t\t\t\t\t\t\troomName = "%s"\n' % (', '.join('"%s"' % k for k in keys), room)
    t, c = before_line(t, 'Case "blockhall", "blockd"', al, 'roomName = "room2b29pool"', nl)
    done.append(('Main teleport aliases', c))
    t, c = before_line(t, 'Case "candy983_lum", "candy983_clear"',
                       '\t\t\t\tCase "scp820jp", "herbicide867"\n\t\t\t\t\t;[Block]\n\t\t\t\t\tIndevUse29(SelectedItem) ;Indev: SCP-820-JP, the SCP-867 herbicide (IndevU29.bb)\n\t\t\t\t\t;[End Block]\n',
                       'IndevUse29(SelectedItem)', nl)
    done.append(('Main item use', c))
    save('Main.bb', t)

    t, nl = load('MapSystem.bb')
    fr = ('\t\tCase %s\n\t\t\t;[Block]\n\t\t\tIndevFillU29(r) ;Indev: batch 29, table in IndevU29Data.bb\n\t\t\t;[End Block]\n'
          % ', '.join('"%s"' % n for n in NAMES))
    t, c = before_line(t, 'Case "room2blockhall"', fr, 'IndevFillU29(r)', nl)
    done.append(('MapSystem FillRoom', c))
    save('MapSystem.bb', t)

    t, nl = load('UpdateEvents.bb')
    ue = '\t\t\tCase "u29room"\n\t\t\t\t;[Block]\n\t\t\t\tUpdateIndevU29(e) ;Indev (IndevU29.bb)\n\t\t\t\t;[End Block]\n'
    t, c = before_line(t, 'Case "v02room"', ue, 'UpdateIndevU29(e)', nl)
    done.append(('UpdateEvents', c))
    save('UpdateEvents.bb', t)

    t, nl = load(r'Data\rooms.ini')
    if '[room2b29pool]' not in t:
        add = open('b29_rooms.ini.txt').read()
        t = t.rstrip('\r\n') + nl + add.replace('\n', nl)
        done.append(('rooms.ini', True))
    save(r'Data\rooms.ini', t)

    t, nl = load(r'Data\items.ini')
    if '[doc820jp]' not in t:
        add = ''
        for n in sorted(DOCS):
            add += ('\n[%s]\ngroup = paper\nmodel = GFX\\items\\paper.x\ninvicon = GFX\\items\\INVpaper.png\n'
                    'document = GFX\\items\\%s.jpg\nscale = 0.003\nsound = 0\n' % (n, n))
        add += ('\n[scp820jp]\ngroup = misc\nmodel = GFX\\items\\scp820jp.b3d\ninvicon = GFX\\items\\INVscp820jp.png\n'
                'scale = 0.009\nsound = 2\n')
        add += ('\n[herbicide867]\ngroup = misc\nmodel = GFX\\items\\Syringe\\syringe.b3d\n'
                'invicon = GFX\\items\\INVherbicide867.png\nscale = 0.005\nsound = 2\n')
        t = t.rstrip('\r\n') + nl + add.replace('\n', nl)
        done.append(('items.ini', True))
    save(r'Data\items.ini', t)

    t, nl = load(r'Data\strings.ini')
    names = ''.join('%s = %s\n' % (k, TITLES[k]) for k in sorted(TITLES))
    t, c = after_line(t, 'candy983_black = ', names, 'doc820jp = ', nl)
    done.append(('strings.ini', c))
    save(r'Data\strings.ini', t)

    for d in done:
        print(d)
