"""Hook the two rooms of batch 36 (IndevU36.bb + generated IndevU36Data.bb) into the game, with the notes and the
four candy items. Run make_assets36.py, make_hd36.py, make_docs36.py and gen_b36.py --game first.
Safe to run twice. Originals are kept once as *.bak_u36."""
from wire33 import load, after_line, before_line
import os
import shutil
from make_docs36 import TITLES, DOCS

ROOT = r"I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9"
ITEMS36 = ['gum1200', 'jar1916', 'pop3147', 'cotton1921']


def save(rel, text):
    p = os.path.join(ROOT, rel)
    bak = p + '.bak_u36'
    if not os.path.exists(bak):
        shutil.copy2(p, bak)
    open(p, 'wb').write(text.encode('latin-1'))


NAMES = [l.strip() for l in open('b36_names.txt') if l.strip()]
ALIASES = [('room2b36confect', ('confect', 'candy', '1200', '1916', '1921', '3147', '3409', 'bay3')),
           ('room2b36taiga', ('taiga', '1479b', 'cabin'))]

if __name__ == '__main__':
    done = []
    t, nl = load('Main.bb')
    t, c = after_line(t, 'Include "IndevU35Data.bb"', 'Include "IndevU36.bb"\nInclude "IndevU36Data.bb"\n', 'Include "IndevU36.bb"', nl)
    done.append(('Main include', c))
    t, c = after_line(t, 'IndevU35Events()', '\tIndevU36Events() ;Indev: batch 36, confectionery and SCP-1479 (IndevU36.bb)\n', 'IndevU36Events()', nl)
    done.append(('Main events', c))
    al = ''
    for room, keys in ALIASES:
        al += '\t\t\t\t\t\t\tCase %s\n\t\t\t\t\t\t\t\troomName = "%s"\n' % (', '.join('"%s"' % k for k in keys), room)
    t, c = before_line(t, 'Case "blockhall", "blockd"', al, 'roomName = "room2b36confect"', nl)
    done.append(('Main teleport aliases', c))
    t, c = before_line(t, 'Case "candy983_lum", "candy983_clear"',
                       '\t\t\t\tCase %s\n\t\t\t\t\t;[Block]\n\t\t\t\t\tIndevUse36(SelectedItem) ;Indev: batch 36 candy (IndevU36.bb)\n\t\t\t\t\t;[End Block]\n'
                       % ', '.join('"%s"' % n for n in ITEMS36), 'IndevUse36(SelectedItem)', nl)
    done.append(('Main item use', c))
    save('Main.bb', t)

    t, nl = load('MapSystem.bb')
    fr = ('\t\tCase %s\n\t\t\t;[Block]\n\t\t\tIndevFillU36(r) ;Indev: batch 36, table in IndevU36Data.bb\n\t\t\t;[End Block]\n'
          % ', '.join('"%s"' % n for n in NAMES))
    t, c = before_line(t, 'Case "room2blockhall"', fr, 'IndevFillU36(r)', nl)
    done.append(('MapSystem FillRoom', c))
    save('MapSystem.bb', t)

    t, nl = load('UpdateEvents.bb')
    ue = '\t\t\tCase "u36room"\n\t\t\t\t;[Block]\n\t\t\t\tUpdateIndevU36(e) ;Indev (IndevU36.bb)\n\t\t\t\t;[End Block]\n'
    t, c = before_line(t, 'Case "v02room"', ue, 'UpdateIndevU36(e)', nl)
    done.append(('UpdateEvents', c))
    save('UpdateEvents.bb', t)

    t, nl = load(r'Data\rooms.ini')
    if '[room2b36confect]' not in t:
        t = t.rstrip('\r\n') + nl + open('b36_rooms.ini.txt').read().replace('\n', nl)
        done.append(('rooms.ini', True))
    save(r'Data\rooms.ini', t)

    t, nl = load(r'Data\items.ini')
    if '[docb36_1200]' not in t:
        add = ''
        for n in DOCS:
            add += ('\n[%s]\ngroup = paper\nmodel = GFX\\items\\paper.x\ninvicon = GFX\\items\\INVpaper.png\n'
                    'document = GFX\\items\\%s.jpg\nscale = 0.003\nsound = 0\n' % (n, n))
        for n in ITEMS36:
            add += ('\n[%s]\ngroup = misc\nmodel = GFX\\items\\%s.b3d\ninvicon = GFX\\items\\INV%s.png\n'
                    'scale = 0.008\nsound = 2\n' % (n, n, n))
        t = t.rstrip('\r\n') + nl + add.replace('\n', nl)
        done.append(('items.ini', True))
    save(r'Data\items.ini', t)

    t, nl = load(r'Data\strings.ini')
    names = ''.join('%s = %s\n' % (k, TITLES[k]) for k in TITLES)
    t, c = after_line(t, 'docarea10p1 = ', names, 'docb36_1200 = ', nl)
    done.append(('strings.ini', c))
    save(r'Data\strings.ini', t)

    for d in done:
        print(d)
