"""Hook the usable items of the fifteenth batch (IndevU15.bb) into the game: the four item templates, their names,
the include, the item-use cases in DrawGUI, and the per-frame tick in the main loop.
Run make_assets15.py first (textures and icons). Safe to run twice. Originals are kept once as *.bak_u15."""
import os
import shutil

ROOT = r"I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9"

ITEMS = [
    # name, group, display name
    ('cookie377', 'misc', 'Fortune Cookie'),
    ('camera978', 'misc', 'Desire Camera'),
    ('knife3041', 'misc', 'Rusted Knife'),
    ('sweater1337', 'misc', 'Red Sweater'),
]


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
    bak = p + '.bak_u15'
    if not os.path.exists(bak):
        shutil.copy2(p, bak)
    open(p, 'wb').write(text.encode('latin-1'))


if __name__ == '__main__':
    done = []
    t, nl = load('Main.bb')
    t, c = after_line(t, 'Include "IndevU14Data.bb"', 'Include "IndevU15.bb"\n', 'Include "IndevU15.bb"', nl)
    done.append(('Main include', c))
    t, c = after_line(t, 'If IndevTestOn Then IndevTestPose()', '\t\t\tIndevUsableTick() ;Indev: the knife dream comes on by itself (IndevU15.bb)\n', 'IndevUsableTick()', nl)
    done.append(('Main tick', c))
    block = ('\t\t\t\tCase "cookie377", "camera978", "knife3041", "sweater1337"\n'
             '\t\t\t\t\t;[Block]\n'
             '\t\t\t\t\tIndevUseU15(SelectedItem) ;Indev: the usable items of the thirteenth batch (IndevU15.bb)\n'
             '\t\t\t\t\t;[End Block]\n')
    t, c = before_line(t, 'Case "scp9097"', block, 'IndevUseU15(SelectedItem)', nl)
    done.append(('Main item use', c))
    save('Main.bb', t)

    t, nl = load(r'Data\items.ini')
    if '[cookie377]' not in t:
        add = ''
        for name, group, _ in ITEMS:
            add += ('\n[%s]\ngroup = %s\nmodel = GFX\\items\\paper.x\ninvicon = GFX\\items\\INV%s.png\n'
                    'texture override = GFX\\items\\%s.jpg\nscale = 0.003\n' % (name, group, name, name))
        t = t.rstrip('\r\n') + nl + add.replace('\n', nl)
        done.append(('items.ini', True))
    save(r'Data\items.ini', t)

    t, nl = load(r'Data\strings.ini')
    names = ''.join('%s = %s\n' % (n, d) for n, _, d in ITEMS)
    t, c = after_line(t, 'bulb = Lightbulb', names, 'cookie377 = ', nl)
    done.append(('strings.ini', c))
    save(r'Data\strings.ini', t)

    for d in done:
        print(d)
